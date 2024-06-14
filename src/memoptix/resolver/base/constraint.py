from __future__ import annotations

import abc
import typing

from .model import BaseModel

M = typing.TypeVar("M", bound=BaseModel)


class BaseConstraint(typing.Generic[M], abc.ABC):
    __slots__ = ()

    def __call__(self, model: M) -> None:
        self._constrain(model)

    @abc.abstractmethod
    def _constrain(self, model: M) -> None:
        raise NotImplementedError
