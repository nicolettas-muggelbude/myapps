"""
Paketmanager-Abstraktionsmodul für MyApps
Unterstützt verschiedene Paketmanager auf unterschiedlichen Linux-Distributionen
"""

import configparser
import gzip
import locale
import subprocess
import logging
from datetime import datetime
from pathlib import Path
from typing import Optional, List
from dataclasses import dataclass
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)


@dataclass
class Package:
    """Repräsentiert ein installiertes Paket"""
    name: str
    version: str
    package_type: str  # z.B. "deb", "rpm", "snap", "flatpak", "desktop"
    description: Optional[str] = None
    size: Optional[int] = None          # Installierte Größe in Bytes (Issue #5)
    install_date: Optional[str] = None  # Installationsdatum "YYYY-MM-DD" (Issue #10)
    icon_name: Optional[str] = None     # Icon-Name aus .desktop-Datei (v0.3.1)
    update_available: Optional[bool] = None  # Update verfügbar? None = noch nicht geprüft


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

        # Hole Pakete mit Größe — OHNE ${Description}: mehrzeilige Beschreibungen
        # brechen das Tab-Parsing (letzte Fortsetzungszeile enthält ${Installed-Size}
        # nach einem Tab → wird als falscher Paketname geparst).
        # Beschreibungen werden asynchron via apt-cache nachgeladen (gui_gtk.py).
        output = self._run_command([
            "dpkg-query", "-W",
            "--showformat=${Package}\t${Version}\t${Installed-Size}\n"
        ])
        if not output:
            return packages

        # Installationsdaten aus dpkg.log lesen (Issue #10)
        install_dates = self._get_install_dates()

        for line in output.splitlines():
            if not line.strip():
                continue

            parts = line.split("\t")
            if len(parts) >= 2:
                package_name = parts[0].strip()
                version = parts[1].strip()

                # Sicherheitscheck: Paketname darf keine Leerzeichen enthalten
                if not package_name or " " in package_name:
                    continue

                # Größe in KB → Bytes umrechnen (${Installed-Size} gibt KB)
                size = None
                if len(parts) >= 3:
                    try:
                        size_kb = int(parts[2].strip())
                        size = size_kb * 1024
                    except (ValueError, IndexError):
                        pass

                packages.append(Package(
                    name=package_name,
                    version=version,
                    package_type="deb",
                    description=None,  # Wird asynchron via apt-cache geladen
                    size=size,
                    install_date=install_dates.get(package_name)
                ))

        logger.info(f"DEB: {len(packages)} Pakete gefunden")
        return packages

    def _get_install_dates(self) -> dict:
        """
        Liest Installationsdaten aus /var/log/dpkg.log* (inkl. rotierte/komprimierte Logs).
        Älteste Dateien zuerst lesen, damit neuere Einträge gewinnen.
        """
        dates = {}
        # Alle dpkg.log Dateien, älteste zuerst (reverse=True: .2.gz → .1 → aktuell)
        log_files = sorted(Path("/var/log").glob("dpkg.log*"), reverse=True)

        for log_file in log_files:
            try:
                if log_file.suffix == ".gz":
                    opener, mode = gzip.open, "rt"
                else:
                    opener, mode = open, "r"

                with opener(log_file, mode, encoding="utf-8", errors="replace") as f:
                    for line in f:
                        # Format: "2024-12-26 10:15:23 install packagename:amd64 ..."
                        parts = line.split()
                        if len(parts) >= 4 and parts[2] in ("install", "upgrade"):
                            pkg_name = parts[3].split(":")[0]  # Architektur-Suffix entfernen
                            dates[pkg_name] = parts[0]  # "YYYY-MM-DD"
            except Exception as e:
                logger.debug(f"Fehler beim Lesen von {log_file}: {e}")

        logger.info(f"DEB: Installationsdaten für {len(dates)} Pakete geladen")
        return dates

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

        # Größen + Installationsdaten via pacman -Qi (ein Aufruf, Issue #5 + #10)
        pkg_info = self._get_package_info()

        for line in output.splitlines():
            if not line.strip():
                continue

            parts = line.split()
            if len(parts) >= 2:
                package_name = parts[0]
                version = parts[1]
                info = pkg_info.get(package_name, {})

                packages.append(Package(
                    name=package_name,
                    version=version,
                    package_type="pkg",
                    size=info.get("size"),
                    install_date=info.get("date")
                ))

        logger.info(f"Pacman: {len(packages)} Pakete gefunden")
        return packages

    def _get_package_info(self) -> dict:
        """
        Holt Größen + Installationsdaten aus einem einzigen 'pacman -Qi' Aufruf.
        Gibt dict {pkg_name: {"size": int|None, "date": str|None}} zurück.
        """
        info = {}
        output = self._run_command(["pacman", "-Qi"])
        if not output:
            return info

        current_name = None
        current = {}

        for line in output.splitlines():
            if line.startswith("Name "):
                # Neues Paket beginnt — vorheriges speichern
                if current_name:
                    info[current_name] = current
                current_name = line.split(":", 1)[1].strip()
                current = {}
            elif line.startswith("Installed Size") and current_name:
                current["size"] = self._parse_size(line.split(":", 1)[1].strip())
            elif line.startswith("Install Date") and current_name:
                current["date"] = self._parse_date(line.split(":", 1)[1].strip())

        # Letztes Paket nicht vergessen
        if current_name:
            info[current_name] = current

        return info

    def _parse_size(self, size_str: str) -> Optional[int]:
        """Parst Größenstrings wie '74.87 KiB', '1.23 MiB', '2.00 GiB'"""
        try:
            parts = size_str.split()
            if len(parts) >= 2:
                value = float(parts[0])
                unit = parts[1].upper()
                if unit == "B":
                    return int(value)
                elif unit in ("KIB", "KB"):
                    return int(value * 1024)
                elif unit in ("MIB", "MB"):
                    return int(value * 1024 * 1024)
                elif unit in ("GIB", "GB"):
                    return int(value * 1024 * 1024 * 1024)
        except Exception:
            pass
        return None

    def _parse_date(self, date_str: str) -> Optional[str]:
        """
        Parst Pacman-Datumsformat in 'YYYY-MM-DD'.
        Typisches Format: "Thu 26 Dec 2024 10:15:23 AM CET"
        """
        # Zeitzone am Ende entfernen (letztes Wort)
        parts = date_str.rsplit(" ", 1)
        date_clean = parts[0].strip()

        formats = [
            "%a %d %b %Y %I:%M:%S %p",  # "Thu 26 Dec 2024 10:15:23 AM"
            "%a %d %b %Y %H:%M:%S",      # "Thu 26 Dec 2024 10:15:23"
        ]
        for fmt in formats:
            try:
                dt = datetime.strptime(date_clean, fmt)
                return dt.strftime("%Y-%m-%d")
            except ValueError:
                continue
        return None


