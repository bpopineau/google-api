"""Google Drive wrapper — upload, download, list, sync."""

from __future__ import annotations

import mimetypes
import os
from pathlib import Path
from typing import Any

from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload

from mygooglib.exceptions import raise_for_http_error

# Google Workspace MIME types
FOLDER_MIME_TYPE = "application/vnd.google-apps.folder"
GOOGLE_DOC_MIME = "application/vnd.google-apps.document"
GOOGLE_SHEET_MIME = "application/vnd.google-apps.spreadsheet"
GOOGLE_SLIDES_MIME = "application/vnd.google-apps.presentation"

# Default fields to return for file metadata
DEFAULT_FIELDS = "id, name, mimeType, modifiedTime, size, parents"


def list_files(
    drive: Any,
    *,
    query: str | None = None,
    parent_id: str | None = None,
    mime_type: str | None = None,
    trashed: bool = False,
    page_size: int = 100,
    fields: str = DEFAULT_FIELDS,
) -> list[dict]:
    """List files matching criteria with full pagination.

    Args:
        drive: Drive API Resource from get_clients().drive
        query: Raw query string (combined with other filters via AND)
        parent_id: Filter to files in this folder
        mime_type: Filter by MIME type
        trashed: Include trashed files (default False)
        page_size: Results per page (max 1000)
        fields: Which file fields to return

    Returns:
        List of file metadata dicts with requested fields.
    """
    query_parts: list[str] = []

    if query:
        query_parts.append(f"({query})")
    if parent_id:
        query_parts.append(f"'{parent_id}' in parents")
    if mime_type:
        query_parts.append(f"mimeType = '{mime_type}'")
    if not trashed:
        query_parts.append("trashed = false")

    q = " and ".join(query_parts) if query_parts else None

    all_files: list[dict] = []
    page_token: str | None = None

    try:
        while True:
            response = (
                drive.files()
                .list(
                    q=q,
                    pageSize=page_size,
                    pageToken=page_token,
                    fields=f"nextPageToken, files({fields})",
                )
                .execute()
            )
            all_files.extend(response.get("files", []))
            page_token = response.get("nextPageToken")
            if not page_token:
                break
    except HttpError as e:
        raise_for_http_error(e)

    return all_files


def find_by_name(
    drive: Any,
    name: str,
    *,
    parent_id: str | None = None,
    mime_type: str | None = None,
) -> dict | None:
    """Find first file with exact name.

    Args:
        drive: Drive API Resource
        name: Exact filename to match
        parent_id: Limit search to this folder
        mime_type: Filter by MIME type

    Returns:
        File metadata dict if found, None otherwise.
    """
    # Escape single quotes in name for query
    escaped_name = name.replace("'", "\\'")
    results = list_files(
        drive,
        query=f"name = '{escaped_name}'",
        parent_id=parent_id,
        mime_type=mime_type,
    )
    return results[0] if results else None


def create_folder(
    drive: Any,
    name: str,
    *,
    parent_id: str | None = None,
) -> str:
    """Create a folder in Drive.

    Args:
        drive: Drive API Resource
        name: Folder name
        parent_id: Parent folder ID (None = root)

    Returns:
        The new folder's ID.
    """
    metadata: dict = {
        "name": name,
        "mimeType": FOLDER_MIME_TYPE,
    }
    if parent_id:
        metadata["parents"] = [parent_id]

    try:
        folder = drive.files().create(body=metadata, fields="id").execute()
        return folder["id"]
    except HttpError as e:
        raise_for_http_error(e)
        raise  # unreachable but satisfies type checker


def upload_file(
    drive: Any,
    local_path: str | os.PathLike,
    *,
    parent_id: str | None = None,
    name: str | None = None,
    mime_type: str | None = None,
) -> str:
    """Upload a local file to Drive.

    Args:
        drive: Drive API Resource
        local_path: Path to local file
        parent_id: Destination folder ID (None = root)
        name: Name in Drive (None = use local filename)
        mime_type: Override MIME type (None = auto-detect)

    Returns:
        The uploaded file's ID.
    """
    path = Path(local_path)
    if not path.exists():
        raise FileNotFoundError(f"Local file not found: {path}")

    file_name = name or path.name
    detected_mime = (
        mime_type or mimetypes.guess_type(str(path))[0] or "application/octet-stream"
    )

    metadata: dict = {"name": file_name}
    if parent_id:
        metadata["parents"] = [parent_id]

    media = MediaFileUpload(str(path), mimetype=detected_mime, resumable=True)

    try:
        result = (
            drive.files().create(body=metadata, media_body=media, fields="id").execute()
        )
        return result["id"]
    except HttpError as e:
        raise_for_http_error(e)
        raise  # unreachable but satisfies type checker


