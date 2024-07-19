from __future__ import annotations

import typing

import attrs

from src.ir import tokens
from src.memoptix import constraints

T = typing.TypeVar("T")


@attrs.define
class CommandReturn:
    _constrs: list[constraints.BaseConstraint] = attrs.field(factory=list)
    _routine: list[tokens.BFToken] = attrs.field(factory=list)

    def __ror__(self, other: constraints.BaseConstraint | tokens.BFToken) -> typing.Self:
        self._insert(other, False)
        return self

    def __or__(self, other: constraints.BaseConstraint | tokens.BFToken | CommandReturn) -> typing.Self:
        if isinstance(other, CommandReturn):
            self._constrs.extend(other._constrs)
            self._routine.extend(other._routine)
        else:
            self._insert(other)
        return self

    def _insert(
        self, other: CommandReturn | constraints.BaseConstraint | tokens.BFToken, at_the_end: bool = True
    ) -> None:
        if at_the_end:

            def _add_item(list_: list[T], item: T) -> None:
                list_.append(item)
        else:

            def _add_item(list_: list[T], item: T) -> None:
                list_.insert(0, item)

        match other:
            case constraints.BaseConstraint():
                _add_item(self._constrs, other)
            case tokens.BFToken():
                _add_item(self._routine, other)
            case _:
                raise ValueError(
                    f"Trying to merge {type(self)!r} with unexpected value {other!r} of type {type(other)!r}."
                )

    def __repr__(self) -> str:
        return f"{type(self).__name__} -> {len(self._constrs)} constraints : {len(self._routine)} tokens"
