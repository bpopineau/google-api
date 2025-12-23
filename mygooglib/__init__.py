"""Personal Google APIs wrapper library.

Quick start:
    from mygooglib import get_clients
    clients = get_clients()
    # Use the ergonomic client wrappers:
    file_id = clients.drive.upload_file("./report.pdf")
    values = clients.sheets.get_range("SPREADSHEET_ID", "Sheet1!A1:C10")
    clients.gmail.send_email(to="me@example.com", subject="Hello", body="World")
"""

from mygooglib.core.auth import SCOPES, get_auth_paths, get_creds, verify_creds_exist
from mygooglib.core.client import Clients, get_clients
from mygooglib.core.config import AppConfig
from mygooglib.core.exceptions import GoogleApiError
from mygooglib.core.utils.file_scanner import FileScanner

# Re-export high-value types for strict typing
from mygooglib.core.types import (
    # Gmail types
    AttachmentMetadataDict,
    LabelDict,
    MessageDict,
    MessageFullDict,
    MessageMetadataDict,
    # Sheets types
    RangeData,
    SendMessageResponseDict,
    SheetInfoDict,
    SpreadsheetDict,
    UpdateValuesResponseDict,
    ValueRangeDict,
)

# Non-breaking aliases for a cleaner public API.
create = get_clients
create_clients = get_clients

__all__ = [
    # Core API
    "get_creds",
    "get_clients",
    "Clients",
    "create",
    "create_clients",
    "GoogleApiError",
    "AppConfig",
    "SCOPES",
    "get_auth_paths",
    "verify_creds_exist",
    "FileScanner",
    # Sheets Types
    "RangeData",
    "SheetInfoDict",
    "SpreadsheetDict",
    "UpdateValuesResponseDict",
    "ValueRangeDict",
    # Gmail Types
    "AttachmentMetadataDict",
    "LabelDict",
    "MessageDict",
    "MessageFullDict",
    "MessageMetadataDict",
    "SendMessageResponseDict",
]
