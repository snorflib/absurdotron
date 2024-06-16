from src import xbf

from .utils import run_and_eval_commands_get_output


def test_display_simple() -> None:
    a = xbf.Unit()
    commands = [xbf.InitUnit(a), xbf.AddUnit(a, ord("a"), a), xbf.DisplayUnit(a)]

    data = run_and_eval_commands_get_output(commands)
    assert data == "a"
