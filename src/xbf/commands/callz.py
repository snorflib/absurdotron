import typing

import attrs

from src import memoptix
from src.ir import tokens
from src.xbf import dtypes, program

from .base import BaseCommand
from .init import Init
from .move import MoveUnit


def _callz(
    subject: dtypes.Unit,
    if_: typing.Iterable[BaseCommand] | None,
    else_: typing.Iterable[BaseCommand] | None,
    program: program.Program,
) -> None:
    else_flag, buffer = dtypes.Unit(), dtypes.Unit()

    Init(else_flag)(program)
    Init(buffer)(program)

    MoveUnit(subject, [(buffer, 1)])(program)
    program.routine.extend(
        [
            tokens.Increment(else_flag),
            tokens.EnterLoop(buffer),
        ]
    )
    MoveUnit(buffer, [(subject, 1)])(program)

    for command in if_ or []:
        command(program)

    program.routine.extend(
        [
            tokens.Decrement(else_flag),
            tokens.ExitLoop(),
            #
            tokens.EnterLoop(else_flag),
            tokens.Decrement(else_flag),
        ]
    )

    for command in else_ or []:
        command(program)

    program.routine.extend(
        [
            tokens.ExitLoop(),
            #
            memoptix.Free(else_flag),
            memoptix.Free(buffer),
        ]
    )


@attrs.frozen
class CallZ(BaseCommand):
    subject: dtypes.Unit
    if_: typing.Iterable[BaseCommand] | None = None
    else_: typing.Iterable[BaseCommand] | None = None

    def _apply(self, context: program.Program) -> None:
        _callz(self.subject, self.if_, self.else_, context)
