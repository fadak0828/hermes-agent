#!/bin/bash
# sync-hermes.sh — Hermes upstream sync + skills sync + personal push
# Usage: ./scripts/sync-hermes.sh [--dry-run]
#
# Flow:
#   1. git fetch upstream (NousResearch)
#   2. git pull (fast-forward main from NousResearch)
#   3. Run skills_sync (bundled → ~/.hermes/skills/)
#   4. git add + commit any changes
#   5. git push to fadak fork
#
# Key principle:
#   NousResearch updates are pulled automatically.
#   User-modified skills (in ~/.hermes/skills/) are NEVER overwritten —
#   skills_sync.py manifest tracks which skills user has changed.
#   Custom personal skills (not in upstream) stay local, not pushed to fork.

set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SKILLS_SYNC="$REPO_DIR/tools/skills_sync.py"
GIT="git -C $REPO_DIR"

DRY_RUN=false
if [[ "${1:-}" == "--dry-run" ]]; then
  DRY_RUN=true
  echo "[dry-run] DRY RUN — no changes will be made"
fi

echo "=========================================="
echo "  Hermes Sync — $(date '+%Y-%m-%d %H:%M:%S')"
echo "=========================================="

# ── Step 1: Fetch upstream ──────────────────────────────────────
echo ""
echo "[1/5] Fetching upstream (NousResearch)..."
$GIT fetch origin

# Check if there are upstream changes
LOCAL_AHEAD=$($GIT rev-list --count HEAD..origin/main 2>/dev/null || echo "0")
if [[ "$LOCAL_AHEAD" == "0" ]]; then
  echo "  ✓ Already up-to-date with upstream"
else
  echo "  ↓ $LOCAL_AHEAD commits behind upstream"
fi

# ── Step 2: Pull upstream ──────────────────────────────────────
echo ""
echo "[2/5] Pulling upstream into main..."
if [[ "$DRY_RUN" == "true" ]]; then
  echo "  [dry-run] Would: git pull --ff-only origin main"
else
  # Only fast-forward — never rebase or merge our changes onto main
  # Our changes live in ~/.hermes/skills/ (local only)
  if !$GIT pull --ff-only origin main 2>/dev/null; then
    echo "  ⚠ Fast-forward failed. Checking for local commits..."
    # If we have local commits, rebase them on top of origin/main
    LOCAL_COMMITS=$($GIT rev-list --count origin/main..HEAD 2>/dev/null || echo "0")
    if [[ "$LOCAL_COMMITS" -gt 0 ]]; then
      echo "  → Rebasing local changes onto new upstream..."
      $GIT rebase origin/main || {
        echo "  ⚠ Rebase conflict! Please resolve manually."
        exit 1
      }
    fi
  fi
  echo "  ✓ Fast-forward / rebase complete"
fi

# ── Step 3: Sync tools ────────────────────────────────────────
echo ""
echo "[3/5] Syncing bundled skills to ~/.hermes/skills/..."
echo "  (User-modified skills are preserved — see .bundled_manifest)"
if [[ "$DRY_RUN" == "true" ]]; then
  echo "  [dry-run] Would run: python3 $SKILLS_SYNC"
else
  cd "$REPO_DIR"
  source venv/bin/activate 2>/dev/null || true
  python3 "$SKILLS_SYNC"
fi

# Also copy check-korean.py to ~/.hermes/bin/ (if present in repo)
if [[ -f "$REPO_DIR/scripts/check-korean.py" ]]; then
  echo ""
  echo "[3b/5] Syncing check-korean.py to ~/.hermes/bin/"
  mkdir -p ~/.hermes/bin/
  cp "$REPO_DIR/scripts/check-korean.py" ~/.hermes/bin/
  chmod +x ~/.hermes/bin/check-korean.py
  echo "  ✓ check-korean.py installed"
fi

# ── Step 4: Commit pushed skills ────────────────────────────────
echo ""
echo "[4/5] Checking for commit-worthy changes..."
CHANGES=$($GIT status --porcelain board/ 'skills/productivity/paperclip-board/' 2>/dev/null | grep -v "^??")
if [[ -n "$CHANGES" ]]; then
  echo "  Changes found:"
  echo "$CHANGES"
  if [[ "$DRY_RUN" == "true" ]]; then
    echo "  [dry-run] Would commit these changes"
  else
    $GIT add board/ 'skills/productivity/paperclip-board/'
    $GIT commit -m "sync: update Board governance layer from local

$(date '+%Y-%m-%d')"
    echo "  ✓ Committed"
  fi
else
  echo "  ✓ No changes to commit"
fi

# ── Step 5: Push to fork ───────────────────────────────────────
echo ""
echo "[5/5] Pushing to fork (fadak/hermes-agent)..."
if [[ "$DRY_RUN" == "true" ]]; then
  echo "  [dry-run] Would: git push origin main"
else
  $GIT push origin main
  echo "  ✓ Pushed to fadak/hermes-agent"
fi

echo ""
echo "=========================================="
echo "  Sync complete — $(date '+%Y-%m-%d %H:%M:%S')"
echo "=========================================="
echo ""
echo "Summary:"
echo "  NousResearch upstream  → followed (auto-pull)"
echo "  ~/.hermes/skills/     → synced (user mods preserved)"
echo "  fadak/hermes-agent    → pushed"
echo ""
echo "To run manually:"
echo "  cd ~/.hermes/hermes-agent && ./scripts/sync-hermes.sh"
echo ""
echo "To schedule as cron (every 6 hours):"
echo "  0 */6 * * * cd ~/.hermes/hermes-agent && ./scripts/sync-hermes.sh >> ~/.hermes/logs/sync.log 2>&1"
