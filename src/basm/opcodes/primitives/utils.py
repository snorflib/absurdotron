import typing

import attrs

from src.basm.opcodes import base, context
from src.ir import tokens

P = typing.ParamSpec("P")
T = typing.TypeVar("T", bound=tokens.BFToken)


@attrs.frozen
class TokenArgs(base.OpCodeArgs):
    args: typing.Iterable[typing.Any]
    kwargs: typing.Mapping[str, typing.Any]
    token: typing.Callable[P, tokens.BFToken]


@attrs.frozen
class _TokenOpCode(base.OpCode[TokenArgs]):
    def _execute(self, context: context.Context) -> base.OpCodeReturn:
        return base.OpCodeReturn([self.args.token(*self.args.args, **self.args.kwargs)])


def token2opcode(token: typing.Callable[P, T]) -> typing.Callable[P, _TokenOpCode]:
    def constructor(*args: P.args, **kwargs: P.kwargs) -> _TokenOpCode:
        op_args = TokenArgs(args, kwargs, token)
        return _TokenOpCode(op_args)

    return constructor
