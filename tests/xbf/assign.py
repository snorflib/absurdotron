from src import xbf

from .utils import run_and_eval_commands


def test_assign_zero() -> None:
    a = xbf.Unit()
    commands = [xbf.InitUnit(a), xbf.AddUnit(a, 50, a), xbf.AssignUnit(a, 0)]

    memory = run_and_eval_commands(commands)
    assert memory[a] == 0


def test_assign_override() -> None:
    a = xbf.Unit()
    commands = [xbf.InitUnit(a), xbf.AddUnit(a, 50, a), xbf.AssignUnit(a, 5)]

    memory = run_and_eval_commands(commands)
    assert memory[a] == 5
