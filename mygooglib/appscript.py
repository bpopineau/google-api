"""Google Apps Script wrapper — run functions from deployed scripts.

This module allows you to execute Apps Script functions from Python.
Requires a deployed Apps Script project with the script ID.
"""

from __future__ import annotations

from typing import Any

from googleapiclient.errors import HttpError

from mygooglib.exceptions import raise_for_http_error
from mygooglib.utils.retry import execute_with_retry_http_error


def run_function(
    script_service: Any,
    script_id: str,
    function_name: str,
    parameters: list[Any] | None = None,
    *,
    dev_mode: bool = False,
) -> Any:
    """Execute a function in a deployed Apps Script project.

    Args:
        script_service: Apps Script API Resource
        script_id: The Apps Script project ID (from script URL or manifest)
        function_name: Name of the function to execute
        parameters: List of parameters to pass to the function
        dev_mode: If True, run in development mode (uses most recent save)

    Returns:
        The return value from the Apps Script function.

    Raises:
        HttpError: If the API call fails.
        RuntimeError: If the script execution fails.

    Notes:
        - The script must be deployed as an API executable.
        - The OAuth token must have the required scopes for the script.
        - Script ID can be found in Project Settings or the script URL.
    """
    request_body = {
        "function": function_name,
        "devMode": dev_mode,
    }
    if parameters:
        request_body["parameters"] = parameters

    try:
        request = script_service.scripts().run(scriptId=script_id, body=request_body)
        response = execute_with_retry_http_error(request, is_write=True)
    except HttpError as e:
        raise_for_http_error(e, context="Apps Script run_function")
        raise

    # Check for script execution errors
    if "error" in response:
        error = response["error"]
        error_message = error.get("message", "Unknown script error")
        error_details = error.get("details", [])
        script_stack = ""
        for detail in error_details:
            if "scriptStackTraceElements" in detail:
                frames = detail["scriptStackTraceElements"]
                script_stack = "\n".join(
                    f"  {f.get('function', '?')} ({f.get('lineNumber', '?')})"
                    for f in frames
                )
        raise RuntimeError(
            f"Apps Script error: {error_message}"
            + (f"\nStack trace:\n{script_stack}" if script_stack else "")
        )

    return response.get("response", {}).get("result")


class AppScriptClient:
    """Simplified Apps Script API wrapper."""

    def __init__(self, service: Any):
        """Initialize with an authorized Apps Script API service object."""
        self.service = service

    def run(
        self,
        script_id: str,
        function_name: str,
        parameters: list[Any] | None = None,
        *,
        dev_mode: bool = False,
    ) -> Any:
        """Execute a function in a deployed Apps Script project.

        Args:
            script_id: The Apps Script project ID
            function_name: Name of the function to execute
            parameters: List of parameters to pass to the function
            dev_mode: If True, run in development mode

        Returns:
            The return value from the Apps Script function.
        """
        return run_function(
            self.service,
            script_id,
            function_name,
            parameters,
            dev_mode=dev_mode,
        )
