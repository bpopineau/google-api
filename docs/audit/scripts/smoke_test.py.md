# Audit Report: scripts/smoke_test.py

## Purpose
- High-level automated health check verifying all integrated Google services.

## Findings
- **Extensive Coverage:** Tests Drive, Sheets, Gmail, Calendar, and Tasks in a single run.
- **Safety:** Default behavior is read-only; mutation operations require an explicit `--write` flag.
- **Diagnostics:** Custom formatting (`_print_jsonable`) provides clean summarized output for complex API payloads.
- **Usability:** Well-structured command-line interface with `argparse`, providing clear help and granular command control.

## Quality Checklist
- [x] Comprehensive service coverage
- [x] Safety guards for write operations
- [x] Clean diagnostic output
