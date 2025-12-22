# Workflow: /optimize
@description Systematic profiling and refactoring to improve performance.

## Phase 1: Establish Baseline
**Role:** Performance Engineer.
**Context:** We cannot optimize what we cannot measure.
**Task:**
1. **Identify Target:** Ask user which script or module to profile (e.g., `scripts/process_data.py`).
2. **Execute Atom:** `atoms/_profile.md`
   - **Input:** The target script.
   - **Output:** Baseline execution time and a list of "Hotspot Functions" (top 3 consumers of cumulative time).
3. **Record Baseline:** Write the baseline metrics to `task.md`.

## Phase 2: Code Analysis (The "Why")
**Role:** Python Internals Expert.
**Context:** Analyze the "Hotspot Functions" identified in Phase 1.
**Task:**
1. Read the source code of the hotspot functions.
2. **Apply Codex Pattern (7.2.1):**
   - "Analyze this Python code. Suggest three specific refactoring techniques (e.g., vectorization, memoization, generator usage) to improve speed and memory efficiency."
3. **Complexity Audit:**
   - Identify Big-O complexity (e.g., O(n^2) nested loops).
   - Check for I/O inside loops (the #1 killer).

## Phase 3: Optimization Planning
**Role:** Principal Architect.
**Task:**
1. **Select Strategy:** Choose the *single* most impactful change from Phase 2.
2. **Risk Assessment:**
   - Will this reduce readability? (If yes, requires strong justification).
   - Will this break existing tests?
3. **Plan Artifact:** Update `task.md` with the specific refactoring plan.
**Constraint:** Do not proceed until plan is approved.

## Phase 4: Execution
**Role:** Senior Software Engineer.
**Task:**
1. **Safety First:** Execute Atom `atoms/_checkpoint.md` (msg: "perf: baseline established for [module]").
2. **Refactor:** Apply the optimization.
3. **Verify Correctness:**
   - Execute Atom: `atoms/_run_tests.md`
   - **Gate:** IF FAIL: Revert immediately. Correctness > Speed.

## Phase 5: Verification (The Proof)
**Role:** QA Automation Engineer.
**Task:**
1. **Execute Atom:** `atoms/_profile.md` (Same target as Phase 1).
2. **Compare:**
   - Calculate % improvement: `(Baseline - New) / Baseline * 100`.
3. **Gate:**
   - **IF > 10% Faster:** Keep changes. Commit with "perf: improved [module] by X%".
   - **IF < 10% Faster:** Ask user: "Improvement is marginal. Revert to maintain readability?"

## Phase 6: Documentation
**Task:**
- Update docstring of optimized function to explain *why* the complex implementation exists (e.g., "Unrolled loop for performance").

