import collections.abc
import io

import attrs

from src import ir, memoptix
from src.basm import opcodes
from src.bfrun import simple


@attrs.frozen
class ExecutorResults:
    tape: list[int]
    memory: dict[ir.Owner, int]
    input: io.StringIO | None = None
    output: io.StringIO | None = None

    def get_by_owner(self, owner: ir.Owner) -> int:
        try:
            value: int = self.tape[self.memory[owner]]
        except IndexError:
            value = 0

        return value

    def output_as_str(self) -> str:
        return self.output.getvalue() if self.output else ""


def execute_opcodes_get_owner_values(opcodes_: list[opcodes.OpCode]) -> dict[ir.Owner, int]:
    result = execute_opcodes(opcodes_)
    owner2value = {}
    for owner in result.memory:
        owner2value[owner] = result.get_by_owner(owner)
    return owner2value


def execute_opcodes(
    opcodes_: list[opcodes.OpCode], input: io.StringIO | None = None, output: io.StringIO | None = None
) -> ExecutorResults:
    program = eval_opcodes(opcodes_)
    memory = resolve_program_memory(program.routine, program.constrs)
    code = compile_routine_with_memory(program.routine, memory)

    executor = eval_bf(code, input=input, output=output)
    return ExecutorResults(executor.memory.cells, memory, executor.input, executor.output)


def eval_opcodes(opcodes_: list[opcodes.OpCode]) -> opcodes.OpCodeReturn:
    opcode_return = opcodes.OpCodeReturn()
    for opcode_ in opcodes_:
        opcode_return |= opcode_()
    return opcode_return


def resolve_program_memory(
    routine: collections.abc.Sequence[ir.BFToken],
    constrs: collections.abc.Sequence[memoptix.BaseConstraint],
) -> dict[ir.Owner, int]:
    metainfo = memoptix.get_metainfo_from_routine(routine)
    resolver = memoptix.build_memory_resolver(constrs, metainfo)

    return resolver.resolve()


def compile_routine_with_memory(routine: list[ir.BFToken], memory: dict[ir.Owner, int]) -> str:
    code = ir.Generator()(routine, memory)
    code.save("hello.txt")
    return code.source_code.getvalue()


def eval_bf(code: str, input: io.StringIO | None = None, output: io.StringIO | None = None) -> simple.Executor:
    exc = simple.Executor(code, input=input, output=output)
    exc()

    return exc
