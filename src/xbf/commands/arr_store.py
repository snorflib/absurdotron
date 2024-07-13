import attrs

from src.ir import tokens
from src.memoptix import metainfo
from src.xbf import dtypes, program

from .base import BaseCommand
from .init_unit import InitUnit
from .migrate import MigrateUnit


def _get_path_tokens(array: dtypes.Array, program: program.Program) -> None:
    if array.length > 255:
        raise NotImplementedError("Only array less then 255 are supported")

    program.routine.append(
        tokens.CodeInjection(
            array,
            ">>" + ("[-" * array.length + f"{array.granularity * ">" + ">"}]" * array.length + ">>"),
        )
    )


def _array_store(
    array: dtypes.Array,
    to_store: dtypes.Unit,
    index: dtypes.Unit | int,
    program: program.Program,
) -> None:
    routine = program.routine

    if isinstance(index, int):
        buffer = dtypes.Unit()
        InitUnit(buffer)(program)
        MigrateUnit(to_store, [(buffer, 1)])(program)

        routine.extend(
            [
                tokens.CodeInjection(array, ">" * index + "[-]" + "<" * index),
                tokens.EnterLoop(buffer),
                tokens.CodeInjection(array, ">" * index + "+" + "<" * index),
                tokens.Increment(to_store),
                tokens.Decrement(buffer),
                tokens.ExitLoop(),
                metainfo.Free(buffer),
            ]
        )
        return

    routine.append(tokens.Decrement(array))
    _array_store(array, index, 2, program)
    _get_path_tokens(array, program)

    routine.append(tokens.CodeInjection(None, "<[-]>+[<<+]-"))
    _array_store(array, to_store, 2, program)

    routine.append(tokens.CodeInjection(array, ">>[[->>]<<<+>+[<<+]->>-]+[->>]+[-<<+]"))


@attrs.frozen
class ArrayStore(BaseCommand):
    array: dtypes.Array
    to_store: dtypes.Unit
    index: dtypes.Unit

    def _apply(self, context: program.Program) -> None:
        _array_store(
            self.array,
            self.to_store,
            self.index,
            context,
        )
