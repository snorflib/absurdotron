from src import basm

from .utils import execute_opcodes


def test_simple_int_int() -> None:
    arr = basm.Array(16)
    opcodes = [
        basm.Init(arr),
        basm.ArrayStore(arr, 5, 5),
    ]

    exc = execute_opcodes(opcodes)

    assert exc.tape[_get_index(arr, 5)] == 5
    assert sum(exc.tape) == 5


def _get_index(arr: basm.Array, idx: int, offset: int = 1) -> int:
    part_width = arr.granularity + 1
    return part_width + idx * part_width + offset
