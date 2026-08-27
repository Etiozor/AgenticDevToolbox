"""
Script de conversion de fichiers Microsoft Word (.docx) vers Markdown (.md)

Version: 1.6.1 - Ra: Correction détection inline vs flottant
Date: 9 mars 2026
Auteur: Philippe Chayer

Changements v1.6.1 (PATCH):
- CORRECTION: Condition de détection des images changée de
  'Graphic' in xml (match inline ET flottant) vers
  '<wp:inline' in xml (inline seulement)
- Bug: les images flottantes déclenchaient l'incrémentation du
  compteur ET une note d'avertissement en double

Changements v1.6:
Nom mythologique: Ra (mythologie égyptienne)
Raison: Dieu égyptien du soleil qui illumine tout, symbolisant la visibilité
        totale des limitations. Comme Ra qui éclaire chaque recoin, cette
        version marque EXACTEMENT où se trouvent les objets non convertibles
        dans le document.
- NOTES INLINE: Insertion de notes à l'endroit EXACT où les objets sont détectés
- DOUBLE VISIBILITÉ: Section globale + notes inline dans le contenu
- FORMAT BLOCKQUOTE: Notes en blockquote (> ⚠️) pour visibilité maximale
- TRAÇABILITÉ PRÉCISE: L'utilisateur voit où était chaque objet manquant

Changements v1.5:
Nom mythologique: Osiris (mythologie égyptienne)
Raison: Dieu égyptien de l'au-delà et juge des morts, symbolisant la
        détection et le jugement des objets qui ne peuvent pas "survivre"
        à la conversion vers Markdown. Osiris veille et avertit l'utilisateur
        de ce qui sera "perdu" dans le processus.
- DÉTECTION: Détection automatique des objets non supportés (objets flottants)
- AVERTISSEMENTS CONSOLE: Affichage clair des limitations lors de la conversion
- AVERTISSEMENTS MARKDOWN: Section "Objets non convertis détectés" dans le fichier généré
- DOCUMENTATION: Notes explicatives sur pourquoi certains objets ne sont pas convertis
- TRAÇABILITÉ: Comptage précis des objets non supportés par type

Changements v1.4:
Nom mythologique: Janus (mythologie romaine)
Raison: Dieu romain aux deux visages, symbolisant la dualité des liens
        (internes/externes) et la capacité de voir dans deux directions
        simultanément.
- LIENS: Utilisation de l'API officielle paragraph.hyperlinks
- LIENS INTERNES: Support complet des bookmarks et ancres internes
- LIENS EXTERNES: Gestion améliorée des URLs web et fichiers
- ROBUSTESSE: Traitement correct du texte des hyperlinks
- CORRECTION: Élimination des duplications de liens

Changements v1.3:
Nom mythologique: Hermès (mythologie grecque)
Raison: Le messager rapide des dieux qui voyage partout, symbolisant
        la compatibilité cross-platform du script (Windows/Linux,
        local/réseau).
- VERSIONNEMENT: Ajout convention de nommage mythologique
- STANDARDISATION: Conformité avec python.instructions.md
- DOCUMENTATION: Format de version standardisé avec nom mythologique

Changements v1.2:
- FIX: Compatibilité cross-platform Windows/Linux pour chemins
- Remplacement détection hardcodée 'C:\\' par détection UNC/montages
  réseau
- working_base déterminé dynamiquement depuis __file__ au lieu de
  C:\\git
- Support chemins UNC Windows (\\\\server\\share) et montages Linux
  (/mnt/, /net/)

Description:
    Convertit un fichier .docx en fichier .md (markdown) en préservant:
    - Le texte et le formatage de base
    - Les images (extraites et sauvegardées)
    - Les hyperliens (convertis en format markdown)
    - Les tableaux
    - Les listes
    - Les titres et sous-titres

Usage:
    python docx_to_markdown.py chemin/vers/fichier.docx

    OU (sans argument - va demander le chemin):
    python docx_to_markdown.py

Dépendances:
    pip install python-docx Pillow

Output:
    - Fichier .md avec le même nom dans le même dossier
    - Sous-dossier {nom_fichier}_images/ contenant les images extraites
"""

