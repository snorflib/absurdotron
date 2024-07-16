from src import xbf

from .utils import run_and_eval_commands


def test_callgt_only_if() -> None:
    a, b = xbf.Unit(), xbf.Unit()
    commands = [
        xbf.Init(a),
        xbf.Init(b),
        xbf.Add(a, 15, a),
        xbf.Add(b, 10, b),
        xbf.CallGT(
            a,
            b,
            if_=[
                xbf.Add(b, 4, b),
            ],
        ),
    ]

    memory = run_and_eval_commands(commands)
    assert memory[a] == 15
    assert memory[b] == 14


def test_callgt_only_else() -> None:
    a, b = xbf.Unit("a"), xbf.Unit("b")
    commands = [
        xbf.Init(a),
        xbf.Init(b),
        xbf.CallGT(
            a,
            b,
            else_=[
                xbf.Add(b, 5, b),
            ],
        ),
    ]

    memory = run_and_eval_commands(commands)
    assert memory[a] == 0
    assert memory[b] == 5


def test_callgt_equal_only_else_two() -> None:
    a, b = xbf.Unit("a"), xbf.Unit("b")
    commands = [
        xbf.Init(a),
        xbf.Init(b),
        xbf.Add(a, 254, a),
        xbf.Add(b, 255, b),
        xbf.CallGT(
            a,
            b,
            else_=[
                xbf.Add(b, 5, b),
            ],
        ),
    ]

    memory = run_and_eval_commands(commands)
    assert memory[a] == 254
    assert memory[b] == 4


def test_callgt_equal() -> None:
    a, b = xbf.Unit("a"), xbf.Unit("b")
    commands = [
        xbf.Init(a),
        xbf.Init(b),
        xbf.Add(a, 5, a),
        xbf.Add(b, 5, b),
        xbf.CallGT(
            a,
            b,
            else_=[
                xbf.Add(a, 5, a),
            ],
        ),
    ]

    memory = run_and_eval_commands(commands)
    assert memory[a] == 10
    assert memory[b] == 5


def test_callgt_nested() -> None:
    a, b = xbf.Unit(), xbf.Unit()
    commands = [
        xbf.Init(a),
        xbf.Init(b),
        xbf.Add(b, 10, b),
        xbf.CallGT(
            a,
            b,
            else_=[
                xbf.Add(a, 11, a),
                xbf.CallGT(
                    a,
                    b,
                    if_=[
                        xbf.Add(b, 5, b),
                    ],
                ),
            ],
        ),
    ]

    memory = run_and_eval_commands(commands)
    assert memory[a] == 11
    assert memory[b] == 15
