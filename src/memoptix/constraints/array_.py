import attrs
import mip  # type: ignore

from src.ir import types
from src.memoptix import exceptions, metainfo, resolver

from .base import BaseConstraint
from .utils import get_all_intersected_owners


def _add_array_intersection_constraint(
    model: resolver.Model,
    array: types.Owner,
    length: int,
    right: types.Owner,
) -> None:
    if (array := model.get_var(array)) is None:
        raise exceptions.ReferencingUnknownOwnerError(array)
    elif (right := model.get_var(right)) is None:
        raise exceptions.ReferencingUnknownOwnerError(right)

    fir_cond_abs = model.add_var(None, var_type=mip.INTEGER)
    fir_cond_neg = model.add_var(None, var_type=mip.INTEGER)
    sec_cond_abs = model.add_var(None, var_type=mip.INTEGER)
    sec_cond_neg = model.add_var(None, var_type=mip.INTEGER)

    model.add_constr((fir_cond_abs - fir_cond_neg) == (right - array - length + 2))  # type: ignore
    model.add_constr((sec_cond_abs - sec_cond_neg) == (array - right + 1))  # type: ignore

    model.add_sos([(fir_cond_abs, 1), (fir_cond_neg, 1)], 1)  # type: ignore
    model.add_sos([(sec_cond_abs, 1), (sec_cond_neg, 1)], 1)  # type: ignore

    model.add_constr(fir_cond_abs + sec_cond_abs >= 2)  # type: ignore


@attrs.frozen
class ArrayConstraint(BaseConstraint):
    anchor: types.Owner
    length: int

    def _constrain(self, model: resolver.Model, meta: metainfo.RoutineMetaInfo) -> None:
        for left, right in get_all_intersected_owners(meta.scopes):
            if self.anchor == left:
                ...
            elif self.anchor == right:
                left, right = right, left
            else:
                continue
            _add_array_intersection_constraint(model, left, self.length, right)
