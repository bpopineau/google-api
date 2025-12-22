"""Global search workflow across multiple Google services."""

from __future__ import annotations

from typing import Any, Dict, List

from mygooglib.services.drive import list_files
from mygooglib.services.gmail import search_messages


def global_search(
    clients: Any,
    query: str,
    *,
    limit: int = 5,
) -> List[Dict[str, Any]]:
    """Search across Drive and Gmail and return a unified result list.

    Args:
        clients: Client factory object (with .drive and .gmail)
        query: Search string
        limit: Max results per service

    Returns:
        List of result dicts: {
            "type": "drive" | "gmail",
            "id": str,
            "title": str,
            "snippet": str,
            "link": str,
            "date": str,
            "mime_type": str (optional)
        }
    """
    results = []

    # 1. Search Drive
    try:
        drive_files = list_files(
            clients.drive.service, query=f"name contains '{query}'", max_results=limit
        )
        for f in drive_files:
            results.append(
                {
                    "type": "drive",
                    "id": f.get("id"),
                    "title": f.get("name"),
                    "snippet": f"Modified: {f.get('modifiedTime')}",
                    "link": f.get(
                        "webViewLink", f"https://drive.google.com/open?id={f.get('id')}"
                    ),
                    "date": f.get("modifiedTime"),
                    "mime_type": f.get("mimeType"),
                }
            )
    except Exception as e:
        # Better to return partial results than fail entirely
        print(f"Drive search failed: {e}")

    # 2. Search Gmail
    try:
        gmail_msgs = search_messages(
            clients.gmail.service, query=query, max_results=limit
        )
        for m in gmail_msgs:
            results.append(
                {
                    "type": "gmail",
                    "id": m.get("id"),
                    "title": m.get("subject", "(No Subject)"),
                    "snippet": m.get("snippet", ""),
                    "link": f"https://mail.google.com/mail/u/0/#inbox/{m.get('id')}",
                    "date": m.get("date"),
                }
            )
    except Exception as e:
        print(f"Gmail search failed: {e}")

    # Sort by date descending (optional, if date formats are compatible)
    # For now, just return combined list.
    return results
