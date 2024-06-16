from .base import DType


class Array(DType):
    __slots__ = ("length",)

    def __init__(self, length: int, name: str | None = None, id: int | None = None) -> None:
        super().__init__(name, id)
        self.length = length
