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

### MemPalace — système de mémoire (serveur MCP, 44 outils)
- **Lien** : `github.com/MemPalace/mempalace` · image `ghcr.io/mempalace/mempalace`
- **Type** : MCP (mémoire) + CLI + API Python + hooks d'auto-save
- **Compatibilité** : **agnostique** — Claude Code, Codex CLI, Gemini CLI, Cursor, clients MCP
- **Installation** : `uv tool install mempalace` (ou `pipx install mempalace`, ou Docker) ;
  puis `mempalace init ~/projects/monapp`. Requiert Python 3.9+, ~300 Mo (embeddings).
- **À quoi ça sert** : mémoire locale « verbatim » (sans résumé) + recherche sémantique.
  Structure en *wings* (personnes/projets) → *rooms* (sujets) → *drawers* (contenu brut),
  graphe de connaissances temporel, coordination d'agents, diaries.
- **Objets réutilisables** :
  - **Serveur MCP** — 44 outils (lecture/écriture palace, requêtes de graphe, navigation cross-wing, diaries).
  - **Hooks d'auto-save** — rétention périodique (Claude Code, Codex, Cursor) → voir [hooks.md](hooks.md).
  - **Backends enfichables** — ChromaDB (défaut), SQLite, Milvus, Qdrant, PostgreSQL/pgvector
    (interface `mempalace/backends/base.py`).
  - **CLI + API Python**, abstraction d'embeddings (local ou API compatible OpenAI),
    commandes *mine* (extraction depuis fichiers de projet et transcripts).
- **Notes** : mémoire **locale, zéro appel API** (96,6 % R@5 sur LongMemEval). Déjà intégré à
  mon workflow GSD via les skills/agents `gsd-mempalace-*` (capture/recall/curator).

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
