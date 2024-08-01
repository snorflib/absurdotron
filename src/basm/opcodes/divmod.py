import attrs

from src.ir import tokens
from src.memoptix import metainfo

from . import base, dtypes
from .callz import callz
from .init import init
from .move import move
from .utils import add_int_long


@attrs.frozen
class DivMod(base.OpCode):
    dividend: dtypes.Unit | int
    divisor: dtypes.Unit | int
    quotient: dtypes.Unit | None = None
    remainder: dtypes.Unit | None = None

    def _execute(self) -> base.OpCodeReturn:
        return div(self.dividend, self.divisor, self.quotient, self.remainder)


@base.convert
def div(
    dividend: dtypes.Unit | int,
    divisor: dtypes.Unit | int,
    quotient: dtypes.Unit | None,
    remainder: dtypes.Unit | None,
) -> base.ToConvert:
    if remainder is quotient is None:
        return None
    elif remainder == quotient:
        raise ValueError("Remainder cannot be Quotient")
    elif isinstance(dividend, int) and isinstance(divisor, int):
        return _div_ints(dividend, divisor, quotient, remainder)
    elif dividend == divisor:
        return _div_by_itself(quotient, remainder)

    return _div_units_and_ints(dividend, divisor, quotient, remainder)


def _div_ints(
    dividend: int,
    divisor: int,
    quotient: dtypes.Unit | None,
    remainder: dtypes.Unit | None,
) -> base.OpCodeReturn:
    quot, rem = divmod(dividend, divisor)

    instrs = base.OpCodeReturn()

    if quotient:
        instrs |= tokens.Clear(quotient)
        instrs |= add_int_long(quot, quotient)

    if remainder:
        instrs |= tokens.Clear(remainder)
        instrs |= add_int_long(rem, remainder)

    return instrs


def _div_by_itself(
    quotient: dtypes.Unit | None,
    remainder: dtypes.Unit | None,
) -> base.OpCodeReturn:
    instrs = base.OpCodeReturn()

    if quotient:
        instrs |= tokens.Clear(quotient)
        instrs |= tokens.Increment(quotient)
    if remainder:
        instrs |= tokens.Clear(remainder)
    return instrs


def _div_units_and_ints(
    dividend: dtypes.Unit | int,
    divisor: dtypes.Unit | int,
    quotient: dtypes.Unit | None,
    remainder: dtypes.Unit | None,
) -> base.OpCodeReturn:
    instrs = base.OpCodeReturn()

    rem_buff, dividend_buff = dtypes.Unit(), dtypes.Unit()
    instrs |= init(rem_buff) | init(dividend_buff)

    dynamic_divisor: bool = False
    if isinstance(int_divisor := divisor, int):
        divisor = dtypes.Unit()
        instrs |= init(divisor)
        instrs |= add_int_long(int_divisor, divisor)
        dynamic_divisor = True
    elif divisor in [quotient, remainder]:
        divisor_new = dtypes.Unit()
        instrs |= init(divisor_new)
        instrs |= move(divisor, [(divisor_new, 1)])
        divisor = divisor_new

        dynamic_divisor = True

    if isinstance(dividend, int):
        instrs |= add_int_long(dividend, dividend_buff)
    else:
        instrs |= move(dividend, [(dividend_buff, 1)])

    instrs |= tokens.EnterLoop(dividend_buff)
    instrs |= tokens.Decrement(dividend_buff)
    instrs |= tokens.Decrement(divisor)
    instrs |= tokens.Increment(rem_buff)

    if dividend not in [remainder, quotient]:
        instrs |= tokens.Increment(dividend)

    else_ = move(rem_buff, [(divisor, 1)])
    if quotient:
        else_ |= tokens.Increment(quotient)
    instrs |= callz(divisor, if_zero=else_)

    instrs |= tokens.ExitLoop()

    if dynamic_divisor:
        instrs |= tokens.Clear(divisor)
        instrs |= metainfo.Free(divisor)

    if remainder:
        instrs |= tokens.Clear(remainder)

    if remainder and not dynamic_divisor:
        instrs |= move(rem_buff, [(divisor, 1), (remainder, 1)])
    elif remainder:
        instrs |= move(rem_buff, [(remainder, 1)])
    elif not dynamic_divisor:
        instrs |= move(rem_buff, [(divisor, 1)])

    else:
        instrs |= tokens.Clear(rem_buff)

    instrs |= metainfo.Free(rem_buff)
    instrs |= metainfo.Free(dividend_buff)

    return instrs
