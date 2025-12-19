"""Google Drive wrapper — upload, download, list, sync."""

from __future__ import annotations

import mimetypes
import os
from pathlib import Path
from typing import Any

from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload

from mygooglib.exceptions import raise_for_http_error
from mygooglib.utils.logging import get_logger
from mygooglib.utils.retry import execute_with_retry_http_error

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
    max_results: int | None = None,
    fields: str = DEFAULT_FIELDS,
) -> list[dict]:
    """List files matching criteria with pagination.

    Args:
        drive: Drive API Resource from get_clients().drive
        query: Raw query string (combined with other filters via AND)
        parent_id: Filter to files in this folder
        mime_type: Filter by MIME type
        trashed: Include trashed files (default False)
        page_size: Results per page (max 1000)
        max_results: If provided, stop fetching after this many results.
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
            # If we have max_results, don't ask for more than we need in this page
            current_page_size = page_size
            if max_results is not None:
                remaining = max_results - len(all_files)
                if remaining <= 0:
                    break
                current_page_size = min(page_size, remaining)

            request = drive.files().list(
                q=q,
                pageSize=current_page_size,
                pageToken=page_token,
                fields=f"nextPageToken, files({fields})",
            )
            response = execute_with_retry_http_error(request, is_write=False)
            files = response.get("files", [])
            all_files.extend(files)

            page_token = response.get("nextPageToken")
            if not page_token:
                break

            if max_results is not None and len(all_files) >= max_results:
                break

    except HttpError as e:
        raise_for_http_error(e, context="Drive list_files")

    # Final slice just in case the API returned more than pageSize
    return all_files[:max_results] if max_results is not None else all_files


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
    raw: bool = False,
) -> str | dict:
    """Create a folder in Drive.

    Args:
        drive: Drive API Resource
        name: Folder name
        parent_id: Parent folder ID (None = root)

    Returns:
        The new folder's ID by default. If raw=True, returns the full API response.
    """
    metadata: dict = {
        "name": name,
        "mimeType": FOLDER_MIME_TYPE,
    }
    if parent_id:
        metadata["parents"] = [parent_id]

    try:
        request = drive.files().create(body=metadata, fields="id")
        folder = execute_with_retry_http_error(request, is_write=True)
        return folder if raw else folder["id"]
    except HttpError as e:
        raise_for_http_error(e, context="Drive create_folder")
        raise  # unreachable but satisfies type checker


def resolve_path(
    drive: Any,
    path: str,
    *,
    parent_id: str = "root",
) -> dict | None:
    """Resolve a human-readable path string to Drive file metadata.

    Supports forward-slash separated paths like 'Folder/Subfolder/File.txt'.
    Traverses the hierarchy from top to bottom.

    Args:
        drive: Drive API Resource
        path: Path string to resolve
        parent_id: Root folder ID to start from (default 'root')

    Returns:
        File metadata dict for the final path component, or None if not found.
    """
    parts = [p.strip() for p in path.split("/") if p.strip()]
    if not parts:
        return None

    # Skip 'root' if it's the first part and we're starting from root
    if parts[0].lower() == "root" and parent_id == "root":
        parts = parts[1:]
        if not parts:
            # If path was just 'root', return root metadata (minimal)
            return {"id": "root", "name": "root", "mimeType": FOLDER_MIME_TYPE}

    current_parent = parent_id
    current_meta = None

    for i, part in enumerate(parts):
        # Search for this part in the current parent
        # If it's the last part, we don't restrict mime_type to folder.
        # Otherwise, we expect it to be a folder (mostly).
        escaped_part = part.replace("'", "\\'")
        results = list_files(
            drive,
            query=f"name = '{escaped_part}'",
            parent_id=current_parent,
            trashed=False,
        )

        if not results:
            return None

        # Take the first match
        current_meta = results[0]
        current_parent = current_meta["id"]

        # If we have more parts to resolve, the current one MUST be a folder.
        if i < len(parts) - 1 and current_meta["mimeType"] != FOLDER_MIME_TYPE:
            return None

    return current_meta


def upload_file(
    drive: Any,
    local_path: str | os.PathLike,
    *,
    parent_id: str | None = None,
    name: str | None = None,
    mime_type: str | None = None,
    raw: bool = False,
    progress_callback: Any | None = None,
) -> str | dict:
    """Upload a local file to Drive.

    Args:
        drive: Drive API Resource
        local_path: Path to local file
        parent_id: Destination folder ID (None = root)
        name: Name in Drive (None = use local filename)
        mime_type: Override MIME type (None = auto-detect)
        progress_callback: Optional callable(bytes_sent, total_bytes)

    Returns:
        The uploaded file's ID by default. If raw=True, returns the full API response.
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
        request = drive.files().create(body=metadata, media_body=media, fields="id")

        if progress_callback:
            response = None
            while response is None:
                status, response = request.next_chunk()
                if status:
                    progress_callback(status.resumable_progress, status.total_size)
            result = response
        else:
            result = execute_with_retry_http_error(request, is_write=True)

        return result if raw else result["id"]
    except HttpError as e:
        raise_for_http_error(e, context="Drive upload_file")
        raise  # unreachable but satisfies type checker


