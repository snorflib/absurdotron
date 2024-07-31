import attrs

from src import basm, ir

from .utils import execute_opcodes_get_owner_values


@attrs.frozen
class _IncrementOpCode(basm.OpCode):
    unit: basm.Unit
    num: int

    def _execute(self, context: basm.Context) -> basm.OpCodeReturn:
        return basm.OpCodeReturn([ir.Increment(self.unit)] * self.num)


def test_simple_move() -> None:
    a, b = basm.Unit(), basm.Unit()
    instrs = [basm.Init(a), basm.Init(b), _IncrementOpCode(a, 5), basm.Move(a, to_=[(b, 1)])]

    memory = execute_opcodes_get_owner_values(instrs)
    assert memory[a] == 0
    assert memory[b] == 5


def test_double_move() -> None:
    a, b = basm.Unit(), basm.Unit()
    instrs = [basm.Init(a), basm.Init(b), _IncrementOpCode(a, 5), basm.Move(a, to_=[(b, 2)])]

    memory = execute_opcodes_get_owner_values(instrs)
    assert memory[a] == 0
    assert memory[b] == 10


def test_double_move_wrapping() -> None:
    a, b = basm.Unit(), basm.Unit()
    instrs = [basm.Init(a), basm.Init(b), _IncrementOpCode(a, 5), basm.Move(a, to_=[(b, -2)])]

    memory = execute_opcodes_get_owner_values(instrs)
    assert memory[a] == 0
    assert memory[b] == 246


def test_move_multiple_targets() -> None:
    a, b, c = basm.Unit(), basm.Unit(), basm.Unit()
    instrs = [
        basm.Init(a),
        basm.Init(b),
        basm.Init(c),
        _IncrementOpCode(a, 5),
        _IncrementOpCode(c, 20),
        basm.Move(a, to_=[(c, -2), (b, 3)]),
    ]

    memory = execute_opcodes_get_owner_values(instrs)
    assert memory[a] == 0
    assert memory[b] == 15
    assert memory[c] == 10


def test_move_same_target_multiple_times() -> None:
    a, b = basm.Unit(), basm.Unit()
    instrs = [
        basm.Init(a),
        basm.Init(b),
        _IncrementOpCode(a, 5),
        _IncrementOpCode(b, 10),
        basm.Move(a, to_=[(b, 5), (b, -1), (b, -4), (b, 3)]),
    ]

    memory = execute_opcodes_get_owner_values(instrs)
    assert memory[a] == 0
    assert memory[b] == 25
