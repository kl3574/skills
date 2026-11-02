# Kimi Code capability map

Use this map after every upstream update. It records where each promoted skill's behavior lands in Kimi Code, which upstream paths the overlay changes, and what the latest smoke test actually proved.

## Baseline

- Upstream release: `v1.3.2`, commit `d1478fcb140db0b93c0c8df17bcfd311844749d0`
- Patch target: upstream `main`, commit `4ae2317ddb22b046e26455e4f9c9b3aaaf62212d`
- Runtime: Kimi Code 2.4.1 on Linux
- Coverage: all 27 promoted skills from `.claude-plugin/plugin.json`
- Patch shape: 20 `SKILL.md` files plus three auxiliary documents, covering 22 skills
- Unchanged: five skills have no file changes; two more keep `SKILL.md` unchanged and patch only auxiliary documents

`Pass` means the named executable path was exercised. `Draft` means only the automatic-mode draft and safe stop were verified. `Gated` identifies a decision or external action that still requires a human.

## Shared capabilities

| Upstream capability | Kimi Code implementation | Source of truth | Revalidation |
| --- | --- | --- | --- |
| Model-invocable skill dependency | Native `Skill` tool, one skill per call | Each patched `SKILL.md` | Inspect the real `skill-loaded` record and trigger |
| User-only skill invocation | Interactive `/skill:<name>` | [Interaction adapter](adapters/interaction.md) | Do not count a literal `kimi -p` string as native invocation |
| Subagents and fresh context | Native `Agent`, fresh by default, `explore`/`plan`/`coder`, optional `model: "primary"` | [Subagent adapter](adapters/subagents.md) | Check profile, foreground/background mode, return report, and nested-agent fallback |
| HITL and approval gates | Plain text or `AskUserQuestion` in interactive modes; drafts and safe stops in `/auto` | [Interaction adapter](adapters/interaction.md) | Verify no fabricated answers or approvals and no premature external writes |
| Branches and parallel implementation | Absolute Git worktrees, explicit Bash `cwd`, committed preparation, clean-state gates, serial merges | [Worktree adapter](adapters/worktrees.md) | Check branch, base, clean status before dispatch and after completion |
| Browser feedback | WebBridge first, registered `mcp__chrome-devtools__*` fallback | `diagnosing-bugs` patch | Check WebBridge `/status`, then exercise real navigation, input, state assertions, and cleanup on one path |
| HTML and client-side guidance | Native `Skill` call to `modern-web-guidance:modern-web-guidance` | `prototype`, `teach`, and architecture patches | Confirm the search-and-retrieve workflow and actual browser rendering |
| Session history and compaction | `/usage`, current-session `/compact`, `/new` for a fresh session, `wire.jsonl` for evidence | `ask-matt` and `retro` patches | Check session semantics and read primary main/subagent records |
| Promoted skill set | `.claude-plugin/plugin.json`, flattened by `install.py` | Upstream plugin manifest | Reconcile added or removed skills in this map before installation |

## Skill mapping

### Engineering