def download_file(
    drive: Any,
    file_id: str,
    dest_path: str | os.PathLike,
    *,
    export_mime_type: str | None = None,
    progress_callback: Any | None = None,
) -> Path:
    """Download a file from Drive.

    Args:
        drive: Drive API Resource
        file_id: ID of file to download
        dest_path: Local destination path
        export_mime_type: For Google Docs/Sheets/Slides, export as this type
            (e.g., 'application/pdf', 'text/csv'). If None and file is a
            Google Workspace file, raises an error.
        progress_callback: Optional callable(bytes_received, total_bytes)

    Returns:
        Path to the downloaded file.
    """
    dest = Path(dest_path)
    dest.parent.mkdir(parents=True, exist_ok=True)

    try:
        # Get file metadata to check if it's a Google Workspace file
        meta_request = drive.files().get(fileId=file_id, fields="mimeType, name, size")
        meta = execute_with_retry_http_error(meta_request, is_write=False)
        file_mime = meta.get("mimeType", "")
        total_size = int(meta.get("size", 0))

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
                status, done = downloader.next_chunk()
                if progress_callback and status:
                    # For exports, total_size might be 0 or unknown from metadata
                    # but status.total_size might be available.
                    progress_callback(
                        status.resumable_progress, status.total_size or total_size
                    )

    except HttpError as e:
        raise_for_http_error(e, context="Drive download_file")

    return dest


def delete_file(
    drive: Any,
    file_id: str,
    *,
    permanent: bool = False,
) -> None:
    """Delete a file or move it to trash.

    Args:
        drive: Drive API Resource
        file_id: ID of file to delete
        permanent: If True, delete permanently. If False (default), move to trash.
    """
    try:
        if permanent:
            request = drive.files().delete(fileId=file_id)
        else:
            request = drive.files().update(fileId=file_id, body={"trashed": True})
        execute_with_retry_http_error(request, is_write=True)
    except HttpError as e:
        raise_for_http_error(e, context="Drive delete_file")


def _update_file(
    drive: Any,
    file_id: str,
    local_path: Path,
    mime_type: str | None = None,
) -> str:
    """Update an existing file's content (internal helper).

    Args:
        drive: Drive API Resource
        file_id: ID of the file to update
        local_path: Path to the new file content
        mime_type: Optional MIME type override

    Returns:
        The file ID of the updated file

    Raises:
        GoogleApiError: If the update fails
    """
    detected_mime = (
        mime_type
        or mimetypes.guess_type(str(local_path))[0]
        or "application/octet-stream"
    )
    media = MediaFileUpload(str(local_path), mimetype=detected_mime, resumable=True)

    try:
        request = drive.files().update(fileId=file_id, media_body=media, fields="id")
        result = execute_with_retry_http_error(request, is_write=True)
        return result["id"]
    except HttpError as e:
        raise_for_http_error(e, context="Drive _update_file")
        raise  # unreachable but satisfies type checker


