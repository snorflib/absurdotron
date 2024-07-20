import attrs

from src import memoptix
from src.ir import tokens
from src.xbf import dtypes, program

from . import base
from .init import init
from .move import move


@attrs.frozen
class CallZ(base.BaseCommand):
    arg: dtypes.Unit
    if_: base.CommandReturn | None = None
    else_: base.CommandReturn | None = None

    def _apply(self, context: program.Program) -> base.CommandReturn:
        return callz(self.arg, self.if_, self.else_)


@base.flatten2return
def callz(
    arg: dtypes.Unit,
    if_: base.CommandReturn | None = None,
    else_: base.CommandReturn | None = None,
) -> base.CommandReturn:
    else_flag, buffer = dtypes.Unit(), dtypes.Unit()

    instrs = base.CommandReturn()
    instrs |= init(else_flag) | init(buffer)

    instrs |= move(arg, [(buffer, 1)])
    instrs |= tokens.Increment(else_flag)
    instrs |= tokens.EnterLoop(buffer)
    instrs |= move(buffer, [(arg, 1)])
    instrs |= if_ or base.CommandReturn()
    instrs |= tokens.Decrement(else_flag)
    instrs |= tokens.ExitLoop()

    instrs |= tokens.EnterLoop(else_flag)
    instrs |= tokens.Decrement(else_flag)
    instrs |= else_ or base.CommandReturn()
    instrs |= tokens.ExitLoop()

    instrs |= memoptix.Free(else_flag)
    instrs |= memoptix.Free(buffer)

    return instrs
