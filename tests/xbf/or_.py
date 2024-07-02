from src import xbf

from .utils import run_and_eval_commands


def test_simple_or() -> None:
    a = xbf.Unit()
    commands = [xbf.InitUnit(a), xbf.AddUnit(a, 10, a), xbf.OrUnit(a, a, a)]

    memory = run_and_eval_commands(commands)
    assert memory[a] == 10


def test_simple_or_zero() -> None:
    a = xbf.Unit()
    commands = [xbf.InitUnit(a), xbf.AddUnit(a, 0, a), xbf.OrUnit(a, a, a)]

    memory = run_and_eval_commands(commands)
    assert memory.get(a, 0) == 0


def test_simple_or_255() -> None:
    a = xbf.Unit()
    commands = [xbf.InitUnit(a), xbf.AddUnit(a, 255, a), xbf.OrUnit(a, a, a)]

    memory = run_and_eval_commands(commands)
    assert memory[a] == 255


def test_or_0_0() -> None:
    a, b, c = xbf.Unit(), xbf.Unit(), xbf.Unit()
    commands = [
        xbf.InitUnit(a),
        xbf.InitUnit(b),
        xbf.InitUnit(c),
        xbf.OrUnit(a, b, c),
    ]

    memory = run_and_eval_commands(commands)
    assert memory[a] == 0
    assert memory[b] == 0
    assert memory[c] == 0


def test_or_same_number_non_zero() -> None:
    a, b = xbf.Unit(), xbf.Unit()
    commands = [
        xbf.InitUnit(a),
        xbf.InitUnit(b),
        xbf.AddUnit(a, 44, a),
        xbf.AddUnit(b, 44, b),
        xbf.OrUnit(a, b, b),
    ]

    memory = run_and_eval_commands(commands)

    assert memory[a] == 44
    assert memory[b] == 44


def test_or_zero_and_non_zero() -> None:
    a, b, c = xbf.Unit(), xbf.Unit(), xbf.Unit()
    commands = [
        xbf.InitUnit(a),
        xbf.InitUnit(b),
        xbf.InitUnit(c),
        xbf.AddUnit(a, 0, a),
        xbf.AddUnit(b, 79, b),
        xbf.OrUnit(a, b, c),
    ]

    memory = run_and_eval_commands(commands)
    assert memory[a] == 0
    assert memory[b] == 79
    assert memory[c] == 0


def test_or_non_zero_and_non_zero() -> None:
    a, b = xbf.Unit(), xbf.Unit()
    commands = [
        xbf.InitUnit(a),
        xbf.InitUnit(b),
        xbf.AddUnit(a, 13, a),
        xbf.AddUnit(b, 91, b),
        xbf.AndUnit(a, b, a),
    ]

    memory = run_and_eval_commands(commands)
    assert memory[b] == 91
    assert memory[a] == 95


def test_or_non_zero_and_non_zero_2() -> None:
    a, b, c = xbf.Unit(), xbf.Unit(), xbf.Unit()
    commands = [
        xbf.InitUnit(a),
        xbf.InitUnit(b),
        xbf.InitUnit(c),
        xbf.AddUnit(a, 167, a),
        xbf.AddUnit(b, 13, b),
        xbf.AndUnit(a, b, c),
    ]

    memory = run_and_eval_commands(commands)
    assert memory[a] == 167
    assert memory[b] == 13
    assert memory[c] == 175


def test_or_in_row() -> None:
    a, b, c = xbf.Unit(), xbf.Unit(), xbf.Unit()
    commands = [
        xbf.InitUnit(a),
        xbf.InitUnit(b),
        xbf.InitUnit(c),
        xbf.AddUnit(a, 155, a),
        xbf.AddUnit(b, 231, b),
        xbf.OrUnit(a, b, c),
        xbf.AddUnit(c, 5, c),
        xbf.OrUnit(c, b, a),
    ]

    memory = run_and_eval_commands(commands)
    assert memory[a] == 155
    assert memory[b] == 231
    assert memory[c] == 4
