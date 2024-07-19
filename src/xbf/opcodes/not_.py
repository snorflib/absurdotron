import attrs

from src.ir import tokens
from src.xbf import dtypes, program

from . import base
from .add import _add_int, _move_without_clear


@attrs.frozen
class Not(base.BaseCommand):
    arg: dtypes.Unit | int
    target: dtypes.Unit

    def _apply(self, context: program.Program) -> base.CommandReturn:
        return not_(self.arg, self.target)


@base.flatten2return
def not_(arg: dtypes.Unit | int, target: dtypes.Unit) -> base.ToFlatten:
    if isinstance(arg, int):
        return _add_int(~arg, target)

    return _not_unit(arg, target)


@base.flatten2return
def _not_unit(arg: dtypes.Unit, target: dtypes.Unit) -> base.ToFlatten:
    if arg == target:
        return _move_without_clear(target, target, -2) | tokens.Decrement(target)

    return tokens.Clear(target), tokens.Decrement(target), _move_without_clear(arg, target, -1)
