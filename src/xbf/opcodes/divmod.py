import attrs

from src.ir import tokens
from src.memoptix import metainfo
from src.xbf import dtypes, program

from .add import Add
from .base import BaseCommand
from .callz import CallZ
from .init import Init
from .move import MoveUnit, move


def _generic_division(
    dividend: dtypes.Unit,
    divisor: dtypes.Unit | int,
    quotient: dtypes.Unit | None,
    remainder: dtypes.Unit | None,
    program: program.Program,
) -> None:
    restore_divisor: bool = True

    if remainder is quotient is None:
        return None
    if remainder is quotient:
        raise ValueError("Remainder cannot be Quotient")

    if dividend is divisor:
        if quotient:
            program.routine.extend([tokens.Clear(quotient), tokens.Increment(quotient)])
        if remainder:
            program.routine.extend([tokens.Clear(remainder)])
        return

    if isinstance(divisor, int):
        divisor_unit = dtypes.Unit("divisor_unit")
        Init(divisor_unit)(program)
        Add(divisor_unit, divisor, divisor_unit)(program)
        divisor = divisor_unit
        restore_divisor = False

    remainder_buf = dtypes.Unit()
    dividend_buf = dtypes.Unit()

    Init(remainder_buf)(program)
    Init(dividend_buf)(program)

    program.routine.extend(move(dividend, [(dividend_buf, 1)]))
    program.routine.append(tokens.EnterLoop(dividend_buf))
    program.routine.append(tokens.Decrement(dividend_buf))
    program.routine.append(tokens.Decrement(divisor))
    program.routine.append(tokens.Increment(remainder_buf))

    if dividend not in [remainder, quotient]:
        program.routine.append(tokens.Increment(dividend))

    else_: list[BaseCommand] = [MoveUnit(remainder_buf, [(divisor, 1)])]
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


@attrs.frozen
class DivModUnit(BaseCommand):
    dividend: dtypes.Unit
    divisor: dtypes.Unit | int
    quotient: dtypes.Unit | None = None
    remainder: dtypes.Unit | None = None

    def _apply(self, context: program.Program) -> None:
        _generic_division(
            self.dividend,
            self.divisor,
            self.quotient,
            self.remainder,
            context,
        )
