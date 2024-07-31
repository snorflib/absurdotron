from src import basm

from .utils import execute_opcodes_get_owner_values


def test_simple_mul() -> None:
    a = basm.Unit()
    opcodes = [basm.Init(a), basm.Add(a, 10, a), basm.Mul(a, 10, a)]

    memory = execute_opcodes_get_owner_values(opcodes)
    assert memory[a] == 100


def test_simple_two_arguments_mul() -> None:
    a, b = basm.Unit(), basm.Unit()
    opcodes = [basm.Init(a), basm.Init(b), basm.Add(a, 10, a), basm.Add(b, 5, b), basm.Mul(a, 10, b)]

    memory = execute_opcodes_get_owner_values(opcodes)
    assert memory[b] == 100
    assert memory[a] == 10


def test_multiply_by_zero() -> None:
    a, b = basm.Unit(), basm.Unit()
    opcodes = [
        basm.Init(a),
        basm.Init(b),
        basm.Add(b, 2, b),
        basm.Add(a, 10, a),
        basm.Mul(a, 0, b),
        basm.Add(a, 1, a),
        basm.Add(b, 1, b),
    ]

    memory = execute_opcodes_get_owner_values(opcodes)
    assert memory[a] == 11
    assert memory[b] == 1


def test_mul_by_itself_and_save_to_it() -> None:
    a = basm.Unit()
    opcodes = [basm.Init(a), basm.Add(a, 10, a), basm.Mul(a, a, a)]

    memory = execute_opcodes_get_owner_values(opcodes)
    assert memory[a] == 100


def test_mul_by_itself() -> None:
    a, b = basm.Unit(), basm.Unit()
    opcodes = [basm.Init(a), basm.Init(b), basm.Add(a, 10, a), basm.Add(b, 5, b), basm.Mul(b, b, a)]

    memory = execute_opcodes_get_owner_values(opcodes)
    assert memory[a] == 25
    assert memory[b] == 5


def test_mul_with_two_arguments() -> None:
    a, b, c = basm.Unit(), basm.Unit(), basm.Unit()
    opcodes = [
        basm.Init(a),
        basm.Init(b),
        basm.Init(c),
        basm.Add(a, 10, a),
        basm.Add(b, 4, b),
        basm.Mul(a, b, c),
        basm.Mul(c, b, c),
    ]

    memory = execute_opcodes_get_owner_values(opcodes)
    assert memory[a] == 10
    assert memory[b] == 4
    assert memory[c] == 160
