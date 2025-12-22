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
