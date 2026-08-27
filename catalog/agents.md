# Agents / subagents

Définitions d'agents spécialisés (un rôle + des outils autorisés) délégables par un orchestrateur.

---

### Agents GSD (`gsd-*`)
- **Source** : fournis par le framework [GSD](frameworks.md) dans `~/.claude/agents/`
- **Type** : agents / subagents
- **Compatibilité** : Claude Code
- **Installation** : via `npx gsd-core`
- **À quoi ça sert** : ~34 agents spécialisés (planner, executor, code-reviewer, debugger,
  roadmapper, researcher, verifier, ui-auditor…) orchestrés par les skills GSD.
- **Notes** : ne pas versionner ici (réinstallables). Mettre au [coffre](../vault/agents/)
  uniquement les agents **faits main**.

---

<!-- Gabarit :
### Nom
- **Lien / source** :
- **Type** : agent
- **Compatibilité** :
- **Installation** :
- **À quoi ça sert** :
- **Notes** :
-->
