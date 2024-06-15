import typing
import uuid

import attrs
import mip  # type: ignore

from src.ir import types
from src.memoptix import exceptions, metainfo, resolver

from .base import BaseConstraint

_NOT_SHARED_FACTOR: typing.Final[typing.Any] = object()


@attrs.define
class LinkedConstraint(BaseConstraint):
    from_: types.Owner
    to_: types.Owner
    length: int
    factor: typing.Hashable | None = _NOT_SHARED_FACTOR

    def __attrs_post_init__(self) -> None:
        if self.from_ == self.to_:
            raise ValueError(f"Owner cannot link itself!\nFrom: {self.from_}\nTo: {self.to_}")

    def _constrain(self, model: resolver.Model, meta: metainfo.RoutineMetaInfo) -> None:
        if (from_ := model.get_var(self.from_)) is None:
            raise exceptions.LinkingFromUnknownOwnerError(self)
        elif (to_ := model.get_var(self.to_)) is None:
            raise exceptions.LinkingToUnknownOwnerError(self)

        if self.factor is None:
            factor_var = 1

        else:
            if self.factor == object():
                self.factor = str(uuid.uuid4())

            if (factor_var := model.get_var(self.factor)) is None:
                factor_var = model.add_var(
                    self.factor,
                    var_type=mip.INTEGER,
                    lb=1,  # type: ignore
                    ub=mip.INT_MAX,
                )

        model.add_constr((to_ - from_) == (factor_var * self.length))  # type: ignore
