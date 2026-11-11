from typing import Any
from datetime import datetime


def type_check(obj: Any, expected_type: type | tuple[type, ...], object_name: str):
    if not isinstance(expected_type, tuple):
        expected_type = (expected_type,)

    if not isinstance(obj, expected_type):
        raise TypeError(
            f"Object {object_name} "
            f"must by of type {' or '.join([t.__name__ for t in expected_type])} "
            f"not {type(obj).__name__}"
        )


def value_check_within(obj: float | int, min: float, max: float, object_name: str):
    if min > obj or max < obj:
        raise ValueError(
            f"Object {object_name} must be in range <{min}, {max}>. Not: {obj}"
        )


def value_check_greater_than(obj: float | int, val_min: float | int, object_name: str):
    if obj < val_min:
        raise ValueError(
            f"Object {object_name} = {obj} must be greater than {val_min} "
        )


if __name__ == "__main__":
    type_check(obj="a", expected_type=int, object_name="a")
