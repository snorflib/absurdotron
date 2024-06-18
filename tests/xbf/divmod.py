from src import xbf

from .utils import run_and_eval_commands


def test_integer_division_quotient() -> None:
    a, b = xbf.Unit(), xbf.Unit()
    commands = [
        xbf.InitUnit(a),
        xbf.InitUnit(b),
        xbf.AddUnit(a, 15, a),
        xbf.DivModUnit(a, 4, quotient=b),
        xbf.AddUnit(b, 1, b),
    ]

    memory = run_and_eval_commands(commands)
    assert memory[a] == 15
    assert memory[b] == 4


def test_integer_division_remainder() -> None:
    a, b = xbf.Unit(), xbf.Unit()
    commands = [
        xbf.InitUnit(a),
        xbf.InitUnit(b),
        xbf.AddUnit(a, 17, a),
        xbf.DivModUnit(a, 4, remainder=b),
        xbf.AddUnit(b, 1, b),
        xbf.AddUnit(a, 1, a),
    ]

    memory = run_and_eval_commands(commands)
    assert memory[a] == 18
    assert memory[b] == 2


def test_integer_remainder_is_divisor() -> None:
    a, b = xbf.Unit(), xbf.Unit()
    commands = [
        xbf.InitUnit(a),
        xbf.InitUnit(b),
        xbf.AddUnit(a, 6, a),
        xbf.DivModUnit(a, 4, remainder=a),
    ]

    memory = run_and_eval_commands(commands)
    assert memory[a] == 2


def test_integer_quotient_is_divisor() -> None:
    a, b = xbf.Unit(), xbf.Unit()
    commands = [
        xbf.InitUnit(a),
        xbf.InitUnit(b),
        xbf.AddUnit(a, 6, a),
        xbf.DivModUnit(a, 4, quotient=a),
    ]

    memory = run_and_eval_commands(commands)
    assert memory[a] == 1

def test_divmod_zero_division() -> None:
    a, b = xbf.Unit(), xbf.Unit()
    commands = [
        xbf.InitUnit(a),
        xbf.InitUnit(b),
        xbf.AddUnit(a, 6, a),
        xbf.DivModUnit(a, 0, quotient=a),
    ]

    memory = run_and_eval_commands(commands)
    assert memory[a] == 0


def test_all_arguments() -> None:
    a, b, c, d = xbf.Unit(), xbf.Unit(), xbf.Unit(), xbf.Unit()
    commands = [
        xbf.InitUnit(a),
        xbf.InitUnit(b),
        xbf.InitUnit(c),
        xbf.InitUnit(d),
        xbf.AddUnit(a, 6, a),
        xbf.AddUnit(c, 4, c),
        xbf.DivModUnit(a, c, quotient=b, remainder=d),
        xbf.AddUnit(a, 1, a),
        xbf.AddUnit(c, 1, c),
        xbf.AddUnit(b, 1, b),
    ]

    memory = run_and_eval_commands(commands)
    assert memory[a] == 7
    assert memory[c] == 5
    assert memory[b] == 2
    assert memory[d] == 2


def test_zero_dividend() -> None:
    a, b = xbf.Unit(), xbf.Unit()
    commands = [
        xbf.InitUnit(a),
        xbf.InitUnit(b),
        xbf.DivModUnit(a, 4, quotient=b, remainder=a),
    ]

    memory = run_and_eval_commands(commands)

    assert memory[a] == 0
    assert memory[b] == 0
