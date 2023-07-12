"""Test the utilities."""
from __future__ import annotations

import pathlib
import tempfile
from unittest import mock

import pytest

from pre_commit_hooks import util
from pre_commit_hooks.util import ExitCode

from . import conftest


def test_fetch_from_url():
    #  GIVEN: we think we don't have any files
    conftest.ensure_all_files_needed_present.cache_clear()
    with mock.patch(
        f"{conftest.__name__}.{conftest.fetch_from_url.__name__}"
    ) as mock_fetch_from_url:
        # WHEN: we try and call the file fetcher multiple times
        conftest.ensure_all_files_needed_present()
        conftest.ensure_all_files_needed_present()
    # THEN: we only get one call
    assert mock_fetch_from_url.call_count == 1


def test_abc_hook():
    # GIVEN: an input path and a example hook
    dummy_file = pathlib.Path("test.file")
    expected_exit = ExitCode.OK
    setuper_parser_mock = mock.MagicMock()
    implementation_mock = mock.MagicMock()

    class DemoHook(util.ABCHook):
        def setup_parser(self) -> None:
            setuper_parser_mock()

        def implementation(self, file_name, args) -> ExitCode:
            implementation_mock()
            assert isinstance(file_name, pathlib.Path)
            assert str(dummy_file) in args.filenames
            return expected_exit

    h = DemoHook()
    # WHEN: we run the hook instance with a input file
    assert expected_exit == h.run([str(dummy_file)])
    # THEN: we confirm our abstract methods were called
    assert setuper_parser_mock.call_count == 1
    assert implementation_mock.call_count == 1


@pytest.mark.parametrize(
    "linesep",
    [("\r\n"), ("\n")],
    ids=["\r\n", "\n"],
)
def test_move_file_pointer_to_end_of_file(linesep: str):
    # GIVEN: a list of lines, written to a file
    #  & the number of lines to read from the bottom of the file
    lines_to_write = list(str(i) for i in range(20))
    n_readback = 3
    with tempfile.TemporaryDirectory() as tmp_folder:
        tmp_file = pathlib.Path(tmp_folder) / "tmp_files.txt"
        with tmp_file.open("w") as fp:
            for line in lines_to_write:
                fp.write(f"{line}{linesep}")
        # WHEN: we re-open the file, set the file pointer then read the remaining lines
        with tmp_file.open("rb") as fp:
            util.move_file_pointer_to_nth_line_before_end(fp, n=n_readback)
            received_lines = fp.readlines()
    # THEN: after we use the sanitization method we read the expected lines
    decoded_lines = [util.sanitize_rb_line(line) for line in received_lines]
    assert decoded_lines == lines_to_write[-n_readback:]
