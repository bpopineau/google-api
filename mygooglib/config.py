"""Configuration management for the MyGoog application."""

from __future__ import annotations

import json
import logging
import os
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


@dataclass
class Config:
    """Application configuration schema."""

    theme: str = "dark"
    window_geometry: list[int] = field(default_factory=lambda: [100, 100, 1200, 800])
    default_view: str = "home"
    log_level: str = "INFO"

    # Example of nested or extensibility structure if needed later
    # features: dict[str, bool] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Config:
        """Create config from dictionary, ignoring unknown keys for forward compatibility."""
        valid_keys = {k for k in cls.__dataclass_fields__}  # type: ignore
        filtered_data = {k: v for k, v in data.items() if k in valid_keys}
        return cls(**filtered_data)


class AppConfig:
    """Singleton configuration manager."""

    _instance = None
    _config: Config

    def __new__(cls) -> AppConfig:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._load()
        return cls._instance

    @property
    def config_dir(self) -> Path:
        """Return the directory where config is stored."""
        path = Path.home() / ".mygooglib"
        path.mkdir(exist_ok=True)
        return path

    @property
    def config_file(self) -> Path:
        """Return the path to the config file."""
        return self.config_dir / "config.json"

    def _load(self) -> None:
        """Load configuration from disk or create default."""
        if not self.config_file.exists():
            self._config = Config()
            self.save()
            return

        try:
            with open(self.config_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                self._config = Config.from_dict(data)
        except (json.JSONDecodeError, OSError) as e:
            logger.error(f"Failed to load config, using defaults: {e}")
            self._config = Config()

    def save(self) -> None:
        """Save current configuration to disk."""
        try:
            with open(self.config_file, "w", encoding="utf-8") as f:
                json.dump(asdict(self._config), f, indent=4)
        except OSError as e:
            logger.error(f"Failed to save config: {e}")

    # Proxy accessors for convenience
    @property
    def theme(self) -> str:
        return self._config.theme

    @theme.setter
    def theme(self, value: str) -> None:
        self._config.theme = value
        self.save()

    @property
    def window_geometry(self) -> list[int]:
        return self._config.window_geometry

    @window_geometry.setter
    def window_geometry(self, value: list[int]) -> None:
        self._config.window_geometry = value
        self.save()

    @property
    def default_view(self) -> str:
        return self._config.default_view

    @default_view.setter
    def default_view(self, value: str) -> None:
        self._config.default_view = value
        self.save()

    @property
    def log_level(self) -> str:
        return self._config.log_level
