"""
Paketmanager-Abstraktionsmodul für MyApps
Unterstützt verschiedene Paketmanager auf unterschiedlichen Linux-Distributionen
"""

import subprocess
import logging
from typing import Optional, List
from dataclasses import dataclass
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)


@dataclass
class Package:
    """Repräsentiert ein installiertes Paket"""
    name: str
    version: str
    package_type: str  # z.B. "deb", "rpm", "snap", "flatpak"
    description: Optional[str] = None


class PackageManagerBase(ABC):
    """Basis-Klasse für alle Paketmanager"""

    def __init__(self, pm_type: str):
        self.pm_type = pm_type

    @abstractmethod
    def get_installed_packages(self) -> List[Package]:
        """
        Gibt alle installierten Pakete zurück

        Returns:
            Liste von Package-Objekten
        """
        pass

    def _run_command(self, command: List[str]) -> Optional[str]:
        """
        Führt einen Befehl aus und gibt die Ausgabe zurück

        Args:
            command: Liste von Befehlsargumenten

        Returns:
            Ausgabe des Befehls oder None bei Fehler
        """
        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout
        except subprocess.CalledProcessError as e:
            logger.error(f"Fehler beim Ausführen von {' '.join(command)}: {e}")
            return None
        except FileNotFoundError:
            logger.warning(f"Befehl nicht gefunden: {command[0]}")
            return None


class DpkgPackageManager(PackageManagerBase):
    """Paketmanager für Debian/Ubuntu/Mint (dpkg)"""

    def __init__(self):
        super().__init__("deb")

    def get_installed_packages(self) -> List[Package]:
        """Gibt alle installierten DEB-Pakete zurück"""
        packages = []

        # Hole Paketliste (schnell, ohne Beschreibungen)
        output = self._run_command(["dpkg-query", "-W", "--showformat=${Package}\t${Version}\n"])
        if not output:
            return packages

        # Erstelle Package-Objekte
        for line in output.splitlines():
            if not line.strip():
                continue

            parts = line.split("\t")
            if len(parts) >= 2:
                package_name = parts[0].strip()
                version = parts[1].strip()

                # Hole lokalisierte Beschreibung via apt-cache (respektiert LANG)
                description = self._get_localized_description(package_name)

                packages.append(Package(
                    name=package_name,
                    version=version,
                    package_type="deb",
                    description=description
                ))

        logger.info(f"DEB: {len(packages)} Pakete gefunden")
        return packages

    def _get_localized_description(self, package_name: str) -> Optional[str]:
        """Holt lokalisierte Beschreibung via apt-cache (respektiert System-Locale)"""
        output = self._run_command(["apt-cache", "show", package_name])
        if not output:
            return None

        # Parse apt-cache output für Description
        for line in output.splitlines():
            if line.startswith("Description:") or line.startswith("Description-de:") or line.startswith("Description-en:"):
                # Nimm ersten gefundenen Description-Header (apt-cache gibt locale-spezifische zuerst)
                desc = line.split(":", 1)[1].strip()
                return desc if desc else None

        return None

    def get_package_description(self, package_name: str) -> Optional[str]:
        """
        Holt ausführliche Beschreibung für ein Paket (lazy loading)

        Args:
            package_name: Name des Pakets

        Returns:
            Beschreibung oder None
        """
        try:
            output = self._run_command(["dpkg", "-s", package_name])
            if not output:
                return None

            # Sammle alle Beschreibungszeilen
            description_lines = []
            in_description = False

            for line in output.splitlines():
                if line.startswith("Description:"):
                    in_description = True
                    # Erste Zeile der Beschreibung
                    desc = line[12:].strip()
                    if desc:
                        description_lines.append(desc)
                elif in_description:
                    if line.startswith(" "):
                        # Fortsetzung der Beschreibung
                        description_lines.append(line.strip())
                    else:
                        # Nächstes Feld, Beschreibung ist zu Ende
                        break

            if description_lines:
                # Maximal 3 Zeilen für Tooltip
                return " ".join(description_lines[:3])

            return None
        except Exception:
            return None


class PacmanPackageManager(PackageManagerBase):
    """Paketmanager für Arch Linux (pacman)"""

    def __init__(self):
        super().__init__("pkg")

    def get_installed_packages(self) -> List[Package]:
        """Gibt alle installierten Pacman-Pakete zurück"""
        packages = []

        output = self._run_command(["pacman", "-Q"])
        if not output:
            return packages

        for line in output.splitlines():
            if not line.strip():
                continue

            parts = line.split()
            if len(parts) >= 2:
                package_name = parts[0]
                version = parts[1]

                packages.append(Package(
                    name=package_name,
                    version=version,
                    package_type="pkg"
                ))

        logger.info(f"Pacman: {len(packages)} Pakete gefunden")
        return packages


