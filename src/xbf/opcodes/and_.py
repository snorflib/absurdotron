import attrs

from src.ir import tokens
from src.memoptix import metainfo
from src.xbf import dtypes, program

from .add import Add
from .assign import AssignUnit
from .base import BaseCommand
from .copy import CopyUnit
from .divmod import DivMod
from .init import Init
from .mul import Mul


def and_(left: dtypes.Unit, right: dtypes.Unit, target: dtypes.Unit, program: program.Program) -> None:
    if left is right is target:
        return
    if left is right:
        program.routine.append(tokens.Clear(target))
        CopyUnit(left, target)(program)
        return

    lquot, rquot = dtypes.Unit(), dtypes.Unit()
    lrem, rrem = dtypes.Unit(), dtypes.Unit()
    bit_scale, break_ = dtypes.Unit(), dtypes.Unit()
    Init(lrem)(program)
    Init(rrem)(program)
    Init(lquot)(program)
    Init(rquot)(program)
    Init(bit_scale)(program)
    Init(break_)(program)

    CopyUnit(left, lquot)(program)
    CopyUnit(right, rquot)(program)

    AssignUnit(break_, 8)(program)
    AssignUnit(bit_scale, 1)(program)

    routine = program.routine
    routine.append(tokens.Clear(target))
    routine.append(tokens.EnterLoop(break_))

    DivMod(lquot, 2, lquot, lrem)(program)
    DivMod(rquot, 2, rquot, rrem)(program)

    routine.append(tokens.EnterLoop(lrem))
    routine.append(tokens.EnterLoop(rrem))
    Add(bit_scale, target, target)(program)
    routine.append(tokens.Decrement(rrem))
    routine.append(tokens.ExitLoop())
    routine.append(tokens.Decrement(lrem))
    routine.append(tokens.ExitLoop())

    routine.append(tokens.Decrement(break_))
    Mul(bit_scale, 2, bit_scale)(program)
    routine.append(tokens.ExitLoop())

    routine.append(tokens.Clear(lrem))
    routine.append(tokens.Clear(rrem))
    routine.append(tokens.Clear(bit_scale))

    routine.append(metainfo.Free(lrem))
    routine.append(metainfo.Free(rrem))
    routine.append(metainfo.Free(bit_scale))
    routine.append(metainfo.Free(lquot))
    routine.append(metainfo.Free(rquot))
    routine.append(metainfo.Free(break_))


@attrs.frozen
class AndUnit(BaseCommand):
    left: dtypes.Unit
    right: dtypes.Unit
    target: dtypes.Unit

    def _apply(self, context: program.Program) -> None:
        and_(self.left, self.right, self.target, program=context)
