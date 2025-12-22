"""
Icon-Management-System für MyApps
Lädt Icons aus System-Verzeichnissen mit Fallback auf generische Icons
"""

import os
import logging
from pathlib import Path
from typing import Optional, Dict
from PIL import Image, ImageTk
import tkinter as tk

logger = logging.getLogger(__name__)


class IconManager:
    """Verwaltet App-Icons mit System-Integration und Fallbacks"""

    # Standard-Icon-Suchpfade (in Prioritätsreihenfolge)
    ICON_SEARCH_PATHS = [
        "/usr/share/pixmaps",
        "/usr/share/icons/hicolor/32x32/apps",
        "/usr/share/icons/hicolor/48x48/apps",
        "/usr/share/icons/hicolor/64x64/apps",
        "/usr/share/icons/hicolor/scalable/apps",
        "~/.local/share/icons/hicolor/32x32/apps",
        "~/.local/share/icons/hicolor/48x48/apps",
        "/var/lib/flatpak/exports/share/icons/hicolor/32x32/apps",
        "/var/lib/flatpak/exports/share/icons/hicolor/48x48/apps",
        "/var/lib/flatpak/exports/share/icons/hicolor/64x64/apps",
    ]

    # Snap-spezifische Pfade
    SNAP_ICON_PATHS = [
        "~/.local/share/icons",
        "/var/lib/snapd/desktop/icons",
    ]

    # Icon-Datei-Endungen (in Prioritätsreihenfolge)
    ICON_EXTENSIONS = [".png", ".svg", ".xpm", ".jpg", ".jpeg"]

    def __init__(self, icon_size: int = 32, fallback_dir: Optional[str] = None):
        """
        Initialisiert den IconManager

        Args:
            icon_size: Zielgröße für Icons in Pixeln (Standard: 32)
            fallback_dir: Verzeichnis mit Fallback-Icons
        """
        self.icon_size = icon_size
        self.fallback_dir = Path(fallback_dir) if fallback_dir else None
        self._icon_cache: Dict[str, ImageTk.PhotoImage] = {}
        self._default_icon: Optional[ImageTk.PhotoImage] = None

        # Erweitere Suchpfade mit expanduser
        self.icon_search_paths = [
            Path(p).expanduser() for p in self.ICON_SEARCH_PATHS
        ]
        self.snap_icon_paths = [
            Path(p).expanduser() for p in self.SNAP_ICON_PATHS
        ]

    def get_icon(self, package_name: str, package_type: str) -> ImageTk.PhotoImage:
        """
        Holt das Icon für ein Paket

        Args:
            package_name: Name des Pakets
            package_type: Typ des Pakets ("deb", "snap", "flatpak", etc.)

        Returns:
            PhotoImage-Objekt (entweder App-Icon oder Fallback)
        """
        # Prüfe Cache
        cache_key = f"{package_type}:{package_name}"
        if cache_key in self._icon_cache:
            return self._icon_cache[cache_key]

        # Versuche Icon zu finden
        icon_path = self._find_icon(package_name, package_type)

        if icon_path and icon_path.exists():
            try:
                icon = self._load_and_resize_icon(icon_path)
                self._icon_cache[cache_key] = icon
                return icon
            except Exception as e:
                logger.debug(f"Fehler beim Laden von Icon {icon_path}: {e}")

        # Fallback auf Standard-Icon
        default_icon = self._get_default_icon()
        self._icon_cache[cache_key] = default_icon
        return default_icon

    def _find_icon(self, package_name: str, package_type: str) -> Optional[Path]:
        """
        Sucht das Icon für ein Paket

        Args:
            package_name: Name des Pakets
            package_type: Typ des Pakets

        Returns:
            Pfad zum Icon oder None
        """
        # Spezielle Behandlung für verschiedene Pakettypen
        if package_type == "snap":
            icon_path = self._find_snap_icon(package_name)
            if icon_path:
                return icon_path

        elif package_type == "flatpak":
            icon_path = self._find_flatpak_icon(package_name)
            if icon_path:
                return icon_path

        # Standard-Suche in allen Pfaden
        return self._find_system_icon(package_name)

    def _find_system_icon(self, package_name: str) -> Optional[Path]:
        """
        Sucht ein Icon in den Standard-System-Verzeichnissen

        Args:
            package_name: Name des Pakets

        Returns:
            Pfad zum Icon oder None
        """
        # Bereinige Paketnamen (entferne Arch-Suffix, Version-Nummern etc.)
        clean_names = self._get_icon_name_variants(package_name)

        for icon_dir in self.icon_search_paths:
            if not icon_dir.exists():
                continue

            for name in clean_names:
                for ext in self.ICON_EXTENSIONS:
                    icon_path = icon_dir / f"{name}{ext}"
                    if icon_path.exists():
                        logger.debug(f"Icon gefunden: {icon_path}")
                        return icon_path

        return None

    def _find_snap_icon(self, package_name: str) -> Optional[Path]:
        """
        Sucht ein Icon für ein Snap-Paket

        Args:
            package_name: Name des Snap-Pakets

        Returns:
            Pfad zum Icon oder None
        """
        for icon_dir in self.snap_icon_paths:
            if not icon_dir.exists():
                continue

            # Snap-Icons haben oft die Form: snap.package-name.icon-name
            for size_dir in ["32x32", "48x48", "64x64", "scalable"]:
                search_dir = icon_dir / "hicolor" / size_dir / "apps"
                if not search_dir.exists():
                    continue

                for ext in self.ICON_EXTENSIONS:
                    # Versuche verschiedene Snap-Icon-Namenskonventionen
                    candidates = [
                        search_dir / f"snap.{package_name}.{package_name}{ext}",
                        search_dir / f"snap.{package_name}{ext}",
                        search_dir / f"{package_name}{ext}",
                    ]

                    for candidate in candidates:
                        if candidate.exists():
                            logger.debug(f"Snap-Icon gefunden: {candidate}")
                            return candidate

        # Fallback auf Standard-Suche
        return self._find_system_icon(package_name)

    def _find_flatpak_icon(self, package_name: str) -> Optional[Path]:
        """
        Sucht ein Icon für ein Flatpak-Paket

        Args:
            package_name: Name/ID des Flatpak-Pakets (z.B. org.mozilla.firefox)

        Returns:
            Pfad zum Icon oder None
        """
        # Flatpak-Icons sind meist unter dem vollen App-ID zu finden
        flatpak_icon_bases = [
            Path("/var/lib/flatpak/exports/share/icons"),
            Path.home() / ".local/share/flatpak/exports/share/icons",
        ]

        for icon_base in flatpak_icon_bases:
            if not icon_base.exists():
                continue

            for size_dir in ["32x32", "48x48", "64x64", "128x128", "scalable"]:
                search_dir = icon_base / "hicolor" / size_dir / "apps"
                if not search_dir.exists():
                    continue

                for ext in self.ICON_EXTENSIONS:
                    icon_path = search_dir / f"{package_name}{ext}"
                    if icon_path.exists():
                        logger.debug(f"Flatpak-Icon gefunden: {icon_path}")
                        return icon_path

        # Fallback: Versuche letzten Teil des App-IDs (z.B. "firefox" aus "org.mozilla.firefox")
        if "." in package_name:
            short_name = package_name.split(".")[-1]
            return self._find_system_icon(short_name)

        return None

    def _get_icon_name_variants(self, package_name: str) -> list[str]:
        """
        Generiert verschiedene Varianten des Paketnamens für die Icon-Suche

        Args:
            package_name: Ursprünglicher Paketname

        Returns:
            Liste von möglichen Icon-Namen
        """
        variants = [package_name]

        # Entferne Architektur-Suffixe (:amd64, :i386, etc.)
        if ":" in package_name:
            base_name = package_name.split(":")[0]
            variants.append(base_name)

        # Entferne Versionsnummern und -Suffixe
        clean_name = package_name.split("-")[0]
        if clean_name != package_name:
            variants.append(clean_name)

        # Flatpak: Letzter Teil des IDs
        if "." in package_name:
            short_name = package_name.split(".")[-1]
            variants.append(short_name)

        return variants

    def _load_and_resize_icon(self, icon_path: Path) -> ImageTk.PhotoImage:
        """
        Lädt ein Icon und skaliert es auf die Zielgröße

        Args:
            icon_path: Pfad zum Icon

        Returns:
            PhotoImage-Objekt

        Raises:
            Exception: Bei Fehler beim Laden
        """
        img = Image.open(icon_path)

        # Konvertiere zu RGBA falls nötig
        if img.mode != "RGBA":
            img = img.convert("RGBA")

        # Skaliere auf Zielgröße (erhält Seitenverhältnis)
        img.thumbnail((self.icon_size, self.icon_size), Image.Resampling.LANCZOS)

        return ImageTk.PhotoImage(img)

    def _get_default_icon(self) -> ImageTk.PhotoImage:
        """
        Gibt das Standard-Fallback-Icon zurück

        Returns:
            PhotoImage-Objekt mit generischem Icon
        """
        if self._default_icon is not None:
            return self._default_icon

        # Versuche Fallback-Icon aus fallback_dir zu laden
        if self.fallback_dir:
            fallback_path = self.fallback_dir / "default-app.png"
            if fallback_path.exists():
                try:
                    self._default_icon = self._load_and_resize_icon(fallback_path)
                    return self._default_icon
                except Exception as e:
                    logger.warning(f"Fehler beim Laden des Fallback-Icons: {e}")

        # Erstelle ein einfaches Standard-Icon (grauer Platzhalter)
        self._default_icon = self._create_placeholder_icon()
        return self._default_icon

    def _create_placeholder_icon(self) -> ImageTk.PhotoImage:
        """
        Erstellt ein einfaches Platzhalter-Icon

        Returns:
            PhotoImage-Objekt mit Platzhalter
        """
        # Erstelle ein graues Quadrat als Platzhalter
        img = Image.new("RGBA", (self.icon_size, self.icon_size), (128, 128, 128, 255))
        return ImageTk.PhotoImage(img)

    def clear_cache(self) -> None:
        """Leert den Icon-Cache"""
        self._icon_cache.clear()
        logger.info("Icon-Cache geleert")

    def preload_icons(self, packages: list) -> None:
        """
        Lädt Icons für eine Liste von Paketen vor (für bessere Performance)

        Args:
            packages: Liste von Package-Objekten
        """
        logger.info(f"Lade Icons für {len(packages)} Pakete vor...")

        for package in packages:
            self.get_icon(package.name, package.package_type)

        logger.info("Icon-Vorladung abgeschlossen")
