from src import xbf

from .utils import run_and_eval_commands


def test_simple_lshift() -> None:
    a = xbf.Unit()
    commands = [xbf.InitUnit(a), xbf.AddUnit(a, 2, a), xbf.LShiftUnit(a, 4, a)]

    memory = run_and_eval_commands(commands)
    assert memory[a] == 32


def test_lshift_with_two_units() -> None:
    a, b = xbf.Unit("a"), xbf.Unit("b")
    commands = [
        xbf.InitUnit(a),
        xbf.InitUnit(b),
        xbf.AddUnit(a, 2, a),
        xbf.LShiftUnit(a, 5, b),
    ]

    memory = run_and_eval_commands(commands)
    assert memory[b] == 64
    assert memory[a] == 2
