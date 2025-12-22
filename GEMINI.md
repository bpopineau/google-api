# mg Project Context

## Overview
mg is a unified desktop application and automation hub for Google Workspace integration.

## Context Files
| File | Purpose |
|------|---------|
| `conductor/product.md` | Product vision and target audience |
| `conductor/product-guidelines.md` | UX/UI standards and tone |
| `conductor/tech-stack.md` | Languages, frameworks, tools |
| `conductor/workflow.md` | Development process and TDD rules |
| `conductor/tracks.md` | Active project tracks |

## Track Workflows
| Command | Description |
|---------|-------------|
| `/track_setup` | One-time project scaffolding |
| `/track_new [description]` | Start new feature/bug track |
| `/track_implement` | Execute current track with TDD |
| `/track_status` | View all track progress |
| `/track_revert` | Revert track/phase/task |

## Development Rules
1. **Read context first** - Load `conductor/` files before major changes
2. **Follow TDD** - Write failing tests → Implement → Refactor
3. **Phase checkpoints** - Verify each phase with user before proceeding
4. **Git notes** - Attach detailed notes to task/phase commits
5. **Commit format** - `<type>(<scope>): <description>`

## Tech Stack Quick Ref
- **Language:** Python >=3.10
- **GUI:** PySide6
- **CLI:** Typer + Rich  
- **Testing:** Pytest
- **Linting:** Ruff
- **Types:** Mypy

