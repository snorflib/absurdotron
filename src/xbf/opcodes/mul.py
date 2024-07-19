import attrs

from src.ir import tokens
from src.memoptix import metainfo
from src.xbf import dtypes, program

from . import base
from .add import _add_int, _move_without_clear, add
from .init import init
from .move import move


@attrs.frozen
class Mul(base.BaseCommand):
    multiplicand: dtypes.Unit | int
    multiplier: dtypes.Unit | int
    target: dtypes.Unit

    def _apply(self, context: program.Program) -> base.CommandReturn:
        return mul(self.multiplicand, self.multiplier, self.target)


@base.flatten2return
def mul(
    multiplicand: dtypes.Unit | int,
    multiplier: dtypes.Unit | int,
    target: dtypes.Unit,
) -> base.ToFlatten:
    if isinstance(multiplicand, int) and isinstance(multiplier, int):
        return _add_int(multiplicand * multiplier, target)
    elif isinstance(multiplier, int):
        return _mul_by_int(multiplicand, multiplier, target)  # type: ignore

    return _mul_two_units(multiplicand, multiplier, target)  # type: ignore


@base.flatten2return
def _mul_by_int(
    multiplicand: dtypes.Unit,
    multiplier: int,
    target: dtypes.Unit,
) -> base.ToFlatten:
    if multiplicand == target:
        return _move_without_clear(multiplicand, target, scale=multiplier - 1)

    return tokens.Clear(target) | _move_without_clear(multiplicand, target, scale=multiplier)


@base.flatten2return
def _mul_two_units(
    multiplicand: dtypes.Unit,
    multiplier: dtypes.Unit,
    target: dtypes.Unit,
) -> base.ToFlatten:
    cand_buf, plier_buf = dtypes.Unit(), dtypes.Unit()

    instrs = base.CommandReturn()
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
