from src import xbf

from .utils import run_and_eval_opcodes


def test_simple_sub() -> None:
    a = xbf.Unit()
    opcodes = [xbf.Init(a), xbf.Sub(a, 100, a)]

    memory = run_and_eval_opcodes(opcodes)
    assert memory[a] == 156


def test_sub_from_itself() -> None:
    a = xbf.Unit()
    opcodes = [xbf.Init(a), xbf.Sub(a, 10, a), xbf.Sub(a, a, a)]

    memory = run_and_eval_opcodes(opcodes)
    assert memory[a] == 0


def test_sub() -> None:
    a, b = xbf.Unit(), xbf.Unit()
    opcodes = [xbf.Init(a), xbf.Init(b), xbf.Sub(a, 10, a), xbf.Sub(b, a, b), xbf.Sub(b, 5, b)]

    memory = run_and_eval_opcodes(opcodes)
    assert memory[a] == 246
    assert memory[b] == 5


def test_sub_two() -> None:
    a, b = xbf.Unit("a"), xbf.Unit("b")
    opcodes = [
        xbf.Init(a),
        xbf.Init(b),
        xbf.Sub(a, 10, a),
        xbf.Add(b, 4, b),
        xbf.Sub(a, b, b),
        xbf.Sub(b, 6, b),
    ]

    memory = run_and_eval_opcodes(opcodes)
    assert memory[a] == 246
    assert memory[b] == 236


def test_sub_two_2() -> None:
    a, b = xbf.Unit(), xbf.Unit()
    opcodes = [
        xbf.Init(a),
        xbf.Init(b),
        xbf.Add(a, 10, a),
        xbf.Add(b, 4, b),
        xbf.Sub(a, b, a),
    ]

    memory = run_and_eval_opcodes(opcodes)
    assert memory[a] == 6
    assert memory[b] == 4


def test_sub_negative() -> None:
    a = xbf.Unit()
    opcodes = [xbf.Init(a), xbf.Sub(a, -5, a)]

    memory = run_and_eval_opcodes(opcodes)
    assert memory[a] == 5


def test_all_integers() -> None:
    a = xbf.Unit()
    opcodes = [xbf.Init(a), xbf.Sub(10, -5, a)]

    memory = run_and_eval_opcodes(opcodes)
    assert memory[a] == 15
