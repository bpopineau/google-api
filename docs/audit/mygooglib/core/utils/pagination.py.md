# Audit Report: mygooglib/core/utils/pagination.py

## Purpose
- Generic utility to handle Google API's `nextPageToken` pagination pattern. It collects all items across multiple pages into a single list, with support for result limits and progress tracking.

## Main Exports
- `paginate(...)`: Higher-order function that takes a request-factory, executes it iteratively, and gathers results.

## Findings
- **Robustness:** Integrated with `execute_with_retry_http_error`, ensuring that transient failures during any page fetch are retried.
- **Flexibility:** Parametrized `items_key` handles services that use different keys (e.g., `files`, `messages`, `tasklists`).
- **Memory:** Collects all items in memory; suitable for most personal automation tasks but might be a bottleneck for extremely large datasets.

## TODOs
- [ ] [Feature] Consider adding a generator-based sibling function (e.g., `paginate_gen`) to handle streaming large datasets without loading everything into memory.

## Quality Checklist
- [x] Docstrings follow project style
- [x] Type hints are complete and modern
- [x] Unused code removed
- [x] Logically verified for edge cases
