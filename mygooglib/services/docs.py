"""Google Docs wrapper — render_template, export_pdf.

These helpers take the raw Docs v1 Resource from `get_clients().docs`.
They return plain Python types by default, with a `raw=True` escape hatch.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from mygooglib.core.utils.base import BaseClient
from mygooglib.core.utils.retry import api_call, execute_with_retry_http_error


@api_call("Docs create", is_write=True)
def create(docs: Any, title: str) -> str:
    """Create a new empty document.

    Args:
        docs: Docs API Resource from get_clients().docs
        title: Title for the new document

    Returns:
        The new document's ID.
    """
    request = docs.documents().create(body={"title": title})
    response = execute_with_retry_http_error(request, is_write=True)
    return response["documentId"]


@api_call("Docs get_text", is_write=False)
def get_text(docs: Any, doc_id: str) -> str:
    """Get all plain text from a document.

    Args:
        docs: Docs API Resource
        doc_id: Document ID

    Returns:
        Full plain text content of the document.
    """
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


@api_call("Docs append_text", is_write=True)
def append_text(docs: Any, doc_id: str, text: str) -> None:
    """Append text to the end of a document.

    Args:
        docs: Docs API Resource
        doc_id: Document ID
        text: Text to append
    """
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


@api_call("Docs render_template", is_write=True)
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
    copy_metadata = {"name": title} if title else {}
    copy_request = drive.files().copy(fileId=template_id, body=copy_metadata)
    new_doc = execute_with_retry_http_error(copy_request, is_write=True)
    new_doc_id = new_doc["id"]

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

    update_request = docs.documents().batchUpdate(
        documentId=new_doc_id, body={"requests": requests}
    )
    response = execute_with_retry_http_error(update_request, is_write=True)

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
    from mygooglib.services.drive import download_file

    return download_file(drive, doc_id, dest_path, export_mime_type="application/pdf")


@api_call("Docs insert_table", is_write=True)
def insert_table(
    docs: Any,
    doc_id: str,
    rows: list[list[str]],
    *,
    headers: list[str] | None = None,
    index: int | None = None,
) -> int:
    """Insert a table into a document.

    Args:
        docs: Docs API Resource
        doc_id: Document ID
        rows: List of lists containing cell values (each inner list is a row)
        headers: Optional header row (prepended to rows)
        index: Position to insert (None = end of document)

    Returns:
        Number of rows inserted (including header if provided).
    """
    if not rows and not headers:
        return 0

    # Build complete data including headers
    all_rows = []
    if headers:
        all_rows.append(headers)
    all_rows.extend(rows)

    num_rows = len(all_rows)
    num_cols = max(len(row) for row in all_rows) if all_rows else 1

    # Get document to find insertion point
    if index is None:
        get_request = docs.documents().get(documentId=doc_id, fields="body/content")
        response = execute_with_retry_http_error(get_request, is_write=False)
        content = response.get("body", {}).get("content", [])
        index = content[-1]["endIndex"] - 1 if content else 1

    # Create table structure
    requests = [
        {
            "insertTable": {
                "rows": num_rows,
                "columns": num_cols,
                "location": {"index": max(1, index)},
            }
        }
    ]

    # Insert table first
    update_request = docs.documents().batchUpdate(
        documentId=doc_id, body={"requests": requests}
    )
    execute_with_retry_http_error(update_request, is_write=True)

    # Now populate the cells (requires a fresh get to know table structure)
    get_request = docs.documents().get(documentId=doc_id)
    doc = execute_with_retry_http_error(get_request, is_write=False)

    # Find the table we just inserted and populate cells
    content = doc.get("body", {}).get("content", [])
    table_element = None
    for element in content:
        if "table" in element:
            table_element = element
            break

    if table_element and "table" in table_element:
        table = table_element["table"]
        cell_requests = []

        for row_idx, row_data in enumerate(all_rows):
            table_row = (
                table.get("tableRows", [])[row_idx]
                if row_idx < len(table.get("tableRows", []))
                else None
            )
            if not table_row:
                continue

            for col_idx, cell_value in enumerate(row_data):
                table_cells = table_row.get("tableCells", [])
                if col_idx >= len(table_cells):
                    continue

                cell = table_cells[col_idx]
                cell_content = cell.get("content", [])
                if cell_content:
                    # Insert at the start of the cell's paragraph
                    para = cell_content[0]
                    start_index = para.get("startIndex", 1)
                    cell_requests.append(
                        {
                            "insertText": {
                                "location": {"index": start_index},
                                "text": str(cell_value),
                            }
                        }
                    )

        if cell_requests:
            # Reverse to maintain correct indices
            cell_requests.reverse()
            populate_request = docs.documents().batchUpdate(
                documentId=doc_id, body={"requests": cell_requests}
            )
            execute_with_retry_http_error(populate_request, is_write=True)

    return num_rows


def render_list(
    docs: Any,
    doc_id: str,
    tag: str,
    items: list[str],
    *,
    bullet: str = "• ",
) -> int:
    """Replace a placeholder tag with a bulleted list.

    Args:
        docs: Docs API Resource
        doc_id: Document ID
        tag: Placeholder tag to replace (e.g., "{{ITEMS}}")
        items: List of strings to render as bullet points
        bullet: Bullet character/string (default "• ")

    Returns:
        Number of items inserted.
    """
    if not items:
        # Just remove the tag if no items
        find_replace(docs, doc_id, {tag: ""})
        return 0

    # Build the bulleted list text
    list_text = "\\n".join(f"{bullet}{item}" for item in items)

    # Replace the tag with the list
    find_replace(docs, doc_id, {tag: list_text})

    return len(items)


@api_call("Docs find_replace", is_write=True)
def find_replace(
    docs: Any,
    doc_id: str,
    replacements: dict[str, str],
    *,
    match_case: bool = True,
) -> int:
    """Perform multiple find-and-replace operations in a document.

    Args:
        docs: Docs API Resource
        doc_id: Document ID
        replacements: Dictionary of search -> replace strings
        match_case: Whether to match case sensitive (default True)

    Returns:
        Number of occurrences replaced (total across all keys).
    """
    if not replacements:
        return 0

    requests = []
    for search_term, replace_term in replacements.items():
        requests.append(
            {
                "replaceAllText": {
                    "containsText": {
                        "text": search_term,
                        "matchCase": match_case,
                    },
                    "replaceText": str(replace_term),
                }
            }
        )

    try:
        update_request = docs.documents().batchUpdate(
            documentId=doc_id, body={"requests": requests}
        )
        response = execute_with_retry_http_error(update_request, is_write=True)

        total_replaced = 0
        for reply in response.get("replies", []):
            if "replaceAllText" in reply:
                total_replaced += reply["replaceAllText"].get("occurrencesChanged", 0)
        return total_replaced

    except Exception as e:
        # Check for empty response or other oddities
        if "replies" not in str(e):
            raise
        return 0


class DocsClient(BaseClient):
    """Simplified Google Docs API wrapper focusing on common operations."""

    def __init__(self, service: Any, drive: Any | None = None):
        """Initialize with an authorized Docs API service object."""
        super().__init__(service)
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

    def find_replace(
        self,
        doc_id: str,
        replacements: dict[str, str],
        *,
        match_case: bool = True,
    ) -> int:
        """Perform multiple find-and-replace operations in a document."""
        return find_replace(self.service, doc_id, replacements, match_case=match_case)

    def insert_table(
        self,
        doc_id: str,
        rows: list[list[str]],
        *,
        headers: list[str] | None = None,
        index: int | None = None,
    ) -> int:
        """Insert a table into a document."""
        return insert_table(self.service, doc_id, rows, headers=headers, index=index)

    def render_list(
        self,
        doc_id: str,
        tag: str,
        items: list[str],
        *,
        bullet: str = "• ",
    ) -> int:
        """Replace a placeholder tag with a bulleted list."""
        return render_list(self.service, doc_id, tag, items, bullet=bullet)
