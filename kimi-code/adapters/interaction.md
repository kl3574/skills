# Kimi Code interaction adapter

Use this adapter whenever a skill asks the user a question, waits for answers, requires approval, or distinguishes HITL from AFK work.

## Never Ask mode

In Never Ask (`/auto`) mode, do not call `AskUserQuestion`, do not invent the user's answers, and do not claim that the user approved or confirmed anything.

Complete only independently knowable and safe AFK work. For mandatory interviews or approval gates, produce the available **draft** and clearly report which HITL steps remain. Do not publish issues or comments, close or reclassify tickets, push branches, commit irreversible decisions, or otherwise act as though a HITL decision occurred. Interactive completion requires the user to rerun in an interactive permission mode and decide how to proceed.

A HITL ticket never becomes AFK merely because questions are unavailable. Keep it unresolved and state the blocker.

## Always Ask or Ask When Needed mode

In `manual` or `/yolo` mode, ask the required questions and wait for the answers before continuing past the corresponding decision gate. Use `AskUserQuestion` for structured choices when appropriate; use a plain text reply for free-form interviews. When independent research can run concurrently, a background question or background agent may be used, but only downstream steps that do not depend on the answer may continue.

The user owns HITL decisions in every mode. The agent supplies evidence, recommendations, and drafts, never a substitute approval.

## Non-interactive verification

In Kimi Code 2.4.1, `kimi -p` cannot be combined with `--auto`. A `/skill:<name>` string passed through `kimi -p` is ordinary prompt text, not proof of a native user-only skill invocation. Inspect the actual `skill-loaded` record and its trigger before counting a smoke test as a native invocation.

A model-invocable dependency loaded by the model is not equivalent to the user-only wrapper that points to it. Verify user-only wrappers and live HITL interviews in an interactive session.
