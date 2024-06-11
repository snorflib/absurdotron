import typing

import attrs

from .code import Code

_MOVE_LEFT: typing.Final[str] = "<"
_MOVE_RIGHT: typing.Final[str] = ">"
_DEFAULT_START_POSITION: typing.Final[int] = 0


@attrs.define
class Pointer:
    code: Code
    position: int = attrs.field(default=_DEFAULT_START_POSITION)

    def move(self, new_pos: typing.Optional[int], gen_path: bool = True) -> None:
        if new_pos is None:
            return
        if gen_path:
            self.code.add(self._get_path(new_pos))

        self.position = new_pos

    def _get_path(self, new_pos: int) -> str:
        direction = _MOVE_RIGHT if new_pos > self.position else _MOVE_LEFT
        return direction * abs(self.position - new_pos)
