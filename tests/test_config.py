"""Tests for the configuration management system."""

import pytest

from mygooglib.core.config import AppConfig, Config


@pytest.fixture
def clean_config(tmp_path, monkeypatch):
    """Fixture to provide a fresh AppConfig instance pointing to a temp dir."""
    monkeypatch.setattr(AppConfig, "config_dir", tmp_path)
    # Reset singleton
    AppConfig._instance = None
    return AppConfig()


def test_accent_color_defaults_and_persists(clean_config):
    """Verify that accent_color has a default and persists changes."""
    config = clean_config

    # Test Default - Expecting 'blue' as the default per plan/spec implication
    # Note: If spec doesn't say, 'blue' is a reasonable default.
    assert config.accent_color == "blue"

    # Test Setter/Persistence
    config.accent_color = "purple"
    assert config.accent_color == "purple"

    # Force reload
    AppConfig._instance = None
    new_config = AppConfig()

    assert new_config.accent_color == "purple"


def test_config_from_dict_ignores_unknown_keys():
    """Verify from_dict ignores extra/unknown keys for forward compatibility."""
    data = {
        "theme": "light",
        "accent_color": "green",
        "unknown_future_key": "some_value",
        "another_unknown": 123,
    }
    config = Config.from_dict(data)

    assert config.theme == "light"
    assert config.accent_color == "green"
    # Should not raise, unknown keys are simply ignored


def test_config_from_dict_uses_defaults_for_missing_keys():
    """Verify from_dict uses defaults when keys are missing."""
    # Partial config - only theme provided
    data = {"theme": "light"}
    config = Config.from_dict(data)

    assert config.theme == "light"
    # Missing keys should get defaults
    assert config.accent_color == "blue"  # default
    assert config.default_view == "home"  # default
    assert config.log_level == "INFO"  # default
