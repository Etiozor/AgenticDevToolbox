#!/usr/bin/env bash
# Ajoute un module d'instructions du coffre au fichier de config du LLM (idempotent).
# Usage : scripts/add-instructions.sh <module> [fichier-cible]
#   module        : nom dans vault/instructions/modules/ (sans .md), ex. rigueur-intellectuelle
#   fichier-cible : défaut ~/.claude/CLAUDE.md (ou AGENTS.md, .cursorrules, ./CLAUDE.md…)
set -euo pipefail

modules="$(dirname "$0")/../vault/instructions/modules"
if [ $# -lt 1 ]; then
  echo "Usage : $0 <module> [fichier-cible]"; echo "Modules :"; ls "$modules" | sed 's/\.md$//; s/^/  /'; exit 1
fi

src="$modules/$1.md"
target="${2:-$HOME/.claude/CLAUDE.md}"
[ -f "$src" ] || { echo "Module introuvable : $src" >&2; exit 1; }

heading="$(head -n1 "$src")"
mkdir -p "$(dirname "$target")"; touch "$target"
if grep -qxF "$heading" "$target"; then
  echo "Déjà présent dans $target ($heading)"; exit 0
fi

{ [ -s "$target" ] && printf '\n'; cat "$src"; } >> "$target"
echo "Ajouté : $1 -> $target"
