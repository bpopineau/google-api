"""Base classes for Google API client wrappers."""

from __future__ import annotations

from typing import Any


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

