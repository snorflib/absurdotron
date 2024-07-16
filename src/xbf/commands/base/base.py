from __future__ import annotations

import abc

from src.xbf import program

from .return_ import CommandReturn


class BaseCommand(abc.ABC):
    __slots__ = ()

    def __call__(self, context: program.Program) -> None:
        base = self._apply(context)
        if base is not None:
            context.constr.extend(base._constrs)
            context.routine.extend(base._routine)

    @abc.abstractmethod
    def _apply(self, context: program.Program) -> None | CommandReturn:
        raise NotImplementedError
