import attrs

from src.ir import tokens

from . import base, dtypes
from .move import move_without_clear
from .utils import add_int_long


@attrs.frozen
class Add(base.OpCode):
    augend: dtypes.Unit | int
    addend: dtypes.Unit | int
    target: dtypes.Unit

    def _execute(self) -> base.OpCodeReturn:
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

    return move_without_clear(argument, target)
