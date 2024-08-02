from src.ir import tokens

from . import base, dtypes


@base.convert
def add_int_long(value: int, unit: dtypes.Unit) -> list[tokens.Increment | tokens.Decrement]:
    token: type[tokens.Increment] | type[tokens.Decrement] = tokens.Increment if value > 0 else tokens.Decrement
    return [token(owner=unit)] * abs(value)
