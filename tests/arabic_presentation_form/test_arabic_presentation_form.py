"""Test check_header_footer."""

from __future__ import annotations

import json
import pathlib
import tempfile

import pytest

from pre_commit_hooks import arabic_presentation_form as _hook
from pre_commit_hooks.util import ExitCode, load_json_source

PATCH_BASE = f"{_hook.__name__}"

CUSTOM_RULES = {}

EXAMPLE_OF_EXPECTED = {}


def generic_test(
    test_file: pathlib.Path,
    custom_rules: _hook.char_map.CHAR_MAP_TYPE = CUSTOM_RULES,
    excluded_chars="",
) -> ExitCode:
    """Helper function to coordinate the running of the test.

    Args:
        test_file (pathlib.Path): test file.

    Returns:
        ExitCode: the result of the `.implementation()` call.
    """
    parsed_args = _hook.ArabicPresentationFormArgs(
        filenames=[test_file],
        custom_rules=load_json_source(json.dumps(custom_rules)),
        excluded_chars=excluded_chars,
    )
    argparser = _hook.ArabicPresentationFormChecker()
    return_code = argparser.implementation(test_file, parsed_args)
    return return_code


@pytest.mark.parametrize(
    ("raw_arabic", "parsed_arabic", "custom_rules", "excluded_chars", "expected"),
    [
        ("ﻃَﺎﻟَﻤَﺎ", "طَالَمَا", {}, "", ExitCode.FAIL),
        ("ﻃَﺎﻟَﻤَﺎ", "ﻃَالَمَا", {"ṭāʾ": {"rule": {"\u0637": "(NOPE)"}}}, "", ExitCode.FAIL),
        ("بَابَ", "بَابَ", {}, "", ExitCode.OK),
        ("ﷺ", "ﷺ", {}, "(ﷺ)", ExitCode.OK),
    ],
    ids=["fix", "unfixable (rule override)", "no fix required", "excluded char"],
)
def test_fixer(
    raw_arabic: str,
    parsed_arabic: str,
    custom_rules: _hook.char_map.CHAR_MAP_TYPE,
    excluded_chars: str,
    expected: ExitCode,
):
    with tempfile.NamedTemporaryFile(mode="a+", encoding="utf-8", delete=False) as file:
        try:
            # GIVEN: a test file
            file.write(raw_arabic)
            file.seek(0)
            #  and the rules to test with
            # WHEN: we run against the test file
            return_code = generic_test(
                pathlib.Path(file.name),
                custom_rules=custom_rules,
                excluded_chars=excluded_chars,
            )
            # file.close()
            assert parsed_arabic in file.read()
        finally:
            file.__del__()
    # THEN: We get the expected exit code
    assert return_code == expected
