import typing

import pytest

from pytest_runtime_types.type_checker import is_instance

_ints = (123, 0, -123)
_floats = (-12.3, 0.0, 12.3)
_strs = ("a", "b", "cde", "asdf")
_others = (object(),)

_none = (None,)
_empty_list = ([],)
_empty_tuple = ((),)
_empty_dict = ({},)
_empty_set = (set(),)

_lists_of_ints = (
    [1],
    [2, 3],
)
_tuples_of_ints = (
    (1,),
    (2, 3),
)
_sets_of_ints = (
    {1},
    {2, 3},
)
_dicts_str_to_int = (
    {"a": 1, "b": 123},
    {"a": 2},
)

_all_cases = (
    _ints
    + _floats
    + _strs
    + _others
    + _lists_of_ints
    + _tuples_of_ints
    + _sets_of_ints
    + _dicts_str_to_int
    + _none
    + _empty_list
    + _empty_tuple
    + _empty_dict
    + _empty_set
)


test_cases = (
    (typing.Any, _all_cases),
    (str, _strs),
    (int, _ints),
    (typing.Union[int, float], _ints + _floats),
    (typing.Optional[typing.Union[int, float]], _ints + _floats + _none),
    (typing.Optional[int], _ints + _none),
    (typing.List[int], _lists_of_ints + _empty_list),
    (typing.Tuple[int], _tuples_of_ints + _empty_tuple),
    (typing.Set[int], _sets_of_ints + _empty_set),
    (typing.Dict[str, int], _dicts_str_to_int + _empty_dict),
    (list[int], _lists_of_ints + _empty_list),
    (tuple[int], _tuples_of_ints + _empty_tuple),
    (set[int], _sets_of_ints + _empty_set),
    (dict[str, int], _dicts_str_to_int + _empty_dict),
)


unwrapped_test_cases = []
for annotation, valid_cases in test_cases:
    assert not list(
        c for c in valid_cases if c not in _all_cases
    ), "_all_cases variable should contain all test cases"
    invalid_cases = (c for c in _all_cases if c not in valid_cases)
    unwrapped_test_cases.extend([(annotation, tc, True) for tc in valid_cases])
    unwrapped_test_cases.extend([(annotation, tc, False) for tc in invalid_cases])


@pytest.mark.parametrize("annotation,value,expected", unwrapped_test_cases)
def test_is_insance(annotation, value, expected):
    assert is_instance(value, annotation) == expected
