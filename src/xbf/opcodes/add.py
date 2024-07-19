import attrs

from src import memoptix
from src.ir import tokens
from src.xbf import dtypes, program

from . import base
from .init import init
from .move import move


@attrs.frozen
class Add(base.BaseCommand):
    left: dtypes.Unit | int
    right: dtypes.Unit | int
    target: dtypes.Unit

    def _apply(self, context: program.Program) -> base.CommandReturn:
        return add(self.left, self.right, target=self.target)


@base.flatten2return
def add(left: dtypes.Unit | int, right: dtypes.Unit | int, target: dtypes.Unit) -> base.ToFlatten:
    if target == left:
        return _add_to_target(right, target)
    elif target == right:
        return _add_to_target(left, target)

    return tokens.Clear(target) | _add_to_target(left, target) | _add_to_target(right, target)


@base.flatten2return
def _add_to_target(argument: dtypes.Unit | int, target: dtypes.Unit) -> base.ToFlatten:
    if isinstance(argument, int):
        return _add_int(argument, target)

    return _move_without_clear(argument, target)


@base.flatten2return
def _add_int(value: int, target: dtypes.Unit) -> base.ToFlatten:
    operation = tokens.Increment if value > 0 else tokens.Decrement
    return [operation(owner=target)] * abs(value)


def _move_without_clear(from_: dtypes.Unit, to_: dtypes.Unit, scale: int = 1) -> base.ToFlatten:
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
