import attrs

from src.xbf import dtypes, program

from .base import BaseCommand
from .divmod import DivModUnit


@attrs.frozen
class ModUnit(BaseCommand):
    dividend: dtypes.Unit
    divisor: dtypes.Unit | int
    target: dtypes.Unit

    def _apply(self, context: program.Program) -> None:
        DivModUnit(self.dividend, self.divisor, remainder=self.target)(context)
