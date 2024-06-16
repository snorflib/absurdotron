import collections.abc

import attrs

from src.ir import tokens
from src.memoptix import metainfo
from src.xbf import dtypes, program

from .add import _generic_addition
from .base import BaseCommand
from .init_unit import InitUnit
from .migrate import _migrate_unit2units


def _multiply(
    origin: dtypes.Unit,
    other: dtypes.Unit | int,
    target: dtypes.Unit,
    program: program.Program,
) -> collections.abc.Sequence[tokens.BFToken]:
    if isinstance(other, int):
        if other == 0:
            return []

        buffer = dtypes.Unit()
        InitUnit(buffer)(program)

        routine = _migrate_unit2units(origin, [(buffer, 1)])
        if origin is target:
            routine.extend(_migrate_unit2units(buffer, [(target, other)]))
        else:
            routine.extend(_migrate_unit2units(buffer, [(target, other), (origin, 1)]))

        routine.append(metainfo.Free(buffer))
        return routine

    origin_buf, other_buf = dtypes.Unit(), dtypes.Unit()

    InitUnit(origin_buf)(program)
    InitUnit(other_buf)(program)

    if origin is other:
        routine = _migrate_unit2units(from_unit=origin, to_units=[(origin_buf, 1), (other_buf, 1)])
    else:
        routine = _migrate_unit2units(from_unit=origin, to_units=[(origin_buf, 1)])
        routine.extend(_migrate_unit2units(from_unit=other, to_units=[(other_buf, 1)]))

    routine.append(tokens.EnterLoop(other_buf))
    routine.extend(_generic_addition(target, origin_buf, target, program, add=True))

    if other is not origin:
        routine.append(tokens.Increment(other))

    routine.append(tokens.Decrement(other_buf))
    routine.append(tokens.ExitLoop())

    # This line also covers the case where target is the
    routine.extend(_migrate_unit2units(origin_buf, [(origin, 1)]))

    routine.append(metainfo.Free(other_buf))
    routine.append(metainfo.Free(origin_buf))
    return routine


@attrs.frozen
class MulUnit(BaseCommand):
    origin: dtypes.Unit
    mul_by: dtypes.Unit | int
    target: dtypes.Unit

    def _apply(self, context: program.Program) -> None:
        context.routine.extend(
            _multiply(
                self.origin,
                self.mul_by,
                self.target,
                program=context,
            )
        )
