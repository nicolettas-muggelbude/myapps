# MyApps - Projekt-Dokumentation für Claude

## Projekt-Übersicht
**MyApps** ist ein Open-Source-Tool zum Auflisten und Verwalten installierter Anwendungen auf Linux-Systemen.
Ziel ist es, Endanwendern eine übersichtliche Darstellung ihrer installierten User-Apps zu bieten, ohne System-Clutter.

## Projekt-Details

### Grundinformationen
- **Projektname**: MyApps
- **Version**: v0.1.0 (Alpha)
- **Lizenz**: GPLv3.0
- **Repository**: GitHub
- **Zielgruppe**: Endanwender (Linux Desktop)

### Technologie-Stack
- **Sprache**: Python 3.8+
- **GUI-Framework**: ttkbootstrap (Dark Mode)
- **Icon-Größe**: 32x32px
- **Lokalisierung**: gettext (i18n)
- **Packaging**: DEB + AppImage

### Unterstützte Distributionen
- Debian, Ubuntu, Linux Mint
- Arch Linux
- Fedora
- Solus
- openSUSE
- + Snap und Flatpak (distributionsübergreifend)

### Paketmanager
- **dpkg**: Debian/Ubuntu/Mint
- **pacman**: Arch Linux
- **rpm/dnf**: Fedora
- **eopkg**: Solus
- **rpm/zypper**: openSUSE
- **snap**: Snap-Pakete
- **flatpak**: Flatpak-Apps

## Features v0.1.0

### Must-Have Features
- [x] Multi-Distro-Support (automatische Erkennung via /etc/os-release)
- [x] Moderne GUI mit ttkbootstrap (Dark Mode)
- [x] App-Icons (32x32px, System-Icons + generischer Fallback)
- [x] Zwei Ansichten: Tabelle (Dateimanager-Style) + Liste (Icon + Name)
- [x] Umschalt-Button zwischen Ansichten
- [x] Distro-spezifische Filter (JSON-basiert, erweiterbar)
- [x] User-Filter (Rechtsklick → "Als System-App markieren")
- [x] Export-Funktionen (txt, csv, json)
- [x] Mehrsprachigkeit (Deutsch + Englisch)

### Spätere Versionen
- **v0.2.0**: Größen-Information (optional einblendbar)
- **v0.3.0**: Installationsdatum anzeigen
- **v0.4.0**: Update-Status prüfen
- **v1.0.0**: Stabile Version nach Community-Testing
- **v2.0.0**: Deinstallations-Funktion

## Projekt-Struktur

```
app_lister/
├── src/
│   └── myapps/
│       ├── __init__.py
│       ├── main.py              # Haupteinstiegspunkt
│       ├── gui.py               # GUI-Logik (ttkbootstrap)
│       ├── distro_detect.py     # Distro-Erkennung
│       ├── package_manager.py   # Paketmanager-Abstraktionen
│       ├── filters.py           # Filter-System
│       ├── icons.py             # Icon-Management
│       ├── export.py            # Export-Funktionen
│       └── i18n.py              # Internationalisierung
├── filters/
│   ├── common.json              # Universelle System-Apps
│   ├── debian.json              # Debian/Ubuntu/Mint
│   ├── arch.json                # Arch Linux
│   ├── fedora.json              # Fedora
│   ├── solus.json               # Solus
│   └── opensuse.json            # openSUSE
├── locales/
│   ├── de/LC_MESSAGES/          # Deutsche Übersetzungen
│   └── en/LC_MESSAGES/          # Englische Übersetzungen
├── assets/
│   └── icons/                   # Fallback-Icons
├── tests/                       # Unit-Tests (pytest)
├── docs/                        # Zusätzliche Dokumentation
├── pyproject.toml               # Python-Projekt-Config
├── requirements.txt             # Python-Dependencies
├── README.md                    # Haupt-Dokumentation (DE + EN)
├── LICENSE                      # GPLv3.0
├── CONTRIBUTING.md              # Contribution Guidelines
├── .gitignore                   # Git-Ignore-Regeln
└── CLAUDE.md                    # Diese Datei
```

## Development Guidelines

### Code-Stil
- **Sprache**: Code-Kommentare auf Deutsch
- **Commit-Messages**: Auf Deutsch
- **Type Hints**: Verwenden für alle Funktionen
- **Docstrings**: Deutsch, ausführlich
- **Logging**: Python logging-Modul (nicht print())

### Community-Integration
- **Testing**: Community-basiert (verschiedene Distros)
- **Filter-Vorschläge**: Via GitHub Issues (Template)
- **Contributions**: Pull Requests willkommen
- **Issue-Tracker**: GitHub Issues

### Filter-System
- Distro-spezifische JSON-Dateien
- User kann eigene Filter in `~/.config/myapps/user-filters.json` hinzufügen
- GUI: Rechtsklick auf App → "Als System-App markieren"

### Icon-System
- System-Icons aus `/usr/share/icons/` und `/usr/share/pixmaps/`
- Snap-Icons: `~/.local/share/icons/` oder snap-spezifische Pfade
- Flatpak-Icons: `/var/lib/flatpak/exports/share/icons/`
- Fallback: Generisches Icon aus `assets/icons/`

## Packaging

### DEB-Paket
- Für Debian, Ubuntu, Mint
- Erstellt ab v0.1.0
- Dependencies: python3, python3-tk, ttkbootstrap

### AppImage
- Distributionsübergreifend
- Erstellt ab v0.1.0
- Alle Dependencies gebündelt

## Changelog

### v0.1.0 (in Entwicklung)
- Initiale Version
- Multi-Distro-Support
- Moderne GUI mit ttkbootstrap
- Export-Funktionen
- Mehrsprachigkeit (DE/EN)

## Notizen für Claude

### Bei jeder Code-Änderung:
1. Type Hints verwenden
2. Deutsche Kommentare schreiben
3. Logging statt print() verwenden
4. Fehlerbehandlung implementieren
5. Tests erwägen (für kritische Funktionen)

### Bei neuen Features:
1. Diese CLAUDE.md aktualisieren
2. README.md aktualisieren
3. Changelog erweitern
4. Tests hinzufügen (wenn möglich)

### User-Präferenzen:
- Keine explizite Nachfrage bei neuen Script-Versionen
- Alle Terminal-Ausgaben auf Deutsch
- Diese CLAUDE.md kontinuierlich fortführen
