# Frameworks agentiques

Frameworks complets qui apportent tout un workflow (planification, exécution, revue…).

---

### GSD — Get Shit Done
- **Lien** : package npm `gsd-core` _(à compléter : dépôt public si disponible)_
- **Type** : framework de workflow agentique (skills + agents + hooks)
- **Compatibilité** : Claude Code (supporte aussi Cursor via hooks dédiés)
- **Installation** : `npx gsd-core` _(installe skills, agents et hooks dans `~/.claude`)_
- **À quoi ça sert** : workflow structuré discuss → plan → execute → verify → ship,
  avec ~70 skills (`gsd-*`), ~34 agents spécialisés et une suite de hooks (garde de
  commit, monitoring de contexte, statusline, boundary de phase…).
- **Notes** : c'est **la majeure partie** de mon `~/.claude`. Ne pas versionner les fichiers
  individuels ici — se réinstalle proprement. Préférences perso associées : voir
  [`vault/settings/`](../vault/settings/). Profil GSD stocké dans `~/.claude/.gsd-profile`.

---

### ponytail — « lazy senior dev mode »
- **Lien** : `github.com/DietrichGebert/ponytail` · Licence MIT
- **Type** : plugin ruleset (skills + hooks + commandes) — philosophie « le meilleur code
  est celui qu'on n'écrit pas » (YAGNI, stdlib d'abord, pas d'abstraction non demandée)
- **Compatibilité** : **agnostique** — 15+ plateformes (Claude Code, Codex, Cursor,
  Windsurf, Cline, Grok, Kiro, Qoder, opencode…). Version instruction-only pour les autres.
- **Installation** (Claude Code) :
  ```
  claude plugin marketplace add DietrichGebert/ponytail
  claude plugin install ponytail@ponytail
  ```
  Instruction-only (Cursor/Windsurf/…) : copier [`vault/instructions/ponytail-AGENTS.md`](../vault/instructions/ponytail-AGENTS.md).
- **À quoi ça sert** : force la solution la plus simple/courte qui marche via une « échelle de
  décision » (réutiliser > stdlib > natif > dépendance installée > 1 ligne > code minimal).
  Impact annoncé : ~54 % de code en moins, ~20 % moins cher, ~27 % plus rapide.
- **Installé le** : 2026-08-27 · **version** : 4.9.0 · **scope** : user
- **Inventaire** : 6 skills, 3 hooks, 0 agent, 0 MCP · ~983 tok always-on. Détail dans
  [skills.md](skills.md) et [hooks.md](hooks.md). Ruleset agnostique versionné au coffre.

---

<!-- Gabarit :
### Nom
- **Lien** :
- **Type** :
- **Compatibilité** :
- **Installation** :
- **À quoi ça sert** :
- **Notes** :
-->
