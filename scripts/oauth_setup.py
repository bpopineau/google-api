from __future__ import annotations

import os
from pathlib import Path

from google_auth_oauthlib.flow import InstalledAppFlow

from mygooglib.core.auth import SCOPES


def _default_secrets_dir() -> Path:
    # Windows-friendly default; overridable via env vars.
    local_app_data = os.environ.get("LOCALAPPDATA")
    if local_app_data:
        return Path(local_app_data) / "mygooglib"
    # Fallback for non-Windows or unusual shells.
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


def main() -> int:
    creds_path, token_path = _get_paths()

    if not creds_path.exists():
        raise FileNotFoundError(
            "OAuth client file not found. Place your downloaded Desktop-app credentials.json at:\n"
            f"  {creds_path}\n\n"
            "Or set MYGOOGLIB_CREDENTIALS_PATH to where you stored it."
        )

    token_path.parent.mkdir(parents=True, exist_ok=True)

    flow = InstalledAppFlow.from_client_secrets_file(str(creds_path), scopes=SCOPES)
    creds = flow.run_local_server(port=0)

    token_path.write_text(creds.to_json(), encoding="utf-8")

    print("Saved token:")
    print(f"  {token_path}")
    print("Scopes granted:")
    for scope in SCOPES:
        print(f"  - {scope}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
