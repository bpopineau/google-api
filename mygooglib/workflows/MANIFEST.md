# mygooglib/workflows

## Purpose
Orchestrates complex, multi-step business logic that often span multiple Google services. Unlike the `services` directory which wraps raw APIs, this directory contains "recipes" or "flows" that solve specific user problems by combining capabilities.

## Key Entry Points
- [`workflows.py`](file:///c:/Users/brand/Projects/google-api/mygooglib/workflows/workflows.py): Base classes and registry for defining and executing workflows.
- [`search.py`](file:///c:/Users/brand/Projects/google-api/mygooglib/workflows/search.py): Implementation of the "Global Search" workflow that queries multiple services.

## Dependencies
- **Internal:** `mygooglib.core`, `mygooglib.services`
