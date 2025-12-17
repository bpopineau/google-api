"""Personal Google APIs wrapper library.

Quick start:
    from mygooglib import get_clients
    clients = get_clients()
    # Use the ergonomic client wrappers:
    file_id = clients.drive.upload_file("./report.pdf")
    values = clients.sheets.get_range("SPREADSHEET_ID", "Sheet1!A1:C10")
    clients.gmail.send_email(to="me@example.com", subject="Hello", body="World")
"""

from mygooglib.auth import get_creds
from mygooglib.client import get_clients

# Non-breaking aliases for a cleaner public API.
create = get_clients
create_clients = get_clients

__all__ = ["get_creds", "get_clients", "create", "create_clients"]
