# MyApps - Projekt-Dokumentation für Claude

## Projekt-Übersicht
**MyApps** ist ein Open-Source-Tool zum Auflisten und Verwalten installierter Anwendungen auf Linux-Systemen.
Ziel ist es, Endanwendern eine übersichtliche Darstellung ihrer installierten User-Apps zu bieten, ohne System-Clutter.

## Projekt-Details

### Grundinformationen
- **Projektname**: MyApps
- **Version**: v0.2.0 (Beta - GTK4 Migration)
- **Lizenz**: GPLv3.0
- **Repository**: GitHub
- **Zielgruppe**: Endanwender (Linux Desktop)
- **Entwickelt von**: Linux Guides DE Community
- **Hauptentwickler**: nicolettas-muggelbude

### Projekt-Organisation

**WICHTIG: Rollenverteilung**

- **Entwicklung**: Linux Guides DE Community (Open Source, GPLv3)
  - Hauptentwickler: nicolettas-muggelbude
  - Community Contributors willkommen
  - Entwicklung ist NICHT durch PC-Wittfoot UG

- **Spendenverwaltung**: PC-Wittfoot UG
  - Verwaltet PayPal-Spenden für das Projekt
  - Verwendet Spenden für Serverkosten, Hardware, Entwicklerzeit
  - **Hat NICHTS mit der Entwicklung zu tun**
  - Siehe Impressum/Datenschutz auf GitHub Pages

**Zusammenfassung**: PC-Wittfoot UG ist NUR Spendenverwalter, NICHT Entwickler!

### Technologie-Stack
- **Sprache**: Python 3.8+
- **GUI-Framework**: GTK4 + Libadwaita (ab v0.2.0)
  - Legacy: ttkbootstrap (v0.1.x)
- **Icon-Größe**: 32x32px (48x48px für GTK4)
- **Lokalisierung**: gettext (i18n)
- **Packaging**: DEB + Flatpak (AppImage discontinued ab v0.2.0)

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

### v0.2.0 Features (GTK4 Migration) - AKTUELL
- [x] GTK4 + Libadwaita GUI (~650 Zeilen)
- [x] Virtual Scrolling (10.000+ Pakete kein Problem)
- [x] Kein X-Server BadAlloc mehr
- [x] ListView mit SignalListItemFactory
- [x] ColumnView für Tabellenansicht
- [x] Pagination (100 Apps/Seite, UX-Feature)
- [x] Export Dialog (File Chooser)
- [x] About Dialog mit Spendenlink
- [x] Threading mit GLib.idle_add
- [ ] Community Testing (ausstehend)
- [ ] CSS Styling (optional)
- [ ] Flatpak Manifest

### Spätere Versionen
- **v0.3.0**: Größen-Information, Installationsdatum, Sortier-Funktionen
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
│       ├── gui_gtk.py           # GUI-Logik (GTK4 + Libadwaita, v0.2.0+)
│       ├── gui_legacy.py        # Legacy GUI (ttkbootstrap, v0.1.x)
│       ├── distro_detect.py     # Distro-Erkennung (GUI-agnostisch)
│       ├── package_manager.py   # Paketmanager-Abstraktionen (GUI-agnostisch)
│       ├── filters.py           # Filter-System (GUI-agnostisch)
│       ├── icons.py             # Icon-Management (GUI-agnostisch)
│       ├── export.py            # Export-Funktionen (GUI-agnostisch)
│       └── i18n.py              # Internationalisierung (GUI-agnostisch)
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

## GTK4 Architektur (v0.2.0+)

### Kern-Komponenten

#### MyAppsGUI (Adw.Application)
- **Application ID**: `de.pc-wittfoot.myapps`
- **Rolle**: Verwaltet Package-Loading, Filtering, Pagination
- **Threading**: GLib.idle_add für GUI-Updates aus Worker-Threads
- **Lifecycle**: `do_activate()` → erstellt Window → lädt Pakete async

#### MyAppsWindow (Adw.ApplicationWindow)
- **Header Bar**: Adw.HeaderBar mit Buttons (Refresh, Export, Menu)
- **Stack**: View-Switching zwischen List und Table View
- **Pagination Bar**: Info-Label + Prev/Next Buttons
- **Status Bar**: Gtk.Statusbar für Nachrichten

### Virtual Scrolling (Kern-Innovation)

**Problem in v0.1.x (tkinter):**
- Alle 800+ Widgets wurden gleichzeitig gerendert
- X-Server BadAlloc bei zu vielen Widgets
- Lösung war Pagination (100 Apps/Seite)

