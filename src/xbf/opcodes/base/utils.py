from __future__ import annotations

import collections
import functools
import typing

from src.ir import tokens
from src.memoptix import constraints

from .return_ import CommandReturn

P = typing.ParamSpec("P")
type ToFlatten = typing.Optional[  # type: ignore
    typing.Iterable["ToFlatten"] | tokens.BFToken | CommandReturn | constraints.BaseConstraint
]


def flatten2return(
    function: typing.Callable[P, ToFlatten],
) -> typing.Callable[P, CommandReturn]:
    CR = CommandReturn

    def _flatten(to_flatten: ToFlatten) -> CommandReturn:
        match to_flatten:
            case tokens.BFToken():
                return CR([], [to_flatten])
            case constraints.BaseConstraint():
                return CR([to_flatten], [])
            case collections.abc.Iterable():
                default = CR()
                for item in to_flatten:
                    default |= _flatten(item)
                return default
            case CommandReturn():
                return to_flatten
            case None:
                return CommandReturn()

        raise ValueError(
            f"During flattening encountered an unexpected value {to_flatten!r} of type {type(to_flatten)!r}"
        )

    @functools.wraps(function)
    def _wrapper(*args: P.args, **kwargs: P.kwargs) -> CommandReturn:
        return _flatten(function(*args, **kwargs))

    return _wrapper
