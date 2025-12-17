from __future__ import annotations

from mygooglib import get_clients
from mygooglib.gmail import send_email
from mygooglib.sheets import get_range

# Replace with your spreadsheet title, ID, or full URL.
SPREADSHEET = "Your Sheet Title"
RANGE = "Sheet1!A1:C10"

# Replace with a real email address.
TO = "you@example.com"


def main() -> int:
    clients = get_clients()

    values = get_range(
        clients.sheets,
        SPREADSHEET,
        RANGE,
        drive=clients.drive,  # required if SPREADSHEET is a title
    )

    lines = ["\t".join(map(str, row)) for row in values]
    body = "\n".join(lines) if lines else "(No values returned.)"

    message_id = send_email(
        clients.gmail,
        to=TO,
        subject=f"Sheet summary: {SPREADSHEET} {RANGE}",
        body=body,
    )

    print(message_id)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
