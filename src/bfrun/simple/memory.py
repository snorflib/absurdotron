import typing

import numpy as np

_DEFAULT_MAX_CELLS: typing.Final[int] = 30_000


class Memory:
    __slots__ = (
        "_array",
        "_pointer",
        "_size",
    )

    def __init__(self, size: int = _DEFAULT_MAX_CELLS) -> None:
        self._array = np.zeros((size,), dtype=np.uint8)
        self._size = size
        self._pointer = 0

    def increment_ptr(self) -> None:
        if self._pointer == self._size - 1:
            raise ValueError("Trying to move the pointer past the array size.")
        self._pointer += 1

    def decrement_ptr(self) -> None:
        if self._pointer == 0:
            raise ValueError("Trying to move the pointer below zero")
        self._pointer -= 1

    def store(self, data: int | str) -> None:
        if isinstance(data, str):
            data = ord(data)

        self._array[self._pointer] = data

    def load(self) -> int:
        return self._array[self._pointer]  # type: ignore

    def increment_data(self) -> None:
        self._array[self._pointer] += 1

    def decrement_data(self) -> None:
        self._array[self._pointer] -= 1

    @property
    def pointer(self) -> int:
        return self._pointer

    @pointer.setter
    def pointer(self, value: int) -> None:
        if value < 0:
            raise ValueError("Trying to set pointer smaller then zero.")
        elif value == self._size - 1:
            raise ValueError(f"Trying to set pointer larger then memory. Memory size: {self._size}")

        self._pointer = value
