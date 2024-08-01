from src import basm

from .utils import execute_opcodes_get_owner_values


def test_calleq_only_if() -> None:
    a, b = basm.Unit(), basm.Unit()
    opcodes = [
        basm.Init(a),
        basm.Init(b),
        basm.Add(a, 15, a),
        basm.Add(b, 15, b),
        basm.CallEq(
            a,
            b,
            if_eq=basm.Add(b, 4, b)(),
        ),
    ]

    memory = execute_opcodes_get_owner_values(opcodes)
    assert memory[a] == 15
    assert memory[b] == 19


def test_calleq_only_else() -> None:
    a, b = basm.Unit("a"), basm.Unit("b")
    opcodes = [
        basm.Init(a),
        basm.Init(b),
        basm.Add(a, 1, a),
        basm.CallEq(
            a,
            b,
            else_=basm.Add(b, 5, b)(),
        ),
    ]

    memory = execute_opcodes_get_owner_values(opcodes)
    assert memory[a] == 1
    assert memory[b] == 5


def test_calleq_equal() -> None:
    a, b = basm.Unit("a"), basm.Unit("b")
    opcodes = [
        basm.Init(a),
        basm.Init(b),
        basm.Add(b, 5, b),
        basm.CallEq(
            a,
            b,
            else_=basm.Add(a, 5, a)(),
        ),
    ]

    memory = execute_opcodes_get_owner_values(opcodes)
    assert memory[a] == 5
    assert memory[b] == 5


def test_calleq_nested() -> None:
    a, b = basm.Unit(), basm.Unit()
    opcodes = [
        basm.Init(a),
        basm.Init(b),
        basm.Add(b, 5, b),
        basm.CallEq(
            a,
            b,
            else_=basm.Add(a, 5, a)() \
                  | basm.CallEq(
                    a,
                    b,
                    if_eq=basm.Add(b, 5, b)(),
                )(),
        ),
    ]

    memory = execute_opcodes_get_owner_values(opcodes)
    assert memory[a] == 5
    assert memory[b] == 10
