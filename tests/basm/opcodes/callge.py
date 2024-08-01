from src import basm

from .utils import execute_opcodes_get_owner_values


def test_callge_only_if() -> None:
    a, b = basm.Unit(), basm.Unit()
    opcodes = [
        basm.Init(a),
        basm.Init(b),
        basm.Add(a, 15, a),
        basm.Add(b, 10, b),
        basm.CallGE(
            a,
            b,
            if_ge=basm.Add(b, 4, b)(),
        ),
    ]

    memory = execute_opcodes_get_owner_values(opcodes)
    assert memory[a] == 15
    assert memory[b] == 14


def test_callge_only_else() -> None:
    a, b = basm.Unit("a"), basm.Unit("b")
    opcodes = [
        basm.Init(a),
        basm.Init(b),
        basm.Add(b, 1, b),
        basm.CallGE(
            a,
            b,
            else_=basm.Add(b, 5, b)(),
        ),
    ]

    memory = execute_opcodes_get_owner_values(opcodes)
    assert memory[a] == 0
    assert memory[b] == 6


def test_callge_equal_only_else_two() -> None:
    a, b = basm.Unit("a"), basm.Unit("b")
    opcodes = [
        basm.Init(a),
        basm.Init(b),
        basm.Add(a, 254, a),
        basm.Add(b, 255, b),
        basm.CallGE(
            a,
            b,
            else_=basm.Add(b, 5, b)(),
        ),
    ]

    memory = execute_opcodes_get_owner_values(opcodes)
    assert memory[a] == 254
    assert memory[b] == 4


def test_callge_equal() -> None:
    a, b = basm.Unit("a"), basm.Unit("b")
    opcodes = [
        basm.Init(a),
        basm.Init(b),
        basm.Add(a, 5, a),
        basm.Add(b, 5, b),
        basm.CallGE(
            a,
            b,
            if_ge=basm.Add(a, 5, a)(),
        ),
    ]

    memory = execute_opcodes_get_owner_values(opcodes)
    assert memory[a] == 10
    assert memory[b] == 5


def test_callge_nested() -> None:
    a, b = basm.Unit(), basm.Unit()
    opcodes = [
        basm.Init(a),
        basm.Init(b),
        basm.Add(b, 10, b),
        basm.CallGE(
            a,
            b,
            else_=basm.Add(a, 10, a)() | basm.CallGE(
                    a,
                    b,
                    if_ge=basm.Add(b, 5, b)(),
                )(),
        ),
    ]

    memory = execute_opcodes_get_owner_values(opcodes)
    assert memory[a] == 10
    assert memory[b] == 15
