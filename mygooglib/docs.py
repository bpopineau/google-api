"""Google Docs wrapper — render_template, export_pdf.

These helpers take the raw Docs v1 Resource from `get_clients().docs`.
They return plain Python types by default, with a `raw=True` escape hatch.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from googleapiclient.errors import HttpError

from mygooglib.exceptions import raise_for_http_error
from mygooglib.utils.retry import execute_with_retry_http_error


def create(docs: Any, title: str) -> str:
    """Create a new empty document.

    Args:
        docs: Docs API Resource from get_clients().docs
        title: Title for the new document

    Returns:
        The new document's ID.
    """
    try:
        request = docs.documents().create(body={"title": title})
        response = execute_with_retry_http_error(request, is_write=True)
        return response["documentId"]
    except HttpError as e:
        raise_for_http_error(e, context="Docs create")
        raise


def get_text(docs: Any, doc_id: str) -> str:
    """Get all plain text from a document.

    Args:
        docs: Docs API Resource
        doc_id: Document ID

    Returns:
        Full plain text content of the document.
    """
    try:
        request = docs.documents().get(documentId=doc_id)
        response = execute_with_retry_http_error(request, is_write=False)

        content = response.get("body", {}).get("content", [])
        text_parts = []
        for element in content:
            if "paragraph" in element:
                for part in element["paragraph"]["elements"]:
                    if "textRun" in part:
                        text_parts.append(part["textRun"]["content"])
        return "".join(text_parts)
    except HttpError as e:
        raise_for_http_error(e, context="Docs get_text")
        raise


def append_text(docs: Any, doc_id: str, text: str) -> None:
    """Append text to the end of a document.

    Args:
        docs: Docs API Resource
        doc_id: Document ID
        text: Text to append
    """
    try:
        # Fetch current content to find the end index
        request = docs.documents().get(documentId=doc_id, fields="body/content")
        response = execute_with_retry_http_error(request, is_write=False)
        content = response.get("body", {}).get("content", [])

        # The last element's endIndex (minus 1 for the trailing newline) is usually the end.
        if not content:
            end_index = 1
        else:
            end_index = content[-1]["endIndex"] - 1

        requests = [
            {
                "insertText": {
                    "location": {"index": max(1, end_index)},
                    "text": text,
                }
            }
        ]
        update_request = docs.documents().batchUpdate(
            documentId=doc_id, body={"requests": requests}
        )
        execute_with_retry_http_error(update_request, is_write=True)
    except HttpError as e:
        raise_for_http_error(e, context="Docs append_text")
        raise


def render_template(
    docs: Any,
    template_id: str,
    data: dict[str, str],
    *,
    title: str | None = None,
    drive: Any | None = None,
    raw: bool = False,
) -> str | dict:
    """Create a new document from a template by replacing placeholders.

    Placeholders in the doc should be in the format {{key}}.

    Args:
        docs: Docs API Resource from get_clients().docs
        template_id: ID of the template document
        data: Dictionary of keys and values to replace
        title: Title for the new document (None = use template name + timestamp)
        drive: Drive API Resource (required to copy the template)
        raw: If True, return full API response dict

    Returns:
        New document ID string by default, or full response if raw=True.
    """
    if drive is None:
        raise ValueError("drive=clients.drive is required to copy the template.")

    # 1. Copy the template using Drive API
    try:
        copy_metadata = {"name": title} if title else {}
        copy_request = drive.files().copy(fileId=template_id, body=copy_metadata)
        new_doc = execute_with_retry_http_error(copy_request, is_write=True)
        new_doc_id = new_doc["id"]
    except HttpError as e:
        raise_for_http_error(e, context="Docs render_template (copy)")
        raise

    # 2. Perform find-and-replace using Docs API
    requests = []
    for key, value in data.items():
        requests.append(
            {
                "replaceAllText": {
                    "containsText": {
                        "text": "{{" + key + "}}",
                        "matchCase": True,
                    },
                    "replaceText": str(value),
                }
            }
        )

    if not requests:
        return new_doc if raw else new_doc_id

    try:
        update_request = docs.documents().batchUpdate(
            documentId=new_doc_id, body={"requests": requests}
        )
        response = execute_with_retry_http_error(update_request, is_write=True)
    except HttpError as e:
        raise_for_http_error(e, context="Docs render_template (update)")
        raise

    return response if raw else new_doc_id


def export_pdf(
    drive: Any,
    doc_id: str,
    dest_path: str | os.PathLike,
) -> Path:
    """Export a Google Doc as a PDF.

    This is a convenience wrapper around drive.download_file.

    Args:
        drive: Drive API Resource
        doc_id: ID of the document to export
        dest_path: Local destination path (should end in .pdf)

    Returns:
        Path to the exported PDF.
    """
    from mygooglib.drive import download_file

    return download_file(drive, doc_id, dest_path, export_mime_type="application/pdf")


class DocsClient:
    """Simplified Google Docs API wrapper focusing on common operations."""

    def __init__(self, service: Any, drive: Any | None = None):
        """Initialize with an authorized Docs API service object."""
        self.service = service
        self.drive = drive

    def render_template(
        self,
        template_id: str,
        data: dict[str, str],
        *,
        title: str | None = None,
        raw: bool = False,
    ) -> str | dict:
        """Create a new document from a template by replacing placeholders."""
        return render_template(
            self.service,
            template_id,
            data,
            title=title,
            drive=self.drive,
            raw=raw,
        )

    def export_pdf(
        self,
        doc_id: str,
        dest_path: str | os.PathLike,
    ) -> Path:
        """Export a Google Doc as a PDF."""
        if self.drive is None:
            raise ValueError("drive=clients.drive is required to export PDF.")
        return export_pdf(self.drive, doc_id, dest_path)

    def create(self, title: str) -> str:
        """Create a new empty document."""
        return create(self.service, title)

    def get_text(self, doc_id: str) -> str:
        """Get all plain text from a document."""
        return get_text(self.service, doc_id)

    def append_text(self, doc_id: str, text: str) -> None:
        """Append text to the end of a document."""
        return append_text(self.service, doc_id, text)
