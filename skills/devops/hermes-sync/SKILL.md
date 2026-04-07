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
- `scripts/check-korean.py` — pure Korean verifier (Chinese/Hanja/Kana detector)
- `tools/skills_sync.py` — skill synchronization engine (bundled with Hermes)

## pure-korean skill

hermes-sync와 함께, `skills/productivity/pure-korean/` 스킬이 제공됩니다.

이 스킬은:
- 모든 답변에서 한자/중국어/일본어를 0개로 유지
- `scripts/check-korean.py`를 사용하여 텍스트 검증
- 한국어 답변 규칙 및 자주 유입되는 한자어 → 순수 한국어 교체 목록 포함

매 답변 작성 전 로드:
```
/skill pure-korean
```

또는 Herme's cron job이 자동으로 로드합니다.
