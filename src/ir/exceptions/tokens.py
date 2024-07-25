import re

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

    blank_line_regex = r"(?:\r?\n){2,}"
    left_side_string = re.split(blank_line_regex, code_segment[before:index].strip())[-1]
    right_side_string = re.split(blank_line_regex, code_segment[index:after].strip())[0]

    return f"\n\n\t\t{left_side_string:>20}{right_side_string:<20}\n\t\t{error_indicator:^40}\n\n{message}"


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
