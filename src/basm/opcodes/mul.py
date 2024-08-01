import attrs

from src.ir import tokens
from src.memoptix import metainfo

from . import base, dtypes
from .add import add
from .init import init
from .move import move, move_without_clear
from .utils import add_int_long


@attrs.frozen
class Mul(base.OpCode):
    multiplicand: dtypes.Unit | int
    multiplier: dtypes.Unit | int
    target: dtypes.Unit

    def _execute(self) -> base.OpCodeReturn:
        return mul(self.multiplicand, self.multiplier, self.target)


@base.convert
def mul(
    multiplicand: dtypes.Unit | int,
    multiplier: dtypes.Unit | int,
    target: dtypes.Unit,
) -> base.ToConvert:
    if isinstance(multiplicand, int) and isinstance(multiplier, int):
        return add_int_long(multiplicand * multiplier, target)
    elif isinstance(multiplier, int):
        return _mul_by_int(multiplicand, multiplier, target)  # type: ignore

    return _mul_two_units(multiplicand, multiplier, target)  # type: ignore


@base.convert
def _mul_by_int(
    multiplicand: dtypes.Unit,
    multiplier: int,
    target: dtypes.Unit,
) -> base.ToConvert:
    if multiplicand == target:
        return move_without_clear(multiplicand, target, scale=multiplier - 1)

    clr = base.OpCodeReturn([tokens.Clear(target)])
    return clr | move_without_clear(multiplicand, target, scale=multiplier)


@base.convert
def _mul_two_units(
    multiplicand: dtypes.Unit,
    multiplier: dtypes.Unit,
    target: dtypes.Unit,
) -> base.ToConvert:
    cand_buf, plier_buf = dtypes.Unit(), dtypes.Unit()

    instrs = base.OpCodeReturn()
    instrs |= init(cand_buf)
    instrs |= init(plier_buf)

    if multiplicand == multiplier:
        instrs |= move(multiplicand, [(cand_buf, 1), (plier_buf, 1)])
    else:
        instrs |= move(multiplicand, [(cand_buf, 1)])
        instrs |= move(multiplier, [(plier_buf, 1)])

    instrs |= tokens.Clear(target)
    instrs |= tokens.EnterLoop(plier_buf)

    instrs |= add(cand_buf, target, target)

    if multiplicand != multiplier != target:
        instrs |= tokens.Increment(multiplier)

    instrs |= tokens.Decrement(plier_buf)
    instrs |= tokens.ExitLoop()

    if multiplicand != target:
        instrs |= move(cand_buf, [(multiplicand, 1)])

    instrs |= metainfo.Free(cand_buf)
    instrs |= metainfo.Free(plier_buf)

    return instrs
