"""Theme manager for dynamic theme application in the MyGoog GUI."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from PySide6.QtCore import QObject, Signal
from PySide6.QtGui import QColor, QGuiApplication, QPalette
from PySide6.QtWidgets import QApplication

from mygooglib import AppConfig

from .styles import get_stylesheet

if TYPE_CHECKING:
    pass

logger = logging.getLogger(__name__)


class ThemeManager(QObject):
    """Centralized theme manager for the application.

    Handles theme detection, application, and change notifications.
    """

    # Signal emitted when theme changes
    theme_changed = Signal(str, str)  # (theme, accent_color)

    _instance: "ThemeManager | None" = None

    def __new__(cls) -> "ThemeManager":
        """Singleton pattern to ensure one theme manager."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    _initialized: bool = False

    def __init__(self) -> None:
        # Prevent re-initialization
        if self._initialized:
            return

        super().__init__()
        self._initialized = True
        self._config = AppConfig()
        self._current_theme = self._config.theme
        self._current_accent = self._config.accent_color

    @property
    def current_theme(self) -> str:
        """Get the current active theme."""
        return self._current_theme

    @property
    def current_accent(self) -> str:
        """Get the current accent color."""
        return self._current_accent

    def detect_system_theme(self) -> str:
        """Detect the system's preferred color scheme.

        Returns:
            "dark" or "light" based on system preference
        """
        try:
            # PySide6 way to detect system theme
            app = QGuiApplication.instance()
            if app and isinstance(app, QGuiApplication):
                palette = app.palette()
                # Compare window background luminance
                bg_color = palette.color(QPalette.ColorRole.Window)
                # Simple luminance check (dark bg = dark theme)
                luminance = (
                    0.299 * bg_color.red()
                    + 0.587 * bg_color.green()
                    + 0.114 * bg_color.blue()
                )
                return "dark" if luminance < 128 else "light"
        except Exception as e:
            logger.warning(f"Failed to detect system theme: {e}")

        # Default to dark
        return "dark"

    def resolve_theme(self, theme: str) -> str:
        """Resolve 'system' theme to actual dark/light value.

        Args:
            theme: "dark", "light", or "system"

        Returns:
            "dark" or "light"
        """
        if theme == "system":
            return self.detect_system_theme()
        return theme if theme in ("dark", "light") else "dark"

    def apply_theme(
        self, theme: str | None = None, accent_color: str | None = None
    ) -> None:
        """Apply theme to the application.

        Args:
            theme: Theme to apply ("dark", "light", "system").
                   If None, uses saved config.
            accent_color: Accent color to apply.
                         If None, uses saved config.
        """
        app = QApplication.instance()
        if not app or not isinstance(app, QApplication):
            logger.warning("No QApplication instance, cannot apply theme")
            return

        # Use provided values or fall back to config
        theme = theme if theme is not None else self._config.theme
        accent_color = (
            accent_color if accent_color is not None else self._config.accent_color
        )

        # Resolve system theme
        resolved_theme = self.resolve_theme(theme)

        # Generate and apply stylesheet
        stylesheet = get_stylesheet(resolved_theme, accent_color)
        app.setStyleSheet(stylesheet)

        # Update state
        self._current_theme = theme
        self._current_accent = accent_color

        # Emit change signal
        self.theme_changed.emit(theme, accent_color)
        logger.info(
            f"Applied theme: {theme} (resolved: {resolved_theme}), accent: {accent_color}"
        )

    def set_theme(self, theme: str) -> None:
        """Set and apply a new theme, saving to config.

        Args:
            theme: "dark", "light", or "system"
        """
        self._config.theme = theme
        self.apply_theme(theme=theme)

    def set_accent_color(self, accent_color: str) -> None:
        """Set and apply a new accent color, saving to config.

        Args:
            accent_color: "blue", "green", "purple", or "orange"
        """
        self._config.accent_color = accent_color
        self.apply_theme(accent_color=accent_color)

    @classmethod
    def reset_instance(cls) -> None:
        """Reset the singleton instance (for testing)."""
        cls._instance = None
