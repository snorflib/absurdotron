from __future__ import annotations

from src.ir import types

from .base import MemoptixError


class MemoryAllocationFailedError(MemoptixError):
    def __str__(self) -> str:
        return (
            "None of the solutions satisfied all constraints. "
            "Make sure you don't have any self-contradicting constraints."
        )


class OwnerIndexIsNotYetDeterminedError(MemoptixError):
    def __init__(self, owner: types.Owner) -> None:
        super().__init__(f"Index of the {owner!r} is not determined. Have you resolved the model?")
