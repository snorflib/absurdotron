import attrs
import mip  # type: ignore

from src.ir import types
from src.memoptix import exceptions, metainfo, resolver

from .base import BaseConstraint
from .utils import get_all_intersected_owners


def _add_intersection_constraint(model: resolver.Model, left: types.Owner, right: types.Owner) -> None:
    if (left := model.get_var(left)) is None:
        raise exceptions.ReferencingUnknownOwnerError(left)
    elif (right := model.get_var(right)) is None:
        raise exceptions.ReferencingUnknownOwnerError(right)

    abs_pos = model.add_var(
        None,
        var_type=mip.INTEGER,
        lb=0,  # type: ignore
        ub=mip.INT_MAX,
    )
    abs_neg = model.add_var(
        None,
        var_type=mip.INTEGER,
        lb=0,  # type: ignore
        ub=mip.INT_MAX,
    )

    model.add_constr((left - right) == (abs_pos - abs_neg))
    model.add_sos([(abs_pos, 1), (abs_neg, 1)], 1)  # type: ignore
    model.add_constr(abs_pos + abs_neg >= 1)  # type: ignore


@attrs.frozen
class UnitConstraint(BaseConstraint):
    unit: types.Owner

    def _constrain(self, model: resolver.Model, meta: metainfo.RoutineMetaInfo) -> None:
        for left, right in get_all_intersected_owners(meta.scopes):
            if self.unit == left:
                ...
            elif self.unit == right:
                left, right = right, left
            else:
                continue
            _add_intersection_constraint(model, left, right)
