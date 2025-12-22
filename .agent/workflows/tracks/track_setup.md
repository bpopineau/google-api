---
description: One-time project scaffolding - creates conductor context files
---

# Workflow: /track_setup

> **Run once per project.** Sets up the Context-Driven Development environment.

## Pre-Flight Check

1. Verify `.agent/workflows/tracks/` directory exists
2. Check if `GEMINI.md` already exists (update vs create)

---

## Step 1: Gather Product Context

**Goal:** Define WHAT we're building.

**Actions:**
1. Interview user to capture:
   - Project vision and goals
   - Target audience
   - Core value proposition
   - Key features and workflows

2. Write to `conductor/product.md`:
   ```markdown
   # Product Guide: [Project Name]
   
   ## Vision
   [One paragraph describing the project's purpose]
   
   ## Target Audience
   [Who uses this and why]
   
   ## Core Value Proposition
   [What makes this valuable]
   
   ## Key Features & Workflows
   [List of major capabilities]
   ```

---

## Step 2: Define Product Guidelines

**Goal:** Establish UI/UX and communication standards.

**Actions:**
1. Discuss with user: tone, design philosophy, UX patterns

2. Write to `conductor/product-guidelines.md`:
   ```markdown
   # Product Guidelines: [Project Name]
   
   ## Communication & Tone
   [How the product speaks]
   
   ## Design Philosophy  
   [Visual approach - e.g., Material Design, minimalism]
   
   ## UX Patterns
   [Standard interactions and behaviors]
   
   ## Visual Identity
   [Colors, dark mode, status indicators]
   ```

---

## Step 3: Document Tech Stack

**Goal:** Set technical boundaries and preferences.

**Actions:**
1. Analyze existing codebase or interview user

2. Write to `conductor/tech-stack.md`:
   ```markdown
   # Tech Stack: [Project Name]
   
   ## Core Technologies
   - **Language:** [e.g., Python >=3.10]
   - **Framework:** [e.g., PySide6, FastAPI]
   - **CLI:** [e.g., Typer + Rich]
   
   ## External Services
   [APIs, databases, auth providers]
   
   ## Development & QA
   - **Testing:** [e.g., Pytest]
   - **Linting:** [e.g., Ruff]
   - **Type Checking:** [e.g., Mypy]
   ```

---

## Step 4: Configure Workflow Preferences

**Goal:** Define how the team works.

**Actions:**
1. Discuss: TDD preference, commit strategy, verification gates

2. Create or adapt `conductor/workflow.md` with:
   - Guiding principles
   - Task workflow (TDD red-green-refactor)
   - Phase checkpoint protocol
   - Quality gates
   - Commit message format
   - Definition of Done

---

## Step 5: Initialize Track Registry

**Actions:**
// turbo
1. Create `conductor/tracks.md` if it doesn't exist:
   ```markdown
   # Project Tracks
   
   This file tracks all major tracks for the project.
   
   ---
   
   [Tracks will be listed here]
   ```

---

## Step 6: Create/Update GEMINI.md

**Actions:**
1. Write `GEMINI.md` to project root:
   ```markdown
   # Project: [Name]
   
   ## Context
   - **Product:** `conductor/product.md`
   - **Guidelines:** `conductor/product-guidelines.md`  
   - **Tech Stack:** `conductor/tech-stack.md`
   - **Workflow:** `conductor/workflow.md`
   - **Active Tracks:** `conductor/tracks.md`
   
   ## Workflow Commands
   - `/track_new [description]` - Start new feature/bug
   - `/track_implement` - Execute current track plan
   - `/track_status` - View all track statuses
   - `/track_revert` - Revert track/phase/task
   ```

---

## Completion

**Output:** Present summary of all created artifacts to user.

**Gate:** Confirm user reviews and approves context files before first track.

