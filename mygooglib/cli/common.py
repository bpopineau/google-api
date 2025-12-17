from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import typer
from rich.console import Console
from rich.text import Text


@dataclass(frozen=True)
class CliState:
    console: Console
    err_console: Console
    debug: bool
    json: bool
    creds_path: Path | None = None
    token_path: Path | None = None

    @staticmethod
    def from_ctx(ctx: typer.Context) -> "CliState":
        obj = getattr(ctx, "obj", None)
        if not isinstance(obj, CliState):
            raise RuntimeError("CLI state not initialized")
        return obj


def configure_environment(state: CliState) -> None:
    if state.creds_path is not None:
        os.environ["MYGOOGLIB_CREDENTIALS_PATH"] = str(state.creds_path)
    if state.token_path is not None:
        os.environ["MYGOOGLIB_TOKEN_PATH"] = str(state.token_path)

    if state.debug:
        os.environ.setdefault("MYGOOGLIB_DEBUG", "1")


def format_output(value: Any, *, json_mode: bool) -> str:
    if not json_mode:
        return str(value)
    return json.dumps(value, indent=2, sort_keys=True, default=str)


def print_error(console: Console, message: str) -> None:
    console.print(Text(message, style="bold red"))


def print_success(console: Console, message: str) -> None:
    console.print(Text(message, style="green"))


def print_kv(console: Console, key: str, value: Any) -> None:
    console.print(Text(f"{key}: ", style="bold") + Text(str(value)))
