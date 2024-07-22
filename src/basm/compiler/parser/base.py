from __future__ import annotations

import abc
import typing

from src.utils import cls


def _preprocess_node_name(name: str) -> str:
    return name.lower().removeprefix("node").removesuffix("node")


class NodeMeta(abc.ABCMeta):
    name: str
    _nodes: dict[str, type[NodeMeta]] = {}

    def __init__(
        self,
        name: str,
        bases: tuple[type[BaseNode], ...],
        data: dict[str, typing.Any],
        *,
        preprocess: bool = True,
    ) -> None:
        name = _preprocess_node_name(name) if preprocess else name
        self._nodes[name] = NodeMeta
        self._name = name

    @classmethod
    def get_node(cls, name: str) -> type[NodeMeta]:
        return cls._nodes[name]


class BaseNode(metaclass=NodeMeta):
    __slots__ = ()


TCode = typing.TypeVar("TCode")
TNode = typing.TypeVar("TNode", bound=BaseNode)


class BaseParser(abc.ABC, typing.Generic[TCode, TNode], metaclass=cls.SingletonMeta):
    __slots__ = ()

    @abc.abstractmethod
    def parse(self, code: TCode) -> TNode:
        raise NotImplementedError
