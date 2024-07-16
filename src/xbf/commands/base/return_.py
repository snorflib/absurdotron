from __future__ import annotations

import typing

import attrs

from src.ir import tokens
from src.memoptix import constraints


@attrs.frozen
class CommandReturn:
    _constrs: list[constraints.BaseConstraint] = attrs.field(factory=list)
    _routine: list[tokens.BFToken] = attrs.field(factory=list)

    def __or__(self, other: CommandReturn | constraints.BaseConstraint | tokens.BFToken) -> typing.Self:
        match other:
            case CommandReturn():
                self._constrs.extend(other._constrs)
                self._routine.extend(other._routine)
            case constraints.BaseConstraint():
                self._constrs.append(other)
            case tokens.BFToken():
                self._routine.append(other)
            case _:
                raise ValueError(
                    f"Trying to merge {type(self)!r} with unexpected " f"value {other!r} of type {type(other)!r}."
                )

        return self

    def __repr__(self) -> str:
        return f"{type(self).__name__} -> {len(self._constrs)} constraints : {len(self._routine)} tokens"
