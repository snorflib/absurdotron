import typing
import uuid

import attrs

from src import memoptix
from src.ir import tokens
from src.memoptix import constraints
from src.xbf import dtypes, program

from .base import BaseCommand
from .init_unit import InitUnit


def _callz(
    subject: dtypes.Unit,
    if_: typing.Iterable[BaseCommand] | None,
    else_: typing.Iterable[BaseCommand] | None,
    program: program.Program,
) -> None:
    else_flag, zero_flag = dtypes.Unit(), dtypes.Unit()
    InitUnit(else_flag)(program)
    InitUnit(zero_flag)(program)

    hash = uuid.uuid4().int
    program.constr.append(constraints.LinkedConstraint(subject, else_flag, 1, hash))
    program.constr.append(constraints.LinkedConstraint(subject, zero_flag, 2, hash))

    program.routine.extend(
        [
            tokens.Increment(else_flag),
            tokens.EnterLoop(subject),
        ]
    )
    for command in if_ or []:
        command(program)

    program.routine.extend(
        [
            tokens.CodeInjection(owner=else_flag, value="-", end_owner=subject),
            tokens.ExitLoop(),
            tokens.EnterLoop(else_flag),
            tokens.Decrement(else_flag),
        ]
    )
    for command in else_ or []:
        command(program)

    program.routine.extend(
        [
            tokens.CodeInjection(owner=zero_flag, value="", end_owner=else_flag),
            tokens.ExitLoop(),
            tokens.CodeInjection(owner=else_flag, value="", end_owner=zero_flag),
        ]
    )

    program.routine.extend(
        [
            memoptix.Free(else_flag),
            memoptix.Free(zero_flag),
        ]
    )


@attrs.frozen
class CallZ(BaseCommand):
    subject: dtypes.Unit
    if_: typing.Iterable[BaseCommand] | None = None
    else_: typing.Iterable[BaseCommand] | None = None

    def _apply(self, context: program.Program) -> None:
        _callz(self.subject, self.if_, self.else_, context)
