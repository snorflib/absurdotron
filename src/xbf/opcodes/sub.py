import attrs

from src.ir import tokens
from src.xbf import dtypes, program

from . import base
from .add import _add_int, _move_without_clear, add


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

    return _clear_target_and_sub(subtrahend, target) | add(target, minuend, target=target)


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
        return _add_int(-subtrahend, target)

    return _move_without_clear(subtrahend, target, -1)
