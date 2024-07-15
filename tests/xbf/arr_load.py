from src import xbf

from .utils import run_and_eval_commands_get_whole_tape


def test_simple_load() -> None:
    arr = xbf.Array(16)
    idx = xbf.Unit()
    value = xbf.Unit()
    commands = [
        xbf.Init(arr),
        xbf.Init(idx),
        xbf.Init(value),
        xbf.AssignUnit(idx, 4),
        xbf.AssignUnit(value, 5),
        xbf.ArrayStore(arr, value, idx),
        xbf.ArrayLoad(arr, idx, idx),
    ]

    tape, var2idx = run_and_eval_commands_get_whole_tape(commands)
    assert tape[var2idx[idx]] == tape[var2idx[value]] == 5
    assert tape[var2idx[arr] + 3 + 4 * 2] == 5
    assert sum(tape) == 15


def test_load_zero_at_zero() -> None:
    arr = xbf.Array(16)
    idx = xbf.Unit()
    value = xbf.Unit()
    value_read = xbf.Unit()
    commands = [
        xbf.Init(arr),
        xbf.Init(idx),
        xbf.Init(value),
        xbf.Init(value_read),
        xbf.AssignUnit(idx, 0),
        xbf.AssignUnit(value, 0),
        xbf.AssignUnit(value_read, 1),
        xbf.ArrayStore(arr, value, idx),
        xbf.ArrayLoad(arr, value_read, idx),
    ]

    tape, var2idx = run_and_eval_commands_get_whole_tape(commands)
    assert tape[var2idx[value]] == tape[var2idx[value_read]] == tape[var2idx[idx]] == 0
    assert sum(tape) == 0
