"""
Google Tasks API wrapper.

Provides a Pythonic interface for task management.
"""

from datetime import date, datetime, timezone

from goog.auth import GoogleAuth
from goog.utils import logger, with_retry


class TasksClient:
    """
    Pythonic wrapper for Google Tasks API.

    Provides intuitive methods for task management:
    - List and manage task lists
    - Add, complete, and delete tasks
    - Handle due dates

    Example:
        >>> from goog import GoogleAuth, TasksClient
        >>> from datetime import date
        >>> auth = GoogleAuth()
        >>> tasks = TasksClient(auth)
        >>> tasks.add_task("Buy groceries", due=date(2024, 1, 20))
    """

    DEFAULT_TASKLIST = "@default"

    def __init__(self, auth: GoogleAuth):
        """
        Initialize the Tasks client.

        Args:
            auth: GoogleAuth instance for authentication.
        """
        self._auth = auth
        self._service = None

    @property
    def service(self):
        """Lazily initialize and return the Tasks service."""
        if self._service is None:
            self._service = self._auth.build_service("tasks", "v1")
        return self._service

    @with_retry()
    def list_tasklists(self) -> list[dict]:
        """
        List all task lists.

        Returns:
            List of task list dictionaries with id, title, etc.

        Example:
            >>> lists = tasks.list_tasklists()
            >>> for lst in lists:
            ...     print(lst['title'], lst['id'])
        """
        result = self.service.tasklists().list().execute()
        items = result.get("items", [])
        logger.info(f"Found {len(items)} task lists")
        return items

    @with_retry()
    def create_tasklist(self, title: str) -> str:
        """
        Create a new task list.

        Args:
            title: Title for the new task list.

        Returns:
            The task list ID.

        Example:
            >>> list_id = tasks.create_tasklist("Work Tasks")
        """
        logger.info(f"Creating task list: {title}")
        result = self.service.tasklists().insert(body={"title": title}).execute()
        list_id = result.get("id")
        logger.debug(f"Created task list with ID: {list_id}")
        return list_id

    @with_retry()
    def delete_tasklist(self, tasklist_id: str) -> None:
        """
        Delete a task list.

        Args:
            tasklist_id: The task list ID to delete.
        """
        logger.info(f"Deleting task list: {tasklist_id}")
        self.service.tasklists().delete(tasklist=tasklist_id).execute()

    @with_retry()
    def list_tasks(
        self,
        tasklist_id: str = "@default",
        show_completed: bool = False,
        show_hidden: bool = False,
        max_results: int = 100,
    ) -> list[dict]:
        """
        List tasks in a task list.

        Args:
            tasklist_id: Task list ID. Default "@default" for My Tasks.
            show_completed: Include completed tasks.
            show_hidden: Include hidden tasks.
            max_results: Maximum tasks to return.

        Returns:
            List of task dictionaries.

        Example:
            >>> tasks_list = tasks.list_tasks()
            >>> for task in tasks_list:
            ...     status = "✓" if task['status'] == 'completed' else "○"
            ...     print(f"{status} {task['title']}")
        """
        result = (
            self.service.tasks()
            .list(
                tasklist=tasklist_id,
                showCompleted=show_completed,
                showHidden=show_hidden,
                maxResults=max_results,
            )
            .execute()
        )
        items = result.get("items", [])
        logger.info(f"Found {len(items)} tasks")
        return items

    def _format_due(self, due: date | datetime) -> str:
        """Format a due date for the API (RFC 3339 timestamp)."""
        if isinstance(due, datetime):
            if due.tzinfo is None:
                due = due.replace(tzinfo=timezone.utc)
            return due.isoformat()
        else:
            # For date, set to midnight UTC
            dt = datetime.combine(due, datetime.min.time(), tzinfo=timezone.utc)
            return dt.isoformat()

    @with_retry()
    def add_task(
        self,
        title: str,
        tasklist_id: str = "@default",
        due: date | datetime | None = None,
        notes: str | None = None,
        parent: str | None = None,
    ) -> str:
        """
        Add a new task.

        Args:
            title: Task title.
            tasklist_id: Task list ID. Default "@default".
            due: Optional due date/datetime.
            notes: Optional task notes.
            parent: Optional parent task ID (for subtasks).

        Returns:
            The task ID.

        Example:
            >>> task_id = tasks.add_task(
            ...     "Review documents",
            ...     due=date(2024, 1, 20),
            ...     notes="Check the quarterly report"
            ... )
        """
        body = {"title": title}

        if due:
            body["due"] = self._format_due(due)
        if notes:
            body["notes"] = notes

        params = {"tasklist": tasklist_id, "body": body}
        if parent:
            params["parent"] = parent

        logger.info(f"Adding task: {title}")
        result = self.service.tasks().insert(**params).execute()
        task_id = result.get("id")
        logger.debug(f"Created task with ID: {task_id}")
        return task_id

    @with_retry()
    def get_task(self, task_id: str, tasklist_id: str = "@default") -> dict:
        """
        Get a task by ID.

        Args:
            task_id: The task ID.
            tasklist_id: Task list ID.

        Returns:
            Task dictionary.
        """
        return self.service.tasks().get(tasklist=tasklist_id, task=task_id).execute()

    @with_retry()
    def update_task(
        self,
        task_id: str,
        tasklist_id: str = "@default",
        title: str | None = None,
        due: date | datetime | None = None,
        notes: str | None = None,
    ) -> dict:
        """
        Update an existing task.

        Args:
            task_id: The task ID to update.
            tasklist_id: Task list ID.
            title: New title (optional).
            due: New due date (optional).
            notes: New notes (optional).

        Returns:
            Updated task dictionary.
        """
        task = self.get_task(task_id, tasklist_id)

        if title is not None:
            task["title"] = title
        if due is not None:
            task["due"] = self._format_due(due)
        if notes is not None:
            task["notes"] = notes

        logger.info(f"Updating task: {task_id}")
        return (
            self.service.tasks()
            .update(tasklist=tasklist_id, task=task_id, body=task)
            .execute()
        )

    @with_retry()
    def complete_task(self, task_id: str, tasklist_id: str = "@default") -> dict:
        """
        Mark a task as completed.

        Args:
            task_id: The task ID.
            tasklist_id: Task list ID.

        Returns:
            Updated task dictionary.

        Example:
            >>> tasks.complete_task("abc123")
        """
        task = self.get_task(task_id, tasklist_id)
        task["status"] = "completed"

        logger.info(f"Completing task: {task_id}")
        return (
            self.service.tasks()
            .update(tasklist=tasklist_id, task=task_id, body=task)
            .execute()
        )

    @with_retry()
    def uncomplete_task(self, task_id: str, tasklist_id: str = "@default") -> dict:
        """
        Mark a completed task as not completed.

        Args:
            task_id: The task ID.
            tasklist_id: Task list ID.

        Returns:
            Updated task dictionary.
        """
        task = self.get_task(task_id, tasklist_id)
        task["status"] = "needsAction"
        task.pop("completed", None)

        logger.info(f"Uncompleting task: {task_id}")
        return (
            self.service.tasks()
            .update(tasklist=tasklist_id, task=task_id, body=task)
            .execute()
        )

    @with_retry()
    def delete_task(self, task_id: str, tasklist_id: str = "@default") -> None:
        """
        Delete a task.

        Args:
            task_id: The task ID to delete.
            tasklist_id: Task list ID.

        Example:
            >>> tasks.delete_task("abc123")
        """
        logger.info(f"Deleting task: {task_id}")
        self.service.tasks().delete(tasklist=tasklist_id, task=task_id).execute()

    @with_retry()
    def clear_completed(self, tasklist_id: str = "@default") -> None:
        """
        Clear all completed tasks from a task list.

        Args:
            tasklist_id: Task list ID.
        """
        logger.info(f"Clearing completed tasks from: {tasklist_id}")
        self.service.tasks().clear(tasklist=tasklist_id).execute()
