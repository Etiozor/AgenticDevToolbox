# Agentic Dev Toolbox

Un **hub personnel et agnostique** pour le développement agentique. Il référence et stocke
tout le matériel réutilisable — skills, agents, hooks, commandes, serveurs MCP, règles,
frameworks et outils — indépendamment d'un LLM (Claude, GPT, Gemini…) ou d'un CLI
(Claude Code, Cursor, Aider, Codex CLI, Gemini CLI…) en particulier.

Objectif : **repartir en quelques minutes** sur une nouvelle machine ou un nouveau projet,
sans réinventer sa configuration ni perdre ses outils.

---

## Deux rôles

Ce repo est **hybride** :

- 🗂️ **`catalog/`** — le *catalogue*. Un index curé de ressources **externes** (frameworks,
  projets GitHub, marketplaces, serveurs MCP, outils) avec, pour chaque entrée, ce que c'est,
  à quoi ça sert, sa compatibilité, et **comment l'installer/le réutiliser**.
- 📦 **`vault/`** — le *coffre*. Les artefacts **réellement à toi**, versionnés, que tu peux
  recopier tels quels : instructions (`CLAUDE.md`, `AGENTS.md`…), settings, skills, agents,
  hooks, commandes et templates maison.

> Règle de tri : si une ressource **s'installe** (npm, marketplace, plugin), on la **catalogue**.
> Si c'est un fichier **écrit à la main** et portable, on le met au **coffre**.

---

## Principe d'agnosticité

Le repo s'organise par **concept**, pas par éditeur. La plupart des écosystèmes agentiques
exposent les mêmes briques sous des noms différents. Table d'équivalence :

| Concept (ce repo)        | Claude Code            | Cursor                 | Autres / standard            |
|--------------------------|------------------------|------------------------|------------------------------|
| **Instructions / règles**| `CLAUDE.md`            | `.cursorrules`, Rules  | `AGENTS.md`, system prompt   |
| **Skills**               | `~/.claude/skills/`    | —                      | prompt packs réutilisables   |
| **Agents / subagents**   | `~/.claude/agents/`    | agents                 | définitions de rôles         |
| **Hooks (cycle de vie)** | `settings.json` hooks  | —                      | scripts pre/post-événement   |
| **Commandes / prompts**  | slash commands         | commands               | prompts paramétrés           |
| **Outils externes**      | **MCP**                | **MCP**                | **MCP** (universel)          |
| **Marketplaces/plugins** | plugins                | extensions             | registres                    |

Chaque entrée du catalogue indique sa **compatibilité** : `agnostique`, ou l'écosystème ciblé.
Les **serveurs MCP** sont la brique la plus agnostique : privilégie-les quand c'est possible.

---

## Structure

```
.
├── catalog/                 # Index de ressources externes (par concept)
│   ├── frameworks.md        # Frameworks agentiques (GSD…)
│   ├── skills.md            # Skills réutilisables
│   ├── agents.md            # Définitions d'agents / subagents
│   ├── hooks.md             # Hooks de cycle de vie
│   ├── commands.md          # Slash commands / prompts
│   ├── mcp-servers.md       # Serveurs MCP (le plus agnostique)
│   ├── clis-and-tools.md    # CLIs & outils agentiques
│   ├── marketplaces.md      # Marketplaces / registres de plugins
│   └── learning.md          # Ressources d'apprentissage & références
├── vault/                   # Artefacts réutilisables réels (à toi)
│   ├── instructions/        # CLAUDE.md, AGENTS.md, .cursorrules…
│   ├── settings/            # Configs portables (préférences)
│   ├── skills/              # Skills maison
│   ├── agents/              # Agents maison
│   ├── hooks/               # Hooks maison
│   ├── commands/            # Commandes maison
│   └── templates/           # Templates / boilerplates
└── docs/
    └── bootstrap.md         # Reconstituer une machine à zéro
```

---

## Démarrage rapide

- **Nouvelle machine ?** → suis [`docs/bootstrap.md`](docs/bootstrap.md).
- **Ajouter une ressource externe ?** → dans le bon fichier de [`catalog/`](catalog/).
- **Ajouter un artefact à toi ?** → dans le bon dossier de [`vault/`](vault/).

Voir aussi [`catalog/README.md`](catalog/README.md) et [`vault/README.md`](vault/README.md).
