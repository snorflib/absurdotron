from __future__ import annotations

import functools
import typing

from src import ir, memoptix

from .return_ import OpCodeReturn

ToConvert = OpCodeReturn | memoptix.BaseConstraint | ir.BFToken | typing.Iterable[ToConvert]


def _convert(data: ToConvert) -> OpCodeReturn:
    match data:
        case OpCodeReturn():
            return data
        case memoptix.BaseConstraint():
            return OpCodeReturn([], [data])
        case ir.BFToken():
            return OpCodeReturn([data], [])
        case typing.Iterable():
            base_ = OpCodeReturn()
            for to_conv in data:
                base_ |= _convert(to_conv)
            return base_
        case _:
            raise ValueError(f"Trying to cast an unsupported data to OpCodeReturn. {type(data).__name__}: {data}")


P = typing.ParamSpec("P")
R = typing.TypeVar("R", bound=ToConvert)


def to_convert(func: typing.Callable[P, R]) -> typing.Callable[P, OpCodeReturn]:
    @functools.wraps(func)
    def _wrapper(*args: P.args, **kwargs: P.kwargs) -> OpCodeReturn:
        return _convert(func(*args, **kwargs))

    return _wrapper
