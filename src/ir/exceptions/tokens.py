
from .base import IRError


def _format_message(code_segment: str, index: int, error_indicator: str, message: str) -> str:
    """
    Formats an exception message to highlight a specific segment of code.

    :param code_segment: The string segment of the code where the error is found.
    :param index: The index within the code segment where the error starts.
    :param error_indicator: A string of '^' characters highlighting the error location.
    :param message: A descriptive message about the error.
    :return: A formatted string combining the code segment and error details.
    """
    before = max(index - 20, 0)
    after = max(index + 20, len(code_segment))
    return (
        f"\n\n"
        f"\t\t{code_segment[before:index]:>20}{code_segment[index:after]:<20}\n"
        f"\t\t{error_indicator:^40}\n\n"
        f"{message}"
    )


class CodeSemanticsViolationError(IRError):
    """
    Exception raised for violations of code semantics during code processing.

    This exception is used to indicate that a segment of code contains characters
    or constructs that violate the expected semantics, potentially leading to
    incorrect or unintended behavior.

    :param code_segment: The code segment where the semantic violation is detected.
    :param index: The index within the code segment where the violation begins.
    """

    def __init__(self, code_segment: str, index: int) -> None:
        message = _format_message(
            code_segment,
            index,
            "^^^^^",
            "Text contains characters that can affect programs' semantic.",
        )
        super().__init__(message)
