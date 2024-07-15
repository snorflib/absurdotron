from src import xbf

from .utils import run_and_eval_commands


def test_simple_sub() -> None:
    a = xbf.Unit()
    commands = [xbf.Init(a), xbf.SubUnit(a, 100, a)]

    memory = run_and_eval_commands(commands)
    assert memory[a] == 156


def test_sub_from_itself() -> None:
    a = xbf.Unit()
    commands = [xbf.Init(a), xbf.SubUnit(a, 10, a), xbf.SubUnit(a, a, a)]

    memory = run_and_eval_commands(commands)
    assert memory[a] == 0


def test_sub() -> None:
    a, b = xbf.Unit(), xbf.Unit()
    commands = [xbf.Init(a), xbf.Init(b), xbf.SubUnit(a, 10, a), xbf.SubUnit(b, a, b), xbf.SubUnit(b, 5, b)]

    memory = run_and_eval_commands(commands)
    assert memory[a] == 246
    assert memory[b] == 5


def test_sub_two() -> None:
    a, b = xbf.Unit(), xbf.Unit()
    commands = [
        xbf.Init(a),
        xbf.Init(b),
        xbf.SubUnit(a, 10, a),
        xbf.AddUnit(b, 4, b),
        xbf.SubUnit(a, b, b),
        xbf.SubUnit(b, 6, b),
    ]

    memory = run_and_eval_commands(commands)
    assert memory[a] == 246
    assert memory[b] == 236


def test_sub_two_2() -> None:
    a, b = xbf.Unit(), xbf.Unit()
    commands = [
        xbf.Init(a),
        xbf.Init(b),
        xbf.AddUnit(a, 10, a),
        xbf.AddUnit(b, 4, b),
        xbf.SubUnit(a, b, a),
    ]

    memory = run_and_eval_commands(commands)
    assert memory[a] == 6
    assert memory[b] == 4


def test_sub_negative() -> None:
    a = xbf.Unit()
    commands = [xbf.Init(a), xbf.SubUnit(a, -5, a)]

    memory = run_and_eval_commands(commands)
    assert memory[a] == 5
