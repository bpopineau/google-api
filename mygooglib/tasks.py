"""Google Tasks wrapper — list_tasklists, add_task, list_tasks, complete_task.

These helpers take the raw Tasks v1 Resource from `get_clients().tasks`.
They return plain Python types by default, with a `raw=True` escape hatch.
"""

from __future__ import annotations

import datetime as dt
from typing import Any

from googleapiclient.errors import HttpError

from mygooglib.exceptions import raise_for_http_error
from mygooglib.utils.datetime import to_rfc3339
from mygooglib.utils.retry import execute_with_retry_http_error


def list_tasklists(
    tasks: Any,
    *,
    max_results: int = 100,
    raw: bool = False,
) -> list[dict] | dict:
    """List the user's task lists.

    Args:
        tasks: Tasks API Resource from get_clients().tasks
        max_results: Maximum number of task lists to return
        raw: If True, return full API response dict

    Returns:
        List of task list dicts by default, or full response if raw=True.
    """
    try:
        request = tasks.tasklists().list(maxResults=max_results)
        response = execute_with_retry_http_error(request, is_write=False)
    except HttpError as e:
        raise_for_http_error(e, context="Tasks list_tasklists")
        raise

    return response if raw else response.get("items", [])


def add_task(
    tasks: Any,
    *,
    title: str,
    tasklist_id: str = "@default",
    notes: str | None = None,
    due: dt.datetime | dt.date | None = None,
    raw: bool = False,
) -> str | dict:
    """Add a task to a task list.

    Args:
        tasks: Tasks API Resource
        title: Task title
        tasklist_id: Task list ID (default "@default")
        notes: Optional task notes
        due: Optional due date/datetime
        raw: If True, return full API response dict

    Returns:
        Task ID string by default, or full response if raw=True.
    """
    body: dict[str, Any] = {"title": title}
    if notes:
        body["notes"] = notes
    if due:
        # Tasks API expects RFC3339 timestamp for due date
        body["due"] = to_rfc3339(due)

    try:
        request = tasks.tasks().insert(tasklist=tasklist_id, body=body)
        response = execute_with_retry_http_error(request, is_write=True)
    except HttpError as e:
        raise_for_http_error(e, context="Tasks add_task")
        raise

    return response if raw else response.get("id")


def list_tasks(
    tasks: Any,
    *,
    tasklist_id: str = "@default",
    show_completed: bool = True,
    show_hidden: bool = False,
    max_results: int = 100,
    raw: bool = False,
    progress_callback: Any | None = None,
) -> list[dict] | dict:
    """List tasks in a task list.

    Args:
        tasks: Tasks API Resource
        tasklist_id: Task list ID (default "@default")
        show_completed: Include completed tasks
        show_hidden: Include hidden tasks
        max_results: Maximum number of tasks to return
        raw: If True, return full API response dict
        progress_callback: Optional callback(count) for progress tracking.

    Returns:
        List of task dicts by default, or full response if raw=True.
    """
    all_items = []
    page_token = None

    try:
        while True:
            request = tasks.tasks().list(
                tasklist=tasklist_id,
                showCompleted=show_completed,
                showHidden=show_hidden,
                maxResults=min(max_results - len(all_items), 100)
                if max_results
                else 100,
                pageToken=page_token,
            )
            response = execute_with_retry_http_error(request, is_write=False)
            items = response.get("items", [])
            all_items.extend(items)

            if progress_callback:
                progress_callback(len(items))

            page_token = response.get("nextPageToken")
            if not page_token or (max_results and len(all_items) >= max_results):
                break

    except HttpError as e:
        raise_for_http_error(e, context="Tasks list_tasks")
        raise

    if raw:
        return {"items": all_items}
    return all_items


def complete_task(
    tasks: Any,
    task_id: str,
    *,
    tasklist_id: str = "@default",
    raw: bool = False,
) -> dict | None:
    """Mark a task as completed."""
    try:
        # We must first get the task to have its current state,
        # then update status to 'completed'.
        # Actually, patch is better.
        body = {"status": "completed"}
        request = tasks.tasks().patch(tasklist=tasklist_id, task=task_id, body=body)
        response = execute_with_retry_http_error(request, is_write=True)
    except HttpError as e:
        raise_for_http_error(e, context="Tasks complete_task")
        raise

    return response if raw else None


def delete_task(
    tasks: Any,
    task_id: str,
    *,
    tasklist_id: str = "@default",
) -> None:
    """Delete a task from a task list."""
    try:
        request = tasks.tasks().delete(tasklist=tasklist_id, task=task_id)
        execute_with_retry_http_error(request, is_write=True)
    except HttpError as e:
        raise_for_http_error(e, context="Tasks delete_task")
        raise


class TasksClient:
    """Simplified Google Tasks API wrapper focusing on common operations."""

    def __init__(self, service: Any):
        """Initialize with an authorized Tasks API service object."""
        self.service = service

    def list_tasklists(
        self, *, max_results: int = 100, raw: bool = False
    ) -> list[dict] | dict:
        """List the user's task lists."""
        return list_tasklists(self.service, max_results=max_results, raw=raw)

    def add_task(
        self,
        *,
        title: str,
        tasklist_id: str = "@default",
        notes: str | None = None,
        due: dt.datetime | dt.date | None = None,
        raw: bool = False,
    ) -> str | dict:
        """Add a task to a task list."""
        return add_task(
            self.service,
            title=title,
            tasklist_id=tasklist_id,
            notes=notes,
            due=due,
            raw=raw,
        )

    def list_tasks(
        self,
        *,
        tasklist_id: str = "@default",
        show_completed: bool = True,
        show_hidden: bool = False,
        max_results: int = 100,
        raw: bool = False,
        progress_callback: Any | None = None,
    ) -> list[dict] | dict:
        """List tasks in a task list."""
        return list_tasks(
            self.service,
            tasklist_id=tasklist_id,
            show_completed=show_completed,
            show_hidden=show_hidden,
            max_results=max_results,
            raw=raw,
            progress_callback=progress_callback,
        )

    def complete_task(
        self,
        task_id: str,
        *,
        tasklist_id: str = "@default",
        raw: bool = False,
    ) -> dict | None:
        """Mark a task as completed."""
        return complete_task(
            self.service,
            task_id,
            tasklist_id=tasklist_id,
            raw=raw,
        )

    def delete_task(
        self,
        task_id: str,
        *,
        tasklist_id: str = "@default",
    ) -> None:
        """Delete a task from a task list."""
        return delete_task(self.service, task_id, tasklist_id=tasklist_id)
