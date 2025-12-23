# Audit Report: mygoog_cli/gmail.py

## Purpose
- Provides CLI commands for interacting with the Gmail API. Supports sending emails, searching messages, viewing content, and batch downloading attachments.

## Main Exports
- `send`: Sends emails with support for multiple recipients (TO/CC/BCC) and multiple attachments.
- `search`: Searches messages with an interactive selection mode for follow-up actions (view, trash, archive).
- `view`: Displays message headers and plain text body in the terminal.
- `save-attachments`: Batch downloads attachments from messages matching a query, with filename filtering support.
- Action commands: `mark-read`, `trash`, `archive`.

## Findings
- **High Utility Workflows:** The `save-attachments` command is exceptionally well-implemented, providing a clear progress indicator and efficient recursive search, making it ideal for automating administrative tasks.
- **Robust Input Handling:** The `_split_emails` helper ensures that email lists can be provided consistently across parameters, supporting both Repeated Typer Options and comma-separated strings.
- **Interactive Triage:** Similar to Drive and Calendar, the interactive search provides a professional "email triage" experience directly in the shell.

## TODOs
- [ ] [Feature] Add support for reading the email body from a file (e.g., `mg gmail send --body-file message.txt`) to avoid shell quoting issues for long bodies.
- [ ] [Feature] Implement HTML email support (already identified as a TODO in the service layer).

## Quality Checklist
- [x] Batch attachment saving is robust and reported correctly
- [x] Email sending handles headers (CC/BCC) and attachments correctly
- [x] Interactive triage mode is intuitive
