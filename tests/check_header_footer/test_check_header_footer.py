"""Test check_header_footer."""

from __future__ import annotations

import json
import pathlib
import typing
from unittest import mock

import pytest

from pre_commit_hooks import check_header_footer as _hook
from pre_commit_hooks.util import ExitCode

from ..conftest import TEST_FILES

PATCH_BASE = f"{_hook.__name__}"

DUMMY_CONFIG = {
    "license": [
        "# SPDX-FileCopyrightText: 2022-present adehad <26027314+adehad@users.noreply.github.com>",  # noqa: E501
        "#",
        "# SPDX-License-Identifier: GPL-3.0-or-later",
    ],
    "c_license": [
        "/* =========================================================================",
        "    Unity Project - A Test Framework for C",
        "    Copyright (c) 2007-21 Mike Karlesky, Mark VanderVoord, Greg Williams",
        "    [Released under MIT License. Please refer to license.txt for details]",
        "============================================================================ */",  # noqa: E501
    ],
    "c_footer": [
        "#endif /* UNITY_USE_COMMAND_LINE_ARGS */",
        "/*-----------------------------------------------*/",
    ],
    "doxygen": ["/// @}"],
}


def get_dummy_rules() -> _hook.RulesDict:
    with mock.patch(
        f"{PATCH_BASE}.pathlib.Path.open",
        mock.mock_open(read_data=json.dumps(DUMMY_CONFIG)),
    ):
        rules = _hook.get_rules(f"dummy_rule.config:{','.join(DUMMY_CONFIG.keys())}")
    return rules


def test_rule_config():
    rules = get_dummy_rules()
    assert set(rules.keys()) == set(DUMMY_CONFIG.keys())


def generic_test(
    test_file: pathlib.Path, header_checks: list[str], footer_checks: list[str]
) -> ExitCode:
    """Helper function to coordinate the running of the test.

    Args:
        test_file (pathlib.Path): test file.
        header_checks (list[str]): selected checks to run for the header.
        footer_checks (list[str]): selected checks to run for the footer.

    Returns:
        ExitCode: the result of the `.implementation()` call.
    """
    rules = get_dummy_rules()
    h_rules = {k: v for k, v in rules.items() if k in header_checks}
    f_rules = {k: v for k, v in rules.items() if k in footer_checks}
    with mock.patch(
        f"{PATCH_BASE}.{_hook.get_rules.__name__}",  # type: ignore[attr-defined]
        side_effect=[h_rules, f_rules],
    ):
        parsed_args = _hook.HeaderFooterArgs(
            filenames=[test_file],
            lines=10,
            footer_lines=15,
            header_config="",
            footer_config="",
        )
        argparser = _hook.HeaderFooterChecker()
        return_code = argparser.implementation(test_file, parsed_args)
    return return_code


@pytest.mark.parametrize(
    ("test_file", "check_to_use", "expected"),
    [
        (TEST_FILES["unity"].path, ["c_license"], ExitCode.OK),
        (TEST_FILES["unity"].path, ["doxygen"], ExitCode.FAIL),
    ],
    ids=["pass", "fail"],
)
def test_header(test_file: pathlib.Path, check_to_use: list[str], expected: ExitCode):
    # GIVEN: a test file
    #  and the rules to test with
    # WHEN: we run against the test file
    return_code = generic_test(test_file, header_checks=check_to_use, footer_checks=[])
    # THEN: We get the expected exit code
    assert return_code == expected


@pytest.mark.parametrize(
    ("test_file", "check_to_use", "expected"),
    [
        (TEST_FILES["unity"].path, ["c_footer"], ExitCode.OK),
        (TEST_FILES["unity"].path, ["doxygen"], ExitCode.FAIL),
    ],
    ids=["pass", "fail"],
)
def test_footer(test_file: pathlib.Path, check_to_use: list[str], expected: ExitCode):
    # GIVEN: a test file
    #  and the rules to test with
    # WHEN: we run against the test file
    return_code = generic_test(test_file, header_checks=[], footer_checks=check_to_use)
    # THEN: We get the expected exit code
    assert return_code == expected


def test_default_args():
    # GIVEN: the result of the argument parser
    default_args = _hook.HeaderFooterChecker().parser.parse_args([])
    # WHEN: we compare the argument parsed fields VS the typehints
    # THEN: they are equal
    assert set(default_args.__dict__.keys()) == set(
        typing.get_type_hints(_hook.HeaderFooterArgs).keys()
    )


def test_both_header_and_footer_runs():
    with mock.patch(
        f"{PATCH_BASE}.{_hook.check_rules_in_file.__name__}",
        side_effect=_hook.check_rules_in_file,
    ) as patch_check_rules:
        # GIVEN: both 1 header and 1 footer rule
        # WHEN: we run the checks
        return_code = generic_test(
            TEST_FILES["unity"].path,
            header_checks=["c_license"],
            footer_checks=["c_footer"],
        )
        # THEN: the rule checking function is called twice
        assert patch_check_rules.call_count == 2
    assert return_code == ExitCode.OK
