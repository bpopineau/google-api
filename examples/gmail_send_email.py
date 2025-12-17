from __future__ import annotations

from mygooglib import get_clients
from mygooglib.gmail import send_email

TO = "you@example.com"  # replace


def main() -> int:
    clients = get_clients()

    message_id = send_email(
        clients.gmail,
        to=TO,
        subject="Test email from mygooglib",
        body="Hello!",
    )

    print(message_id)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
