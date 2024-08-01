from __future__ import annotations

import abc
import typing

import attrs

from src.basm.opcodes import context

if typing.TYPE_CHECKING:
    from .return_ import OpCodeReturn


@attrs.frozen
class OpCode(abc.ABC):
    def __call__(self) -> OpCodeReturn:
        return self._execute(context)

    @abc.abstractmethod
    def _execute(self) -> OpCodeReturn:
        raise NotImplementedError
