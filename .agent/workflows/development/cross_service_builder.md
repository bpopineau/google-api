---
description: Guide for building features that combine multiple mygooglib services
---

# /cross_service_builder

**Goal**: Build integration features systematically.

## ⚠️ Task Management
- **Rule**: Add sub-items to `task.md` for each stage of the build.

---

1. Identify Pattern & Update Task
   - **Source**: `sheets`, `gmail`, etc.
   - **Target**: `calendar`, `docs`, etc.
   - **Action**: Add to `task.md`:
     - `[ ] Design Data Flow`
     - `[ ] Stage 1: Read Source`
     - `[ ] Stage 2: Transform`
     - `[ ] Stage 3: Write Target`

2. Design Data Flow
   - Sketch mapping: `Source Field A` -> `Target Field B`.
   - **Gate**:
     - **IF MAPPED**: Mark `Design Data Flow` as `[x]`.
     - **IF UNCLEAR**: Stop. Check API docs. Recurse.

3. Implement Stage 1 (Read Source)
   - Verify reading works in isolation.
   - **Prove It**: `print(rows)` shows data.
   - **Action**: Mark `[x]` after verification.

4. Implement Stage 2 (Transform Logic)
   - Write pure python logic (dict -> dict).
   - **Prove It**: Unit test transformation logic.
   - **Action**: Mark `[x]` after verification.

5. Implement Stage 3 (Write Target)
   - Verify writing works with test data.
   - **Gate**:
     - **IF SUCCESS**: Mark `[x]`.
     - **IF API ERROR**: Stop. Debug permissions/payload. Recurse.

6. Finalize & Document
   - Create reusable function in `mygooglib/workflows.py` (optional).
   - Update `docs/guides/usage.md`.

---

**Result**: Ensure all sub-tasks in `task.md` are `[x]`.

