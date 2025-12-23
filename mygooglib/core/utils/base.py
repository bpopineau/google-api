"""Base classes for Google API client wrappers."""

from __future__ import annotations

from typing import Any

from mygooglib.core.types import DryRunReport


def make_dry_run_report(
    action: str,
    resource_id: str,
    details: dict[str, Any] | None = None,
    reason: str | None = None,
) -> DryRunReport:
    """Create a DryRunReport for a dry-run operation.

    This factory function ensures consistent structure across all dry-run
    operations in the library.

    Args:
        action: Operation identifier (e.g., "drive.delete", "sheets.update").
        resource_id: The ID or identifier of the affected resource.
        details: Dictionary of proposed changes. Defaults to empty dict.
        reason: Optional explanation for the operation.

    Returns:
        A DryRunReport TypedDict with the specified fields.

    Example:
        >>> report = make_dry_run_report(
        ...     "drive.delete",
        ...     "abc123",
        ...     {"file_name": "test.txt", "permanent": False}
        ... )
    """
    report: DryRunReport = {
        "action": action,
        "resource_id": resource_id,
        "details": details or {},
    }
    if reason is not None:
        report["reason"] = reason
    return report


class BaseClient:
    """Base class for Google API service wrappers.

    Provides common initialization pattern for all service clients.
    Subclasses store the raw API service and delegate to standalone functions.
    """

    def __init__(self, service: Any):
        """Initialize with an authorized Google API service object.

        Args:
            service: The raw API service Resource from googleapiclient.discovery.build()
        """
        self.service = service

    def __getattr__(self, name: str) -> Any:
        """Delegate attribute access to the underlying service resource.
        
        This allows the wrapper to be used both with its ergonomic methods
        AND as a direct proxy to the Google API Discovery resource (e.g., drive.files()).
        """
        return getattr(self.service, name)
