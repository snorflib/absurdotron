import types as builtin_types
import typing

import attrs

from src.ir import exceptions, tokens


@attrs.frozen
class AutoMatchEnterExitLoop:
    raise_on_loop_mismatch: bool = True
    stack: list[tokens.EnterLoop] = attrs.field(init=False, factory=list)

    def __call__(self, token: tokens.BFToken) -> typing.Optional[tokens.EnterLoop]:
        if isinstance(token, tokens.EnterLoop):
            self.stack.append(token)
            return None

        if not isinstance(token, tokens.ExitLoop):
            return None

        if not self.stack:
            if self.raise_on_loop_mismatch:
                raise exceptions.NotOpenedLoopError(token)

            return None

        return self.stack.pop()

    def __enter__(self) -> typing.Self:
        return self

    def __exit__(
        self,
        exc_type: typing.Optional[type[BaseException]],
        exc: typing.Optional[BaseException],
        traceback: typing.Optional[builtin_types.TracebackType],
    ) -> None:
        self.close()

    def close(self) -> None:
        if not self.stack:
            return

        last_token = self.stack.pop()
        self.stack.clear()

        if self.raise_on_loop_mismatch:
            raise exceptions.NotClosedLoopError(last_token)
