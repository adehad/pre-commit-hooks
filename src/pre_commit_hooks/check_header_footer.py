"""Check for lines found in the first or last lines of a file."""
from __future__ import annotations

import functools
import io
import json
import pathlib
import re
from typing import Any, Dict, NamedTuple, Sequence

from .util import (
    ABCArgs,
    ABCHook,
    ExitCode,
    move_file_pointer_to_nth_line_before_end,
    sanitize_rb_line,
)

RulesDict = Dict[str, re.Pattern[Any]]


def check_rules_in_file(
    f: io.BufferedReader, max_lines: int, rules: RulesDict
) -> ExitCode:
    """Check the text for rules.

    Args:
        f (io.BufferedReader): File pointer to file to check.
        max_lines (int): Maximum lines to search for rule.
        rules (RulesDict): The rules to check form.

    Returns:
        ExitCode: The PASS/FAIL state.
    """
    exit_code = ExitCode.OK
    a = []
    for idx, line in enumerate(f):
        if idx > max_lines:
            break
        a.append(sanitize_rb_line(line))

    search_region = "\n".join(a)
    for name, rule in rules.items():
        match = rule.search(search_region)
        if not match:
            print(f"Failed on check '{name}' for file {f.name}")
            exit_code = ExitCode.FAIL

    return exit_code


class RuleConfig(NamedTuple):
    """Holder for User Input rules."""

    file_path: pathlib.Path
    enabled_rules: list[str]

    @classmethod
    def parse_arg(cls, arg_input: str) -> RuleConfig:
        """Parse an user input into a Rules object."""
        file_path, rules = arg_input.split(":")
        return cls(file_path=pathlib.Path(file_path), enabled_rules=rules.split(","))

    @property
    def rules(self) -> RulesDict:
        """Return the compiled rules."""
        with self.file_path.open() as fp:
            all_rules: dict[str, str] = json.load(fp)
        return {
            rule: re.compile(re.escape("\n".join(all_rules[rule])))
            for rule in self.enabled_rules
        }


@functools.lru_cache(maxsize=2)
def get_rules(config: str) -> RulesDict:
    """Return the rules from a given config string.

    Args:
        config (str): The config string.

    Returns:
        RulesDict: The compiles rules.
    """
    rules: RulesDict = {}
    if config:
        rules = RuleConfig.parse_arg(config).rules
    return rules


class HeaderFooterArgs(ABCArgs):
    """Args."""

    lines: int
    footer_lines: int
    header_config: str
    footer_config: str


class HeaderFooterChecker(ABCHook):
    """Checker for Header and Footer."""

    def setup_parser(self) -> None:
        """Custom arguments."""
        self.parser.add_argument(
            "--lines",
            type=int,
            default=60,
            help="How many lines to search from the top of the file.",
        )
        self.parser.add_argument(
            "--footer-lines",
            type=int,
            default=5,
            help="How many lines to search from the bottom of the file.",
        )
        self.parser.add_argument(
            "--header-config",
            type=str,
            default="",
            metavar="<filename>:comma,separated,rules",
            help="The configuration for checking the header.",
        )
        self.parser.add_argument(
            "--footer-config",
            type=str,
            default="",
            metavar="<filename>:comma,separated,rules",
            help="The configuration for checking the footer.",
        )

    def implementation(
        self,
        file_name: pathlib.Path,
        args: HeaderFooterArgs,
    ) -> ExitCode:
        """Check Implementation."""
        exit_code = int(ExitCode.OK)
        h_rules = get_rules(args.header_config)
        f_rules = get_rules(args.footer_config)
        with file_name.open("rb") as f:
            if h_rules:
                n_lines = args.lines
                exit_code |= check_rules_in_file(f, max_lines=n_lines, rules=h_rules)
            if f_rules:
                n_lines = args.footer_lines
                move_file_pointer_to_nth_line_before_end(f, n=n_lines)
                exit_code |= check_rules_in_file(f, max_lines=n_lines, rules=f_rules)
        return ExitCode(exit_code)


def main(argv: Sequence[str] | None = None) -> int:
    """Main entrypoint."""
    argparser = HeaderFooterChecker()
    return argparser.run(argv=argv)


if __name__ == "__main__":
    raise SystemExit(main())
