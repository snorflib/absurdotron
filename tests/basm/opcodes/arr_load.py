from src import basm

from .utils import execute_opcodes, ExecutorResults


def test_read_simple_int() -> None:
    arr = basm.Array(16)
    one_int = basm.Unit()
    opcodes = [
        basm.Init(arr),
        basm.Init(one_int),
        basm.ArrayStore(arr, 5, 5),
        basm.ArrayLoad(arr, [one_int], 5)
    ]

    exc = execute_opcodes(opcodes)

    assert exc.get_by_owner(one_int) == 5
    assert sum(exc.tape) == 10


def test_read_2_ints() -> None:
    arr = basm.Array(16)
    one = basm.Unit()
    two = basm.Unit()
    opcodes = [
        basm.Init(arr),
        basm.Init(one),
        basm.Init(two),
        basm.ArrayStore(arr, 5, 5),
        basm.ArrayStore(arr, 6, 6),
        basm.ArrayLoad(arr, [one, two], 5)
    ]

    exc = execute_opcodes(opcodes)

    assert exc.get_by_owner(one) == 5
    assert exc.get_by_owner(two) == 6
    assert sum(exc.tape) == 22


def test_read_by_units() -> None:
    arr = basm.Array(16, 2)
    idx = basm.Unit("idx")
    one = basm.Unit()
    two = basm.Unit()
    opcodes = [
        basm.Init(arr),
        basm.Init(idx),
        basm.Init(one),
        basm.Init(two),
        #
        basm.Assign(idx, 7),
        #
        basm.ArrayStore(arr, 2590, [idx]),
        basm.ArrayLoad(arr, [one, two], [idx])
    ]

    exc = execute_opcodes(opcodes)

    assert exc.get_by_owner(one) == 30
    assert exc.get_by_owner(two) == 10
    assert sum(exc.tape) == 87
