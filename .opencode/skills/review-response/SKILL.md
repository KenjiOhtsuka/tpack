---
name: review-response
description: Use when a pull request has review comments from human reviewers or automated tools like CodeRabbit. Fetches all review comments, evaluates each for actionability, implements fixes, pushes changes, and replies to threads.
---

# PR Review Response

When a user asks you to handle PR review comments (from CodeRabbit, human reviewers, etc.):

1. **Fetch all comments and reviews** on the PR using `gh pr view <PR> --comments --json comments,reviews` and `gh api repos/<owner>/<repo>/pulls/<PR>/comments`.

2. **Categorize each comment:**
   - **Actionable** — requires a code change; implement it
   - **Not actionable** — explain briefly why and reply

3. **For actionable comments:**
   - Read the relevant code to understand the context
   - Implement the fix on the same branch
   - Verify with tests
   - Commit and push

4. **For non-actionable comments** (theoretical concerns, out of scope, unrealistic threat model):
   - Reply inline explaining the reasoning
   - Use `gh api repos/<owner>/<repo>/pulls/<PR>/comments -f body="..." -F in_reply_to=<comment_id> --method POST`

5. **Distinguish between:**
   - **Line comments** (reply-able via `in_reply_to`) — fetch these with `gh api repos/.../pulls/<PR>/comments`
   - **Review body comments** (not individually reply-able) — address the concern and note it in a general PR comment or commit message

6. **Always verify existing tests still pass** after making changes before pushing.
