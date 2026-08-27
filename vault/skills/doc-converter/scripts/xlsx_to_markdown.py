"""
Script de conversion de fichiers Microsoft Excel (.xlsx) vers Markdown (.md)

Version: 1.7.1 - Maat: Corrections flake8
Date: 9 mars 2026
Auteur: Philippe Chayer

Changements v1.7.1 (PATCH):
- CORRECTION flake8: Suppression des imports inutilisés
  (os, List, Tuple, get_column_letter, PIL.Image)
- CORRECTION flake8: f-string sans placeholder (ligne print) converti en str normal
- CORRECTION flake8: Lignes trop longues wrapées

Changements v1.7:
Nom mythologique: Maat (mythologie égyptienne)
Raison: Déesse égyptienne de la vérité, de l'ordre et de l'harmonie, symbolisant
        l'équilibre parfait. Comme Maat qui établit l'ordre cosmique, cette version
        établit l'ordre dans les données en éliminant le vide superflu et ne
        conservant que l'essentiel.
- RANGÉES VIDES: Détection et élimination des rangées vides à la fin des onglets
- OPTIMISATION: Conversion uniquement des données réelles
- PROPRETÉ: Fichiers markdown sans rangées vides inutiles
- MÉTHODE: Nouvelle fonction _find_last_data_row() pour détection précise

Changements v1.6:
Nom mythologique: Hathor (mythologie égyptienne)
Raison: Déesse égyptienne de la joie et de la musique, souvent représentée
        avec un miroir qui reflète la réalité. Comme Hathor qui montre ce
        qui existe vraiment, cette version montre EXACTEMENT où se trouvent
        les graphiques dans chaque feuille.
- NOTES INLINE: Insertion de notes immédiatement après l'en-tête de feuille
- DOUBLE VISIBILITÉ: Section globale + notes inline par feuille
- FORMAT BLOCKQUOTE: Notes en blockquote (> ⚠️) pour visibilité maximale
- POSITION PRÉCISE: L'utilisateur voit les graphiques AVANT le tableau de données

Changements v1.5:
Nom mythologique: Anubis (mythologie égyptienne)
Raison: Dieu égyptien de l'embaumement et gardien des tombes, symbolisant
        la préservation et la documentation complète de TOUS les objets,
        même ceux qui ne peuvent pas être convertis. Anubis veille sur
        les graphiques "perdus" pendant la conversion.
- GRAPHIQUES: Détection des graphiques présents sur chaque feuille
- DOCUMENTATION GLOBALE: Section "Graphiques non convertis détectés" au début du fichier
- DOCUMENTATION LOCALE: Notes dans chaque feuille pour documenter les graphiques
- INFORMATION: Type, titre et position des graphiques documentés
- AVERTISSEMENT: Note claire que les graphiques ne peuvent pas être convertis

Changements v1.4:
Nom mythologique: Seshat (mythologie égyptienne)
Raison: Déesse égyptienne de l'écriture, des calculs et de l'architecture,
        partenaire de Thot. Elle mesure et enregistre tout avec précision,
        symbolisant la conversion complète de TOUS les types de liens Excel.
- LIENS: Amélioration de la gestion des hyperliens
- LIENS INTERNES: Support complet des liens vers cellules (location)
- LIENS EXTERNES: Support URLs web, fichiers et mailto
- ROBUSTESSE: Détection correcte des types de liens
- CORRECTION: Gestion améliorée des cas edge

Changements v1.3:
Nom mythologique: Thot (mythologie égyptienne)
Raison: Le dieu de l'écriture, de la sagesse et des calculs,
        symbolisant la conversion de données structurées et de
        tableaux Excel vers format documentation.
- VERSIONNEMENT: Ajout convention de nommage mythologique
- STANDARDISATION: Conformité avec python.instructions.md
- DOCUMENTATION: Format de version standardisé avec nom mythologique

Changements v1.2:
- FIX: Compatibilité cross-platform Windows/Linux pour chemins
- Remplacement détection hardcodée 'C:\\' par détection
  UNC/montages réseau
- working_base déterminé dynamiquement depuis __file__ au lieu de
  C:\\git
- Support chemins UNC Windows (\\\\server\\share) et montages Linux
  (/mnt/, /net/)

Description:
    Convertit un fichier .xlsx en fichier .md (markdown) en préservant:
    - Le contenu de toutes les feuilles
    - Les tableaux (formatés en markdown)
    - Les formules (affichées comme valeurs calculées)
    - Les hyperliens (convertis en format markdown)
    - Les métadonnées du fichier
    - Les images (si présentes)

Usage:
    python xlsx_to_markdown.py chemin/vers/fichier.xlsx

    OU (sans argument - va demander le chemin):
    python xlsx_to_markdown.py

Dépendances:
    pip install openpyxl Pillow

Output:
    - Fichier .md avec le même nom dans le même dossier
    - Sous-dossier {nom_fichier}_images/ contenant les images
      extraites (si présentes)
"""

