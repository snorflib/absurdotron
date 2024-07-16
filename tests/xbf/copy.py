from src import xbf

from .utils import run_and_eval_commands


def test_copy_simple() -> None:
    a, b = xbf.Unit(), xbf.Unit()
    commands = [
        xbf.Init(a),
        xbf.Init(b),
        xbf.Add(a, 10, a),
        xbf.CopyUnit(a, b),
    ]

    memory = run_and_eval_commands(commands)
    assert memory[a] == 10
    assert memory[b] == 10


def test_copy_override() -> None:
    a, b = xbf.Unit(), xbf.Unit()
    commands = [
        xbf.Init(a),
        xbf.Init(b),
        xbf.Add(a, 10, a),
        xbf.Add(b, 15, b),
        xbf.CopyUnit(a, b),
    ]

    memory = run_and_eval_commands(commands)
    assert memory[a] == 10
    assert memory[b] == 10
