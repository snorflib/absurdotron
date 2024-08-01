from src import basm

from .utils import execute_opcodes_get_owner_values


def test_callneq_only_if() -> None:
    a, b = basm.Unit(), basm.Unit()
    opcodes = [
        basm.Init(a),
        basm.Init(b),
        basm.Add(a, 14, a),
        basm.Add(b, 15, b),
        basm.CallNeq(
            a,
            b,
            if_neq=basm.Add(b, 4, b)(),
        ),
    ]

    memory = execute_opcodes_get_owner_values(opcodes)
    assert memory[a] == 14
    assert memory[b] == 19


def test_callneq_only_else() -> None:
    a, b = basm.Unit("a"), basm.Unit("b")
    opcodes = [
        basm.Init(a),
        basm.Init(b),
        basm.Add(b, 1, b),
        basm.Add(a, 1, a),
        basm.CallNeq(
            a,
            b,
            else_=basm.Add(b, 5, b)(),
        ),
    ]

    memory = execute_opcodes_get_owner_values(opcodes)
    assert memory[a] == 1
    assert memory[b] == 6


def test_callneq_equal() -> None:
    a, b = basm.Unit("a"), basm.Unit("b")
    opcodes = [
        basm.Init(a),
        basm.Init(b),
        basm.Add(a, 5, a),
        basm.Add(b, 5, b),
        basm.CallNeq(
            a,
            b,
            else_= basm.Add(a, 5, a)(),
        ),
    ]

    memory = execute_opcodes_get_owner_values(opcodes)
    assert memory[a] == 10
    assert memory[b] == 5


def test_callneq_nested() -> None:
    a, b = basm.Unit(), basm.Unit()
    opcodes = [
        basm.Init(a),
        basm.Init(b),
        basm.CallNeq(
            a,
            b,
            else_=basm.Add(a, 10, a)() |\
                basm.CallNeq(
                    a,
                    b,
                    if_neq=basm.Add(b, 5, b)(),
                )()
        ),
    ]

    memory = execute_opcodes_get_owner_values(opcodes)
    assert memory[a] == 10
    assert memory[b] == 5
