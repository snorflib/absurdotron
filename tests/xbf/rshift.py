from src import xbf

from .utils import run_and_eval_commands


def test_simple_rshift() -> None:
    a = xbf.Unit()
    commands = [xbf.InitUnit(a), xbf.AddUnit(a, 32, a), xbf.RShiftUnit(a, 4, a)]

    memory = run_and_eval_commands(commands)
    assert memory[a] == 2


def test_rshift_with_two_units() -> None:
    a, b = xbf.Unit("a"), xbf.Unit("b")
    commands = [
        xbf.InitUnit(a),
        xbf.InitUnit(b),
        xbf.AddUnit(a, 150, a),
        xbf.RShiftUnit(a, 5, b),
    ]

    memory = run_and_eval_commands(commands)
    assert memory[b] == 4
    assert memory[a] == 150


def test_out_of_bounds() -> None:
    a = xbf.Unit()
    commands = [xbf.InitUnit(a), xbf.AddUnit(a, 32, a), xbf.RShiftUnit(a, 6, a)]

    memory = run_and_eval_commands(commands)
    assert memory[a] == 0
