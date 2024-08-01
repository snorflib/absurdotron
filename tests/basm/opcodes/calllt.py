from src import basm

from .utils import execute_opcodes_get_owner_values


def test_calllt_only_if() -> None:
    a, b = basm.Unit(), basm.Unit()
    opcodes = [
        basm.Init(a),
        basm.Init(b),
        basm.Add(a, 9, a),
        basm.Add(b, 10, b),
        basm.CallLT(
            a,
            b,
            if_lt=basm.Add(b, 4, b)(),
        ),
    ]

    memory = execute_opcodes_get_owner_values(opcodes)
    assert memory[a] == 9
    assert memory[b] == 14


def test_calllt_only_else() -> None:
    a, b = basm.Unit("a"), basm.Unit("b")
    opcodes = [
        basm.Init(a),
        basm.Init(b),
        basm.CallLT(
            a,
            b,
            else_=basm.Add(b, 5, b)(),
        ),
    ]

    memory = execute_opcodes_get_owner_values(opcodes)
    assert memory[a] == 0
    assert memory[b] == 5


def test_calllt_equal_only_else_two() -> None:
    a, b = basm.Unit("a"), basm.Unit("b")
    opcodes = [
        basm.Init(a),
        basm.Init(b),
        basm.Add(a, 5, a),
        basm.Add(b, 4, b),
        basm.CallLT(
            a,
            b,
            else_=basm.Add(b, 5, b)(),
        ),
    ]

    memory = execute_opcodes_get_owner_values(opcodes)
    assert memory[a] == 5
    assert memory[b] == 9


def test_calllt_equal() -> None:
    a, b = basm.Unit("a"), basm.Unit("b")
    opcodes = [
        basm.Init(a),
        basm.Init(b),
        basm.Add(a, 5, a),
        basm.Add(b, 5, b),
        basm.CallLT(
            a,
            b,
            else_=basm.Add(a, 5, a)(),
        ),
    ]

    memory = execute_opcodes_get_owner_values(opcodes)
    assert memory[a] == 10
    assert memory[b] == 5


def test_calllt_nested() -> None:
    a, b = basm.Unit(), basm.Unit()
    opcodes = [
        basm.Init(a),
        basm.Init(b),
        basm.Add(a, 1, a),
        basm.Add(b, 1, b),
        basm.CallLT(
            a,
            b,
            else_=basm.Add(b, 1, b)() | basm.CallLT(
                    a,
                    b,
                    if_lt=basm.Add(b, 5, b)(),
                )()
        ),
    ]

    memory = execute_opcodes_get_owner_values(opcodes)
    assert memory[a] == 1
    assert memory[b] == 7
