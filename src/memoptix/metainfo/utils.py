import collections.abc
import typing

from src.ir import tokens, tools, types

from .free import Free
from .scope import OwnerUsageScope


def find_optimal_usage_scope(
    scope_estimate: tuple[int, int], loops: typing.Iterable[tuple[int, int]]
) -> tuple[int, int]:
    """
    Resizes a rough-usage estimation to ensure its safety for merging with other usage intervals.
    This adjustment is done to ensure that when a memory unit is re-used, older data is not needed.

    :param scope_estimate: The initial rough estimate of the memory usage interval.
    :param loops: A list of loop intervals to consider for adjustment.
    :return: An adjusted interval that avoids unnecessary overlap with loop intervals.
    """

    def overlap(a: tuple[int, int], b: tuple[int, int]) -> bool:
        return a[0] <= b[1] and b[0] <= a[1]

    def within(a: tuple[int, int], b: tuple[int, int]) -> bool:
        return b[0] <= a[0] and a[1] <= b[1]

    def adjust_interval(candidate: tuple[int, int], other: tuple[int, int]) -> tuple[int, int]:
        if within(candidate, other) or within(other, candidate):
            return candidate
        else:
            start = min(candidate[0], other[0])
            end = max(candidate[1], other[1])
            return start, end

    loops = sorted(loops, key=lambda x: x[0])
    for loop in loops:
        if overlap(scope_estimate, loop) and not within(scope_estimate, loop) and not within(loop, scope_estimate):
            scope_estimate = adjust_interval(scope_estimate, loop)

    return scope_estimate


def get_memory_owner_scopes(routine: collections.abc.Sequence[tokens.BFToken]) -> dict[types.Owner, OwnerUsageScope]:
    jump_map, token_map = tools.build_jump_map(routine)
    life_cycles: dict[types.Owner, tuple[int, int]] = {}
    freed_owners: set[types.Owner] = set()

    for idx, token in enumerate(routine):
        if isinstance(token, tokens.CompilerInjection) and (end_owner := token.end_owner):
            life_cycles[end_owner] = (life_cycles[end_owner][0], life_cycles[end_owner][1])

        if isinstance(token, tokens.ExitLoop):
            owner = token_map[jump_map.inverse[idx]].owner
        elif (owner := token.owner) is None:
            continue

        if owner not in life_cycles:
            life_cycles[owner] = (idx, len(routine))
        elif isinstance(token, Free):
            life_cycles[owner] = (life_cycles[owner][0], idx)
            freed_owners.add(owner)
        elif owner in freed_owners:
            raise ValueError(f"Owner was freed, but it now referenced by {token} at index {idx}")

    if len(freed_owners) > len(life_cycles):
        # Warn user. Not needed
        ...

    scopes: dict[types.Owner, OwnerUsageScope] = {}
    for owner, bounds in life_cycles.items():
        scopes[owner] = OwnerUsageScope(
            owner=owner,
            rough_bounds=life_cycles[owner],
            adjusted_bounds=find_optimal_usage_scope(bounds, jump_map.items()),
        )

    return scopes
