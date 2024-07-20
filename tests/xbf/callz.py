from src import xbf

from .utils import run_and_eval_opcodes


def test_callz_only_if() -> None:
    a, b = xbf.Unit(), xbf.Unit()
    opcodes = [
        xbf.Init(a),
        xbf.Init(b),
        xbf.Add(a, 1, a),
        xbf.CallZ(
            a,
            if_=xbf.Add(b, 5, b)(None),
        ),
    ]

    memory = run_and_eval_opcodes(opcodes)
    assert memory[a] == 1
    assert memory[b] == 5


def test_callz_only_else() -> None:
    a, b = xbf.Unit("a"), xbf.Unit("b")
    opcodes = [
        xbf.Init(a),
        xbf.Init(b),
        xbf.CallZ(
            a,
            else_=xbf.Add(b, 5, b)(None),
        ),
    ]

    memory = run_and_eval_opcodes(opcodes)
    assert memory[a] == 0
    assert memory[b] == 5


def test_callz_nested() -> None:
    a, b = xbf.Unit(), xbf.Unit()
    opcodes = [
        xbf.Init(a),
        xbf.Init(b),
        xbf.CallZ(
            a,
            else_=xbf.Add(a, 1, a)(None)
            | xbf.CallZ(
                a,
                if_=xbf.Add(b, 5, b)(None),
            )(None),
        ),
    ]

    memory = run_and_eval_opcodes(opcodes)
    assert memory[a] == 1
    assert memory[b] == 5
