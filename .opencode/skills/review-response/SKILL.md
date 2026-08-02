---
name: review-response
description: Use when a pull request has review comments from human reviewers or automated tools like CodeRabbit. Fetches all review comments, evaluates each for actionability, implements fixes, pushes changes, and replies to threads.
---

# PR Review Response

When a user asks you to handle PR review comments (from CodeRabbit, human reviewers, etc.):

1. **Fetch all comments and reviews** on the PR. Use paginated requests so nothing is missed (replace `{owner}`, `{repo}`, `{pr}` with actual values, or quoted variables such as `"$PR_NUMBER"`):

   ```sh
   # all line comments, paginated into a single array
   gh api --paginate --slurp "repos/{owner}/{repo}/pulls/{pr}/comments"
   # reviews (includes review-body comments), paginated
   gh api --paginate --slurp "repos/{owner}/{repo}/pulls/{pr}/reviews"
   # issue comments on the PR
   gh api --paginate --slurp "repos/{owner}/{repo}/issues/{pr}/comments"
   ```

2. **Categorize each comment:**
   - **Actionable** — requires a code change; implement it
   - **Not actionable** — explain briefly why and reply

3. **For actionable comments:**
   - Read the relevant code to understand the context
   - Implement the fix on the same branch
   - Verify with tests
   - Review `git status` and `git diff`, stage only the intended files, then commit and push

4. **For non-actionable line comments** (theoretical concerns, out of scope, unrealistic threat model):
   - Reply inline explaining the reasoning
   - Use `gh api "repos/{owner}/{repo}/pulls/{pr}/comments" -f body="..." -F in_reply_to={comment_id} --method POST`

5. **Distinguish between:**
   - **Line comments** (reply-able via `in_reply_to`) — fetch these with `gh api --paginate "repos/{owner}/{repo}/pulls/{pr}/comments"`
   - **Review body comments** (not individually reply-able) — address the concern and note it in a general PR comment rather than an inline reply

6. **Always verify existing tests still pass** after making changes before pushing.
