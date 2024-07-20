import attrs

from src.memoptix import constraints
from src.xbf import dtypes, program

from . import base


@attrs.frozen
class Init(base.BaseCommand):
    obj: dtypes.Unit | dtypes.Array

    def _apply(self, context: program.Program) -> base.CommandReturn:
        return init(self.obj)


@base.flatten2return
def init(obj: dtypes.Unit | dtypes.Array) -> base.ToFlatten:
    if isinstance(obj, dtypes.Unit):
        return constraints.UnitConstraint(obj)
    return constraints.ArrayConstraint(obj, obj.length)
