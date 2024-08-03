from __future__ import annotations

import collections.abc

from src.ir import tokens, tools, types

from .code import Code
from .pointer import Pointer


def assemble(
    code: Code,
    pointer: Pointer,
    routine: collections.abc.Collection[tokens.BFToken],
    memory: dict[types.Owner, int],
) -> None:
    with tools.AutoMatchEnterExitLoop() as matcher:
        for curr_token in routine:
            owner_token = matcher(curr_token) or curr_token
            so, eo = _get_token_owner(owner_token)
            value = _get_token_value(curr_token)

            pointer.move(memory.get(so, None))
            code.add(value)
            pointer.move(memory.get(eo, None), gen_path=False)


def _get_token_owner(token: tokens.BFToken) -> tuple[types.Owner | None, types.Owner | None]:
    start_owner = end_owner = token.owner
    if isinstance(token, tokens.CompilerInjection):
        end_owner = token.end_owner

    return start_owner, end_owner


def _get_token_value(token: tokens.BFToken) -> str:
    return getattr(token, "value", "")
