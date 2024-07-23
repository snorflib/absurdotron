import typing

from src.basm.opcodes import base


class Memory(dict[str, type[base.OpCode[typing.Any]]]):
    ...
