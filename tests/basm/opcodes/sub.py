from src import basm

from .utils import execute_opcodes_get_owner_values


def test_simple_sub() -> None:
    a = basm.Unit()
    opcodes = [basm.Init(a), basm.Sub(a, 100, a)]

    memory = execute_opcodes_get_owner_values(opcodes)
    assert memory[a] == 156


def test_sub_from_itself() -> None:
    a = basm.Unit()
    opcodes = [basm.Init(a), basm.Sub(a, 10, a), basm.Sub(a, a, a)]

    memory = execute_opcodes_get_owner_values(opcodes)
    assert memory[a] == 0


def test_sub() -> None:
    a, b = basm.Unit(), basm.Unit()
    opcodes = [basm.Init(a), basm.Init(b), basm.Sub(a, 10, a), basm.Sub(b, a, b), basm.Sub(b, 5, b)]

    memory = execute_opcodes_get_owner_values(opcodes)
    assert memory[a] == 246
    assert memory[b] == 5


def test_sub_two() -> None:
    a, b = basm.Unit("a"), basm.Unit("b")
    opcodes = [
        basm.Init(a),
        basm.Init(b),
        basm.Sub(a, 10, a),
        basm.Add(b, 4, b),
        basm.Sub(a, b, b),
        basm.Sub(b, 6, b),
    ]

    memory = execute_opcodes_get_owner_values(opcodes)
    assert memory[a] == 246
    assert memory[b] == 236


def test_sub_two_2() -> None:
    a, b = basm.Unit(), basm.Unit()
    opcodes = [
        basm.Init(a),
        basm.Init(b),
        basm.Add(a, 10, a),
        basm.Add(b, 4, b),
        basm.Sub(a, b, a),
    ]

    memory = execute_opcodes_get_owner_values(opcodes)
    assert memory[a] == 6
    assert memory[b] == 4


def test_sub_negative() -> None:
    a = basm.Unit()
    opcodes = [basm.Init(a), basm.Sub(a, -5, a)]

    memory = execute_opcodes_get_owner_values(opcodes)
    assert memory[a] == 5


def test_all_integers() -> None:
    a = basm.Unit()
    opcodes = [basm.Init(a), basm.Sub(10, -5, a)]

    memory = execute_opcodes_get_owner_values(opcodes)
    assert memory[a] == 15
