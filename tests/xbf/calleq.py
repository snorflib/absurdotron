from src import xbf

from .utils import run_and_eval_opcodes


def test_calleq_only_if() -> None:
    a, b = xbf.Unit(), xbf.Unit()
    opcodes = [
        xbf.Init(a),
        xbf.Init(b),
        xbf.Add(a, 15, a),
        xbf.Add(b, 15, b),
        xbf.CallEq(
            a,
            b,
            if_=[
                xbf.Add(b, 4, b),
            ],
        ),
    ]

    memory = run_and_eval_opcodes(opcodes)
    assert memory[a] == 15
    assert memory[b] == 19


def test_calleq_only_else() -> None:
    a, b = xbf.Unit("a"), xbf.Unit("b")
    opcodes = [
        xbf.Init(a),
        xbf.Init(b),
        xbf.Add(a, 1, a),
        xbf.CallEq(
            a,
            b,
            else_=[
                xbf.Add(b, 5, b),
            ],
        ),
    ]

    memory = run_and_eval_opcodes(opcodes)
    assert memory[a] == 1
    assert memory[b] == 5


def test_calleq_equal() -> None:
    a, b = xbf.Unit("a"), xbf.Unit("b")
    opcodes = [
        xbf.Init(a),
        xbf.Init(b),
        xbf.Add(b, 5, b),
        xbf.CallEq(
            a,
            b,
            else_=[
                xbf.Add(a, 5, a),
            ],
        ),
    ]

    memory = run_and_eval_opcodes(opcodes)
    assert memory[a] == 5
    assert memory[b] == 5


def test_calleq_nested() -> None:
    a, b = xbf.Unit(), xbf.Unit()
    opcodes = [
        xbf.Init(a),
        xbf.Init(b),
        xbf.Add(b, 5, b),
        xbf.CallEq(
            a,
            b,
            else_=[
                xbf.Add(a, 5, a),
                xbf.CallEq(
                    a,
                    b,
                    if_=[
                        xbf.Add(b, 5, b),
                    ],
                ),
            ],
        ),
    ]

    memory = run_and_eval_opcodes(opcodes)
    assert memory[a] == 5
    assert memory[b] == 10
