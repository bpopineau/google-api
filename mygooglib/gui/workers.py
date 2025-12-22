"""QThread workers for async API operations."""

from __future__ import annotations

from typing import Any, Callable

from PySide6.QtCore import QThread, Signal


class ApiWorker(QThread):
    """Base worker for running API calls off the main thread.

    Signals:
        finished: Emitted with the result when the operation completes successfully.
        error: Emitted with the exception if the operation fails.
        progress: Emitted with (current, total) for progress updates.
    """

    finished = Signal(object)
    error = Signal(Exception)
    progress = Signal(int, int)

    def __init__(
        self,
        func: Callable[..., Any],
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """Initialize the worker.

        Args:
            func: The function to call (typically an API method).
            *args: Positional arguments to pass to the function.
            **kwargs: Keyword arguments to pass to the function.
        """
        super().__init__()
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self._result: Any = None

    def run(self) -> None:
        """Execute the function in a separate thread."""
        try:
            self._result = self.func(*self.args, **self.kwargs)
            self.finished.emit(self._result)
        except Exception as e:
            self.error.emit(e)


class BatchApiWorker(ApiWorker):
    """Worker for batch operations with progress reporting."""

    def __init__(
        self,
        items: list[Any],
        process_func: Callable[[Any], Any],
    ) -> None:
        """Initialize the batch worker.

        Args:
            items: List of items to process.
            process_func: Function to call for each item.
        """
        super().__init__(self._process_all)
        self.items = items
        self.process_func = process_func
        self.results: list[Any] = []
        self.errors: list[tuple[int, Exception]] = []

    def _process_all(self) -> list[Any]:
        """Process all items, emitting progress along the way."""
        total = len(self.items)
        for i, item in enumerate(self.items):
            try:
                result = self.process_func(item)
                self.results.append(result)
            except Exception as e:
                self.errors.append((i, e))
            self.progress.emit(i + 1, total)
        return self.results


class SyncWorker(QThread):
    """Worker to coordinate scanning local files and syncing to Sheets.

    Signals:
        started_scan: Emitted when file scanning starts.
        started_upload: Emitted with total file count when upload starts.
        finished: Emitted when the entire sync completes.
        error: Emitted with error message if any step fails.
    """

    started_scan = Signal()
    started_upload = Signal(int)
    finished = Signal(dict)
    error = Signal(str)

    def __init__(
        self,
        clients: Any,
        directory: str,
        spreadsheet_id: str,
        sheet_name: str,
    ) -> None:
        super().__init__()
        self.clients = clients
        self.directory = directory
        self.spreadsheet_id = spreadsheet_id
        self.sheet_name = sheet_name

    def run(self) -> None:
        from mygooglib.utils.file_scanner import FileScanner

        try:
            # 1. Ensure spreadsheet exists
            spreadsheet_id = self.spreadsheet_id
            
            # Check if it exists (handles ID, Title, or URL)
            if not self.clients.sheets.exists(spreadsheet_id):
                # If it doesn't exist, we assume the input was intended to be a title
                # or it was a deleted ID. In both cases, we create a new one.
                # Use the provided spreadsheet_id as the title if it doesn't look like an ID,
                # otherwise maybe use a default name or just the ID string as title.
                title = spreadsheet_id
                # If it's a long ID that's missing, it's safer to use a descriptive name
                if len(title) > 40 and " " not in title:
                    title = f"Synced Metadata ({title[:8]})"
                
                spreadsheet_id = self.clients.sheets.create_spreadsheet(
                    title,
                    sheet_name=self.sheet_name,
                )

            # 2. Scan
            self.started_scan.emit()
            scanner = FileScanner()
            files = scanner.scan(self.directory)

            if not files:
                self.finished.emit({"updatedRows": 0, "message": "No files found"})
                return

            # 3. Prepare Data
            self.started_upload.emit(len(files))
            headers = ["Filename", "Path", "Last Modified"]
            rows = [
                [f["filename"], f["absolute_path"], str(f["last_modified_timestamp"])]
                for f in files
            ]

            # 4. Upload
            result = self.clients.sheets.batch_write(
                spreadsheet_id,
                self.sheet_name,
                rows,
                headers=headers,
                clear=True,
            )

            self.finished.emit(result or {"updatedRows": len(rows)})

        except Exception as e:
            self.error.emit(str(e))
