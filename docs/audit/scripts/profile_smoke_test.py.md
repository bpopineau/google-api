# Audit Report: scripts/profile_smoke_test.py

## Purpose
- Performance profiling wrapper around `smoke_test.py`.

## Findings
- **Integration:** Successfully imports and executes the logic from `smoke_test.py` while wrapping it in `cProfile`.
- **Output:** Correctly redirects profiling stats to both a file (`profiling_results.txt`) and the console, facilitating performance regression checks.

## Quality Checklist
- [x] Functional profiling wrapper for smoke tests
- [x] Clear artifact generation
