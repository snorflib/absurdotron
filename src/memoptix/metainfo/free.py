import attrs

from src.ir import tokens


@attrs.frozen
class Free(tokens.BFToken):
    ...
