"""Developer CLI workflow automation Tools."""

from __future__ import annotations

import re
import shlex
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import typer
from rich import print as rprint
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="Developer workflow automation tools.")
console = Console()

TASK_FILE = Path("task.md")

# Regex patterns
TASK_PATTERN = re.compile(r"^(\s*)-\s*\[([ x/])\]\s*(.+)$")
CMD_PATTERN = re.compile(r"`([^`]+)`|\(([^)]+)\)")


@dataclass
class TaskItem:
    """Represents a single line item in task.md."""

    line_num: int
    raw_line: str
    indent: int
    state: str  # ' ', 'x', '/'
    text: str
    command: Optional[str] = None


def _get_task_file() -> Path:
    """Get path to task.md, looking in CWD or specific brain locations."""
    # For now, simpler: just use CWD.
    if not TASK_FILE.exists():
        # Fallback to brain dir if we are in a subfolder or something?
        # For this MVP, require running from root or where task.md is.
        pass
    return TASK_FILE


def _parse_tasks(path: Path) -> list[TaskItem]:
    """Parse task.md into a list of TaskItems."""
    if not path.exists():
        return []

    items = []
    lines = path.read_text("utf-8").splitlines()

    for i, line in enumerate(lines):
        match = TASK_PATTERN.match(line)
        if match:
            indent_str, state, text = match.groups()
            indent = len(indent_str)

            # Extract potential command
            cmd_match = CMD_PATTERN.search(text)
            if cmd_match:
                raw_cmd = cmd_match.group(1) or cmd_match.group(2)
                # Cleanup: remove internal backticks if caught inside parens
                cmd = raw_cmd.replace("`", "")
            else:
                cmd = None

            # Filter out common non-commands usually found in parens, if needed.
            # But the user convention is specific enough: (`cmd`) or `cmd`

            items.append(
                TaskItem(
                    line_num=i,
                    raw_line=line,
                    indent=indent,
                    state=state,
                    text=text.strip(),
                    command=cmd,
                )
            )

    return items


def _find_context(
    items: list[TaskItem],
) -> tuple[Optional[TaskItem], Optional[TaskItem], Optional[TaskItem]]:
    """Find the Phase, Active Task, and Next Task."""
    phase = None
    active = None
    next_task = None

    # Simple logic:
    # 1. Provide the Phase (top level item above active)
    # 2. Provide Active (first [/])
    # 3. Provide Next (first [ ] after Active)

    # First find active — find the LAST [/] (most nested/specific)
    active_idx = -1
    for i, item in enumerate(items):
        if item.state == "/":
            active = item
            active_idx = i
            # Don't break - keep scanning to find the deepest one

    if active:
        # Find Phase (scan backwards for indent 0/smaller)
        for i in range(active_idx, -1, -1):
            if items[i].indent < active.indent:
                phase = items[i]
                break

        # Find Next (scan forwards from active)
        for i in range(active_idx + 1, len(items)):
            if items[i].state == " ":
                next_task = items[i]
                break
    else:
        # No active task? Maybe all done or fresh start.
        # Find first empty
        for i, item in enumerate(items):
            if item.state == " ":
                next_task = item
                # Find phase for this next task
                for j in range(i, -1, -1):
                    if items[j].indent < item.indent:
                        phase = items[j]
                        break
                break

    return phase, active, next_task


@app.command()
def init():
    """Initialize a new task.md file from template."""
    path = _get_task_file()
    if path.exists():
        rprint(f"[red]Error: {path} already exists.[/red]")
        raise typer.Exit(1)

    # Template
    content = """# Task: Evolve Development Cycle

- [ ] Phase 0: INITIALIZE
    - [ ] Pre-Flight Check (`git status`)
    - [ ] Create Task Artifact
- [ ] Phase 1: ANALYZE
    - [ ] Health Check (`/health_check`)
    - [ ] Coverage Audit (`/coverage_audit`)
    - [ ] Feature Proposals (`/propose_features`)
- [ ] Phase 2: PLAN
    - [ ] Check Goals (`AUTOMATION_GOALS.md`)
    - [ ] Present Analysis
    - [ ] Create Implementation Plan (`/plan_feature`)
- [ ] Phase 3: BUILD
    - [ ] Scaffold (Optional)
    - [ ] Implement Core Logic
    - [ ] Import Verification
    - [ ] Write Unit Tests
    - [ ] CLI Support (Optional)
    - [ ] Lint Check
    - [ ] Code Quality Audit (`/code_quality_audit`)
- [ ] Phase 4: VERIFY
    - [ ] Unit Tests (`pytest`)
    - [ ] Smoke Tests (`smoke_test.py`)
    - [ ] Negative Testing (Failure modes)
    - [ ] Manual Check
- [ ] Phase 5: DOCUMENT
    - [ ] Docstrings
    - [ ] Guides/README
    - [ ] Walkthrough Artifact
- [ ] Phase 6: RELEASE (Optional)
    - [ ] Release Prep
    - [ ] Final Verification
    - [ ] Push
"""
    path.write_text(content, encoding="utf-8")
    rprint(f"[green]Created {path}[/green]")


