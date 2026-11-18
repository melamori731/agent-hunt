#!/usr/bin/env bash
set -euo pipefail
mkdir -p "$HOME/.cursor/skills"
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT
git clone --depth 1 https://github.com/melamori731/marvin.git "$TMP/marvin"
for d in "$TMP/marvin/cursor/skills"/*/; do
  name=$(basename "$d")
  rm -rf "$HOME/.cursor/skills/$name"
  cp -a "$d" "$HOME/.cursor/skills/$name"
done
test -f "$HOME/.cursor/skills/marvin/SKILL.md"
ls -1 "$HOME/.cursor/skills"
