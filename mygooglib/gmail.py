"""Gmail wrapper — send_email, search_messages, mark_read.

These helpers take the raw Gmail v1 Resource from `get_clients().gmail`.
They return plain Python types by default, with a `raw=True` escape hatch.
"""

from __future__ import annotations

import base64
import mimetypes
from collections.abc import Iterable, Sequence
from email.message import EmailMessage
from pathlib import Path
from typing import Any

from googleapiclient.errors import HttpError

from mygooglib.exceptions import raise_for_http_error
from mygooglib.utils.retry import execute_with_retry_http_error


def _as_address_list(value: str | Sequence[str] | None) -> str | None:
    """Convert email address(es) to comma-separated string (internal helper).

    Args:
        value: Single email address, list of addresses, or None

    Returns:
        Comma-separated string of addresses, or None
    """
    if value is None:
        return None
    if isinstance(value, str):
        return value
    return ", ".join(value)


def _guess_mime(path: Path) -> tuple[str, str]:
    """Guess MIME type from file path (internal helper).

    Args:
        path: Path to the file

    Returns:
        Tuple of (maintype, subtype) for MIME type, e.g. ('application', 'pdf')
    """
    mime = mimetypes.guess_type(str(path))[0] or "application/octet-stream"
    if "/" not in mime:
        return "application", "octet-stream"
    maintype, subtype = mime.split("/", 1)
    return maintype, subtype


def send_email(
    gmail: Any,
    *,
    to: str | Sequence[str],
    subject: str,
    body: str,
    attachments: Sequence[str | Path] | None = None,
    cc: str | Sequence[str] | None = None,
    bcc: str | Sequence[str] | None = None,
    user_id: str = "me",
    raw: bool = False,
    idempotency_key: str | None = None,
) -> str | dict | None:
    """Send a plain-text email with optional file attachments.

    Args:
            gmail: Gmail API Resource from get_clients().gmail
            to: Recipient email (or list of emails)
            subject: Subject line
            body: Plain text body
            attachments: Optional list of file paths
            cc: Optional CC email(s)
            bcc: Optional BCC email(s)
            user_id: Gmail userId (default "me")
            raw: If True, return full API response dict
            idempotency_key: Optional unique key to prevent duplicate sends.
                             If provided and the key was already used, the function
                             returns None instead of sending.

    Returns:
            Message ID string by default, or full response if raw=True.
            Returns None if idempotency_key was already processed.
    """
    # Check idempotency if key provided
    if idempotency_key:
        from mygooglib.utils.idempotency import IdempotencyStore

        store = IdempotencyStore()
        if store.check(idempotency_key):
            # Already processed, skip sending
            return None

    msg = EmailMessage()
    msg["To"] = _as_address_list(to)
    msg["Subject"] = subject
    cc_value = _as_address_list(cc)
    if cc_value:
        msg["Cc"] = cc_value
    bcc_value = _as_address_list(bcc)
    if bcc_value:
        msg["Bcc"] = bcc_value
    msg.set_content(body)

    for item in attachments or []:
        path = item if isinstance(item, Path) else Path(item)
        if not path.exists():
            raise FileNotFoundError(f"Attachment not found: {path}")
        data = path.read_bytes()
        maintype, subtype = _guess_mime(path)
        msg.add_attachment(data, maintype=maintype, subtype=subtype, filename=path.name)

    encoded = base64.urlsafe_b64encode(msg.as_bytes()).decode("utf-8")
    payload = {"raw": encoded}

    try:
        request = gmail.users().messages().send(userId=user_id, body=payload)
        response = execute_with_retry_http_error(request, is_write=True)
    except HttpError as e:
        raise_for_http_error(e, context="Gmail send_email")
        raise

    # Record successful send if idempotency key was provided
    if idempotency_key:
        import json

        metadata = json.dumps({"message_id": response.get("id")})
        store.add(idempotency_key, metadata=metadata)

    return response if raw else response.get("id")


def _headers_to_dict(headers: Iterable[dict[str, str]] | None) -> dict[str, str]:
    """Convert Gmail API headers list to a normalized dict (internal helper).

    Args:
        headers: List of header dicts from Gmail API (each with 'name' and 'value' keys)

    Returns:
        Dict mapping lowercase header names to values
    """
    result: dict[str, str] = {}
    for header in headers or []:
        name = (header.get("name") or "").strip()
        value = (header.get("value") or "").strip()
        if name:
            result[name.lower()] = value
    return result


