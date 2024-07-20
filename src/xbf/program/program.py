from __future__ import annotations

import attrs

from src.ir import tokens
from src.memoptix import constraints


@attrs.frozen
class Program:
    constr: list[constraints.BaseConstraint] = attrs.field(factory=list)
    routine: list[tokens.BFToken] = attrs.field(factory=list)

    def update(self, program: Program) -> None:
        self.constr.extend(program.constr)
        self.routine.extend(program.routine)
