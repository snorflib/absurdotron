import collections.abc

import bidict

from src.ir import exceptions, tokens


def build_jump_map(
    routine: collections.abc.Collection[tokens.BFToken],
) -> tuple[bidict.bidict[int, int], dict[int, tokens.EnterLoop | tokens.ExitLoop]]:
    stack: list[tuple[int, tokens.EnterLoop]] = []
    token_map: dict[int, tokens.EnterLoop | tokens.ExitLoop] = {}
    jump_map: bidict.bidict[int, int] = bidict.bidict()

    for idx, token in enumerate(routine):
        if isinstance(token, tokens.EnterLoop):
            stack.append((idx, token))
        elif isinstance(token, tokens.ExitLoop):
            if not stack:
                raise exceptions.NotOpenedLoopError(token)

            idx_, token_ = stack.pop()
            jump_map[idx_] = idx

            token_map[idx_] = token_
            token_map[idx] = token

    if stack:
        raise exceptions.NotClosedLoopError(stack.pop()[1])

    return jump_map, token_map
