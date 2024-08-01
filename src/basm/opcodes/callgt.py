import typing

import attrs

from src.xbf import dtypes, program

from .base import BaseCommand
from .callge import CallGE


def _callgt(
    left: dtypes.Unit,
    right: dtypes.Unit,
    if_: typing.Iterable[BaseCommand] | None,
    else_: typing.Iterable[BaseCommand] | None,
    program: program.Program,
) -> None:
    CallGE(right, left, else_, if_)(program)


@attrs.frozen
class CallGT(BaseCommand):
    left: dtypes.Unit
    right: dtypes.Unit
    if_: typing.Iterable[BaseCommand] | None = None
    else_: typing.Iterable[BaseCommand] | None = None

    def _apply(self, context: program.Program) -> None:
        _callgt(self.left, self.right, self.if_, self.else_, context)
