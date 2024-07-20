from src import xbf

from .utils import run_and_eval_opcodes


def test_simple_not() -> None:
    a = xbf.Unit()
    opcodes = [xbf.Init(a), xbf.Add(a, 10, a), xbf.Not(a, a)]

    memory = run_and_eval_opcodes(opcodes)
    assert memory[a] == 245


def test_double_not() -> None:
    a = xbf.Unit()
    opcodes = [xbf.Init(a), xbf.Add(a, 10, a), xbf.Not(a, a), xbf.Not(a, a)]

    memory = run_and_eval_opcodes(opcodes)
    assert memory[a] == 10


def test_not_target_override() -> None:
    a, b = xbf.Unit("a"), xbf.Unit("b")
    opcodes = [
        xbf.Init(a),
        xbf.Init(b),
        xbf.Add(a, 10, a),
        xbf.Add(b, 10, b),
        xbf.Not(a, b),
        xbf.Not(b, a),
    ]

    memory = run_and_eval_opcodes(opcodes)
    assert memory[a] == 10
    assert memory[b] == 245
