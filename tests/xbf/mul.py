from src import xbf

from .utils import run_and_eval_commands


def test_simple_mul() -> None:
    a = xbf.Unit()
    commands = [xbf.InitUnit(a), xbf.AddUnit(a, 10, a), xbf.MulUnit(a, 10, a)]

    memory = run_and_eval_commands(commands)
    assert memory[a] == 100


def test_simple_two_arguments_mul() -> None:
    a, b = xbf.Unit(), xbf.Unit()
    commands = [xbf.InitUnit(a), xbf.InitUnit(b), xbf.AddUnit(a, 10, a), xbf.AddUnit(b, 5, b), xbf.MulUnit(a, 10, b)]

    memory = run_and_eval_commands(commands)
    assert memory[b] == 105
    assert memory[a] == 10


def test_multiply_by_zero() -> None:
    a, b = xbf.Unit(), xbf.Unit()
    commands = [
        xbf.InitUnit(a),
        xbf.InitUnit(b),
        xbf.AddUnit(b, 2, b),
        xbf.AddUnit(a, 10, a),
        xbf.MulUnit(a, 0, b),
        xbf.AddUnit(a, 1, a),
        xbf.AddUnit(b, 1, b),
    ]

    memory = run_and_eval_commands(commands)
    assert memory[a] == 11
    assert memory[b] == 3


def test_mul_by_itself_and_save_to_it() -> None:
    a = xbf.Unit()
    commands = [xbf.InitUnit(a), xbf.AddUnit(a, 10, a), xbf.MulUnit(a, a, a)]

    memory = run_and_eval_commands(commands)
    assert memory[a] == 110  # 10 * 10 = 100 -> +10 before multiplication


def test_mul_by_itself() -> None:
    a, b = xbf.Unit(), xbf.Unit()
    commands = [xbf.InitUnit(a), xbf.InitUnit(b), xbf.AddUnit(a, 10, a), xbf.AddUnit(b, 5, b), xbf.MulUnit(b, b, a)]

    memory = run_and_eval_commands(commands)
    assert memory[a] == 35
    assert memory[b] == 5


def test_mul_with_two_arguments() -> None:
    a, b, c = xbf.Unit(), xbf.Unit(), xbf.Unit()
    commands = [
        xbf.InitUnit(a),
        xbf.InitUnit(b),
        xbf.InitUnit(c),
        xbf.AddUnit(a, 10, a),
        xbf.AddUnit(b, 4, b),
        xbf.MulUnit(a, b, c),
        xbf.MulUnit(c, b, c),
        xbf.AddUnit(a, 1, a),
    ]

    memory = run_and_eval_commands(commands)
    assert memory[a] == 11
    assert memory[b] == 4
    assert memory[c] == 200
