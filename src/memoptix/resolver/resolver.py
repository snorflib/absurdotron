import attrs

from src.ir import types
from src.memoptix import constraints, metainfo


@attrs.define(hash=False)
class Unit:
    start: int
    end: int
    owner: types.Owner
    width: int = 1

    def __hash__(self) -> int:
        return hash(self.owner)


@attrs.frozen
class MemoryResolver:
    _units: list[Unit] = attrs.field(factory=list)

    def add_unit(self, unit: Unit) -> None:
        self._units.append(unit)

    def resolve(self) -> dict[types.Owner, int]:
        sorted_units = sorted(self._units, key=lambda unit: unit.start)
        unit_to_index: dict[int, Unit] = {}
        indices = {}

        for new_unit in sorted_units:
            for idx in unit_to_index:
                for idx_offset in range(idx, idx + new_unit.width):
                    if unit_to_index[idx_offset].end >= new_unit.start:
                        break

                else:
                    for idx_offset in range(idx, idx + new_unit.width):
                        unit_to_index[idx_offset] = new_unit
                    indices[new_unit.owner] = idx
                    break
            else:
                idx = len(unit_to_index)
                for idx_offset in range(idx, idx + new_unit.width):
                    unit_to_index[idx_offset] = new_unit
                indices[new_unit.owner] = idx

        return indices


def build_memory_resolver(
    constrs: list[constraints.BaseConstraint],
    metainfo: metainfo.RoutineMetaInfo,
) -> MemoryResolver:
    owner_to_constraints = {constr.owner: constr for constr in constrs}

    resolver = MemoryResolver()

    for owner in metainfo.owners:
        start, end = metainfo.scopes[owner].adjusted_bounds
        constr = owner_to_constraints.get(owner, constraints.UnitConstraint(owner))
        match constr:
            case constraints.UnitConstraint():
                resolver.add_unit(Unit(start, end, owner))
            case constraints.ArrayConstraint():
                resolver.add_unit(Unit(start, end, owner, width=constr.length))

    return resolver
