import uuid


class DType:
    __slots__ = (
        "id",
        "name",
    )

    def __init__(self, name: str | None = None, id: int | None = None) -> None:
        self.name = name
        self.id = id or uuid.uuid4().int

    def __hash__(self) -> int:
        return self.id

    def __repr__(self) -> str:
        return f"{type(self).__name__}( {self.name or self.id} )"
