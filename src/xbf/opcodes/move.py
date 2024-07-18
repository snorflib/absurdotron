import attrs

from src.ir import tokens
from src.xbf import dtypes, program

from .base import BaseCommand


def _move_unit2units(from_unit: dtypes.Unit, to_units: list[tuple[dtypes.Unit, int]]) -> list[tokens.BFToken]:
    filling_sequence = []
    for unit, scale in to_units:
        if unit == from_unit:
            raise ValueError("Target byte sequence cannot contain the start byte instance.")

        token = tokens.Increment if scale > 0 else tokens.Decrement
        filling_sequence.extend([token(owner=unit)] * abs(scale))

    instructions: list[tokens.BFToken] = [tokens.EnterLoop(from_unit)]
    instructions.extend(filling_sequence)
    instructions.append(tokens.Decrement(from_unit))
    instructions.append(tokens.ExitLoop())

    return instructions


@attrs.frozen
class MoveUnit(BaseCommand):
    unit: dtypes.Unit
    to: list[tuple[dtypes.Unit, int]]

    def _apply(self, context: program.Program) -> None:
        context.routine.extend(
            _move_unit2units(
                self.unit,
                self.to,
            )
        )
