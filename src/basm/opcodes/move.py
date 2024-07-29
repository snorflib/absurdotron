import typing

import attrs

from src.ir import tokens

from . import base, context, dtypes
from .utils import assigning_sequence


@attrs.frozen
class MoveArgs(base.OpCodeArgs):
    from_: dtypes.Unit
    to_: typing.Iterable[tuple[dtypes.Unit, int]]


@attrs.frozen
class Move(base.OpCode[MoveArgs]):
    def _execute(self, context: context.Context) -> base.OpCodeReturn:
        return move(self.args.from_, self.args.to_)


@base.convert
def move(from_: dtypes.Unit, to_: typing.Iterable[tuple[dtypes.Unit, int]]) -> base.ToConvert:
    units = _calculate_total_scale_per_unit(to_)

    if from_ in units:
        raise ValueError("Target unit sequence cannot contain the start unit instance.")

    instrs = base.OpCodeReturn()
    instrs |= tokens.EnterLoop(from_)

    for unit, scale in units.items():
        instrs |= assigning_sequence(scale, unit)

    instrs |= tokens.Decrement(from_)
    instrs |= tokens.ExitLoop()

    return instrs


def _calculate_total_scale_per_unit(unit2scale: typing.Iterable[tuple[dtypes.Unit, int]]) -> dict[dtypes.Unit, int]:
    units: dict[dtypes.Unit, int] = {}
    for unit, scale in unit2scale:
        units.setdefault(unit, 0)
        units[unit] += scale

    return units