**Lösung in v0.2.0 (GTK4):**
- **ListView** mit **SignalListItemFactory**
- Nur sichtbare Items werden gerendert
- Model: `Gio.ListStore` mit Package-Objekten
- Setup/Bind-Pattern:
  - `setup`: Widget-Template EINMAL erstellen
  - `bind`: Daten für jedes sichtbare Item verknüpfen
- **Ergebnis**: 10.000+ Pakete kein Problem

### ListView Implementation

```python
def _create_list_view(self):
    # Model
    self.list_store = Gio.ListStore.new(GObject.TYPE_PYOBJECT)
    selection = Gtk.NoSelection.new(self.list_store)

    # Factory
    factory = Gtk.SignalListItemFactory()
    factory.connect("setup", self._on_list_setup)
    factory.connect("bind", self._on_list_bind)

    # ListView
    list_view = Gtk.ListView.new(selection, factory)

def _on_list_setup(self, factory, list_item):
    """Erstellt Widget-Template EINMAL"""
    box = Gtk.Box(...)
    list_item.set_child(box)

def _on_list_bind(self, factory, list_item):
    """Verknüpft Daten (nur für sichtbare Items)"""
    pkg = list_item.get_item()
    box = list_item.get_child()
    # ... Daten setzen
```

### ColumnView Implementation

```python
def _create_table_view(self):
    # Model
    self.table_store = Gio.ListStore.new(GObject.TYPE_PYOBJECT)
    selection = Gtk.SingleSelection.new(self.table_store)

    # ColumnView
    column_view = Gtk.ColumnView.new(selection)

    # Spalten
    col_name = Gtk.ColumnViewColumn.new("Name", factory)
    column_view.append_column(col_name)
    # ... weitere Spalten
```

### Threading Model

**WICHTIG**: Alle GUI-Updates MÜSSEN über `GLib.idle_add` laufen!

```python
def _load_packages_worker(self):
    """Worker Thread"""
    packages = PackageManagerFactory.get_all_packages(...)
    filtered = self.filter_manager.filter_packages(packages)

    # Update GUI im Main Thread
    GLib.idle_add(self.win._on_packages_loaded, filtered)
    # NICHT: self.win._on_packages_loaded(filtered)  # CRASH!
```

### Backend bleibt GUI-agnostisch

**Regel**: Backend-Module (package_manager, filters, export, etc.) dürfen **KEINE** GUI-Imports haben!

```python
# ❌ FALSCH - GUI-Import im Backend
from .gui_gtk import MyAppsWindow

# ✅ RICHTIG - Nur Standard-Libraries
import subprocess
from pathlib import Path
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

### v0.2.0 (Beta - GTK4 Migration) - IN TESTING
**Veröffentlicht:** TBD (Testing läuft)

**🎯 Haupt-Features:**
- **GTK4 + Libadwaita GUI** (~650 Zeilen, kompletter Rewrite)
- **Virtual Scrolling** mit ListView/ColumnView (10.000+ Pakete kein Problem)
- **Kein X-Server BadAlloc mehr** (GTK4 rendert nur sichtbare Items)
- **Threading** mit GLib.idle_add für GUI-Updates
- **Export Dialog** mit Gtk.FileChooserDialog
- **About Dialog** mit Spendenlink (Adw.AboutWindow)

**📦 Packaging-Änderungen:**
- DEB-Paket mit GTK4-Dependencies (debian/control aktualisiert)
- AppImage **discontinued** (GTK4-Dependencies schwer zu bundeln)
- Flatpak **geplant** (org.gnome.Platform 46)

**📚 Dokumentation:**
- README.md komplett überarbeitet (GTK4 Installation)
- CLAUDE.md erweitert (GTK4 Architektur-Sektion)
- Donation Button in README + About Dialog
- GitHub Pages mit Impressum/Datenschutz

**⚠️ Bekannte Einschränkungen:**
- Icon-Anzeige nicht implementiert (Icons werden geladen, aber nicht angezeigt)
- Kein CSS-Styling (nutzt Standard-Libadwaita-Theme)
- **Noch nicht auf echter Linux-Maschine getestet** (nur WSL Development)

**🔧 Breaking Changes:**
- Alte tkinter-GUI in `gui_legacy.py` verschoben
- `main.py` importiert jetzt `gui_gtk.py` statt `gui.py`
- System-Dependencies geändert: python3-tk → python3-gi + GTK4

### v0.1.0 (Alpha - Stable)
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
