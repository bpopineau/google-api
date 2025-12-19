---
description: Profiles code and refactors for performance.
---

# /optimize

## Phase 1: Profiling
**Role:** Performance Engineer.
1. **Baseline Measurement:**
   - Create a profiling script `scripts/profile_target.py`.
   - Run with `cProfile` or `timeit`.
   - **Output:** Capture baseline execution time.

## Phase 2: Analysis
**Role:** Python Internals Expert.
1. **Analyze Hotspots:**
   - Identify the slowest functions from the profile data.
2. **Complexity Check:**
   - Analyze Big-O complexity of the hotspots.
   - Check for unnecessary loops, N+1 queries, or heavy I/O.

## Phase 3: Optimization Plan
**Role:** Senior Software Engineer.
1. **Propose Changes:**
   - Use the **Codex Pattern**: "Suggest 3 specific refactoring techniques (e.g., vectorization, memoization)".
   - **Constraint:** Do not trade readability for negligible speed gains.

## Phase 4: Verification
**Task:**
   - Apply changes.
   - Run `scripts/profile_target.py` again.
   - **Gate:** IF SPEEDUP < 10%: Revert. (Avoid premature optimization).
