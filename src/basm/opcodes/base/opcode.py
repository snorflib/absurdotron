from __future__ import annotations

import abc
import typing

import attrs

from src.basm import context

from .args import OpCodeArgs
from .return_ import OpCodeReturn

TArgs = typing.TypeVar("TArgs", bound=OpCodeArgs, covariant=True)


class OpCodeRegistry(abc.ABCMeta):
    name: str
    opcodes: dict[str, OpCodeRegistry] = {}

    def __init__(
        self,
        name: str,
        bases: tuple[OpCodeRegistry, ...],
        data: dict[str, typing.Any],
        *,
        preprocess: bool = True,
    ) -> None:
        self.opcodes[name] = self
        self.name = name

    @classmethod
    def get_node(cls, name: str) -> OpCodeRegistry:
        return cls.opcodes[name]


@attrs.frozen
class OpCode(abc.ABC, typing.Generic[TArgs], metaclass=OpCodeRegistry):
    args: TArgs

    def __call__(self, context: context.Context) -> OpCodeReturn:
        return self._execute(context)

    @abc.abstractmethod
    def _execute(self, context: context.Context) -> OpCodeReturn:
        raise NotImplementedError
