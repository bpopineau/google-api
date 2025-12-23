# mygooglib/core

## Purpose
Provides the foundational infrastructure for the entire library, including authentication, configuration management, exception handling, and shared type definitions. This directory serves as the base layer that all other modules depend on.

## Key Entry Points
- [`client.py`](file:///c:/Users/brand/Projects/google-api/mygooglib/core/client.py): The primary access point for initializing service clients and managing API connections.
- [`auth.py`](file:///c:/Users/brand/Projects/google-api/mygooglib/core/auth.py): Handles OAuth 2.0 flows, token management, and credential storage.
- [`config.py`](file:///c:/Users/brand/Projects/google-api/mygooglib/core/config.py): Manages application settings, environment variables, and user preferences.
- [`types.py`](file:///c:/Users/brand/Projects/google-api/mygooglib/core/types.py): Defines common data structures and type hints used across the library.

## Dependencies
- **External:** `google-auth`, `google-auth-oauthlib`, `pydantic`
- **Internal:** None (This is the bottom of the dependency tree)