class RpmPackageManager(PackageManagerBase):
    """Paketmanager für Fedora/RHEL/CentOS/openSUSE (rpm)"""

    def __init__(self):
        super().__init__("rpm")

    def get_installed_packages(self) -> List[Package]:
        """Gibt alle installierten RPM-Pakete zurück"""
        packages = []

        # rpm -qa gibt alle installierten Pakete aus
        output = self._run_command(["rpm", "-qa", "--queryformat", "%{NAME} %{VERSION}-%{RELEASE}\n"])
        if not output:
            return packages

        for line in output.splitlines():
            if not line.strip():
                continue

            parts = line.split(maxsplit=1)
            if len(parts) >= 2:
                package_name = parts[0]
                version = parts[1]

                packages.append(Package(
                    name=package_name,
                    version=version,
                    package_type="rpm"
                ))

        logger.info(f"RPM: {len(packages)} Pakete gefunden")
        return packages


class EopkgPackageManager(PackageManagerBase):
    """Paketmanager für Solus (eopkg)"""

    def __init__(self):
        super().__init__("eopkg")

    def get_installed_packages(self) -> List[Package]:
        """Gibt alle installierten eopkg-Pakete zurück"""
        packages = []

        output = self._run_command(["eopkg", "list-installed"])
        if not output:
            return packages

        for line in output.splitlines():
            if not line.strip():
                continue

            # eopkg list-installed Format: "package-name - version"
            if " - " in line:
                parts = line.split(" - ")
                if len(parts) >= 2:
                    package_name = parts[0].strip()
                    version = parts[1].strip()

                    packages.append(Package(
                        name=package_name,
                        version=version,
                        package_type="eopkg"
                    ))

        logger.info(f"eopkg: {len(packages)} Pakete gefunden")
        return packages


class SnapPackageManager(PackageManagerBase):
    """Paketmanager für Snap"""

    def __init__(self):
        super().__init__("snap")

    def get_installed_packages(self) -> List[Package]:
        """Gibt alle installierten Snap-Pakete zurück"""
        packages = []

        output = self._run_command(["snap", "list"])
        if not output:
            return packages

        for line in output.splitlines()[1:]:  # Überspringe Header
            if not line.strip():
                continue

            parts = line.split()
            if len(parts) >= 2:
                package_name = parts[0]
                version = parts[1]

                packages.append(Package(
                    name=package_name,
                    version=version,
                    package_type="snap"
                ))

        logger.info(f"Snap: {len(packages)} Pakete gefunden")
        return packages


class FlatpakPackageManager(PackageManagerBase):
    """Paketmanager für Flatpak"""

    def __init__(self):
        super().__init__("flatpak")

    def get_installed_packages(self) -> List[Package]:
        """Gibt alle installierten Flatpak-Apps zurück"""
        packages = []

        output = self._run_command(["flatpak", "list", "--app", "--columns=name,application,version"])
        if not output:
            return packages

        for line in output.splitlines():
            if not line.strip():
                continue

            parts = line.split("\t")
            if len(parts) >= 2:
                display_name = parts[0].strip()
                app_id = parts[1].strip()
                version = parts[2].strip() if len(parts) >= 3 else "unknown"

                # Verwende App-ID als Namen (z.B. org.mozilla.firefox)
                packages.append(Package(
                    name=app_id,
                    version=version,
                    package_type="flatpak",
                    description=display_name
                ))

        logger.info(f"Flatpak: {len(packages)} Pakete gefunden")
        return packages


class PackageManagerFactory:
    """Factory-Klasse zum Erstellen von Paketmanager-Instanzen"""

    _PACKAGE_MANAGERS = {
        "dpkg": DpkgPackageManager,
        "pacman": PacmanPackageManager,
        "rpm": RpmPackageManager,
        "dnf": RpmPackageManager,  # dnf verwendet rpm unter der Haube
        "zypper": RpmPackageManager,  # zypper verwendet rpm unter der Haube
        "eopkg": EopkgPackageManager,
        "snap": SnapPackageManager,
        "flatpak": FlatpakPackageManager,
    }

    @classmethod
    def create(cls, pm_name: str) -> Optional[PackageManagerBase]:
        """
        Erstellt eine Paketmanager-Instanz basierend auf dem Namen

        Args:
            pm_name: Name des Paketmanagers (z.B. "dpkg", "pacman")

        Returns:
            PackageManagerBase-Instanz oder None wenn unbekannt
        """
        pm_class = cls._PACKAGE_MANAGERS.get(pm_name.lower())
        if pm_class:
            return pm_class()
        else:
            logger.warning(f"Unbekannter Paketmanager: {pm_name}")
            return None

    @classmethod
    def get_all_packages(cls, package_managers: List[str]) -> List[Package]:
        """
        Holt alle Pakete von allen angegebenen Paketmanagern

        Args:
            package_managers: Liste von Paketmanager-Namen

        Returns:
            Kombinierte Liste aller Pakete
        """
        all_packages = []

        for pm_name in package_managers:
            pm = cls.create(pm_name)
            if pm:
                try:
                    packages = pm.get_installed_packages()
                    all_packages.extend(packages)
                except Exception as e:
                    logger.error(f"Fehler beim Abrufen der Pakete von {pm_name}: {e}")

        logger.info(f"Insgesamt {len(all_packages)} Pakete von {len(package_managers)} Paketmanagern gefunden")
        return all_packages
