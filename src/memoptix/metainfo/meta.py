import collections.abc

import attrs

from src.ir import tokens, types

from .scope import OwnerUsageScope
from .utils import get_memory_owner_scopes


@attrs.frozen
class RoutineMetaInfo:
    scopes: dict[types.Owner, OwnerUsageScope]
    owners: set[types.Owner]
    routine: collections.abc.Sequence[tokens.BFToken]


def get_metainfo_from_routine(routine: collections.abc.Sequence[tokens.BFToken]) -> RoutineMetaInfo:
    scopes = get_memory_owner_scopes(routine)
    return RoutineMetaInfo(
        scopes=scopes,
        owners=set(scopes.keys()),
        routine=routine,
    )
