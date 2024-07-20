from __future__ import annotations

import typing

from src.ir import tokens

from .base import IRError


class NotClosedLoopError(IRError):
    """
    Raised when a BrainFuck loop is not properly closed.

    This exception is thrown when an `EnterLoop` token does not have a corresponding `ExitLoop` token, indicating
    an unclosed loop in the BrainFuck code.

    :param token: Optional; the `EnterLoop` token instance where the loop starts.
    :type token: EnterLoop, optional
    """

    def __init__(self, token: typing.Optional[tokens.EnterLoop] = None) -> None:
        if token is None:
            message = "Loop not closed."

        else:
            message = f"Loop starting with {token} was never closed."

        super().__init__(message)


class NotOpenedLoopError(IRError):
    """
    Raised when a BrainFuck loop is closed without being opened.

    This exception is triggered when an `ExitLoop` token is encountered without a preceding `EnterLoop` token,
    indicating an attempt to close a loop that was never opened.

    :param token: Optional; the `ExitLoop` token instance where the erroneous loop closure occurs.
    :type token: ExitLoop, optional
    """

    def __init__(self, token: typing.Optional[tokens.ExitLoop] = None) -> None:
        if token is None:
            message = "Trying to close an unopened loop."

        else:
            message = f"Loop {token} was never opened in the first place."

        super().__init__(message)
