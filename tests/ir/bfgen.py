import io

from src.ir import bfgen, tokens


def test_simple_increment_decrement() -> None:
    """Test generating code with simple increment and decrement operations."""
    program = [tokens.Increment("byte1"), tokens.Decrement("byte2")]

    code = bfgen.Generator()(
        program,
        {"byte1": 0, "byte2": 1},
    )

    expected_code = "+>-"
    assert code.source_code.getvalue() == expected_code, f"Expected {expected_code}, got {code.source_code.getvalue()}"


def test_pointer_movement() -> None:
    """Test that the pointer moves correctly through the memory."""
    program = [tokens.Increment("byte1"), tokens.Increment("byte3")]

    code = bfgen.Generator()(
        program,
        {"byte1": 0, "byte2": 1, "byte3": 2},
    )

    expected_code = "+>>+"
    assert code.source_code.getvalue() == expected_code, f"Expected {expected_code}, got {code.source_code.getvalue()}"


def test_code_with_loops() -> None:
    """Test that the pointer moves correctly through the memory."""
    program = [
        tokens.Increment("byte1"),
        tokens.EnterLoop("byte2"),
        tokens.Increment("byte3"),
        tokens.Decrement("byte2"),
        tokens.ExitLoop(),
        tokens.Display("byte3"),
    ]

    code = bfgen.Generator()(
        program,
        {"byte1": 0, "byte2": 1, "byte3": 2},
    )

    expected_code = "+>[>+<-]>."
    assert code.source_code.getvalue() == expected_code, f"Expected {expected_code}, got {code.source_code.getvalue()}"


def test_code_saving_and_output() -> None:
    """Test saving the generated code to a file and copying to clipboard functionality."""
    program = [tokens.Increment("byte1")]
    stdout_capture = io.StringIO()

    bfgen.Generator(
        code=bfgen.Code(source_code=stdout_capture),
    )(
        program,
        {"byte1": 0},
    )

    assert "+" == stdout_capture.getvalue(), "The displayed code does not match the expected Brainfuck code."
