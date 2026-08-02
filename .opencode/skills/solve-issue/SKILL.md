---
name: solve-issue
description: Use when asked to fix a specific GitHub issue. Reads the issue, understands context, implements the fix on a branch, creates a PR, and closes the issue.
---

# Solve GitHub Issue

1. **Read the issue**: `gh issue view {issue-number}`. Identify the problem, expected behavior, and any linked context.

2. **Read relevant code**: Use `grep`, `glob`, and `read` to understand the area of code that needs changing. Study conventions of neighboring files (imports, libraries, naming, typing).

3. **Create a branch**: Start from a clean, current default branch. Fetch and fast-forward the default branch, verify the worktree is clean, then create the fix branch:

   ```sh
   default_branch="$(gh repo view --json defaultBranchRef --jq '.defaultBranchRef.name')"
   git fetch origin "$default_branch"
   git checkout "$default_branch"
   git pull --ff-only origin "$default_branch"
   git status --porcelain   # must be empty
   git checkout -b fix/<short-description>
   ```

4. **Implement the fix**: Follow existing code conventions — mimic style, use the same libraries, no new dependencies. Do not add explanatory comments.

5. **Test**: Run the project's documented test suite. Discover the canonical test command from `CONTRIBUTING.md` and any CI configuration before consulting `pyproject.toml`. Verify all existing tests still pass.

6. **Commit**: Stage only intended files (`git add`), then `git commit -m "..."` with a concise message matching repo style.

7. **Push**: `git push -u origin HEAD`.

8. **Create a PR**: Use the repository's default branch as the base and reference the issue explicitly in the body:

   ```sh
   gh pr create --fill --base "$default_branch" --body "Fixes #${issue_number}"
   ```

   The `Fixes #<issue-number>` reference makes GitHub auto-close the issue on merge.
