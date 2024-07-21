from src.ir import tokens

from .utils import token2opcode

DSP = token2opcode(tokens.Display)
INP = token2opcode(tokens.Input)

INC = token2opcode(tokens.Increment)
DEC = token2opcode(tokens.Decrement)

ETL = token2opcode(tokens.EnterLoop)
EXL = token2opcode(tokens.ExitLoop)

CMI = token2opcode(tokens.CommentInjection)
CDI = token2opcode(tokens.CodeInjection)

__all__ = (
    "DSP",
    "INP",
    "INC",
    "DEC",
    "ETL",
    "EXL",
    "CMI",
    "CDI",
)
