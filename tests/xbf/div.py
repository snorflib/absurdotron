from src import xbf

from .utils import run_and_eval_commands


def test_simple_div() -> None:
    a = xbf.Unit()
    commands = [xbf.InitUnit(a), xbf.AddUnit(a, 50, a), xbf.DivUnit(a, 10, a)]

    memory = run_and_eval_commands(commands)
    assert memory[a] == 5


def test_zero_division() -> None:
    a = xbf.Unit()
    commands = [xbf.InitUnit(a), xbf.AddUnit(a, 50, a), xbf.DivUnit(a, 0, a)]

    memory = run_and_eval_commands(commands)
    assert memory[a] == 0


def test_two_arguments() -> None:
    a, b = xbf.Unit(), xbf.Unit()
    commands = [xbf.InitUnit(a), xbf.InitUnit(b), xbf.AddUnit(a, 50, a), xbf.DivUnit(a, 20, b)]

    memory = run_and_eval_commands(commands)
    assert memory[a] == 50
    assert memory[b] == 2