import os
import sys
import re
from pathlib import Path
from typing import List, Optional
import zipfile
import shutil
from urllib.parse import quote
import hashlib
from datetime import datetime

try:
    from docx import Document
    from docx.oxml.text.paragraph import CT_P
    from docx.oxml.table import CT_Tbl
    from docx.table import Table
    from docx.text.paragraph import Paragraph
except ImportError:
    print("ERREUR: Le package 'python-docx' n'est pas installé.")
    print("Installez-le avec: pip install python-docx")
    sys.exit(1)

try:
    import PIL  # noqa: F401 — présence vérifiée, Pillow requis pour traitement images
except ImportError:
    print("AVERTISSEMENT: Le package 'Pillow' n'est pas installé.")
    print("Les images ne seront pas traitées correctement.")
    print("Installez-le avec: pip install Pillow")


class DocxToMarkdown:
    """Convertisseur de fichiers Word (.docx) vers Markdown (.md)"""

    def __init__(self, docx_path: str, output_dir: Optional[str] = None):
        """
        Initialise le convertisseur

        Args:
            docx_path: Chemin vers le fichier .docx à convertir
            output_dir: Dossier de sortie optionnel. Si None, sera
                        déterminé automatiquement.
        """
        self.docx_path = Path(docx_path)

        if not self.docx_path.exists():
            raise FileNotFoundError(f"Le fichier {docx_path} n'existe pas.")

        if not self.docx_path.suffix.lower() == '.docx':
            raise ValueError(
                f"Le fichier doit être un .docx "
                f"(reçu: {self.docx_path.suffix})"
            )

        # Déterminer le dossier de sortie
        self.output_dir = self._determine_output_dir(output_dir)
        self.output_filename = self.docx_path.stem + '.md'
        self.output_path = self.output_dir / self.output_filename

        # Dossier pour les images
        self.images_dir = self.output_dir / f"{self.docx_path.stem}_images"
        self.images_extracted = []

        # Charger le document
        try:
            self.document = Document(self.docx_path)
        except Exception as e:
            raise ValueError(
                f"Impossible de lire le fichier Word: {e}"
            )

        # Récupérer les métadonnées du fichier
        self.file_stats = self.docx_path.stat()
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
        if self._is_local_path(self.docx_path):
            return self.docx_path.parent

        # Si le fichier n'est PAS local, créer dans _working
        # avec un nom descriptif
        # Utiliser le nom du fichier pour créer un sous-dossier unique
        # Cross-platform: Utiliser le chemin absolu du script pour
        # déterminer _working
        script_dir = Path(__file__).resolve().parent.parent
        working_base = script_dir / '_working'

        # Créer un nom de dossier basé sur le fichier source
        folder_name = f"conversion_{self.docx_path.stem}"
        output_path = working_base / folder_name

        # Créer le dossier s'il n'existe pas
        output_path.mkdir(parents=True, exist_ok=True)

        print("   ℹ Fichier source distant détecté")
        print(f"   📁 Sortie créée dans: {output_path}")

        return output_path

    def _calculate_file_hash(self) -> str:
        """Calcule le hash MD5 du fichier pour détecter les changements"""
        md5_hash = hashlib.md5()
        with open(self.docx_path, "rb") as f:
            # Lire par chunks pour ne pas surcharger la mémoire
            for chunk in iter(lambda: f.read(4096), b""):
                md5_hash.update(chunk)
        return md5_hash.hexdigest()

    def _get_document_properties(self) -> dict:
        """Récupère les propriétés du document Word (métadonnées internes)"""
        props = {}
        try:
            core_props = self.document.core_properties
            props['title'] = core_props.title or "N/A"
            props['author'] = core_props.author or "N/A"
            props['last_modified_by'] = (
                core_props.last_modified_by or "N/A"
            )
            props['created'] = (
                core_props.created.strftime("%Y-%m-%d %H:%M:%S")
                if core_props.created else "N/A"
            )
            props['modified'] = (
                core_props.modified.strftime("%Y-%m-%d %H:%M:%S")
                if core_props.modified else "N/A"
            )
            props['revision'] = core_props.revision or "N/A"
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

        metadata = f"""---
# Métadonnées du document source

**Fichier source:** `{self.docx_path.name}`
**Taille du fichier:** {file_size}
**Dernière modification du fichier:** {file_modified}
**Hash MD5:** `{self.file_hash}`
**Date de conversion:** {conversion_date}

## Propriétés du document Word

**Titre:** {doc_props.get('title', 'N/A')}
**Auteur:** {doc_props.get('author', 'N/A')}
**Dernière modification par:** {doc_props.get('last_modified_by', 'N/A')}
**Date de création:** {doc_props.get('created', 'N/A')}
**Date de modification:** {doc_props.get('modified', 'N/A')}
**Révision:** {doc_props.get('revision', 'N/A')}

---

"""
        return metadata

    def detect_unsupported_in_paragraph(self, paragraph) -> list:
        """
        Détecte les objets non supportés dans UN paragraphe spécifique (v1.6)

        Args:
            paragraph: Objet Paragraph de python-docx

        Returns:
            list: Liste des objets non supportés détectés dans ce paragraphe
                  Chaque élément: {'type': str, 'description': str}
        """
        objects = []

        # Inspecter le XML du paragraphe
        # Note: paragraph._element.xml peut être bytes ou str selon la version
        para_xml = paragraph._element.xml
        if isinstance(para_xml, bytes):
            para_xml = para_xml.decode('utf-8')

        # Détecter les objets flottants (anchored shapes)
        if '<wp:anchor' in para_xml:
            objects.append({
                'type': 'floating_shape',
                'description': 'Image flottante ou forme'
            })

        # Détecter les graphiques
        if '<c:chart' in para_xml:
            objects.append({
                'type': 'chart',
                'description': 'Graphique Word'
            })

        # Détecter les objets OLE embarqués
        if '<o:OLEObject' in para_xml:
            objects.append({
                'type': 'ole_object',
                'description': 'Objet OLE embarqué (PDF, Excel, etc.)'
            })

        # Détecter les zones de texte
        if '<wps:txbx' in para_xml or '<v:textbox' in para_xml:
            objects.append({
                'type': 'text_box',
                'description': 'Zone de texte'
            })

        return objects

    def detect_unsupported_objects(self) -> dict:
        """
        Détecte les objets non supportés dans le document Word (v1.5)

        Retourne un dictionnaire avec les types d'objets non supportés
        détectés et leur nombre.

        Returns:
            dict: {'floating_shapes': int, 'charts': int, 'ole_objects': int}
        """
        unsupported = {
            'floating_shapes': 0,
            'charts': 0,
            'ole_objects': 0,
            'text_boxes': 0
        }

        # Inspecter le XML du document pour détecter les objets
        # de la couche de dessin (drawing layer)
        # Note: document.element.xml peut être bytes ou str selon la version
        doc_xml = self.document.element.xml
        if isinstance(doc_xml, bytes):
            doc_xml = doc_xml.decode('utf-8')

        # Détecter les objets flottants (anchored shapes)
        # Tag: <w:drawing><wp:anchor>
        if '<wp:anchor' in doc_xml:
            unsupported['floating_shapes'] = doc_xml.count('<wp:anchor')

        # Détecter les graphiques (charts)
        # Tag: <c:chart>
        if '<c:chart' in doc_xml or 'chart' in doc_xml.lower():
            unsupported['charts'] = doc_xml.count('<c:chart')

        # Détecter les objets OLE embarqués
        # Tag: <o:OLEObject>
        if '<o:OLEObject' in doc_xml:
            unsupported['ole_objects'] = doc_xml.count('<o:OLEObject')

        # Détecter les zones de texte (text boxes)
        # Tag: <wps:txbx> ou <v:textbox>
        if '<wps:txbx' in doc_xml or '<v:textbox' in doc_xml:
            unsupported['text_boxes'] = (
                doc_xml.count('<wps:txbx') + doc_xml.count('<v:textbox')
            )

        return unsupported

    def extract_images(self) -> None:
        """Extrait toutes les images du fichier .docx"""

        # Les fichiers .docx sont des archives ZIP
        # Les images sont dans word/media/
        try:
            with zipfile.ZipFile(self.docx_path, 'r') as zip_ref:
                # Trouver tous les fichiers d'images
                image_files = [
                    f for f in zip_ref.namelist()
                    if f.startswith('word/media/')
                ]

                if image_files:
                    # Créer le dossier d'images si nécessaire
                    self.images_dir.mkdir(exist_ok=True)

                    # Extraire chaque image
                    for img_file in image_files:
                        img_name = os.path.basename(img_file)
                        img_path = self.images_dir / img_name

                        with zip_ref.open(img_file) as source:
                            with open(img_path, 'wb') as target:
                                shutil.copyfileobj(source, target)

                        self.images_extracted.append(img_name)
                        print(f"  ✓ Image extraite: {img_name}")

        except Exception as e:
            print(
                f"  ⚠ Avertissement: Impossible d'extraire "
                f"les images - {e}"
            )

    def process_paragraph(self, paragraph: Paragraph) -> str:
        """
        Convertit un paragraphe Word en Markdown

        Args:
            paragraph: Objet Paragraph de python-docx

        Returns:
            Texte formaté en Markdown
        """
        text = paragraph.text.strip()

        if not text:
            return ""

        # Détection des titres (basé sur le style)
        style_name = paragraph.style.name.lower()

        if 'heading 1' in style_name or 'titre 1' in style_name:
            return f"# {text}\n"
        elif 'heading 2' in style_name or 'titre 2' in style_name:
            return f"## {text}\n"
        elif 'heading 3' in style_name or 'titre 3' in style_name:
            return f"### {text}\n"
        elif 'heading 4' in style_name or 'titre 4' in style_name:
            return f"#### {text}\n"
        elif 'heading 5' in style_name or 'titre 5' in style_name:
            return f"##### {text}\n"
        elif 'heading 6' in style_name or 'titre 6' in style_name:
            return f"###### {text}\n"

        # Utiliser l'API officielle pour extraire les hyperlinks
        # Cela gère TOUS les types de liens (externes ET internes)
        hyperlinks = paragraph.hyperlinks

        # Créer un mapping des hyperlinks par leur texte pour traitement
        hyperlinks_map = {}
        for hyperlink in hyperlinks:
            link_text = hyperlink.text
            # Utiliser .url qui combine address + fragment automatiquement
            link_url = hyperlink.url

            # Si pas d'URL externe, vérifier si c'est un lien interne
            if not link_url and hyperlink.fragment:
                # Lien interne (bookmark) - utiliser format markdown #anchor
                link_url = f"#{hyperlink.fragment}"
            elif not link_url and hyperlink.address:
                # Lien externe sans fragment
                link_url = hyperlink.address

            if link_text and link_url:
                hyperlinks_map[link_text] = link_url

        # Traiter le contenu du paragraphe
        # Utiliser iter_inner_content() pour parcourir runs ET hyperlinks
        markdown_text = ""
        processed_hyperlinks = set()  # Pour éviter duplications

        for item in paragraph.iter_inner_content():
            # Si c'est un hyperlink
            if hasattr(item, 'text') and hasattr(item, 'url'):
                link_text = item.text
                link_url = item.url

                # Gérer les liens internes
                if not link_url and item.fragment:
                    link_url = f"#{item.fragment}"
                elif not link_url and item.address:
                    link_url = item.address

                # Éviter duplications
                if link_text and link_url and link_text not in processed_hyperlinks:
                    markdown_text += f"[{link_text}]({link_url})"
                    processed_hyperlinks.add(link_text)
            # Si c'est un run normal
            else:
                run = item
                run_text = run.text

                # Ne traiter que si ce run n'est pas déjà dans un hyperlink
                if run_text and run_text not in processed_hyperlinks:
                    # Gras
                    if run.bold:
                        run_text = f"**{run_text}**"

                    # Italique
                    if run.italic:
                        run_text = f"*{run_text}*"

                    # Code (monospace)
                    if run.font.name and 'courier' in run.font.name.lower():
                        run_text = f"`{run_text}`"

                    markdown_text += run_text

        # Si le texte est vide après traitement, utiliser le texte brut
        if not markdown_text.strip():
            markdown_text = text

        return markdown_text + "\n"

    def process_table(self, table: Table) -> str:
        """
        Convertit un tableau Word en tableau Markdown

        Args:
            table: Objet Table de python-docx

        Returns:
            Tableau formaté en Markdown
        """
        markdown_table = "\n"

        for i, row in enumerate(table.rows):
            row_data = [cell.text.strip() for cell in row.cells]
            markdown_table += "| " + " | ".join(row_data) + " |\n"

            # Ajouter la ligne de séparation après l'en-tête
            if i == 0:
                separator = ["---"] * len(row_data)
                markdown_table += "| " + " | ".join(separator) + " |\n"

        markdown_table += "\n"
        return markdown_table

    def _extract_hyperlinks_from_paragraph(self, paragraph: Paragraph) -> dict:
        """
        MÉTHODE OBSOLÈTE - Conservée pour compatibilité

        Utiliser paragraph.hyperlinks à la place (API officielle)

        Extrait les hyperliens d'un paragraphe Word

        Args:
            paragraph: Objet Paragraph de python-docx

        Returns:
            Dictionnaire {hyperlink_id: (texte, url)}
        """
        # NOTE: Cette méthode n'est plus utilisée depuis v1.4
        # Le code utilise maintenant paragraph.hyperlinks (API officielle)
        # qui gère correctement les liens internes ET externes
        hyperlinks = {}

        try:
            # Parcourir les éléments XML du paragraphe pour
            # trouver les hyperliens
            from docx.oxml.ns import qn

            # Chercher les éléments hyperlink dans le XML du
            # paragraphe
            for hyperlink in paragraph._element.xpath(
                './/w:hyperlink'
            ):
                # Obtenir l'ID de relation
                r_id = hyperlink.get(qn('r:id'))

                if r_id and r_id in paragraph.part.rels:
                    # Récupérer l'URL depuis les relations
                    url = paragraph.part.rels[r_id].target_ref

                    # Extraire le texte du hyperlien
                    link_text = ''.join(
                        node.text for node in hyperlink.xpath('.//w:t')
                        if node.text
                    )

                    if link_text and url:
                        hyperlinks[r_id] = (link_text, url)
        except Exception:
            # En cas d'erreur, retourner un dictionnaire vide
            pass

        return hyperlinks

    def generate_toc(self, markdown_content: List[str]) -> str:
        """
        Génère une table des matières basée sur les titres du
        document

        Args:
            markdown_content: Contenu markdown du document

        Returns:
            Table des matières formatée en markdown
        """
        toc_lines = ["# Table des matières\n"]

        for line in markdown_content:
            line = line.strip()

            # Détecter les titres (lignes commençant par #)
            if line.startswith('#'):
                # Compter le niveau de titre
                level = 0
                for char in line:
                    if char == '#':
                        level += 1
                    else:
                        break

                # Extraire le texte du titre (sans les #)
                title_text = line.lstrip('#').strip()

                # Ignorer le titre "Table des matières" lui-même
                if title_text.lower() == 'table des matières':
                    continue

                # Créer l'ancre (slug) pour le lien
                # Convertir en minuscules, remplacer espaces par tirets
                anchor = title_text.lower()
                # Enlever caractères spéciaux
                anchor = re.sub(r'[^\w\s-]', '', anchor)
                # Remplacer espaces/tirets multiples
                anchor = re.sub(r'[-\s]+', '-', anchor)
                # Enlever tirets aux extrémités
                anchor = anchor.strip('-')

                # Indentation basée sur le niveau (niveau 1 = pas d'indent)
                indent = '  ' * (level - 1)

                # Ajouter la ligne TOC
                toc_lines.append(f"{indent}- [{title_text}](#{anchor})")

        toc_lines.append("\n---\n")  # Séparateur après la TOC
        return "\n".join(toc_lines)

    def convert(self) -> str:
        """
        Convertit le document Word complet en Markdown

        Returns:
            Chemin du fichier markdown créé
        """
        print(f"\n🔄 Conversion de: {self.docx_path.name}")
        print(f"   Vers: {self.output_path.name}")

        # Détecter les objets non supportés (v1.5)
        print("\n🔍 Détection des objets non supportés...")
        unsupported = self.detect_unsupported_objects()

        has_unsupported = any(count > 0 for count in unsupported.values())

        if has_unsupported:
            print(
                "\n⚠️  AVERTISSEMENT: Ce document contient des objets "
                "qui ne peuvent pas être convertis:\n"
            )
            if unsupported['floating_shapes'] > 0:
                print(
                    f"   • {unsupported['floating_shapes']} "
                    f"objet(s) flottant(s) (images flottantes, formes)"
                )
            if unsupported['charts'] > 0:
                print(
                    f"   • {unsupported['charts']} graphique(s)"
                )
            if unsupported['ole_objects'] > 0:
                print(
                    f"   • {unsupported['ole_objects']} "
                    f"objet(s) OLE embarqué(s)"
                )
            if unsupported['text_boxes'] > 0:
                print(
                    f"   • {unsupported['text_boxes']} zone(s) de texte"
                )
            print(
                "\n   RAISON: python-docx ne supporte que les images "
                "inline (dans le texte)."
            )
            print(
                "   DOCUMENTATION: "
                "https://python-docx.readthedocs.io/en/latest/user/shapes.html"
            )
            print()
        else:
            print("   ✓ Aucun objet non supporté détecté")

        # Extraire les images d'abord
        print("\n📷 Extraction des images...")
        self.extract_images()

        if self.images_extracted:
            print(f"   ✓ {len(self.images_extracted)} image(s) extraite(s)")
        else:
            print("   ℹ Aucune image trouvée dans le document")

        # Convertir le contenu
        print("\n📝 Conversion du texte et formatage...")
        markdown_content = []
        image_counter = 0

        # Parcourir tous les éléments du document
        for element in self.document.element.body:

            # Paragraphe
            if isinstance(element, CT_P):
                paragraph = Paragraph(element, self.document)

                # Vérifier si le paragraphe contient une image inline
                # Note: <wp:inline> = image inline, <wp:anchor> = image flottante
                # 'Graphic' match les deux types, causant un double traitement (v1.6.1)
                if '<wp:inline' in paragraph._element.xml:
                    if image_counter < len(self.images_extracted):
                        img_name = self.images_extracted[image_counter]
                        # Encoder le chemin pour gérer les espaces
                        # et caractères spéciaux
                        img_folder = f"{self.docx_path.stem}_images"
                        img_rel_path = f"{img_folder}/{img_name}"
                        # Encoder les espaces et caractères spéciaux
                        # pour l'URL markdown
                        img_rel_path_encoded = quote(
                            img_rel_path, safe='/'
                        )
                        markdown_content.append(
                            f"\n![Image {image_counter + 1}]"
                            f"({img_rel_path_encoded})\n"
                        )
                        image_counter += 1

                # Détecter les objets non supportés DANS CE PARAGRAPHE (v1.6)
                unsupported_in_para = self.detect_unsupported_in_paragraph(paragraph)

                # Insérer une note inline pour chaque objet détecté
                if unsupported_in_para:
                    for obj in unsupported_in_para:
                        note = (
                            f"\n> ⚠️ **[Objet non converti détecté]** "
                            f"Type: {obj['description']}\n\n"
                        )
                        markdown_content.append(note)

                # Traiter le texte du paragraphe
                para_text = self.process_paragraph(paragraph)
                if para_text:
                    markdown_content.append(para_text)

            # Tableau
            elif isinstance(element, CT_Tbl):
                table = Table(element, self.document)
                markdown_content.append(self.process_table(table))

        # Générer la table des matières
        print("\n📑 Génération de la table des matières...")
        toc = self.generate_toc(markdown_content)
        print("   ✓ Table des matières générée")

        # Générer l'en-tête de métadonnées
        print("\n📋 Ajout des métadonnées du document...")
        metadata_header = self._generate_metadata_header()
        print("   ✓ Métadonnées ajoutées")

        # Ajouter une section d'avertissement si des objets non supportés ont été détectés (v1.5)
        unsupported_warning = ""
        if has_unsupported:
            unsupported_warning = "\n## ⚠️ Objets non convertis détectés\n\n"
            unsupported_warning += (
                "Ce document Word contenait des objets qui n'ont **pas pu être convertis** "
                "en Markdown. Ces objets ont été **omis** de la conversion :"
            )
            unsupported_warning += "\n\n"

            if unsupported['floating_shapes'] > 0:
                unsupported_warning += (
                    f"- **{unsupported['floating_shapes']} objet(s) flottant(s)** "
                    f"(images flottantes, formes, dessins)\n"
                )
            if unsupported['charts'] > 0:
                unsupported_warning += f"- **{unsupported['charts']} graphique(s)**\n"
            if unsupported['ole_objects'] > 0:
                unsupported_warning += (
                    f"- **{unsupported['ole_objects']} objet(s) OLE embarqué(s)** "
                    f"(fichiers PDF, Excel, etc.)\n"
                )
            if unsupported['text_boxes'] > 0:
                unsupported_warning += f"- **{unsupported['text_boxes']} zone(s) de texte**\n"

            unsupported_warning += (
                "\n> **Raison technique** : La bibliothèque python-docx ne supporte"
                " que les images inline (dans le texte). Les objets de la couche"
                " de dessin (drawing layer) ne sont pas accessibles.\n"
            )
            unsupported_warning += (
                "> \n"
                "> **Documentation** :"
                " https://python-docx.readthedocs.io/en/latest/user/shapes.html\n"
            )
            unsupported_warning += "\n---\n\n"

        # Assembler le contenu final avec métadonnées, TOC, avertissement et contenu
        final_markdown = (
            metadata_header + toc + unsupported_warning + "\n" + "\n".join(markdown_content)
        )

        # Post-traitement pour préserver les URLs
        # Les URLs sont généralement déjà en texte, mais on peut
        # améliorer la détection
        url_pattern = r'(https?://[^\s\)]+)'
        final_markdown = re.sub(url_pattern, r'<\1>', final_markdown)

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

        return str(self.output_path)


def main():
    """Fonction principale"""

    print("=" * 70)
    print("  Convertisseur Word (.docx) -> Markdown (.md)")
    print("=" * 70)

    # Parser les arguments
    docx_path = None
    output_dir = None

    if len(sys.argv) > 1:
        docx_path = sys.argv[1]
        # Vérifier s'il y a un argument --output ou -o
        if (len(sys.argv) > 2 and
                sys.argv[2] in ['--output', '-o']):
            if len(sys.argv) > 3:
                output_dir = sys.argv[3]
    else:
        docx_path = input(
            "\n📂 Entrez le chemin du fichier .docx: "
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
        converter = DocxToMarkdown(docx_path, output_dir)
        output_file = converter.convert()

        print("\n" + "=" * 70)
        print("✅ CONVERSION RÉUSSIE!")
        print("=" * 70)
        print(f"\n📄 Fichier markdown: {output_file}")

        if converter.images_extracted:
            print(f"📁 Dossier d'images: {converter.images_dir}")

        print("\n")

    except Exception as e:
        print("\n" + "=" * 70)
        print("❌ ERREUR lors de la conversion")
        print("=" * 70)
        print(f"\n{type(e).__name__}: {e}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
