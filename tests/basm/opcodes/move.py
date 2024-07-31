import attrs

from src import ir
from src.basm import opcodes

from .utils import execute_opcodes_get_owner_values


@attrs.frozen
class _IncrementOpCode(opcodes.OpCode):
    unit: opcodes.Unit
    num: int

    def _execute(self, context: opcodes.Context) -> opcodes.OpCodeReturn:
        return opcodes.OpCodeReturn([ir.Increment(self.unit)] * self.num)


def test_simple_move() -> None:
    a, b = opcodes.Unit(), opcodes.Unit()
    instrs = [opcodes.Init(a), opcodes.Init(b), _IncrementOpCode(a, 5), opcodes.Move(a, to_=[(b, 1)])]

    memory = execute_opcodes_get_owner_values(instrs)
    assert memory[a] == 0
    assert memory[b] == 5


def test_double_move() -> None:
    a, b = opcodes.Unit(), opcodes.Unit()
    instrs = [opcodes.Init(a), opcodes.Init(b), _IncrementOpCode(a, 5), opcodes.Move(a, to_=[(b, 2)])]

    memory = execute_opcodes_get_owner_values(instrs)
    assert memory[a] == 0
    assert memory[b] == 10


def test_double_move_wrapping() -> None:
    a, b = opcodes.Unit(), opcodes.Unit()
    instrs = [opcodes.Init(a), opcodes.Init(b), _IncrementOpCode(a, 5), opcodes.Move(a, to_=[(b, -2)])]

    memory = execute_opcodes_get_owner_values(instrs)
    assert memory[a] == 0
    assert memory[b] == 246


def test_move_multiple_targets() -> None:
    a, b, c = opcodes.Unit(), opcodes.Unit(), opcodes.Unit()
    instrs = [
        opcodes.Init(a),
        opcodes.Init(b),
        opcodes.Init(c),
        _IncrementOpCode(a, 5),
        _IncrementOpCode(c, 20),
        opcodes.Move(a, to_=[(c, -2), (b, 3)]),
    ]

    memory = execute_opcodes_get_owner_values(instrs)
    assert memory[a] == 0
    assert memory[b] == 15
    assert memory[c] == 10


def test_move_same_target_multiple_times() -> None:
    a, b = opcodes.Unit(), opcodes.Unit()
    instrs = [
        opcodes.Init(a),
        opcodes.Init(b),
        _IncrementOpCode(a, 5),
        _IncrementOpCode(b, 10),
        opcodes.Move(a, to_=[(b, 5), (b, -1), (b, -4), (b, 3)]),
    ]

    memory = execute_opcodes_get_owner_values(instrs)
    assert memory[a] == 0
    assert memory[b] == 25
