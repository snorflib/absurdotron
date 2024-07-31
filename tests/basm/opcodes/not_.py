from src import basm

from .utils import execute_opcodes_get_owner_values


def test_simple_not() -> None:
    a = basm.Unit()
    opcodes = [basm.Init(a), basm.Add(a, 10, a), basm.Not(a, a)]

    memory = execute_opcodes_get_owner_values(opcodes)
    assert memory[a] == 245


def test_double_not() -> None:
    a = basm.Unit()
    opcodes = [basm.Init(a), basm.Add(a, 10, a), basm.Not(a, a), basm.Not(a, a)]

    memory = execute_opcodes_get_owner_values(opcodes)
    assert memory[a] == 10


def test_not_target_override() -> None:
    a, b = basm.Unit("a"), basm.Unit("b")
    opcodes = [
        basm.Init(a),
        basm.Init(b),
        basm.Add(a, 10, a),
        basm.Add(b, 10, b),
        basm.Not(a, b),
        basm.Not(b, a),
    ]

    memory = execute_opcodes_get_owner_values(opcodes)
    assert memory[a] == 10
    assert memory[b] == 245
