# Audit Report: mygoog_cli/docs.py

## Purpose
- Provides CLI commands for interacting with Google Docs. Supports document lifecycle management, content manipulation, find-and-replace, and document templating.

## Main Exports
- `create`: Creates a new, empty document.
- `get-text`: Extracts the plain text content of a document.
- `append`: Adds text to the end of a document.
- `replace`: Performs batch find-and-replace using a JSON map.
- `render`: Generates a new document from a template, performing variable substitution.
- `export-pdf`: Exports a Google Doc as a local PDF file.

## Findings
- **Data Input Flexibility:** The `render` and `replace` commands intelligently handle both literal JSON strings and paths to JSON files, making them suitable for both quick one-offs and automated pipelines.
- **Service Coordination:** Correctly identifies that exporting to PDF requires the Drive API, demonstrating good integration between service layers at the CLI level.
- **Error Handling:** Implements robust JSON parsing with clear error messages for invalid data inputs.

## Quality Checklist
- [x] Command signatures are clear and consistent
- [x] JSON data handling is versatile and robust
- [x] Export logic correctly uses the appropriate API
