"""Arabic Presentation Form."""

from __future__ import annotations

import functools
import pathlib
import re
import sys
from collections.abc import Sequence
from typing import Any

from ..util import (
    ABCArgs,
    ABCHook,
    ExitCode,
    HashableDict,
    load_json_source,
)
from . import char_map

sys.stdout.reconfigure(  # type: ignore[attr-defined]
    encoding="utf-8"  # For Windows: we want to be sure to use UTF-8
)
RulesDict = dict[re.Pattern[Any], str]


def apply_rules_to_lines(
    line: str,
    rules: RulesDict,
    exclude: re.Pattern[str],
    file_name: pathlib.Path | str,
    line_no: str | int,
) -> tuple[ExitCode, str]:
    """Check the text for rules.

    Args:
        line (str): Line to check the rules.
        rules (RulesDict): The rules to check form.
        exclude (re.Pattern): characters to exclude from check.
        file_name (str): the name of the file being checked.
        line_no (int): The line number being checked.

    Returns:
        (ExitCode, str): (The PASS/FAIL state, The new line).
    """
    exit_code = ExitCode.OK
    new_line = exclude.sub(" ", line)  # Replace with space to not affect col numbers

    if not char_map.is_contains_non_general_form(max(new_line)):
        return exit_code, line

    new_chars: list[str] = []
    exit_code = ExitCode.FAIL

    for col_no, c in enumerate(line, start=1):
        new_c = apply_rule(rules=HashableDict(rules), character=c)
        new_c_as_unicode_hex = [f"\\u{ord(c):04x}" for c in new_c]
        fix_char_loc = (
            f"{file_name}:{line_no}:{col_no} [{new_c} ({new_c_as_unicode_hex})]"
        )
        if c != new_c:
            output_str = f"[Fixed] {fix_char_loc}"
        elif char_map.is_contains_non_general_form(new_c):
            output_str = f"[Not Fixed] {fix_char_loc}"
        else:
            output_str = ""

        if output_str:
            print(output_str)
            output_str = ""

        new_chars.append(new_c)

    new_line = "".join(new_chars)

    return exit_code, new_line


def get_rules(custom_rules: char_map.CHAR_MAP_TYPE) -> RulesDict:
    """Return the rules from a given config string.

    Args:
        custom_rules (str): Any additional rules to apply.

    Returns:
        RulesDict: The compiles rules.

    """
    regex_rules = {}
    complete_rules: char_map.CHAR_MAP_TYPE = {}
    complete_rules.update(char_map.CHAR_MAP)
    complete_rules.update(custom_rules)
    for _rule_name, char_mapping_rule in complete_rules.items():
        for expected_out, expected_regex in char_mapping_rule["rule"].items():
            regex_rules.update({re.compile(expected_regex): expected_out})
    return regex_rules


@functools.lru_cache
def apply_rule(rules: RulesDict, character: str) -> str:
    """Apply the rule from the list of rules to the character.

    Args:
        rules (RulesDict): rules to apply for the character.
        character (str): The letter/character to check against.

    Returns:
        str: The character after applying any rules.
    """
    new_char = character
    for reg_pattern, replace_char in rules.items():
        if reg_pattern.match(character):
            new_char = reg_pattern.sub(replace_char, character)
            break
    return new_char


class ArabicPresentationFormArgs(ABCArgs):
    """Args."""

    excluded_chars: str
    custom_rules: char_map.CHAR_MAP_TYPE


class ArabicPresentationFormChecker(ABCHook):
    """Checker for Header and Footer."""

    def setup_parser(self) -> None:
        """Custom arguments."""
        self.parser.add_argument(
            "--excluded-chars",
            type=str,
            default="",
            metavar="exclude-char-regex",
            help="Regex for characters to exclude. e.g. (ﷺ)",
        )
        self.parser.add_argument(
            "--custom-rules",
            type=load_json_source,
            default=dict(),
            metavar="Path-OR-JSON-String",
            help=(
                '"RuleName": {"rule": {"ReplacementCharacter(s)": "RegexOfApplicableCharacter(s)"}}'  # noqa: E501
                '. e.g. "ʾalif": {"rule": {"\u0627": "(\ufe8d|\ufe8e)"}},'  # noqa: RUF001
                + ". To exclude a unicode character, overwrite its default entry."
            ),
        )

    def implementation(
        self,
        file_name: pathlib.Path,
        args: ArabicPresentationFormArgs,
    ) -> ExitCode:
        """Check Implementation."""
        exit_code = int(ExitCode.OK)
        exclude_regex = re.compile(args.excluded_chars)

        new_file_lines = []
        with file_name.open("r", encoding="utf-8") as f:
            for line_no, line in enumerate(iter(f.readlines()), start=1):
                intermediate_exit_code, new_line = apply_rules_to_lines(
                    line=line,
                    line_no=line_no,
                    file_name=file_name,
                    rules=get_rules(args.custom_rules),
                    exclude=exclude_regex,
                )
                exit_code |= intermediate_exit_code

                if char_map.is_contains_non_general_form(
                    max(exclude_regex.sub("", new_line) or " ")
                ):
                    print(f"Incomplete Fixes Applied: {file_name}:{line_no}")

                new_file_lines.append(new_line)

        with file_name.open("w", encoding="utf-8") as f:
            f.writelines(new_file_lines)
        return ExitCode(exit_code)


def main(argv: Sequence[str] | None = None) -> int:
    """Main entrypoint."""
    argparser = ArabicPresentationFormChecker()
    return argparser.run(argv=argv)
