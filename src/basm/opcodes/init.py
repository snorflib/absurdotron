import attrs

from src.basm import context
from src.memoptix import constraints

from . import base, dtypes


@attrs.frozen
class InitArgs(base.OpCodeArgs):
    obj: dtypes.Unit | dtypes.Array


@attrs.frozen
class Init(base.OpCode[InitArgs]):
    def _apply(self, context: context.Context) -> base.OpCodeReturn:
        return init(self.args.obj)


@base.to_convert
def init(obj: dtypes.Unit | dtypes.Array) -> base.ToConvert:
    if isinstance(obj, dtypes.Unit):
        return constraints.UnitConstraint(obj)
    return constraints.ArrayConstraint(obj, obj.length)
