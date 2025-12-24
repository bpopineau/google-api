"""Tests for the Unified Debug Console."""

import pytest


def test_console_module_exists():
    try:
        from mygoog_cli.console import start_console  # noqa: F401
    except ImportError:
        pytest.fail("mygoog_cli.console module or start_console function not found")
