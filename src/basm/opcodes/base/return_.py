from __future__ import annotations

import collections.abc
import functools
import typing

import attrs

from src import ir, memoptix


@attrs.define
class OpCodeReturn:
    routine: list[ir.BFToken] = attrs.field(factory=list)
    constrs: list[memoptix.BaseConstraint] = attrs.field(factory=list)

    def __or__(self, other: ToConvert) -> typing.Self:
        if isinstance(other, OpCodeReturn):
            self.routine.extend(other.routine)
            self.constrs.extend(other.constrs)
            return self

        return self | _to_opcode_return(other)

    def __repr__(self) -> str:
        return f"{type(self).__name__} -> {len(self.constrs)} constraints : {len(self.routine)} tokens"


ToConvert = None | OpCodeReturn | memoptix.BaseConstraint | ir.BFToken | collections.abc.Iterable["ToConvert"]

P = typing.ParamSpec("P")
R = typing.TypeVar("R", bound=ToConvert)


def _to_opcode_return(data: ToConvert) -> OpCodeReturn:
    match data:
        case OpCodeReturn():
            return data
        case memoptix.BaseConstraint():
            return OpCodeReturn([], [data])
        case ir.BFToken():
            return OpCodeReturn([data], [])
        case collections.abc.Iterable():
            base_ = OpCodeReturn()
            for to_conv in data:
                base_ |= _to_opcode_return(to_conv)
            return base_
        case None:
            return OpCodeReturn()
        case _:
            raise ValueError(f"Trying to cast an unsupported data to OpCodeReturn. {type(data).__name__}: {data}")


def convert(func: typing.Callable[P, R]) -> typing.Callable[P, OpCodeReturn]:
    @functools.wraps(func)
    def _wrapper(*args: P.args, **kwargs: P.kwargs) -> OpCodeReturn:
        return _to_opcode_return(func(*args, **kwargs))

    return _wrapper
