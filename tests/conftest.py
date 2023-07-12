"""Pytest configuration and other utilities."""
from __future__ import annotations

import pathlib
import urllib.request
from functools import lru_cache
from typing import NamedTuple

_CURRENT_DIR = pathlib.Path(__file__).parent


class FileDetail(NamedTuple):
    url: str
    path: pathlib.Path


TEST_FILES: dict[str, FileDetail] = {
    "unity": FileDetail(
        "https://raw.githubusercontent.com/ThrowTheSwitch/Unity/1b9199ee380e203603b6649df9510db9cab147d9/src/unity.c",
        (_CURRENT_DIR / "samples/unity.c").resolve(),
    ),
}


def fetch_from_url(filepath: pathlib.Path, url: str):
    if filepath.exists():
        return
    urllib.request.urlretrieve(url, filepath)


@lru_cache
def ensure_all_files_needed_present():
    for f in TEST_FILES.values():
        fetch_from_url(f.path, f.url)


ensure_all_files_needed_present()
