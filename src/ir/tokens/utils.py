from __future__ import annotations

import re

import attrs

from src.ir import exceptions

from .base import BFToken


def check_injection_safety(_inst: BFToken, _attr: attrs.Attribute, info: str) -> None:  # type: ignore
    """
    Validate the given string for BrainFuck command character injection.

    This function checks if the `info` string contains any BrainFuck command characters.
    If such characters are detected, a `CodeSemanticsViolationError` is raised.
    """
    match = re.match(r".*([,.><\[\]+-]).*", info)
    if match is not None:
        raise exceptions.CodeSemanticsViolationError(info, match.start(1))
