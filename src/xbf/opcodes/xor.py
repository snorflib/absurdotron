import attrs

from src.ir import tokens
from src.memoptix import metainfo
from src.xbf import dtypes, program

from .add import Add
from .assign import AssignUnit
from .base import BaseCommand
from .callz import CallZ
from .clear import ClearUnit
from .copy import CopyUnit
from .divmod import DivMod
from .init import Init
from .move import Move
from .mul import Mul


def xor_(left: dtypes.Unit, right: dtypes.Unit, target: dtypes.Unit, program: program.Program) -> None:
    if left is right:
        program.routine.append(tokens.Clear(target))
        return

    lquot, rquot = dtypes.Unit(), dtypes.Unit()
    lrem, rrem = dtypes.Unit(), dtypes.Unit()
    bit_scale, break_ = dtypes.Unit(), dtypes.Unit()
    xored_bit = dtypes.Unit()

    Init(lrem)(program)
    Init(rrem)(program)
    Init(lquot)(program)
    Init(rquot)(program)
    Init(bit_scale)(program)
    Init(break_)(program)
    Init(xored_bit)(program)

    CopyUnit(left, lquot)(program)
    CopyUnit(right, rquot)(program)

    AssignUnit(break_, 8)(program)
    AssignUnit(bit_scale, 1)(program)

    routine = program.routine
    routine.append(tokens.Clear(target))
    routine.append(tokens.EnterLoop(break_))

    DivMod(lquot, 2, lquot, lrem)(program)
    DivMod(rquot, 2, rquot, rrem)(program)

    Move(lrem, [(xored_bit, 1)])(program)
    Move(rrem, [(xored_bit, 1)])(program)

    routine.append(tokens.EnterLoop(xored_bit))
    routine.append(tokens.Decrement(xored_bit))
    CallZ(
        xored_bit,
        if_=[ClearUnit(xored_bit)],
        else_=[
            Add(target, bit_scale, target),
        ],
    )(program)
    routine.append(tokens.ExitLoop())

    routine.append(tokens.Decrement(break_))
    Mul(bit_scale, 2, bit_scale)(program)
    routine.append(tokens.ExitLoop())

    routine.append(tokens.Clear(bit_scale))
    routine.append(metainfo.Free(lrem))
    routine.append(metainfo.Free(rrem))
    routine.append(metainfo.Free(bit_scale))
    routine.append(metainfo.Free(lquot))
    routine.append(metainfo.Free(rquot))
    routine.append(metainfo.Free(xored_bit))
    routine.append(metainfo.Free(break_))


@attrs.frozen
class XorUnit(BaseCommand):
    left: dtypes.Unit
    right: dtypes.Unit
    target: dtypes.Unit

    def _apply(self, context: program.Program) -> None:
        xor_(self.left, self.right, self.target, program=context)
