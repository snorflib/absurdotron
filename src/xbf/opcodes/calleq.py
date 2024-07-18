import typing

import attrs

from src.xbf import dtypes, program

from .base import BaseCommand
from .callneq import CallNeq


def _calleq(
    left: dtypes.Unit,
    right: dtypes.Unit,
    if_: typing.Iterable[BaseCommand] | None,
    else_: typing.Iterable[BaseCommand] | None,
    program: program.Program,
) -> None:
    CallNeq(left, right, else_, if_)(program)


@attrs.frozen
class CallEq(BaseCommand):
    left: dtypes.Unit
    right: dtypes.Unit
    if_: typing.Iterable[BaseCommand] | None = None
    else_: typing.Iterable[BaseCommand] | None = None

    def _apply(self, context: program.Program) -> None:
        _calleq(self.left, self.right, self.if_, self.else_, context)
