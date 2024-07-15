import attrs

from src.ir import tokens
from src.memoptix import metainfo
from src.xbf import dtypes, program

from .base import BaseCommand
from .init import Init
from .move import _move_unit2units


def _not_unit(unit: dtypes.Unit, target: dtypes.Unit, program: program.Program) -> list[tokens.BFToken]:
    buffer = dtypes.Unit()
    Init(buffer)(program)

    routine = _move_unit2units(unit, [(buffer, 1)])
    routine.append(tokens.Increment(buffer))

    if target is unit:
        routine.extend(_move_unit2units(buffer, [(unit, -1)]))
        routine.append(metainfo.Free(buffer))
        return routine

    routine.append(tokens.Clear(target))
    routine.extend(_move_unit2units(buffer, [(unit, 1), (target, -1)]))
    routine.append(tokens.Decrement(unit))

    routine.append(metainfo.Free(buffer))
    return routine


@attrs.frozen
class NotUnit(BaseCommand):
    unit: dtypes.Unit
    save_to: dtypes.Unit

    def _apply(self, context: program.Program) -> None:
        context.routine.extend(_not_unit(self.unit, self.save_to, context))
