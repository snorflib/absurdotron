from src import xbf

from .utils import run_and_eval_opcodes_get_output


def test_display_simple() -> None:
    a = xbf.Unit()
    opcodes = [xbf.Init(a), xbf.Add(a, ord("a"), a), xbf.DisplayUnit(a)]

    data = run_and_eval_opcodes_get_output(opcodes)
    assert data == "a"
