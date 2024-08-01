from src import basm

from .utils import execute_opcodes_get_owner_values


def test_callz_only_if() -> None:
    a, b = basm.Unit(), basm.Unit()
    opcodes = [
        basm.Init(a),
        basm.Init(b),
        basm.Add(a, 1, a),
        basm.CallZ(
            a,
            else_=basm.Add(b, 5, b)(),
        ),
    ]

    memory = execute_opcodes_get_owner_values(opcodes)
    assert memory[a] == 1
    assert memory[b] == 5


def test_callz_only_else() -> None:
    a, b = basm.Unit("a"), basm.Unit("b")
    opcodes = [
        basm.Init(a),
        basm.Init(b),
        basm.CallZ(
            a,
            if_zero=basm.Add(b, 5, b)(),
        ),
    ]

    memory = execute_opcodes_get_owner_values(opcodes)
    assert memory[a] == 0
    assert memory[b] == 5


def test_callz_nested() -> None:
    a, b = basm.Unit(), basm.Unit()
    opcodes = [
        basm.Init(a),
        basm.Init(b),
        basm.CallZ(
            a,
            if_zero=basm.Add(a, 1, a)()
            | basm.CallZ(
                a,
                else_=basm.Add(b, 5, b)(),
            )(),
        ),
    ]

    memory = execute_opcodes_get_owner_values(opcodes)
    assert memory[a] == 1
    assert memory[b] == 5
