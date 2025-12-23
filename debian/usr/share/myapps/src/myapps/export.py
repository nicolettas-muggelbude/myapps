"""
Export-Modul für MyApps
Exportiert Paketlisten in verschiedene Formate (txt, csv, json)
"""

import json
import csv
import logging
from pathlib import Path
from typing import List
from datetime import datetime

logger = logging.getLogger(__name__)


class Exporter:
    """Klasse zum Exportieren von Paketlisten"""

    @staticmethod
    def export_to_txt(packages: List, output_path: str) -> bool:
        """
        Exportiert Pakete in eine Textdatei

        Args:
            packages: Liste von Package-Objekten
            output_path: Pfad zur Ausgabedatei

        Returns:
            True bei Erfolg, False bei Fehler
        """
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(f"# MyApps Export - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"# Anzahl Pakete: {len(packages)}\n\n")

                # Gruppiere nach Pakettyp
                grouped = {}
                for pkg in packages:
                    if pkg.package_type not in grouped:
                        grouped[pkg.package_type] = []
                    grouped[pkg.package_type].append(pkg)

                # Schreibe gruppiert
                for pkg_type, pkgs in sorted(grouped.items()):
                    f.write(f"\n=== {pkg_type.upper()} Pakete ({len(pkgs)}) ===\n\n")
                    for pkg in sorted(pkgs, key=lambda p: p.name):
                        f.write(f"{pkg.name} ({pkg.version})\n")

            logger.info(f"Export nach {output_path} erfolgreich (TXT)")
            return True
        except Exception as e:
            logger.error(f"Fehler beim TXT-Export: {e}")
            return False

    @staticmethod
    def export_to_csv(packages: List, output_path: str) -> bool:
        """
        Exportiert Pakete in eine CSV-Datei

        Args:
            packages: Liste von Package-Objekten
            output_path: Pfad zur Ausgabedatei

        Returns:
            True bei Erfolg, False bei Fehler
        """
        try:
            with open(output_path, 'w', encoding='utf-8', newline='') as f:
                writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

                # Header
                writer.writerow(['Name', 'Version', 'Typ', 'Beschreibung'])

                # Daten
                for pkg in sorted(packages, key=lambda p: (p.package_type, p.name)):
                    writer.writerow([
                        pkg.name,
                        pkg.version,
                        pkg.package_type,
                        pkg.description or ''
                    ])

            logger.info(f"Export nach {output_path} erfolgreich (CSV)")
            return True
        except Exception as e:
            logger.error(f"Fehler beim CSV-Export: {e}")
            return False

    @staticmethod
    def export_to_json(packages: List, output_path: str) -> bool:
        """
        Exportiert Pakete in eine JSON-Datei

        Args:
            packages: Liste von Package-Objekten
            output_path: Pfad zur Ausgabedatei

        Returns:
            True bei Erfolg, False bei Fehler
        """
        try:
            # Konvertiere Packages zu Dictionaries
            packages_data = []
            for pkg in packages:
                packages_data.append({
                    'name': pkg.name,
                    'version': pkg.version,
                    'type': pkg.package_type,
                    'description': pkg.description
                })

            # Sortiere nach Typ und Name
            packages_data.sort(key=lambda p: (p['type'], p['name']))

            # Erstelle Export-Struktur
            export_data = {
                'export_date': datetime.now().isoformat(),
                'total_packages': len(packages),
                'packages_by_type': {},
                'packages': packages_data
            }

            # Zähle Pakete nach Typ
            for pkg in packages:
                pkg_type = pkg.package_type
                if pkg_type not in export_data['packages_by_type']:
                    export_data['packages_by_type'][pkg_type] = 0
                export_data['packages_by_type'][pkg_type] += 1

            # Schreibe JSON
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, ensure_ascii=False)

            logger.info(f"Export nach {output_path} erfolgreich (JSON)")
            return True
        except Exception as e:
            logger.error(f"Fehler beim JSON-Export: {e}")
            return False

    @staticmethod
    def export(packages: List, output_path: str, format: str = None) -> bool:
        """
        Exportiert Pakete im angegebenen Format

        Args:
            packages: Liste von Package-Objekten
            output_path: Pfad zur Ausgabedatei
            format: Export-Format ('txt', 'csv', 'json') - wird aus Dateiendung ermittelt falls None

        Returns:
            True bei Erfolg, False bei Fehler
        """
        # Ermittle Format aus Dateiendung falls nicht angegeben
        if format is None:
            suffix = Path(output_path).suffix.lower()
            format_map = {
                '.txt': 'txt',
                '.csv': 'csv',
                '.json': 'json'
            }
            format = format_map.get(suffix, 'txt')

        # Rufe entsprechende Export-Methode auf
        if format == 'txt':
            return Exporter.export_to_txt(packages, output_path)
        elif format == 'csv':
            return Exporter.export_to_csv(packages, output_path)
        elif format == 'json':
            return Exporter.export_to_json(packages, output_path)
        else:
            logger.error(f"Unbekanntes Export-Format: {format}")
            return False
