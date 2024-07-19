import collections
import typing

import attrs

from src.ir import tokens
from src.xbf import dtypes, program

from . import base


@attrs.frozen
class Move(base.BaseCommand):
    from_: dtypes.Unit
    to_: typing.Iterable[tuple[dtypes.Unit, int]]

    def _apply(self, context: program.Program) -> base.CommandReturn:
        return move(self.from_, self.to_)


@base.flatten2return
def move(from_: dtypes.Unit, to_: typing.Iterable[tuple[dtypes.Unit, int]]) -> base.ToFlatten:
    units = _calculate_total_scale_per_unit(to_)

    if from_ in units:
        raise ValueError("Target byte sequence cannot contain the start byte instance.")

    instrs = base.CommandReturn()
    instrs |= tokens.EnterLoop(from_)

    for unit, scale in units.items():
        instrs |= _integer2token(scale, unit)

    instrs |= tokens.Decrement(from_)
    instrs |= tokens.ExitLoop()

    return instrs


def _calculate_total_scale_per_unit(unit2scale: typing.Iterable[tuple[dtypes.Unit, int]]) -> dict[dtypes.Unit, int]:
    units: dict[dtypes.Unit, int] = {}
    for unit, scale in unit2scale:
        units.setdefault(unit, 0)
        units[unit] += scale

    return units


@base.flatten2return
def _integer2token(value: int, unit: dtypes.Unit) -> base.CommandReturn:
    token = tokens.Increment if value > 0 else tokens.Decrement
    return [token(owner=unit)] * abs(value)  # type: ignore
