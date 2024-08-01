import typing

import attrs

from . import base, dtypes
from .callge import _callge


@attrs.frozen
class CallGT(base.OpCode):
    left: dtypes.Unit
    right: dtypes.Unit
    if_gt: base.OpCodeReturn | None = None
    else_: base.OpCodeReturn | None = None

    def _execute(self) -> base.OpCodeReturn:
        return _callge(self.right, self.left, self.else_, self.if_gt)
