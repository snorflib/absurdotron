import typing

import attrs

from src import memoptix
from src.ir import tokens
from src.xbf import dtypes, program

from .assign import AssignUnit
from .base import BaseCommand
from .callz import CallZ
from .clear import ClearUnit
from .copy import CopyUnit
from .init import Init
from .sub import Sub


def _callge(
    left: dtypes.Unit,
    right: dtypes.Unit,
    if_: typing.Iterable[BaseCommand] | None,
    else_: typing.Iterable[BaseCommand] | None,
    program: program.Program,
) -> None:
    else_flag, true_flag = dtypes.Unit(), dtypes.Unit()
    right_buffer, left_buffer = dtypes.Unit(), dtypes.Unit()

    Init(else_flag)(program)
    Init(true_flag)(program)
    Init(right_buffer)(program)
    Init(left_buffer)(program)

    CopyUnit(left, left_buffer)(program)
    CopyUnit(right, right_buffer)(program)

    program.routine.extend(
        [
            tokens.EnterLoop(right_buffer),
            tokens.Decrement(right_buffer),
        ]
    )
    CallZ(
        left_buffer,
        else_=[ClearUnit(right_buffer), AssignUnit(else_flag, 1)],
        if_=[Sub(left_buffer, 1, left_buffer)],
    )(program)
    program.routine.append(tokens.ExitLoop())

    program.routine.extend(
        [
            tokens.Increment(true_flag),
            tokens.EnterLoop(else_flag),
            tokens.Decrement(true_flag),
            tokens.Decrement(else_flag),
        ]
    )

    for command in else_ or []:
        command(program)

    program.routine.extend(
        [
            tokens.ExitLoop(),
            #
            tokens.EnterLoop(true_flag),
            tokens.Decrement(true_flag),
        ]
    )

    for command in if_ or []:
        command(program)

    program.routine.extend(
        [
            tokens.ExitLoop(),
            #
            memoptix.Free(else_flag),
            memoptix.Free(true_flag),
            memoptix.Free(left_buffer),
            memoptix.Free(right_buffer),
        ]
    )


@attrs.frozen
class CallGE(BaseCommand):
    left: dtypes.Unit
    right: dtypes.Unit
    if_: typing.Iterable[BaseCommand] | None = None
    else_: typing.Iterable[BaseCommand] | None = None

    def _apply(self, context: program.Program) -> None:
        _callge(self.left, self.right, self.if_, self.else_, context)
