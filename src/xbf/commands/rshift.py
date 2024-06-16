import attrs

from src.xbf import dtypes, program

from .base import BaseCommand
from .divmod import _generic_division


@attrs.frozen
class RShiftUnit(BaseCommand):
    origin: dtypes.Unit
    by: int
    target: dtypes.Unit

    def _apply(self, context: program.Program) -> None:
        _generic_division(self.origin, 2**self.by, quotient=self.target, remainder=None, program=context)
