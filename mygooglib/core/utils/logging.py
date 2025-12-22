"""Minimal, opt-in logging helpers.

This library is intended for personal scripts, so having an environment-variable
switch for debug logs is useful.

Design goals:
- Off by default (no handlers added)
- When enabled, logs only non-sensitive info
- Does not configure the root logger

Env vars:
- MYGOOGLIB_DEBUG=1              -> sets mygooglib logger to DEBUG
- MYGOOGLIB_LOG_LEVEL=INFO|DEBUG -> explicit level (overrides MYGOOGLIB_DEBUG)
"""

from __future__ import annotations

import logging
import os

_CONFIGURED = False


def _env_log_level() -> int | None:
    level = os.environ.get("MYGOOGLIB_LOG_LEVEL")
    if level:
        return int(getattr(logging, level.upper(), logging.INFO))
    if os.environ.get("MYGOOGLIB_DEBUG"):
        return logging.DEBUG
    return None


def configure_from_env(*, logger_name: str = "mygooglib") -> None:
    """Configure the `mygooglib` logger if env vars request it."""
    global _CONFIGURED

    if _CONFIGURED:
        return

    level = _env_log_level()
    if level is None:
        return

    base_logger = logging.getLogger(logger_name)
    base_logger.setLevel(level)

    # Add a single StreamHandler to the package logger.
    if not any(isinstance(h, logging.StreamHandler) for h in base_logger.handlers):
        handler = logging.StreamHandler()
        handler.setLevel(level)
        handler.setFormatter(logging.Formatter("[%(levelname)s] %(name)s: %(message)s"))
        base_logger.addHandler(handler)

    # Don't double-log through the root logger.
    base_logger.propagate = False

    _CONFIGURED = True


def get_logger(name: str = "mygooglib") -> logging.Logger:
    """Get a logger, applying env-based config if requested."""
    configure_from_env(logger_name="mygooglib")
    return logging.getLogger(name)
