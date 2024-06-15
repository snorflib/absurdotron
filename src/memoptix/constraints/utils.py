from src.ir import types
from src.memoptix import metainfo


def _intervals_intersects(int1: tuple[int, int], int2: tuple[int, int]) -> bool:
    """
    Determine if two intervals intersects.

    :param int1: The first interval as a tuple of two integers.
    :param int2: The second interval as a tuple of two integers.
    :return: True if the intervals overlap, False otherwise.
    """
    return max(int1[1], int2[1]) - min(int1[0], int2[0]) < (int1[1] - int1[0]) + (int2[1] - int2[0]) or (
        (int1[0] <= int2[0]) and (int1[1] >= int2[1])
    )


def get_all_intersected_owners(
    scopes: dict[types.Owner, metainfo.OwnerUsageScope],
) -> list[tuple[types.Owner, types.Owner]]:
    """
    Get indices of all intersecting intervals in a list of intervals.
    """

    intersections = []
    length = len(scopes)
    infos = list(scopes.items())

    for a_idx, (owner, meta_info) in enumerate(infos):
        bounds_a = meta_info.adjusted_bounds
        if a_idx + 1 == length:
            break

        for owner_b, meta_info2 in infos[a_idx + 1 :]:
            bounds_b = meta_info2.adjusted_bounds

            if _intervals_intersects(bounds_a, bounds_b):
                intersections.append((owner, owner_b))

    return intersections
