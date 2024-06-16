from src import xbf

from .utils import run_and_eval_commands


def test_input_add() -> None:
    a = xbf.Unit()
    commands = [xbf.InitUnit(a), xbf.InputUnit(a)]

    memory = run_and_eval_commands(
        commands,
        input=[
            50,
        ],
    )
    assert memory[a] == 50


def test_input_override() -> None:
    a = xbf.Unit()
    commands = [xbf.InitUnit(a), xbf.InputUnit(a), xbf.InputUnit(a)]

    memory = run_and_eval_commands(
        commands,
        input=[
            50,
            10,
        ],
    )
    assert memory[a] == 10
