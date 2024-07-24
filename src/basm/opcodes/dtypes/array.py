import attrs

from .base import DType


@attrs.frozen
class Array(DType):
    length: int
    granularity: int = 1
