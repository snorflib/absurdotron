from src import memoptix
from src.ir import tokens


def test_unit_segregation_intersecting_lifecycles() -> None:
    """Test that owners with intersecting lifecycles are not assigned the same memory address."""
    program = [tokens.Increment("a"), tokens.Increment("b"), tokens.Decrement("a"), tokens.Increment("b")]
    meta = memoptix.get_metainfo_from_routine(program)

    constraints = [memoptix.UnitConstraint("a"), memoptix.UnitConstraint("b")]
    resolver = memoptix.build_memory_resolver(constraints, meta)
    resolver.resolve()

    indexes = resolver.model.get_vars_by_owners(meta.owners)
    assert indexes["a"] != indexes["b"], "Owners 'a' and 'b' with intersecting lifecycles should not share an address"


def test_unit_segregation_non_intersecting_lifecycles() -> None:
    """Verify that owners without intersecting lifecycles can potentially share the same memory address."""
    program = [
        tokens.Increment("a"),
        tokens.Decrement("a"),
        memoptix.Free("a"),
        tokens.Increment("b"),
        tokens.Increment("b"),
        memoptix.Free(
            "b",
        ),
    ]
    meta = memoptix.get_metainfo_from_routine(program)

    constraints = [memoptix.UnitConstraint("a"), memoptix.UnitConstraint("b")]
    resolver = memoptix.build_memory_resolver(constraints, meta)
    resolver.resolve()

    indexes = resolver.model.get_vars_by_owners(meta.owners)
    assert indexes["a"] == indexes["b"], "Owners 'a' and 'b' without intersecting lifecycles could share an address"


def test_unit_segregation_with_loops() -> None:
    """Test proper handling of lifecycles involving loops."""
    program = [
        tokens.Increment("1"),
        tokens.Decrement("1"),
        tokens.EnterLoop("3"),
        tokens.Increment("2"),
        tokens.EnterLoop("1"),
        tokens.Increment("2"),
        memoptix.Free("2"),
        tokens.ExitLoop(),
        memoptix.Free("1"),
        tokens.Decrement("4"),
        tokens.ExitLoop(),
        memoptix.Free("3"),
        tokens.Decrement("4"),
        memoptix.Free("4"),
    ]
    meta = memoptix.get_metainfo_from_routine(program)

    constraints = [
        memoptix.UnitConstraint("1"),
        memoptix.UnitConstraint("2"),
        memoptix.UnitConstraint("3"),
        memoptix.UnitConstraint("4"),
    ]
    resolver = memoptix.build_memory_resolver(constraints, meta)
    resolver.resolve()

    indexes = resolver.model.get_vars_by_owners(meta.owners)
    # Ensure no overlap for adjusted bounds that intersect
    assert (
        indexes["1"] != indexes["3"]
    ), "Owners '1' and '3' should not share an address due to overlapping lifecycles within loops"
    assert (
        indexes["2"] != indexes["4"]
    ), "Owners '2' and '4' should not share an address due to overlapping lifecycles within loops"
