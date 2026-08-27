# Hooks de cycle de vie

Scripts déclenchés automatiquement par le CLI sur des événements (SessionStart, PreToolUse,
PostToolUse, Stop, PreCompact…). Câblés dans `settings.json`.

---

### Hooks GSD
- **Source** : fournis par le framework [GSD](frameworks.md) dans `~/.claude/hooks/`
- **Type** : hooks (Node.js / Bash)
- **Compatibilité** : Claude Code
- **Installation** : via `npx gsd-core` (câblage auto dans `settings.json`)
- **À quoi ça sert** : garde de commit, monitoring de contexte, statusline, boundary de
  phase, scanner d'injection à la lecture, workflow-guard, mise à jour graphify…
- **Notes** : les entrées `hooks` de mon `settings.json` pointent vers ces scripts avec des
  **chemins absolus Windows** → non portables tels quels. Voir la config portable dans
  [`vault/settings/`](../vault/settings/) et le [bootstrap](../docs/bootstrap.md).

---

### Hooks ponytail
- **Source** : plugin [ponytail](frameworks.md)
- **Type** : hooks (harness-only — aucun coût de contexte modèle)
- **Compatibilité** : agnostique (via plugin)
- **Installation** : `claude plugin install ponytail@ponytail`
- **À quoi ça sert** : `SessionStart`, `SubagentStart`, `UserPromptSubmit` — injectent
  automatiquement le ruleset « lazy dev » au bon moment.

---

<!-- Gabarit (pour un hook fait main, à mettre au coffre) :
### Nom
- **Événement** : SessionStart | PreToolUse | PostToolUse | …
- **Type** : hook (langage)
- **Compatibilité** :
- **À quoi ça sert** :
- **Notes** :
-->
