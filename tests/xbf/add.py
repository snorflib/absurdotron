from src import xbf

from .utils import run_and_eval_commands


def test_simple_add() -> None:
    a = xbf.Unit()
    commands = [xbf.Init(a), xbf.Add([a, 50], a)]

    memory = run_and_eval_commands(commands)
    assert memory[a] == 50


def test_add_to_itself() -> None:
    a = xbf.Unit()
    commands = [xbf.Init(a), xbf.Add([a, 10], a), xbf.Add([a, a], a)]

    memory = run_and_eval_commands(commands)
    assert memory[a] == 20


def test_add_complex_one() -> None:
    a, b = xbf.Unit(), xbf.Unit()
    commands = [xbf.Init(a), xbf.Init(b), xbf.Add([a, 10], a), xbf.Add([b, a], b), xbf.Add([b, 5], b)]

    memory = run_and_eval_commands(commands)
    assert memory[a] == 10
    assert memory[b] == 15


def test_add_complex_two() -> None:
    a, b = xbf.Unit(), xbf.Unit()
    commands = [
        xbf.Init(a),
        xbf.Init(b),
        xbf.Add([a, 10], a),
        xbf.Add([b, 5], b),
        xbf.Add([a, b], b),
    ]

    memory = run_and_eval_commands(commands)
    assert memory[a] == 10
    assert memory[b] == 15


def test_add_three_args() -> None:
    a, b, c = xbf.Unit(), xbf.Unit(), xbf.Unit()
    commands = [
        xbf.Init(a),
        xbf.Init(b),
        xbf.Init(c),
        xbf.Add([a, 10], a),
        xbf.Add([b, 10], b),
        xbf.Add([c, 10], c),
        xbf.Add([b, a], c),
    ]

    memory = run_and_eval_commands(commands)
    assert memory[a] == 10
    assert memory[b] == 10
    assert memory[c] == 20


def test_add_negative() -> None:
    a = xbf.Unit()
    commands = [xbf.Init(a), xbf.Add([a, -5], a)]

    memory = run_and_eval_commands(commands)
    assert memory[a] == 251


def test_save_target_to_add_target() -> None:
    a, b = xbf.Unit("a"), xbf.Unit("b")
    commands = [
        xbf.Init(a),
        xbf.Init(b),
        xbf.Add([a, 10], a),
        xbf.Add([b, 10], b),
        xbf.Add([a, a], a),
        xbf.Add([b, a], a),
    ]

    memory = run_and_eval_commands(commands)
    assert memory[a] == 30
    assert memory[b] == 10


def test_add_multiple_self_instances() -> None:
    a = xbf.Unit("a")
    commands = [xbf.Init(a), xbf.Add([10], a), xbf.Add([a, a, a, a], a)]

    memory = run_and_eval_commands(commands)
    assert memory[a] == 40


def test_add_ints_and_multiple_self_instances() -> None:
    a, b, c = xbf.Unit("a"), xbf.Unit("b"), xbf.Unit("c")
    commands = [
        xbf.Init(a),
        xbf.Init(b),
        xbf.Init(c),
        xbf.Add([10], a),
        xbf.Add([5], b),
        xbf.Add([1], c),
        xbf.Add([10, a, c, a, 10, b], a),
    ]

    memory = run_and_eval_commands(commands)
    assert memory[a] == 46


def test_add_ints_units_self() -> None:
    a, b = xbf.Unit("a"), xbf.Unit("b")
    commands = [
        xbf.Init(a),
        xbf.Init(b),
        xbf.Add([a, 10], a),
        xbf.Add([b, 10], b),
        xbf.Add([30, 10, a, b, b, a], a),
    ]
    memory = run_and_eval_commands(commands)
    assert memory[a] == 80
    assert memory[b] == 10
