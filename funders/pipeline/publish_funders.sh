#!/bin/bash
# Non-destructive publish of the funders tracker to the repo under /funders/.
# Run from inside a full clone's funders/pipeline dir. Token via env GH_PAT.
set -e
PIPE="$(cd "$(dirname "$0")" && pwd)"     # <clone>/funders/pipeline
FROOT="$(cd "$PIPE/.." && pwd)"           # <clone>/funders
ROOT="$(cd "$FROOT/.." && pwd)"           # <clone> (repo root)
: "${GH_PAT:?GH_PAT not set}"
cd "$PIPE"
python3 build_funders.py
python3 gen_funders.py
cp funders.html "$FROOT/index.html"
cp research_funders_contacts.csv "$FROOT/research_funders_contacts.csv"
cd "$ROOT"
git config user.email "amit@rndcatalyst.com"
git config user.name  "ag811987"
git add -A
if git diff --cached --quiet; then echo "nothing to commit"; exit 0; fi
git commit -qm "${1:-Funders outreach sync}"
git push "https://ag811987:${GH_PAT}@github.com/ag811987/r1-stem-advancement.git" HEAD:main 2>&1 | sed "s/${GH_PAT}/[REDACTED]/g"
echo "PUSH_EXIT=${PIPESTATUS[0]}"
