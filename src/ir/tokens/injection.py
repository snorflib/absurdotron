import attrs

from src.ir import types

from .base import BFToken
from .utils import check_injection_safety


@attrs.frozen
class CompilerInjection(BFToken):
    """
    A class representing a compiler injection token in the compiler.
    """

    value: str
    end_owner: types.Owner | None = None

    def __attrs_post_init__(self) -> None:
        if self.end_owner is None:
            object.__setattr__(self, "end_owner", self.owner)


@attrs.frozen
class CommentInjection(CompilerInjection):
    """
    A subclass of 'CompilerInjection' specifically for injecting comments into the compiler output.
    """

    value: str = attrs.field(validator=check_injection_safety)
    owner: types.Owner | None = attrs.field(init=False, default=None)
    end_owner: types.Owner | None = attrs.field(init=False, default=None)


@attrs.frozen
class CodeInjection(CompilerInjection):
    """
    A class for code injection tokens, inheriting from 'CompilerInjection'.

    This token has been inherited, to possibly be extended with checks and more functionality in the future.
    """
