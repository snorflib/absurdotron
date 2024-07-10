import attrs

from src.ir import types

from .base import BaseConstraint


@attrs.frozen
class UnitConstraint(BaseConstraint):
    owner: types.Owner
