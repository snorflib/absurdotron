
import attrs

from . import base, dtypes
from .callneq import CallNeq


@attrs.frozen
class CallEq(base.OpCode):
    left: dtypes.Unit
    right: dtypes.Unit
    if_: base.OpCodeReturn | None = None
    else_: base.OpCodeReturn | None = None

    def _execute(self) -> None:
        _calleq(self.left, self.right, self.if_, self.else_)


def _calleq(
    left: dtypes.Unit,
    right: dtypes.Unit,
    if_: base.OpCodeReturn | None,
    else_: base.OpCodeReturn | None,
) -> None:
    CallNeq(left, right, else_, if_)(program)
