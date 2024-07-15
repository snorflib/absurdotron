from src import xbf

from .utils import run_and_eval_commands


def test_simple_add() -> None:
    a = xbf.Unit()
    commands = [xbf.Init(a), xbf.AddUnit(a, 50, a)]

    memory = run_and_eval_commands(commands)
    assert memory[a] == 50


def test_add_to_itself() -> None:
    a = xbf.Unit()
    commands = [xbf.Init(a), xbf.AddUnit(a, 10, a), xbf.AddUnit(a, a, a)]

    memory = run_and_eval_commands(commands)
    assert memory[a] == 20


def test_add_complex_one() -> None:
    a, b = xbf.Unit(), xbf.Unit()
    commands = [xbf.Init(a), xbf.Init(b), xbf.AddUnit(a, 10, a), xbf.AddUnit(b, a, b), xbf.AddUnit(b, 5, b)]

    memory = run_and_eval_commands(commands)
    assert memory[a] == 10
    assert memory[b] == 15


def test_add_complex_two() -> None:
    a, b = xbf.Unit(), xbf.Unit()
    commands = [
        xbf.Init(a),
        xbf.Init(b),
        xbf.AddUnit(a, 10, a),
        xbf.AddUnit(b, 5, b),
        xbf.AddUnit(a, b, b),
    ]

    memory = run_and_eval_commands(commands)
    assert memory[a] == 10
    assert memory[b] == 15


def test_add_three_args() -> None:
    a, b, c = xbf.Unit(), xbf.Unit(), xbf.Unit()
    commands = [
        xbf.Init(a),
        xbf.Init(b),
        xbf.Init(c),
        xbf.AddUnit(a, 10, a),
        xbf.AddUnit(b, 10, b),
        xbf.AddUnit(c, 10, c),
        xbf.AddUnit(b, a, c),
    ]

    memory = run_and_eval_commands(commands)
    assert memory[a] == 10
    assert memory[b] == 10
    assert memory[c] == 30


def test_add_negative() -> None:
    a = xbf.Unit()
    commands = [xbf.Init(a), xbf.AddUnit(a, -5, a)]

    memory = run_and_eval_commands(commands)
    assert memory[a] == 251


def test_save_target_to_add_target() -> None:
    a, b = xbf.Unit("a"), xbf.Unit("b")
    commands = [
        xbf.Init(a),
        xbf.Init(b),
        xbf.AddUnit(a, 10, a),
        xbf.AddUnit(b, 10, b),
        xbf.AddUnit(a, a, a),
        xbf.AddUnit(b, a, a),
    ]

    memory = run_and_eval_commands(commands)
    assert memory[a] == 30
    assert memory[b] == 10
