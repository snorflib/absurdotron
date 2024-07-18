from src import xbf

from .utils import run_and_eval_opcodes


def test_copy_simple() -> None:
    a, b = xbf.Unit(), xbf.Unit()
    opcodes = [
        xbf.Init(a),
        xbf.Init(b),
        xbf.Add(a, 10, a),
        xbf.CopyUnit(a, b),
    ]

    memory = run_and_eval_opcodes(opcodes)
    assert memory[a] == 10
    assert memory[b] == 10


def test_copy_override() -> None:
    a, b = xbf.Unit(), xbf.Unit()
    opcodes = [
        xbf.Init(a),
        xbf.Init(b),
        xbf.Add(a, 10, a),
        xbf.Add(b, 15, b),
        xbf.CopyUnit(a, b),
    ]

    memory = run_and_eval_opcodes(opcodes)
    assert memory[a] == 10
    assert memory[b] == 10
