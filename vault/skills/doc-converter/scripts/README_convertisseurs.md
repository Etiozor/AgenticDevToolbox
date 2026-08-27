# Table des matières

- [Table des matières](#table-des-matières)
- [Convertisseurs de Documents vers Markdown](#convertisseurs-de-documents-vers-markdown)
  - [Scripts disponibles](#scripts-disponibles)
    - [1. `docx_to_markdown.py` - Convertisseur Word vers Markdown](#1-docx_to_markdownpy---convertisseur-word-vers-markdown)
      - [Installation des dépendances](#installation-des-dépendances)
      - [Utilisation](#utilisation)
      - [Gestion automatique du dossier de sortie](#gestion-automatique-du-dossier-de-sortie)
      - [Fonctionnalités](#fonctionnalités)
      - [Sortie](#sortie)
    - [2. `xlsx_to_markdown.py` - Convertisseur Excel vers Markdown](#2-xlsx_to_markdownpy---convertisseur-excel-vers-markdown)
      - [Installation des dépendances](#installation-des-dépendances-1)
      - [Utilisation](#utilisation-1)
      - [Gestion automatique du dossier de sortie](#gestion-automatique-du-dossier-de-sortie-1)
      - [Fonctionnalités](#fonctionnalités-1)
      - [Sortie](#sortie-1)
    - [3. `md_to_docx.py` — Convertisseur Markdown vers Word](#3-md_to_docxpy--convertisseur-markdown-vers-word)
      - [Installation des dépendances](#installation-des-dépendances-2)
      - [Utilisation](#utilisation-2)
      - [Gestion automatique du dossier de sortie](#gestion-automatique-du-dossier-de-sortie-2)
      - [Fonctionnalités](#fonctionnalités-2)
      - [Éléments non supportés](#éléments-non-supportés)
      - [Sortie](#sortie-2)
  - [Avantages du format Markdown pour l'IA](#avantages-du-format-markdown-pour-lia)
    - [Comparaison des formats](#comparaison-des-formats)
    - [Bénéfices spécifiques](#bénéfices-spécifiques)
  - [Workflow recommandé](#workflow-recommandé)
    - [Pour la documentation DWA (Word)](#pour-la-documentation-dwa-word)
    - [Pour les fichiers de pilotage (Excel)](#pour-les-fichiers-de-pilotage-excel)
    - [Pour partager un document Markdown sous Word](#pour-partager-un-document-markdown-sous-word)
  - [Dépannage](#dépannage)
    - [Erreur: Package non installé](#erreur-package-non-installé)
    - [Erreur: Fichier introuvable](#erreur-fichier-introuvable)
    - [Images ne s'affichent pas (docx\_to\_markdown / xlsx\_to\_markdown)](#images-ne-saffichent-pas-docx_to_markdown--xlsx_to_markdown)
    - [Blocs Mermaid non rendus en image (md\_to\_docx)](#blocs-mermaid-non-rendus-en-image-md_to_docx)
    - [Extension `.md` incorrecte (md\_to\_docx)](#extension-md-incorrecte-md_to_docx)
  - [Historique des versions](#historique-des-versions)
    - [Version 1.0](#version-10)
    - [Version 2.0](#version-20)
  - [Références](#références)

---

# Convertisseurs de Documents vers Markdown

Ce dossier contient des scripts Python pour convertir différents types de documents Microsoft Office vers le format Markdown (.md), optimisé pour l'analyse par IA.

## Scripts disponibles

### 1. `docx_to_markdown.py` - Convertisseur Word vers Markdown

Convertit les fichiers Microsoft Word (.docx) en Markdown.

#### Installation des dépendances

`pip install python-docx Pillow`

#### Utilisation

`# Avec chemin du fichier en argument (détection automatique du dossier de sortie)`
`python C:\git\_DEV\Utilitaires\docx_to_markdown.py "chemin\vers\fichier.docx"`

`# Avec dossier de sortie personnalisé`
`python C:\git\_DEV\Utilitaires\docx_to_markdown.py "chemin\vers\fichier.docx" --output "C:\chemin\sortie"`

`# Ou avec l'option courte -o`
`python C:\git\_DEV\Utilitaires\docx_to_markdown.py "chemin\vers\fichier.docx" -o "C:\chemin\sortie"`

`# Sans argument (le script demandera le chemin)`
`python C:\git\_DEV\Utilitaires\docx_to_markdown.py`

#### Gestion automatique du dossier de sortie

**Règle importante:** Le script détecte automatiquement si le fichier source est local ou distant.
**Fichier local** (sur `C:\`) → Le fichier `.md` est créé dans le **même dossier** que le source
**Fichier distant** (réseau UNC, ex: `\\serveur\partage\`) → Le fichier `.md` est créé dans `C:\git\_DEV\_working\conversion_{nom_fichier}\`
**Dossier personnalisé** (avec `--output`) → Le fichier `.md` est créé dans le dossier spécifié

**Exemples:**

`# Fichier local - sortie au même endroit`
`python docx_to_markdown.py "C:\Docs\rapport.docx"`
`# → Crée: C:\Docs\rapport.md`

`# Fichier réseau - sortie automatique dans _working`
`python docx_to_markdown.py "\\serveur\partage\documents\rapport.docx"`
`# → Crée: C:\git\_DEV\_working\conversion_rapport\rapport.md`

`# Dossier personnalisé`
`python docx_to_markdown.py "\\serveur\docs\rapport.docx" -o "C:\MesDocs"`
`# → Crée: C:\MesDocs\rapport.md`

#### Fonctionnalités

✅ Extraction et préservation des images
✅ Génération automatique de Table des Matières (TOC)
✅ Préservation du formatage (gras, italique, titres)
✅ Conversion des tableaux
✅ Préservation des liens hypertextes
✅ Métadonnées du document (MD5 hash, dates, auteur, révision)
✅ Support des styles de titre français et anglais

#### Sortie

Fichier `.md` dans le même dossier que le source
Dossier `{nom_fichier}_images/` avec les images extraites
En-tête de métadonnées incluant hash MD5 pour détecter les changements

### 2. `xlsx_to_markdown.py` - Convertisseur Excel vers Markdown

Convertit les fichiers Microsoft Excel (.xlsx, .xlsm) en Markdown.

#### Installation des dépendances

`pip install openpyxl Pillow`

#### Utilisation

`# Avec chemin du fichier en argument (détection automatique du dossier de sortie)`
`python C:\git\_DEV\Utilitaires\xlsx_to_markdown.py "chemin\vers\fichier.xlsx"`

`# Avec dossier de sortie personnalisé`
`python C:\git\_DEV\Utilitaires\xlsx_to_markdown.py "chemin\vers\fichier.xlsx" --output "C:\chemin\sortie"`

`# Ou avec l'option courte -o`
`python C:\git\_DEV\Utilitaires\xlsx_to_markdown.py "chemin\vers\fichier.xlsx" -o "C:\chemin\sortie"`

`# Sans argument (le script demandera le chemin)`
`python C:\git\_DEV\Utilitaires\xlsx_to_markdown.py`

#### Gestion automatique du dossier de sortie

**Règle importante:** Le script détecte automatiquement si le fichier source est local ou distant.
**Fichier local** (sur `C:\`) → Le fichier `.md` est créé dans le **même dossier** que le source
**Fichier distant** (réseau UNC, ex: `\\serveur\partage\`) → Le fichier `.md` est créé dans `C:\git\_DEV\_working\conversion_{nom_fichier}\`
**Dossier personnalisé** (avec `--output`) → Le fichier `.md` est créé dans le dossier spécifié

**Exemples:**

`# Fichier local - sortie au même endroit`
`python xlsx_to_markdown.py "C:\Docs\tableau.xlsx"`
`# → Crée: C:\Docs\tableau.md`

`# Fichier réseau - sortie automatique dans _working`
`python xlsx_to_markdown.py "\\ad.network.ca\dfsa\TALEND\DEVL\BI\PILOTAGE_DVSONDT01.xlsx"`
`# → Crée: C:\git\_DEV\_working\conversion_PILOTAGE_DVSONDT01\PILOTAGE_DVSONDT01.md`

`# Dossier personnalisé`
`python xlsx_to_markdown.py "\\serveur\docs\tableau.xlsx" -o "C:\MonAnalyse"`
`# → Crée: C:\MonAnalyse\tableau.md`

#### Fonctionnalités

✅ Conversion de toutes les feuilles du classeur
✅ Génération automatique de Table des Matières (liste des feuilles)
✅ Conversion des données en tableaux Markdown
✅ Extraction des images (si présentes)
✅ Affichage des valeurs calculées des formules
✅ Métadonnées du document (MD5 hash, dates, créateur)
✅ Formatage des dates et nombres
✅ Support des fichiers .xlsx et .xlsm

#### Sortie

Fichier `.md` dans le même dossier que le source
Dossier `{nom_fichier}_images/` avec les images extraites (si présentes)
En-tête de métadonnées incluant hash MD5 et liste des feuilles
Chaque feuille devient une section avec ancre de navigation

### 3. `md_to_docx.py` — Convertisseur Markdown vers Word

Convertit n'importe quel fichier Markdown (`.md`) en document Microsoft Word (`.docx`).

#### Installation des dépendances

`pip install python-docx`
`npm install -g @mermaid-js/mermaid-cli  # optionnel — pour rendu Mermaid en image PNG`

#### Utilisation

`# Conversion simple (sortie dans le même dossier que la source)`
`python C:\git\_DEV\Utilitaires\md_to_docx.py "chemin\vers\fichier.md"`

`# Avec dossier de sortie personnalisé`
`python C:\git\_DEV\Utilitaires\md_to_docx.py "fichier.md" -o "C:\chemin\sortie"`

`# Sans rendu Mermaid (code brut conservé, mmdc non requis)`
`python C:\git\_DEV\Utilitaires\md_to_docx.py "fichier.md" --no-mermaid`

#### Gestion automatique du dossier de sortie

**Règle identique aux autres convertisseurs :**
**Fichier local** (sur `C:\`) → Le fichier `.docx` est créé dans le **même dossier** que la source
**Fichier distant** (réseau UNC, ex: `\\serveur\partage\`) → Le fichier `.docx` est créé dans `C:\git\_DEV\_working\conversion_{nom_fichier}\`
**Dossier personnalisé** (avec `-o`) → Le fichier `.docx` est créé dans le dossier spécifié

**Exemples :**

`# Fichier local - sortie au même endroit`
`python md_to_docx.py "C:\Docs\guide.md"`
`# → Crée: C:\Docs\guide.docx`

`# Fichier local avec chemin complet`
`python "C:\git\_DEV\Utilitaires\md_to_docx.py" "C:\git\_DEV\dev - Cybermetrie\BIMRK1541_analyse_GA4_mobile\ANALYSE_BIMRK1541_GA4_Mobile_DL_Voute.md"`

`# Fichier réseau - sortie automatique dans _working`
`python md_to_docx.py "\\serveur\partage\docs\guide.md"`
`# → Crée: C:\git\_DEV\_working\conversion_guide\guide.docx`

`# Dossier personnalisé`
`python md_to_docx.py "guide.md" -o "C:\MonDossier"`
`# → Crée: C:\MonDossier\guide.docx`

#### Fonctionnalités

✅ Titres H1–H4, paragraphes, listes à puces et numérotées
✅ Tableaux Markdown (première ligne en en-tête gras)
✅ Blockquotes (indenté, bordure bleue, italique)
✅ Blocs de code (Courier New 9pt, fond gris clair)
✅ Inline : **gras**, *italique*, `` `code` ``, [liens](url) **cliquables**
✅ Blocs Mermaid → image PNG centrée (si `mmdc`/Node.js disponible)
⚠️  Blocs Mermaid → code brut + avertissement (si `mmdc` absent ou `--no-mermaid`)
✅ En-tête centré (nom du fichier source) et pied de page (numéro de page)
✅ Marges 2.5 cm, police Calibri 11 pt
✅ Détection et rapport des éléments non convertibles (HTML brut, YAML front matter, footnotes, task lists)
✅ Auto-détection du dossier de sortie (local / réseau UNC / `-o`)
✅ YAML front matter automatiquement ignoré
✅ Séparateurs horizontaux (`---`)

#### Éléments non supportés

Les éléments suivants sont **détectés et signalés** dans la console et dans une section en fin de document, mais leur conversion est partielle ou absente :

| Élément | Comportement |
| --- | --- |
| YAML front matter (---) | Ignoré (exclu du document) |
| Balises HTML brutes (`, `, etc.) | Balise supprimée, texte conservé |
| Notes de bas de page ([^1]:) | Non converties (limitation python-docx) |
| Task lists (- [x] texte) | Converties en liste à puces (case ignorée) |
| Blocs Mermaid sans mmdc | Code brut conservé avec avertissement |


#### Sortie

Fichier `.docx` avec en-tête (nom du fichier) et pied de page (numéro)
Section « ⚠️ Éléments non convertis » en fin de document (si applicable)
Affichage console du statut de chaque étape

## Avantages du format Markdown pour l'IA

### Comparaison des formats

| Critère | Word (.docx) | Excel (.xlsx) | MHT | Markdown (.md) |
| --- | --- | --- | --- | --- |
| Lisibilité IA | ❌ Non lisible | ❌ Non lisible | ⚠️ 98% pollution HTML | ✅ 100% clean |
| Taille relative | Baseline | Baseline | 38x plus gros | 1x (optimal) |
| Encodage | Binaire | Binaire | Quoted-printable | UTF-8 |
| Recherche | ❌ Impossible | ❌ Impossible | ⚠️ Difficile | ✅ Excellente |
| Métadonnées | ❌ Non accessible | ❌ Non accessible | ❌ Non accessible | ✅ En-tête visible |
| Images | ❌ Embarquées | ❌ Embarquées | ❌ Base64 | ✅ Fichiers séparés |
| TOC | ⚠️ Manuel | ⚠️ N/A | ❌ Aucune | ✅ Auto-générée |

### Bénéfices spécifiques

**Détection de changements** : Hash MD5 dans les métadonnées permet de savoir quand reconvertir
**Navigation optimale** : Table des matières avec liens cliquables vers chaque section
**Recherche efficace** : Format texte pur permet grep_search, semantic_search, read_file
**Portabilité** : Compatible avec tout éditeur de texte et viewer Markdown
**Versioning Git** : Diff visible des changements de contenu

## Workflow recommandé

### Pour la documentation DWA (Word)

**Première conversion** (Word → Markdown, pour analyse IA)
   ```powershell
   python C:\git\_DEV\Utilitaires\docx_to_markdown.py "C:\git\_DEV\Documentation_DWA\Documentation Framework DL.docx"
   ```

**Vérifier si reconversion nécessaire**

Lire l'en-tête du fichier `.md` existant
Comparer le Hash MD5 avec le fichier `.docx` actuel
Si différent → reconvertir avec la commande ci-dessus

**Utiliser le fichier Markdown**

Format recommandé pour l'IA (38x plus efficace que MHT)
Suivre AUSSI les liens web dans le document

### Pour les fichiers de pilotage (Excel)

**Conversion** (Excel → Markdown, pour analyse IA)
   ```powershell
   python C:\git\_DEV\Utilitaires\xlsx_to_markdown.py "chemin\vers\PILOTAGE_*.xlsx"
   ```

**Utilisation**

Analyse rapide du contenu des feuilles
Recherche de définitions en double
Vérification des configurations

### Pour partager un document Markdown sous Word

**Conversion simple** (Markdown → Word, pour partage ou impression)
   ```powershell
   python C:\git\_DEV\Utilitaires\md_to_docx.py "chemin\vers\document.md"
   ```

**Avec rendu Mermaid** (nécessite Node.js + mmdc installé)
   ```powershell
   # Vérifier si mmdc est disponible
   mmdc --version
   # Conversion avec rendu Mermaid en images PNG
   python C:\git\_DEV\Utilitaires\md_to_docx.py "document.md"
   ```

**Sans mmdc** (rendu Mermaid désactivé)
   ```powershell
   python C:\git\_DEV\Utilitaires\md_to_docx.py "document.md" --no-mermaid
   ```

**Utilisation typique** — Guide Confluence ou documentation DWA
   ```powershell
   # Convertir le guide dv-check vers Word pour le partager en réunion
   python C:\git\_DEV\Utilitaires\md_to_docx.py `
     "C:\git\_DEV\Documentation CoPilot\GUIDE_CONFLUENCE_dv-check-hooks.md"
   ```

## Dépannage

### Erreur: Package non installé

**Symptôme:**

`ERREUR: Le package 'python-docx' n'est pas installé.`

**Solution:**

`# Tous les packages requis`
`pip install python-docx Pillow openpyxl`

### Erreur: Fichier introuvable

**Symptôme:**

`FileNotFoundError: Le fichier ... n'existe pas.`

**Solution:**

Vérifier le chemin du fichier
Utiliser des guillemets si le chemin contient des espaces
Utiliser le chemin absolu complet

### Images ne s'affichent pas (docx_to_markdown / xlsx_to_markdown)

**Cause:** Le dossier `{nom_fichier}_images/` n'est pas au bon endroit

**Solution:**

S'assurer que le dossier d'images est dans le même répertoire que le fichier `.md`
Vérifier que les images ont bien été extraites lors de la conversion

### Blocs Mermaid non rendus en image (md_to_docx)

**Symptôme:** Les diagrammes Mermaid apparaissent comme du code brut dans le `.docx`
**Cause:** `mmdc` (Mermaid CLI) n'est pas installé ou introuvable dans le PATH
**Solution:**

`# Vérifier si Node.js est installé`
`node --version`

`# Installer Mermaid CLI globalement`
`npm install -g @mermaid-js/mermaid-cli`

`# Vérifier que mmdc est accessible`
`mmdc --version`

**Cas particulier — `mmdc` installé mais introuvable (dossier npm global absent du PATH) :**

`npm list -g` confirme `@mermaid-js/mermaid-cli` installé et le fichier `mmdc.cmd` existe bien sur disque, mais `shutil.which('mmdc')`/`shutil.which('mmdc.cmd')` (utilisé par `_detect_mmdc()`) retourne `None` car le dossier d'installation globale npm (`%APPDATA%\npm`, ex. `C:\Users\<utilisateur>\AppData\Roaming\npm`) n'est pas dans la variable `PATH`.
Résultat : **tous** les diagrammes Mermaid du document tombent en fallback code brut (pas seulement un diagramme en particulier), et aucune image n'apparaît dans `word/media` du `.docx` généré.

Diagnostic rapide :

`# Localiser le dossier npm global`
`npm root -g`

`# Vérifier si ce dossier (un niveau au-dessus de node_modules) est dans le PATH`
`$env:PATH -split ';' | Select-String -SimpleMatch 'npm'`

Solution — ajouter le dossier npm global au `PATH` de façon **permanente** (variable utilisateur, pas besoin d'être admin) :

`[Environment]::SetEnvironmentVariable('PATH', $env:PATH + ';' + (Split-Path (npm root -g) -Parent), 'User')`

Fermer et rouvrir le terminal (ou VS Code) pour que le changement soit pris en compte. Pour un correctif temporaire (session courante seulement, sans persister) :

`$env:PATH += ";$(Split-Path (npm root -g) -Parent)"`

*Si Node.js n'est pas disponible, utiliser `--no-mermaid` pour éviter les avertissements : ```powershell python md_to_docx.py "document.md" --no-mermaid ```*

### Extension `.md` incorrecte (md_to_docx)

**Symptôme:**

`ValueError: Le fichier doit être un .md (reçu : .txt)`

**Solution:** Renommer le fichier avec l'extension `.md`, ou vérifier que le chemin fourni pointe bien vers un fichier Markdown.

## Historique des versions

### Version 1.0

Création du convertisseur Word → Markdown (`docx_to_markdown.py`)
Création du convertisseur Excel → Markdown (`xlsx_to_markdown.py`)
Support complet des métadonnées avec MD5 hash
Génération automatique de TOC
Extraction et encodage URL des images
Support multi-feuilles pour Excel

### Version 2.0

Ajout du convertisseur Markdown → Word (`md_to_docx.py` v2.0.0 — Thot, Mythologie égyptienne)
Architecture classe `MdToDocx` (argparse CLI, auto-détection chemin local/réseau)
Rendu Mermaid via `mmdc` → PNG inline dans Word (fallback code brut si mmdc absent)
Hyperliens cliquables dans le document Word (manipulation XML python-docx)
En-tête (nom du fichier) et pied de page (numéro de page) automatiques
Marges 2.5 cm, police Calibri 11 pt
Détection et rapport des éléments non convertibles (HTML, YAML, footnotes, task lists)

## Références

**Documentation python-docx**: <https://python-docx.readthedocs.io/>
**Documentation openpyxl**: <https://openpyxl.readthedocs.io/>
**Mermaid CLI (mmdc)**: <https://github.com/mermaid-js/mermaid-cli>
**Mermaid — syntaxe des diagrammes**: <https://mermaid.js.org/>
**Markdown Guide**: <https://www.markdownguide.org/>
**OOXML — spécification des champs Word**: <https://learn.microsoft.com/en-us/openspecs/office_standards/ms-oi29500/>
