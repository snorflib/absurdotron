import attrs

from src import memoptix
from src.ir import tokens

from . import base, dtypes
from .init import init
from .move import move


@attrs.frozen
class CallZ(base.OpCode):
    arg: dtypes.Unit
    if_zero: base.OpCodeReturn | None = None
    else_: base.OpCodeReturn | None = None

    def _execute(self) -> base.OpCodeReturn:
        return callz(self.arg, self.if_zero, self.else_)


@base.convert
def callz(
    arg: dtypes.Unit,
    if_zero: base.OpCodeReturn | None = None,
    else_: base.OpCodeReturn | None = None,
) -> base.ToConvert:
    else_flag, buffer = dtypes.Unit(), dtypes.Unit()

    return [
        init(else_flag) | init(buffer),
        # if arg is not zero statement ->
        move(arg, [(buffer, 1)]),
        tokens.Increment(else_flag),
        tokens.EnterLoop(buffer),
        move(buffer, [(arg, 1)]),
        else_,
        tokens.Decrement(else_flag),
        tokens.ExitLoop(),
        # elif arg is zero statement ->
        tokens.EnterLoop(else_flag),
        tokens.Decrement(else_flag),
        if_zero,
        tokens.ExitLoop(),
        #
        memoptix.Free(else_flag),
        memoptix.Free(buffer),
    ]
