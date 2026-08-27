# Serveurs MCP

Le **Model Context Protocol** est la brique la plus **agnostique** : un serveur MCP se
branche indifféremment sur Claude Code, Cursor, et tout client compatible. Privilégie-les.

> Référence protocole & serveurs de référence : `github.com/modelcontextprotocol/servers`
> et `modelcontextprotocol.io`.

---

## Connectés / utilisés

### Connecteurs claude.ai (Google Workspace, Postman…)
- **Type** : MCP (connecteurs claude.ai)
- **Compatibilité** : claude.ai / Claude Code
- **Installation** : via les réglages de connecteurs sur claude.ai (OAuth)
- **À quoi ça sert** : Gmail, Google Calendar, Google Drive, Postman.
- **Notes** : nécessitent une autorisation OAuth en session interactive.

### Serveurs de recherche/docs (référencés par des agents)
- **Exemples vus** : `context7`, `firecrawl`, `exa`, `tavily`, `ref`, `jina`, `perplexity`.
- **Type** : MCP (recherche web, scraping, docs).
- **Compatibilité** : agnostique.
- **À quoi ça sert** : recherche web, extraction de contenu, accès docs pour agents.
- **Notes** : à documenter au fur et à mesure (clé API / endpoint par serveur).

---

<!-- Gabarit :
### Nom
- **Lien / package** :
- **Type** : MCP
- **Compatibilité** : agnostique
- **Installation** : `claude mcp add …` / config client
- **À quoi ça sert** :
- **Notes** : auth requise ?
-->
