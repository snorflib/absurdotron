from __future__ import annotations

import abc
import ast
import typing

import attrs
import pyparsing

from .base import BaseNode, BaseParser


class BASMNode(abc.ABC, BaseNode):
    __slots__ = ()

    @classmethod
    @abc.abstractmethod
    def from_parser_results(cls: type[typing.Self], results: pyparsing.results.ParseResults) -> typing.Self:
        raise NotImplementedError


TValue = typing.TypeVar("TValue", bound=int | str)


@attrs.frozen
class _ValueNode(BaseNode, typing.Generic[TValue]):
    value: TValue

    @classmethod
    def from_parser_results(cls: type[typing.Self], results: pyparsing.results.ParseResults) -> typing.Self:
        types_ = typing.get_args(cls.__orig_bases__[0])  # type: ignore
        if len(types_) != 1:
            raise ValueError(
                f"Generic node {cls.__name__} only supports one type conversion. "
                "Defined {len(types_)} types. {types_}"
            )

        try:
            pre_parsed_value = ast.literal_eval(results[0])
        except ValueError:
            pre_parsed_value = results[0]

        return cls(types_[0](pre_parsed_value))


class StrNode(_ValueNode[str]):
    __slots__ = ()


class IdNode(_ValueNode[str]):
    __slots__ = ()


class HexNode(_ValueNode[int]):
    __slots__ = ()


@attrs.frozen
class CallNode(BASMNode):
    opcode: IdNode
    args: list[_ValueNode[typing.Any]]

    @classmethod
    def from_parser_results(cls: type[typing.Self], results: pyparsing.results.ParseResults) -> typing.Self:
        return cls(*results.as_list()[0])


@attrs.frozen
class RootNode(BASMNode):
    calls: list[CallNode]

    @classmethod
    def from_parser_results(cls: type[typing.Self], results: pyparsing.results.ParseResults) -> typing.Self:
        return cls(results.as_list())


def _get_default_basm_parser() -> pyparsing.ParserElement:
    string = pyparsing.QuotedString(
        quoteChar='"',
        escChar="\\",
        unquoteResults=True,
        multiline=True,
    ).set_parse_action(StrNode.from_parser_results)

    hex_num = pyparsing.Combine(
        "0x" + pyparsing.Word(pyparsing.hexnums, min=1),
    ).set_parse_action(HexNode.from_parser_results)

    identifier = pyparsing.Word(
        pyparsing.alphas + "_",
        pyparsing.alphanums + "_",
        min=1,
    ).set_parse_action(IdNode.from_parser_results)

    arg = pyparsing.Or([identifier, hex_num, string])

    delimiter = pyparsing.Literal(",")
    line_end = pyparsing.Literal(";")

    args = pyparsing.Group(pyparsing.delimitedList(arg, delim=delimiter))
    call = pyparsing.Group(identifier + args + pyparsing.Suppress(line_end)).add_parse_action(
        CallNode.from_parser_results
    )

    root = pyparsing.OneOrMore(call) + pyparsing.Suppress(pyparsing.StringEnd())  # type: ignore
    root.add_parse_action(RootNode.from_parser_results)

    return root


class BASMParser(BaseParser[str, RootNode]):
    _parser = _get_default_basm_parser()

    def parse(self, code: str) -> RootNode:
        result = self._parser.parseString(code, parse_all=True)
        return typing.cast(RootNode, result.as_list()[0])


def parse_basm(code: str) -> RootNode:
    return BASMParser().parse(code)
