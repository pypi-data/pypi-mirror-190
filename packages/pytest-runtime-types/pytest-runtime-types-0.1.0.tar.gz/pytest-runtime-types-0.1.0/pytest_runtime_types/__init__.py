# -*- coding: utf-8 -*-

import sys
from os import path
from typing import Generator, List

import pytest

from .collector import TypeCollector

with open(path.join(path.dirname(__file__), "VERSION"), encoding="utf-8") as f:
    __version__ = f.read().strip()

__author__ = "Wiktor Latanowicz"


class TypingError(pytest.fail.Exception):
    pass


def fail(reason):
    raise TypingError(reason)


fail.Exception = TypingError


def pytest_addoption(parser):
    group = parser.getgroup("runtime-types")
    group.addoption(
        "--source",
        action="store",
        dest="source",
        nargs="*",
        default=(),
        help="Limits runtime type checking to given source dir.",
    )


@pytest.hookimpl()
def pytest_load_initial_conftests(
    early_config,
    parser,
    args: List[str],
) -> None:
    early_config.addinivalue_line(
        "markers", "runtime_types(): check values against annotation in runtime"
    )


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_call(item: pytest.Item) -> Generator[None, None, None]:
    marker = item.get_closest_marker("runtime_types")
    if not marker:
        yield
        return

    collector = TypeCollector()

    for source in item.config.option.source:
        collector.sources.append(source)

    sys.setprofile(collector.trace_func)
    sys.settrace(collector.trace_func)

    yield

    sys.settrace(None)
    sys.setprofile(None)

    error_report = collector.error_report()
    if error_report:
        error_report = f"Function argument and/or return value do not match annotations.\n\n{error_report}"
        fail(error_report)
