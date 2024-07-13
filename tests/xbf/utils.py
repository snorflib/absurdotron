import io

from src import ir, memoptix, xbf
from src.bfrun import simple


def run_and_eval_commands_get_output(
    commands: list[xbf.BaseCommand],
    input: str | list[int] | None = None,
) -> str:
    program = eval_commands(commands)
    memory = resolve_program_memory(program)
    code = compile_routine_with_memory(program.routine, memory)

    output = eval_bf(code, input=input).output
    if output is None:
        return ""

    return output.getvalue()


def run_and_eval_commands_get_whole_tape(
    commands: list[xbf.BaseCommand],
    input: str | list[int] | None = None,
) -> tuple[list[int], dict[ir.Owner, int]]:
    program = eval_commands(commands)
    memory = resolve_program_memory(program)
    code = compile_routine_with_memory(program.routine, memory)

    tape = eval_bf(code, input=input).memory.cells
    return tape, memory


def run_and_eval_commands(
    commands: list[xbf.BaseCommand],
    input: str | list[int] | None = None,
) -> dict[ir.Owner, int]:
    program = eval_commands(commands)
    memory = resolve_program_memory(program)
    code = compile_routine_with_memory(program.routine, memory)

    tape = eval_bf(code, input=input).memory.cells
    for owner, index in memory.items():
        try:
            value: str | int = tape[index]
        except IndexError:
            value = 0

        memory[owner] = value if isinstance(value, int) else ord(value)

    return memory


def eval_commands(commands: list[xbf.BaseCommand]) -> xbf.Program:
    program = xbf.Program()
    for command in commands:
        command(program)
    return program


def resolve_program_memory(program: xbf.Program) -> dict[ir.Owner, int]:
    metainfo = memoptix.get_metainfo_from_routine(program.routine)
    resolver = memoptix.build_memory_resolver(program.constr, metainfo)

    return resolver.resolve()


def compile_routine_with_memory(routine: list[ir.BFToken], memory: dict[ir.Owner, int]) -> str:
    code = ir.Generator()(routine, memory)
    return code.source_code.getvalue()


def eval_bf(code: str, input: str | list[int] | None = "") -> simple.Executor:
    if isinstance(input, list):
        input_str: str = "".join([chr(c) for c in input])
    else:
        input_str = input or ""

    exc = simple.Executor(code, input=io.StringIO(input_str), output=io.StringIO())
    exc()

    return exc