| Skill | Kimi Code mapping | Patched upstream paths | Latest verification |
| --- | --- | --- | --- |
| [ask-matt](../skills/engineering/ask-matt/SKILL.md) | `/skill:` invocation, `/usage`, current-session `/compact`, `/new`, native Agent routes | `SKILL.md`, `PHASE-BOUNDARIES.md` | Pass: route and session-semantics checks |
| [diagnosing-bugs](../skills/engineering/diagnosing-bugs/SKILL.md) | Confirm project browser dependencies; WebBridge, then Chrome DevTools MCP, then another feedback loop | `SKILL.md` | Pass: red-green diagnosis and both browser paths |
| [grill-with-docs](../skills/engineering/grill-with-docs/SKILL.md) | Interaction adapter plus separate native `grilling` and `domain-modeling` calls | `SKILL.md` | Draft: first round and safe stop; live HITL not run |
| [triage](../skills/engineering/triage/SKILL.md) | Interaction adapter before maintainer decisions or applying outcomes | `SKILL.md` | Pass: reproduction and recommendation. Gated: labels, comments, and closure |
| [improve-codebase-architecture](../skills/engineering/improve-codebase-architecture/SKILL.md) | `explore` Agent, modern-web guidance, interaction adapter | `SKILL.md` | Pass: HTML report and browser review. Gated: candidate selection |
| [setup-matt-pocock-skills](../skills/engineering/setup-matt-pocock-skills/SKILL.md) | Interaction adapter; `AGENTS.md` first, preserving unrelated content | `SKILL.md` | Draft: configuration proposal; confirmed writes not run |
| [tdd](../skills/engineering/tdd/SKILL.md) | Native `Skill` workflow needs no textual change | None | Pass: independent red-green implementations and fixes |
| [to-spec](../skills/engineering/to-spec/SKILL.md) | Existing workflow composes with the interaction policy without a file patch | None | Draft: specification; approval and publication gated |
| [to-tickets](../skills/engineering/to-tickets/SKILL.md) | Automatic mode may draft but cannot claim approval or publish | `SKILL.md` | Pass: local ticket execution. Gated: external publication |
| [wayfinder](../skills/engineering/wayfinder/SKILL.md) | Interaction, subagent, and worktree adapters; committed research claims before dispatch | `SKILL.md` | Pass: clean claim, cited report, ticket resolution. HITL maps not run |
| [implement](../skills/engineering/implement/SKILL.md) | Interaction adapter for ambiguous ticket references; native TDD and review calls | `SKILL.md` | Pass: implementation, tests, and review |
| [implement-spec](../skills/engineering/implement-spec/SKILL.md) | Assigned absolute worktrees, background coders, clean gates, serial merges, interaction adapter | `SKILL.md` | Pass: parallel implementation, integration, dual-axis review, cleanup |
| [prototype](../skills/engineering/prototype/SKILL.md) | Interaction and worktree adapters; modern-web guidance before browser code | `SKILL.md` | Pass: throwaway branch, browser interactions, state checks |
| [research](../skills/engineering/research/SKILL.md) | Background `coder`; inline research inside a subagent that cannot dispatch another | `SKILL.md` | Pass: clean worktree, official citations, report-only diff, ticket resolution |
| [domain-modeling](../skills/engineering/domain-modeling/SKILL.md) | Native `Skill` workflow needs no textual change | None | Pass: glossary and domain evaluation |
| [codebase-design](../skills/engineering/codebase-design/SKILL.md) | Independent foreground Agents; `plan` for read-only designs, `coder` for written artifacts | `DESIGN-IT-TWICE.md` only | Pass: architecture vocabulary and design evaluation |
| [code-review](../skills/engineering/code-review/SKILL.md) | Two foreground `coder` calls, normally `model: "primary"`; interaction adapter for missing inputs | `SKILL.md` | Pass: Standards and Spec reviews on real diffs |
| [pr](../skills/engineering/pr/SKILL.md) | Native PR template needs no textual change | None | Pass: private draft PR publication and readback, closed without merge |
| [retro](../skills/engineering/retro/SKILL.md) | `$KIMI_CODE_HOME/sessions`, main and subagent `wire.jsonl`, secret redaction | `SKILL.md` | Pass: real main/subagent session review |
| [wizard](../skills/engineering/wizard/SKILL.md) | Interaction gates; inspect non-secret sources and keep live values with the human | `SKILL.md` | Pass: `bash -n` and static mapping. Live provisioning not run |

### Productivity

| Skill | Kimi Code mapping | Patched upstream paths | Latest verification |
| --- | --- | --- | --- |
| [grill-me](../skills/productivity/grill-me/SKILL.md) | Interaction adapter, then native `grilling` | `SKILL.md` | Draft: first round and safe stop; native user-only invocation and live HITL not run |
| [grilling](../skills/productivity/grilling/SKILL.md) | Interaction adapter for every round; background `explore` for facts | `SKILL.md` | Draft: real native load, first-round questions, no fabricated answers |
| [handoff](../skills/productivity/handoff/SKILL.md) | Kimi `arguments: [purpose]` replaces `argument-hint` | `SKILL.md` | Pass: portable, redacted handoff and cleanup |
| [teach](../skills/productivity/teach/SKILL.md) | Kimi `arguments: [topic]`, interaction adapter, modern-web guidance | `SKILL.md` | Draft: learning mission; lesson generation and delivery require the mission |
| [to-questionnaire](../skills/productivity/to-questionnaire/SKILL.md) | Interaction adapter for recipient and required-answer exchanges | `SKILL.md` | Draft: questionnaire; recipient decisions and sending not run |
| [wait-what](../skills/productivity/wait-what/SKILL.md) | Native glossary-based explanation needs no textual change | None | Pass: concise re-pitch from project vocabulary |
| [writing-for-agents](../skills/productivity/writing-for-agents/SKILL.md) | Kimi mechanics plus links to all three adapters | `SKILL-MECHANICS.md` only | Pass: native load and document review |

## Update checklist

1. Record the old and new upstream commits in this file and `README.md`.
2. Run `python3 kimi-code/install.py --check` before touching the managed installation.
3. Compare every changed upstream path named in the tables:

   ```bash
   git diff <old-upstream-commit>..<new-upstream-commit> -- <path-from-table>
   ```

4. Check `.claude-plugin/plugin.json` for added, removed, renamed, or reparented skills. Update the map and flat-name collision checks together.
5. Check adapter contracts against the current Kimi Code tools, permission mode, session commands, browser integrations, and flat skill layout.
6. Reconcile the patch and rerun the affected executable scenarios. Keep draft and gated outcomes distinct from passes.
7. Install into an empty temporary directory and verify native skill loading before using `--force` on the managed directory.
