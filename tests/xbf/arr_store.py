from src import xbf

from .utils import run_and_eval_commands_get_whole_tape


def test_simple_assignment() -> None:
    arr = xbf.Array(16)
    idx = xbf.Unit()
    value = xbf.Unit()
    commands = [
        xbf.InitArray(arr),
        xbf.InitUnit(idx),
        xbf.InitUnit(value),
        xbf.AssignUnit(idx, 4),
        xbf.AssignUnit(value, 5),
        xbf.ArrayStore(arr, value, idx),
    ]

    tape, var2idx = run_and_eval_commands_get_whole_tape(commands)
    assert tape[var2idx[idx]] == 4
    assert tape[var2idx[value]] == 5
    assert tape[var2idx[arr] + 3 + 4 * 2] == 5
    assert sum(tape) == 14


def test_value_override() -> None:
    arr = xbf.Array(16)
    idx = xbf.Unit()
    value = xbf.Unit()
    value_2 = xbf.Unit()
    commands = [
        xbf.InitArray(arr),
        xbf.InitUnit(idx),
        xbf.InitUnit(value),
        xbf.AssignUnit(idx, 4),
        xbf.AssignUnit(value, 5),
        xbf.AssignUnit(value_2, 50),
        xbf.ArrayStore(arr, value, idx),
        xbf.ArrayStore(arr, value_2, idx),
    ]

    tape, var2idx = run_and_eval_commands_get_whole_tape(commands)
    assert tape[var2idx[idx]] == 4
    assert tape[var2idx[value]] == 5
    assert tape[var2idx[value_2]] == 50
    assert tape[var2idx[arr] + 3 + 4 * 2] == 50


def test_zero_index() -> None:
    arr = xbf.Array(16)
    idx = xbf.Unit()
    value = xbf.Unit()
    commands = [
        xbf.InitArray(arr),
        xbf.InitUnit(idx),
        xbf.InitUnit(value),
        xbf.AssignUnit(idx, 0),
        xbf.AssignUnit(value, 5),
        xbf.ArrayStore(arr, value, idx),
        xbf.AssignUnit(idx, 1),
        xbf.AssignUnit(value, 10),
        xbf.ArrayStore(arr, value, idx),
    ]

    tape, var2idx = run_and_eval_commands_get_whole_tape(commands)
    assert tape[var2idx[idx]] == 1
    assert tape[var2idx[arr] + 3] == 5
    assert tape[var2idx[arr] + 5] == 10
