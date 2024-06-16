from src import xbf

from .utils import run_and_eval_commands


def test_clear() -> None:
    a = xbf.Unit()
    commands = [xbf.InitUnit(a), xbf.AddUnit(a, 50, a), xbf.ClearUnit(a)]

    memory = run_and_eval_commands(commands)
    assert memory[a] == 0
