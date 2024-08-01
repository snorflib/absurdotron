from src import basm

from .utils import execute_opcodes_get_owner_values


def test_callgt_only_if() -> None:
    a, b = basm.Unit(), basm.Unit()
    opcodes = [
        basm.Init(a),
        basm.Init(b),
        basm.Add(a, 15, a),
        basm.Add(b, 10, b),
        basm.CallGT(
            a,
            b,
            if_gt=basm.Add(b, 4, b)(),
        ),
    ]

    memory = execute_opcodes_get_owner_values(opcodes)
    assert memory[a] == 15
    assert memory[b] == 14


def test_callgt_only_else() -> None:
    a, b = basm.Unit("a"), basm.Unit("b")
    opcodes = [
        basm.Init(a),
        basm.Init(b),
        basm.CallGT(
            a,
            b,
            else_=basm.Add(b, 5, b)(),
        ),
    ]

    memory = execute_opcodes_get_owner_values(opcodes)
    assert memory[a] == 0
    assert memory[b] == 5


def test_callgt_equal_only_else_two() -> None:
    a, b = basm.Unit("a"), basm.Unit("b")
    opcodes = [
        basm.Init(a),
        basm.Init(b),
        basm.Add(a, 254, a),
        basm.Add(b, 255, b),
        basm.CallGT(
            a,
            b,
            else_=basm.Add(b, 5, b)(),
        ),
    ]

    memory = execute_opcodes_get_owner_values(opcodes)
    assert memory[a] == 254
    assert memory[b] == 4


def test_callgt_equal() -> None:
    a, b = basm.Unit("a"), basm.Unit("b")
    opcodes = [
        basm.Init(a),
        basm.Init(b),
        basm.Add(a, 5, a),
        basm.Add(b, 5, b),
        basm.CallGT(
            a,
            b,
            else_=basm.Add(a, 5, a)(),
        ),
    ]

    memory = execute_opcodes_get_owner_values(opcodes)
    assert memory[a] == 10
    assert memory[b] == 5


def test_callgt_nested() -> None:
    a, b = basm.Unit(), basm.Unit()
    opcodes = [
        basm.Init(a),
        basm.Init(b),
        basm.Add(b, 10, b),
        basm.CallGT(
            a,
            b,
            else_= basm.Add(a, 11, a)() | basm.CallGT(
                a,
                b,
                if_gt=basm.Add(b, 5, b)(),
            )()
        ),
    ]

    memory = execute_opcodes_get_owner_values(opcodes)
    assert memory[a] == 11
    assert memory[b] == 15
