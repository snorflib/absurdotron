import attrs

from src import ir, xbf

from .utils import run_and_eval_opcodes


@attrs.frozen
class MockUpIncrementCommand(xbf.BaseCommand):
    unit: xbf.Unit
    num: int

    def _apply(self, context: xbf.Program) -> None:
        for _ in range(self.num):
            context.routine.append(ir.Increment(self.unit))


def test_simple_migrate() -> None:
    a, b = xbf.Unit(), xbf.Unit()
    opcodes = [xbf.Init(a), xbf.Init(b), MockUpIncrementCommand(a, 5), xbf.Move(a, to_=[(b, 1)])]

    memory = run_and_eval_opcodes(opcodes)
    assert memory[a] == 0
    assert memory[b] == 5


def test_double_migrate() -> None:
    a, b = xbf.Unit(), xbf.Unit()
    opcodes = [xbf.Init(a), xbf.Init(b), MockUpIncrementCommand(a, 5), xbf.Move(a, to_=[(b, 2)])]

    memory = run_and_eval_opcodes(opcodes)
    assert memory[a] == 0
    assert memory[b] == 10


def test_double_migrate_wrapping() -> None:
    a, b = xbf.Unit(), xbf.Unit()
    opcodes = [xbf.Init(a), xbf.Init(b), MockUpIncrementCommand(a, 5), xbf.Move(a, to_=[(b, -2)])]

    memory = run_and_eval_opcodes(opcodes)
    assert memory[a] == 0
    assert memory[b] == 246


def test_migrate_multiple_targets() -> None:
    a, b, c = xbf.Unit(), xbf.Unit(), xbf.Unit()
    opcodes = [
        xbf.Init(a),
        xbf.Init(b),
        xbf.Init(c),
        MockUpIncrementCommand(a, 5),
        MockUpIncrementCommand(c, 20),
        xbf.Move(a, to_=[(c, -2), (b, 3)]),
    ]

    memory = run_and_eval_opcodes(opcodes)
    assert memory[a] == 0
    assert memory[b] == 15
    assert memory[c] == 10
