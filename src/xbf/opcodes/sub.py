import collections

import attrs

from src import memoptix
from src.ir import tokens
from src.xbf import dtypes, program

from . import base
from .add import _add, _add_ints
from .move import _move_unit2units


@attrs.frozen
class Sub(base.BaseCommand):
    minuends: list[dtypes.Unit | int]
    subtrahends: list[dtypes.Unit | int]
    target: dtypes.Unit

    def _apply(self, context: program.Program) -> base.CommandReturn:
        return _sub(self.minuends, self.subtrahends, self.target)


@base.flatten2return
def _sub(
    minuends: list[dtypes.Unit | int], subtrahends: list[dtypes.Unit | int], target: dtypes.Unit
) -> base.ToFlatten:
    minuends, subtrahends = _reduce_minuends_and_subtrahends(minuends, subtrahends)

    if target in minuends:
        return _add(*minuends, target=target) | _sub_from_target(*subtrahends, target=target)

    return _sub_from_target(target, *subtrahends, target=target) | _add(target, *minuends, target=target)


def _reduce_minuends_and_subtrahends(
    minuends: list[dtypes.Unit | int], subtrahends: list[dtypes.Unit | int]
) -> tuple[list[dtypes.Unit | int], list[dtypes.Unit | int]]:
    new_minuends = []

    for minuend in minuends:
        if minuend in subtrahends:
            subtrahends.remove(minuend)
            continue
        new_minuends.append(minuend)

    return new_minuends, subtrahends


@base.flatten2return
def _sub_from_target(*args: dtypes.Unit | int, target: dtypes.Unit) -> base.ToFlatten:
    arg_sorts = {int: [], dtypes.Unit: []}  # type: ignore
    for arg in args:
        arg_sorts[type(arg)].append(arg)

    return [
        _sub_units(*arg_sorts[dtypes.Unit], target=target),
        _sub_ints(sum(arg_sorts[int], 0), target=target),
    ]


def _sub_ints(value: int, target: dtypes.Unit) -> base.CommandReturn:
    return _add_ints(-value, target)


@base.flatten2return
def _sub_units(*args: dtypes.Unit, target: dtypes.Unit) -> base.ToFlatten:
    # If target exists it will be placed as a first key.
    counts = {target: 0} | collections.Counter(args)

    instrs: list[base.ToFlatten] = []
    for arg, scale in counts.items():
        instrs.append(_move_without_clear(arg, target, -scale))

    return instrs


def _move_without_clear(from_: dtypes.Unit, to_: dtypes.Unit, scale: int = 1) -> base.ToFlatten:
    if scale == 0:
        return None

    if (from_ == to_) and (scale == -1):
        return [tokens.Clear(from_)]

    buffer = dtypes.Unit()
    return [
        memoptix.UnitConstraint(buffer),
        _move_unit2units(from_, [(buffer, 1)]),
        _move_unit2units(buffer, [(from_, 1), (to_, scale)]),
        memoptix.Free(buffer),
    ]
