"""
Internationalisierungs-Modul für MyApps
Unterstützt Deutsch und Englisch
"""

import gettext
import logging
import os
from pathlib import Path
from typing import Callable

logger = logging.getLogger(__name__)

# Globale Translation-Funktion
_: Callable[[str], str] = lambda x: x


def init_i18n(locale_dir: str, language: str = None) -> Callable[[str], str]:
    """
    Initialisiert das i18n-System

    Args:
        locale_dir: Pfad zum Verzeichnis mit Übersetzungen
        language: Sprachcode (z.B. 'de', 'en') - None für System-Sprache

    Returns:
        Translation-Funktion
    """
    global _

    try:
        # Bestimme Sprache
        if language is None:
            # Nutze System-Sprache
            language = os.environ.get('LANG', 'en_US').split('_')[0]

        # Erstelle Translations-Objekt
        locale_path = Path(locale_dir)

        if not locale_path.exists():
            logger.warning(f"Locale-Verzeichnis nicht gefunden: {locale_path}")
            logger.info("Verwende Englisch als Fallback")
            return lambda x: x

        # Versuche Übersetzung zu laden
        try:
            translation = gettext.translation(
                'myapps',
                localedir=str(locale_path),
                languages=[language],
                fallback=True
            )
            _ = translation.gettext
            logger.info(f"Sprache geladen: {language}")
        except Exception as e:
            logger.warning(f"Fehler beim Laden der Sprache {language}: {e}")
            logger.info("Verwende Englisch als Fallback")
            _ = lambda x: x

    except Exception as e:
        logger.error(f"Fehler bei i18n-Initialisierung: {e}")
        _ = lambda x: x

    return _


def get_available_languages(locale_dir: str) -> list[tuple[str, str]]:
    """
    Gibt verfügbare Sprachen zurück

    Args:
        locale_dir: Pfad zum Verzeichnis mit Übersetzungen

    Returns:
        Liste von (code, name) Tupeln (z.B. [('de', 'Deutsch'), ('en', 'English')])
    """
    available = [
        ('en', 'English'),  # Immer verfügbar (Fallback)
    ]

    locale_path = Path(locale_dir)
    if not locale_path.exists():
        return available

    # Prüfe welche Sprachen vorhanden sind
    for lang_dir in locale_path.iterdir():
        if lang_dir.is_dir() and (lang_dir / 'LC_MESSAGES' / 'myapps.mo').exists():
            lang_code = lang_dir.name

            # Mapping von Codes zu Namen
            lang_names = {
                'de': 'Deutsch',
                'en': 'English',
                'fr': 'Français',
                'es': 'Español',
                'it': 'Italiano',
            }

            lang_name = lang_names.get(lang_code, lang_code.upper())

            if (lang_code, lang_name) not in available:
                available.append((lang_code, lang_name))

    return sorted(available, key=lambda x: x[0])


def set_language(language: str, locale_dir: str) -> bool:
    """
    Wechselt die Sprache zur Laufzeit

    Args:
        language: Sprachcode (z.B. 'de', 'en')
        locale_dir: Pfad zum Verzeichnis mit Übersetzungen

    Returns:
        True bei Erfolg, False bei Fehler
    """
    global _

    try:
        locale_path = Path(locale_dir)

        if not locale_path.exists():
            logger.warning(f"Locale-Verzeichnis nicht gefunden: {locale_path}")
            return False

        translation = gettext.translation(
            'myapps',
            localedir=str(locale_path),
            languages=[language],
            fallback=True
        )
        _ = translation.gettext

        logger.info(f"Sprache gewechselt zu: {language}")
        return True

    except Exception as e:
        logger.error(f"Fehler beim Sprachwechsel: {e}")
        return False


# Strings für die Übersetzung (werden von gettext extrahiert)
# Diese dienen als Referenz für Übersetzer

TRANSLATABLE_STRINGS = {
    # Hauptfenster
    'app_title': 'MyApps - Installierte Anwendungen',
    'refresh': 'Aktualisieren',
    'export': 'Exportieren',
    'settings': 'Einstellungen',
    'about': 'Über',

    # Ansichten
    'view_table': 'Tabellenansicht',
    'view_list': 'Listenansicht',
    'switch_view': 'Ansicht wechseln',

    # Spaltenüberschriften
    'col_name': 'Name',
    'col_version': 'Version',
    'col_type': 'Typ',
    'col_description': 'Beschreibung',

    # Pakettypen
    'type_deb': 'DEB',
    'type_rpm': 'RPM',
    'type_pkg': 'PKG',
    'type_eopkg': 'eopkg',
    'type_snap': 'Snap',
    'type_flatpak': 'Flatpak',

    # Kontextmenü
    'context_hide': 'Als System-App markieren',
    'context_copy': 'Namen kopieren',

    # Export
    'export_title': 'Exportieren',
    'export_format': 'Format',
    'export_location': 'Speicherort',
    'export_success': 'Export erfolgreich!',
    'export_error': 'Fehler beim Export',

    # Einstellungen
    'settings_title': 'Einstellungen',
    'settings_language': 'Sprache',
    'settings_theme': 'Theme',
    'settings_icon_size': 'Icon-Größe',

    # Status
    'status_loading': 'Lade Pakete...',
    'status_filtering': 'Filtere System-Apps...',
    'status_ready': 'Bereit',
    'status_packages': '{} Pakete gefunden',

    # Fehler
    'error_load': 'Fehler beim Laden der Pakete',
    'error_export': 'Fehler beim Exportieren',
    'error_unknown': 'Unbekannter Fehler',

    # Über-Dialog
    'about_title': 'Über MyApps',
    'about_version': 'Version',
    'about_description': 'Tool zum Auflisten und Verwalten installierter Linux-Anwendungen',
    'about_license': 'Lizenz: GPLv3.0',
    'about_website': 'Website',
}
