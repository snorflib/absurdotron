import attrs

from src.xbf import dtypes, program

from .add import _generic_addition
from .base import BaseCommand


@attrs.frozen
class SubUnit(BaseCommand):
    origin: dtypes.Unit
    to_sub: dtypes.Unit | int
    target: dtypes.Unit

    def _apply(self, context: program.Program) -> None:
        context.routine.extend(
            _generic_addition(
                self.origin,
                self.to_sub,
                self.target,
                context,
                add=False,
            )
        )
