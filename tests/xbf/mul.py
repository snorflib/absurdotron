from src import xbf

from .utils import run_and_eval_opcodes


def test_simple_mul() -> None:
    a = xbf.Unit()
    opcodes = [xbf.Init(a), xbf.Add(a, 10, a), xbf.MulUnit(a, 10, a)]

    memory = run_and_eval_opcodes(opcodes)
    assert memory[a] == 100


def test_simple_two_arguments_mul() -> None:
    a, b = xbf.Unit(), xbf.Unit()
    opcodes = [xbf.Init(a), xbf.Init(b), xbf.Add(a, 10, a), xbf.Add(b, 5, b), xbf.MulUnit(a, 10, b)]

    memory = run_and_eval_opcodes(opcodes)
    assert memory[b] == 100
    assert memory[a] == 10


def test_multiply_by_zero() -> None:
    a, b = xbf.Unit(), xbf.Unit()
    opcodes = [
        xbf.Init(a),
        xbf.Init(b),
        xbf.Add(b, 2, b),
        xbf.Add(a, 10, a),
        xbf.MulUnit(a, 0, b),
        xbf.Add(a, 1, a),
        xbf.Add(b, 1, b),
    ]

    memory = run_and_eval_opcodes(opcodes)
    assert memory[a] == 11
    assert memory[b] == 3


def test_mul_by_itself_and_save_to_it() -> None:
    a = xbf.Unit()
    opcodes = [xbf.Init(a), xbf.Add(a, 10, a), xbf.MulUnit(a, a, a)]

    memory = run_and_eval_opcodes(opcodes)
    assert memory[a] == 110  # 10 * 10 = 100 -> +10 before multiplication


def test_mul_by_itself() -> None:
    a, b = xbf.Unit(), xbf.Unit()
    opcodes = [xbf.Init(a), xbf.Init(b), xbf.Add(a, 10, a), xbf.Add(b, 5, b), xbf.MulUnit(b, b, a)]

    memory = run_and_eval_opcodes(opcodes)
    assert memory[a] == 25
    assert memory[b] == 5


def test_mul_with_two_arguments() -> None:
    a, b, c = xbf.Unit(), xbf.Unit(), xbf.Unit()
    opcodes = [
        xbf.Init(a),
        xbf.Init(b),
        xbf.Init(c),
        xbf.Add(a, 10, a),
        xbf.Add(b, 4, b),
        xbf.MulUnit(a, b, c),
        xbf.MulUnit(c, b, c),
        xbf.Add(a, 1, a),
    ]

    memory = run_and_eval_opcodes(opcodes)
    assert memory[a] == 11
    assert memory[b] == 4
    assert memory[c] == 200
