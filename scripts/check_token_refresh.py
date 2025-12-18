from __future__ import annotations

import datetime as dt

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

from mygooglib.auth import SCOPES, get_auth_paths


def _fmt_dt(value: dt.datetime | None) -> str:
    if value is None:
        return "(none)"
    if value.tzinfo is None:
        return value.isoformat() + "Z?"
    return value.isoformat()


def main() -> int:
    _, token_path = get_auth_paths()
    if not token_path.exists():
        raise FileNotFoundError(
            "token.json not found. Run scripts/oauth_setup.py first to generate it.\n"
            f"Expected at: {token_path}"
        )

    creds = Credentials.from_authorized_user_file(str(token_path), scopes=SCOPES)

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
