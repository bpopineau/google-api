# Specification: Directory Manifests (MANIFEST.md)

## Overview
This feature introduces `MANIFEST.md` files to every major directory in the repository. These files serve as "Signposts" for AI agents and developers, providing immediate high-level context about a directory's responsibility, its primary entry points, and its architectural dependencies.

## Functional Requirements

### 1. File Format and Location
- A `MANIFEST.md` file will be created in the root of the following directories:
    - `mygooglib/core/`
    - `mygooglib/services/`
    - `mygooglib/workflows/`
    - `mygoog_cli/`
    - `mygoog_gui/`
    - `tests/`
    - `scripts/`

### 2. Standard Structure
Each `MANIFEST.md` MUST follow this structure:
- **Purpose:** 1-2 sentences explaining the "Single Responsibility" of the directory.
- **Key Entry Points:** List of the 2-3 most important files/classes/functions that external code should interact with.
- **Dependencies:** List of other internal modules or external libraries this directory heavily relies on.
- **Architectural Rules:** (Optional) Any specific constraints (e.g., "Files in this directory must not import from `mygoog_gui`").

### 3. Agent-Friendliness
- Content should be concise and optimized for quick parsing by LLMs.
- Avoid repeating information that is already in `context_map.md` (like full method signatures).

## Non-Functional Requirements
- **Consistency:** All manifests should share the same heading structure.
- **Low Maintenance:** Focus on high-level intent rather than implementation details that change frequently.

## Acceptance Criteria
- [ ] Every listed directory contains a `MANIFEST.md` file.
- [ ] Each file contains at least the "Purpose", "Entry Points", and "Dependencies" sections.
- [ ] An AI agent (e.g., Gemini) can correctly identify the purpose of `mygooglib/core/` by reading its manifest.

## Out of Scope
- Auto-generation of these manifests (they are manually authored to capture *intent*).
- Full API documentation (docstrings handle this).
