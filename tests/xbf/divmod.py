from src import xbf

from .utils import run_and_eval_opcodes


def test_integer_division_quotient() -> None:
    a, b = xbf.Unit(), xbf.Unit()
    opcodes = [
        xbf.Init(a),
        xbf.Init(b),
        xbf.Add(a, 15, a),
        xbf.DivMod(a, 4, quotient=b),
        xbf.Add(b, 1, b),
    ]

    memory = run_and_eval_opcodes(opcodes)
    assert memory[a] == 15
    assert memory[b] == 4


def test_integer_division_remainder() -> None:
    a, b = xbf.Unit(), xbf.Unit()
    opcodes = [
        xbf.Init(a),
        xbf.Init(b),
        xbf.Add(a, 17, a),
        xbf.DivMod(a, 4, remainder=b),
        xbf.Add(b, 1, b),
        xbf.Add(a, 1, a),
    ]

    memory = run_and_eval_opcodes(opcodes)
    assert memory[a] == 18
    assert memory[b] == 2


def test_integer_remainder_is_divisor() -> None:
    a, b = xbf.Unit(), xbf.Unit()
    opcodes = [
        xbf.Init(a),
        xbf.Init(b),
        xbf.Add(a, 6, a),
        xbf.DivMod(a, 4, remainder=a),
    ]

    memory = run_and_eval_opcodes(opcodes)
    assert memory[a] == 2


def test_integer_quotient_is_divisor() -> None:
    a, b = xbf.Unit(), xbf.Unit()
    opcodes = [
        xbf.Init(a),
        xbf.Init(b),
        xbf.Add(a, 6, a),
        xbf.DivMod(a, 4, quotient=a),
    ]

    memory = run_and_eval_opcodes(opcodes)
    assert memory[a] == 1


def test_divmod_zero_division() -> None:
    a, b = xbf.Unit(), xbf.Unit()
    opcodes = [
        xbf.Init(a),
        xbf.Init(b),
        xbf.Add(a, 6, a),
        xbf.DivMod(a, 0, quotient=a),
    ]

    memory = run_and_eval_opcodes(opcodes)
    assert memory[a] == 0


def test_all_arguments() -> None:
    a, b, c, d = xbf.Unit(), xbf.Unit(), xbf.Unit(), xbf.Unit()
    opcodes = [
        xbf.Init(a),
        xbf.Init(b),
        xbf.Init(c),
        xbf.Init(d),
        xbf.Add(a, 6, a),
        xbf.Add(c, 4, c),
        xbf.DivMod(a, c, quotient=b, remainder=d),
        xbf.Add(a, 1, a),
        xbf.Add(c, 1, c),
        xbf.Add(b, 1, b),
    ]

    memory = run_and_eval_opcodes(opcodes)
    assert memory[a] == 7
    assert memory[c] == 5
    assert memory[b] == 2
    assert memory[d] == 2


def test_zero_dividend() -> None:
    a, b = xbf.Unit(), xbf.Unit()
    opcodes = [
        xbf.Init(a),
        xbf.Init(b),
        xbf.DivMod(a, 4, quotient=b, remainder=a),
    ]

    memory = run_and_eval_opcodes(opcodes)

    assert memory[a] == 0
    assert memory[b] == 0


def test_division_by_integer_dividend_to_quotient() -> None:
    a, b = xbf.Unit(), xbf.Unit()
    opcodes = [
        xbf.Init(a),
        xbf.Init(b),
        xbf.AssignUnit(a, 22),
        xbf.DivMod(a, 4, quotient=a, remainder=b),
    ]

    memory = run_and_eval_opcodes(opcodes)
    assert memory[a] == 5
    assert memory[b] == 2
