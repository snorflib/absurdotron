import io

import attrs
import bidict

from .memory import Memory
from .utils import build_jump_map


@attrs.define
class Executor:
    code: io.StringIO | str
    input: io.StringIO | None = None
    output: io.StringIO | None = None
    memory: Memory = attrs.field(factory=Memory)
    pc: int = attrs.field(init=False, default=0)
    jump_map: bidict.bidict[int, int] = attrs.field(init=None, factory=bidict.bidict)  # type: ignore

    def __call__(self) -> None:
        if isinstance(self.code, io.StringIO):
            self.code = self.code.getvalue()

        self.jump_map = build_jump_map(self.code)
        while self.pc < len(self.code):
            self._execute_command(self.code[self.pc])
            self.pc += 1

    def _execute_command(self, command: str) -> None:
        match command:
            case ">":
                self.memory.increment_ptr()
            case "<":
                self.memory.decrement_ptr()
            case "-":
                self.memory.decrement_data()
            case "+":
                self.memory.increment_data()
            case "[":
                if not self.memory.load():
                    self.pc = self.jump_map[self.pc]
            case "]":
                if self.memory.load():
                    self.pc = self.jump_map.inverse[self.pc]
            case ",":
                if self.input:
                    self.memory.store(self.input.read(1))
                    return

                self.memory.store(input()[0])
            case ".":
                if self.output:
                    self.output.write(chr(self.memory.load()))
                    return

                print(chr(self.memory.load()), end="")
