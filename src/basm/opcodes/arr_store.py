import attrs

from src.ir import tokens, types
from src.memoptix import metainfo

from . import base, dtypes
from .add import add_int_long
from .init import init
from .move import move


@attrs.frozen
class ArrayStore(base.OpCode):
    array: dtypes.Array
    to_store: list[dtypes.Unit] | int
    # little endian
    index: list[dtypes.Unit] | int

    def _execute(self) -> base.OpCodeReturn:
        return array_store(
            self.array,
            self.to_store,
            self.index,
        )


@base.convert
def array_store(
    array: dtypes.Array,
    to_store: list[dtypes.Unit] | int,
    index: list[dtypes.Unit] | int,
) -> base.ToConvert:
    if isinstance(index, int):
        return _array_store_by_int(array, to_store, index)

    return _array_store_by_unit(array, to_store, index)


@base.convert
def _array_store_by_int(
    array: dtypes.Array,
    to_store: list[dtypes.Unit] | int,
    index: int,
) -> base.ToConvert:
    if isinstance(to_store, int):
        return _go_to_int_index_from_control(array, index) |\
               _int_to_next_partitions_from_current(array, to_store) |\
               _go_from_int_index_from_control(array, index)

    ret = base.OpCodeReturn()
    ret |= tokens.Decrement(array)
    ret |= _go_to_int_index_from_control(array, index)
    ret |= _units_to_next_partitions_from_current(array, to_store)
    ret |= _go_from_int_index_from_control(array, index)
    ret |= tokens.Increment(array)

    return ret


@base.convert
def _array_store_by_unit(
    array: dtypes.Array,
    to_store: list[dtypes.Unit] | int,
    index: list[dtypes.Unit],
) -> base.ToConvert:
    ret = base.OpCodeReturn()
    ret |= _assign_to_control(array, -1)
    ret |= _go_to_unit_indexes_from_control(array, index)

    if isinstance(to_store, int):
        return ret |\
               _int_to_next_partitions_from_current(array, to_store) |\
               _move_to_control_traceless(array)

    ret |= _units_to_next_partitions_from_current(array, to_store)
    ret |= _move_to_control_traceless(array)

    return ret


@base.convert
def _go_to_unit_indexes_from_control(array: dtypes.Array, index: list[dtypes.Unit]) -> base.ToConvert:
    ret = _apply_single_unit_index(array, index.pop(0))

    if not index:
        return ret

    step = array.granularity + 1
    for _idx, unit in enumerate(index):
        ret |= _unit_to_from_current(array, unit, (array.granularity + 1) * 2)

        ret |= _move_pointer_by_value((array.granularity + 1) * 2)
        ret |= tokens.EnterLoop(None)
        ret |= tokens.Decrement(None)
        ret |= _move_pointer_by_value(-(array.granularity + 1) * 2)
        ret |= tokens.Increment(None)
        ret |= _move_pointer_by_value((array.granularity + 1) * 2)
        ret |= tokens.ExitLoop()
        ret |= _move_pointer_by_value(-(array.granularity + 1) * 2)

        # step *= 1 >> 8
        ret |= _go_to_index_stored_in_current_unit(array, step)

    return ret


@base.convert
def _apply_single_unit_index(array: dtypes.Array, index: dtypes.Unit) -> base.ToConvert:
    ret = _assign_to_control(array, index, offset=array.granularity + 1)
    ret |= _move_pointer_by_value(array.granularity + 1, array)
    ret |= _go_to_index_stored_in_current_unit(array, array.granularity + 1)
    return ret


@base.convert
def _go_to_index_stored_in_current_unit(array: dtypes.Array, step: int = 1, owner: types.Owner = None, max: int = 255) -> base.ToConvert:
    step_left = "[-"
    step_right = _move_pointer_by_value_str(step) + "]"
    code = step_left * max + step_right * max

    return tokens.CompilerInjection(owner, code)


@base.convert
def _go_to_int_index_from_control(array: dtypes.Array, index: int) -> base.ToConvert:
    return tokens.CodeInjection(array, ">" * (index + 1) * (1 + array.granularity))


@base.convert
def _go_from_int_index_from_control(array: dtypes.Array, index: int) -> base.ToConvert:
    return tokens.CodeInjection(array, "<" * (index + 1) * (1 + array.granularity))


