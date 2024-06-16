import attrs

from src.ir import tokens
from src.memoptix import constraints


@attrs.frozen
class Program:
    constr: list[constraints.BaseConstraint] = attrs.field(factory=list)
    routine: list[tokens.BFToken] = attrs.field(factory=list)