def download_file(
    drive: Any,
    file_id: str,
    dest_path: str | os.PathLike,
    *,
    export_mime_type: str | None = None,
) -> Path:
    """Download a file from Drive.

    Args:
        drive: Drive API Resource
        file_id: ID of file to download
        dest_path: Local destination path
        export_mime_type: For Google Docs/Sheets/Slides, export as this type
            (e.g., 'application/pdf', 'text/csv'). If None and file is a
            Google Workspace file, raises an error.

    Returns:
        Path to the downloaded file.
    """
    dest = Path(dest_path)
    dest.parent.mkdir(parents=True, exist_ok=True)

    try:
        # Get file metadata to check if it's a Google Workspace file
        meta = drive.files().get(fileId=file_id, fields="mimeType, name").execute()
        file_mime = meta.get("mimeType", "")

        is_workspace_file = file_mime.startswith("application/vnd.google-apps.")

        if is_workspace_file:
            if not export_mime_type:
                raise ValueError(
                    f"File '{meta.get('name')}' is a Google Workspace file ({file_mime}). "
                    "Specify export_mime_type (e.g., 'application/pdf', 'text/csv')."
                )
            request = drive.files().export_media(
                fileId=file_id, mimeType=export_mime_type
            )
        else:
            request = drive.files().get_media(fileId=file_id)

        with open(dest, "wb") as f:
            downloader = MediaIoBaseDownload(f, request)
            done = False
            while not done:
                _, done = downloader.next_chunk()

    except HttpError as e:
        raise_for_http_error(e)

    return dest


def _update_file(
    drive: Any,
    file_id: str,
    local_path: Path,
    mime_type: str | None = None,
) -> str:
    """Update an existing file's content (internal helper)."""
    detected_mime = (
        mime_type
        or mimetypes.guess_type(str(local_path))[0]
        or "application/octet-stream"
    )
    media = MediaFileUpload(str(local_path), mimetype=detected_mime, resumable=True)

    try:
        result = (
            drive.files()
            .update(fileId=file_id, media_body=media, fields="id")
            .execute()
        )
        return result["id"]
    except HttpError as e:
        raise_for_http_error(e)
        raise  # unreachable but satisfies type checker


def sync_folder(
    drive: Any,
    local_path: str | os.PathLike,
    drive_folder_id: str,
) -> dict:
    """Sync a local folder to a Drive folder.

    Uploads new files and updates changed files (by comparing modified times).
    Does not delete remote files that are missing locally (safe sync).

    Args:
        drive: Drive API Resource
        local_path: Local folder to sync
        drive_folder_id: Target Drive folder ID

    Returns:
        Summary dict: {created: int, updated: int, skipped: int, errors: list[str]}
    """
    local_dir = Path(local_path)
    if not local_dir.is_dir():
        raise NotADirectoryError(f"Not a directory: {local_dir}")

    # Get existing files in Drive folder
    remote_files = list_files(drive, parent_id=drive_folder_id)
    remote_by_name: dict[str, dict] = {f["name"]: f for f in remote_files}

    created = 0
    updated = 0
    skipped = 0
    errors: list[str] = []

    # Iterate local files (non-recursive for now)
    for item in local_dir.iterdir():
        if item.is_dir():
            # Skip subdirectories for v0.1 (could recurse later)
            continue

        try:
            if item.name in remote_by_name:
                # File exists remotely — check if update needed
                remote = remote_by_name[item.name]
                remote_modified = remote.get("modifiedTime", "")
                local_modified = item.stat().st_mtime

                # Parse remote time (ISO format) and compare
                # Simple heuristic: always update if local is newer
                from datetime import datetime, timezone

                try:
                    remote_dt = datetime.fromisoformat(
                        remote_modified.replace("Z", "+00:00")
                    )
                    local_dt = datetime.fromtimestamp(local_modified, tz=timezone.utc)

                    if local_dt > remote_dt:
                        _update_file(drive, remote["id"], item)
                        updated += 1
                    else:
                        skipped += 1
                except (ValueError, KeyError):
                    # Can't parse time, update to be safe
                    _update_file(drive, remote["id"], item)
                    updated += 1
            else:
                # New file — upload
                upload_file(drive, item, parent_id=drive_folder_id)
                created += 1

        except Exception as e:
            errors.append(f"{item.name}: {e}")

    return {
        "created": created,
        "updated": updated,
        "skipped": skipped,
        "errors": errors,
    }
