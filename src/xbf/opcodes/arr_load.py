import attrs

from src.ir import tokens
from src.xbf import dtypes, program

from .arr_store import _array_store, _get_path_tokens
from .base import BaseCommand


def _array_load(
    array: dtypes.Array,
    load_to: dtypes.Unit,
    index: dtypes.Unit,
    program: program.Program,
) -> None:
    routine = program.routine

    routine.append(tokens.Decrement(array))
    _array_store(array, index, 2, program)
    _get_path_tokens(array, program)

    routine.append(tokens.CodeInjection(None, "<[<+>->+<]<[->+<]>>[[<<+]->>+[->>]<<]+[-<<+]"))
    routine.extend(
        [
            tokens.Clear(load_to),
            tokens.CompilerInjection(array, ">>[-<<"),
            tokens.Increment(load_to),
            tokens.CompilerInjection(array, ">>]<<"),
        ]
    )


@attrs.frozen
class ArrayLoad(BaseCommand):
    array: dtypes.Array
    to_store: dtypes.Unit
    index: dtypes.Unit

    def _apply(self, context: program.Program) -> None:
        _array_load(
            self.array,
            self.to_store,
            self.index,
            context,
        )
