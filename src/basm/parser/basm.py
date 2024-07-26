from __future__ import annotations

import abc
import ast
import typing

import attrs
import pyparsing as pyp

from src.ir.exceptions import tokens

from .base import BaseNode, BaseNodeVisitor, BaseParser


class BASMNode(abc.ABC, BaseNode):
    __slots__ = ()

    @classmethod
    @abc.abstractmethod
    def from_parser_results(cls: type[typing.Self], results: pyp.results.ParseResults) -> typing.Self:
        raise NotImplementedError


TValue = typing.TypeVar("TValue", bound=int | str)


@attrs.frozen
class _ValueNode(BaseNode, typing.Generic[TValue]):
    value: TValue

    @classmethod
    def from_parser_results(cls: type[typing.Self], results: pyp.results.ParseResults) -> typing.Self:
        types_ = typing.get_args(cls.__orig_bases__[0])  # type: ignore
        if len(types_) != 1:
            raise ValueError(
                f"Generic node {cls.__name__} only supports one type conversion. "
                "Defined {len(types_)} types. {types_}"
            )

        try:
            pre_parsed_value = ast.literal_eval(results[0])
        except Exception:
            pre_parsed_value = results[0]

        return cls(types_[0](pre_parsed_value))


class StrNode(_ValueNode[str]):
    __slots__ = ()


class IdNode(_ValueNode[str]):
    __slots__ = ()


class HexNode(_ValueNode[int]):
    __slots__ = ()


class IntNode(_ValueNode[int]):
    __slots__ = ()


@attrs.frozen
class CallNode(BASMNode):
    opcode: IdNode
    args: list[_ValueNode[typing.Any]]

    @classmethod
    def from_parser_results(cls: type[typing.Self], results: pyp.results.ParseResults) -> typing.Self:
        return cls(*results.as_list()[0])


@attrs.frozen
class VarDefNode(BASMNode):
    dtype: IdNode
    params: list[HexNode | StrNode]
    vars: list[IdNode]

    @classmethod
    def from_parser_results(cls: type[typing.Self], results: pyp.results.ParseResults) -> typing.Self:
        return cls(*results.as_list()[0])


@attrs.frozen
class RootNode(BASMNode):
    nodes: list[CallNode | VarDefNode]

    @classmethod
    def from_parser_results(cls: type[typing.Self], results: pyp.results.ParseResults) -> typing.Self:
        return cls(results.as_list())


class BaseBASMVisitor(BaseNodeVisitor):
    def visit_StrNode(self, node: StrNode) -> typing.Any:
        ...

    def visit_HexNode(self, node: HexNode) -> typing.Any:
        ...

    def visit_IdNode(self, node: IdNode) -> typing.Any:
        ...

    def visit_CallNode(self, node: CallNode) -> typing.Any:
        ...

    def visit_VarDefNode(self, node: VarDefNode) -> typing.Any:
        ...

    def visit_RootNode(self, node: RootNode) -> typing.Any:
        ...


def _get_default_basm_parser() -> pyp.ParserElement:
    delimiter = pyp.Literal(",")
    line_end = pyp.Literal(";")
    type_dec = pyp.Keyword("dec")
    iargs_enter = pyp.Literal("<")
    iargs_exit = pyp.Literal(">")

    string = pyp.QuotedString(
        quote_char='"',
        end_quote_char='"',
        esc_char="\\",
        unquote_results=True,
        multiline=True,
    ).set_parse_action(StrNode.from_parser_results)

    hex_num = pyp.Combine(
        "0x" + pyp.Word(pyp.hexnums, min=1),
    ).set_parse_action(HexNode.from_parser_results)

    dec_num = pyp.Word(pyp.nums, min=1).set_parse_action(IntNode.from_parser_results)

    identifier = ~type_dec + pyp.Word(
        pyp.alphas + "_",
        pyp.alphanums + "_",
        min=1,
    )
    identifier.set_parse_action(IdNode.from_parser_results)

    arg = pyp.Or([identifier, hex_num, string, dec_num])

    args = pyp.delimitedList(arg, delim=delimiter)
    call = pyp.Group(identifier + pyp.Group(pyp.Optional(args)) + pyp.Suppress(line_end)).add_parse_action(
        CallNode.from_parser_results
    )

    literals = pyp.delimitedList(pyp.Or([hex_num, string, dec_num]), delim=delimiter)
    type_args = pyp.Suppress(iargs_enter) + literals + pyp.Suppress(iargs_exit)
    var_dec = pyp.Group(
        pyp.Suppress(type_dec)
        + identifier
        + pyp.Group(pyp.Optional(type_args))
        + pyp.Group(args)
        + pyp.Suppress(line_end)
    ).add_parse_action(VarDefNode.from_parser_results)

    root = pyp.OneOrMore(pyp.Or([var_dec, call])) + pyp.Suppress(pyp.StringEnd())  # type: ignore
    root.add_parse_action(RootNode.from_parser_results)

    return root


class BASMSyntaxError(BaseException):
    def __init__(self, code: str, location: int, expected: str) -> None:
        print(location)
        message = tokens._format_message(
            code,
            location,
            "^^^",
            expected,
        )
        super().__init__(message)


class BASMParser(BaseParser[str, RootNode]):
    _parser = _get_default_basm_parser()

    def parse(self, code: str) -> RootNode:
        try:
            result = self._parser.parseString(code, parse_all=True)
        except pyp.ParseException as exc:
            raise BASMSyntaxError(code, exc.loc, exc.msg) from exc

        return typing.cast(RootNode, result.as_list()[0])


def parse_basm(code: str) -> RootNode:
    return BASMParser().parse(code)
