# pre_commit_hooks
<!--
[![PyPI - Version](https://img.shields.io/pypi/v/pre_commit_hooks.svg)](https://pypi.org/project/pre_commit_hooks)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pre_commit_hooks.svg)](https://pypi.org/project/pre_commit_hooks)
 -->

-----

**Table of Contents**

- [pre_commit_hooks](#pre_commit_hooks)
  - [Usage](#installation)
  - [Local Installation](#local-installation)
  - [Development](#development)
  - [License](#license)

## Usage

### check-header-footer

Some example usages of this are to check for the License or Copyright header.
For the footer the use case presented in the example is for a specific doxygen tag,

Arguments:
- `--lines`: How many lines to search from the top of the file.
- `--footer-lines`: How many lines to search from the bottom of the file.
- `--header-config`: `<config_filename>:comma,separated,rules` to apply to the header check.
- `--footer-config`: `<config_filename>:comma,separated,rules` to apply to the footer check.

The config file is a json of `{rule: expected lines}`. The lines are separated using an array.
Internally we use a regex comparison to find the exact strings.

```json
// config.json Example
{
    "license": [
        "# SPDX-FileCopyrightText: 2022-present adehad <26027314+adehad@users.noreply.github.com>",
        "#",
        "# SPDX-License-Identifier: GPL-3.0-or-later"
    ],
    "c_license": [
        "/*",
        " * Copyright (c) 2023 COMPANY_NAME",
        " * All rights reserved",
        " */"
    ],
    "doxygen": [
        "/// @}"
    ]
}
```

With pre-commit we can specify the `types_or` for specific file types, and restrict
to a subset of files. Running header and footer checks at the same time.

```yaml
repos:
  - repo: https://github.com/adehad/pre-commit-hooks
    rev: main
    hooks:
      - id: check-header-footer
        files: ^Source/(?!Generated).*
        types_or: [c, c++]
        args:
          - --header-config=config.json:c_license
          - --footer-config=config.json:doxygen
```

or for verbosity the header and footer stages can be isolated, this can be used for
checking the header and footer separated (see below) or can be used to select different
rules for different languages.

```yaml
repos:
  - repo: https://github.com/adehad/pre-commit-hooks
    rev: main
    hooks:
      - id: check-header-footer
        name: Checking for License
        files: ^Source/(?!Generated).*
        types_or: [c, c++]
        args:
          - --header-config=config.json:c_license
  - repo: https://github.com/adehad/pre-commit-hooks
    rev: main
    hooks:
      - id: check-header-footer
        name: Checking for Doxygen file group
        files: ^Source/(?!Generated).*
        types_or: [c, c++]
        args:
          - --footer-config=config.json:doxygen
```

Future work:
1. Support a year parameter that can be used to apply fixes.


### arabic-presentation-form

Replace characters in Arabic Presentation form (A or B), and convert them into 'default' unicode characters.
One application is when using the 'Scheherazade New' font, and it does not support these characters.

Arguments:
- `--excluded-chars`: Regex of characters to exclude from being fixed.
- `--custom-rules`: Rules to update or override the tools inbuilt configuration. Format and example below:
  ```json
  "RuleName": {"rule": {"ReplacementCharacter(s)": "RegexOfApplicableCharacter(s)"}}
  "ʾalif": {"rule": {"\u0627": "(\ufe8d|\ufe8e)"}},
  ```

Example where we are extending the applicable file types and using a specific folder (all subfolders under `site/data`)

```yaml
repos:
  - repo: https://github.com/adehad/pre-commit-hooks
    rev: main
    hooks:
      - id: arabic-presentation-form
        entry: arabic-presentation-form
        language: python
        types_or: [text, json, markdown]
        args: [--excluded-chars, (ﷺ)]
        files: ^site/data/
```

## Local Installation

```console
pipx install git+https://github.com/adehad/pre-commit-hooks.git@main
```

## Development

```console
hatch shell
```

```console
hatch run lint
hatch run docs
hatch run cov
```


## License

`pre_commit_hooks` is distributed under the terms of the [GPL-3.0-or-later](https://spdx.org/licenses/GPL-3.0-or-later.html) license.
