from src import xbf

from .utils import run_and_eval_commands


def test_callgt_only_if() -> None:
    a, b = xbf.Unit(), xbf.Unit()
    commands = [
        xbf.InitUnit(a),
        xbf.InitUnit(b),
        xbf.AddUnit(a, 15, a),
        xbf.AddUnit(b, 10, b),
        xbf.CallGT(
            a,
            b,
            if_=[
                xbf.AddUnit(b, 4, b),
            ],
        ),
    ]

    memory = run_and_eval_commands(commands)
    assert memory[a] == 15
    assert memory[b] == 14


def test_callgt_only_else() -> None:
    a, b = xbf.Unit("a"), xbf.Unit("b")
    commands = [
        xbf.InitUnit(a),
        xbf.InitUnit(b),
        xbf.CallGT(
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


def test_callgt_equal_only_else_two() -> None:
    a, b = xbf.Unit("a"), xbf.Unit("b")
    commands = [
        xbf.InitUnit(a),
        xbf.InitUnit(b),
        xbf.AddUnit(a, 254, a),
        xbf.AddUnit(b, 255, b),
        xbf.CallGT(
            a,
            b,
            else_=[
                xbf.AddUnit(b, 5, b),
            ],
        ),
    ]

    memory = run_and_eval_commands(commands)
    assert memory[a] == 254
    assert memory[b] == 4


def test_callgt_equal() -> None:
    a, b = xbf.Unit("a"), xbf.Unit("b")
    commands = [
        xbf.InitUnit(a),
        xbf.InitUnit(b),
        xbf.AddUnit(a, 5, a),
        xbf.AddUnit(b, 5, b),
        xbf.CallGT(
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


def test_callgt_nested() -> None:
    a, b = xbf.Unit(), xbf.Unit()
    commands = [
        xbf.InitUnit(a),
        xbf.InitUnit(b),
        xbf.AddUnit(b, 10, b),
        xbf.CallGT(
            a,
            b,
            else_=[
                xbf.AddUnit(a, 11, a),
                xbf.CallGT(
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
    assert memory[a] == 11
    assert memory[b] == 15
