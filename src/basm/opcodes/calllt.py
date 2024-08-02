
import attrs

from . import base, dtypes
from .callge import _callge


@attrs.frozen
class CallLT(base.OpCode):
    left: dtypes.Unit
    right: dtypes.Unit
    if_lt: base.OpCodeReturn | None = None
    else_: base.OpCodeReturn | None = None

    def _execute(self) -> base.OpCodeReturn:
        return _callge(self.left, self.right, self.else_, self.if_lt)