class RpmPackageManager(PackageManagerBase):
    """Paketmanager für Fedora/RHEL/CentOS/openSUSE (rpm)"""

    def __init__(self):
        super().__init__("rpm")

    def get_installed_packages(self) -> List[Package]:
        """Gibt alle installierten RPM-Pakete zurück"""
        packages = []

        # rpm -qa gibt alle installierten Pakete aus (Größe + Datum, Issue #5 + #10)
        output = self._run_command([
            "rpm", "-qa", "--queryformat",
            "%{NAME}\t%{VERSION}-%{RELEASE}\t%{SIZE}\t%{INSTALLTIME}\n"
        ])
        if not output:
            return packages

        for line in output.splitlines():
            if not line.strip():
                continue

            parts = line.split("\t")
            if len(parts) >= 2:
                package_name = parts[0]
                version = parts[1]

                # Größe direkt in Bytes (%{SIZE} liefert Bytes)
                size = None
                if len(parts) >= 3:
                    try:
                        size = int(parts[2].strip())
                    except (ValueError, IndexError):
                        pass

                # Installationsdatum aus Unix-Timestamp (%{INSTALLTIME})
                install_date = None
                if len(parts) >= 4:
                    try:
                        timestamp = int(parts[3].strip())
                        install_date = datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d")
                    except (ValueError, OSError):
                        pass

                packages.append(Package(
                    name=package_name,
                    version=version,
                    package_type="rpm",
                    size=size,
                    install_date=install_date
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

        # Snap-Namen sammeln für Batch-Aufruf
        snap_data = []
        for line in output.splitlines()[1:]:  # Überspringe Header
            if not line.strip():
                continue
            parts = line.split()
            if len(parts) >= 2:
                snap_data.append((parts[0], parts[1]))

        # Größen in einem Aufruf (Issue #5)
        snap_names = [name for name, _ in snap_data]
        sizes = self._get_sizes(snap_names)

        for package_name, version in snap_data:
            packages.append(Package(
                name=package_name,
                version=version,
                package_type="snap",
                size=sizes.get(package_name),
                install_date=self._get_install_date(package_name)
            ))

        logger.info(f"Snap: {len(packages)} Pakete gefunden")
        return packages

    def _get_sizes(self, snap_names: List[str]) -> dict:
        """Holt installierte Größen aller Snaps in einem einzigen du-Aufruf"""
        sizes = {}
        paths = [f"/snap/{name}/current" for name in snap_names
                 if Path(f"/snap/{name}/current").exists()]
        if not paths:
            return sizes
        try:
            result = subprocess.run(
                ["du", "-sb"] + paths,
                capture_output=True, text=True, timeout=30
            )
            if result.returncode == 0:
                for line in result.stdout.splitlines():
                    parts = line.split()
                    if len(parts) >= 2:
                        snap_name = Path(parts[1]).parent.name  # /snap/<name>/current → <name>
                        sizes[snap_name] = int(parts[0])
        except Exception as e:
            logger.debug(f"Snap du-Aufruf fehlgeschlagen: {e}")
        return sizes

    def _get_install_date(self, snap_name: str) -> Optional[str]:
        """Liest Installationsdatum aus mtime von /snap/<name>/current"""
        path = Path(f"/snap/{snap_name}/current")
        try:
            if path.exists():
                mtime = path.stat().st_mtime
                return datetime.fromtimestamp(mtime).strftime("%Y-%m-%d")
        except OSError:
            pass
        return None


class FlatpakPackageManager(PackageManagerBase):
    """Paketmanager für Flatpak"""

    def __init__(self):
        super().__init__("flatpak")

    def get_installed_packages(self) -> List[Package]:
        """Gibt alle installierten Flatpak-Apps zurück"""
        packages = []

        # installed-size Spalte hinzugefügt (Issue #5)
        output = self._run_command([
            "flatpak", "list", "--app",
            "--columns=name,application,version,installed-size"
        ])
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

                # Größe: installed-size liefert Bytes als int (Issue #5)
                size = None
                if len(parts) >= 4:
                    try:
                        size = int(parts[3].strip())
                    except ValueError:
                        pass

                # Datum aus Filesystem (Issue #10)
                install_date = self._get_install_date(app_id)

                # Verwende App-ID als Namen (z.B. org.mozilla.firefox)
                packages.append(Package(
                    name=app_id,
                    version=version,
                    package_type="flatpak",
                    description=display_name,
                    size=size,
                    install_date=install_date
                ))

        logger.info(f"Flatpak: {len(packages)} Pakete gefunden")
        return packages

    def _get_install_date(self, app_id: str) -> Optional[str]:
        """
        Liest Installationsdatum aus mtime des Flatpak-App-Verzeichnisses.
        Prüft System- und User-Installation.
        """
        search_paths = [
            Path("/var/lib/flatpak/app") / app_id,
            Path.home() / ".local/share/flatpak/app" / app_id,
        ]
        for path in search_paths:
            try:
                if path.exists():
                    mtime = path.stat().st_mtime
                    return datetime.fromtimestamp(mtime).strftime("%Y-%m-%d")
            except OSError:
                pass
        return None


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


class DesktopFileManager(PackageManagerBase):
    """
    Liest .desktop-Dateien und gibt grafische Anwendungen zurück (v0.3.1, Issue #4).
    Unabhängig vom Paketmanager — zeigt was der Desktop-Launcher kennt.
    """

    # Suchpfade in Prioritätsreihenfolge (system vor user)
    _SYSTEM_PATHS = [
        Path("/usr/share/applications"),
        Path("/usr/local/share/applications"),
        Path("/var/lib/flatpak/exports/share/applications"),
        Path("/var/lib/snapd/desktop/applications"),
    ]

    def __init__(self):
        super().__init__("desktop")

    def get_installed_packages(self) -> List[Package]:
        """Liest alle .desktop-Dateien und gibt sortierte App-Liste zurück"""
        apps: List[Package] = []
        # Duplikate via Namen vermeiden (erster Treffer gewinnt)
        seen_names: set = set()

        # User-Pfade dynamisch ergänzen
        home = Path.home()
        search_paths = list(self._SYSTEM_PATHS) + [
            home / ".local/share/applications",
            home / ".local/share/flatpak/exports/share/applications",
        ]

        for path in search_paths:
            if not path.exists():
                continue
            for desktop_file in sorted(path.glob("*.desktop")):
                try:
                    pkg = self._parse_desktop_file(desktop_file)
                    if pkg and pkg.name not in seen_names:
                        seen_names.add(pkg.name)
                        apps.append(pkg)
                except Exception as e:
                    logger.debug(f"Fehler beim Parsen von {desktop_file}: {e}")

        logger.info(f"{len(apps)} Desktop-Apps aus .desktop-Dateien geladen")
        return sorted(apps, key=lambda p: p.name.lower())

    def _parse_desktop_file(self, path: Path) -> Optional[Package]:
        """Parst eine einzelne .desktop-Datei und gibt Package zurück"""
        config = configparser.RawConfigParser(interpolation=None)
        try:
            config.read(str(path), encoding="utf-8")
        except Exception:
            return None

        if "Desktop Entry" not in config:
            return None

        entry = config["Desktop Entry"]

        # Nur Typ Application (kein Link, Directory usw.)
        if entry.get("Type", "") != "Application":
            return None

        # Ausgeblendete Apps überspringen
        if entry.get("NoDisplay", "false").lower() == "true":
            return None
        if entry.get("Hidden", "false").lower() == "true":
            return None

        # Sprachcode für lokalisierte Felder (z.B. "de")
        lang_code = (locale.getlocale()[0] or "").split("_")[0].lower()

        # Lokalisierter Name — Fallback: Dateiname ohne Endung
        name = (
            entry.get(f"Name[{lang_code}]") or
            entry.get("Name") or
            path.stem
        )
        if not name:
            return None

        # Lokalisierter Kommentar
        comment = (
            entry.get(f"Comment[{lang_code}]") or
            entry.get("Comment") or
            ""
        )

        # Kategorien als Fallback für Beschreibung
        categories_raw = entry.get("Categories", "")
        categories = categories_raw.rstrip(";").replace(";", ", ") if categories_raw else ""

        # Icon-Name aus .desktop (oft != Paketname)
        icon_name = entry.get("Icon", "") or None

        # Paket-Typ aus Pfad ableiten
        path_str = str(path)
        if "flatpak" in path_str:
            pkg_type = "flatpak"
        elif "snap" in path_str or "snapd" in path_str:
            pkg_type = "snap"
        else:
            pkg_type = "desktop"

        description = comment if comment else categories

        return Package(
            name=name,
            version="",
            package_type=pkg_type,
            description=description or None,
            size=None,
            install_date=None,
            icon_name=icon_name,
        )


class UpdateChecker:
    """Prüft welche installierten Pakete Updates haben (Issue #7)"""

    def get_updatable_packages(self, pm_names: List[str]) -> set:
        """
        Gibt Menge der Paketnamen zurück, für die Updates verfügbar sind.

        Args:
            pm_names: Liste aktiver Paketmanager-Namen aus DistroInfo

        Returns:
            Menge von Paketnamen mit verfügbaren Updates
        """
        updatable: set = set()

        if "dpkg" in pm_names:
            updatable.update(self._check_apt())
        if "pacman" in pm_names:
            updatable.update(self._check_pacman())
        if "dnf" in pm_names:
            updatable.update(self._check_dnf())
        elif "zypper" in pm_names:
            updatable.update(self._check_zypper())
        if "snap" in pm_names:
            updatable.update(self._check_snap())
        if "flatpak" in pm_names:
            updatable.update(self._check_flatpak())

        logger.info(f"UpdateChecker: {len(updatable)} Pakete mit Updates gefunden")
        return updatable

    def _run(self, command: List[str], allow_nonzero: bool = False, timeout: int = 30) -> Optional[str]:
        """Führt Befehl aus, gibt stdout zurück oder None bei Fehler/Timeout"""
        try:
            result = subprocess.run(
                command, capture_output=True, text=True, timeout=timeout
            )
            if result.returncode == 0 or allow_nonzero:
                return result.stdout
            return None
        except (subprocess.TimeoutExpired, FileNotFoundError, OSError) as e:
            logger.debug(f"Update-Check '{command[0]}' fehlgeschlagen: {e}")
            return None

    def _check_apt(self) -> set:
        """Prüft via 'apt list --upgradable' (Debian/Ubuntu)"""
        names: set = set()
        output = self._run(["apt", "list", "--upgradable"])
        if not output:
            return names
        for line in output.splitlines():
            # Format: "packagename/focal-updates VERSION ARCH [upgradable from: OLD]"
            if "/" in line and "upgradable" in line:
                names.add(line.split("/")[0].strip())
        return names

    def _check_pacman(self) -> set:
        """Prüft via checkupdates (Arch), Fallback auf pacman -Qu"""
        names: set = set()
        # checkupdates bevorzugt — kein root nötig, kein DB-Lock
        output = self._run(["checkupdates"])
        if output is None:
            output = self._run(["pacman", "-Qu"])
        if not output:
            return names
        for line in output.splitlines():
            # Format: "packagename OLD -> NEW"
            parts = line.split()
            if parts:
                names.add(parts[0])
        return names

    def _check_dnf(self) -> set:
        """Prüft via 'dnf check-update' (Fedora/RHEL) — Exit-Code 100 = Updates vorhanden"""
        names: set = set()
        output = self._run(["dnf", "check-update", "--quiet"], allow_nonzero=True)
        if not output:
            return names
        for line in output.splitlines():
            # Format: "packagename.arch VERSION REPO"
            parts = line.split()
            if parts and not line.startswith((" ", "Last", "Obsoleting")):
                pkg_name = parts[0].rsplit(".", 1)[0]  # Architektur-Suffix entfernen
                if pkg_name:
                    names.add(pkg_name)
        return names

    def _check_zypper(self) -> set:
        """Prüft via 'zypper list-updates' (openSUSE)"""
        names: set = set()
        output = self._run(["zypper", "--non-interactive", "list-updates", "--type", "package"])
        if not output:
            return names
        for line in output.splitlines():
            # Format: "| S | Repository | Name | Current Ver | Available Ver | Arch |"
            if line.startswith("|") and "Name" not in line and "---" not in line:
                parts = [p.strip() for p in line.split("|")]
                # parts: ["", S, Repo, Name, ...]
                if len(parts) >= 4 and parts[3]:
                    names.add(parts[3])
        return names

    def _check_snap(self) -> set:
        """Prüft via 'snap refresh --list' (Snap)"""
        names: set = set()
        output = self._run(["snap", "refresh", "--list"])
        if not output:
            return names
        for line in output.splitlines()[1:]:  # Überspringe Header
            parts = line.split()
            if parts:
                names.add(parts[0])
        return names

    def _check_flatpak(self) -> set:
        """Prüft via 'flatpak remote-ls --updates' (Flatpak)"""
        names: set = set()
        output = self._run([
            "flatpak", "remote-ls", "--updates", "--columns=application"
        ])
        if not output:
            return names
        for line in output.splitlines():
            line = line.strip()
            if line:
                names.add(line)
        return names