@app.command()
def status():
    """Show current dev workflow status from task.md."""
    path = _get_task_file()
    items = _parse_tasks(path)

    if not items:
        rprint("[yellow]No tasks found. Run `mg dev init`?[/yellow]")
        return

    phase, active, next_item = _find_context(items)

    table = Table(title="Workflow Status")
    table.add_column("Level", style="dim")
    table.add_column("Item", style="bold")
    table.add_column("Command", style="cyan")

    if phase:
        table.add_row("PHASE", phase.text, "")

    if active:
        table.add_row("ACTIVE \[/]", active.text, active.command or "")
    else:
        table.add_row("ACTIVE", "[dim]None[/dim]", "")

    if next_item:
        table.add_row("NEXT \[ ]", next_item.text, next_item.command or "")

    console.print(table)


@app.command()
def check():
    """Run the verification command for the active task."""
    path = _get_task_file()
    items = _parse_tasks(path)
    _, active, _ = _find_context(items)

    if not active:
        rprint("[red]No active task found marked \[/].[/red]")
        raise typer.Exit(1)

    if not active.command:
        rprint(f"[yellow]Task '{active.text}' has no command defined.[/yellow]")
        return

    rprint(f"Running: [bold]{active.command}[/bold]")

    # Run the command
    args = shlex.split(active.command)
    result = subprocess.run(args)

    if result.returncode == 0:
        rprint("[green]PASS[/green]")
    else:
        rprint("[red]FAIL[/red]")
        raise typer.Exit(result.returncode)


@app.command()
def next(force: bool = False):
    """Verify current task and advance to the next one."""
    path = _get_task_file()
    items = _parse_tasks(path)
    _, active, next_item = _find_context(items)

    # 1. Verify Active
    if active:
        if active.command:
            rprint(f"Verifying: [bold]{active.command}[/bold]")
            if not force:
                try:
                    args = shlex.split(active.command)
                    result = subprocess.run(args)
                    if result.returncode != 0:
                        rprint(
                            "[red]Verification FAILED. Fix issues or use --force.[/red]"
                        )
                        raise typer.Exit(result.returncode)
                except FileNotFoundError:
                    rprint(f"[red]Command not found: {args[0]}[/red]")
                    if not force:
                        raise typer.Exit(1)
            else:
                rprint("[yellow]Skipping verification (--force)[/yellow]")

        # Mark active as done [x]
        _update_line_state(path, active.line_num, "x")
        rprint(f"[green]Completed: {active.text}[/green]")

    # 2. Advance to Next
    if next_item:
        _update_line_state(path, next_item.line_num, "/")
        rprint(f"[blue]Now Active: {next_item.text}[/blue]")
        if next_item.command:
            rprint(f"Next Gate: [cyan]{next_item.command}[/cyan]")
    else:
        rprint("[green]No next task found! All done?[/green]")


def _update_line_state(path: Path, line_num: int, new_state: str):
    """Update a specific line in the file with a new state character."""
    lines = path.read_text("utf-8").splitlines()
    if 0 <= line_num < len(lines):
        # Regex replace ONLY the state bracket
        lines[line_num] = re.sub(
            r"\[([ x/])\]", f"[{new_state}]", lines[line_num], count=1
        )
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")


@app.command()
def todo():
    """List TODOs in the codebase."""
    # Simple recursive grep, excluding venv/git
    cmd = [
        "grep",
        "-r",
        "TODO",
        ".",
        "--exclude-dir=.git",
        "--exclude-dir=.venv",
        "--exclude-dir=__pycache__",
    ]
    try:
        subprocess.run(cmd)
    except FileNotFoundError:
        # Fallback for Windows if grep not in path
        rprint("[yellow]grep not found, trying Select-String (powershell)...[/yellow]")
        subprocess.run(
            [
                "powershell",
                "-Command",
                "Select-String -Path .\\* -Pattern 'TODO' -Recurse -Exclude .venv,.git",
            ]
        )

