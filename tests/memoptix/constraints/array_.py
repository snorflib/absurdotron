import pytest

from src import memoptix
from src.ir import tokens


def _check_two_intervals_not_intersecting(x_start: int, x_end: int, y_start: int, y_end: int) -> bool:
    return x_start >= y_end or y_start >= x_end


def test_array_segregation_intersecting_lifecycles() -> None:
    """Test that owners with intersecting lifecycles are not assigned the same memory address."""

    program = [tokens.Increment("a"), tokens.Increment("b"), tokens.Decrement("a"), tokens.Increment("b")]
    meta = memoptix.get_metainfo_from_routine(program)

    constraints = [memoptix.ArrayConstraint("a", 5), memoptix.UnitConstraint("b")]
    resolver = memoptix.build_memory_resolver(constraints, meta)
    resolver.resolve()

    indexes = resolver.model.get_vars_by_owners(meta.owners)
    assert indexes["a"] != indexes["b"]
    assert indexes["b"] not in range(indexes["a"], indexes["a"] + 5)


def test_two_array_lifecycles() -> None:
    """Test that owners with intersecting lifecycles are not assigned the same memory address."""
    program = [
        tokens.Increment("a"),
        tokens.EnterLoop("a"),
        tokens.Increment("b"),
        tokens.Increment("d"),
        tokens.ExitLoop(),
        tokens.Increment("b"),
        tokens.Increment("d"),
        tokens.Decrement("a"),
    ]
    meta = memoptix.get_metainfo_from_routine(program)

    constraints = [memoptix.ArrayConstraint("a", 5), memoptix.ArrayConstraint("b", 10), memoptix.UnitConstraint("d")]
    resolver = memoptix.build_memory_resolver(constraints, meta)
    resolver.resolve()

    indexes = resolver.model.get_vars_by_owners(meta.owners)
    a_start, b_start = indexes["a"], indexes["b"]

    assert a_start != b_start != indexes["d"]
    assert _check_two_intervals_not_intersecting(a_start, a_start + 5, b_start, b_start + 10)


def test_arrays_with_links_resolvable() -> None:
    """Test that owners with intersecting lifecycles are not assigned the same memory address."""

    program = [tokens.Increment("a"), tokens.Increment("b"), tokens.Decrement("a"), tokens.Increment("b")]
    meta = memoptix.get_metainfo_from_routine(program)

    constraints = [
        memoptix.ArrayConstraint("a", 5),
        memoptix.UnitConstraint("b"),
        memoptix.LinkedConstraint(from_="a", to_="b", length=6),
    ]
    resolver = memoptix.build_memory_resolver(constraints, meta)
    resolver.resolve()

    indexes = resolver.model.get_vars_by_owners(meta.owners)
    assert indexes["b"] >= indexes["a"] + 5


def test_arrays_with_links_unresolvable() -> None:
    """Test that owners with intersecting lifecycles are not assigned the same memory address."""

    program = [tokens.Increment("a"), tokens.Increment("b"), tokens.Decrement("a"), tokens.Increment("b")]
    meta = memoptix.get_metainfo_from_routine(program)

    constraints = [
        memoptix.ArrayConstraint("a", 5),
        memoptix.UnitConstraint("b"),
        memoptix.LinkedConstraint(from_="a", to_="b", length=1, factor=None),
    ]
    resolver = memoptix.build_memory_resolver(constraints, meta)

    with pytest.raises(memoptix.MemoryAllocationFailedError):
        resolver.resolve()


def test_array_place_reallocation() -> None:
    program = [
        tokens.Increment("a"),
        tokens.Increment("b"),
        memoptix.Free("b"),
        memoptix.Free("a"),
        tokens.Decrement("c"),
        memoptix.Free("c"),
    ]
    meta = memoptix.get_metainfo_from_routine(program)

    constraints = [
        memoptix.ArrayConstraint("a", 10),
        memoptix.ArrayConstraint("b", 5),
        memoptix.ArrayConstraint("c", 10),
    ]
    resolver = memoptix.build_memory_resolver(constraints, meta)
    resolver.resolve()

    indexes = resolver.model.get_vars_by_owners(meta.owners)
    assert (indexes["a"] == indexes["c"]) or (indexes["b"] == indexes["c"])
