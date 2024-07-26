from .base import OpCode, OpCodeArgs, OpCodeReturn
from .init import Init
from .primitives import (
    CDI,
    CMI,
    DEC,
    DSP,
    ETL,
    EXL,
    INC,
    INP,
)

__all__ = (
    "OpCode",
    "OpCodeArgs",
    "OpCodeReturn",
    #
    "DSP",
    "INP",
    "INC",
    "DEC",
    "ETL",
    "EXL",
    "CMI",
    "CDI",
    #
    "Init",
)
