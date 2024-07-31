import typing

import attrs

from src import memoptix
from src.ir import tokens

from . import base, context, dtypes
from .init import init
from .utils import add_int_long


@attrs.frozen
class Move(base.OpCode):
    from_: dtypes.Unit
    to_: typing.Iterable[tuple[dtypes.Unit, int]]

    def _execute(self, context: context.Context) -> base.OpCodeReturn:
        return move(self.from_, self.to_)


@base.convert
def move_without_clear(from_: dtypes.Unit, to_: dtypes.Unit, scale: int = 1) -> base.ToConvert:
    if scale == 0:
        return None

    if (from_ == to_) and (scale == -1):
        return [tokens.Clear(from_)]

    buffer = dtypes.Unit()
    return [
        init(buffer),
        move(from_, [(buffer, 1)]),
        move(buffer, [(from_, 1), (to_, scale)]),
        memoptix.Free(buffer),
    ]


@base.convert
def move(from_: dtypes.Unit, to_: typing.Iterable[tuple[dtypes.Unit, int]]) -> base.ToConvert:
    units = _calculate_total_scale_per_unit(to_)

    if from_ in units:
        raise ValueError("Target unit sequence cannot contain the start unit instance.")

    instrs = base.OpCodeReturn()
    instrs |= tokens.EnterLoop(from_)

    for unit, scale in units.items():
        instrs |= add_int_long(scale, unit)

    instrs |= tokens.Decrement(from_)
    instrs |= tokens.ExitLoop()

    return instrs


def _calculate_total_scale_per_unit(unit2scale: typing.Iterable[tuple[dtypes.Unit, int]]) -> dict[dtypes.Unit, int]:
    units: dict[dtypes.Unit, int] = {}
    for unit, scale in unit2scale:
        units.setdefault(unit, 0)
        units[unit] += scale

    return units
