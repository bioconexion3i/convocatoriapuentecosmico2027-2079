#!/bin/bash
REPO_DIR="/home/bio/convocatoriapuentecosmico2027-2079"
cd "$REPO_DIR" || exit 1
if [[ -z $(git status --porcelain) ]]; then exit 0; fi
git add -A
git commit -m "⚡ Sincronización automática SOE - $(date '+%Y-%m-%d %H:%M:%S')"
git push origin main 2>&1
