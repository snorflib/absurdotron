from src import xbf

from .utils import run_and_eval_commands


def test_simple_xor() -> None:
    a = xbf.Unit()
    commands = [xbf.InitUnit(a), xbf.AddUnit(a, 10, a), xbf.XorUnit(a, a, a)]

    memory = run_and_eval_commands(commands)
    assert memory[a] == 0


def test_simple_xor_zero() -> None:
    a = xbf.Unit()
    commands = [xbf.InitUnit(a), xbf.AddUnit(a, 0, a), xbf.XorUnit(a, a, a)]

    memory = run_and_eval_commands(commands)
    assert memory.get(a, 0) == 0


def test_simple_xor_255() -> None:
    a = xbf.Unit()
    commands = [xbf.InitUnit(a), xbf.AddUnit(a, 255, a), xbf.XorUnit(a, a, a)]

    memory = run_and_eval_commands(commands)
    assert memory[a] == 0


def test_xor_0_0() -> None:
    a, b, c = xbf.Unit(), xbf.Unit(), xbf.Unit()
    commands = [
        xbf.InitUnit(a),
        xbf.InitUnit(b),
        xbf.InitUnit(c),
        xbf.XorUnit(a, b, c),
    ]

    memory = run_and_eval_commands(commands)
    assert memory[a] == 0
    assert memory[b] == 0
    assert memory[c] == 0


def test_xor_same_number_non_zero() -> None:
    a, b = xbf.Unit(), xbf.Unit()
    commands = [
        xbf.InitUnit(a),
        xbf.InitUnit(b),
        xbf.AddUnit(a, 44, a),
        xbf.AddUnit(b, 44, b),
        xbf.XorUnit(a, b, b),
    ]

    memory = run_and_eval_commands(commands)

    assert memory[a] == 44
    assert memory[b] == 0


def test_xor_zero_and_non_zero() -> None:
    a, b, c = xbf.Unit(), xbf.Unit(), xbf.Unit()
    commands = [
        xbf.InitUnit(a),
        xbf.InitUnit(b),
        xbf.InitUnit(c),
        xbf.AddUnit(a, 0, a),
        xbf.AddUnit(b, 79, b),
        xbf.XorUnit(a, b, c),
    ]

    memory = run_and_eval_commands(commands)
    assert memory[a] == 0
    assert memory[b] == 79
    assert memory[c] == 79


def test_xor_non_zero_and_non_zero() -> None:
    a, b = xbf.Unit(), xbf.Unit()
    commands = [
        xbf.InitUnit(a),
        xbf.InitUnit(b),
        xbf.AddUnit(a, 13, a),
        xbf.AddUnit(b, 91, b),
        xbf.XorUnit(a, b, a)
    ]

    memory = run_and_eval_commands(commands)
    assert memory[b] == 91
    assert memory[a] == 86


def test_xor_non_zero_and_non_zero_2() -> None:
    a, b, c = xbf.Unit(), xbf.Unit(), xbf.Unit()
    commands = [
        xbf.InitUnit(a),
        xbf.InitUnit(b),
        xbf.InitUnit(c),
        xbf.AddUnit(a, 167, a),
        xbf.AddUnit(b, 13, b),
        xbf.XorUnit(a, b, c),
    ]

    memory = run_and_eval_commands(commands)
    assert memory[a] == 167
    assert memory[b] == 13
    assert memory[c] == 170


def test_xor_in_row() -> None:
    a, b, c = xbf.Unit(), xbf.Unit(), xbf.Unit()
    commands = [
        xbf.InitUnit(a),
        xbf.InitUnit(b),
        xbf.InitUnit(c),
        xbf.AddUnit(a, 155, a),
        xbf.AddUnit(b, 231, b),
        xbf.XorUnit(a, b, c),
        xbf.AddUnit(c, 5, c),
        xbf.XorUnit(c, b, a),
    ]

    memory = run_and_eval_commands(commands)
    assert memory[a] == 102
    assert memory[b] == 231
    assert memory[c] == 129
