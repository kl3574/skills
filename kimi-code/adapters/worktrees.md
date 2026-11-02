# Kimi Code worktree adapter

Use this adapter whenever a skill uses branches, worktrees, integration branches, or parallel implementation agents.

1. The main agent creates the integration worktree and every per-task worktree before dispatching subagents. Assign each one an **absolute worktree path** and a branch. Record which path belongs to each ticket or research task. Commit every preparation edit, including ticket claims, before dispatch; an expected uncommitted edit still makes the worktree dirty.
2. Put that absolute worktree path in the subagent prompt. Every `Read`, `Write`, `Edit`, `Grep`, and `Glob` path must be absolute or rooted at that path. Every `Bash` call must set `cwd` explicitly to that worktree. Never rely on `cd` persisting between calls or on a subagent inheriting the intended directory.
3. Each implementer works only in its assigned worktree. Before editing, verify the branch, base commit, and clean status. If the worktree is dirty or based on the wrong commit, stop and report to the main agent; do not reset or clean away changes. There is no exception for a dirty edit the main agent made or can explain.
4. Integration merges are **serial**: the main agent, or one merger acting at a time, merges each finished branch into the integration worktree using the explicit integration `cwd`. Implementers report their branch and commit and do not race integration merges.
5. Research and prototype branches follow the same rules. A background context is not a filesystem boundary. Push only when the skill and user request authorize it, and never open a PR for a research-only branch.
6. Remove worktrees only after the required checks pass, the work is merged or deliberately preserved, and the worktree is clean. Do not use destructive reset or clean commands as a shortcut.
7. Use Tower only when the user has explicitly enabled it. Without Tower, use ordinary `Agent` calls with the path and serial-merge rules above.
