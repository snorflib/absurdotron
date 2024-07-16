from src import xbf

from .utils import run_and_eval_commands


def test_callle_only_if() -> None:
    a, b = xbf.Unit(), xbf.Unit()
    commands = [
        xbf.Init(a),
        xbf.Init(b),
        xbf.Add(a, 9, a),
        xbf.Add(b, 10, b),
        xbf.CallLE(
            a,
            b,
            if_=[
                xbf.Add(b, 4, b),
            ],
        ),
    ]

    memory = run_and_eval_commands(commands)
    assert memory[a] == 9
    assert memory[b] == 14


def test_callle_only_else() -> None:
    a, b = xbf.Unit("a"), xbf.Unit("b")
    commands = [
        xbf.Init(a),
        xbf.Init(b),
        xbf.Add(a, 1, a),
        xbf.CallLE(
            a,
            b,
            else_=[
                xbf.Add(b, 5, b),
            ],
        ),
    ]

    memory = run_and_eval_commands(commands)
    assert memory[a] == 1
    assert memory[b] == 5


def test_callle_only_else_two() -> None:
    a, b = xbf.Unit("a"), xbf.Unit("b")
    commands = [
        xbf.Init(a),
        xbf.Init(b),
        xbf.Add(a, 1, a),
        xbf.CallLE(
            a,
            b,
            else_=[
                xbf.Add(b, 5, b),
            ],
        ),
    ]

    memory = run_and_eval_commands(commands)
    assert memory[a] == 1
    assert memory[b] == 5


def test_callle_equal() -> None:
    a, b = xbf.Unit("a"), xbf.Unit("b")
    commands = [
        xbf.Init(a),
        xbf.Init(b),
        xbf.Add(a, 5, a),
        xbf.Add(b, 5, b),
        xbf.CallLE(
            a,
            b,
            if_=[
                xbf.Add(a, 5, a),
            ],
        ),
    ]

    memory = run_and_eval_commands(commands)
    assert memory[a] == 10
    assert memory[b] == 5


def test_callle_nested() -> None:
    a, b = xbf.Unit(), xbf.Unit()
    commands = [
        xbf.Init(a),
        xbf.Init(b),
        xbf.Add(a, 2, a),
        xbf.Add(b, 1, b),
        xbf.CallLE(
            a,
            b,
            else_=[
                xbf.Add(b, 1, b),
                xbf.CallLE(
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
    assert memory[a] == 2
    assert memory[b] == 7
