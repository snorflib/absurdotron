
import attrs

from . import base, dtypes
from .callneq import _callneq


@attrs.frozen
class CallEq(base.OpCode):
    left: dtypes.Unit
    right: dtypes.Unit
    if_eq: base.OpCodeReturn | None = None
    else_: base.OpCodeReturn | None = None

    def _execute(self) -> base.OpCodeReturn:
        return _calleq(self.left, self.right, self.if_eq, self.else_)


def _calleq(
    left: dtypes.Unit,
    right: dtypes.Unit,
    if_eq: base.OpCodeReturn | None,
    else_: base.OpCodeReturn | None,
) -> base.OpCodeReturn:
    return _callneq(left, right, else_, if_eq)
