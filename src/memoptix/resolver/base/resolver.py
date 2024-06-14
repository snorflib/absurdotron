from __future__ import annotations

import abc
import typing

import attrs

from .constraint import BaseConstraint
from .model import BaseModel

M = typing.TypeVar("M", bound=BaseModel)


@attrs.frozen
class BaseResolver(typing.Generic[M], abc.ABC):
    __slots__ = ("model",)

    model: M

    def constrain(self, constraint: BaseConstraint[M]) -> None:
        constraint(self.model)
