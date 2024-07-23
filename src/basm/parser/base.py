from __future__ import annotations

import abc
import typing


def _preprocess_node_name(name: str) -> str:
    return name.lower().removeprefix("node").removesuffix("node")


class BaseNode:
    __slots__ = ()


class BaseNodeVisitor:
    __slots__ = ()

    def visit(self, node: BaseNode) -> typing.Any:
        return getattr(self, "visit_" + type(node).__name__, self._default_visit)(node)

    def _default_visit(self, node: BaseNode) -> None:
        return None


TCode = typing.TypeVar("TCode")
TNode = typing.TypeVar("TNode", bound=BaseNode)


class BaseParser(abc.ABC, typing.Generic[TCode, TNode]):
    __slots__ = ()

    @abc.abstractmethod
    def parse(self, code: TCode) -> TNode:
        raise NotImplementedError
