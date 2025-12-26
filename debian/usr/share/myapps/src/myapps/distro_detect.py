"""
Distro-Erkennungsmodul für MyApps
Erkennt automatisch die Linux-Distribution und deren Paketmanager
"""

import os
import logging
from typing import Optional, Dict
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class DistroInfo:
    """Informationen über die erkannte Distribution"""
    name: str  # z.B. "ubuntu", "arch", "fedora"
    pretty_name: str  # z.B. "Ubuntu 22.04 LTS"
    version: str  # z.B. "22.04"
    id_like: list[str]  # z.B. ["debian"]
    package_managers: list[str]  # z.B. ["dpkg", "snap", "flatpak"]


class DistroDetector:
    """Klasse zur Erkennung der Linux-Distribution"""

    # Mapping von Distribution-IDs zu Paketmanagern
    DISTRO_PACKAGE_MANAGERS = {
        "debian": ["dpkg"],
        "ubuntu": ["dpkg"],
        "linuxmint": ["dpkg"],
        "mint": ["dpkg"],
        "arch": ["pacman"],
        "manjaro": ["pacman"],
        "endeavouros": ["pacman"],
        "garuda": ["pacman"],
        "fedora": ["rpm", "dnf"],
        "rhel": ["rpm", "dnf"],
        "centos": ["rpm", "dnf"],
        "solus": ["eopkg"],
        "opensuse": ["rpm", "zypper"],
        "opensuse-leap": ["rpm", "zypper"],
        "opensuse-tumbleweed": ["rpm", "zypper"],
    }

    def __init__(self):
        self._distro_info: Optional[DistroInfo] = None

    def detect(self) -> DistroInfo:
        """
        Erkennt die aktuelle Linux-Distribution

        Returns:
            DistroInfo: Informationen über die Distribution

        Raises:
            RuntimeError: Wenn die Distribution nicht erkannt werden kann
        """
        if self._distro_info is not None:
            return self._distro_info

        os_release_path = "/etc/os-release"

        if not os.path.exists(os_release_path):
            logger.error(f"{os_release_path} nicht gefunden")
            raise RuntimeError("Distribution konnte nicht erkannt werden: /etc/os-release fehlt")

        # Parse /etc/os-release
        os_release_data = self._parse_os_release(os_release_path)

        distro_id = os_release_data.get("ID", "unknown").lower()
        pretty_name = os_release_data.get("PRETTY_NAME", "Unknown Linux")
        version = os_release_data.get("VERSION_ID", "unknown")
        id_like = os_release_data.get("ID_LIKE", "").lower().split()

        # Bestimme Paketmanager basierend auf Distro-ID oder ID_LIKE
        package_managers = self._determine_package_managers(distro_id, id_like)

        # Füge universelle Paketmanager hinzu (Snap, Flatpak)
        universal_pms = self._detect_universal_package_managers()
        package_managers.extend(universal_pms)

        self._distro_info = DistroInfo(
            name=distro_id,
            pretty_name=pretty_name,
            version=version,
            id_like=id_like,
            package_managers=package_managers
        )

        logger.info(f"Distribution erkannt: {self._distro_info.pretty_name}")
        logger.info(f"Paketmanager: {', '.join(self._distro_info.package_managers)}")

        return self._distro_info

    def _parse_os_release(self, path: str) -> Dict[str, str]:
        """
        Parst die /etc/os-release Datei

        Args:
            path: Pfad zur os-release Datei

        Returns:
            Dictionary mit Key-Value-Paaren aus der Datei
        """
        data = {}

        try:
            with open(path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue

                    if '=' in line:
                        key, value = line.split('=', 1)
                        # Entferne Anführungszeichen
                        value = value.strip('"').strip("'")
                        data[key] = value
        except Exception as e:
            logger.error(f"Fehler beim Parsen von {path}: {e}")
            raise

        return data

    def _determine_package_managers(self, distro_id: str, id_like: list[str]) -> list[str]:
        """
        Bestimmt die Paketmanager basierend auf Distro-ID

        Args:
            distro_id: Distribution ID (z.B. "ubuntu")
            id_like: Liste von ähnlichen Distributionen

        Returns:
            Liste von Paketmanager-Namen
        """
        # Prüfe zuerst die exakte Distro-ID
        if distro_id in self.DISTRO_PACKAGE_MANAGERS:
            return self.DISTRO_PACKAGE_MANAGERS[distro_id].copy()

        # Prüfe dann ID_LIKE
        for like_id in id_like:
            if like_id in self.DISTRO_PACKAGE_MANAGERS:
                logger.info(f"Paketmanager basierend auf ID_LIKE={like_id} erkannt")
                return self.DISTRO_PACKAGE_MANAGERS[like_id].copy()

        logger.warning(f"Unbekannte Distribution: {distro_id}, verwende Standard-Fallback")
        # Fallback: Versuche häufigste Paketmanager zu erkennen
        return self._fallback_package_manager_detection()

    def _fallback_package_manager_detection(self) -> list[str]:
        """
        Fallback-Erkennung von Paketmanagern durch Prüfung verfügbarer Befehle

        Returns:
            Liste von verfügbaren Paketmanagern
        """
        available_pms = []

        pm_commands = {
            "dpkg": "/usr/bin/dpkg",
            "pacman": "/usr/bin/pacman",
            "rpm": "/usr/bin/rpm",
            "dnf": "/usr/bin/dnf",
            "zypper": "/usr/bin/zypper",
            "eopkg": "/usr/bin/eopkg",
        }

        for pm_name, pm_path in pm_commands.items():
            if os.path.exists(pm_path):
                available_pms.append(pm_name)
                logger.info(f"Paketmanager {pm_name} durch Fallback-Erkennung gefunden")

        if not available_pms:
            logger.error("Kein Paketmanager erkannt!")

        return available_pms

    def _detect_universal_package_managers(self) -> list[str]:
        """
        Erkennt universelle Paketmanager wie Snap und Flatpak

        Returns:
            Liste von verfügbaren universellen Paketmanagern
        """
        universal_pms = []

        # Prüfe Snap
        if os.path.exists("/usr/bin/snap") or os.path.exists("/snap/bin/snap"):
            universal_pms.append("snap")
            logger.info("Snap gefunden")

        # Prüfe Flatpak
        if os.path.exists("/usr/bin/flatpak"):
            universal_pms.append("flatpak")
            logger.info("Flatpak gefunden")

        return universal_pms

    def get_filter_files(self) -> list[str]:
        """
        Gibt die relevanten Filter-Dateien für die aktuelle Distribution zurück

        Returns:
            Liste von Filter-Dateinamen (ohne Pfad)
        """
        if self._distro_info is None:
            self.detect()

        filter_files = ["common.json"]  # Immer common.json laden

        # Füge distro-spezifische Filter hinzu
        distro_name = self._distro_info.name

        # Direkte Zuordnung
        distro_filter_map = {
            "ubuntu": "debian.json",
            "debian": "debian.json",
            "linuxmint": "debian.json",
            "mint": "debian.json",
            "arch": "arch.json",
            "manjaro": "arch.json",
            "endeavouros": "arch.json",
            "garuda": "arch.json",
            "fedora": "fedora.json",
            "rhel": "fedora.json",
            "centos": "fedora.json",
            "solus": "solus.json",
            "opensuse": "opensuse.json",
            "opensuse-leap": "opensuse.json",
            "opensuse-tumbleweed": "opensuse.json",
        }

        if distro_name in distro_filter_map:
            filter_files.append(distro_filter_map[distro_name])
        else:
            # Fallback auf ID_LIKE
            for like_id in self._distro_info.id_like:
                if like_id in distro_filter_map:
                    filter_files.append(distro_filter_map[like_id])
                    break

        logger.info(f"Filter-Dateien: {', '.join(filter_files)}")
        return filter_files


# Globale Instanz für einfachen Zugriff
_detector = DistroDetector()


def get_distro_info() -> DistroInfo:
    """
    Convenience-Funktion zur Distro-Erkennung

    Returns:
        DistroInfo: Informationen über die aktuelle Distribution
    """
    return _detector.detect()


def get_filter_files() -> list[str]:
    """
    Convenience-Funktion für Filter-Dateien

    Returns:
        Liste von Filter-Dateinamen
    """
    return _detector.get_filter_files()
