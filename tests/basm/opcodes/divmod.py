from src import basm

from .utils import execute_opcodes_get_owner_values


def test_integer_division_quotient() -> None:
    a, b = basm.Unit(), basm.Unit()
    opcodes = [
        basm.Init(a),
        basm.Init(b),
        basm.Add(a, 15, a),
        basm.DivMod(a, 4, quotient=b),
        basm.Add(b, 1, b),
    ]

    memory = execute_opcodes_get_owner_values(opcodes)
    assert memory[a] == 15
    assert memory[b] == 4


def test_integer_division_remainder() -> None:
    a, b = basm.Unit(), basm.Unit()
    opcodes = [
        basm.Init(a),
        basm.Init(b),
        basm.Add(a, 17, a),
        basm.DivMod(a, 4, remainder=b),
        basm.Add(b, 1, b),
        basm.Add(a, 1, a),
    ]

    memory = execute_opcodes_get_owner_values(opcodes)
    assert memory[a] == 18
    assert memory[b] == 2


def test_integer_remainder_is_divisor() -> None:
    a, b = basm.Unit(), basm.Unit()
    opcodes = [
        basm.Init(a),
        basm.Init(b),
        basm.Add(a, 6, a),
        basm.DivMod(a, 4, remainder=a),
    ]

    memory = execute_opcodes_get_owner_values(opcodes)
    assert memory[a] == 2


def test_integer_quotient_is_divisor() -> None:
    a, b = basm.Unit(), basm.Unit()
    opcodes = [
        basm.Init(a),
        basm.Init(b),
        basm.Add(a, 6, a),
        basm.DivMod(a, 4, quotient=a),
    ]

    memory = execute_opcodes_get_owner_values(opcodes)
    assert memory[a] == 1


def test_divmod_zero_division() -> None:
    a, b = basm.Unit(), basm.Unit()
    opcodes = [
        basm.Init(a),
        basm.Init(b),
        basm.Add(a, 6, a),
        basm.DivMod(a, 0, quotient=a),
    ]

    memory = execute_opcodes_get_owner_values(opcodes)
    assert memory[a] == 0


def test_all_arguments() -> None:
    a, b, c, d = basm.Unit(), basm.Unit(), basm.Unit(), basm.Unit()
    opcodes = [
        basm.Init(a),
        basm.Init(b),
        basm.Init(c),
        basm.Init(d),
        basm.Add(a, 147, a),
        basm.Add(c, 43, c),
        basm.DivMod(a, c, remainder=b, quotient=d),
    ]

    memory = execute_opcodes_get_owner_values(opcodes)
    assert memory[a] == 147
    assert memory[c] == 43
    assert memory[b] == 18
    assert memory[d] == 3


def test_zero_dividend() -> None:
    a, b = basm.Unit(), basm.Unit()
    opcodes = [
        basm.Init(a),
        basm.Init(b),
        basm.DivMod(a, 4, quotient=b, remainder=a),
    ]

    memory = execute_opcodes_get_owner_values(opcodes)

    assert memory[a] == 0
    assert memory[b] == 0


def test_division_by_integer_dividend_to_quotient() -> None:
    a, b = basm.Unit(), basm.Unit()
    opcodes = [
        basm.Init(a),
        basm.Init(b),
        basm.Add(a, 22, a),
        basm.DivMod(a, 4, quotient=a, remainder=b),
    ]

    memory = execute_opcodes_get_owner_values(opcodes)
    assert memory[a] == 5
    assert memory[b] == 2


def test_dividend_as_remainder() -> None:
    a, b = basm.Unit(), basm.Unit()
    opcodes = [
        basm.Init(a),
        basm.Add(a, 25, a),
        basm.Add(b, 6, b),
        basm.DivMod(a, b, remainder=a),
    ]

    memory = execute_opcodes_get_owner_values(opcodes)
    assert memory[a] == 1

def test_dividend_as_quotient() -> None:
    a, b = basm.Unit(), basm.Unit()
    opcodes = [
        basm.Init(a),
        basm.Add(a, 29, a),
        basm.Add(b, 7, b),
        basm.DivMod(a, b, quotient=a),
    ]

    memory = execute_opcodes_get_owner_values(opcodes)
    assert memory[a] == 4

def test_divisor_as_quotient() -> None:
    a, b = basm.Unit(), basm.Unit()
    opcodes = [
        basm.Init(a),
        basm.Init(b),
        basm.Add(a, 20, a),
        basm.Add(b, 4, b),
        basm.DivMod(a, b, quotient=b),
    ]

    memory = execute_opcodes_get_owner_values(opcodes)
    assert memory[a] == 20
    assert memory[b] == 5
def test_divisor_as_remainder() -> None:
    a, b = basm.Unit(), basm.Unit()
    opcodes = [
        basm.Init(a),
        basm.Init(b),
        basm.Add(a, 18, a),
        basm.Add(b, 5, b),
        basm.DivMod(a, b, remainder=b),
    ]

    memory = execute_opcodes_get_owner_values(opcodes)
    assert memory[a] == 18
    assert memory[b] == 3
