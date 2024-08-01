from src import basm

from .utils import execute_opcodes_get_owner_values


def test_callle_only_if() -> None:
    a, b = basm.Unit(), basm.Unit()
    opcodes = [
        basm.Init(a),
        basm.Init(b),
        basm.Add(a, 9, a),
        basm.Add(b, 10, b),
        basm.CallLE(
            a,
            b,
            if_le=basm.Add(b, 4, b)(),
        ),
    ]

    memory = execute_opcodes_get_owner_values(opcodes)
    assert memory[a] == 9
    assert memory[b] == 14


def test_callle_only_else() -> None:
    a, b = basm.Unit("a"), basm.Unit("b")
    opcodes = [
        basm.Init(a),
        basm.Init(b),
        basm.Add(a, 1, a),
        basm.CallLE(
            a,
            b,
            else_=basm.Add(b, 5, b)(),
        ),
    ]

    memory = execute_opcodes_get_owner_values(opcodes)
    assert memory[a] == 1
    assert memory[b] == 5


def test_callle_only_else_two() -> None:
    a, b = basm.Unit("a"), basm.Unit("b")
    opcodes = [
        basm.Init(a),
        basm.Init(b),
        basm.Add(a, 1, a),
        basm.CallLE(
            a,
            b,
            else_=basm.Add(b, 5, b)(),
        ),
    ]

    memory = execute_opcodes_get_owner_values(opcodes)
    assert memory[a] == 1
    assert memory[b] == 5


def test_callle_equal() -> None:
    a, b = basm.Unit("a"), basm.Unit("b")
    opcodes = [
        basm.Init(a),
        basm.Init(b),
        basm.Add(a, 5, a),
        basm.Add(b, 5, b),
        basm.CallLE(
            a,
            b,
            if_le=basm.Add(a, 5, a)(),
        ),
    ]

    memory = execute_opcodes_get_owner_values(opcodes)
    assert memory[a] == 10
    assert memory[b] == 5


def test_callle_nested() -> None:
    a, b = basm.Unit(), basm.Unit()
    opcodes = [
        basm.Init(a),
        basm.Init(b),
        basm.Add(a, 2, a),
        basm.Add(b, 1, b),
        basm.CallLE(
            a,
            b,
            else_=basm.Add(b, 1, b)() | basm.CallLE(
                    a,
                    b,
                    if_le=basm.Add(b, 5, b)()
                )(),
        ),
    ]

    memory = execute_opcodes_get_owner_values(opcodes)
    assert memory[a] == 2
    assert memory[b] == 7
