"""Utility functions."""

from __future__ import annotations

import abc
import argparse
import enum
import io
import json
import os
import pathlib
import typing
from collections.abc import Sequence
from typing import Any


class ExitCode(enum.IntEnum):
    """Exit Codes returned by the application."""

    OK = 0
    FAIL = 1


class ABCArgs(abc.ABC, argparse.Namespace):
    """ABC for Namespaces."""

    filenames: Sequence[str]


class ABCHook(abc.ABC):
    """Hook base."""

    def __init__(self) -> None:
        """Initialize the hook with required defaults."""
        parser = argparse.ArgumentParser()
        parser.add_argument("filenames", nargs="*")
        self._parser = parser
        self.setup_parser()

    @property
    def parser(self) -> argparse.ArgumentParser:
        """Return the parser."""
        return self._parser

    @abc.abstractmethod
    def setup_parser(self) -> None:
        """The custom implementation of any additional arguments."""

    @abc.abstractmethod
    def implementation(self, file_name: pathlib.Path, args: Any) -> ExitCode:
        """The custom implementation.

        Args:
            file_name (pathlib.Path): The file to be processed.
            args (ABCArgs): The arguments from self.parser.parse_args()

        Returns:
            ExitCode: The PASS/FAIL state.
        """

    def run(self, argv: Sequence[str] | None) -> ExitCode:
        """Run the custom implementation, feeding it all files."""
        args: ABCArgs = self.parser.parse_args(argv)  # type: ignore[assignment]
        return_value = int(ExitCode.OK)
        for filename in args.filenames:
            return_value |= int(
                self.implementation(file_name=pathlib.Path(filename), args=args)
            )
        return ExitCode(return_value)


def move_file_pointer_to_nth_line_before_end(
    file_pointer: io.BufferedReader, n: int = 1
) -> None:
    """Move the file pointer to the nth before last line of a file.

    Args:
        file_pointer (io.BufferedReader): File pointer opened in 'rb' mode.
        n (int): Lines before the last. 1 = End of the file. Defaults to 1.
    """
    num_newlines = 0
    try:
        file_pointer.seek(-2, os.SEEK_END)
        while num_newlines < n:
            file_pointer.seek(-2, os.SEEK_CUR)
            if file_pointer.read(1) == b"\n":
                num_newlines += 1
    except OSError:
        file_pointer.seek(0)


def sanitize_rb_line(line: bytes) -> str:
    """Sanitize a line read in binary mode. Removing line endings.

    Args:
        line (bytes): The data in bytes

    Returns:
        str: The sanitized line.
    """
    return line.decode().rstrip()


def load_json_source(file_or_json_str: str) -> dict[str, Any]:
    """Load a potential JSON source.

    Args:
        file_or_json_str (str): path to JSON file, or stringified JSON.

    Returns:
        dict[str, Any]: Loaded JSON.
    """
    default: dict[str, Any] = {}
    file_source = pathlib.Path(file_or_json_str)
    if file_source.is_file():
        with file_source.open(encoding="utf-8") as fp:
            return typing.cast(dict[str, Any], json.load(fp))

    try:
        return json.loads(file_or_json_str)  # type: ignore[no-any-return]
    except Exception:
        print("Unsupported JSON source, no custom rules applied!")
        return default


class HashableDict(dict):  # type: ignore[type-arg]
    """Hashable dict but not immutable."""

    def __hash__(self) -> int:  # type: ignore[override]
        """Hash."""
        return hash((frozenset(self), frozenset(self.values())))
