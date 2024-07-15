from src import xbf

from .utils import run_and_eval_commands


def test_callz_only_if() -> None:
    a, b = xbf.Unit(), xbf.Unit()
    commands = [
        xbf.Init(a),
        xbf.Init(b),
        xbf.AddUnit(a, 1, a),
        xbf.CallZ(
            a,
            if_=[
                xbf.AddUnit(b, 5, b),
            ],
        ),
    ]

    memory = run_and_eval_commands(commands)
    assert memory[a] == 1
    assert memory[b] == 5


def test_callz_only_else() -> None:
    a, b = xbf.Unit("a"), xbf.Unit("b")
    commands = [
        xbf.Init(a),
        xbf.Init(b),
        xbf.CallZ(
            a,
            else_=[
                xbf.AddUnit(b, 5, b),
            ],
        ),
    ]

    memory = run_and_eval_commands(commands)
    assert memory[a] == 0
    assert memory[b] == 5


def test_callz_nested() -> None:
    a, b = xbf.Unit(), xbf.Unit()
    commands = [
        xbf.Init(a),
        xbf.Init(b),
        xbf.CallZ(
            a,
            else_=[
                xbf.AddUnit(a, 1, a),
                xbf.CallZ(
                    a,
                    if_=[
                        xbf.AddUnit(b, 5, b),
                    ],
                ),
            ],
        ),
    ]

    memory = run_and_eval_commands(commands)
    assert memory[a] == 1
    assert memory[b] == 5
