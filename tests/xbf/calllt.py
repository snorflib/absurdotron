from src import xbf

from .utils import run_and_eval_commands


def test_calllt_only_if() -> None:
    a, b = xbf.Unit(), xbf.Unit()
    commands = [
        xbf.Init(a),
        xbf.Init(b),
        xbf.AddUnit(a, 9, a),
        xbf.AddUnit(b, 10, b),
        xbf.CallLT(
            a,
            b,
            if_=[
                xbf.AddUnit(b, 4, b),
            ],
        ),
    ]

    memory = run_and_eval_commands(commands)
    assert memory[a] == 9
    assert memory[b] == 14


def test_calllt_only_else() -> None:
    a, b = xbf.Unit("a"), xbf.Unit("b")
    commands = [
        xbf.Init(a),
        xbf.Init(b),
        xbf.CallLT(
            a,
            b,
            else_=[
                xbf.AddUnit(b, 5, b),
            ],
        ),
    ]

    memory = run_and_eval_commands(commands)
    assert memory[a] == 0
    assert memory[b] == 5


def test_calllt_equal_only_else_two() -> None:
    a, b = xbf.Unit("a"), xbf.Unit("b")
    commands = [
        xbf.Init(a),
        xbf.Init(b),
        xbf.AddUnit(a, 5, a),
        xbf.AddUnit(b, 4, b),
        xbf.CallLT(
            a,
            b,
            else_=[
                xbf.AddUnit(b, 5, b),
            ],
        ),
    ]

    memory = run_and_eval_commands(commands)
    assert memory[a] == 5
    assert memory[b] == 9


def test_calllt_equal() -> None:
    a, b = xbf.Unit("a"), xbf.Unit("b")
    commands = [
        xbf.Init(a),
        xbf.Init(b),
        xbf.AddUnit(a, 5, a),
        xbf.AddUnit(b, 5, b),
        xbf.CallLT(
            a,
            b,
            else_=[
                xbf.AddUnit(a, 5, a),
            ],
        ),
    ]

    memory = run_and_eval_commands(commands)
    assert memory[a] == 10
    assert memory[b] == 5


def test_calllt_nested() -> None:
    a, b = xbf.Unit(), xbf.Unit()
    commands = [
        xbf.Init(a),
        xbf.Init(b),
        xbf.AddUnit(a, 1, a),
        xbf.AddUnit(b, 1, b),
        xbf.CallLT(
            a,
            b,
            else_=[
                xbf.AddUnit(b, 1, b),
                xbf.CallLT(
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
    assert memory[a] == 1
    assert memory[b] == 7
