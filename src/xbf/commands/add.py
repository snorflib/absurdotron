import collections
import typing

import attrs

from src import memoptix
from src.ir import tokens
from src.xbf import dtypes, program

from .base import BaseCommand, CommandReturn, ToFlatten, flatten2return
from .move import _move_unit2units


@attrs.frozen
class Add(BaseCommand):
    arguments: typing.Iterable[dtypes.Unit | int]
    target: dtypes.Unit

    def _apply(self, context: program.Program) -> CommandReturn:
        return add(*self.arguments, target=self.target)


@flatten2return
def add(*args: dtypes.Unit | int, target: dtypes.Unit) -> ToFlatten:
    arg_sorts = {int: [], dtypes.Unit: []}  # type: ignore
    for arg in args:
        arg_sorts[type(arg)].append(arg)

    return [
        _add_units(*arg_sorts[dtypes.Unit], target=target),
        _add_ints(*arg_sorts[int], target=target),
    ]


@flatten2return
def _add_ints(*args: int, target: dtypes.Unit) -> ToFlatten:
    value = sum(args, 0)
    operation = tokens.Increment if value > 0 else tokens.Decrement
    return [operation(owner=target)] * abs(value)


@flatten2return
def _add_units(*args: dtypes.Unit, target: dtypes.Unit) -> ToFlatten:
    # If target exists it will be placed as a first key.
    counts = {target: 0} | collections.Counter(args)
    counts[target] -= 1

    instrs: list[ToFlatten] = []
    for arg, scale in counts.items():
        instrs.append(_add_without_clear(arg, target, scale))

    return instrs


def _add_without_clear(from_: dtypes.Unit, to_: dtypes.Unit, scale: int = 1) -> ToFlatten:
    if scale == 0:
        return None

    buffer = dtypes.Unit()
    return [
        memoptix.UnitConstraint(buffer),
        _move_unit2units(from_, [(buffer, 1)]),
        _move_unit2units(buffer, [(from_, 1), (to_, scale)]),
        memoptix.Free(buffer),
    ]
