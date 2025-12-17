"""Credential loading and OAuth flow for the library."""

from __future__ import annotations

import os
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

# v0.1 scopes: Drive, Sheets, Gmail send/modify
SCOPES: list[str] = [
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/gmail.send",
    "https://www.googleapis.com/auth/gmail.modify",
]


def _default_secrets_dir() -> Path:
    local_app_data = os.environ.get("LOCALAPPDATA")
    if local_app_data:
        return Path(local_app_data) / "mygooglib"
    return Path.home() / ".config" / "mygooglib"


def _get_paths() -> tuple[Path, Path]:
    secrets_dir = _default_secrets_dir()
    creds_path = Path(
        os.environ.get("MYGOOGLIB_CREDENTIALS_PATH", "")
        or (secrets_dir / "credentials.json")
    )
    token_path = Path(
        os.environ.get("MYGOOGLIB_TOKEN_PATH", "") or (secrets_dir / "token.json")
    )
    return creds_path, token_path


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

    creds: Credentials | None = None

    if token_path.exists():
        creds = Credentials.from_authorized_user_file(str(token_path), scopes=scopes)

    if creds and creds.valid:
        return creds

    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
        token_path.write_text(creds.to_json(), encoding="utf-8")
        return creds

    # Need fresh authorization
    if not creds_path.exists():
        raise FileNotFoundError(
            f"OAuth client file not found at {creds_path}.\n"
            "Download it from Google Cloud Console and place it there,\n"
            "or set MYGOOGLIB_CREDENTIALS_PATH."
        )

    flow = InstalledAppFlow.from_client_secrets_file(str(creds_path), scopes=scopes)
    new_creds = flow.run_local_server(port=0)

    token_path.parent.mkdir(parents=True, exist_ok=True)
    token_path.write_text(new_creds.to_json(), encoding="utf-8")

    return new_creds  # type: ignore[return-value]
