from .base import BFToken
from .commands import (
    Clear,
    Command,
    Decrement,
    Display,
    EnterLoop,
    ExitLoop,
    Increment,
    Input,
)
from .injection import (
    CodeInjection,
    CommentInjection,
    CompilerInjection,
)

ORDER_FIXED_TOKENS = (
    "Display",
    "Input",
    "EnterLoop",
    "ExitLoop",
    "Clear",
    "CompilerInjection",
    "CommentInjection",
    "CodeInjection",
)

__all__ = (
    "BFToken",
    "Command",
    "Increment",
    "Decrement",
    "Display",
    "Input",
    "EnterLoop",
    "ExitLoop",
    "Clear",
    "CompilerInjection",
    "CommentInjection",
    "CodeInjection",
    "ORDER_FIXED_TOKENS",
)
