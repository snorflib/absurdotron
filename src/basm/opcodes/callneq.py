import attrs

from src import memoptix
from src.ir import tokens

from . import base, dtypes
from .init import init
from .sub import sub


@attrs.frozen
class CallNeq(base.OpCode):
    left: dtypes.Unit
    right: dtypes.Unit
    if_neq: base.OpCodeReturn | None = None
    else_: base.OpCodeReturn | None = None

    def _execute(self) -> base.OpCodeReturn:
        return _callneq(self.left, self.right, self.if_neq, self.else_)


def _callneq(
    left: dtypes.Unit,
    right: dtypes.Unit,
    if_neq: base.OpCodeReturn | None,
    else_: base.OpCodeReturn | None,
) -> base.OpCodeReturn:
    else_flag, buffer = dtypes.Unit(), dtypes.Unit()

    ret = init(else_flag) | init(buffer) | sub(left, right, buffer)
    ret |= tokens.Increment(else_flag)
    ret |= tokens.EnterLoop(buffer)
    ret |= tokens.Clear(buffer)
    ret |= if_neq
    ret |= tokens.Decrement(else_flag)
    ret |= tokens.ExitLoop()

    ret |= tokens.EnterLoop(else_flag)
    ret |= tokens.Decrement(else_flag)
    ret |= else_
    ret |= tokens.ExitLoop()

    ret |= memoptix.Free(else_flag)
    ret |= memoptix.Free(buffer)

    return ret
