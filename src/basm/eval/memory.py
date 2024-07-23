import typing

from src.basm.opcodes import base


class Memory(dict[str, base.OpCode[typing.Any]]):
    ...
