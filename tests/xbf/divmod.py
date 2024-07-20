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
        xbf.Add(a, 147, a),
        xbf.Add(c, 43, c),
        xbf.DivMod(a, c, remainder=b, quotient=d),
    ]

    memory = run_and_eval_opcodes(opcodes)
    assert memory[a] == 147
    assert memory[c] == 43
    assert memory[b] == 18
    assert memory[d] == 3


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
        xbf.Add(a, 22, a),
        xbf.DivMod(a, 4, quotient=a, remainder=b),
    ]

    memory = run_and_eval_opcodes(opcodes)
    assert memory[a] == 5
    assert memory[b] == 2


def test_dividend_as_remainder() -> None:
    a, b = xbf.Unit(), xbf.Unit()
    opcodes = [
        xbf.Init(a),
        xbf.Add(a, 25, a),
        xbf.Add(b, 6, b),
        xbf.DivMod(a, b, remainder=a),
    ]

    memory = run_and_eval_opcodes(opcodes)
    assert memory[a] == 1

def test_dividend_as_quotient() -> None:
    a, b = xbf.Unit(), xbf.Unit()
    opcodes = [
        xbf.Init(a),
        xbf.Add(a, 29, a),
        xbf.Add(b, 7, b),
        xbf.DivMod(a, b, quotient=a),
    ]

    memory = run_and_eval_opcodes(opcodes)
    assert memory[a] == 4

def test_divisor_as_quotient() -> None:
    a, b = xbf.Unit(), xbf.Unit()
    opcodes = [
        xbf.Init(a),
        xbf.Init(b),
        xbf.Add(a, 20, a),
        xbf.Add(b, 4, b),
        xbf.DivMod(a, b, quotient=b),
    ]

    memory = run_and_eval_opcodes(opcodes)
    assert memory[a] == 20
    assert memory[b] == 5
def test_divisor_as_remainder() -> None:
    a, b = xbf.Unit(), xbf.Unit()
    opcodes = [
        xbf.Init(a),
        xbf.Init(b),
        xbf.Add(a, 18, a),
        xbf.Add(b, 5, b),
        xbf.DivMod(a, b, remainder=b),
    ]

    memory = run_and_eval_opcodes(opcodes)
    assert memory[a] == 18
    assert memory[b] == 3
