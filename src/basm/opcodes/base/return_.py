from __future__ import annotations

import typing

import attrs

from src import ir, memoptix


@attrs.define
class OpCodeReturn:
    routine: list[ir.BFToken] = attrs.field(factory=list)
    constrs: list[memoptix.BaseConstraint] = attrs.field(factory=list)

    def __or__(self, other: OpCodeReturn | memoptix.BaseConstraint | ir.BFToken) -> typing.Self:
        match other:
            case OpCodeReturn():
                self.routine.extend(other.routine)
                self.constrs.extend(other.constrs)
            case memoptix.BaseConstraint():
                self.constrs.append(other)
            case ir.BFToken():
                self.routine.append(other)
            case _:
                raise ValueError(
                    f"Trying to merge {type(self)!r} with unexpected value {other!r} of type {type(other)!r}."
                )
        return self

    def __repr__(self) -> str:
        return f"{type(self).__name__} -> {len(self.constrs)} constraints : {len(self.routine)} tokens"