import sys
import re
from pathlib import Path
from typing import Optional
from urllib.parse import quote
import hashlib
from datetime import datetime

try:
    from openpyxl import load_workbook
    from openpyxl.worksheet.worksheet import Worksheet
except ImportError:
    print("ERREUR: Le package 'openpyxl' n'est pas installé.")
    print("Installez-le avec: pip install openpyxl")
    sys.exit(1)

try:
    import PIL  # noqa: F401 — présence vérifiée, Pillow requis pour traitement images
except ImportError:
    print("AVERTISSEMENT: Le package 'Pillow' n'est pas installé.")
    print("Les images ne seront pas traitées correctement.")
    print("Installez-le avec: pip install Pillow")


class XlsxToMarkdown:
    """Convertisseur de fichiers Excel (.xlsx) vers Markdown (.md)"""

    def __init__(self, xlsx_path: str, output_dir: Optional[str] = None):
        """
        Initialise le convertisseur

        Args:
            xlsx_path: Chemin vers le fichier .xlsx à convertir
            output_dir: Dossier de sortie optionnel. Si None, sera
                        déterminé automatiquement.
        """
        self.xlsx_path = Path(xlsx_path)

        if not self.xlsx_path.exists():
            raise FileNotFoundError(f"Le fichier {xlsx_path} n'existe pas.")

        if not self.xlsx_path.suffix.lower() in ['.xlsx', '.xlsm']:
            raise ValueError(
                f"Le fichier doit être un .xlsx ou .xlsm "
                f"(reçu: {self.xlsx_path.suffix})"
            )

        # Déterminer le dossier de sortie
        self.output_dir = self._determine_output_dir(output_dir)
        self.output_filename = self.xlsx_path.stem + '.md'
        self.output_path = self.output_dir / self.output_filename

        # Dossier pour les images
        self.images_dir = self.output_dir / f"{self.xlsx_path.stem}_images"
        self.images_extracted = []

        # Charger le workbook
        try:
            print("   Chargement du fichier Excel...")
            self.workbook = load_workbook(self.xlsx_path, data_only=True)
        except Exception as e:
            raise ValueError(f"Impossible de lire le fichier Excel: {e}")

        # Récupérer les métadonnées du fichier
        self.file_stats = self.xlsx_path.stat()
        self.file_hash = self._calculate_file_hash()

    def _is_local_path(self, path: Path) -> bool:
        r"""
        Vérifie si le chemin est LOCAL (pas sur un partage réseau)

        Sur Windows: Détecte les chemins UNC (\\server\share)
        Sur Linux: Détecte les montages réseau (/mnt/, /net/, etc.)

        Args:
            path: Chemin à vérifier

        Returns:
            True si le chemin est local, False si réseau
        """
        try:
            path_str = str(path.resolve())

            # Windows: Vérifier si c'est un chemin UNC (\\server\share)
            if path_str.startswith('\\\\'):
                return False  # Chemin réseau UNC

            # Linux: Vérifier les points de montage réseau courants
            if path_str.startswith('/mnt/') or path_str.startswith('/net/'):
                return False  # Chemin réseau monté

            # Tout le reste est considéré local
            return True
        except Exception:
            # En cas d'erreur, assumer local par défaut
            return True

    def _determine_output_dir(
        self, custom_output_dir: Optional[str] = None
    ) -> Path:
        """
        Détermine le dossier de sortie selon la localisation du
        fichier source

        Args:
            custom_output_dir: Dossier de sortie personnalisé
                               (optionnel)

        Returns:
            Path du dossier de sortie
        """
        # Si l'utilisateur a spécifié un dossier, l'utiliser
        if custom_output_dir:
            output_path = Path(custom_output_dir)
            output_path.mkdir(parents=True, exist_ok=True)
            return output_path

        # Si le fichier est local, créer la sortie au même endroit
        if self._is_local_path(self.xlsx_path):
            return self.xlsx_path.parent

        # Si le fichier n'est PAS local, créer dans _working
        # avec un nom descriptif
        # Utiliser le nom du fichier pour créer un sous-dossier unique
        # Cross-platform: Utiliser le chemin absolu du script pour
        # déterminer _working
        script_dir = Path(__file__).resolve().parent.parent
        working_base = script_dir / '_working'

        # Créer un nom de dossier basé sur le fichier source
        folder_name = f"conversion_{self.xlsx_path.stem}"
        output_path = working_base / folder_name

        # Créer le dossier s'il n'existe pas
        output_path.mkdir(parents=True, exist_ok=True)

        print("   ℹ Fichier source distant détecté")
        print(f"   📁 Sortie créée dans: {output_path}")

        return output_path

    def _calculate_file_hash(self) -> str:
        """Calcule le hash MD5 du fichier pour détecter les changements"""
        md5_hash = hashlib.md5()
        with open(self.xlsx_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                md5_hash.update(chunk)
        return md5_hash.hexdigest()

    def _get_document_properties(self) -> dict:
        """Récupère les propriétés du document Excel (métadonnées internes)"""
        props = {}
        try:
            excel_props = self.workbook.properties
            props['title'] = excel_props.title or "N/A"
            props['creator'] = excel_props.creator or "N/A"
            props['last_modified_by'] = (
                excel_props.lastModifiedBy or "N/A"
            )
            props['created'] = (
                excel_props.created.strftime("%Y-%m-%d %H:%M:%S")
                if excel_props.created else "N/A"
            )
            props['modified'] = (
                excel_props.modified.strftime("%Y-%m-%d %H:%M:%S")
                if excel_props.modified else "N/A"
            )
            props['subject'] = excel_props.subject or "N/A"
            props['description'] = excel_props.description or "N/A"
        except Exception as e:
            print(
                f"   ⚠ Impossible de lire toutes les propriétés "
                f"du document: {e}"
            )
        return props

    def _generate_metadata_header(self) -> str:
        """Génère l'en-tête de métadonnées pour le fichier markdown"""
        doc_props = self._get_document_properties()

        # Taille du fichier en format lisible
        file_size_bytes = self.file_stats.st_size
        if file_size_bytes < 1024:
            file_size = f"{file_size_bytes} bytes"
        elif file_size_bytes < 1024 * 1024:
            file_size = f"{file_size_bytes / 1024:.2f} KB"
        else:
            file_size = f"{file_size_bytes / (1024 * 1024):.2f} MB"

        # Date de dernière modification du fichier
        file_modified = datetime.fromtimestamp(
            self.file_stats.st_mtime
        ).strftime("%Y-%m-%d %H:%M:%S")

        # Date de conversion
        conversion_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Nombre de feuilles
        num_sheets = len(self.workbook.sheetnames)

        metadata = f"""---
# Métadonnées du document source

**Fichier source:** `{self.xlsx_path.name}`
**Taille du fichier:** {file_size}
**Dernière modification du fichier:** {file_modified}
**Hash MD5:** `{self.file_hash}`
**Date de conversion:** {conversion_date}
**Nombre de feuilles:** {num_sheets}

## Propriétés du document Excel

**Titre:** {doc_props.get('title', 'N/A')}
**Créateur:** {doc_props.get('creator', 'N/A')}
**Dernière modification par:** {doc_props.get('last_modified_by', 'N/A')}
**Date de création:** {doc_props.get('created', 'N/A')}
**Date de modification:** {doc_props.get('modified', 'N/A')}
**Sujet:** {doc_props.get('subject', 'N/A')}
**Description:** {doc_props.get('description', 'N/A')}

## Liste des feuilles

{self._generate_sheet_list()}

---

"""
        return metadata

    def _generate_sheet_list(self) -> str:
        """Génère une liste des feuilles du workbook"""
        sheet_list = []
        for i, sheet_name in enumerate(self.workbook.sheetnames, 1):
            # Créer l'ancre (slug) pour le lien
            anchor = sheet_name.lower()
            anchor = re.sub(r'[^\w\s-]', '', anchor)
            anchor = re.sub(r'[-\s]+', '-', anchor)
            anchor = anchor.strip('-')
            sheet_list.append(
                f"{i}. [{sheet_name}](#feuille--{anchor})"
            )
        return "\n".join(sheet_list)

    def extract_images(self) -> None:
        """Extrait toutes les images du fichier Excel"""
        print("\n📷 Recherche d'images dans le fichier Excel...")

        try:
            for sheet in self.workbook.worksheets:
                if hasattr(sheet, '_images') and sheet._images:
                    # Créer le dossier d'images si nécessaire
                    if not self.images_dir.exists():
                        self.images_dir.mkdir(exist_ok=True)

                    for idx, img in enumerate(sheet._images):
                        # Générer un nom de fichier
                        img_name = f"{sheet.title}_image_{idx + 1}.png"
                        img_path = self.images_dir / img_name

                        # Sauvegarder l'image
                        with open(img_path, 'wb') as f:
                            f.write(img._data())

                        self.images_extracted.append(
                            (sheet.title, img_name)
                        )
                        print(
                            f"  ✓ Image extraite: {img_name} "
                            f"(Feuille: {sheet.title})"
                        )
        except Exception as e:
            print(
                f"  ⚠ Avertissement: Impossible d'extraire "
                f"toutes les images - {e}"
            )

        if self.images_extracted:
            print(f"   ✓ {len(self.images_extracted)} image(s) extraite(s)")
        else:
            print("   ℹ Aucune image trouvée dans le document")

    def _find_last_data_row(self, worksheet: Worksheet) -> int:
        """
        Trouve la dernière rangée contenant des données réelles

        Args:
            worksheet: Feuille Excel à analyser

        Returns:
            Numéro de la dernière rangée avec données (1-based),
            ou 0 si aucune donnée
        """
        last_row_with_data = 0

        # Parcourir toutes les rangées depuis la fin
        for row_idx in range(worksheet.max_row, 0, -1):
            # Vérifier si au moins une cellule de cette rangée contient des données
            row_has_data = False
            for cell in worksheet[row_idx]:
                if cell.value is not None:
                    row_has_data = True
                    break

            # Si on trouve une rangée avec données, c'est la dernière
            if row_has_data:
                last_row_with_data = row_idx
                break

        return last_row_with_data

    def process_worksheet(self, worksheet: Worksheet) -> str:
        """
        Convertit une feuille Excel en Markdown

        Args:
            worksheet: Feuille Excel à convertir

        Returns:
            Contenu de la feuille formaté en Markdown
        """
        # Créer l'ancre pour la feuille
        sheet_anchor = worksheet.title.lower()
        sheet_anchor = re.sub(r'[^\w\s-]', '', sheet_anchor)
        sheet_anchor = re.sub(r'[-\s]+', '-', sheet_anchor)
        sheet_anchor = sheet_anchor.strip('-')

        markdown_content = [f"\n## Feuille : {worksheet.title}\n"]

        # Détecter et documenter les graphiques IMMÉDIATEMENT (v1.6)
        if hasattr(worksheet, '_charts') and worksheet._charts:
            markdown_content.append(
                "\n> \u26a0\ufe0f **["
                + str(len(worksheet._charts))
                + " graphique(s) non converti(s) détecté(s) sur cette feuille]**\n"
            )
            markdown_content.append(
                "> Les graphiques Excel ne peuvent pas être convertis en Markdown.\n"
            )

            # Lister chaque graphique avec ses métadonnées
            for idx, chart in enumerate(worksheet._charts, 1):
                chart_type = type(chart).__name__
                chart_info = f"> - **Graphique {idx}**: Type `{chart_type}`"

                # Ajouter le titre si disponible
                if hasattr(chart, 'title') and chart.title:
                    chart_title = str(chart.title)
                    chart_info += f", Titre: \"{chart_title}\""

                # Ajouter la position si disponible
                if hasattr(chart, 'anchor') and chart.anchor:
                    chart_info += f", Position: {chart.anchor}"

                chart_info += "\n"
                markdown_content.append(chart_info)

            markdown_content.append("\n")

        # Trouver la dernière rangée avec des données réelles (v1.7)
        last_data_row = self._find_last_data_row(worksheet)

        # Si aucune donnée, feuille vide
        if last_data_row == 0:
            markdown_content.append("*Cette feuille est vide*\n")
            return "\n".join(markdown_content)

        # Convertir en tableau Markdown
        markdown_content.append("\n")

        # Parcourir les lignes UNIQUEMENT jusqu'à la dernière avec données (v1.7)
        for row_idx, row in enumerate(
            worksheet.iter_rows(min_row=1, max_row=last_data_row), 1
        ):
            row_data = []

            for cell in row:
                # Obtenir la valeur de la cellule
                cell_value = cell.value

                # Vérifier si la cellule contient un hyperlien
                if cell.hyperlink:
                    # La cellule a un hyperlien
                    display_text = (
                        str(cell_value) if cell_value else "Lien"
                    )

                    # Déterminer le type de lien (externe ou interne)
                    # .target = liens externes (URL, fichiers, mailto:)
                    # .location = références internes (Sheet1!A1, etc.)
                    if cell.hyperlink.target:
                        # Lien externe (URL, fichier, mailto:, etc.)
                        url = cell.hyperlink.target
                    elif cell.hyperlink.location:
                        # Lien interne (référence de cellule)
                        # Formater comme référence Excel
                        url = cell.hyperlink.location
                    else:
                        # Fallback si ni target ni location n'est défini
                        url = "#"

                    # Formater en markdown [texte](url)
                    cell_value = f"[{display_text}]({url})"
                elif cell_value is None:
                    cell_value = ""
                elif isinstance(cell_value, (int, float)):
                    # Formater les nombres
                    cell_value = str(cell_value)
                elif isinstance(cell_value, datetime):
                    # Formater les dates
                    cell_value = cell_value.strftime("%Y-%m-%d %H:%M:%S")
                else:
                    cell_value = str(cell_value)

                # Échapper les pipes pour ne pas casser le tableau markdown
                cell_value = cell_value.replace("|", "\\|")

                row_data.append(cell_value)

            # Créer la ligne du tableau
            markdown_content.append("| " + " | ".join(row_data) + " |")

            # Ajouter la ligne de séparation après la première ligne (en-tête)
            if row_idx == 1:
                separator = ["---"] * len(row_data)
                markdown_content.append("| " + " | ".join(separator) + " |")

        markdown_content.append("\n")

        # Ajouter les images de cette feuille si présentes
        sheet_images = [
            img for sheet, img in self.images_extracted
            if sheet == worksheet.title
        ]
        if sheet_images:
            markdown_content.append("\n### Images de cette feuille\n")
            for img_name in sheet_images:
                img_folder = f"{self.xlsx_path.stem}_images"
                img_rel_path = f"{img_folder}/{img_name}"
                img_rel_path_encoded = quote(img_rel_path, safe='/')
                markdown_content.append(
                    f"\n![{img_name}]({img_rel_path_encoded})\n"
                )

        return "\n".join(markdown_content)

    def generate_toc(self) -> str:
        """
        Génère une table des matières basée sur les feuilles du
        classeur

        Returns:
            Table des matières formatée en markdown
        """
        toc_lines = ["# Table des matières\n"]

        for i, sheet_name in enumerate(self.workbook.sheetnames, 1):
            # Créer l'ancre (slug) pour le lien
            anchor = sheet_name.lower()
            anchor = re.sub(r'[^\w\s-]', '', anchor)
            anchor = re.sub(r'[-\s]+', '-', anchor)
            anchor = anchor.strip('-')

            toc_lines.append(
                f"{i}. [Feuille : {sheet_name}](#feuille--{anchor})"
            )

        toc_lines.append("\n---\n")
        return "\n".join(toc_lines)

    def convert(self) -> str:
        """
        Convertit le fichier Excel complet en Markdown

        Returns:
            Chemin du fichier markdown créé
        """
        print(f"\n🔄 Conversion de: {self.xlsx_path.name}")
        print(f"   Vers: {self.output_path.name}")

        # Extraire les images d'abord
        self.extract_images()

        # Convertir le contenu
        print(
            f"\n📝 Conversion de {len(self.workbook.sheetnames)} "
            f"feuille(s)..."
        )
        markdown_content = []

        # Parcourir toutes les feuilles
        for idx, sheet in enumerate(self.workbook.worksheets, 1):
            print(
                f"   Feuille {idx}/{len(self.workbook.sheetnames)}: "
                f"{sheet.title}"
            )
            sheet_markdown = self.process_worksheet(sheet)
            markdown_content.append(sheet_markdown)

        # Générer la table des matières
        print("\n📑 Génération de la table des matières...")
        toc = self.generate_toc()
        print("   ✓ Table des matières générée")

        # Générer l'en-tête de métadonnées
        print("\n📋 Ajout des métadonnées du document...")
        metadata_header = self._generate_metadata_header()
        print("   ✓ Métadonnées ajoutées")

        # Vérifier si des graphiques ont été détectés sur l'une des feuilles (v1.5)
        total_charts = 0
        sheets_with_charts = []
        for sheet in self.workbook.worksheets:
            if hasattr(sheet, '_charts') and sheet._charts:
                num_charts = len(sheet._charts)
                total_charts += num_charts
                sheets_with_charts.append((sheet.title, num_charts))

        # Générer l'avertissement si des graphiques ont été détectés
        charts_warning = ""
        if total_charts > 0:
            charts_warning = "\n## ⚠️ Graphiques non convertis détectés\n\n"
            charts_warning += (
                f"Ce fichier Excel contenait **{total_charts} graphique(s)** qui n'ont "
                "**pas pu être convertis** en Markdown. Les graphiques ont été **documentés** "
                "mais **omis** de la conversion :\n\n"
            )

            for sheet_name, count in sheets_with_charts:
                charts_warning += f"- **Feuille \"{sheet_name}\"** : {count} graphique(s)\n"

            charts_warning += (
                "\n> **Raison technique** : Les graphiques Excel ne peuvent pas être représentés "
                "en format Markdown (texte pur). Seule leur présence et leurs métadonnées sont "
                "documentées dans les sections de chaque feuille.\n"
            )
            charts_warning += (
                "> \n"
                "> **Documentation** :"
                " https://openpyxl.readthedocs.io/en/stable/charts/introduction.html\n"
            )
            charts_warning += (
                "> \n"
                "> **Note** : Consultez les sections \"Graphiques présents\" dans chaque feuille "
                "pour plus de détails.\n"
            )
            charts_warning += "\n---\n\n"

        # Assembler le contenu final
        final_markdown = (
            metadata_header + toc + charts_warning + "\n" + "\n".join(markdown_content)
        )

        # Sauvegarder le fichier markdown
        print("\n💾 Sauvegarde du fichier markdown...")
        try:
            with open(self.output_path, 'w', encoding='utf-8') as f:
                f.write(final_markdown)
            print(f"   ✓ Fichier sauvegardé: {self.output_path}")
        except Exception as e:
            raise IOError(
                f"Impossible de sauvegarder le fichier markdown: {e}"
            )

        # Fermer le workbook
        self.workbook.close()

        return str(self.output_path)


def main():
    """Fonction principale"""

    print("=" * 70)
    print("  Convertisseur Excel (.xlsx) -> Markdown (.md)")
    print("=" * 70)

    # Parser les arguments
    xlsx_path = None
    output_dir = None

    if len(sys.argv) > 1:
        xlsx_path = sys.argv[1]
        # Vérifier s'il y a un argument --output ou -o
        if (len(sys.argv) > 2 and
                sys.argv[2] in ['--output', '-o']):
            if len(sys.argv) > 3:
                output_dir = sys.argv[3]
    else:
        xlsx_path = input(
            "\n📂 Entrez le chemin du fichier .xlsx: "
        ).strip().strip('"')
        use_custom = input(
            "   Spécifier un dossier de sortie personnalisé? (o/N): "
        ).strip().lower()
        if use_custom == 'o':
            output_dir = input(
                "   📁 Chemin du dossier de sortie: "
            ).strip().strip('"')

    try:
        # Créer le convertisseur et lancer la conversion
        converter = XlsxToMarkdown(xlsx_path, output_dir)
        output_file = converter.convert()

        print("\n" + "=" * 70)
        print("✅ CONVERSION RÉUSSIE!")
        print("=" * 70)
        print(f"\n📄 Fichier markdown: {output_file}")

        if converter.images_extracted:
            print(f"📁 Dossier d'images: {converter.images_dir}")
            print(f"   {len(converter.images_extracted)} image(s) extraite(s)")

        print("\n")

    except Exception as e:
        print("\n" + "=" * 70)
        print("❌ ERREUR lors de la conversion")
        print("=" * 70)
        print(f"\n{type(e).__name__}: {e}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
