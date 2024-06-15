from __future__ import annotations

from src.ir import types
from src.memoptix import constraints

from .base import MemoptixError


class ReferencingUnknownOwnerError(MemoptixError):
    def __init__(self, owner: types.Owner) -> None:
        self.owner = owner
        super().__init__()

    def __str__(self) -> str:
        return (
            f"An unknown owner {self.owner!r} was referenced. Possible solutions:"
            f"\n\tUsed owner was not added to a model."
            f"\n\tOwner and its variable have different names."
        )


class LinkingFromUnknownOwnerError(ReferencingUnknownOwnerError):
    def __init__(self, link: constraints.LinkedConstraint) -> None:
        self.link = link
        super().__init__(link.from_)

    def __str__(self) -> str:
        return f"Trying to apply a link {self.link} with unknown link departure: {self.link.from_!r}"


class LinkingToUnknownOwnerError(ReferencingUnknownOwnerError):
    def __init__(self, link: constraints.LinkedConstraint) -> None:
        self.link = link
        super().__init__(link.to_)

    def __str__(self) -> str:
        return f"Trying to apply a link {self.link} with unknown link destination: {self.link.to_!r}"
