import typing

import attrs

from src.xbf import dtypes, program

from .base import BaseCommand
from .callge import CallGE


def _callle(
    left: dtypes.Unit,
    right: dtypes.Unit,
    if_: typing.Iterable[BaseCommand] | None,
    else_: typing.Iterable[BaseCommand] | None,
    program: program.Program,
) -> None:
    CallGE(right, left, if_, else_)(program)


@attrs.frozen
class CallLE(BaseCommand):
    left: dtypes.Unit
    right: dtypes.Unit
    if_: typing.Iterable[BaseCommand] | None = None
    else_: typing.Iterable[BaseCommand] | None = None

    def _apply(self, context: program.Program) -> None:
        _callle(self.left, self.right, self.if_, self.else_, context)
