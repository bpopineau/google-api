"""Idempotency utilities to prevent duplicate operations.

This module provides a local SQLite-based store to track processed items
(e.g., email message IDs, file hashes, or arbitrary keys) to ensure
scripts don't repeat actions if run multiple times.
"""

from __future__ import annotations

import functools
import sqlite3
from pathlib import Path
from typing import Any, Callable

# Default location: ~/.mygooglib/idempotency.db
DEFAULT_DB_PATH = Path.home() / ".mygooglib" / "idempotency.db"


class IdempotencyStore:
    """Local SQLite store for tracking processed keys."""

    def __init__(self, db_path: Path | str | None = None):
        """Initialize the store.

        Args:
            db_path: Path to the SQLite database. Defaults to ~/.mygooglib/idempotency.db.
        """
        if db_path is None:
            db_path = DEFAULT_DB_PATH
        self.db_path = Path(db_path)
        self._init_db()

    def _init_db(self) -> None:
        """Create the database and table if they don't exist."""
        if not self.db_path.parent.exists():
            self.db_path.parent.mkdir(parents=True, exist_ok=True)

        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS processed_items (
                    key TEXT PRIMARY KEY,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    metadata TEXT
                )
                """
            )
            conn.commit()

    def check(self, key: str) -> bool:
        """Check if a key has been processed.

        Args:
            key: Unique identifier.

        Returns:
            True if the key exists, False otherwise.
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("SELECT 1 FROM processed_items WHERE key = ?", (key,))
            return cursor.fetchone() is not None

    def add(self, key: str, metadata: str | None = None) -> None:
        """Mark a key as processed.

        Args:
            key: Unique identifier.
            metadata: Optional string (e.g., JSON) to store with the key.
        """
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "INSERT OR IGNORE INTO processed_items (key, metadata) VALUES (?, ?)",
                (key, metadata),
            )
            conn.commit()

    def check_and_add(self, key: str, metadata: str | None = None) -> bool:
        """Atomic check-and-set.

        Args:
            key: Unique identifier.
            metadata: Optional metadata.

        Returns:
            True if the item was NEW (and is now added).
            False if the item was ALREADY processed.
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute(
                    "INSERT INTO processed_items (key, metadata) VALUES (?, ?)",
                    (key, metadata),
                )
                conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def clear(self) -> None:
        """Clear all records (mostly for testing)."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("DELETE FROM processed_items")
            conn.commit()


def idempotent(
    key_func: Callable[..., str], store: IdempotencyStore | None = None
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """Decorator to make a function idempotent based on a key derived from arguments.

    Args:
        key_func: A function that takes the same arguments as the decorated function
                  and returns a string key.
        store: Optional IdempotencyStore instance. If None, uses default.

    Returns:
        Decorated function that skips execution if the key is already in the store.
    """
    _store = store or IdempotencyStore()

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            key = key_func(*args, **kwargs)
            if _store.check(key):
                # Already processed
                return None  # Or distinct sentinel?

            result = func(*args, **kwargs)
            _store.add(key)
            return result

        return wrapper

    return decorator
