import attrs

from src.ir import tokens
from src.memoptix import metainfo

from . import base, dtypes
from .add import add, add_int_long
from .copy import copy
from .divmod import div
from .init import init
from .move import move
from .mul import mul


@attrs.frozen
class Or(base.OpCode):
    left: dtypes.Unit
    right: dtypes.Unit
    target: dtypes.Unit

    def _execute(self) -> base.OpCodeReturn:
        return or_(self.left, self.right, self.target)


@base.convert
def or_(left: dtypes.Unit, right: dtypes.Unit, target: dtypes.Unit) -> base.ToConvert:
    if left == right == target:
        return
    if left == right:
        return tokens.Clear(target), copy(left, target)

    lquot, rquot = dtypes.Unit(), dtypes.Unit()
    lrem, rrem = dtypes.Unit(), dtypes.Unit()
    bit_scale, break_ = dtypes.Unit(), dtypes.Unit()
    ored_bit = dtypes.Unit()

    ret = init(lrem) | init(rrem) | init(lquot) | init(rquot) | init(bit_scale) | init(break_) | init(ored_bit)

    ret |= copy(left, lquot) | copy(right, rquot)
    ret |= add_int_long(8, break_) | tokens.Increment(bit_scale)

    ret |= tokens.Clear(target)
    ret |= tokens.EnterLoop(break_)

    ret |= div(lquot, 2, lquot, lrem)
    ret |= div(rquot, 2, rquot, rrem)

    ret |= move(lrem, [(ored_bit, 1)])
    ret |= move(rrem, [(ored_bit, 1)])

    ret |= tokens.EnterLoop(ored_bit)
    ret |= add(bit_scale, target, target)
    ret |= tokens.Clear(ored_bit)
    ret |= tokens.ExitLoop()

    ret |= tokens.Decrement(break_)
    ret |= mul(bit_scale, 2, bit_scale)
    ret |= tokens.ExitLoop()

    ret |= tokens.Clear(bit_scale)
    ret |= metainfo.Free(lrem)
    ret |= metainfo.Free(rrem)
    ret |= metainfo.Free(bit_scale)
    ret |= metainfo.Free(ored_bit)
    ret |= metainfo.Free(lquot)
    ret |= metainfo.Free(rquot)
    ret |= metainfo.Free(break_)

    return ret
