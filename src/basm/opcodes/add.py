import attrs

from src import memoptix
from src.ir import tokens

from . import base, context, dtypes
from .init import init
from .move import move
from .utils import add_int_long


@attrs.frozen
class Add(base.OpCode):
    augend: dtypes.Unit | int
    addend: dtypes.Unit | int
    target: dtypes.Unit

    def _execute(self, context: context.Context) -> base.OpCodeReturn:
        return add(self.augend, self.addend, target=self.target)


@base.convert
def add(augend: dtypes.Unit | int, addend: dtypes.Unit | int, target: dtypes.Unit) -> base.ToConvert:
    if target == augend:
        return _add_to_target(addend, target)
    elif target == addend:
        return _add_to_target(augend, target)

    clr = base.OpCodeReturn([tokens.Clear(target)])
    return clr | _add_to_target(augend, target) | _add_to_target(addend, target)


@base.convert
def _add_to_target(argument: dtypes.Unit | int, target: dtypes.Unit) -> base.ToConvert:
    if isinstance(argument, int):
        return add_int_long(argument, target)

    return _move_without_clear(argument, target)


@base.convert
def _move_without_clear(from_: dtypes.Unit, to_: dtypes.Unit, scale: int = 1) -> base.ToConvert:
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
