import attrs
import multimethod

from src.memoptix import constraints
from src.xbf import dtypes, program

from .base import BaseCommand


@attrs.frozen
class Init(BaseCommand):
    obj: dtypes.Unit | dtypes.Array

    def _apply(self, context: program.Program) -> None:
        context.update(_init(self.obj))


@multimethod.multimethod
def _init(obj: dtypes.Unit) -> program.Program:
    return program.Program([constraints.UnitConstraint(obj)])


@_init.register
def _(obj: dtypes.Array) -> program.Program:
    return program.Program([constraints.ArrayConstraint(obj, obj.length)])
