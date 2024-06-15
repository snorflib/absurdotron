from __future__ import annotations

import abc

from src.memoptix import metainfo, resolver


class BaseConstraint(abc.ABC):
    __slots__ = ()

    def __call__(self, model: resolver.Model, meta: metainfo.RoutineMetaInfo) -> None:
        return self._constrain(model, meta)

    @abc.abstractmethod
    def _constrain(self, model: resolver.Model, meta: metainfo.RoutineMetaInfo) -> None:
        raise NotImplementedError
