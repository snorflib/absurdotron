import attrs

from src.ir import tokens

from . import base, dtypes
from .add import add
from .move import move_without_clear
from .utils import add_int_long


@attrs.frozen
class Sub(base.OpCode):
    minuend: dtypes.Unit | int
    subtrahend: dtypes.Unit | int
    target: dtypes.Unit

    def _execute(self) -> base.OpCodeReturn:
        return sub(self.minuend, self.subtrahend, self.target)


@base.convert
def sub(
    minuend: dtypes.Unit | int,
    subtrahend: dtypes.Unit | int,
    target: dtypes.Unit,
) -> base.ToConvert:
    if target == minuend:
        return _sub_from_target(subtrahend, target=target)

    return _clear_target_and_sub(subtrahend, target) | add(target, minuend, target=target)


@base.convert
def _clear_target_and_sub(subtrahend: dtypes.Unit | int, target: dtypes.Unit) -> base.ToConvert:
    if subtrahend == target:
        return move_without_clear(subtrahend, target, -2)

    return (
        tokens.Clear(target),
        _sub_from_target(subtrahend, target),
    )


@base.convert
def _sub_from_target(subtrahend: dtypes.Unit | int, target: dtypes.Unit) -> base.ToConvert:
    if isinstance(subtrahend, int):
        return add_int_long(-subtrahend, target)

    return move_without_clear(subtrahend, target, -1)
