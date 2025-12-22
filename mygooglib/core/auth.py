"""Credential loading and OAuth flow for the library."""

from __future__ import annotations

import os
from pathlib import Path
from typing import cast

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

from mygooglib.core.utils.logging import get_logger

# v0.1 scopes: Drive, Sheets, Gmail send/modify, Calendar, Tasks
# Note: These are broad. For production, consider narrower scopes like 'drive.file'.
SCOPES: list[str] = [
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/gmail.send",
    "https://www.googleapis.com/auth/gmail.modify",
    "https://www.googleapis.com/auth/calendar",
    "https://www.googleapis.com/auth/tasks",
    # Added in v0.3 for Contacts integration:
    "https://www.googleapis.com/auth/contacts.readonly",
]


def _default_secrets_dir() -> Path:
    local_app_data = os.environ.get("LOCALAPPDATA")
    if local_app_data:
        return Path(local_app_data) / "mygoog"
    return Path.home() / ".mygoog"


def _get_paths() -> tuple[Path, Path]:
    secrets_dir = _default_secrets_dir()

    # Creds path priority: env var > secrets_dir > project root (fallback)
    creds_path = Path(
        os.environ.get("MYGOOGLIB_CREDENTIALS_PATH", "")
        or (secrets_dir / "credentials.json")
    )
    if not creds_path.exists() and Path("credentials.json").exists():
        creds_path = Path("credentials.json")

    # Token path priority: env var > secrets_dir > project root (fallback)
    token_path = Path(
        os.environ.get("MYGOOGLIB_TOKEN_PATH", "") or (secrets_dir / "token.json")
    )
    if not token_path.exists() and Path("token.json").exists():
        token_path = Path("token.json")

    return creds_path, token_path


def get_auth_paths() -> tuple[Path, Path]:
    """Return the resolved (credentials.json, token.json) paths.

    This is useful for CLIs/scripts that want to display where secrets live,
    without re-implementing internal path logic.
    """

    return _get_paths()


def get_creds(*, scopes: list[str] | None = None) -> Credentials:
    """Load or create OAuth credentials.

    If token.json exists and is valid/refreshable, returns those credentials.
    Otherwise runs InstalledAppFlow (opens browser) and saves token.json.

    Args:
        scopes: Override default scopes if needed.

    Returns:
        Authorized Credentials object.
    """
    scopes = scopes or SCOPES
    creds_path, token_path = _get_paths()

    logger = get_logger("mygooglib.core.auth")

    creds: Credentials | None = None

    if token_path.exists():
        creds = Credentials.from_authorized_user_file(str(token_path), scopes=scopes)

    if creds and creds.valid:
        return creds

    if creds and creds.expired and creds.refresh_token:
        logger.info("Refreshing OAuth token (token path: %s)", token_path)
        try:
            creds.refresh(Request())
            token_path.parent.mkdir(parents=True, exist_ok=True)
            token_path.write_text(creds.to_json(), encoding="utf-8")
            logger.info("Saved refreshed token to %s", token_path)
            return creds
        except Exception as e:
            # Token refresh can fail due to network issues, revoked tokens, or expired refresh tokens
            logger.error("Failed to refresh OAuth token: %s", e)
            raise RuntimeError(
                f"OAuth token refresh failed: {e}. "
                "Your refresh token may be expired or revoked. "
                "Delete token.json and re-run scripts/oauth_setup.py to re-authenticate."
            ) from e

    # Need fresh authorization
    if not creds_path.exists():
        raise FileNotFoundError(
            f"OAuth client file not found at {creds_path}.\n"
            "Download it from Google Cloud Console and place it there,\n"
            "or set MYGOOGLIB_CREDENTIALS_PATH."
        )

    logger.info("Launching OAuth flow (credentials path: %s)", creds_path)
    flow = InstalledAppFlow.from_client_secrets_file(str(creds_path), scopes=scopes)
    new_creds = flow.run_local_server(port=0)

    token_path.parent.mkdir(parents=True, exist_ok=True)
    token_path.write_text(new_creds.to_json(), encoding="utf-8")

    logger.info("Saved new token to %s", token_path)

    return cast(Credentials, new_creds)


def verify_creds_exist() -> bool:
    """Check if valid or refreshable credentials likely exist.

    This is a fast, non-blocking check suitable for GUI startup detection.
    It does NOT attempt to refresh tokens or verify against the API.

    Returns:
        True if token.json exists, False otherwise.
    """
    _, token_path = _get_paths()
    return token_path.exists()
