import attrs

from src.ir import tokens
from src.xbf import dtypes, program

from .base import BaseCommand


@attrs.frozen
class ClearUnit(BaseCommand):
    unit: dtypes.Unit

    def _apply(self, context: program.Program) -> None:
        context.routine.append(tokens.Clear(self.unit))
