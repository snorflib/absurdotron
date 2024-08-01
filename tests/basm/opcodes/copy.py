from src import basm

from .utils import execute_opcodes_get_owner_values


def test_copy_simple() -> None:
    a, b = basm.Unit(), basm.Unit()
    opcodes = [
        basm.Init(a),
        basm.Init(b),
        basm.Add(a, 10, a),
        basm.Copy(a, b),
    ]

    memory = execute_opcodes_get_owner_values(opcodes)
    assert memory[a] == 10
    assert memory[b] == 10


def test_copy_override() -> None:
    a, b = basm.Unit(), basm.Unit()
    opcodes = [
        basm.Init(a),
        basm.Init(b),
        basm.Add(a, 10, a),
        basm.Add(b, 15, b),
        basm.Copy(a, b),
    ]

    memory = execute_opcodes_get_owner_values(opcodes)
    assert memory[a] == 10
    assert memory[b] == 10
