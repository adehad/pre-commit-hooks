"""About."""

# SPDX-FileCopyrightText: 2022-present adehad <26027314+adehad@users.noreply.github.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later
from __future__ import annotations

try:
    import importlib.metadata

    __version__ = importlib.metadata.version("pre_commit_hooks")
except Exception:
    __version__ = "unknown"
