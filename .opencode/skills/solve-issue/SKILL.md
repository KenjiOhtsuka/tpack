---
name: solve-issue
description: Use when asked to fix a specific GitHub issue. Reads the issue, understands context, implements the fix on a branch, creates a PR, and closes the issue.
---

# Solve GitHub Issue

1. **Read the issue**: `gh issue view <number>`. Identify the problem, expected behavior, and any linked context.

2. **Read relevant code**: Use `grep`, `glob`, and `read` to understand the area of code that needs changing. Study conventions of neighboring files (imports, libraries, naming, typing).

3. **Create a branch**: `git checkout -b fix/<short-description>`. Run from the default branch.

4. **Implement the fix**: Follow existing code conventions — mimic style, use the same libraries, no new dependencies. Do not add explanatory comments.

5. **Test**: Run the project's test suite (`pytest` or equivalent found in `pyproject.toml`). Verify all existing tests still pass.

6. **Commit**: Stage only intended files (`git add`), then `git commit -m "..."` with a concise message matching repo style.

7. **Push**: `git push -u origin HEAD`.

8. **Create a PR**: `gh pr create --fill --base main`. Ensure the PR body includes `Fixes #<issue-number>` so GitHub auto-closes the issue on merge.
