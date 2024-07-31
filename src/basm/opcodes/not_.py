import attrs

from src.ir import tokens

from . import base, context, dtypes
from .move import move_without_clear
from .utils import add_int_long


@attrs.frozen
class Not(base.OpCode):
    arg: dtypes.Unit | int
    target: dtypes.Unit

    def _execute(self, context: context.Context) -> base.OpCodeReturn:
        return not_(self.arg, self.target)


@base.convert
def not_(arg: dtypes.Unit | int, target: dtypes.Unit) -> base.ToConvert:
    if isinstance(arg, int):
        return add_int_long(~arg, target)

    return _not_unit(arg, target)


@base.convert
def _not_unit(arg: dtypes.Unit, target: dtypes.Unit) -> base.ToConvert:
    if arg == target:
        return move_without_clear(target, target, -2) | tokens.Decrement(target)

    return tokens.Clear(target), tokens.Decrement(target), move_without_clear(arg, target, -1)
