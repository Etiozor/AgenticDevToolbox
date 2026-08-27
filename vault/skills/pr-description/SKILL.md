---
name: pr-description
description: 'Génère la description complète d''une Pull Request selon le template {CLIENT_NAME} Data Vault. Analyse le diff Git et produit une description structurée en français: Issue liée, Objectif, Fichiers modifiés (avec emojis ✅❌🔧🔄🏷️), Type de changement Conventional Commits/SemVer, Tests effectués, Risques, Checklist DWA, Reviewers. Utiliser quand l''utilisateur demande: "préparer une PR", "créer une PR", "description de PR", "générer PR", "/pr-description".'
license: MIT
---

# Générateur de Description de Pull Request — {CLIENT_NAME} Data Vault

## Vue d'ensemble

Génère la description complète d'une Pull Request GitHub selon le template standard {CLIENT_NAME} pour les projets Data Vault (DWA Framework, Snowflake SQL). Analyse le diff Git actuel et produit une description structurée, en français, prête à copier dans GitHub.

**Déclenché par** : "préparer une PR", "créer une PR", "description de PR", "générer une PR", `/pr-description`

Si la branche cible n'est pas spécifiée, demander à l'utilisateur de confirmer `develop` (ou `main`/`dev` si `develop` n'existe pas).

## Règles préalables

### Bugs multi-repos

Avant de générer la description, vérifier si la modification touche plusieurs dépôts. Dans ce cas :
- créer une PR distincte par dépôt;
- générer les descriptions dans l'ordre des dépendances;
- mentionner les PR complémentaires dans chaque description.

## Workflow

### 1.1. Analyser les changements Git et identifier les tickets Jira

```bash
# Branche courante et cible
git branch --show-current
git log origin/develop..HEAD --oneline 2>/dev/null || git log origin/main..HEAD --oneline

# Fichiers modifiés (avec statut A/M/D)
git diff origin/develop...HEAD --name-status 2>/dev/null || git diff --name-status HEAD~1

# Diff complet pour analyser les changements
git diff origin/develop...HEAD 2>/dev/null || git diff HEAD~1
```

#### 1.2. Auto-détecter les tickets Jira

Extraire automatiquement les tickets Jira depuis le nom de branche et les messages de commits :

```bash
# Extraire depuis le nom de branche (pattern: PROJET-XXXX)
git branch --show-current

# Extraire depuis les messages de commits de la branche
git log origin/develop..HEAD --format="%s %b" 2>/dev/null | grep -oE '[A-Z]+-[0-9]+'
```

**Logique de décision** :

| Situation | Action |
| --------- | ------ |
| Ticket trouvé dans le nom de branche (ex: `feature/{PROJECT_MRKT}-1321-...`) | Utiliser automatiquement — **TU DOIS** confirmer avec l'utilisateur |
| Ticket(s) trouvé(s) dans les messages de commits | Proposer la liste extraite — demander confirmation |
| Aucun ticket détecté | **Demander à l'utilisateur** : "Quel(s) ticket(s) Jira sont associés à cette PR? (ex: {PROJECT_MRKT}-1321)" |
| Plusieurs tickets différents détectés | Présenter la liste et demander confirmation |

**Format Jira {CLIENT_NAME}** : `https://{JIRA_URL_CLIENT}/browse/{PROJECT_MRKT}-1321`

Les tickets confirmés sont placés dans la section **Issue liée** de la description, en plus ou à la place des références GitHub `#XXX` :

```markdown
## 📋 Issue liée

Jira : [{PROJECT_MRKT}-1321](https://{JIRA_URL_CLIENT}/browse/{PROJECT_MRKT}-1321)
Fixes #(numéro GitHub si applicable)
Related to #(numéro GitHub si applicable)
```

### 2. Cataloguer les changements par fichier

Utiliser le sous-agent `Explore` (thoroughness: **medium**) pour analyser tous les fichiers SQL modifiés en un seul appel — évite N appels #tool:read/readFile (ou `read_file`) individuels lorsque plusieurs fichiers `.sql` sont dans le diff :

```
"Dans le repository {GIT_CLIENT}, pour ces fichiers modifiés: [liste du git diff]
Pour chaque fichier .sql, identifie:
- Type d'objet DWA : HUB_*, SAT_*, LNK_*, D_* (dim), F_* (fait), BV_*, V_* (abstraction)
- Couche : abstraction/, acces/, acces_structuree/, regles_affaires/, depot/
- Colonnes ajoutées (présentes dans la version modifiée mais pas l'originale)
- Colonnes supprimées (présentes dans l'originale mais pas la modifiée)
- Tags COMMENT = 'origine=...' modifiés ou ajoutés
- Corrections de logique visibles (CASE WHEN, filtres, jointures)
Pour les fichiers non-.sql (.xlsx, .py, .md, .cfg): indiquer type seulement.
Retourne: tableau structuré par fichier avec ces informations, prêt pour une description de PR."
```

**Règle d'application** : Utiliser `Explore` si ≥ 2 fichiers `.sql` sont dans le diff. Pour 1 seul fichier `.sql`, #tool:read/readFile (ou `read_file`) direct est préférable.

Sur la base du résultat, assigner les emojis indicateurs pour chaque changement :

| Emoji | Signification |
| ----- | ------------- |
| ✅    | Ajout de colonne, fichier, ou fonctionnalité |
| ❌    | Suppression de colonne ou fonctionnalité |
| 🔧    | Correction de bug, logique, ou format |
| 🔄    | Modification/mise à jour |
| 🏷️   | Correction ou ajout de tags `COMMENT = 'origine=...'` |

#### Fichiers de pilotage Excel (`.xlsx`)

Si un fichier `.xlsx` est dans le diff, **ne pas** se contenter de "🔄 Mise à jour" — extraire et comparer les deux versions pour produire un résumé par table de ce qui a changé.

**Étape 1 — Extraire la version précédente (branche source)**

```powershell
# Remplacer $relPath par le chemin relatif du fichier .xlsx dans git
# ex: "{PROJECT_MRKT}/Sondage/{REPO_PREFIX}-{DV_SYSTEM_02}_DataVault_Sondage_Business/environnement_etl/pilotage/PILOTAGE_{DV_SYSTEM_02}.xlsx"
git show "origin/develop:$relPath" > "$env:TEMP\PILOTAGE_AVANT.xlsx"
```

**Étape 2 — Convertir en Markdown (priorité : MCP MarkItDown)**

Utiliser en priorité le MCP `mcp_microsoft_mar_convert_to_markdown` (outil `convert_to_markdown`) pour convertir les deux fichiers :

```
# Version AVANT
uri: "file:///C:/Windows/Temp/PILOTAGE_AVANT.xlsx"

# Version APRÈS (fichier courant dans le workspace)
uri: "file:///{GIT_CLIENT}/<relPath>"
```

Si le MCP n'est pas disponible ou échoue, utiliser en fallback :

```powershell
python {GIT_CLIENT}\_DEV\Utilitaires\xlsx_to_markdown.py "$env:TEMP\PILOTAGE_AVANT.xlsx" -o "$env:TEMP\pilotage_avant"
python {GIT_CLIENT}\_DEV\Utilitaires\xlsx_to_markdown.py "{GIT_CLIENT}\$relPath" -o "$env:TEMP\pilotage_apres"
```

**Étape 3 — Comparer tous les onglets**

Analyser les onglets **Pilotage - SYSTEME**, **Pilotage - TABLE**, **Pilotage - COLONNE**, **Pilotage - MAPPING**, **Pilotage - MAPPING_COLONNE** et détecter **tout** changement, quelle que soit la colonne concernée :

- Onglet `Pilotage - TABLE` : `NOM_LOGIQUE_TABLE`, `NOM_TABLE_PHYSQ`, `COMPORTEMENT_TABLE` (clusters, index, etc.), `FILTRE_DELTA`, `CD_MODE_CHARG`, `DESCR_TABLE`, nouvelles tables, tables supprimées
- Onglet `Pilotage - COLONNE` : `NOM_COLONNE`, `TYPE_DONNEE`, `TAILLE`, `COMPORTEMENT_COLONNE` (tags origine), `DESC_EXPRESSION_COLONNE`, `IND_SUPPR_SRC`, `IND_CLEF`, `ORDRE_COLONNE`, nouvelles colonnes, colonnes supprimées
- Onglet `Pilotage - MAPPING` / `Pilotage - MAPPING_COLONNE` : nouvelles règles de mapping, suppressions, modifications de clés ou expressions
- Onglet `Pilotage - SYSTEME` : changements de paramètres système

**Étape 4 — Produire un résumé par table**

Ne **pas** lister les valeurs champ-par-champ dans la description de PR. Regrouper les changements **par table logique** en une phrase synthétique par item :

```markdown
### 2. **PILOTAGE_{DV_SYSTEM_02}.xlsx**
**Changements:**
- 🔄 `V_NOM_TABLE_A` — ajout de 3 colonnes, tag origine corrigé sur `NOM_COL`
- 🔄 `V_NOM_TABLE_B` — `FILTRE_DELTA` mis à jour, `COMPORTEMENT_TABLE` : ajout cluster sur `COL_CLE`
- ✅ `V_NOM_TABLE_C` — nouvelle table ajoutée au pilotage
- ❌ `V_NOM_TABLE_D` — table supprimée du pilotage
- 🔧 `V_NOM_TABLE_E` — correction du `TYPE_DONNEE` de `NOM_COL`, colonne `AUTRE_COL` masquée (`IND_SUPPR_SRC = O`)
```

Le niveau de détail doit rester au niveau de la **table** : une ligne par table affectée, avec les types de changements en mots, sans copier les valeurs brutes.

### 3. Déterminer le type de changement

| Situation | Type Conventional Commits | SemVer |
| --------- | ------------------------- | ------ |
| Nouvelle colonne, nouveau fichier SQL, nouvelle variable | `feat:` | MINEURE (X.Y.0) |
| Correction bug, fix de logique, correction tag origine | `fix:` | PATCH (X.Y.Z) |
| Suppression colonne, changement schéma incompatible | `feat!:` / `BREAKING CHANGE:` | MAJEURE (X.0.0) |
| Refactoring sans impact fonctionnel | `refactor:` | — |
| Pilotage ou documentation seulement | `docs:` | — |
| Amélioration performance | `perf:` | PATCH |

**Scope** : Utiliser le nom du projet en majuscules entre parenthèses — ex: `feat({DV_SYSTEM_02}):`, `fix({DV_SYSTEM_01}):`

### 4. Générer la description complète

Produire la description en français en suivant **exactement** la structure ci-dessous (en markdown).

**Titre de la PR** (première ligne, pas dans le corps) :
```
<type>[scope]: <description courte imperative en français, max 72 chars>
```

---

## Structure de la Description

```markdown
# 🔧 [Titre descriptif des changements]

## 📋 Issue liée

Jira : [{PROJECT_MRKT}-XXXX](https://{JIRA_URL_CLIENT}/browse/{PROJECT_MRKT}-XXXX)
Fixes #(numéro GitHub)
Closes #(numéro GitHub)
Related to #(numéro GitHub)

> **Note** : Supprimer les lignes non applicables. Le lien Jira est obligatoire si un ticket existe. `Fixes`/`Closes` ferme l'issue GitHub automatiquement lors du merge.

---

## 🎯 Objectif principal

[Description concise de l'objectif en 2-3 phrases.]

### Contexte métier

[Explication du problème métier résolu, sans jargon technique inutile.]

---

## 🔧 Fichiers modifiés

### 1. **NomFichier.sql** - [Description courte de la vue/table]
**Changements:**
- ✅ **Ajout** de la colonne `NOM_COLONNE` : description fonctionnelle
  - Source: `305:TABLE_SOURCE.COLONNE_SOURCE`
- 🔧 **Correction** [description précise]

### 2. **PILOTAGE_DV_NomProjet.xlsx**
**Changements:**
- 🔄 Mise à jour des métadonnées de colonnes
- 🔧 Correction des définitions dans l'onglet `Pilotage - COLONNE`

### 3. **VARIABLES.SQL**
**Changements:**
- ✅ Ajout de la variable `$VAR_NOM_VARIABLE`

### 4. **ORDRE_EXECUTION.TXT**
**Changements:**
- ✅ Ajout de `NomFichier.sql`

---

## 🏷️ Type de changement

- [ ] 🐛 `fix:` Bug fix - Version **PATCH** (X.Y.Z)
- [ ] ✨ `feat:` Nouvelle fonctionnalité - Version **MINEURE** (X.Y.0)
- [ ] 💥 `BREAKING CHANGE:` Breaking change - Version **MAJEURE** (X.0.0)
- [ ] 📚 `docs:` Documentation seulement
- [ ] 🔧 `refactor:` Refactoring (pas de bug fix, pas de feature)
- [ ] 🎨 `style:` Formatage, espacement (pas de changement logique)
- [ ] ⚡ `perf:` Amélioration de performance
- [ ] ✅ `test:` Ajout ou correction de tests
- [ ] 🧹 `chore:` Maintenance, tâches diverses

**Corrélation SemVer** : `fix:` → PATCH | `feat:` → MINEUR | `BREAKING CHANGE:` → MAJEUR

---

## 🧪 Tests effectués

### Tests manuels Data Vault
- [ ] Validation avec `analyze_dv_priorities.py`
- [ ] Validation de la cohérence du fichier de pilotage
- [ ] Test de chargement complet (full load)
- [ ] Test de chargement incrémental (delta)

### Résultats de tests
- **Nombre de rangées chargées** : X rangées dans TABLE_CIBLE
- **Temps d'exécution** : XX minutes
- **Warnings/Erreurs** : Aucun / [liste]
- **Environnement** : {ENV_DEV} | **Job ETL** : NOM_JOB_vX.Y.Z

### Requêtes de validation exécutées
```sql
-- Vérification du nombre de rangées
SELECT COUNT(*) FROM {DB_ENV_CLIENT}.ACCES.TABLE_CIBLE;
```

---

## ⚠️ Risques et impacts

- **Tables modifiées** : `TABLE_1`, `TABLE_2`
- **Colonnes supprimées** : `NOM_COLONNE` retirée de `TABLE` (déplacée vers `AUTRE_TABLE` si applicable)
- **Breaking changes** : Oui/Non — [détails si Oui]
- **Actions requises** : Mise à jour des rapports utilisant les colonnes supprimées (si applicable)

### Dépendances
- [ ] Aucune dépendance
- [ ] Nécessite déploiement préalable de : PR_#XXX

---

## ✅ Checklist de validation (OBLIGATOIRE)

### Standards de code
- [ ] Code suit les standards **SQL Snowflake** du projet
- [ ] Auto-revue complète effectuée
- [ ] Pas de code commenté inutile (dead code)

### Data Vault et DWA Framework
- [ ] Tous les tags `COMMENT = 'origine=...'` sont présents et corrects
- [ ] Le fichier de pilotage est synchronisé avec les scripts SQL
- [ ] Fichier `ORDRE_EXECUTION.sql` mis à jour (si nouvelles variables)
- [ ] Fichier `VARIABLES.SQL` mis à jour (si nouvelles variables)
- [ ] Aucun problème détecté (`analyze_dv_priorities.py`)

### Documentation
- [ ] La documentation a été mise à jour (si applicable)

### Tests et qualité
- [ ] Tests de chargement réussis (full et/ou delta)
- [ ] Aucun warning critique dans les logs
- [ ] Pas de régression sur les tables existantes

### Processus
- [ ] Branche créée depuis `develop` (ou branche appropriée)
- [ ] Commits suivent **Conventional Commits** (`feat:`, `fix:`, etc.)
- [ ] Aucun fichier sensible (credentials, `.env`) dans le commit
- [ ] Revue par un pair demandée (@mention)

---

## 👥 Reviewers

- @reviewer-technique - Expert Data Vault
- @reviewer-metier - Expert métier domaine

**Points d'attention pour la revue** :
- [Point critique 1 à valider]
- [Logique métier spécifique à vérifier]

---

## 📝 Notes additionnelles

[Information supplémentaire pertinente, références à des discussions, etc.]

### Déploiement
- [ ] Peut être déployé immédiatement après merge
- [ ] Nécessite coordination avec : [Équipe/Système]

---

## 📚 Références

- **Conventional Commits** : [conventionalcommits.org](https://www.conventionalcommits.org/)
- **Semantic Versioning** : [semver.org](https://semver.org/)
- **Documentation DWA** : [Confluence DWA](https://{CONFLUENCE_URL_CLIENT}/spaces/RIAG/pages/165185391/Frameworks+DL+DV)
- **Normes du projet** : `standards.instructions.md`
```

---

### 5. Valider la cohérence Data Vault avant de livrer

- `PILOTAGE_DV_*.xlsx` listé s'il a été modifié
- `VARIABLES.SQL` listé s'il a été modifié
- `ORDRE_EXECUTION.sql` listé s'il a été modifié
- `analyze_dv_priorities.py` coché dans la checklist si des fichiers ont changé
- Aucun secret, credential, ou chemin réseau UNC dans la description

---

## Règles de Formatage

- **Langue** : Français québécois — toujours
- **Temps** : Présent impératif — "Ajoute", "Corrige", "Supprime" (jamais "a ajouté")
- **Noms techniqes** : Toujours entre back-ticks — `D_SONDG_QUESTR.sql`, `NOM_BILLT`, `DV_CLE_HUB_COMM`
- **Chemins** : Nom de fichier seulement, sans chemin complet — `F_SONDG_REPNS.sql` (pas `acces/F_SONDG_REPNS.sql`)
- **Sources supprimées** : Ne jamais inventer de sources — ne lister que ce qui est visible dans le diff

---

## Protocole de Sécurité

- Ne JAMAIS inclure de secrets, tokens, mots de passe, ou clés API dans la description
- Ne JAMAIS inclure de chemins réseau UNC (`\\{SERVEUR_FICHIERS_CLIENT}\...`) dans la description publiée
- Ne JAMAIS inclure de credentials ou numéros de compte de service
- Valider que le diff ne contient pas de fichiers `.env`, `.cfg` avec mots de passe, ou clés privées
