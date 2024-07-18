from src import xbf

from .utils import run_and_eval_opcodes


def test_assign_zero() -> None:
    a = xbf.Unit()
    opcodes = [xbf.Init(a), xbf.Add(a, 50, a), xbf.AssignUnit(a, 0)]

    memory = run_and_eval_opcodes(opcodes)
    assert memory[a] == 0


def test_assign_override() -> None:
    a = xbf.Unit()
    opcodes = [xbf.Init(a), xbf.Add(a, 50, a), xbf.AssignUnit(a, 5)]

    memory = run_and_eval_opcodes(opcodes)
    assert memory[a] == 5