@base.convert
def _int_to_next_partitions_from_current(array: dtypes.Array, to_store: int) -> base.ToConvert:
    ret = base.OpCodeReturn()
    offset = 0

    for part in _int_to_8bits_little_endian(to_store):
        ret |= tokens.CodeInjection(array, ">")
        ret |= tokens.Clear(None)
        ret |= add_int_long(part, None)

        offset += 1
        if offset % array.granularity == 0:
            ret |= tokens.CodeInjection(None, ">")
            offset += 1

    return ret | tokens.CodeInjection(None, "<" * offset)


def _int_to_8bits_little_endian(number: int) -> list[int]:
    byte_list = []
    while number > 0:
        byte_list.append(number & 0xFF)
        number >>= 8

    if not byte_list:
        return [0]
    return byte_list

@base.convert
def _units_to_next_partitions_from_current(array: dtypes.Array, to_store: list[dtypes.Unit]) -> base.ToConvert:
    ret = base.OpCodeReturn()
    offset = 0
    in_part_off = 0

    for part in to_store:
        in_part_off += 1
        ret |= _unit_to_from_current(array, part, in_part_off)

        if in_part_off % array.granularity == 0:
            ret |= tokens.CodeInjection(None, ">" * (array.granularity + 1))
            offset += array.granularity + 1
            in_part_off = 0

    return ret | tokens.CodeInjection(None, "<" * offset)


@base.convert
def _unit_to_from_current(array: dtypes.Array, unit: dtypes.Unit, offset: int) -> base.ToConvert:
    ret = _move_pointer_by_value(offset)
    ret |= tokens.CompilerInjection(None, "[-]")
    ret |= _move_pointer_by_value(-offset)
    ret |= _move_to_control_with_trace(array)

    ret |= _assign_to_control(array, unit, array.granularity + 1)
    ret |= _move_from_control_to_marked(array, offset)

    return ret


@base.convert
def _assign_to_control(array: dtypes, value: dtypes.Unit | int, offset: int = 0) -> base.ToConvert:
    if isinstance(value, int):
        return _move_pointer_by_value(offset, array) | add_int_long(value, None)

    buffer = dtypes.Unit()
    ret = init(buffer) | move(value, [(buffer, 1)])
    ret |= _move_pointer_by_value(offset, array)
    ret |= tokens.Clear(None)
    ret |= _move_pointer_by_value(-offset)

    ret |= tokens.EnterLoop(buffer)
    ret |= tokens.Increment(value)
    ret |= tokens.Decrement(buffer)

    ret |=  _move_pointer_by_value(offset, array)
    ret |= tokens.Increment(None)
    ret |= _move_pointer_by_value(-offset)

    ret |= tokens.ExitLoop()
    ret |= metainfo.Free(buffer)

    return ret


@base.convert
def _move_from_control_to_marked(array: dtypes, offset: int) -> base.ToConvert:
    assert offset != 0

    ret = base.OpCodeReturn()

    ret |= _move_pointer_by_value(array.granularity + 1, array)
    ret |= tokens.EnterLoop(None)
    ret |= _move_from_control_by_trace_instance(array)
    ret |= _move_pointer_by_value(-array.granularity - 1)

    ret |= _move_pointer_by_value(offset)
    ret |= tokens.Increment(None)
    ret |= _move_pointer_by_value(-offset)

    ret |= _move_to_control_with_trace(array)
    ret |= _move_pointer_by_value(array.granularity + 1, array)
    ret |= tokens.Decrement(None)

    ret |= tokens.ExitLoop()

    ret |= tokens.Increment(None)
    ret |= _move_from_control_by_trace_instance(array)
    ret |= _move_pointer_by_value(-array.granularity - 1)

    return ret


@base.convert
def _move_to_control_with_trace(arr: dtypes.Array) -> base.ToConvert:
    width = arr.granularity + 1
    return tokens.CompilerInjection(None, "+[" + _move_pointer_by_value_str(-width) + "+]-")


@base.convert
def _move_from_control_by_trace_instance(arr: dtypes.Array) -> base.ToConvert:
    width = arr.granularity + 1
    return tokens.CompilerInjection(None, "[-" + _move_pointer_by_value_str(width) + "]")


@base.convert
def _move_to_control_traceless(arr: dtypes.Array) -> base.ToConvert:
    width = arr.granularity + 1
    return tokens.CompilerInjection("+[-" + _move_pointer_by_value_str(-width) + "+]")


@base.convert
def _move_pointer_by_value(value: int, owner: types.Owner = None) -> base.ToConvert:
    return tokens.CodeInjection(owner, ( "<" if value < 0 else ">") * abs(value))

def _move_pointer_by_value_str(value: int) -> str:
    return ( "<" if value < 0 else ">") * abs(value)
