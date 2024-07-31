from src import basm

from .utils import execute_opcodes_get_owner_values


def test_simple_add() -> None:
    a = basm.Unit()
    opcodes = [basm.Init(a), basm.Add(a, 50, a)]

    memory = execute_opcodes_get_owner_values(opcodes)
    assert memory[a] == 50


def test_add_to_itself() -> None:
    a = basm.Unit()
    opcodes = [basm.Init(a), basm.Add(a, 10, a), basm.Add(a, a, a)]

    memory = execute_opcodes_get_owner_values(opcodes)
    assert memory[a] == 20


def test_add_complex_one() -> None:
    a, b = basm.Unit(), basm.Unit()
    opcodes = [basm.Init(a), basm.Init(b), basm.Add(a, 10, a), basm.Add(b, a, b), basm.Add(b, 5, b)]

    memory = execute_opcodes_get_owner_values(opcodes)
    assert memory[a] == 10
    assert memory[b] == 15


def test_add_complex_two() -> None:
    a, b = basm.Unit(), basm.Unit()
    opcodes = [
        basm.Init(a),
        basm.Init(b),
        basm.Add(a, 10, a),
        basm.Add(b, 5, b),
        basm.Add(a, b, b),
    ]

    memory = execute_opcodes_get_owner_values(opcodes)
    assert memory[a] == 10
    assert memory[b] == 15


def test_add_three_args() -> None:
    a, b, c = basm.Unit(), basm.Unit(), basm.Unit()
    opcodes = [
        basm.Init(a),
        basm.Init(b),
        basm.Init(c),
        basm.Add(a, 10, a),
        basm.Add(b, 10, b),
        basm.Add(c, 10, c),
        basm.Add(b, a, c),
    ]

    memory = execute_opcodes_get_owner_values(opcodes)
    assert memory[a] == 10
    assert memory[b] == 10
    assert memory[c] == 20


def test_add_negative() -> None:
    a = basm.Unit()
    opcodes = [basm.Init(a), basm.Add(a, -5, a)]

    memory = execute_opcodes_get_owner_values(opcodes)
    assert memory[a] == 251


def test_save_target_to_add_target() -> None:
    a, b = basm.Unit("a"), basm.Unit("b")
    opcodes = [
        basm.Init(a),
        basm.Init(b),
        basm.Add(a, 10, a),
        basm.Add(b, 10, b),
        basm.Add(a, a, a),
        basm.Add(b, a, a),
    ]

    memory = execute_opcodes_get_owner_values(opcodes)
    assert memory[a] == 30
    assert memory[b] == 10
