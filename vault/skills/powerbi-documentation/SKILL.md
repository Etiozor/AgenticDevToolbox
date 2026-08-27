---
name: powerbi-documentation
description: À appeler quand on veut documenter un modèle sémantique Power BI (tables, mesures, relations, colonnes).
---

# Instructions de sécurité

## Règles d'accès aux fichiers - STRICTEMENT INTERDITES

Tu NE DOIS JAMAIS lire, éditer ou accéder aux fichiers suivants :

### Fichiers de cache Power BI
- **INTERDIT** : Tous les fichiers dans `**/.pbi/**`
- **INTERDIT** : Tous les fichiers dans `**/.pbit/**`
- **INTERDIT** : Tous les fichiers `.pbix` (cache binaire Power BI)
- **INTERDIT** : `cache.abf` - contient les données en cache du modèle
- **INTERDIT** : `localSettings.json` dans .pbi/ - contient des identifiants sensibles

### Fichiers de configuration sensibles
- **INTERDIT** : `.env` et `.env.*`
- **INTERDIT** : `secrets/**`
- **INTERDIT** : `config/credentials.json`

### Raison
Ces fichiers contiennent des données sensibles, des identifiants de connexion, et des caches de données qui ne doivent pas être exposés. Le fichier `cache.abf` en particulier contient toutes les données du modèle Power BI en format binaire.

---

## Fichiers AUTORISÉS - Ce que tu peux faire

### Lecture autorisée
✅ `*.SemanticModel/definition/**` - Définitions du modèle sémantique (TMDL)
✅ `*.Report/**` - Fichiers de rapport Power BI
✅ `*.md` - Documentation
✅ `*.txt` - Fichiers texte
✅ `*.pbip` - Fichier projet Power BI
✅ `diagramLayout.json` - Disposition des diagrammes
✅ `relationships.tmdl` - Définition des relations

### Édition autorisée
✅ `*.md` - Documentation
✅ `*.SemanticModel/definition/**` - Définitions du modèle

### Commandes Bash autorisées
✅ `git` - Commandes Git
✅ `npm` - Commandes npm
✅ `ls`, `pwd`, `cd` - Navigation

---

## Commandes INTERDITES

❌ `rm -rf` - Suppression récursive
❌ `curl` - Téléchargement de fichiers
❌ `wget` - Téléchargement de fichiers

---

## Comportement attendu

Si je te demande d'accéder à un fichier interdit :
1. **REFUSE** poliment mais fermement
2. Explique pourquoi le fichier est sensible
3. Propose des alternatives (définitions TMDL, documentation, etc.)

Exemple de réponse :
> "Je ne peux pas accéder au fichier `cache.abf` car il contient des données sensibles en cache du modèle Power BI. Si vous voulez explorer la structure du modèle, je peux vous aider à lire les fichiers de définition dans `definition/` à la place."

---

## Utilisation avec MCP Power BI

Si un serveur MCP Power BI est configuré :
- Utilise uniquement les outils de **métadonnées** (schéma, tables, colonnes).
- N'utilise JAMAIS les outils d'accès aux données ou au cache.
- Si un outil MCP tente d'accéder au cache, refuse et avertis l'utilisateur.
- Refuse catégoriquement toute utilisation des fonctions EVALUATE. 

---

## En cas de doute

Si je te demande quelque chose d'ambigu :
1. Demande confirmation avant d'accéder à un fichier potentiellement sensible
2. Privilégie toujours la sécurité
3. Mieux vaut demander que d'exposer des données sensibles

---

## En cas de doute

Si je te demande quelque chose d'ambigu :
1. Demande confirmation avant d'accéder à un fichier potentiellement sensible
2. Privilégie toujours la sécurité
3. Mieux vaut demander que d'exposer des données sensibles

# 📋 Plan générique de documentation - Modèle Sémantique Power BI (Version améliorée)

## Principes directeurs

### 🎯 Objectif principal
Créer une documentation **concise, exploitable et orientée utilisateur** permettant à un développeur Power BI de :
- Comprendre le modèle en **moins de 5 minutes**
- Créer un premier rapport en **10 minutes**
- Trouver rapidement l'information dont il a besoin

