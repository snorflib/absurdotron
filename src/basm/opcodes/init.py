import attrs

from src.memoptix import constraints

from . import base, context, dtypes


@attrs.frozen
class Init(base.OpCode):
    obj: dtypes.Unit | dtypes.Array

    def _execute(self, context: context.Context) -> base.OpCodeReturn:
        return init(self.obj)


@base.convert
def init(obj: dtypes.Unit | dtypes.Array) -> base.ToConvert:
    if isinstance(obj, dtypes.Unit):
        return constraints.UnitConstraint(obj)
    return constraints.ArrayConstraint(obj, obj.length)
