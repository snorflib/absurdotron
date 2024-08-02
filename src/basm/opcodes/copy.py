import attrs

from src.ir import tokens
from src.memoptix import metainfo

from . import base, dtypes
from .init import init
from .move import move



@attrs.frozen
class Copy(base.OpCode):
    from_: dtypes.Unit
    to_: dtypes.Unit

    def _execute(self) -> base.OpCodeReturn:
        return copy(self.from_, self.to_)


@base.convert
def copy(from_: dtypes.Unit, to_: dtypes.Unit) -> base.ToConvert:
    if from_ == to_:
        return []

    buffer = dtypes.Unit()

    return init(buffer) | tokens.Clear(to_) | move(from_, [(buffer, 1)]) | move(buffer, [(from_, 1), (to_, 1)]) | metainfo.Free(buffer)
