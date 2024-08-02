from src import basm

from .utils import execute_opcodes_get_owner_values


def test_simple_or() -> None:
    a = basm.Unit()
    opcodes = [basm.Init(a), basm.Add(a, 10, a), basm.Or(a, a, a)]

    memory = execute_opcodes_get_owner_values(opcodes)
    assert memory[a] == 10


def test_simple_or_zero() -> None:
    a = basm.Unit()
    opcodes = [basm.Init(a), basm.Add(a, 0, a), basm.Or(a, a, a)]

    memory = execute_opcodes_get_owner_values(opcodes)
    assert memory.get(a, 0) == 0


def test_simple_or_255() -> None:
    a = basm.Unit()
    opcodes = [basm.Init(a), basm.Add(a, 255, a), basm.Or(a, a, a)]

    memory = execute_opcodes_get_owner_values(opcodes)
    assert memory[a] == 255


def test_or_0_0() -> None:
    a, b, c = basm.Unit(), basm.Unit(), basm.Unit()
    opcodes = [
        basm.Init(a),
        basm.Init(b),
        basm.Init(c),
        basm.Or(a, b, c),
    ]

    memory = execute_opcodes_get_owner_values(opcodes)
    assert memory[a] == 0
    assert memory[b] == 0
    assert memory[c] == 0


def test_or_same_number_non_zero() -> None:
    a, b = basm.Unit(), basm.Unit()
    opcodes = [
        basm.Init(a),
        basm.Init(b),
        basm.Add(a, 44, a),
        basm.Add(b, 44, b),
        basm.Or(a, b, b),
    ]

    memory = execute_opcodes_get_owner_values(opcodes)

    assert memory[a] == 44
    assert memory[b] == 44


def test_or_zero_and_non_zero() -> None:
    a, b, c = basm.Unit(), basm.Unit(), basm.Unit()
    opcodes = [
        basm.Init(a),
        basm.Init(b),
        basm.Init(c),
        basm.Add(a, 0, a),
        basm.Add(b, 79, b),
        basm.Or(a, b, c),
    ]

    memory = execute_opcodes_get_owner_values(opcodes)
    assert memory[a] == 0
    assert memory[b] == 79
    assert memory[c] == 79


def test_or_non_zero_and_non_zero() -> None:
    a, b = basm.Unit(), basm.Unit()
    opcodes = [
        basm.Init(a),
        basm.Init(b),
        basm.Add(a, 13, a),
        basm.Add(b, 91, b),
        basm.Or(a, b, a),
    ]

    memory = execute_opcodes_get_owner_values(opcodes)
    assert memory[b] == 91
    assert memory[a] == 95


def test_or_non_zero_and_non_zero_2() -> None:
    a, b, c = basm.Unit(), basm.Unit(), basm.Unit()
    opcodes = [
        basm.Init(a),
        basm.Init(b),
        basm.Init(c),
        basm.Add(a, 167, a),
        basm.Add(b, 13, b),
        basm.Or(a, b, c),
    ]

    memory = execute_opcodes_get_owner_values(opcodes)
    assert memory[a] == 167
    assert memory[b] == 13
    assert memory[c] == 175


def test_or_in_row() -> None:
    a, b, c = basm.Unit(), basm.Unit(), basm.Unit()
    opcodes = [
        basm.Init(a),
        basm.Init(b),
        basm.Init(c),
        basm.Add(a, 155, a),
        basm.Add(b, 231, b),
        basm.Or(a, b, c),
        basm.Add(c, 5, c),
        basm.Or(c, b, a),
    ]

    memory = execute_opcodes_get_owner_values(opcodes)
    assert memory[a] == 231
    assert memory[b] == 231
    assert memory[c] == 4
