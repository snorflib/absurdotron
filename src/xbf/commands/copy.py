import attrs

from src.ir import tokens
from src.memoptix import metainfo
from src.xbf import dtypes, program

from .base import BaseCommand
from .init_unit import InitUnit
from .move import _move_unit2units


def _copy(from_: dtypes.Unit, to: dtypes.Unit, program: program.Program) -> list[tokens.BFToken]:
    if from_ is to:
        return []

    buffer = dtypes.Unit()
    InitUnit(buffer)(program)

    routine: list[tokens.BFToken] = [tokens.Clear(to)]
    routine.extend(_move_unit2units(from_, [(buffer, 1)]))
    routine.extend(_move_unit2units(buffer, [(from_, 1), (to, 1)]))

    routine.append(metainfo.Free(buffer))

    return routine


@attrs.frozen
class CopyUnit(BaseCommand):
    from_: dtypes.Unit
    to_: dtypes.Unit

    def _apply(self, context: program.Program) -> None:
        context.routine.extend(
            _copy(
                self.from_,
                self.to_,
                context,
            )
        )
