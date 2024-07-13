import attrs

from src.memoptix import constraints
from src.xbf import dtypes, program

from .base import BaseCommand


@attrs.frozen
class InitArray(BaseCommand):
    array: dtypes.Array

    def _apply(self, context: program.Program) -> None:
        context.constr.append(constraints.ArrayConstraint(self.array, self.array.length))
