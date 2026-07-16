#!/bin/bash
# Non-destructive publish: run from inside a full clone's pipeline/ dir.
# Regenerates the served index.html from pipeline data and pushes WITHOUT
# clobbering the rest of the repo tree. Token comes from env var GH_PAT.
set -e
PIPE="$(cd "$(dirname "$0")" && pwd)"     # <clone>/pipeline
ROOT="$(cd "$PIPE/.." && pwd)"            # <clone> (repo root, served by Pages)
: "${GH_PAT:?GH_PAT not set}"
cd "$PIPE"
python3 build_all.py
python3 gen_v2.py
cp advancement_contacts.html "$ROOT/index.html"   # self-contained page (data inline)
cp r1_stem_advancement_contacts.csv "$ROOT/r1_stem_advancement_contacts.csv" 2>/dev/null || true
touch "$ROOT/.nojekyll"
cd "$ROOT"
git config user.email "amit@rndcatalyst.com"
git config user.name  "ag811987"
git add -A
if git diff --cached --quiet; then echo "nothing to commit"; exit 0; fi
git commit -qm "${1:-Outreach sync}"
git push "https://ag811987:${GH_PAT}@github.com/ag811987/r1-stem-advancement.git" HEAD:main 2>&1 | sed "s/${GH_PAT}/[REDACTED]/g"
echo "PUSH_EXIT=${PIPESTATUS[0]}"