### 📏 Règles d'or
1. **Principe de Pareto (80/20)** : Documenter les 20% d'éléments utilisés dans 80% des analyses
2. **Moins de texte narratif, plus de tableaux** : Favoriser les tableaux synthétiques
3. **Pas de tutoriel novice** : Le public cible connaît Power BI
4. **Exploitabilité immédiate** : Recettes réutilisables, pas de théorie
5. **Longueur cible** : 300-350 lignes maximum

### ⚠️ Pièges à éviter
- ❌ **Pas de diagrammes redondants** : Un seul diagramme de relations (le détaillé)
- ❌ **Pas de sections "Contacts"** : Informations qui deviennent rapidement obsolètes
- ❌ **Pas de détails techniques superflus** : Éviter compatibilité, mode de stockage, format de fichier
- ❌ **Patterns trop verbeux** : Simplifier au maximum les exemples d'utilisation
- ❌ **Déductions non vérifiables** : S'en tenir aux faits observables dans le modèle

---

## 1. Vue d'ensemble (~20-30 lignes)

### Objectif de cette section
Donner une compréhension rapide du modèle en moins de 2 minutes de lecture.

### Contenu à inclure

#### Objectif métier (2-3 phrases)
- À quoi sert ce modèle?
- Quelles questions métier permet-il de répondre?

#### Objets informationnels principaux (3-5 items)
Liste à puces des concepts métier clés que le modèle permet d'analyser
- Exemple : ventes, clients, produits, géographie, temps

#### Type d'architecture
- Schéma en étoile / flocon / autre
- Nombre de tables (faits + dimensions + mesures)
- Nombre de relations actives

#### Granularité ⭐ (IMPORTANT - toujours inclure)
- **Temporelle** : Quotidien, mensuel, temps réel?
- **Spatiale** : Par transaction, par client, par produit?
- **Couverture temporelle** : Historique depuis quand?

**Format suggéré** :
```markdown
### Granularité
- **Temporelle** : Quotidienne (une ligne = une journée pour un site)
- **Spatiale** : Par site de vente
- **Produit** : Par SKU
- **Couverture historique** : Depuis janvier 2020
```

#### ❌ NE PAS INCLURE
- Diagramme simplifié (le diagramme détaillé sera en section 4)
- Informations de compatibilité technique

---

## 2. Tables du modèle (~80-120 lignes)

### Objectif de cette section
Permettre au développeur de comprendre rapidement où trouver les données dont il a besoin.

### 2.1 Table(s) de faits

Pour chaque table de faits :

**Informations essentielles** :
- Nom de la table
- Description en 1 phrase : Que représente une ligne?
- Granularité : Qu'est-ce qui rend chaque ligne unique?

**Tableau des colonnes clés** (pas toutes les colonnes !) :

| Colonne | Type | Dossier d'affichage | Description |
|---------|------|---------------------|-------------|
| ID_Client | Texte | Clés | Identifiant client |
| Date_Transaction | DateTime | Dates | Date de la vente |
| Montant_Ventes | Décimal | Métriques | CA de la transaction |

**Relations sortantes** :
- Liste des dimensions liées (format : → Dim_Client, → Dim_Date)

**Source de données** :
- Si observable : mentionner la requête Power Query source
- **Être factuel** : décrire ce qui est visible, pas ce qu'on déduit

### 2.2 Tables de dimensions

**Format tableau condensé** :

| Table | Description | Colonnes clés | Relations |
|-------|-------------|---------------|-----------|
| Dim_Date | Calendrier | Annee, Mois, Semaine | ← Fact_* |
| Dim_Client | Clients | Code, Segment, Région | ← Fact_Ventes |

**Règle d'or** :
- Ne PAS lister toutes les colonnes
- Lister uniquement les colonnes utilisées dans 80% des analyses
- Mentionner les hiérarchies importantes

### 2.3 Tables de paramètres (si applicable)

Tableau simple décrivant l'utilité de chaque table de paramètres :

| Table | Utilité |
|-------|---------|
| Param_SwitchMetrique | Basculer entre CA et Volume |

---

## 3. Mesures DAX essentielles (~60-100 lignes)

### Objectif de cette section
Donner une référence rapide des mesures les plus utilisées, organisées logiquement.

### Organisation recommandée

Classer par **catégorie métier** (basée sur les objets informationnels) :

