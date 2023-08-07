import inspect
import warnings
from dataclasses import dataclass
from itertools import groupby
from os import path
from typing import Any, Type, Union

from .type_checker import is_instance


@dataclass(frozen=True)
class TypeMismatch:
    function_name: str
    file_name: str
    line_number: int

    def to_report_header(self):
        return f"""Function name: {self.function_name}
Called in: {self.file_name}:{self.line_number}
"""


@dataclass(frozen=True)
class ArgumentTypeError(TypeMismatch):
    argument_name: str
    argument_value: Any
    argument_type: Type[Any]
    expected_type: Type[Any]

    def to_report(self):
        return f"""    Type mismatch in argument:
        name: {self.argument_name}
        value: {self.argument_value}
        type: {self.argument_type}
        expected type: {self.expected_type}
"""


@dataclass(frozen=True)
class ReturnTypeError(TypeMismatch):
    return_value: Any
    return_type: Type[Any]
    expected_type: Type[Any]

    def to_report(self):
        return f"""    Type mismatch in return:
        value: {self.return_value}
        type: {self.return_type}
        expected type: {self.expected_type}
"""


class TypeCollector:
    def __init__(self):
        self.frames = []
        self.sources = []

    def get_function_from_frame(self, frame):
        func_name = frame.f_code.co_name

        if func_name in frame.f_locals:
            return frame.f_locals[func_name], func_name

        if func_name in frame.f_globals:
            return frame.f_globals[func_name], func_name

        if func_name in frame.f_builtins:
            return frame.f_builtins[func_name], func_name

        if "self" in frame.f_locals and hasattr(frame.f_locals["self"], func_name):
            friendly_func_name = (
                f"{frame.f_locals['self'].__class__.__name__}.{func_name}"
            )
            return getattr(frame.f_locals["self"], func_name), friendly_func_name

        if "cls" in frame.f_locals and hasattr(frame.f_locals["cls"], func_name):
            friendly_func_name = f"{frame.f_locals['cls'].__name__}.{func_name}"
            return getattr(frame.f_locals["cls"], func_name), friendly_func_name

        return None

    def trace_func(self, frame, event, arg):
        if event in ("return", "call", "c_call"):
            filename = frame.f_back.f_code.co_filename
            if not self.is_file_in_sources(filename):
                return
            lineno = frame.f_back.f_lineno

            called_func = self.get_function_from_frame(frame)
            if not called_func:
                warnings.warn(
                    RuntimeError(
                        f"Cannot determine called function object in {filename}:{lineno}. This is probably a bug in pytest_runtime_types."
                    )
                )
                return

            function, func_name = called_func

            try:
                annotations = inspect.get_annotations(function, eval_str=True)
            except TypeError:
                return

            call_args = inspect.getargvalues(frame)
            self.frames.append(
                {
                    "event": event,
                    "ret_value": arg,
                    "frame": frame,
                    "called_in_file": filename,
                    "called_in_lineno": lineno,
                    "func": function,
                    "func_name": func_name,
                    "annotations": annotations,
                    "call_args": call_args,
                }
            )

    def get_typing_errors(self):
        for f in self.frames:
            event = f["event"]
            func = f["func"]
            func_name = f["func_name"]
            call_args = f["call_args"]
            annotations = f["annotations"]
            ret_value = f["ret_value"]

            filename = f["called_in_file"]
            lineno = f["called_in_lineno"]

            for arg_name, arg_value in call_args.locals.items():
                if arg_name in annotations:
                    if not is_instance(arg_value, annotations[arg_name]):
                        yield ArgumentTypeError(
                            func_name,
                            filename,
                            lineno,
                            arg_name,
                            arg_value,
                            arg_value.__class__,
                            annotations[arg_name],
                        )

            if event == "return":
                if "return" in annotations:
                    return_annotation = annotations["return"]
                    if inspect.isgeneratorfunction(func):
                        # @TODO check if annotation is Generator[x,y,z]
                        args = return_annotation.__args__
                        if len(args) == 3:
                            warnings.warn(
                                RuntimeError(
                                    f"Invalid generator function annotation in {filename}:{lineno}."
                                )
                            )

                        return_type = Union[
                            args[0] if len(args) >= 1 else Any,
                            args[1] if len(args) >= 2 else Any,
                        ]
                    else:
                        # @TODO check if annotation is NOT Generator[x,y,z]
                        return_type = return_annotation

                    if not is_instance(ret_value, return_type):
                        yield ReturnTypeError(
                            func_name,
                            filename,
                            lineno,
                            ret_value,
                            ret_value.__class__,
                            annotations["return"],
                        )

    def raise_type_errors(self):
        for e in self.get_typing_errors():
            raise e

    def is_file_in_sources(self, filename):
        if not self.sources:
            return True

        for source in self.sources:
            if self.is_in_path(filename, source):
                return True
        return False

    def is_in_path(self, filename, directory):
        filename = path.realpath(filename)
        directory = path.realpath(directory)
        return path.commonprefix([filename, directory]) == directory

    def error_report(self):
        grouping_function = lambda e: (e.function_name, e.file_name, e.line_number)
        grouped_errors = groupby(set(self.get_typing_errors()), grouping_function)

        reports = []

        for _, error_group in grouped_errors:
            error_group = list(error_group)
            report = error_group[0].to_report_header()
            report += "".join(map(lambda e: e.to_report(), error_group))
            reports.append(report)

        if not reports:
            return None

        return "\n\n".join(reports)
