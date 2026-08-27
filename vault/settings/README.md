# Settings portables

Configs réutilisables, **débarrassées des chemins machine et des secrets**.

## Contenu

- **`claude-code.preferences.json`** — mes préférences Claude Code (model, effort, thème,
  TUI, permissions). Extrait portable de `~/.claude/settings.json`.

## Comment réappliquer

Ne **pas** écraser bêtement `~/.claude/settings.json` : il contient le câblage des hooks GSD
(chemins absolus) régénéré par l'installeur. À la place :

1. Installe GSD (`npx gsd-core`) → il recrée les blocs `hooks`/`statusLine`.
2. Fusionne les clés de `claude-code.preferences.json` (model, effortLevel, theme, tui,
   permissions) dans le `settings.json` généré.

Détails : [`docs/bootstrap.md`](../../docs/bootstrap.md).