def search_messages(
    gmail: Any,
    query: str,
    *,
    user_id: str = "me",
    max_results: int = 50,
    include_spam_trash: bool = False,
    raw: bool = False,
    progress_callback: Any | None = None,
) -> list[dict] | dict:
    """Search Gmail and return lightweight message dicts.

    Args:
            gmail: Gmail API Resource
            query: Gmail search query string (same syntax as the web UI)
            user_id: Gmail userId (default "me")
            max_results: Max messages to return (pagination handled)
            include_spam_trash: Include spam and trash
            raw: If True, return the raw list() response for the first page
            progress_callback: Optional callable(current_count, total_count)

    Returns:
            By default, list of dicts with keys: id, threadId, subject, sender, from, to, date, snippet.
            If raw=True, returns the first page list() response.
    """
    if max_results < 1:
        return [] if not raw else {"messages": []}

    page_token: str | None = None
    collected: list[dict] = []
    first_page: dict | None = None

    try:
        while len(collected) < max_results:
            list_request = (
                gmail.users()
                .messages()
                .list(
                    userId=user_id,
                    q=query,
                    includeSpamTrash=include_spam_trash,
                    pageToken=page_token,
                    maxResults=min(500, max_results - len(collected)),
                )
            )
            response = execute_with_retry_http_error(list_request, is_write=False)
            if first_page is None:
                first_page = response

            message_refs = response.get("messages", []) or []
            if not message_refs:
                break

            # Batch fetch metadata for this page of results to reduce round-trips.
            batch = gmail.new_batch_http_request()
            batch_results: dict[str, dict] = {}

            def _callback(
                request_id: str, response: dict, exception: Exception | None
            ) -> None:
                if not exception:
                    batch_results[request_id] = response

            for ref in message_refs:
                msg_id = ref.get("id")
                if not msg_id:
                    continue
                batch.add(
                    gmail.users()
                    .messages()
                    .get(
                        userId=user_id,
                        id=msg_id,
                        format="metadata",
                        metadataHeaders=["From", "To", "Subject", "Date"],
                    ),
                    callback=_callback,
                    request_id=msg_id,
                )

            # Wrap batch in a simple object with .execute() for retry helper.
            class _BatchWrapper:
                def __init__(self, b: Any):
                    self.b = b

                def execute(self) -> Any:
                    return self.b.execute()

            execute_with_retry_http_error(_BatchWrapper(batch), is_write=False)

            # Process batch results in order.
            for ref in message_refs:
                msg_id = ref.get("id")
                meta = batch_results.get(msg_id or "")
                if not meta:
                    continue

                payload = meta.get("payload") or {}
                headers = _headers_to_dict(payload.get("headers"))
                sender = headers.get("from")
                collected.append(
                    {
                        "id": meta.get("id"),
                        "threadId": meta.get("threadId"),
                        "subject": headers.get("subject"),
                        "sender": sender,
                        "from": headers.get("from"),
                        "to": headers.get("to"),
                        "date": headers.get("date"),
                        "snippet": meta.get("snippet"),
                    }
                )

                if progress_callback:
                    progress_callback(len(collected), max_results)

                if len(collected) >= max_results:
                    break

            page_token = response.get("nextPageToken")
            if not page_token:
                break

    except HttpError as e:
        raise_for_http_error(e, context="Gmail search_messages")
        raise

    if raw:
        return first_page or {"messages": []}
    return collected


def mark_read(
    gmail: Any,
    message_id: str,
    *,
    user_id: str = "me",
    raw: bool = False,
) -> dict | None:
    """Mark a message as read by removing the UNREAD label."""
    try:
        request = (
            gmail.users()
            .messages()
            .modify(
                userId=user_id,
                id=message_id,
                body={"removeLabelIds": ["UNREAD"]},
            )
        )
        response = execute_with_retry_http_error(request, is_write=True)
    except HttpError as e:
        raise_for_http_error(e, context="Gmail mark_read")
        raise

    return response if raw else None


def trash_message(
    gmail: Any,
    message_id: str,
    *,
    user_id: str = "me",
    raw: bool = False,
) -> dict | None:
    """Move a message to trash."""
    try:
        request = gmail.users().messages().trash(userId=user_id, id=message_id)
        response = execute_with_retry_http_error(request, is_write=True)
    except HttpError as e:
        raise_for_http_error(e, context="Gmail trash_message")
        raise
    return response if raw else None