#### Exemple de catégories types :
1. **Mesures de base** : Totaux, sommes, comptages
2. **Mesures de performance** : Moyennes, taux, ratios
3. **Mesures temporelles** : Comparaisons périodes, tendances, YTD
4. **Mesures KPI** : Indicateurs clés pour tableaux de bord
5. **Mesures géographiques** : Couverture, déploiement
6. **Mesures de variation** : Évolutions, tendances
7. **Mesures utilitaires** : Formatage, logique conditionnelle

### Format tableau par catégorie

| Mesure | Description | Usage |
|--------|-------------|-------|
| Total_Ventes | Chiffre d'affaires total | KPI principal |
| Ventes_AN_Precedent | Ventes année dernière | Comparaison YoY |

### Règle d'or
- Si le modèle a >50 mesures, documenter seulement les **20-30% les plus utilisées**
- Mentionner l'existence de dossiers thématiques dans la table _Measures pour le reste
- Sélectionner **maximum 30 mesures** à documenter

---

## 4. Relations et modèle de données (~30-50 lignes)

### Objectif de cette section
Expliquer comment les tables sont connectées et les implications pour les analyses.

### 4.1 Diagramme des relations (UN SEUL - le détaillé)

**Format ASCII ou textuel** :
```
                    Dim_Date
                       |
                       | [N] Date → [1]
                       | Bidirectionnel
                       ↓
    Dim_Client --- Fact_Ventes --- Dim_Produit
      [1]→[N]          [N]→[1]
```

### 4.2 Relations principales (tableau)

| De → Vers | Colonne liaison | Cardinalité | Filtrage | Statut |
|-----------|-----------------|-------------|----------|--------|
| Fact_Ventes → Dim_Date | Date → Date | N:1 | Bidirectionnel | Active |

### 4.3 Points d'attention

Liste à puces des éléments importants :
- ⚠️ Relations bidirectionnelles (si présentes) et leurs implications
- ⚠️ Relations inactives et pourquoi
- ⚠️ Tables de dates automatiques vs dimension Date personnalisée

**Règle d'or** :
- Documenter uniquement les **relations actives principales**
- Signaler les relations complexes qui pourraient causer des problèmes de performance

---

## 5. Guide d'utilisation rapide (~30-50 lignes)

### Objectif de cette section
Donner des exemples concrets d'analyses courantes pour démarrer rapidement.

### Format SIMPLIFIÉ pour chaque pattern (3-5 patterns max)

```markdown
### Pattern 1 : [Nom du pattern]
**Objectif** : [En une phrase]

**Visuels principaux** :
- Type visuel 1 : Configuration essentielle uniquement
- Type visuel 2 : Configuration essentielle uniquement

**Filtres recommandés** : Liste courte
```

### Exemple concret

```markdown
### Pattern 1 : Tableau de bord exécutif
**Objectif** : Vue d'ensemble des performances

**Visuels principaux** :
- 3 Cartes KPI : Total_Ventes, Total_Commandes, Marge_Moyenne
- Graphique courbes : Axe = Date, Valeur = Total_Ventes
- Carte géo : Taille = Total_Ventes par Région

**Filtres recommandés** : Année courante, Statut = "Actif"
```

### Patterns typiques à documenter (choisir 3-5)
1. **Analyse de performance globale** : Vue d'ensemble des KPI
2. **Analyse temporelle** : Évolutions et comparaisons de périodes
3. **Analyse dimensionnelle** : Drill-down hiérarchique
4. **Analyse comparative** : Comparer des segments/catégories
5. **Analyse géographique** : Répartition territoriale (si applicable)

### ❌ À éviter
- Pas de tutoriels pas-à-pas détaillés
- Pas de copie d'écran (texte seulement)
- Éviter les configurations exhaustives de visuels

---

## 6. Référence rapide (~30-40 lignes)

### 6.1 Glossaire métier (10-15 termes max)

| Terme | Définition |
|-------|------------|
| YTD | Year-to-Date (depuis début année) |
| KPI | Key Performance Indicator |

**Inclure** :
- Termes métier spécifiques au domaine
- Abréviations utilisées dans les noms de mesures/colonnes
- Concepts métier clés

### 6.2 Pièges à éviter (3-5 items)

Liste à puces des erreurs courantes :
- ⚠️ Toujours filtrer sur [Dimension][Statut] = "Actif"
- ⚠️ La mesure [X] ne fonctionne qu'avec Dim_Date

