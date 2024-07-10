from src import xbf

from .utils import run_and_eval_commands


def test_callge_only_if() -> None:
    a, b = xbf.Unit(), xbf.Unit()
    commands = [
        xbf.InitUnit(a),
        xbf.InitUnit(b),
        xbf.AddUnit(a, 15, a),
        xbf.AddUnit(b, 10, b),
        xbf.CallGE(
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


def test_callge_only_else() -> None:
    a, b = xbf.Unit("a"), xbf.Unit("b")
    commands = [
        xbf.InitUnit(a),
        xbf.InitUnit(b),
        xbf.AddUnit(b, 1, b),
        xbf.CallGE(
            a,
            b,
            else_=[
                xbf.AddUnit(b, 5, b),
            ],
        ),
    ]

    memory = run_and_eval_commands(commands)
    assert memory[a] == 0
    assert memory[b] == 6


def test_callge_equal_only_else_two() -> None:
    a, b = xbf.Unit("a"), xbf.Unit("b")
    commands = [
        xbf.InitUnit(a),
        xbf.InitUnit(b),
        xbf.AddUnit(a, 254, a),
        xbf.AddUnit(b, 255, b),
        xbf.CallGE(
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


def test_callge_equal() -> None:
    a, b = xbf.Unit("a"), xbf.Unit("b")
    commands = [
        xbf.InitUnit(a),
        xbf.InitUnit(b),
        xbf.AddUnit(a, 5, a),
        xbf.AddUnit(b, 5, b),
        xbf.CallGE(
            a,
            b,
            if_=[
                xbf.AddUnit(a, 5, a),
            ],
        ),
    ]

    memory = run_and_eval_commands(commands)
    assert memory[a] == 10
    assert memory[b] == 5


def test_callge_nested() -> None:
    a, b = xbf.Unit(), xbf.Unit()
    commands = [
        xbf.InitUnit(a),
        xbf.InitUnit(b),
        xbf.AddUnit(b, 10, b),
        xbf.CallGE(
            a,
            b,
            else_=[
                xbf.AddUnit(a, 10, a),
                xbf.CallGE(
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
    assert memory[a] == 10
    assert memory[b] == 15
