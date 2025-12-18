---
description: systematically refactor code with safety checks
---

1. Verify Baseline
// turbo
   - `/development`
   - **Constraint**: Do not proceed if tests fail. Fix the baseline first.

2. Scope and Plan
   - **Action**: Identify the specific target (function, class, module).
   - **Thought Process**:
     - "What is the Code Smell?" (Duplication, Long Method, Feature Envy, etc.)
     - "What is the Target State?" (Extracted function, moved class, etc.)
   - **Safety**: Is this an API-breaking change? If so, plan for backwards compatibility (deprecation warning).

3. Execute Refactor
   - **Action**: Apply the changes incrementally.
   - **Tip**: Use `replace_file_content` for small chunks or `multi_replace_file_content` for larger structural changes.

4. Verify Changes
// turbo
   - `/development`
   - **Logic**: valid refactoring shouldn't change behavior. Tests must pass.

5. Cleanup
   - **Action**: Remove old code, unused imports, or temporary shims.
   - **Action**: Update type hints and docstrings if the signature changed slightly (though it shouldn't for pure refactors).
