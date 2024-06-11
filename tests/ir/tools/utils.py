import attrs

from src.ir import tokens


@attrs.frozen
class MockToken(tokens.BFToken):
    owner: None = None


@attrs.frozen
class MockEnterToken(tokens.EnterLoop):
    owner: None = None
