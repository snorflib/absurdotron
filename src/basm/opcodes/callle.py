import typing

import attrs

from . import base, dtypes
from .callge import _callge


@attrs.frozen
class CallLE(base.OpCode):
    left: dtypes.Unit
    right: dtypes.Unit
    if_le: base.OpCodeReturn | None = None
    else_: base.OpCodeReturn | None = None

    def _execute(self) -> base.OpCodeReturn:
        return _callge(self.right, self.left, self.if_le, self.else_)
