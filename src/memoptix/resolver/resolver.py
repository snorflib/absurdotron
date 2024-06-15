from __future__ import annotations

import collections.abc
import typing

import attrs
import mip  # type: ignore

from src.ir import tokens
from src.memoptix import constraints, exceptions, metainfo

from .model import Model


@attrs.frozen
class MemoryResolver:
    meta: metainfo.RoutineMetaInfo
    model: Model = attrs.field(factory=Model)

    def resolve(self, **kwargs: typing.Any) -> typing.Self:
        status = self.model.optimize(**kwargs)

        if status is mip.OptimizationStatus.INFEASIBLE:
            raise exceptions.MemoryAllocationFailedError

        return self

    def constrain(self, constraint: constraints.BaseConstraint) -> None:
        constraint(self.model, self.meta)


def build_memory_resolver(
    constraints: typing.Iterable[constraints.BaseConstraint],
    meta_info: metainfo.RoutineMetaInfo | collections.abc.Sequence[tokens.BFToken],
    resolver: typing.Optional[MemoryResolver] = None,
) -> MemoryResolver:
    if not isinstance(meta_info, metainfo.RoutineMetaInfo):
        meta_info = metainfo.get_metainfo_from_routine(meta_info)

    resolver = resolver or MemoryResolver(meta_info)

    for owner in meta_info.owners:
        resolver.model.add_var(owner, var_type=mip.INTEGER)

    for constraint in constraints:
        resolver.constrain(constraint)

    return resolver
