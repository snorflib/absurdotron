import attrs

from src.ir import tokens
from src.memoptix import metainfo
from src.xbf import dtypes, program

from . import base
from .add import _add_int
from .callz import CallZ
from .init import init
from .move import Move, move


@attrs.frozen
class DivMod(base.BaseCommand):
    dividend: dtypes.Unit | int
    divisor: dtypes.Unit | int
    quotient: dtypes.Unit | None = None
    remainder: dtypes.Unit | None = None

    def _apply(self, context: program.Program) -> base.CommandReturn:
        return div(self.dividend, self.divisor, self.quotient, self.remainder)


@base.flatten2return
def div(
    dividend: dtypes.Unit | int,
    divisor: dtypes.Unit | int,
    quotient: dtypes.Unit | None,
    remainder: dtypes.Unit | None,
) -> base.ToFlatten:
    if remainder is quotient is None:
        return None
    elif remainder == quotient:
        raise ValueError("Remainder cannot be Quotient")
    elif isinstance(dividend, int) and isinstance(divisor, int):
        return _div_ints(dividend, divisor, quotient, remainder)
    elif dividend == divisor:
        return _div_by_itself(quotient, remainder)

    return _div_standard(dividend, divisor, quotient, remainder)


@base.flatten2return
def _div_ints(
    dividend: int,
    divisor: int,
    quotient: dtypes.Unit | None,
    remainder: dtypes.Unit | None,
) -> base.CommandReturn:
    quot, rem = divmod(dividend, divisor)

    instrs = base.CommandReturn()

    if quotient:
        instrs |= tokens.Clear(quotient)
        instrs |= _add_int(quot, quotient)

    if remainder:
        instrs |= tokens.Clear(remainder)
        instrs |= _add_int(rem, remainder)

    return instrs


@base.flatten2return
def _div_by_itself(
    quotient: dtypes.Unit | None,
    remainder: dtypes.Unit | None,
) -> base.CommandReturn:
    instrs = base.CommandReturn()

    if quotient:
        instrs |= tokens.Clear(quotient)
        instrs |= tokens.Increment(quotient)
    if remainder:
        instrs |= tokens.Clear(remainder)
    return instrs


@base.flatten2return
def _div_standard(
    dividend: dtypes.Unit | int,
    divisor: dtypes.Unit | int,
    quotient: dtypes.Unit | None,
    remainder: dtypes.Unit | None,
) -> base.CommandReturn:
    instrs = base.CommandReturn()

    rem_buff, dividend_buff = dtypes.Unit(), dtypes.Unit()
    instrs |= init(rem_buff) | init(dividend_buff)

    restore_divisor: bool = True

    if isinstance(dividend, int):
        instrs |= _add_int(dividend, dividend_buff)
    else:
        instrs |= move(dividend, [(dividend_buff, 1)])

    instrs |= tokens.EnterLoop(dividend_buff)
    instrs |= tokens.Decrement(dividend_buff)
    instrs |= tokens.Decrement(divisor)
    instrs |= tokens.Increment(rem_buff)

    if dividend not in [remainder, quotient]:
        instrs |= tokens.Increment(dividend)

    else_: list[BaseCommand] = [Move(remainder_buf, [(divisor, 1)])]
    if quotient:
        else_.append(Add(quotient, 1, quotient))
    CallZ(divisor, else_=else_)(program)

    program.routine.append(tokens.ExitLoop())

    if restore_divisor:
        Add(remainder_buf, 0, divisor)(program)
    else:
        program.routine.append(tokens.Clear(divisor))
        program.routine.append(metainfo.Free(divisor))

    if remainder:
        program.routine.extend([tokens.Clear(remainder)])
        program.routine.extend(move(remainder_buf, [(remainder, 1)]))
    else:
        program.routine.append(tokens.Clear(remainder_buf))

    program.routine.extend(
        [
            metainfo.Free(remainder_buf),
            metainfo.Free(dividend_buf),
        ]
    )

    return instrs
