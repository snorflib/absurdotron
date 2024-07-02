import attrs

from src.ir import tokens
from src.memoptix import metainfo
from src.xbf import dtypes, program

from .add import AddUnit
from .assign import AssignUnit
from .base import BaseCommand
from .copy import CopyUnit
from .divmod import DivModUnit
from .init_unit import InitUnit
from .migrate import MigrateUnit
from .mul import MulUnit


def or_(left: dtypes.Unit, right: dtypes.Unit, target: dtypes.Unit, program: program.Program) -> None:
    if left is right is target:
        return
    if left is right:
        program.routine.append(tokens.Clear(target))
        CopyUnit(left, target)(program)
        return

    lquot, rquot = dtypes.Unit(), dtypes.Unit()
    lrem, rrem = dtypes.Unit(), dtypes.Unit()
    bit_scale, break_ = dtypes.Unit(), dtypes.Unit()
    ored_bit = dtypes.Unit()

    InitUnit(lrem)(program)
    InitUnit(rrem)(program)
    InitUnit(lquot)(program)
    InitUnit(rquot)(program)
    InitUnit(bit_scale)(program)
    InitUnit(break_)(program)
    InitUnit(ored_bit)(program)

    CopyUnit(left, lquot)(program)
    CopyUnit(right, rquot)(program)

    AssignUnit(break_, 7)(program)
    AssignUnit(bit_scale, 1)(program)

    routine = program.routine
    routine.append(tokens.Clear(target))
    routine.append(tokens.EnterLoop(break_))

    DivModUnit(lquot, 2, lquot, lrem)(program)
    DivModUnit(rquot, 2, rquot, rrem)(program)

    MigrateUnit(lrem, [(ored_bit, 1)])(program)
    MigrateUnit(rrem, [(ored_bit, 1)])(program)

    routine.append(tokens.EnterLoop(ored_bit))
    AddUnit(bit_scale, target, target)(program)
    routine.append(tokens.Clear(ored_bit))
    routine.append(tokens.ExitLoop())

    routine.append(tokens.Decrement(break_))
    MulUnit(bit_scale, 2, bit_scale)(program)
    routine.append(tokens.ExitLoop())

    routine.append(tokens.Clear(bit_scale))
    routine.append(metainfo.Free(lrem))
    routine.append(metainfo.Free(rrem))
    routine.append(metainfo.Free(bit_scale))
    routine.append(metainfo.Free(lquot))
    routine.append(metainfo.Free(rquot))
    routine.append(metainfo.Free(break_))


@attrs.frozen
class OrUnit(BaseCommand):
    left: dtypes.Unit
    right: dtypes.Unit
    target: dtypes.Unit

    def _apply(self, context: program.Program) -> None:
        or_(self.left, self.right, self.target, program=context)
