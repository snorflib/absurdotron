from src import basm

from .utils import execute_opcodes, ExecutorResults


def test_int_int() -> None:
    arr = basm.Array(16)
    opcodes = [
        basm.Init(arr),
        basm.ArrayStore(arr, 5, 5),
    ]

    exc = execute_opcodes(opcodes)

    assert _get_value_by_index(exc, arr, 5) == 5
    assert sum(exc.tape) == 5


def test_zero_indexed() -> None:
    arr = basm.Array(16)
    opcodes = [
        basm.Init(arr),
        basm.ArrayStore(arr, 5, 0),
    ]

    exc = execute_opcodes(opcodes)

    assert _get_value_by_index(exc, arr, 0) == 5
    assert sum(exc.tape) == 5


def test_over_write() -> None:
    arr = basm.Array(16)
    opcodes = [
        basm.Init(arr),
        basm.ArrayStore(arr, 5, 15),
        basm.ArrayStore(arr, 8, 15),
    ]

    exc = execute_opcodes(opcodes)

    assert _get_value_by_index(exc, arr, 15) == 8
    assert sum(exc.tape) == 8


def test_place_multiple_bytes() -> None:
    arr = basm.Array(16)
    opcodes = [
        basm.Init(arr),
        basm.ArrayStore(arr, 65279, 5),
    ]

    exc = execute_opcodes(opcodes)

    assert _get_value_by_index(exc, arr, 5) == 255
    assert _get_value_by_index(exc, arr, 6) == 254
    assert sum(exc.tape) == 509


def test_place_multiple_bytes_granularity_2() -> None:
    arr = basm.Array(16, 2)
    opcodes = [
        basm.Init(arr),
        basm.ArrayStore(arr, 65279, 5),
    ]

    exc = execute_opcodes(opcodes)

    assert _get_value_by_index(exc, arr, 5) == 255
    assert _get_value_by_index(exc, arr, 5, offset=2) == 254
    assert sum(exc.tape) == 509


def test_place_multiple_bytes_partition_overflow() -> None:
    arr = basm.Array(16, 2)
    opcodes = [
        basm.Init(arr),
        basm.ArrayStore(arr, 16711677, 5),
    ]

    exc = execute_opcodes(opcodes)

    assert _get_value_by_index(exc, arr, 5) == 253
    assert _get_value_by_index(exc, arr, 5, offset=2) == 255
    assert _get_value_by_index(exc, arr, 6) == 254
    assert sum(exc.tape) == 762


def test_unit_assignment() -> None:
    arr = basm.Array(16)
    to_store = basm.Unit()
    opcodes = [
        basm.Init(arr),
        basm.Init(to_store),
        basm.Assign(to_store, 10),
        basm.ArrayStore(arr, [to_store], 9),
    ]

    exc = execute_opcodes(opcodes)

    assert _get_value_by_index(exc, arr, 9) == 10
    assert sum(exc.tape) == 20


def test_unit_assignment_gran() -> None:
    arr = basm.Array(16, 3)
    to_store = basm.Unit()
    opcodes = [
        basm.Init(arr),
        basm.Init(to_store),
        basm.Assign(to_store, 255),
        basm.ArrayStore(arr, [to_store], 100),
    ]

    exc = execute_opcodes(opcodes)

    assert _get_value_by_index(exc, arr, 100) == 255
    assert sum(exc.tape) == 510

def _get_value_by_index(exc: ExecutorResults, arr: basm.Array, idx: int, offset: int = 1) -> int:
    part_width = arr.granularity + 1
    rel_idx = part_width + idx * part_width + offset

    return exc.tape[exc.memory[arr] + rel_idx]