def sync_folder(
    drive: Any,
    local_path: str | os.PathLike,
    drive_folder_id: str,
    *,
    recursive: bool = True,
    dry_run: bool = False,
    progress_callback: Any | None = None,
) -> dict:
    """Sync a local folder to a Drive folder.

    Uploads new files and updates changed files (by comparing modified times).
    Does not delete remote files that are missing locally (safe sync).

    Args:
        drive: Drive API Resource
        local_path: Local folder to sync
        drive_folder_id: Target Drive folder ID
        recursive: If True (default), sync subfolders recursively.
        dry_run: If True, don't actually perform any changes.
        progress_callback: Optional callable(current_count, total_count, item_name)

    Returns:
        Summary dict: {created: int, updated: int, skipped: int, errors: list[str]}
    """
    local_dir = Path(local_path)
    if not local_dir.is_dir():
        raise NotADirectoryError(f"Not a directory: {local_dir}")

    created = 0
    updated = 0
    skipped = 0
    errors: list[str] = []
    logger = get_logger("mygooglib.drive")

    from datetime import datetime, timezone

    # Pre-scan to count total items for progress bar
    total_items = 0
    if progress_callback:
        for _ in local_dir.rglob("*") if recursive else local_dir.iterdir():
            total_items += 1

    current_item_idx = 0

    def _ensure_remote_folder(parent_id: str, name: str) -> str:
        nonlocal created
        # List once per lookup; keeps behavior simple and predictable.
        existing = list_files(
            drive,
            parent_id=parent_id,
            mime_type=FOLDER_MIME_TYPE,
        )
        for f in existing:
            if f.get("name") == name:
                return f["id"]

        if dry_run:
            created += 1
            return "DRY_RUN_FOLDER_ID"

        folder_id = create_folder(drive, name, parent_id=parent_id)
        created += 1
        return folder_id

    def _sync_dir(local_current: Path, remote_parent_id: str) -> None:
        nonlocal created, updated, skipped, errors, current_item_idx

        # Get existing items in this Drive folder.
        remote_items = list_files(drive, parent_id=remote_parent_id)
        remote_files_by_name: dict[str, dict] = {}
        remote_folders_by_name: dict[str, dict] = {}
        for item in remote_items:
            name = item.get("name")
            if not name:
                continue
            if item.get("mimeType") == FOLDER_MIME_TYPE:
                remote_folders_by_name.setdefault(name, item)
            else:
                remote_files_by_name.setdefault(name, item)

        for entry in local_current.iterdir():
            current_item_idx += 1
            if progress_callback:
                progress_callback(current_item_idx, total_items, entry.name)

            try:
                if entry.is_dir():
                    if not recursive:
                        continue

                    remote_folder = remote_folders_by_name.get(entry.name)
                    remote_folder_id = (
                        remote_folder.get("id")
                        if remote_folder
                        else _ensure_remote_folder(remote_parent_id, entry.name)
                    )
                    _sync_dir(entry, remote_folder_id)
                    continue

                # Local file
                remote = remote_files_by_name.get(entry.name)
                if remote:
                    remote_modified = remote.get("modifiedTime", "")
                    local_modified = entry.stat().st_mtime

                    try:
                        remote_dt = datetime.fromisoformat(
                            remote_modified.replace("Z", "+00:00")
                        )
                        local_dt = datetime.fromtimestamp(
                            local_modified, tz=timezone.utc
                        )

                        if local_dt > remote_dt:
                            if not dry_run:
                                _update_file(drive, remote["id"], entry)
                            updated += 1
                        else:
                            skipped += 1
                    except (ValueError, KeyError):
                        # Can't parse time, update to be safe.
                        if not dry_run:
                            _update_file(drive, remote["id"], entry)
                        updated += 1
                else:
                    if not dry_run:
                        upload_file(drive, entry, parent_id=remote_parent_id)
                    created += 1

            except Exception as e:
                error_msg = f"{entry.relative_to(local_dir)}: {e}"
                errors.append(error_msg)
                # Log errors as they occur so users can monitor progress
                logger.error("Sync error: %s", error_msg)

    _sync_dir(local_dir, drive_folder_id)

    return {
        "created": created,
        "updated": updated,
        "skipped": skipped,
        "errors": errors,
        "dry_run": dry_run,
    }


