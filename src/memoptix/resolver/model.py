from __future__ import annotations

import typing

import attrs
import mip  # type: ignore

from src.ir import types
from src.memoptix import exceptions


def owner_to_str_key(owner: types.Owner) -> str:
    return str(hash(owner))


@attrs.frozen
class Model:
    model: mip.Model = attrs.field(factory=mip.Model)

    def add_var(
        self,
        owner: types.Owner | None,
        lb: mip.numbers.Real = 0.0,  # type: ignore
        ub: mip.numbers.Real = mip.INF,  # type: ignore
        obj: mip.numbers.Real = 0.0,  # type: ignore
        var_type: str = mip.CONTINUOUS,
        column: typing.Optional[mip.Column] = None,
    ) -> mip.Var:
        return self.model.add_var(
            "" if owner is None else owner_to_str_key(owner),
            lb=lb,
            ub=ub,
            obj=obj,
            var_type=var_type,
            column=column,  # type: ignore
        )

    def add_constr(
        self,
        lin_expr: mip.LinExpr,
        name: str = "",
        priority: typing.Optional[mip.ConstraintPriority] = None,
    ) -> mip.Constr:
        return self.model.add_constr(
            lin_expr=lin_expr,
            name=name,
            priority=priority,
        )

    def add_sos(self, sos: list[tuple[mip.Var, mip.numbers.Real]], sos_type: int) -> None:
        self.model.add_sos(sos=sos, sos_type=sos_type)

    def get_var(self, owner: types.Owner) -> typing.Optional[mip.Var]:
        return self.model.var_by_name(owner_to_str_key(owner))

    def optimize(
        self,
        max_seconds: mip.numbers.Real = mip.INF,  # type: ignore
        max_nodes: int = mip.INT_MAX,
        max_solutions: int = mip.INT_MAX,
        max_seconds_same_incumbent: mip.numbers.Real = mip.INF,  # type: ignore
        max_nodes_same_incumbent: int = mip.INT_MAX,
        relax: bool = False,
        verbose: int = 0,
    ) -> mip.OptimizationStatus:
        self.model.verbose = verbose
        return self.model.optimize(
            max_seconds=max_seconds,
            max_nodes=max_nodes,
            max_solutions=max_solutions,
            max_seconds_same_incumbent=max_seconds_same_incumbent,
            max_nodes_same_incumbent=max_nodes_same_incumbent,
            relax=relax,
        )

    def get_vars_by_owners(self, owners: typing.Iterable[types.Owner]) -> dict[types.Owner, int]:
        indexes = {}
        for owner in owners:
            if (index := self.get_var(owner)) is None:
                raise exceptions.ReferencingUnknownOwnerError(owner)
            if index.x is None:
                raise exceptions.OwnerIndexIsNotYetDeterminedError(owner)
            indexes[owner] = int(index.x)  # type: ignore

        return indexes