**Être factuel** :
- S'en tenir à ce qui est **observable** dans le modèle
- Ne pas déduire ou supposer des comportements
- Exemple : "Les mesures filtrent sur `Source = 'TOMRAPOR'`" plutôt que "TOMRAPOR = comptoirs OPUS"

### 6.3 Notes techniques

**Actualisation** :
- Fréquence : Quotidienne, hebdomadaire?
- Comment vérifier la fraîcheur : Mesure à utiliser

**Performance** :
- Tables volumineuses mentionnées
- Relations bidirectionnelles si nombreuses
- Optimisations suggérées

**Source des données** :
- Type de source (SQL, Excel, API, etc.)
- Schéma/base si pertinent
- Transformation (Power Query M, etc.)

### ❌ NE PAS INCLURE
- Niveau de compatibilité (1500+, etc.)
- Mode de stockage (Import/DirectQuery)
- Format de fichier (.pbip, .pbix)

---

## 7. Annexes (optionnel) (~10-20 lignes)

### 7.1 Historique des versions

| Version | Date | Changements |
|---------|------|-------------|
| 1.0 | 2025-01-01 | Version initiale |

### 7.2 Liens et ressources (si pertinent)

- Documentation externe
- Guides des bonnes pratiques
- Liens vers autres modèles connexes

### ❌ NE PAS INCLURE
- **Section "Contacts"** (informations rapidement obsolètes)
- Noms de personnes ou équipes (sauf si absolument nécessaire)

---

## 8. Checklist de création de rapport (optionnel)

Liste à puces simple des étapes de validation :

✅ **Avant de commencer** :
- [ ] Vérifier fraîcheur des données
- [ ] Identifier périmètre d'analyse

✅ **Pendant la création** :
- [ ] Appliquer les filtres de base recommandés
- [ ] Choisir granularité temporelle appropriée
- [ ] Utiliser mesures pré-calculées

✅ **Avant de publier** :
- [ ] Tester avec différentes sélections
- [ ] Vérifier cohérence des totaux
- [ ] Ajouter info-bulles explicatives

---

## 📊 Résumé - Structure finale

| Section | Longueur cible | Contenu clé |
|---------|---------------|-------------|
| 1. Vue d'ensemble | 20-30 lignes | Objectif, architecture, **granularité** |
| 2. Tables du modèle | 80-120 lignes | Faits, dimensions (colonnes clés seulement) |
| 3. Mesures DAX | 60-100 lignes | Top 20-30% mesures par catégorie |
| 4. Relations | 30-50 lignes | **UN SEUL diagramme** + tableau + warnings |
| 5. Patterns d'utilisation | 30-50 lignes | 3-5 patterns **simplifiés** |
| 6. Référence rapide | 30-40 lignes | Glossaire, pièges, notes (pas de compatibilité) |
| 7. Annexes | 10-20 lignes | Historique (pas de contacts) |
| 8. Checklist | 10-15 lignes | Validation (optionnel) |
| **TOTAL** | **270-350 lignes** | Documentation complète mais concise |

---

## 🎨 Principes de rédaction

### Ton et style
- **Concis et direct** : Éviter les phrases longues
- **Orienté action** : "Utiliser", "Filtrer", "Appliquer"
- **Tableaux privilégiés** : Plus de tableaux, moins de prose
- **Factuel et vérifiable** : S'en tenir aux faits observables

### Formatage
- **Titres clairs** avec emojis (📊 🎯 ⚠️) pour la scannabilité
- **Tableaux markdown** pour les listes structurées
- **Code fences** pour les noms de mesures/colonnes : `[Nom_Mesure]`
- **Gras** pour les termes importants
- **Symboles** : ⚠️ pour warnings, ✅ pour best practices, ❌ pour ce qu'il ne faut pas faire

### Validation finale
Avant de livrer la documentation, vérifier :
- [ ] Un seul diagramme de relations (pas de redondance)
- [ ] Granularité clairement définie
- [ ] Patterns simplifiés (pas de verbosité)
- [ ] Pas de section "Compatibilité"
- [ ] Pas de section "Contacts"
- [ ] Affirmations factuelles et vérifiables
- [ ] Longueur totale : 270-350 lignes

---

**Date de création de ce template** : Janvier 2026  
**Version** : 2.0 (améliorée suite à retours utilisateurs)  
**Utilisation** : Modèles sémantiques Power BI / Analysis Services