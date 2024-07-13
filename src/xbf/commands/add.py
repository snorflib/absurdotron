import collections.abc

import attrs

from src.ir import tokens
from src.memoptix import metainfo
from src.xbf import dtypes, program

from .base import BaseCommand
from .init_unit import InitUnit
from .move import _move_unit2units


def _add_an_integer(origin: dtypes.Unit, integer: int) -> collections.abc.Sequence[tokens.Increment | tokens.Decrement]:
    """Adds or subtracts an integer value to/from a BF Byte."""
    operation: type[tokens.Increment | tokens.Decrement] = tokens.Increment if integer > 0 else tokens.Decrement
    return [operation(owner=origin)] * abs(integer)


def _quick_migration(from_: dtypes.Unit, to: dtypes.Unit, program: program.Program) -> list[tokens.BFToken]:
    buffer = dtypes.Unit()
    InitUnit(buffer)(program)
    routine = _move_unit2units(from_, [(buffer, 1)])
    routine.extend(_move_unit2units(buffer, [(from_, 1), (to, 1)]))
    routine.append(metainfo.Free(buffer))
    return routine


def _generic_addition(
    origin: dtypes.Unit,
    other: dtypes.Unit | int,
    target: dtypes.Unit,
    program: program.Program,
    add: bool = True,
) -> collections.abc.Sequence[tokens.BFToken]:
    """
    Adds or subtracts a value to/from a BF Byte.

    :param origin: Target BF Byte.
    :param other: Value to add/subtract, either a BF Byte or an integer.
    :param add: Specifies addition (True) or subtraction (False).
    :return: Token sequence to perform the operation.

    If `other` is an integer, directly adds/subtracts it from `origin`.
    If `other` is a BF Byte, uses a buffer to transfer the value.
    """

    if isinstance(other, int):
        if target is origin:
            return _add_an_integer(origin, other * (1 if add else -1))

        routine = _quick_migration(origin, target, program)
        routine.extend(_add_an_integer(target, other * (1 if add else -1)))
        return routine

    if origin is other:
        if add is False:
            # a - a = 0
            return [tokens.Clear(origin)]

        buffer_unit = dtypes.Unit()
        InitUnit(buffer_unit)(program)
        routine = _move_unit2units(from_unit=origin, to_units=[(buffer_unit, 1)])

        if other is target:
            routine.extend(_move_unit2units(from_unit=buffer_unit, to_units=[(target, 2)]))
        else:
            routine.extend(_move_unit2units(from_unit=buffer_unit, to_units=[(origin, 1), (target, 2)]))

        routine.append(metainfo.Free(buffer_unit))
        return routine

    if (other is target) and (add is True):
        origin, other = other, origin

    other_buffer = dtypes.Unit()
    InitUnit(other_buffer)(program)
    routine = _move_unit2units(from_unit=other, to_units=[(other_buffer, 1)])

    if origin is target:
        routine.extend(_move_unit2units(from_unit=other_buffer, to_units=[(other, 1), (origin, 1 if add else -1)]))
        routine.append(metainfo.Free(other_buffer))
        return routine

    origin_buffer = dtypes.Unit()
    InitUnit(origin_buffer)(program)
    routine.extend(_move_unit2units(from_unit=origin, to_units=[(origin_buffer, 1)]))
    routine.extend(_move_unit2units(from_unit=origin_buffer, to_units=[(origin, 1), (target, 1)]))

    if other is target:
        routine.extend(_move_unit2units(from_unit=other_buffer, to_units=[(target, 1 if add else -1)]))
    else:
        routine.extend(_move_unit2units(from_unit=other_buffer, to_units=[(other, 1), (target, 1 if add else -1)]))

    routine.append(metainfo.Free(origin_buffer))
    routine.append(metainfo.Free(other_buffer))
    return routine


@attrs.frozen
class AddUnit(BaseCommand):
    origin: dtypes.Unit
    to_add: dtypes.Unit | int
    target: dtypes.Unit

    def _apply(self, context: program.Program) -> None:
        context.routine.extend(
            _generic_addition(
                self.origin,
                self.to_add,
                self.target,
                program=context,
                add=True,
            )
        )
