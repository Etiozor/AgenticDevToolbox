# 📦 Coffre

Les artefacts **réellement à toi**, versionnés et portables — recopiables tels quels
sur une nouvelle machine. (Ce qui *s'installe* va au [catalogue](../catalog/), pas ici.)

## Dossiers

| Dossier | Contenu |
|---|---|
| [instructions/](instructions/) | `CLAUDE.md`, `AGENTS.md`, `.cursorrules`, system prompts |
| [settings/](settings/) | Configs portables (préférences, permissions) |
| [skills/](skills/) | Skills écrits main |
| [agents/](agents/) | Agents écrits main |
| [hooks/](hooks/) | Hooks écrits main |
| [commands/](commands/) | Slash commands / prompts maison |
| [templates/](templates/) | Templates / boilerplates de projet |

## ⚠️ Ne jamais committer de secrets

Pas de clés API, tokens, `.env`, ni `.credentials.json`. Le [`.gitignore`](../.gitignore)
en bloque les plus courants — vérifie avant chaque commit.
