# 🗂️ Catalogue

Index curé des ressources **externes** de développement agentique (rien qui s'écrit
à la main ici — ça, c'est le [coffre](../vault/)).

## Fichiers

| Fichier | Contenu |
|---|---|
| [frameworks.md](frameworks.md) | Frameworks agentiques complets (GSD…) |
| [skills.md](skills.md) | Skills réutilisables |
| [agents.md](agents.md) | Définitions d'agents / subagents |
| [hooks.md](hooks.md) | Hooks de cycle de vie |
| [commands.md](commands.md) | Slash commands / prompts |
| [mcp-servers.md](mcp-servers.md) | Serveurs MCP (brique la plus agnostique) |
| [clis-and-tools.md](clis-and-tools.md) | CLIs & outils agentiques |
| [marketplaces.md](marketplaces.md) | Marketplaces / registres de plugins |
| [learning.md](learning.md) | Ressources d'apprentissage & références |

## Format d'une entrée

Copie ce gabarit pour ajouter une ressource :

```markdown
### Nom de la ressource
- **Lien** : https://…
- **Type** : framework / skill / agent / hook / commande / MCP / outil
- **Compatibilité** : agnostique | Claude Code | Cursor | Aider | …
- **Installation** : `npx …` / marketplace / clone / plugin
- **À quoi ça sert** : une ou deux phrases.
- **Notes** : retours d'expérience, pièges, pourquoi je le garde.
```
