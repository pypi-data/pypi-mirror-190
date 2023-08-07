import collections
import typing
import warnings


def is_instance(value, type_):
    if type_ == typing.Any:
        return True

    if type_ is None and value is None:
        return True

    if isinstance(type_, tuple):
        return any(is_instance(value, t) for t in type_)

    if isinstance(type_, typing._UnionGenericAlias):
        return _check_union_generic_alias(value, type_)

    if hasattr(type_, "__origin__"):
        return _check_generic_alias(value, type_)

    try:
        return isinstance(value, type_)
    except TypeError:
        warnings.warn(
            RuntimeError(
                f"Don't know how to check if value is of type {type_} {type_.__class__}. This is probably a bug in pytest_runtime_types."
            )
        )
        return True


def _check_union_generic_alias(value, type_):
    union_types = tuple(type_.__args__)
    return is_instance(value, union_types)


def _check_generic_alias(value, type_):
    if issubclass(type_.__origin__, collections.abc.Mapping):
        return is_instance(value, type_.__origin__) and _check_mapping(
            value, *type_.__args__
        )

    if issubclass(type_.__origin__, collections.abc.Iterable):
        return is_instance(value, type_.__origin__) and _check_iterable(
            value, type_.__args__
        )


def _check_iterable(value, type_):
    return all(is_instance(v, type_) for v in value)


def _check_mapping(value, key_type, value_type):
    for key in value:
        if not is_instance(key, key_type):
            return False
        if not is_instance(value[key], value_type):
            return False
    return True
