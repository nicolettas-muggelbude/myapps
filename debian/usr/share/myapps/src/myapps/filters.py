"""
Filter-System für MyApps
Lädt und wendet Systemapp-Filter an, um User-Apps von System-Apps zu trennen
"""

import json
import os
import logging
from typing import List, Set
from pathlib import Path

logger = logging.getLogger(__name__)


class FilterManager:
    """Verwaltet Filter für System-Apps"""

    def __init__(self, filter_dir: str):
        """
        Initialisiert den FilterManager

        Args:
            filter_dir: Pfad zum Verzeichnis mit Filter-JSON-Dateien
        """
        self.filter_dir = Path(filter_dir)
        self.system_keywords: Set[str] = set()
        self.user_filters_path = Path.home() / ".config" / "myapps" / "user-filters.json"

    def load_filters(self, filter_files: List[str]) -> None:
        """
        Lädt Filter aus den angegebenen JSON-Dateien

        Args:
            filter_files: Liste von Filter-Dateinamen (z.B. ["common.json", "debian.json"])
        """
        self.system_keywords.clear()

        for filename in filter_files:
            filter_path = self.filter_dir / filename

            if not filter_path.exists():
                logger.warning(f"Filter-Datei nicht gefunden: {filter_path}")
                continue

            try:
                with open(filter_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    keywords = data.get("keywords", [])
                    self.system_keywords.update(keyword.lower() for keyword in keywords)
                    logger.info(f"Filter geladen: {filename} ({len(keywords)} Keywords)")
            except Exception as e:
                logger.error(f"Fehler beim Laden von {filename}: {e}")

        # Lade User-Filter
        self._load_user_filters()

        logger.info(f"Insgesamt {len(self.system_keywords)} Filter-Keywords geladen")

    def _load_user_filters(self) -> None:
        """Lädt benutzerdefinierte Filter aus ~/.config/myapps/user-filters.json"""
        if not self.user_filters_path.exists():
            logger.debug("Keine User-Filter-Datei gefunden")
            return

        try:
            with open(self.user_filters_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                user_keywords = data.get("keywords", [])
                self.system_keywords.update(keyword.lower() for keyword in user_keywords)
                logger.info(f"User-Filter geladen: {len(user_keywords)} Keywords")
        except Exception as e:
            logger.error(f"Fehler beim Laden der User-Filter: {e}")

    def save_user_filter(self, package_name: str) -> bool:
        """
        Fügt ein Paket zur User-Filter-Liste hinzu

        Args:
            package_name: Name des Pakets das gefiltert werden soll

        Returns:
            True bei Erfolg, False bei Fehler
        """
        # Erstelle Konfigurations-Verzeichnis falls nötig
        self.user_filters_path.parent.mkdir(parents=True, exist_ok=True)

        # Lade existierende User-Filter
        existing_keywords = []
        if self.user_filters_path.exists():
            try:
                with open(self.user_filters_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    existing_keywords = data.get("keywords", [])
            except Exception as e:
                logger.error(f"Fehler beim Lesen der User-Filter: {e}")

        # Füge neues Keyword hinzu (falls noch nicht vorhanden)
        package_lower = package_name.lower()
        if package_lower not in [k.lower() for k in existing_keywords]:
            existing_keywords.append(package_name)

            # Speichere aktualisierte Filter
            try:
                with open(self.user_filters_path, 'w', encoding='utf-8') as f:
                    json.dump({
                        "description": "Benutzerdefinierte Filter",
                        "keywords": existing_keywords
                    }, f, indent=2, ensure_ascii=False)

                # Füge auch zum aktuellen Filter-Set hinzu
                self.system_keywords.add(package_lower)

                logger.info(f"Paket '{package_name}' zur User-Filter-Liste hinzugefügt")
                return True
            except Exception as e:
                logger.error(f"Fehler beim Speichern der User-Filter: {e}")
                return False
        else:
            logger.debug(f"Paket '{package_name}' ist bereits in den User-Filtern")
            return True

    def is_user_app(self, package_name: str) -> bool:
        """
        Prüft, ob ein Paket eine User-App ist (nicht gefiltert werden soll)

        Args:
            package_name: Name des Pakets

        Returns:
            True wenn es eine User-App ist, False wenn es gefiltert werden soll
        """
        package_lower = package_name.lower()

        # Prüfe ob ein Filter-Keyword im Paketnamen vorkommt
        for keyword in self.system_keywords:
            if keyword in package_lower:
                return False

        return True

    def filter_packages(self, packages: List) -> List:
        """
        Filtert eine Liste von Paketen und gibt nur User-Apps zurück

        Args:
            packages: Liste von Package-Objekten

        Returns:
            Gefilterte Liste mit nur User-Apps
        """
        user_apps = [pkg for pkg in packages if self.is_user_app(pkg.name)]

        filtered_count = len(packages) - len(user_apps)
        logger.info(f"{filtered_count} System-Pakete gefiltert, {len(user_apps)} User-Apps übrig")

        return user_apps

    def get_stats(self) -> dict:
        """
        Gibt Statistiken über geladene Filter zurück

        Returns:
            Dictionary mit Statistiken
        """
        user_filter_count = 0
        if self.user_filters_path.exists():
            try:
                with open(self.user_filters_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    user_filter_count = len(data.get("keywords", []))
            except Exception:
                pass

        return {
            "total_keywords": len(self.system_keywords),
            "user_filters": user_filter_count,
            "user_filters_path": str(self.user_filters_path)
        }
