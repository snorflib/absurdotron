import typing

import attrs

from src import memoptix
from src.ir import tokens
from src.xbf import dtypes, program

from .base import BaseCommand
from .init_unit import InitUnit
from .migrate import MigrateUnit


def _callz(
    subject: dtypes.Unit,
    if_: typing.Iterable[BaseCommand] | None,
    else_: typing.Iterable[BaseCommand] | None,
    program: program.Program,
) -> None:
    else_flag, zero_flag, buffer = dtypes.Unit(), dtypes.Unit(), dtypes.Unit()

    InitUnit(else_flag)(program)
    InitUnit(zero_flag)(program)
    InitUnit(buffer)(program)

    MigrateUnit(subject, [(buffer, 1)])(program)
    program.routine.extend(
        [
            tokens.Increment(else_flag),
            tokens.EnterLoop(buffer),
        ]
    )
    for command in if_ or []:
        command(program)

    MigrateUnit(buffer, [(subject, 1)])(program)

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
        ]
    )

    program.routine.extend(
        [
            memoptix.Free(else_flag),
            memoptix.Free(zero_flag),
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
