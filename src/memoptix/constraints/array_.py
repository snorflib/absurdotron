import attrs

from src.ir import types

from .base import BaseConstraint


@attrs.frozen
class ArrayConstraint(BaseConstraint):
    owner: types.Owner
    length: int
