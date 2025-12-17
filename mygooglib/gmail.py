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
    if value is None:
        return None
    if isinstance(value, str):
        return value
    return ", ".join(value)


def _guess_mime(path: Path) -> tuple[str, str]:
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
) -> str | dict:
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

    Returns:
            Message ID string by default, or full response if raw=True.
    """
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

    return response if raw else response.get("id")


def _headers_to_dict(headers: Iterable[dict[str, str]] | None) -> dict[str, str]:
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
) -> list[dict] | dict:
    """Search Gmail and return lightweight message dicts.

    Args:
            gmail: Gmail API Resource
            query: Gmail search query string (same syntax as the web UI)
            user_id: Gmail userId (default "me")
            max_results: Max messages to return (pagination handled)
            include_spam_trash: Include spam and trash
            raw: If True, return the raw list() response for the first page

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

            for ref in message_refs:
                msg_id = ref.get("id")
                if not msg_id:
                    continue
                get_request = (
                    gmail.users()
                    .messages()
                    .get(
                        userId=user_id,
                        id=msg_id,
                        format="metadata",
                        metadataHeaders=["From", "To", "Subject", "Date"],
                    )
                )
                meta = execute_with_retry_http_error(get_request, is_write=False)
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
