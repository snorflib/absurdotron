import attrs

from src.ir import types


@attrs.frozen
class OwnerUsageScope:
    owner: types.Owner
    adjusted_bounds: tuple[int, int]
    rough_bounds: tuple[int, int]
