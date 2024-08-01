from src import basm

from .utils import execute_opcodes_get_owner_values


def test_simple_and() -> None:
    a = basm.Unit()
    opcodes = [basm.Init(a), basm.Add(a, 10, a), basm.And(a, a, a)]

    memory = execute_opcodes_get_owner_values(opcodes)
    assert memory[a] == 10


def test_simple_and_zero() -> None:
    a = basm.Unit()
    opcodes = [basm.Init(a), basm.Add(a, 0, a), basm.And(a, a, a)]

    memory = execute_opcodes_get_owner_values(opcodes)
    assert memory.get(a, 0) == 0


def test_simple_and_255() -> None:
    a = basm.Unit()
    opcodes = [basm.Init(a), basm.Add(a, 255, a), basm.And(a, a, a)]

    memory = execute_opcodes_get_owner_values(opcodes)
    assert memory[a] == 255


def test_and_0_0() -> None:
    a, b, c = basm.Unit(), basm.Unit(), basm.Unit()
    opcodes = [
        basm.Init(a),
        basm.Init(b),
        basm.Init(c),
        basm.And(a, b, c),
    ]

    memory = execute_opcodes_get_owner_values(opcodes)
    assert memory[a] == 0
    assert memory[b] == 0
    assert memory[c] == 0


def test_and_same_number_non_zero() -> None:
    a, b = basm.Unit(), basm.Unit()
    opcodes = [
        basm.Init(a),
        basm.Init(b),
        basm.Add(a, 44, a),
        basm.Add(b, 44, b),
        basm.And(a, b, b),
    ]

    memory = execute_opcodes_get_owner_values(opcodes)

    assert memory[a] == 44
    assert memory[b] == 44


def test_and_zero_and_non_zero() -> None:
    a, b, c = basm.Unit(), basm.Unit(), basm.Unit()
    opcodes = [
        basm.Init(a),
        basm.Init(b),
        basm.Init(c),
        basm.Add(a, 0, a),
        basm.Add(b, 79, b),
        basm.And(a, b, c),
    ]

    memory = execute_opcodes_get_owner_values(opcodes)
    assert memory[a] == 0
    assert memory[b] == 79
    assert memory[c] == 0


def test_and_non_zero_and_non_zero() -> None:
    a, b = basm.Unit(), basm.Unit()
    opcodes = [
        basm.Init(a),
        basm.Init(b),
        basm.Add(a, 13, a),
        basm.Add(b, 91, b),
        basm.And(a, b, a),
    ]

    memory = execute_opcodes_get_owner_values(opcodes)
    assert memory[b] == 91
    assert memory[a] == 9


def test_and_non_zero_and_non_zero_2() -> None:
    a, b, c = basm.Unit(), basm.Unit(), basm.Unit()
    opcodes = [
        basm.Init(a),
        basm.Init(b),
        basm.Init(c),
        basm.Add(a, 167, a),
        basm.Add(b, 13, b),
        basm.And(a, b, c),
    ]

    memory = execute_opcodes_get_owner_values(opcodes)
    assert memory[a] == 167
    assert memory[b] == 13
    assert memory[c] == 5