def archive_message(
    gmail: Any,
    message_id: str,
    *,
    user_id: str = "me",
    raw: bool = False,
) -> dict | None:
    """Archive a message by removing the INBOX label."""
    try:
        request = (
            gmail.users()
            .messages()
            .modify(
                userId=user_id,
                id=message_id,
                body={"removeLabelIds": ["INBOX"]},
            )
        )
        response = execute_with_retry_http_error(request, is_write=True)
    except HttpError as e:
        raise_for_http_error(e, context="Gmail archive_message")
        raise
    return response if raw else None


def get_message(
    gmail: Any,
    message_id: str,
    *,
    user_id: str = "me",
    raw: bool = False,
) -> dict:
    """Get full message details including body.

    Args:
        gmail: Gmail API Resource
        message_id: Message ID
        user_id: Gmail userId (default "me")
        raw: If True, return the raw API response

    Returns:
        Dict with id, threadId, subject, from, to, date, snippet, and body.
    """
    try:
        request = (
            gmail.users().messages().get(userId=user_id, id=message_id, format="full")
        )
        response = execute_with_retry_http_error(request, is_write=False)
    except HttpError as e:
        raise_for_http_error(e, context="Gmail get_message")
        raise

    if raw:
        return response

    payload = response.get("payload") or {}
    headers = _headers_to_dict(payload.get("headers"))

    # Extract body
    body = ""
    parts = [payload]
    while parts:
        part = parts.pop(0)
        if part.get("parts"):
            parts.extend(part.get("parts") or [])
        if part.get("mimeType") == "text/plain":
            data = part.get("body", {}).get("data")
            if data:
                body += base64.urlsafe_b64decode(data).decode("utf-8")

    return {
        "id": response.get("id"),
        "threadId": response.get("threadId"),
        "subject": headers.get("subject"),
        "from": headers.get("from"),
        "to": headers.get("to"),
        "date": headers.get("date"),
        "snippet": response.get("snippet"),
        "body": body,
    }


def get_attachment(
    gmail: Any,
    message_id: str,
    attachment_id: str,
    *,
    user_id: str = "me",
) -> bytes:
    """Download a single attachment by ID.

    Args:
        gmail: Gmail API Resource
        message_id: Message ID containing the attachment
        attachment_id: Attachment ID from message parts
        user_id: Gmail userId (default "me")

    Returns:
        Raw bytes of the attachment
    """
    try:
        request = (
            gmail.users()
            .messages()
            .attachments()
            .get(userId=user_id, messageId=message_id, id=attachment_id)
        )
        response = execute_with_retry_http_error(request, is_write=False)
    except HttpError as e:
        raise_for_http_error(e, context="Gmail get_attachment")
        raise

    data = response.get("data", "")
    return base64.urlsafe_b64decode(data)


def _extract_attachments(payload: dict) -> list[dict]:
    """Extract attachment metadata from message payload (internal helper).

    Returns list of dicts with keys: filename, attachment_id, mime_type, size
    """
    attachments = []
    parts = [payload]
    while parts:
        part = parts.pop(0)
        if part.get("parts"):
            parts.extend(part.get("parts") or [])

        body = part.get("body", {})
        attachment_id = body.get("attachmentId")
        filename = part.get("filename")

        # Only include parts that are actual attachments (have attachmentId and filename)
        if attachment_id and filename:
            attachments.append(
                {
                    "filename": filename,
                    "attachment_id": attachment_id,
                    "mime_type": part.get("mimeType"),
                    "size": body.get("size", 0),
                }
            )

    return attachments


