from __future__ import annotations

import datetime as dt
import os
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

from scripts.oauth_setup import V0_1_SCOPES, _default_secrets_dir


def _token_path() -> Path:
    secrets_dir = _default_secrets_dir()
    return Path(
        os.environ.get("MYGOOGLIB_TOKEN_PATH", "") or (secrets_dir / "token.json")
    )


def _fmt_dt(value: dt.datetime | None) -> str:
    if value is None:
        return "(none)"
    if value.tzinfo is None:
        return value.isoformat() + "Z?"
    return value.isoformat()


def main() -> int:
    token_path = _token_path()
    if not token_path.exists():
        raise FileNotFoundError(
            "token.json not found. Run scripts/oauth_setup.py first to generate it.\n"
            f"Expected at: {token_path}"
        )

    creds = Credentials.from_authorized_user_file(str(token_path), scopes=V0_1_SCOPES)

    print(f"Token file: {token_path}")
    print(f"Expired: {creds.expired}")
    print(f"Valid: {creds.valid}")
    print(f"Expiry: {_fmt_dt(creds.expiry)}")

    # Force a refresh to confirm refresh token behavior.
    # (This should not re-prompt the user.)
    creds.refresh(Request())

    token_path.write_text(creds.to_json(), encoding="utf-8")

    print("\nRefresh OK. Updated token saved.")
    print(f"Expired: {creds.expired}")
    print(f"Valid: {creds.valid}")
    print(f"Expiry: {_fmt_dt(creds.expiry)}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
