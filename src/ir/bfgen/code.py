import io
import pathlib
import sys
import typing

import attrs
import pyperclip  # type: ignore

_DEFAULT_MAX_OUTPUT_SIZE: typing.Final[int] = 10_000


@attrs.frozen
class Code:
    max_output_size: int = attrs.field(default=_DEFAULT_MAX_OUTPUT_SIZE)
    source_code: io.StringIO = attrs.field(factory=io.StringIO)

    def add(self, code: str) -> None:
        self.source_code.write(code)

    def save(
        self,
        filepath: typing.Optional[pathlib.Path | str] = None,
        copy2clipboard: bool = False,
        display: bool = False,
    ) -> None:
        value: str = self.source_code.getvalue()

        if filepath:
            with open(filepath, "w") as file:
                file.write(value)

        if (len(value) > self.max_output_size) and (copy2clipboard or display):
            raise RuntimeError(
                "The code is too large to safely output it or store to a clipboard."
                "Please, provide a file path instead."
            )

        if copy2clipboard:
            pyperclip.copy(value)

        if display:
            sys.stdout.write(value)
            sys.stdout.flush()
