from src import xbf

from .utils import run_and_eval_opcodes


def test_clear() -> None:
    a = xbf.Unit()
    opcodes = [xbf.Init(a), xbf.Add(a, 50, a), xbf.ClearUnit(a)]

    memory = run_and_eval_opcodes(opcodes)
    assert memory[a] == 0
