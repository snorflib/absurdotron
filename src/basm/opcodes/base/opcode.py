from __future__ import annotations

import abc
import typing

import attrs

from src.basm.opcodes import context

from .args import OpCodeArgs
from .return_ import OpCodeReturn

TArgs = typing.TypeVar("TArgs", bound=OpCodeArgs, covariant=True)


@attrs.frozen
class OpCode(abc.ABC, typing.Generic[TArgs]):
    args: TArgs

    def __call__(self, context: context.Context) -> OpCodeReturn:
        return self._execute(context)

    @abc.abstractmethod
    def _execute(self, context: context.Context) -> OpCodeReturn:
        raise NotImplementedError
