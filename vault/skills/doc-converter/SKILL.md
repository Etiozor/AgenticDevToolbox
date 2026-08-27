---
name: doc-converter
description: |
  Convertit les documents Office en Markdown pour une lecture optimale par l'IA.
  Deux scripts : docx_to_markdown.py (Word .docx) et xlsx_to_markdown.py (Excel .xlsx).
  Gere automatiquement la sortie selon la localisation du fichier (local ou reseau UNC).
  Pour les fichiers de pilotage DWA Excel, cherche TOUJOURS dans depot/ avant pilotage/.
  Toujours repondre en francais.

  Declenche par : "/doc-converter", "convertis ce fichier", "xlsx vers markdown",
  "docx vers markdown", "lire le pilotage", "convertir Excel en Markdown",
  "convertir Word en Markdown", "lire le fichier de pilotage", "convertir la documentation",
  "converti ce Word", "converti ce Excel", "lire ce fichier Office".

  Utilisable par : utilisateurs, agents, skills.
license: proprietary
allowed-tools:
  - run_in_terminal
  - file_search
  - read_file
  - vscode/askQuestions
---

# Skill : doc-converter

Convertit des fichiers Office (.docx, .xlsx) en Markdown pour lecture par l'IA.

## Regles de priorite pour les fichiers de pilotage

**REGLE ABSOLUE** : Pour les fichiers de pilotage DWA, chercher TOUJOURS dans `depot/` avant `pilotage/`.

```powershell
# Etape 1 - PRIORITE 1 : Chercher dans depot/
ls "\\{SERVEUR_FICHIERS_CLIENT}\dfsa\TALEND\DEVL\BI\environnement_etl\{ENV_DEV}\{nom_repo}\pilotage\depot\*.xlsx"

# Etape 2 - PRIORITE 2 : Si vide, chercher dans pilotage/
ls "\\{SERVEUR_FICHIERS_CLIENT}\dfsa\TALEND\DEVL\BI\environnement_etl\{ENV_DEV}\{nom_repo}\pilotage\*.xlsx"
```

**Raison** : `depot/` contient la version generee/actualisee par le framework DWA (toujours plus recente).

## Conversion Word (.docx) vers Markdown

```powershell
# Fichier local (sortie automatique au meme endroit)
python {GIT_CLIENT}\_DEV\Utilitaires\docx_to_markdown.py "CHEMIN_VERS_FICHIER.docx"

# Fichier reseau UNC (sortie automatique dans _working)
python {GIT_CLIENT}\_DEV\Utilitaires\docx_to_markdown.py "\\serveur\partage\fichier.docx"

# Avec dossier de sortie personnalise
python {GIT_CLIENT}\_DEV\Utilitaires\docx_to_markdown.py "CHEMIN_FICHIER.docx" -o "C:\chemin\sortie"
```

## Conversion Excel (.xlsx) vers Markdown

```powershell
# Fichier de pilotage distant (sortie automatique dans _working)
python {GIT_CLIENT}\_DEV\Utilitaires\xlsx_to_markdown.py "\\{SERVEUR_FICHIERS_CLIENT}\dfsa\TALEND\DEVL\BI\environnement_etl\{ENV_DEV}\{DV_SYSTEM_01}_DataVault_Qualtrics\pilotage\PILOTAGE_{DV_SYSTEM_01}.xlsx"
# => Sortie : {GIT_CLIENT}\_DEV\_working\conversion_PILOTAGE_{DV_SYSTEM_01}\PILOTAGE_{DV_SYSTEM_01}.md
```

## Gestion automatique de la sortie

| Source | Sortie |
|--------|--------|
| Fichier sur `C:\` | Meme endroit que la source |
| Fichier reseau (UNC `\\`) | `{GIT_CLIENT}\_DEV\_working\conversion_{nom}\` |
| Option `--output` ou `-o` | Dossier specifie |

## Verification de la necessite de reconversion (MD5)

Avant de convertir, verifier si une version convertie existe deja et si elle est encore valide :
1. Lire l'en-tete metadonnees du fichier .md existant (contient le hash MD5)
2. Comparer le hash MD5 avec le fichier source actuel
3. Si different → reconvertir. Si identique → reutiliser.

## Dependances Python

```powershell
pip install python-docx Pillow openpyxl
```

## Documentation complete

`{GIT_CLIENT}\_DEV\Utilitaires\README_convertisseurs.md`
