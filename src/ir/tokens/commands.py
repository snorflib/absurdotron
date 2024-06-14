from __future__ import annotations

import typing

import attrs

from .base import BFToken


@attrs.frozen
class Command(BFToken):
    value: typing.ClassVar[str | None]


C = typing.TypeVar("C", bound=type[Command])


def command(value: str) -> typing.Callable[[C], C]:
    @typing.dataclass_transform()
    def wrapper(class_: C) -> C:
        class_.value = value
        return attrs.frozen(class_)

    return wrapper


@command("-")
class Decrement(Command):
    """
    Token for decrementing the current memory cell in BrainFuck.

    It decreases the value at the current position by 1. Represented by '-' in BrainFuck.
    """


@command("+")
class Increment(Command):
    """
    Token for incrementing the current memory cell in BrainFuck.

    It increases the value at the current position by 1. Represented by '+' in BrainFuck.
    """


@command(".")
class Display(Command):
    """
    Token for outputting the value of the current memory cell in BrainFuck.

    Outputs the ASCII character of the current cell's value. Represented by '.' in BrainFuck.
    """


@command(",")
class Input(Command):
    """
    Token for input in BrainFuck.

    Accepts a single ASCII character as input and stores it in the current cell. Represented by ',' in BrainFuck.
    """


@command("[")
class EnterLoop(Command):
    """
    Token marking the start of a loop in BrainFuck.

    Loop continues while the current cell's value is non-zero. Represented by '[' in BrainFuck.
    """


@command("]")
class ExitLoop(Command):
    """
    Token marking the end of a loop in BrainFuck.

    Loop ends or returns to the start (EnterLoop) if the current cell's
    value is non-zero. Represented by ']' in BrainFuck.
    The owner is always None, as it's a loop must be balanced, thus it will
    be mapped back to the `entering` owner later.
    """

    owner: None = attrs.field(init=False, repr=False, default=None)


@command("[-]")
class Clear(Command):
    """
    Token representing a clear command in BrainFuck.

    Sets the value of the current cell to zero. Represented by '[-]' as syntactic sugar in BrainFuck.
    """
