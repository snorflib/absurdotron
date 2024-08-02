
import attrs

from src import memoptix
from src.ir import tokens

from . import base, dtypes
from .callz import callz
from .init import init
from .move import move


@attrs.frozen
class CallGE(base.OpCode):
    left: dtypes.Unit
    right: dtypes.Unit
    if_ge: base.OpCodeReturn | None = None
    else_: base.OpCodeReturn | None = None

    def _execute(self) -> base.OpCodeReturn:
        return _callge(self.left, self.right, self.if_ge, self.else_)


def _callge(
    left: dtypes.Unit,
    right: dtypes.Unit,
    if_ge: base.OpCodeReturn | None,
    else_: base.OpCodeReturn | None,
) -> base.OpCodeReturn:
    else_flag = dtypes.Unit()
    right_buffer, left_buffer = dtypes.Unit(), dtypes.Unit()

    ret = init(else_flag) | init(right_buffer) | init(left_buffer)
    ret |= move(left, [(left_buffer, 1)])
    ret |= move(right, [(right_buffer, 1)])

    ret |= tokens.EnterLoop(right_buffer)
    ret |= tokens.Decrement(right_buffer)
    ret |= tokens.Increment(right)

    ret |= callz(
        left_buffer,
        if_zero=base.OpCodeReturn() | move(right_buffer, [(right, 1)]) | tokens.Increment(else_flag),
        else_=base.OpCodeReturn() | tokens.Decrement(left_buffer) | tokens.Increment(left),
    )
    ret |= tokens.ExitLoop()
    ret |= move(left_buffer, [(left, 1)])

    ret |= callz(else_flag, if_zero=if_ge, else_=else_)

    ret |= tokens.Clear(else_flag)
    ret |= memoptix.Free(else_flag)
    ret |= memoptix.Free(left_buffer)
    ret |= memoptix.Free(right_buffer)

    return ret
