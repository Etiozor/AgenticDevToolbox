# Bootstrap — reconstituer une machine à zéro

Objectif : retrouver un environnement de dev agentique fonctionnel en quelques minutes
à partir de ce repo.

## 1. Prérequis

- **Node.js** (pour les CLIs et hooks) et **Git** (Git Bash sous Windows).
- Le CLI agentique voulu — p. ex. **Claude Code** (voir [catalog/clis-and-tools.md](../catalog/clis-and-tools.md)).

## 2. Cloner ce repo

```bash
git clone <url-de-ce-repo> agentic-dev-toolbox
cd agentic-dev-toolbox
```

## 3. Instructions globales

Copie tes instructions perso :

```bash
cp vault/instructions/CLAUDE.md ~/.claude/CLAUDE.md   # Claude Code
```

(Adapte pour `AGENTS.md` / `.cursorrules` selon le CLI.)

Pour n'ajouter qu'un bloc précis (sans écraser le fichier existant) :

```bash
scripts/add-instructions.sh rigueur-intellectuelle [fichier-cible]
```

## 4. Réinstaller les frameworks (catalogue)

Depuis [catalog/frameworks.md](../catalog/frameworks.md) et
[catalog/marketplaces.md](../catalog/marketplaces.md) :

```bash
npx gsd-core            # installe skills + agents + hooks GSD dans ~/.claude
```

Ajoute les marketplaces de plugins voulues, puis active les plugins
(ex. `fabric-skills@fabric-collection`).

## 5. Appliquer les préférences

Le `settings.json` généré par GSD contient le câblage des hooks (chemins absolus, à ne pas
copier depuis une autre machine). **Fusionne** seulement tes préférences portables :

- source : [`vault/settings/claude-code.preferences.json`](../vault/settings/claude-code.preferences.json)
- clés à reporter : `model`, `effortLevel`, `theme`, `tui`, `permissions`.

## 6. Serveurs MCP

Rebranche les serveurs MCP voulus (voir [catalog/mcp-servers.md](../catalog/mcp-servers.md)).
Les connecteurs claude.ai (Gmail, Calendar, Drive, Postman) se ré-autorisent en OAuth
depuis les réglages de connecteurs claude.ai.

## 7. Vérification

- `/graphify` est bien déclenchable (instructions globales OK).
- Les commandes `/gsd-*` répondent (GSD installé).
- Thème/modèle/effort conformes à tes préférences.

---

> Rappel : **aucun secret** dans ce repo. Les clés/tokens se re-saisissent à la main
> sur la nouvelle machine.
