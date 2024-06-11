import bidict
import pytest

from src.ir import exceptions, tokens, tools

from .utils import MockEnterToken


def test_basic_jump_map() -> None:
    """Test a basic sequence with properly nested loops."""
    sequence = [MockEnterToken(), tokens.ExitLoop()]
    jump_map, token_map = tools.build_jump_map(sequence)
    assert jump_map == bidict.bidict({0: 1})
    assert len(token_map) == 2
    assert isinstance(token_map[0], MockEnterToken)
    assert isinstance(token_map[1], tokens.ExitLoop)


def test_nested_loops() -> None:
    """Test a sequence with nested loops."""
    sequence = [MockEnterToken(), MockEnterToken(), tokens.ExitLoop(), tokens.ExitLoop()]
    jump_map, token_map = tools.build_jump_map(sequence)
    assert jump_map == bidict.bidict({0: 3, 1: 2})
    assert len(token_map) == 4


def test_unopened_loop_error() -> None:
    """Test handling of an exit loop without a corresponding enter loop."""
    sequence = [tokens.ExitLoop()]
    with pytest.raises(exceptions.NotOpenedLoopError):
        tools.build_jump_map(sequence)


def test_unclosed_loop_error() -> None:
    """Test handling of an enter loop without a corresponding exit loop."""
    sequence = [MockEnterToken()]
    with pytest.raises(exceptions.NotClosedLoopError):
        tools.build_jump_map(sequence)


def test_auto_matching_basic() -> None:
    """Test basic auto-matching functionality."""
    enter_loop = MockEnterToken()
    exit_loop = tokens.ExitLoop()

    with tools.AutoMatchEnterExitLoop() as gen:
        gen(enter_loop)
        matched = gen(exit_loop)

    assert matched == enter_loop


def test_unopened_matching() -> None:
    """Test handling of an tokens.ExitLoop without a preceding EnterLoop."""
    with pytest.raises(exceptions.NotOpenedLoopError):
        with tools.AutoMatchEnterExitLoop() as gen:
            gen(tokens.ExitLoop())


def test_unclosed_matching() -> None:
    """Test handling of remaining EnterLoop tokens at the end."""
    with pytest.raises(exceptions.NotClosedLoopError):
        with tools.AutoMatchEnterExitLoop() as gen:
            gen(MockEnterToken())
