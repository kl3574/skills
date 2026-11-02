# Kimi Code adaptation overlay

This directory packages the Kimi Code adaptation as an overlay. Upstream skill sources stay unchanged in Git, which keeps later upstream merges small and makes adaptation drift explicit.

## Verified baseline

- Upstream release: `v1.3.2`, commit `d1478fcb140db0b93c0c8df17bcfd311844749d0`
- Patch target: upstream `main`, commit `4ae2317ddb22b046e26455e4f9c9b3aaaf62212d`
- Runtime: Kimi Code 2.4.1 on Linux
- Optional browser integrations: Kimi WebBridge 2.0.30 and `chrome-devtools-mcp` 1.12.0

The patch changes 23 files: 20 `SKILL.md` files and three auxiliary documents, covering 22 skills. All 27 promoted skills are listed in [CAPABILITY-MAP.md](CAPABILITY-MAP.md), including five with no file changes and two that patch only auxiliary documents.

## Contents

- `kimi-code.patch`: reviewed behavior changes against the upstream skill sources
- `adapters/interaction.md`: HITL decisions, automatic-mode stopping, and non-interactive verification limits
- `adapters/subagents.md`: native `Agent` profiles, foreground and background execution, and fresh context
- `adapters/worktrees.md`: absolute paths, clean-state gates, committed claims, and serial merges
- `install.py`: patch validation, source-to-flat link rewriting, safe installation, and replacement backups
- `CAPABILITY-MAP.md`: per-skill implementation mapping, changed paths, and verification status

## Requirements

Install Git and Python 3 before using the installer. No Python packages are required.

The core skills need only Kimi Code. Browser feedback uses WebBridge first and a registered `chrome-devtools` MCP as fallback. HTML generation skills also expect the `modern-web-guidance` plugin. These integrations are optional and are not installed by this overlay.

## Validate

From the repository root:

```bash
python3 kimi-code/install.py --check
```

This applies the patch to a temporary copy, verifies source and flattened adapter links, and writes nothing into the repository or a skill directory. A nonzero exit means upstream drift needs review before installation.

## Install into a new or unmanaged directory

```bash
python3 kimi-code/install.py --dest "$HOME/.agents/skills"
```

Existing directories managed by this overlay stop installation by default. Other skill directories in the destination are left alone.

To replace the managed set:

```bash
python3 kimi-code/install.py --dest "$HOME/.agents/skills" --force
```

`--force` first moves every existing managed directory to `.kimi-code-backup-<timestamp>` inside the destination. Keep that backup until the new installation passes your checks.

The installer rewrites adapter links from repository layout to Kimi's flat `<destination>/<skill>` layout and installs `_kimi-code` beside those skill directories.

## Update after an upstream release

1. Fetch and merge the desired upstream commit into this overlay branch.
2. Run `python3 kimi-code/install.py --check`. Stop if the patch no longer applies or an adapter link breaks.
3. Open [CAPABILITY-MAP.md](CAPABILITY-MAP.md). For every changed upstream path, compare the upstream behavior with the mapped Kimi capability and the current adapter contract.
4. Reconcile changes in a temporary worktree, regenerate `kimi-code.patch`, and update the baseline commits and verification column in the map.
5. Install into an empty temporary directory, validate real skill loading and the affected workflows, then update the managed installation with `--force`.

Do not apply `--force` to hide a failed `--check`. A clean application is evidence of textual compatibility, not proof that the skill still behaves as intended.

## Verification boundaries

The map distinguishes executable checks from draft-only and externally gated checks. In particular:

- Automatic mode verifies safe drafts and stopping, not a completed live HITL interview.
- `kimi -p` does not prove a native user-only `/skill:<name>` invocation. See the interaction adapter.
- `to-spec`, `to-tickets`, and `triage` require human approval before their external changes are applied.
- The wizard receives syntax and static checks only unless a human performs the real provisioning flow.

## Upstream relationship

This is a Kimi-specific distribution, not an upstream pull request. The upstream contribution guide limits pull requests to collaborators, and its scope policy excludes harness-specific branches and native question-tool routing. Keep this overlay in the fork and continue syncing upstream releases through the map.
