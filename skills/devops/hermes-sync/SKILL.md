---
name: hermes-sync
description: Sync Hermes codebase from NousResearch upstream + sync bundled skills to ~/.hermes/skills/. Preserves user-modified skills (never overwrites). Run after git pull to keep skills in sync.
version: 1.0.0
---

# hermes-sync

Sync Hermes agent from upstream (NousResearch) and keep skills synchronized.

## What it does

1. **Fetch + pull** latest from `origin/main` (NousResearch/hermes-agent)
2. **Sync skills** via `tools/skills_sync.py` — bundled skills → `~/.hermes/skills/`
3. **Preserve user modifications** — skills the user has edited are NEVER overwritten
4. **Commit + push** any local changes to `fadak/hermes-agent` fork

## Usage

```bash
cd ~/.hermes/hermes-agent
./scripts/sync-hermes.sh
```

Or run via cron (every 6 hours):
```bash
0 */6 * * * cd ~/.hermes/skills/devops/hermes-sync && ./scripts/sync-hermes.sh >> ~/.hermes/logs/sync.log 2>&1
```

## Key principles

- **Upstream first**: Always builds on latest NousResearch code
- **User modifications preserved**: skills_sync.py manifest tracks which skills you've changed — those are never touched by upstream updates
- **Personal skills**: Skills you create in `~/.hermes/skills/` (not in upstream) stay local, not pushed to fork
- **Separation**: Core code in repo `skills/` = upstream | Personal customizations in `~/.hermes/skills/` = local only

## Files

- `scripts/sync-hermes.sh` — main sync script
- `tools/skills_sync.py` — skill synchronization engine (bundled with Hermes)
