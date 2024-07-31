from __future__ import annotations

import abc

import attrs

from src.basm.opcodes import context

from .return_ import OpCodeReturn


@attrs.frozen
class OpCode(abc.ABC):
    def __call__(self, context: context.Context) -> OpCodeReturn:
        return self._execute(context)

    @abc.abstractmethod
    def _execute(self, context: context.Context) -> OpCodeReturn:
        raise NotImplementedError
