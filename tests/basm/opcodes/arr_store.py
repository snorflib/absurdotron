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


def test_multiple_units_assignment() -> None:
    arr = basm.Array(16, 3)
    to_store, to_store_one = basm.Unit(), basm.Unit()
    opcodes = [
        basm.Init(arr),
        basm.Init(to_store),
        basm.Init(to_store_one),
        basm.Assign(to_store, 255),
        basm.Assign(to_store_one, 5),
        basm.ArrayStore(arr, [to_store, to_store_one], 0),
    ]

    exc = execute_opcodes(opcodes)

    assert _get_value_by_index(exc, arr, 0) == 255
    assert _get_value_by_index(exc, arr, 0, offset=2) == 5
    assert sum(exc.tape) == 520


def test_multiple_units_assignment_partition_overflow() -> None:
    arr = basm.Array(16, 2)
    to_store, to_store_one, to_store_sec = basm.Unit(), basm.Unit(), basm.Unit()
    opcodes = [
        basm.Init(arr),
        basm.Init(to_store),
        basm.Init(to_store_one),
        basm.Init(to_store_sec),
        basm.Assign(to_store, 255),
        basm.Assign(to_store_one, 5),
        basm.Assign(to_store_sec, 25),
        basm.ArrayStore(arr, [to_store, to_store_one, to_store_sec], 50),
    ]

    exc = execute_opcodes(opcodes)

    assert _get_value_by_index(exc, arr, 50) == 255
    assert _get_value_by_index(exc, arr, 50, offset=2) == 5
    assert _get_value_by_index(exc, arr, 51) == 25
    assert sum(exc.tape) == 570


def test_unit_assignment_overwrite() -> None:
    arr = basm.Array(16)
    to_store, to_store_one = basm.Unit(), basm.Unit()
    opcodes = [
        basm.Init(arr),
        basm.Init(to_store),
        basm.Init(to_store_one),
        basm.Assign(to_store, 255),
        basm.ArrayStore(arr, [to_store], 10),
        basm.Assign(to_store_one, 5),
        basm.ArrayStore(arr, [to_store_one], 10),
    ]

    exc = execute_opcodes(opcodes)

    assert _get_value_by_index(exc, arr, 10) == 5
    assert sum(exc.tape) == 265


def test_unit_idx() -> None:
    arr = basm.Array(16)
    idx = basm.Unit()
    opcodes = [
        basm.Init(arr),
        basm.Init(idx),
        basm.Assign(idx, 10),
        basm.ArrayStore(arr, 26, [idx]),
    ]

    exc = execute_opcodes(opcodes)

    assert _get_value_by_index(exc, arr, 10) == 26
    assert sum(exc.tape) == 36


def test_unit_idx_reassign() -> None:
    arr = basm.Array(16)
    idx = basm.Unit()
    opcodes = [
        basm.Init(arr),
        basm.Init(idx),
        basm.Assign(idx, 10),
        basm.ArrayStore(arr, 26, [idx]),
        basm.ArrayStore(arr, 5, [idx]),
    ]

    exc = execute_opcodes(opcodes)

    assert _get_value_by_index(exc, arr, 10) == 5
    assert sum(exc.tape) == 15


def test_unit_idx_partition_overflow() -> None:
    arr = basm.Array(16, granularity=2)
    idx = basm.Unit()
    opcodes = [
        basm.Init(arr),
        basm.Init(idx),
        basm.Assign(idx, 10),
        basm.ArrayStore(arr, 16711677, [idx]),
    ]

    exc = execute_opcodes(opcodes)

    assert _get_value_by_index(exc, arr, 10) == 253
    assert _get_value_by_index(exc, arr, 10, offset=2) == 255
    assert _get_value_by_index(exc, arr, 11) == 254
    assert sum(exc.tape) == 772


def test_large_index() -> None:
    arr = basm.Array(16, granularity=2)
    idx, idx1, idx2 = basm.Unit(), basm.Unit(), basm.Unit()
    opcodes = [
        basm.Init(arr),
        basm.Init(idx),
        basm.Init(idx1),
        basm.Init(idx2),
        basm.Assign(idx, 5),
        basm.Assign(idx1, 3),
        basm.Assign(idx2, 3),
        basm.ArrayStore(arr, 260, [idx, idx1, idx2]),
    ]

    exc = execute_opcodes(opcodes)

    assert _get_value_by_index(exc, arr, 197381) == 4
    assert _get_value_by_index(exc, arr, 197381, offset=2) == 1
    assert sum(exc.tape) == 16


def test_unit_value_and_idx() -> None:
    arr = basm.Array(16)
    idx = basm.Unit()
    to_store = basm.Unit()
    opcodes = [
        basm.Init(arr),
        basm.Init(idx),
        basm.Init(to_store),
        basm.Assign(idx, 10),
        basm.Assign(to_store, 15),
        basm.ArrayStore(arr, [to_store], [idx]),
    ]

    exc = execute_opcodes(opcodes)

    assert _get_value_by_index(exc, arr, 10) == 15
    assert sum(exc.tape) == 40


def test_units_and_indexes() -> None:
    arr = basm.Array(16, 2)
    idx, idx1 = basm.Unit(), basm.Unit()
    to_store, to_store1, to_store2 = basm.Unit(), basm.Unit(), basm.Unit()
    opcodes = [
        basm.Init(arr),
        basm.Init(idx),
        basm.Init(idx1),
        basm.Init(to_store),
        basm.Init(to_store1),
        basm.Init(to_store2),
        basm.Assign(idx, 10),
        basm.Assign(idx1, 10),
        basm.Assign(to_store, 15),
        basm.Assign(to_store1, 16),
        basm.Assign(to_store2, 17),
        basm.ArrayStore(arr, [to_store, to_store1, to_store2], [idx, idx1]),
        basm.Assign(to_store1, 5),
        basm.ArrayStore(arr, [to_store, to_store1], 2570),
    ]

    exc = execute_opcodes(opcodes)

    assert _get_value_by_index(exc, arr, 2570) == 15
    assert _get_value_by_index(exc, arr, 2570, offset=2) == 5
    assert _get_value_by_index(exc, arr, 2571) == 17
    assert sum(exc.tape) == 94


def test_mixed() -> None:
    arr = basm.Array(16, 3)
    idx, idx1 = basm.Unit(), basm.Unit()
    to_store, to_store1 = basm.Unit(), basm.Unit()
    opcodes = [
        basm.Init(arr),
        basm.Init(idx),
        basm.Init(idx1),
        basm.Init(to_store),
        basm.Init(to_store1),
        basm.Assign(idx, 34),
        basm.Assign(idx1, 5),
        basm.Assign(to_store, 10),
        basm.Assign(to_store1, 20),
        basm.ArrayStore(arr, [to_store], [idx, idx1]),
        basm.ArrayStore(arr, [to_store1], 1314),
        basm.ArrayStore(arr, [to_store1], [idx]),
        basm.ArrayStore(arr, 99, [idx]),
        basm.ArrayStore(arr, [idx], [idx1]),
        basm.ArrayStore(arr, 1, 34),
    ]

    exc = execute_opcodes(opcodes)

    assert _get_value_by_index(exc, arr, 1314) == 20
    assert _get_value_by_index(exc, arr, 34) == 1
    assert _get_value_by_index(exc, arr, 5) == 34
    assert sum(exc.tape) == 124



def _get_value_by_index(exc: ExecutorResults, arr: basm.Array, idx: int, offset: int = 1) -> int:
    part_width = arr.granularity + 1
    rel_idx = part_width + idx * part_width + offset

    return exc.tape[exc.memory[arr] + rel_idx]
