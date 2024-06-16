import attrs

from src.xbf import dtypes, program

from .base import BaseCommand
from .mul import _multiply


@attrs.frozen
class LShiftUnit(BaseCommand):
    origin: dtypes.Unit
    by: int
    target: dtypes.Unit

    def _apply(self, context: program.Program) -> None:
        context.routine.extend(
            _multiply(
                self.origin,
                2**self.by,
                self.target,
                context,
            )
        )
