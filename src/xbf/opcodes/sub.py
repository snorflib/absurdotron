import attrs

from src import memoptix
from src.ir import tokens
from src.xbf import dtypes, program

from . import base
from .add import _add, _add_ints
from .move import _move_unit2units


@attrs.frozen
class Sub(base.BaseCommand):
    minuend: dtypes.Unit | int
    subtrahend: dtypes.Unit | int
    target: dtypes.Unit

    def _apply(self, context: program.Program) -> base.CommandReturn:
        return sub(self.minuend, self.subtrahend, self.target)


@base.flatten2return
def sub(
    minuend: dtypes.Unit | int,
    subtrahend: dtypes.Unit | int,
    target: dtypes.Unit,
) -> base.ToFlatten:
    if target == minuend:
        return _sub_from_target(subtrahend, target=target)

    return _clear_target_and_sub(subtrahend, target) | _add(target, minuend, target=target)


@base.flatten2return
def _clear_target_and_sub(subtrahend: dtypes.Unit | int, target: dtypes.Unit) -> base.ToFlatten:
    if subtrahend == target:
        return _move_without_clear(subtrahend, target, -2)  # type: ignore

    return (
        tokens.Clear(target),
        _sub_from_target(subtrahend, target),
    )


@base.flatten2return
def _sub_from_target(subtrahend: dtypes.Unit | int, target: dtypes.Unit) -> base.ToFlatten:
    if isinstance(subtrahend, int):
        return _add_ints(-subtrahend, target)

    return _move_without_clear(subtrahend, target, -1)


@base.flatten2return
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
