import attrs

from src.ir import tokens, types
from src.memoptix import metainfo

from . import base, dtypes
from .add import add_int_long
from .init import init
from .move import move
from .arr_store import (
    _go_to_int_index_from_control, 
    _go_from_int_index_from_control, 
    _move_pointer_by_value, 
    _inplace_move, 
    _move_from_control_by_trace_instance, 
    _move_pointer_by_value_str,
    _assign_to_control, 
    _go_to_unit_indexes_from_control, 
    _move_to_control_traceless,
    _move_to_control_with_trace,
)


@attrs.frozen
class ArrayLoad(base.OpCode):
    array: dtypes.Array
    load_in: list[dtypes.Unit]
    # little endian
    index: list[dtypes.Unit] | int

    def _execute(self) -> base.OpCodeReturn:
        return array_load(
            self.array,
            self.load_in,
            self.index,
        )


@base.convert
def array_load(
    array: dtypes.Array,
    load_in: list[dtypes.Unit],
    index: list[dtypes.Unit] | int,
) -> base.ToConvert:
    if isinstance(index, int):
        return _array_load_by_int(array, load_in, index)

    return _array_load_by_unit(array, load_in, index)


@base.convert
def _array_load_by_int(
    array: dtypes.Array,
    load_in: list[dtypes.Unit],
    index: int,
) -> base.ToConvert:
    ret = base.OpCodeReturn()
    ret |= tokens.Decrement(array)
    ret |= _go_to_int_index_from_control(array, index)
    ret |= _units_from_next_partitions_from_current(array, load_in)
    ret |= _go_from_int_index_from_control(array, index)
    ret |= tokens.Increment(array)

    return ret


@base.convert
def _array_load_by_unit(
    array: dtypes.Array,
    load_in: list[dtypes.Unit] | int,
    index: list[dtypes.Unit],
) -> base.ToConvert:
    ret = base.OpCodeReturn()
    ret |= _assign_to_control(array, -1)
    ret |= _go_to_unit_indexes_from_control(array, index)
    ret |= _units_from_next_partitions_from_current(array, load_in)
    ret |= _move_to_control_traceless(array)

    return ret


@base.convert
def _units_from_next_partitions_from_current(array: dtypes.Array, load_in: list[dtypes.Unit]) -> base.ToConvert:
    ret = base.OpCodeReturn()
    offset = 0
    in_part_off = 0

    for part in load_in:
        in_part_off += 1
        ret |= _unit_from_current(array, part, in_part_off)

        if in_part_off % array.granularity == 0:
            ret |= tokens.CodeInjection(None, ">" * (array.granularity + 1))
            offset += array.granularity + 1
            in_part_off = 0

    return ret | tokens.CodeInjection(None, "<" * offset)


@base.convert
def _unit_from_current(array: dtypes.Array, unit: dtypes.Unit, offset: int) -> base.ToConvert:
    width = array.granularity + 1

    ret = _move_pointer_by_value(offset)
    ret |= tokens.EnterLoop(None)
    ret |= tokens.Decrement(None)
    ret |= _move_pointer_by_value(-offset) | tokens.Increment(None)
    ret |= _move_pointer_by_value(width) | tokens.Increment(None)
    ret |= _move_pointer_by_value(offset - width)
    ret |= tokens.ExitLoop()
    
    ret |= _move_pointer_by_value(-offset)
    ret |= _inplace_move(-offset)
    ret |= _move_pointer_by_value(width)
    
    ret |= tokens.EnterLoop(None)
    ret |= _move_to_control_from_value(array)
    ret |= _move_pointer_by_value(width)
    ret |= tokens.Increment(None)
    ret |= _move_from_control_by_trace_instance(array)
    ret |= _move_pointer_by_value(-width)
    ret |= tokens.ExitLoop()

    ret |= _move_to_control_with_trace(array)

    ret |= _move_pointer_by_value(width)
    ret |= tokens.EnterLoop(None)
    ret |= tokens.Decrement()
    ret |= _move_from_control(array, unit, width)
    ret |= tokens.ExitLoop()

    ret |= tokens.Increment(None)
    ret |= _move_from_control_by_trace_instance(array)
    ret |= _move_pointer_by_value(-width * 2)

    return ret


@base.convert
def _move_from_control(array: dtypes, to_: dtypes.Unit, offset: int = 0) -> base.ToConvert:
    ret = base.OpCodeReturn()

    ret |= tokens.EnterLoop(None)
    ret |= tokens.Decrement(None)
    ret |= _move_pointer_by_value(-offset)

    ret |= tokens.Increment(to_)
    ret |= _move_pointer_by_value(offset, array)

    ret |= tokens.ExitLoop()
    return ret


@base.convert
def _move_to_control_from_value(arr: dtypes.Array) -> base.ToConvert:
    width = arr.granularity + 1
    return tokens.CompilerInjection(None, "[" + _move_pointer_by_value_str(-width) + "+]-")


@base.convert
def _move_to_control_traceless(arr: dtypes.Array) -> base.ToConvert:
    width = arr.granularity + 1
    return tokens.CompilerInjection(None, "+[-" + _move_pointer_by_value_str(-width) + "+]")
