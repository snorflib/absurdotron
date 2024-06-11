import collections.abc

import attrs

from src.ir import tokens, types

from .assembler import _assemble
from .code import Code
from .pointer import Pointer


@attrs.frozen
class Generator:
    code: Code = attrs.field(factory=Code)
    pointer: Pointer = attrs.field(default=None)

    def __attrs_post_init__(self) -> None:
        if self.pointer is None:
            object.__setattr__(self, "pointer", Pointer(self.code))

    def __call__(self, routine: collections.abc.Collection[tokens.BFToken], memory: dict[types.Owner, int]) -> Code:
        _assemble(self.code, self.pointer, routine, memory)
        return self.code
