# Kimi Code subagent adapter

Use this adapter whenever a skill asks for a subagent, sub-agent, background agent, or parallel agents.

1. Use Kimi Code's native `Agent` tool, not a `Task` tool. A fresh context is the default: omit `fork` or set it to `false`. Use `resume` only when the skill explicitly requires continuing an earlier agent.
2. Choose the profile by the work:
   - `explore`: read-only codebase exploration and fact finding.
   - `plan`: read-only architecture and implementation planning.
   - `coder`: implementation, code review, merging, research reports, or any task that must write files.
3. For foreground parallel work, issue the independent `Agent` calls in the same response with `run_in_background` omitted or `false`, then aggregate their returned reports.
4. For background work, set `run_in_background: true`. Continue only with independent work. Wait for the result when the next step depends on it. Do not use `AgentSwarm` unless the user has enabled swarm mode.
5. An exploration task that must save notes is a `coder` task, not an `explore` task, because the `explore` profile is read-only.
6. Keep the native `Skill` tool for model-invocable inline skills. Skills with model invocation disabled are rejected by the tool and are invoked by the human through `/skill:<name>` instead. Do not replace a skill invocation with prose describing a slash command.
7. For judgment-heavy code review, architecture, or merging that should use the caller's model, set `model: "primary"`. Otherwise omit `model` to use the configured subagent pool default.
8. For independent branches or worktrees, also follow [the worktree adapter](worktrees.md). Context isolation alone is not filesystem isolation.
9. If the `Agent` tool is unavailable, including inside a Kimi subagent that cannot dispatch another subagent, do not invent a nested agent or simulate parallel reports. Complete the scoped work inline and state that nested or parallel execution was unavailable.
