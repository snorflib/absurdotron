import attrs

from src.memoptix import constraints
from src.xbf import dtypes, program

from .base import BaseCommand


@attrs.frozen
class InitUnit(BaseCommand):
    unit: dtypes.Unit

    def _apply(self, context: program.Program) -> None:
        context.constr.append(constraints.UnitConstraint(self.unit))
