import io

from src.bfrun import simple


def test_simple_data_change() -> None:
    exc = simple.Executor("+++>>++<--")
    exc()

    assert exc.memory._array[:3].tolist() == [3, 254, 2]


def test_simple_data_input() -> None:
    input = io.StringIO("abc")
    exc = simple.Executor(",,>,", input=input)
    exc()

    assert exc.memory._array[:2].tolist() == [ord("b"), ord("c")]


def test_hello() -> None:
    output = io.StringIO()

    exc = simple.Executor("+[----->+++<]>+.---.+++++++..+++.[--->+<]>----.", output=output)
    exc()

    assert exc.output
    assert exc.output.getvalue() == "hello!"


def test_non_balanced_loops() -> None:
    exc = simple.Executor(">+<[>-]>[->>+<]<<")
    exc()

    assert exc.memory._array[:4].tolist() == [0, 0, 0, 1]
