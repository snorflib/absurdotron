from .base import DType


class Array(DType):
    __slots__ = (
        "length",
        "granularity",
    )

    def __init__(self, length: int, granularity: int = 1, name: str | None = None, id: int | None = None) -> None:
        super().__init__(name, id)
        self.length = length
        self.granularity = granularity
