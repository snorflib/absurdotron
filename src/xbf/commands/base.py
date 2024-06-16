from __future__ import annotations

import abc

from src.xbf import program


class BaseCommand(abc.ABC):
    __slots__ = ()

    def __call__(self, context: program.Program) -> None:
        return self._apply(context)

    @abc.abstractmethod
    def _apply(self, context: program.Program) -> None:
        raise NotImplementedError
