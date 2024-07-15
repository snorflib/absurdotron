from src import xbf

from .utils import run_and_eval_commands


def test_calleq_only_if() -> None:
    a, b = xbf.Unit(), xbf.Unit()
    commands = [
        xbf.Init(a),
        xbf.Init(b),
        xbf.AddUnit(a, 15, a),
        xbf.AddUnit(b, 15, b),
        xbf.CallEq(
            a,
            b,
            if_=[
                xbf.AddUnit(b, 4, b),
            ],
        ),
    ]

    memory = run_and_eval_commands(commands)
    assert memory[a] == 15
    assert memory[b] == 19


def test_calleq_only_else() -> None:
    a, b = xbf.Unit("a"), xbf.Unit("b")
    commands = [
        xbf.Init(a),
        xbf.Init(b),
        xbf.AddUnit(a, 1, a),
        xbf.CallEq(
            a,
            b,
            else_=[
                xbf.AddUnit(b, 5, b),
            ],
        ),
    ]

    memory = run_and_eval_commands(commands)
    assert memory[a] == 1
    assert memory[b] == 5


def test_calleq_equal() -> None:
    a, b = xbf.Unit("a"), xbf.Unit("b")
    commands = [
        xbf.Init(a),
        xbf.Init(b),
        xbf.AddUnit(b, 5, b),
        xbf.CallEq(
            a,
            b,
            else_=[
                xbf.AddUnit(a, 5, a),
            ],
        ),
    ]

    memory = run_and_eval_commands(commands)
    assert memory[a] == 5
    assert memory[b] == 5


def test_calleq_nested() -> None:
    a, b = xbf.Unit(), xbf.Unit()
    commands = [
        xbf.Init(a),
        xbf.Init(b),
        xbf.AddUnit(b, 5, b),
        xbf.CallEq(
            a,
            b,
            else_=[
                xbf.AddUnit(a, 5, a),
                xbf.CallEq(
                    a,
                    b,
                    if_=[
                        xbf.AddUnit(b, 5, b),
                    ],
                ),
            ],
        ),
    ]

    memory = run_and_eval_commands(commands)
    assert memory[a] == 5
    assert memory[b] == 10
