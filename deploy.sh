#!/usr/bin/env bash
# Deploy Bruno Brief PWA to GitHub Pages (repo: BrunoTheBaker/bruno-brief)
# Usage: GITHUB_TOKEN=ghp_xxx ./deploy.sh   OR   just run after `gh auth login`
set -euo pipefail
cd "$(dirname "$0")"
REPO="bruno-brief"
GH_USER="BrunoTheBaker"

# 1. Pick auth: explicit env token > gh CLI token
if [[ -n "${GITHUB_TOKEN:-}" ]]; then
  AUTH_HEADER=(-H "Authorization: Bearer $GITHUB_TOKEN")
  echo "Using GITHUB_TOKEN from env"
else
  TOK=$(gh auth token 2>/dev/null || true)
  [[ -z "$TOK" ]] && { echo "❌ No GitHub auth. Run: gh auth login"; exit 1; }
  AUTH_HEADER=(-H "Authorization: Bearer $TOK")
  echo "Using gh CLI token"
fi

# 2. Create repo if missing
CODE=$(curl -s -o /dev/null -w "%{http_code}" "${AUTH_HEADER[@]}" "https://api.github.com/repos/$GH_USER/$REPO")
if [[ "$CODE" == "404" ]]; then
  echo "Creating repo: $REPO"
  curl -s "${AUTH_HEADER[@]}" -X POST "https://api.github.com/user/repos" \
    -d "{\"name\":\"$REPO\",\"private\":false,\"has_issues\":false,\"has_projects\":false}" >/dev/null
fi

# 3. Push files to main
git remote remove origin 2>/dev/null || true
git remote add origin "https://$GH_USER:${TOK:-$GITHUB_TOKEN}@github.com/$GH_USER/$REPO.git"
git branch -M main
git push -u origin main --force || { echo "push failed"; exit 1; }

# 4. Enable GitHub Pages (branch: main, root)
echo "Enabling GitHub Pages..."
curl -s "${AUTH_HEADER[@]}" -X POST \
  "https://api.github.com/repos/$GH_USER/$REPO/pages" \
  -H "Accept: application/vnd.github+json" \
  -d '{"build_type":"legacy","source":{"branch":"main","path":"/"}}' >/dev/null \
  || true   # may 409 if already enabled

echo "✅ Pushed. Pages live at: https://$GH_USER.github.io/$REPO/"
echo "   (also at https://$GH_USER.github.io/$REPO/index.html)"
