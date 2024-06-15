import pytest

from src import ir, memoptix
from src.memoptix import exceptions


def test_indexed_owner_basic_assignment() -> None:
    """Ensure IndexedOwner correctly assigns specified memory indexes."""
    program = [ir.Decrement("0"), ir.Increment("1"), ir.Decrement("0")]
    meta = memoptix.get_metainfo_from_routine(program)

    constraints = [memoptix.IndexedOwnerConstraint("0", 10), memoptix.IndexedOwnerConstraint("1", 20)]
    resolver = memoptix.build_memory_resolver(constraints, meta)

    resolver.resolve()
    indexes = resolver.model.get_vars_by_owners(meta.owners)
    assert indexes["0"] == 10, "Owner '0' should be indexed at 10"
    assert indexes["1"] == 20, "Owner '1' should be indexed at 20"


def test_indexed_owner_conflicting_indexes() -> None:
    """Test that conflicting IndexedOwner constraints raise a MemoryAllocationFailed exception."""
    program = [ir.Decrement("0"), ir.Increment("1"), ir.Decrement("0")]
    meta = memoptix.get_metainfo_from_routine(program)

    constraints = [memoptix.IndexedOwnerConstraint("0", 10), memoptix.IndexedOwnerConstraint("0", 15)]
    resolver = memoptix.build_memory_resolver(constraints, meta)

    with pytest.raises(exceptions.MemoryAllocationFailedError):
        resolver.resolve()


def test_indexed_owner_nonexistent_owner() -> None:
    """Optional: Test behavior when an index is assigned to a nonexistent owner."""
    program = [ir.Decrement("0"), ir.Increment("1"), ir.Decrement("0")]
    meta = memoptix.get_metainfo_from_routine(program)

    constraints = [memoptix.IndexedOwnerConstraint("2", 30)]

    with pytest.raises(exceptions.ReferencingUnknownOwnerError):
        resolver = memoptix.build_memory_resolver(constraints, meta)
        resolver.resolve()
