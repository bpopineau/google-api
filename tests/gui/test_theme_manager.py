"""Tests for the theme manager and stylesheet generation."""

from mygoog_gui.styles import (
    ACCENT_PALETTES,
    DARK_COLORS,
    LIGHT_COLORS,
    get_stylesheet,
)


class TestGetStylesheet:
    """Tests for the get_stylesheet function."""

    def test_dark_theme_uses_dark_colors(self):
        """Verify dark theme includes dark background colors."""
        stylesheet = get_stylesheet("dark", "green")

        # Dark theme should have dark background
        assert DARK_COLORS["bg_primary"] in stylesheet
        assert DARK_COLORS["bg_secondary"] in stylesheet

    def test_light_theme_uses_light_colors(self):
        """Verify light theme includes light background colors."""
        stylesheet = get_stylesheet("light", "green")

        # Light theme should have light background
        assert LIGHT_COLORS["bg_primary"] in stylesheet
        assert LIGHT_COLORS["bg_secondary"] in stylesheet

    def test_accent_color_applied(self):
        """Verify accent color is included in stylesheet."""
        stylesheet = get_stylesheet("dark", "purple")

        # Purple accent should be present
        assert ACCENT_PALETTES["purple"]["accent"] in stylesheet
        assert ACCENT_PALETTES["purple"]["accent_hover"] in stylesheet

    def test_all_accent_colors_valid(self):
        """Verify all accent color options produce valid stylesheets."""
        for accent in ["blue", "green", "purple", "orange"]:
            stylesheet = get_stylesheet("dark", accent)
            assert len(stylesheet) > 0
            assert ACCENT_PALETTES[accent]["accent"] in stylesheet

    def test_all_theme_accent_combinations(self):
        """Verify all theme/accent combinations work."""
        for theme in ["dark", "light"]:
            for accent in ["blue", "green", "purple", "orange"]:
                stylesheet = get_stylesheet(theme, accent)
                assert len(stylesheet) > 1000  # Should be substantial

    def test_invalid_accent_falls_back_to_green(self):
        """Verify invalid accent color falls back to green."""
        stylesheet = get_stylesheet("dark", "invalid_color")
        assert ACCENT_PALETTES["green"]["accent"] in stylesheet

    def test_stylesheet_contains_expected_selectors(self):
        """Verify stylesheet has key QSS selectors."""
        stylesheet = get_stylesheet("dark", "blue")

        expected_selectors = [
            "QMainWindow",
            "QPushButton",
            "QLineEdit",
            "QComboBox",
            "#sidebar",
        ]
        for selector in expected_selectors:
            assert selector in stylesheet
