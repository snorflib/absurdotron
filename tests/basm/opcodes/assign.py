from src import basm
import pytest
from .utils import execute_opcodes_get_owner_values


def test_assign_not_short() -> None:
    _test_all_values()


@pytest.mark.skip(reason="Not currently implemented")
def test_assign_short() -> None:
    _test_all_values(True)



def _test_all_values(use_short: bool = False) -> None:
    for value in range(0, 256):
        a = basm.Unit()
        opcodes = [basm.Init(a), basm.Add(a, 2, a), basm.Assign(a, value, use_short=use_short)]

        memory = execute_opcodes_get_owner_values(opcodes)
        assert memory[a] == value