class DriveClient:
    """Simplified Google Drive API wrapper focusing on common operations."""

    def __init__(self, service: Any):
        """Initialize with an authorized Drive API service object."""
        self.service = service

    def list_files(
        self,
        *,
        query: str | None = None,
        parent_id: str | None = None,
        mime_type: str | None = None,
        trashed: bool = False,
        page_size: int = 100,
        max_results: int | None = None,
        fields: str = DEFAULT_FIELDS,
    ) -> list[dict]:
        """List files matching criteria with pagination."""
        return list_files(
            self.service,
            query=query,
            parent_id=parent_id,
            mime_type=mime_type,
            trashed=trashed,
            page_size=page_size,
            max_results=max_results,
            fields=fields,
        )

    def find_by_name(
        self,
        name: str,
        *,
        parent_id: str | None = None,
        mime_type: str | None = None,
    ) -> dict | None:
        """Find first file with exact name."""
        return find_by_name(
            self.service,
            name,
            parent_id=parent_id,
            mime_type=mime_type,
        )

    def create_folder(
        self,
        name: str,
        *,
        parent_id: str | None = None,
        raw: bool = False,
    ) -> str | dict:
        """Create a folder in Drive."""
        return create_folder(
            self.service,
            name,
            parent_id=parent_id,
            raw=raw,
        )

    def upload_file(
        self,
        local_path: str | os.PathLike,
        *,
        parent_id: str | None = None,
        name: str | None = None,
        mime_type: str | None = None,
        raw: bool = False,
        progress_callback: Any | None = None,
    ) -> str | dict:
        """Upload a local file to Drive."""
        return upload_file(
            self.service,
            local_path,
            parent_id=parent_id,
            name=name,
            mime_type=mime_type,
            raw=raw,
            progress_callback=progress_callback,
        )

    def download_file(
        self,
        file_id: str,
        dest_path: str | os.PathLike,
        *,
        export_mime_type: str | None = None,
        progress_callback: Any | None = None,
    ) -> Path:
        """Download a file from Drive."""
        return download_file(
            self.service,
            file_id,
            dest_path,
            export_mime_type=export_mime_type,
            progress_callback=progress_callback,
        )

    def delete_file(
        self,
        file_id: str,
        *,
        permanent: bool = False,
    ) -> None:
        """Delete a file or move it to trash."""
        return delete_file(
            self.service,
            file_id,
            permanent=permanent,
        )

    def sync_folder(
        self,
        local_path: str | os.PathLike,
        drive_folder_id: str,
        *,
        recursive: bool = True,
        dry_run: bool = False,
        progress_callback: Any | None = None,
    ) -> dict:
        """Sync a local folder to a Drive folder."""
        return sync_folder(
            self.service,
            local_path,
            drive_folder_id,
            recursive=recursive,
            dry_run=dry_run,
            progress_callback=progress_callback,
        )

    def resolve_path(
        self,
        path: str,
        *,
        parent_id: str = "root",
    ) -> dict | None:
        """Resolve a human-readable path string to Drive file metadata."""
        return resolve_path(self.service, path, parent_id=parent_id)
