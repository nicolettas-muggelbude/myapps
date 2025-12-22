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
├── debian/                      # DEB-Paket-Struktur
│   ├── DEBIAN/control           # Package-Metadaten
│   ├── DEBIAN/postinst          # Post-Install-Script
│   ├── usr/bin/myapps           # Launcher-Script
│   └── usr/share/...            # App-Dateien
├── tests/                       # Unit-Tests (pytest)
├── docs/                        # Zusätzliche Dokumentation
├── .github/
│   └── ISSUE_TEMPLATE/          # GitHub Issue Templates
│       ├── bug_report.yml
│       ├── feature_request.yml
│       ├── filter_suggestion.yml
│       └── config.yml
├── build-deb.sh                 # DEB-Build-Script
├── build-appimage.sh            # AppImage-Build-Script
├── pyproject.toml               # Python-Projekt-Config
├── requirements.txt             # Python-Dependencies
├── README.md                    # Haupt-Dokumentation (Deutsch)
├── README.en.md                 # Haupt-Dokumentation (Englisch)
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
- **Ziel-Distributionen**: Debian, Ubuntu, Mint
- **Build-Script**: `build-deb.sh`
- **Größe**: ~51 KB
- **Dependencies**: python3 (>= 3.8), python3-tk, python3-pip
- **Installation**: `sudo dpkg -i myapps_0.1.0_all.deb`
- **Struktur**:
  - Launcher-Script in `/usr/bin/myapps`
  - App-Dateien in `/usr/share/myapps/`
  - Desktop-Entry in `/usr/share/applications/`
  - Icon in `/usr/share/icons/hicolor/256x256/apps/`
- **Post-Install**: Installiert ttkbootstrap und Pillow via pip

### AppImage
- **Ziel-Distributionen**: Alle Linux-Distributionen
- **Build-Script**: `build-appimage.sh`
- **Größe**: ~7.8 MB
- **Dependencies**: python3, python3-tk (müssen auf dem System installiert sein)
- **Gebündelte Pakete**: ttkbootstrap, Pillow (im vendor/-Verzeichnis)
- **Ausführung**: `chmod +x MyApps-0.1.0-x86_64.AppImage && ./MyApps-0.1.0-x86_64.AppImage`
- **AppRun-Script**:
  - Prüft ob python3 und python3-tk vorhanden sind
  - Setzt PYTHONPATH auf vendor-Verzeichnis
  - Startet App mit `python3 -m src.myapps.main`
- **WSL-Kompatibilität**: Build-Script erkennt extrahiertes appimagetool für Systeme ohne FUSE

### Build-Scripts

#### build-deb.sh
```bash
./build-deb.sh              # Auto-Version aus pyproject.toml
./build-deb.sh 0.1.0        # Spezifische Version
```
- Farbige Ausgabe (Blau/Grün/Rot)
- 7 Schritte: Aufräumen, Debian-Struktur, Dateien kopieren, Icons, Control-Datei, postinst, Build
- Automatische Version-Erkennung aus pyproject.toml
- Ausgabe: `myapps_VERSION_all.deb`

#### build-appimage.sh
```bash
./build-appimage.sh         # Auto-Version aus pyproject.toml
./build-appimage.sh 0.1.0   # Spezifische Version
```
- Farbige Ausgabe (Blau/Grün/Rot)
- 7 Schritte: Aufräumen, AppDir-Struktur, Dateien kopieren, .desktop-Datei, Dependencies, AppRun, Build
- Automatische Version-Erkennung aus pyproject.toml
- Erkennt extrahiertes appimagetool für WSL/FUSE-lose Systeme
- Ausgabe: `MyApps-VERSION-x86_64.AppImage`

## Changelog

### v0.1.0 (Alpha - Ready for Release)
**Initiale Version**

**Core Features:**
- Multi-Distro-Support (Debian, Ubuntu, Mint, Arch, Fedora, Solus, openSUSE)
- Moderne GUI mit ttkbootstrap Dark Mode
- Zwei Ansichten: Tabelle und Liste (Messenger-Style)
- Export-Funktionen (TXT, CSV, JSON)
- Mehrsprachigkeit (Deutsch/Englisch via gettext)
- Intelligente Filterung (89% Filter-Rate: 1330 Pakete → 145 User-Apps)

**GUI-Verbesserungen:**
- Listenansicht mit modernem Messenger-Design
- Rekursives Scrolling-Binding für alle Widgets
- Lazy-Loading Tooltips mit Paketbeschreibungen
- Moderner Export-Dialog (500x500px, quadratisch)
- Verbessertes Fallback-Icon (blaues Paket-Symbol)
- Entfernung aller Emojis (Darstellungsprobleme)
- Standard-Ansicht: Liste

**Package Management:**
- DEB-Paket (51 KB) mit build-deb.sh
- AppImage (7.8 MB) mit build-appimage.sh
- Automatische Versions-Erkennung in Build-Scripts
- WSL-Kompatibilität (extrahiertes appimagetool)

**Entwicklung:**
- Vollständige Type Hints in allen Modulen
- Deutsche Code-Kommentare
- Logging statt print()
- GitHub Issue Templates (Bug, Feature, Filter)
- Umfassende README (DE + EN)
- CONTRIBUTING.md für Community-Beiträge

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
