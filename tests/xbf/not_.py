from src import xbf

from .utils import run_and_eval_commands


def test_simple_not() -> None:
    a = xbf.Unit()
    commands = [xbf.Init(a), xbf.AddUnit(a, 10, a), xbf.NotUnit(a, a)]

    memory = run_and_eval_commands(commands)
    assert memory[a] == 245


def test_double_not() -> None:
    a = xbf.Unit()
    commands = [xbf.Init(a), xbf.AddUnit(a, 10, a), xbf.NotUnit(a, a), xbf.NotUnit(a, a)]

    memory = run_and_eval_commands(commands)
    assert memory[a] == 10


def test_not_target_override() -> None:
    a, b = xbf.Unit("a"), xbf.Unit("b")
    commands = [
        xbf.Init(a),
        xbf.Init(b),
        xbf.AddUnit(a, 10, a),
        xbf.AddUnit(b, 10, b),
        xbf.NotUnit(a, b),
        xbf.NotUnit(b, a),
    ]

    memory = run_and_eval_commands(commands)
    assert memory[a] == 10
    assert memory[b] == 245
