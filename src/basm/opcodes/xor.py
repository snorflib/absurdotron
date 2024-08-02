import attrs

from src.ir import tokens
from src.memoptix import metainfo

from . import base, dtypes
from .add import add, add_int_long
from .callz import callz
from .copy import copy
from .divmod import div
from .init import init
from .move import move
from .mul import mul


@attrs.frozen
class Xor(base.OpCode):
    left: dtypes.Unit
    right: dtypes.Unit
    target: dtypes.Unit

    def _execute(self) -> base.OpCodeReturn:
        return xor_(self.left, self.right, self.target)


@base.convert
def xor_(left: dtypes.Unit, right: dtypes.Unit, target: dtypes.Unit) -> base.OpCodeReturn:
    if left == right:
        return tokens.Clear(target)

    lquot, rquot = dtypes.Unit(), dtypes.Unit()
    lrem, rrem = dtypes.Unit(), dtypes.Unit()
    bit_scale, break_ = dtypes.Unit(), dtypes.Unit()
    xored_bit = dtypes.Unit()

    ret = init(lrem) | init(rrem) | init(lquot) | init(rquot) | init(bit_scale) | init(break_) | init(xored_bit)

    ret |= copy(left, lquot)| copy(right, rquot)
    ret |= add_int_long(8, break_) | tokens.Increment(bit_scale)

    ret |= tokens.Clear(target)
    ret |= tokens.EnterLoop(break_)
    ret |= div(lquot, 2, lquot, lrem) | div(rquot, 2, rquot, rrem)

    ret |= move(lrem, [(xored_bit, 1)])
    ret |= move(rrem, [(xored_bit, 1)])

    ret |= tokens.EnterLoop(xored_bit)
    ret |= tokens.Decrement(xored_bit)
    ret |= callz(
        xored_bit,
        else_=base.OpCodeReturn() | tokens.Clear(xored_bit),
        if_zero=add(target, bit_scale, target),
    )
    ret |= tokens.ExitLoop()

    ret |= tokens.Decrement(break_)
    ret |= mul(bit_scale, 2, bit_scale)
    ret |= tokens.ExitLoop()

    ret |= tokens.Clear(bit_scale)
    ret |= metainfo.Free(lrem)
    ret |= metainfo.Free(rrem)
    ret |= metainfo.Free(bit_scale)
    ret |= metainfo.Free(lquot)
    ret |= metainfo.Free(rquot)
    ret |= metainfo.Free(xored_bit)
    ret |= metainfo.Free(break_)

    return ret
