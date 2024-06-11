import pytest

from src import ir

_OwnerPlaceholder = 0


def test_compiler_injection_initialization() -> None:
    token = ir.CompilerInjection(value="++", owner=_OwnerPlaceholder)
    assert token.value == "++"


def test_compiler_injection_default_exit() -> None:
    token = ir.CodeInjection(value="+-", owner=_OwnerPlaceholder)
    assert token.end_owner == token.owner


def test_comment_injection_attributes() -> None:
    comment = ir.CommentInjection(value="This is a comment")
    assert comment.owner is None
    assert comment.end_owner is None


def test_check_injection_safety_valid() -> None:
    try:
        ir.CommentInjection(value="This is safe")
    except Exception as exc:
        pytest.fail(f"Unexpected `{exc}` error for safe string")


def test_check_injection_safety_invalid() -> None:
    with pytest.raises(ir.CodeSemanticsViolationError):
        ir.CommentInjection(value="++[>.<]")


def test_check_injection_safety_error_details() -> None:
    with pytest.raises(ir.CodeSemanticsViolationError) as exc_info:
        ir.CommentInjection(value="++[>.<]")
    assert "++[>.<]" in str(exc_info.value)
