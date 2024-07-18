from src import xbf

from .utils import run_and_eval_opcodes


def test_callneq_only_if() -> None:
    a, b = xbf.Unit(), xbf.Unit()
    opcodes = [
        xbf.Init(a),
        xbf.Init(b),
        xbf.Add(a, 14, a),
        xbf.Add(b, 15, b),
        xbf.CallNeq(
            a,
            b,
            if_=[
                xbf.Add(b, 4, b),
            ],
        ),
    ]

    memory = run_and_eval_opcodes(opcodes)
    assert memory[a] == 14
    assert memory[b] == 19


def test_callneq_only_else() -> None:
    a, b = xbf.Unit("a"), xbf.Unit("b")
    opcodes = [
        xbf.Init(a),
        xbf.Init(b),
        xbf.Add(b, 1, b),
        xbf.Add(a, 1, a),
        xbf.CallNeq(
            a,
            b,
            else_=[
                xbf.Add(b, 5, b),
            ],
        ),
    ]

    memory = run_and_eval_opcodes(opcodes)
    assert memory[a] == 1
    assert memory[b] == 6


def test_callneq_equal() -> None:
    a, b = xbf.Unit("a"), xbf.Unit("b")
    opcodes = [
        xbf.Init(a),
        xbf.Init(b),
        xbf.Add(a, 5, a),
        xbf.Add(b, 5, b),
        xbf.CallNeq(
            a,
            b,
            else_=[
                xbf.Add(a, 5, a),
            ],
        ),
    ]

    memory = run_and_eval_opcodes(opcodes)
    assert memory[a] == 10
    assert memory[b] == 5


def test_callneq_nested() -> None:
    a, b = xbf.Unit(), xbf.Unit()
    opcodes = [
        xbf.Init(a),
        xbf.Init(b),
        xbf.CallNeq(
            a,
            b,
            else_=[
                xbf.Add(a, 10, a),
                xbf.CallNeq(
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
    assert memory[a] == 10
    assert memory[b] == 5
