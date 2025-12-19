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
