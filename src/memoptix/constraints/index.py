import attrs

from src.ir import types
from src.memoptix import exceptions, metainfo, resolver

from .base import BaseConstraint


@attrs.frozen
class IndexedOwnerConstraint(BaseConstraint):
    owner: types.Owner
    index: int

    def _constrain(self, model: resolver.Model, meta: metainfo.RoutineMetaInfo) -> None:
        if (var := model.get_var(self.owner)) is None:
            raise exceptions.ReferencingUnknownOwnerError(self.owner)

        model.add_constr(var == self.index)
