# Skills réutilisables

Capacités packagées (un `SKILL.md` + ressources) déclenchables à la demande.

---

### graphify
- **Lien** : local `~/.claude/skills/graphify/SKILL.md` _(écosystème GSD)_
- **Type** : skill
- **Compatibilité** : Claude Code
- **Installation** : fourni avec GSD ; déclencheur `/graphify`
- **À quoi ça sert** : transforme n'importe quelle entrée (code, docs, papiers, images,
  vidéos) en graphe de connaissances persistant (god nodes, détection de communautés,
  requêtes/chemins/explications).
- **Notes** : câblé dans mon `CLAUDE.md` global (voir [`vault/instructions/`](../vault/instructions/)).

---

### fabric-skills (Microsoft Skills for Fabric)
- **Lien** : `github.com/microsoft/skills-for-fabric`
- **Type** : collection de skills (plugin)
- **Compatibilité** : Claude Code (via marketplace de plugins)
- **Installation** : marketplace `fabric-collection` → plugin `fabric-skills@fabric-collection`
- **À quoi ça sert** : ~40 skills pour Microsoft Fabric (Eventhouse, Dataflows, Spark,
  Warehouse, Power BI/FabricIQ, Activator, migrations Databricks/HDInsight/Synapse…).
- **Notes** : voir [marketplaces.md](marketplaces.md) pour la source.

---

### Skills ponytail (`/ponytail*`)
- **Lien** : `github.com/DietrichGebert/ponytail` _(voir [frameworks.md](frameworks.md))_
- **Type** : skills (6)
- **Compatibilité** : agnostique (via plugin ou instruction-only)
- **Installation** : `claude plugin install ponytail@ponytail`
- **À quoi ça sert** : `ponytail` (mode principal, intensité), `ponytail-review` (revue de
  code), `ponytail-audit`, `ponytail-debt` (dette), `ponytail-gain` (métriques),
  `ponytail-help`.
- **Notes** : ~983 tok always-on ; coût on-invoke par skill listé via `claude plugin details ponytail`.

---

### powerbi-audit & powerbi-documentation (maison)
- **Source** : faites main — versionnées au coffre [`vault/skills/`](../vault/skills/)
- **Type** : skills (2)
- **Compatibilité** : Claude (skills génériques)
- **Installation** : copier le dossier dans l'emplacement de skills du client
  (ex. Claude Desktop `local-agent-mode-sessions/.../skills/`, ou `~/.claude/skills/`).
- **À quoi ça sert** : `powerbi-audit` audite un modèle sémantique Power BI ;
  `powerbi-documentation` le documente (tables, mesures, relations, colonnes). Toutes deux
  incluent des règles de sécurité (interdiction de lire `.pbix`, `.pbi/`, `cache.abf`,
  `localSettings.json`, `.env`…).
- **Notes** : elles vivaient dans un dossier de **session Claude Desktop** (volatile) → mises
  au coffre pour être portables. Description de `powerbi-documentation` corrigée au passage
  (elle dupliquait celle d'audit).

---

### git-commit · pr-description · doc-converter (Azure DevOps — iA_agentic_starter_packs)
- **Source** : `dev.azure.com/agiledssazure/iA_agentic_starter_packs`
  (`GitHub_CoPilot/.github/skills/`) — versionnées au coffre [`vault/skills/`](../vault/skills/)
- **Type** : skills (3) + utilitaires Python
- **Compatibilité** : agnostique (format SKILL.md) — pensées GitHub Copilot / Claude
- **Installation** : copier le dossier dans l'emplacement de skills du client
- **À quoi ça sert** :
  - `git-commit` (MIT) — commit conventionnel : détection type/scope, staging intelligent,
    message généré depuis le diff. Déclencheur `/commit`.
  - `pr-description` (MIT) — génère une description de PR structurée (template DWA Data Vault,
    en français). Déclencheur `/pr-description`. ⚠️ spécifique client (placeholders `{CLIENT_NAME}`).
  - `doc-converter` (proprietary, org) — convertit Office → Markdown pour lecture IA.
    Scripts réels co-localisés dans [`vault/skills/doc-converter/scripts/`](../vault/skills/doc-converter/scripts/) :
    `docx_to_markdown.py`, `xlsx_to_markdown.py` (+ requirements + `README_convertisseurs.md`).
    Deps : `pip install python-docx Pillow openpyxl`.
- **Notes** : le `SKILL.md` de `doc-converter` référence des chemins client
  (`{GIT_CLIENT}\_DEV\Utilitaires\`) — à adapter selon la machine. Le convertisseur inverse
  `md_to_docx.py` (Markdown → Word) existe dans le repo source mais a été **exclu** (hors périmètre
  « conversion en markdown »).

---

<!-- Gabarit :
### Nom
- **Lien** :
- **Type** : skill
- **Compatibilité** :
- **Installation** :
- **À quoi ça sert** :
- **Notes** :
-->
