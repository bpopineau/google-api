"""
Google Drive API wrapper.

Provides a Pythonic interface for Drive file operations.
"""

import mimetypes
import os
from pathlib import Path
from typing import BinaryIO

from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload

from goog.auth import GoogleAuth
from goog.utils import logger, with_retry


class DriveClient:
    """
    Pythonic wrapper for Google Drive API.

    Provides intuitive methods for common Drive operations:
    - Upload/download files
    - List and search files
    - Create folders
    - Copy and delete files

    Example:
        >>> from goog import GoogleAuth, DriveClient
        >>> auth = GoogleAuth()
        >>> drive = DriveClient(auth)
        >>> file_id = drive.upload_file("report.pdf", name="Monthly Report")
        >>> print(f"Uploaded with ID: {file_id}")
    """

    FOLDER_MIME_TYPE = "application/vnd.google-apps.folder"

    def __init__(self, auth: GoogleAuth):
        """
        Initialize the Drive client.

        Args:
            auth: GoogleAuth instance for authentication.
        """
        self._auth = auth
        self._service = None

    @property
    def service(self):
        """Lazily initialize and return the Drive service."""
        if self._service is None:
            self._service = self._auth.build_service("drive", "v3")
        return self._service

    @with_retry()
    def upload_file(
        self,
        local_path: str | Path,
        parent_id: str | None = None,
        name: str | None = None,
        mime_type: str | None = None,
    ) -> str:
        """
        Upload a local file to Google Drive.

        Args:
            local_path: Path to the local file to upload.
            parent_id: Optional ID of the parent folder.
            name: Optional name for the file in Drive.
                  Defaults to the local filename.
            mime_type: Optional MIME type. Auto-detected if not provided.

        Returns:
            The file ID of the uploaded file.

        Example:
            >>> drive.upload_file("data.csv", parent_id="folder123")
            'abc123xyz'
        """
        local_path = Path(local_path)
        if not local_path.exists():
            raise FileNotFoundError(f"Local file not found: {local_path}")

        file_name = name or local_path.name
        detected_mime = mime_type or mimetypes.guess_type(str(local_path))[0]

        # Build file metadata
        file_metadata = {"name": file_name}
        if parent_id:
            file_metadata["parents"] = [parent_id]

        # Create media object for upload
        media = MediaFileUpload(
            str(local_path),
            mimetype=detected_mime,
            resumable=True,
        )

        logger.info(f"Uploading {file_name} to Drive")
        result = (
            self.service.files()
            .create(body=file_metadata, media_body=media, fields="id")
            .execute()
        )

        file_id = result.get("id")
        logger.debug(f"Upload complete, file ID: {file_id}")
        return file_id

    @with_retry()
    def download_file(
        self,
        file_id: str,
        local_path: str | Path,
    ) -> Path:
        """
        Download a file from Google Drive.

        Args:
            file_id: The ID of the file to download.
            local_path: Path where the file should be saved.

        Returns:
            Path to the downloaded file.

        Example:
            >>> drive.download_file("abc123", "downloaded.pdf")
            PosixPath('downloaded.pdf')
        """
        local_path = Path(local_path)
        local_path.parent.mkdir(parents=True, exist_ok=True)

        logger.info(f"Downloading file {file_id} to {local_path}")

        request = self.service.files().get_media(fileId=file_id)

        with open(local_path, "wb") as fh:
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while not done:
                status, done = downloader.next_chunk()
                if status:
                    logger.debug(f"Download progress: {int(status.progress() * 100)}%")

        logger.debug("Download complete")
        return local_path

    @with_retry()
    def list_files(
        self,
        query: str | None = None,
        parent_id: str | None = None,
        page_size: int = 100,
        max_results: int | None = None,
    ) -> list[dict]:
        """
        List files in Google Drive.

        Args:
            query: Optional query string in Drive query syntax.
            parent_id: Optional parent folder ID to list contents of.
            page_size: Number of files per page (max 1000).
            max_results: Maximum total results to return.

        Returns:
            List of file metadata dictionaries with id, name, mimeType, etc.

        Example:
            >>> files = drive.list_files(parent_id="folder123")
            >>> for f in files:
            ...     print(f"{f['name']} ({f['id']})")
        """
        # Build query
        query_parts = []
        if query:
            query_parts.append(query)
        if parent_id:
            query_parts.append(f"'{parent_id}' in parents")
        query_parts.append("trashed = false")  # Exclude trashed by default

        full_query = " and ".join(query_parts)

        logger.debug(f"Listing files with query: {full_query}")

        all_files = []
        page_token = None

        while True:
            response = (
                self.service.files()
                .list(
                    q=full_query,
                    pageSize=min(page_size, 1000),
                    pageToken=page_token,
                    fields="nextPageToken, files(id, name, mimeType, size, createdTime, modifiedTime, parents)",
                )
                .execute()
            )

            files = response.get("files", [])
            all_files.extend(files)

            # Check if we've reached max_results
            if max_results and len(all_files) >= max_results:
                all_files = all_files[:max_results]
                break

            page_token = response.get("nextPageToken")
            if not page_token:
                break

        logger.info(f"Found {len(all_files)} files")
        return all_files

    @with_retry()
    def find_file(
        self,
        name: str,
        parent_id: str | None = None,
    ) -> dict | None:
        """
        Find a file by exact name.

        Args:
            name: Exact filename to search for.
            parent_id: Optional parent folder to search within.

        Returns:
            File metadata dict if found, None otherwise.

        Example:
            >>> file = drive.find_file("report.pdf")
            >>> if file:
            ...     print(f"Found: {file['id']}")
        """
        query = f"name = '{name}'"
        files = self.list_files(query=query, parent_id=parent_id, max_results=1)
        return files[0] if files else None

    @with_retry()
    def create_folder(
        self,
        name: str,
        parent_id: str | None = None,
    ) -> str:
        """
        Create a folder in Google Drive.

        Args:
            name: Name of the folder to create.
            parent_id: Optional parent folder ID.

        Returns:
            The folder ID.

        Example:
            >>> folder_id = drive.create_folder("Projects")
            >>> drive.upload_file("doc.pdf", parent_id=folder_id)
        """
        file_metadata = {
            "name": name,
            "mimeType": self.FOLDER_MIME_TYPE,
        }
        if parent_id:
            file_metadata["parents"] = [parent_id]

        logger.info(f"Creating folder: {name}")
        result = self.service.files().create(body=file_metadata, fields="id").execute()

        folder_id = result.get("id")
        logger.debug(f"Created folder with ID: {folder_id}")
        return folder_id

    @with_retry()
    def delete_file(self, file_id: str) -> None:
        """
        Permanently delete a file or folder.

        Args:
            file_id: ID of the file/folder to delete.

        Warning:
            This permanently deletes the file. Use `trash_file` to move
            to trash instead.

        Example:
            >>> drive.delete_file("abc123")
        """
        logger.info(f"Deleting file: {file_id}")
        self.service.files().delete(fileId=file_id).execute()
        logger.debug("Delete complete")

    @with_retry()
    def trash_file(self, file_id: str) -> None:
        """
        Move a file to trash.

        Args:
            file_id: ID of the file to trash.

        Example:
            >>> drive.trash_file("abc123")
        """
        logger.info(f"Moving file to trash: {file_id}")
        self.service.files().update(
            fileId=file_id,
            body={"trashed": True},
        ).execute()
        logger.debug("Moved to trash")

    @with_retry()
    def copy_file(
        self,
        file_id: str,
        new_name: str | None = None,
        parent_id: str | None = None,
    ) -> str:
        """
        Copy a file.

        Args:
            file_id: ID of the file to copy.
            new_name: Optional new name for the copy.
            parent_id: Optional destination folder ID.

        Returns:
            The new file ID.

        Example:
            >>> new_id = drive.copy_file("abc123", new_name="Copy of Report")
        """
        body = {}
        if new_name:
            body["name"] = new_name
        if parent_id:
            body["parents"] = [parent_id]

        logger.info(f"Copying file: {file_id}")
        result = (
            self.service.files().copy(fileId=file_id, body=body, fields="id").execute()
        )

        new_file_id = result.get("id")
        logger.debug(f"Copy created with ID: {new_file_id}")
        return new_file_id

    @with_retry()
    def get_file(self, file_id: str) -> dict:
        """
        Get file metadata.

        Args:
            file_id: ID of the file.

        Returns:
            File metadata dictionary.

        Example:
            >>> info = drive.get_file("abc123")
            >>> print(info['name'], info['mimeType'])
        """
        return (
            self.service.files()
            .get(
                fileId=file_id,
                fields="id, name, mimeType, size, createdTime, modifiedTime, parents, webViewLink",
            )
            .execute()
        )