def save_attachments(
    gmail: Any,
    query: str,
    dest_folder: str | Path,
    *,
    user_id: str = "me",
    max_messages: int = 50,
    filename_filter: str | None = None,
    progress_callback: Any | None = None,
) -> list[Path]:
    """Save all attachments from messages matching a query to a folder.

    Args:
        gmail: Gmail API Resource
        query: Gmail search query string (e.g., "has:attachment from:invoices@")
        dest_folder: Destination folder path
        user_id: Gmail userId (default "me")
        max_messages: Maximum number of messages to process
        filename_filter: Optional substring filter for filenames (case-insensitive)
        progress_callback: Optional callable(saved_count, message_index, total_messages)

    Returns:
        List of Paths to saved attachment files
    """
    dest = Path(dest_folder)
    dest.mkdir(parents=True, exist_ok=True)

    # Search for messages
    messages = search_messages(gmail, query, user_id=user_id, max_results=max_messages)

    saved_files: list[Path] = []

    for idx, msg_meta in enumerate(messages):
        msg_id = msg_meta.get("id")
        if not msg_id:
            continue

        # Get full message to access parts
        try:
            request = (
                gmail.users().messages().get(userId=user_id, id=msg_id, format="full")
            )
            msg = execute_with_retry_http_error(request, is_write=False)
        except HttpError as e:
            raise_for_http_error(e, context="Gmail save_attachments get_message")
            raise

        payload = msg.get("payload", {})
        attachments = _extract_attachments(payload)

        for att in attachments:
            filename = att["filename"]

            # Apply filename filter if specified
            if filename_filter and filename_filter.lower() not in filename.lower():
                continue

            # Download attachment
            data = get_attachment(gmail, msg_id, att["attachment_id"], user_id=user_id)

            # Handle duplicate filenames by adding message ID prefix if needed
            target = dest / filename
            if target.exists():
                stem = Path(filename).stem
                suffix = Path(filename).suffix
                target = dest / f"{stem}_{msg_id[:8]}{suffix}"

            target.write_bytes(data)
            saved_files.append(target)

            if progress_callback:
                progress_callback(len(saved_files), idx + 1, len(messages))

    return saved_files


class GmailClient:
    """Simplified Gmail API wrapper focusing on common operations."""

    def __init__(self, service: Any):
        """Initialize with an authorized Gmail API service object."""
        self.service = service

    def send_email(
        self,
        *,
        to: str | Sequence[str],
        subject: str,
        body: str,
        attachments: Sequence[str | Path] | None = None,
        cc: str | Sequence[str] | None = None,
        bcc: str | Sequence[str] | None = None,
        user_id: str = "me",
        raw: bool = False,
        idempotency_key: str | None = None,
    ) -> str | dict | None:
        """Send a plain-text email with optional file attachments."""
        return send_email(
            self.service,
            to=to,
            subject=subject,
            body=body,
            attachments=attachments,
            cc=cc,
            bcc=bcc,
            user_id=user_id,
            raw=raw,
            idempotency_key=idempotency_key,
        )

    def search_messages(
        self,
        query: str,
        *,
        user_id: str = "me",
        max_results: int = 50,
        include_spam_trash: bool = False,
        raw: bool = False,
        progress_callback: Any | None = None,
    ) -> list[dict] | dict:
        """Search Gmail and return lightweight message dicts."""
        return search_messages(
            self.service,
            query,
            user_id=user_id,
            max_results=max_results,
            include_spam_trash=include_spam_trash,
            raw=raw,
            progress_callback=progress_callback,
        )

    def mark_read(
        self,
        message_id: str,
        *,
        user_id: str = "me",
        raw: bool = False,
    ) -> dict | None:
        """Mark a message as read by removing the UNREAD label."""
        return mark_read(
            self.service,
            message_id,
            user_id=user_id,
            raw=raw,
        )

    def trash_message(
        self,
        message_id: str,
        *,
        user_id: str = "me",
        raw: bool = False,
    ) -> dict | None:
        """Move a message to trash."""
        return trash_message(
            self.service,
            message_id,
            user_id=user_id,
            raw=raw,
        )

    def archive_message(
        self,
        message_id: str,
        *,
        user_id: str = "me",
        raw: bool = False,
    ) -> dict | None:
        """Archive a message by removing the INBOX label."""
        return archive_message(
            self.service,
            message_id,
            user_id=user_id,
            raw=raw,
        )

    def get_message(
        self,
        message_id: str,
        *,
        user_id: str = "me",
        raw: bool = False,
    ) -> dict:
        """Get full message details including body."""
        return get_message(
            self.service,
            message_id,
            user_id=user_id,
            raw=raw,
        )

    def get_attachment(
        self,
        message_id: str,
        attachment_id: str,
        *,
        user_id: str = "me",
    ) -> bytes:
        """Download a single attachment by ID."""
        return get_attachment(
            self.service,
            message_id,
            attachment_id,
            user_id=user_id,
        )

    def save_attachments(
        self,
        query: str,
        dest_folder: str | Path,
        *,
        user_id: str = "me",
        max_messages: int = 50,
        filename_filter: str | None = None,
        progress_callback: Any | None = None,
    ) -> list[Path]:
        """Save all attachments from messages matching a query to a folder."""
        return save_attachments(
            self.service,
            query,
            dest_folder,
            user_id=user_id,
            max_messages=max_messages,
            filename_filter=filename_filter,
            progress_callback=progress_callback,
        )
