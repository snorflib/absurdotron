import pytest

from src import memoptix
from src.ir import tokens


def test_link_basic_constant_distance() -> None:
    """Test that memoptix.LinkedConstraint enforces a constant distance correctly between two owners."""
    program = [tokens.Increment("a"), tokens.Decrement("b")]
    meta = memoptix.get_metainfo_from_routine(program)

    constraints = [memoptix.LinkedConstraint(from_="a", to_="b", length=5, factor=None)]
    resolver = memoptix.build_memory_resolver(constraints, meta)
    indexes = resolver.resolve().model.get_vars_by_owners(meta.owners)

    assert indexes["b"] == indexes["a"] + 5, "Owner 'b' should be exactly 5 places away from 'a'"


def test_link__linking_error() -> None:
    """Test that linking an owner to it raises a ValueError."""
    with pytest.raises(ValueError):
        memoptix.LinkedConstraint(from_="a", to_="a", length=5)


def test_link_scaled_distance() -> None:
    """Test that memoptix.LinkedConstraint correctly applies scaling to the distance."""
    program = [tokens.Increment("a"), tokens.Decrement("b")]
    meta = memoptix.get_metainfo_from_routine(program)

    constraints = [memoptix.LinkedConstraint(from_="a", to_="b", length=5)]
    resolver = memoptix.build_memory_resolver(constraints, meta)
    indexes = resolver.resolve().model.get_vars_by_owners(meta.owners)

    assert indexes["b"] >= indexes["a"] + 5
    assert indexes["a"] % 5 == 0


def test_link_consistent_factor_scaling() -> None:
    """Ensure links with the same factor string scale their distances by the same factor."""
    program = [tokens.Increment("a"), tokens.Decrement("b"), tokens.Increment("c")]
    meta = memoptix.get_metainfo_from_routine(program)

    constraints = [
        memoptix.LinkedConstraint(from_="a", to_="b", length=3, factor="scale1"),
        memoptix.LinkedConstraint(from_="b", to_="c", length=2, factor="scale1"),
    ]
    resolver = memoptix.build_memory_resolver(constraints, meta)
    indexes = resolver.resolve().model.get_vars_by_owners(meta.owners)

    factor = (indexes["b"] - indexes["a"]) // 3
    assert indexes["c"] == indexes["b"] + 2 * factor, "Both links should scale their length by the same factor"


def test_link_nonexistent_owner() -> None:
    """Optional: Test linking behavior when an owner does not exist in the metadata."""
    program = [tokens.Increment("a")]
    meta = memoptix.get_metainfo_from_routine(program)
    constraints = [memoptix.LinkedConstraint(from_="a", to_="z", length=10, factor=None)]
    with pytest.raises(memoptix.ReferencingUnknownOwnerError):
        resolver = memoptix.build_memory_resolver(constraints, meta)

        resolver.resolve()
