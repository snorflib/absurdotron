import pytest

from src.ir import tokens
from src.memoptix import metainfo
from src.memoptix.metainfo import utils


@pytest.mark.parametrize(
    "scope_estimate, loops, expected_result",
    [
        # No overlap with single loop
        ((2, 5), [(6, 9)], (2, 5)),
        # Overlap with single loop, adjustment expected
        ((2, 5), [(4, 6)], (2, 6)),
        # Complete overlap within the loop
        ((2, 5), [(1, 6)], (2, 5)),
        # Multiple loops, no overlap with scope estimate
        ((2, 5), [(1, 1), (6, 7)], (2, 5)),
        # Multiple loops, one overlapping loop
        ((2, 5), [(1, 3), (4, 6), (7, 9)], (1, 6)),
        # Edge case with overlapping ends
        ((2, 5), [(5, 7)], (2, 7)),
        # Check for non-mutating for contained scope
        ((2, 4), [(1, 5)], (2, 4)),
        # Check nested loops
        ((6, 8), [(5, 7), (1, 10)], (5, 8)),
    ],
)
def test_find_optimal_usage_scope(
    scope_estimate: tuple[int, int],
    loops: list[tuple[int, int]],
    expected_result: tuple[int, int],
) -> None:
    """
    Tests the find_optimal_usage_scope function with various scenarios to ensure correct interval adjustments.
    """
    assert utils.find_optimal_usage_scope(scope_estimate, loops) == expected_result


def test_rough_scopes_no_loops() -> None:
    sequence = [
        tokens.Increment("1"),
        tokens.Decrement("1"),
        metainfo.Free("1"),
        tokens.Increment("2"),
        tokens.Decrement("3"),
        metainfo.Free("3"),
        tokens.Decrement("2"),
        metainfo.Free("2"),
    ]
    info = metainfo.get_metainfo_from_routine(sequence)

    assert info.scopes["1"].rough_bounds == (0, 2)
    assert info.scopes["2"].rough_bounds == (3, 7)
    assert info.scopes["3"].rough_bounds == (4, 5)


def test_rough_bounds_with_loops() -> None:
    sequence = [
        tokens.Increment("1"),
        tokens.Decrement("1"),
        tokens.EnterLoop("3"),
        tokens.Increment("2"),
        tokens.EnterLoop("1"),
        tokens.Increment("2"),
        metainfo.Free("2"),
        tokens.ExitLoop(),
        metainfo.Free("1"),
        tokens.Decrement("4"),
        tokens.ExitLoop(),
        metainfo.Free("3"),
        tokens.Decrement("4"),
        metainfo.Free("4"),
    ]
    info = metainfo.get_metainfo_from_routine(sequence)
    assert info.scopes["1"].rough_bounds == (0, 8)
    assert info.scopes["2"].rough_bounds == (3, 6)
    assert info.scopes["3"].rough_bounds == (2, 11)
    assert info.scopes["4"].rough_bounds == (9, 13)


def test_adjusted_bounds_no_loops() -> None:
    sequence = [
        tokens.Increment("1"),
        tokens.Decrement("1"),
        metainfo.Free("1"),
        tokens.Increment("2"),
        tokens.Decrement("3"),
        tokens.Decrement("2"),
        metainfo.Free("3"),
        metainfo.Free("2"),
    ]
    info = metainfo.get_metainfo_from_routine(sequence)
    assert info.scopes["1"].adjusted_bounds == (0, 2)
    assert info.scopes["2"].adjusted_bounds == (3, 7)
    assert info.scopes["3"].adjusted_bounds == (4, 6)


def test_adjusted_bounds_with_loops() -> None:
    sequence = [
        tokens.Increment("1"),
        tokens.Decrement("1"),
        tokens.EnterLoop("3"),
        tokens.Increment("2"),
        tokens.EnterLoop("1"),
        tokens.Increment("2"),
        metainfo.Free("2"),
        tokens.ExitLoop(),
        tokens.Decrement("4"),
        tokens.ExitLoop(),
        metainfo.Free("1"),
        metainfo.Free("3"),
        tokens.Decrement("4"),
        metainfo.Free("4"),
    ]
    info = metainfo.get_metainfo_from_routine(sequence)

    assert info.scopes["1"].adjusted_bounds == (0, 10)
    assert info.scopes["2"].adjusted_bounds == (3, 7)
    assert info.scopes["3"].adjusted_bounds == (2, 11)
    assert info.scopes["4"].adjusted_bounds == (2, 13)
