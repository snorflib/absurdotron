from __future__ import annotations

import collections.abc

from src.ir import tokens, tools, types
from src.ir.tokens.injection import CompilerInjection

from .code import Code
from .pointer import Pointer


def _assemble(
    code: Code,
    pointer: Pointer,
    routine: collections.abc.Collection[tokens.BFToken],
    memory: dict[types.Owner, int],
) -> None:
    with tools.AutoMatchEnterExitLoop() as matcher:
        for token in routine:
            curr_token = matcher(token) or token
            so, eo = _get_token_owner(curr_token)
            value = _get_token_value(curr_token)

            pointer.move(memory.get(so, None))
            code.add(value)
            pointer.move(memory.get(eo, None), gen_path=False)


def _get_token_owner(token: tokens.BFToken) -> tuple[types.Owner | None, types.Owner | None]:
    start_owner = end_owner = token.owner
    if isinstance(token, CompilerInjection):
        end_owner = token.end_owner

    return start_owner, end_owner


def _get_token_value(token: tokens.BFToken) -> str:
    return getattr(token, "value", "")
