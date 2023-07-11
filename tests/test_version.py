"""Simple test for version."""
from __future__ import annotations

import pre_commit_hooks


def test_version():
    """Test version is sensible."""
    assert len(pre_commit_hooks.__version__.split(".")) == 3
