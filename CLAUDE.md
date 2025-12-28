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

### v0.2.0 Features (GTK4 Migration) - ✅ RELEASED (26.12.2024)
- [x] GTK4 + Libadwaita GUI (~800 Zeilen)
- [x] Pagination (100 Apps/Seite, da Virtual Scrolling in v0.3.0 verschoben)
- [x] ListView mit SignalListItemFactory
- [x] ColumnView für Tabellenansicht
- [x] Export Dialog (File Chooser)
- [x] About Dialog mit Spendenlink
- [x] Threading mit GLib.idle_add
- [x] Searchbar (Live-Suche in Name + Beschreibung)
- [x] Flatpak Manifest (io.github.nicolettas-muggelbude.myapps.yml)
- [x] MetaInfo XML für Flathub
- [x] Desktop Entry für Flatpak
- [x] DEB-Paket mit GTK4-Dependencies (5.8 MB)
- [x] GitHub Release v0.2.0
- [x] Screenshots-Ordner erstellt (docs/screenshots/)
- [ ] Screenshots für Flathub (vom User zu erstellen)
- [ ] Community Testing (läuft)

### Spätere Versionen
- **v0.3.0**: Virtual Scrolling (10.000+ Pakete ohne Pagination), .desktop-only View (Issue #4), Größen-Information (Issue #5), Performance-Optimierungen (Issue #9 - Caching)
- **v0.4.0**: Update-Status prüfen, Installationsdatum
- **v1.0.0**: Stabile Version nach Community-Testing, Snap-Paket
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
- **Application ID**: `io.github.nicolettas-muggelbude.myapps` (GitHub-basiert, neutral)
  - **WICHTIG**: Nicht de.pc-wittfoot.myapps! PC-Wittfoot UG ist nur Spendenverwalter, kein Entwickler
- **Rolle**: Verwaltet Package-Loading, Filtering, Pagination, Suche
- **Threading**: GLib.idle_add für GUI-Updates aus Worker-Threads
- **Lifecycle**: `do_activate()` → erstellt Window → lädt Pakete async

#### MyAppsWindow (Adw.ApplicationWindow)
- **Header Bar**: Adw.HeaderBar mit Buttons (Refresh, Export, Menu)
  - **SearchEntry**: Zentral im Title-Bereich für Live-Suche (300px breit)
- **Stack**: View-Switching zwischen List und Table View
- **Pagination Bar**: Info-Label + Prev/Next Buttons
- **Status Bar**: Gtk.Statusbar für Nachrichten (zeigt Anzahl gefundener Apps bei Suche)

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

### DEB-Paket (v0.1.x - tkinter)
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

### DEB-Paket (v0.2.0+ - GTK4)
- **Ziel-Distributionen**: Debian, Ubuntu, Mint
- **Build-Script**: `build-deb.sh`
- **Größe**: ~5.8 MB (bundelt Pillow)
- **Dependencies**:
  - python3 (>= 3.8)
  - python3-gi, python3-gi-cairo
  - gir1.2-gtk-4.0, gir1.2-adw-1
  - python3-pil
- **Installation**: `sudo dpkg -i myapps_0.2.0_all.deb`
- **Struktur**:
  - Binary in `/usr/bin/myapps`
  - Python-Paket in `/usr/lib/python3/dist-packages/myapps/`
  - Desktop-Entry in `/usr/share/applications/`
  - MetaInfo in `/usr/share/metainfo/`
  - Icon in `/usr/share/icons/hicolor/scalable/apps/`
  - Filters in `/usr/share/myapps/filters/`
  - Locales in `/usr/share/myapps/locales/`

### openSUSE Build Service (OBS) - v0.2.0+
**URL:** https://build.opensuse.org
**Projekt:** home:nicoletta:myapps
**Package:** myapps

**Zweck:**
- Multi-Distro Builds aus einer Konfiguration
- Native Pakete (DEB für Debian/Ubuntu, RPM für Fedora/openSUSE)
- Kein Sandbox (voller /var/lib Zugriff für Paketmanager-DBs)
- Alternative zu Flathub (nach Ablehnung)

**Unterstützte Distributionen (11):**
- **Debian:** 12 (Bookworm), 13 (Trixie)
- **Ubuntu:** 22.04 LTS, 24.04 LTS, 25.10
- **Fedora:** 41, 42, 43
- **openSUSE:** Leap 16, Slowroll, Tumbleweed

**Dateien in OBS:**
- `myapps-0.2.0.tar.gz` - Git-Archive des Source Codes (5.7 MB)
- `myapps.spec` - RPM Build Specification

**RPM .spec Highlights:**
```spec
Name:           myapps
Version:        0.2.0
Release:        1%{?dist}
BuildArch:      noarch

# Runtime Dependencies
Requires:       python3 >= 3.8
Requires:       python3-gobject
Requires:       gtk4
Requires:       libadwaita
Requires:       python3-pillow

# Build Steps
%build
%py3_build

%install
%py3_install
# + Install desktop file, metainfo, icon, filters, locales, assets
```

**User Installation (nach Build-Erfolg):**

*Debian/Ubuntu:*
```bash
# Repo hinzufügen (einmalig)
echo "deb https://download.opensuse.org/repositories/home:/nicoletta:/myapps/Debian_12/ /" | sudo tee /etc/apt/sources.list.d/myapps.list
wget -qO- https://download.opensuse.org/repositories/home:/nicoletta:/myapps/Debian_12/Release.key | sudo gpg --dearmor -o /etc/apt/trusted.gpg.d/myapps.gpg
sudo apt update

# Installieren
sudo apt install myapps
```

*Fedora:*
```bash
# Repo hinzufügen (einmalig)
sudo dnf config-manager --add-repo https://download.opensuse.org/repositories/home:/nicoletta:/myapps/Fedora_41/home:nicoletta:myapps.repo

# Installieren
sudo dnf install myapps
```

*openSUSE:*
```bash
# Repo hinzufügen (einmalig)
sudo zypper addrepo https://download.opensuse.org/repositories/home:/nicoletta:/myapps/openSUSE_Tumbleweed/home:nicoletta:myapps.repo

# Installieren
sudo zypper install myapps
```

**Build-Workflow:**
1. Source Tarball erstellen: `git archive --format=tar.gz --prefix=myapps-0.2.0/ -o myapps-0.2.0.tar.gz HEAD`
2. .spec Datei schreiben (defines build steps)
3. In OBS hochladen (Web UI oder `osc` CLI)
4. Repositories auswählen (welche Distros)
5. Builds triggern (automatisch nach Upload)
6. Warten auf Build-Ergebnisse (5-15 Min pro Distro)
7. Repository-URLs in README eintragen

**Vorteile gegenüber Flathub:**
- ✅ Kein Sandbox (voller System-Zugriff)
- ✅ Native Integration (systemd, distro package manager)
- ✅ Kleinere Download-Größe (shared dependencies)
- ✅ Vertrauter Workflow für Linux-User (apt/dnf/zypper)

**Nachteile:**
- ❌ Kein App Store UI (Terminal-Installation)
- ❌ Nutzer müssen Repo manuell hinzufügen
- ❌ Keine automatische Sandbox-Sicherheit

### Flatpak (Flathub - ABGELEHNT)
**Status:** ❌ Nicht verfügbar auf Flathub

**Grund der Ablehnung:**
- MyApps benötigt `/var/lib/*` Zugriff für Paketmanager-Datenbanken
- Flathub erlaubt dies aus Sicherheitsgründen nicht
- Antwort: "then this application is not suitable for flathub"

**Technische Details:**
- **App-ID:** `io.github.nicolettas-muggelbude.myapps`
- **Runtime:** org.gnome.Platform 46
- **Manifest:** `io.github.nicolettas-muggelbude.myapps.yml`
- **Build-Fehler:**
  - `finish-args-host-var-access` - /var/lib Zugriff verboten
  - `finish-args-flatpak-system-folder-access` - System-Ordner verboten
  - `runtime-is-eol-org.gnome.Platform-47` - Runtime EOL

**Alternative:** openSUSE Build Service (siehe oben)

**Flatpak bleibt im Repo (für Self-Hosting):**
- User können Flatpak selbst bauen: `flatpak-builder --force-clean build-dir io.github.nicolettas-muggelbude.myapps.yml`
- Lokale Installation möglich: `flatpak-builder --install ...`
- Nur nicht auf Flathub verfügbar

### AppImage (discontinued ab v0.2.0)
- **Grund:** GTK4 + Libadwaita schwer in AppImage zu bundeln
- **Problem:** System-Dependencies (GTK4, Libadwaita) müssen auf Host vorhanden sein
- **Alternative:** DEB-Paket oder OBS-Pakete verwenden
- **v0.1.x AppImage:** Noch verfügbar für Legacy tkinter Version

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

### v0.2.0 (Major Update - GTK4 Migration) - ✅ RELEASED
**Veröffentlicht:** 26. Dezember 2024
**GitHub Release:** https://github.com/nicolettas-muggelbude/myapps/releases/tag/v0.2.0

**🎯 Haupt-Features:**
- **GTK4 + Libadwaita GUI** (~800 Zeilen, kompletter Rewrite)
  - Moderne GNOME-Integration mit nativem Dark Mode
  - ListView mit SignalListItemFactory (Setup/Bind-Pattern)
  - ColumnView für Tabellenansicht
- **Searchbar** (Issue #2 - IMPLEMENTIERT)
  - Live-Suche in App-Name und Beschreibung
  - Case-insensitive, funktioniert mit Pagination
  - Export respektiert Suchergebnisse
- **Pagination** (100 Apps/Seite)
  - UX-Feature für bessere Übersichtlichkeit
  - Virtual Scrolling verschoben auf v0.3.0
- **Threading** mit GLib.idle_add für GUI-Updates
- **Export Dialog** mit Gtk.FileChooserDialog (TXT, CSV, JSON)
- **About Dialog** mit Spendenlink (Adw.AboutWindow)
- **Deutsche Beschreibungen** in Listenansicht (via apt-cache)
- **Englische Beschreibungen** in Tabellenansicht (schneller)

**📦 Packaging:**
- **DEB-Paket** (5.8 MB) mit GTK4-Dependencies
  - Dependencies: python3-gi, gir1.2-gtk-4.0, gir1.2-adw-1, python3-pil
  - Bundelt nur noch Pillow, keine GUI-Frameworks
- **Flatpak-Manifest** (YAML) für GNOME Platform 46
  - App-ID: `io.github.nicolettas-muggelbude.myapps` (GitHub-basiert, neutral)
  - MetaInfo XML für Flathub vorbereitet
  - Desktop Entry inkludiert
- **AppImage discontinued** (GTK4-Dependencies schwer zu bundeln)

**📚 Dokumentation:**
- `README.md` komplett überarbeitet (GTK4 Installation)
- `CONTRIBUTING.md` erweitert (GTK4 System-Dependencies)
- `CLAUDE.md` aktualisiert (v0.2.0 Release-Stand)
- Donation Button in README + About Dialog
- Screenshots-Ordner erstellt (`docs/screenshots/`)

**🐛 Bugfixes:**
- Kein X-Server BadAlloc mehr durch GTK4
- Tooltips funktionieren jetzt korrekt
- Export-Dialog deutlich verbessert

**🗂️ GitHub Issues:**
- Issue #2 (Searchbar) → ✅ Implementiert
- Issue #4 (.desktop-only View) → Verschoben auf v0.3.0
- Issue #5 (Größen-Information) → Verschoben auf v0.3.0
- Issue #9 (Performance-Optimierungen) → Verschoben auf v0.3.0

**⚠️ Bekannte Einschränkungen:**
- Icon-Anzeige nicht implementiert (Icons werden geladen, aber nicht angezeigt)
- Kein CSS-Styling (nutzt Standard-Libadwaita-Theme)
- Virtual Scrolling noch nicht implementiert (Pagination als Workaround)
- Community Testing läuft noch

**🔧 Breaking Changes:**
- Alte tkinter-GUI in `gui_legacy.py` verschoben (nicht mehr gewartet)
- `main.py` importiert jetzt `gui_gtk.py` statt `gui.py`
- System-Dependencies geändert: `python3-tk` → `python3-gi + GTK4`
- App-ID geändert: `de.pc-wittfoot.myapps` → `io.github.nicolettas-muggelbude.myapps`

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

### Versionsverwaltung:
**WICHTIG**: Version wird automatisch aus pyproject.toml gelesen!

#### Versionsänderung durchführen:
1. **NUR** `pyproject.toml` ändern:
   ```toml
   version = "X.Y.Z"
   ```
2. **NICHT** manuell ändern:
   - ❌ `src/myapps/gui_gtk.py` (VERSION wird automatisch gelesen)
   - ❌ About-Dialog (verwendet VERSION Konstante)
   - ❌ Irgendwo anders im Code

#### Wie es funktioniert:
- `get_version_from_pyproject()` in `gui_gtk.py`
- Liest `pyproject.toml` beim App-Start
- Setzt `VERSION` Konstante automatisch
- Fallback: `"0.0.0"` bei Fehler
- About-Dialog zeigt: `f"Version {VERSION}"`

#### Vorteile:
- ✅ Single Source of Truth (pyproject.toml)
- ✅ Keine vergessenen Version-Updates
- ✅ Konsistenz garantiert

### Changelog-Verwaltung (WHATS_NEW.md):
**WICHTIG**: Changelog wird automatisch aus WHATS_NEW.md geladen!

#### Neue Version hinzufügen:
1. **WHATS_NEW.md** bearbeiten:
   ```markdown
   ## vX.Y.Z
   - Feature 1 Beschreibung
   - Feature 2 Beschreibung
   - Fix: Bugfix Beschreibung
   ```
2. Version-Header MUSS Format `## vX.Y.Z` haben (exakt!)
3. Features MÜSSEN mit `- ` beginnen (Bullet-Point)
4. Reihenfolge: Neueste Version OBEN

#### Wie es funktioniert:
- `get_whats_new(version)` in `gui_gtk.py`
- Liest `WHATS_NEW.md` beim Öffnen des About-Dialogs
- Findet Version-Sektion via `## vX.Y.Z` Header
- Extrahiert alle Zeilen mit `- ` Präfix
- Zeigt Features im About-Dialog dynamisch an
- Fallback: "Keine Changelog-Informationen verfügbar"

#### Release-Workflow:
1. `pyproject.toml` Version ändern → `version = "X.Y.Z"`
2. `WHATS_NEW.md` neue Sektion oben hinzufügen → `## vX.Y.Z`
3. Packaging-Dateien aktualisieren (spec, changelog, dsc, PKGBUILD)
4. Git Tag erstellen → `git tag -a vX.Y.Z -m "..."`
5. GitHub Release erstellen mit Release Notes
6. **Fertig!** About-Dialog zeigt automatisch korrekte Version + Features

#### Vorteile:
- ✅ Single Source of Truth für Changelog (WHATS_NEW.md)
- ✅ Keine hartcodierten Features im Code
- ✅ Konsistenz zwischen Releases und About-Dialog
- ✅ Einfach erweiterbar für neue Versionen

### Release Notes Format:
**WICHTIG**: Alle Releases MÜSSEN diesem Format folgen für Konsistenz!

#### Download-Buttons (IMMER einbinden):
**WICHTIG:** HTML verwenden (nicht Markdown), da GitHub Markdown-Syntax escaped!

```html
## 📦 Installation

### **OBS-Pakete** - Empfohlen ✅

<a href="https://software.opensuse.org//download.html?project=home%3Anicoletta%3Amyapps&package=myapps"><img src="https://img.shields.io/badge/Download-OBS_Pakete-73BA25?style=for-the-badge&logo=opensuse&logoColor=white" alt="OBS Download"></a>

**Installationsanleitung hier...**

---

### **AUR-Paket** - Arch Linux ✅

<a href="https://aur.archlinux.org/packages/myapps"><img src="https://img.shields.io/badge/Download-AUR-1793D1?style=for-the-badge&logo=archlinux&logoColor=white" alt="AUR Download"></a>

**Installationsanleitung hier...**

---
```

#### Spendenbutton (IMMER am Ende):
**WICHTIG:** HTML verwenden (nicht Markdown), da GitHub Markdown-Syntax escaped!

```html
## 💝 MyApps unterstützen

Dieses Projekt ist **Open Source** (GPLv3) und wird von der Community entwickelt!

<a href="https://www.paypal.com/ncp/payment/UYJ73YNEZ3KHL"><img src="https://img.shields.io/badge/PayPal-Spenden-00457C?style=for-the-badge&logo=paypal&logoColor=white" alt="Spenden via PayPal"></a>

**Spenden gehen an:** PC-Wittfoot UG (Spendenverwalter)
**Verwendung:** Serverkosten, Hardware, Entwicklerzeit für MyApps

**Hinweis:** Die Entwicklung erfolgt durch die Linux Guides DE Community (Open Source).
PC-Wittfoot UG verwaltet nur die Spenden, ist aber NICHT der Entwickler.

**Rechtliches:**
[Impressum](https://nicolettas-muggelbude.github.io/myapps/impressum) | [Datenschutz](https://nicolettas-muggelbude.github.io/myapps/datenschutz)

---

**Changelog:** https://github.com/nicolettas-muggelbude/myapps/compare/vX.X.X...vY.Y.Y
```

#### Vollständige Struktur:
1. **Titel** mit Emoji (z.B. "# MyApps v0.2.1 - Bugfix Release")
2. **Kurzbeschreibung** in Bold
3. **Separator** (`---`)
4. **Änderungen/Features** (mit Emojis und Checkmarks)
5. **Separator** (`---`)
6. **📦 Installation** (OBS + AUR Buttons)
7. **Separator** (`---`)
8. **🙏 Danke** (optional, bei Community-Beiträgen)
9. **Separator** (`---`)
10. **💝 Spendenbutton** mit Rechtlichem
11. **Changelog-Link** am Ende

## Aktueller Projekt-Stand (27.12.2024)

### ✅ Abgeschlossen

- **v0.2.2 Release** (27.12.2024) - AKTUELL
  - **Kritischer Bugfix:** NameError auf OBS-Paketen behoben
  - **Problem:** ImageTk Type Hints wurden zur Parse-Zeit aufgelöst
  - **Lösung:** Type Hints als String-Literale geschrieben
  - **Betroffene Systeme:** Alle 11 OBS-Distributionen
  - **GitHub Release:** https://github.com/nicolettas-muggelbude/myapps/releases/tag/v0.2.2
  - **AUR aktualisiert:** https://aur.archlinux.org/packages/myapps
  - **OBS-Upload pending:** myapps-0.2.2.tar.gz, myapps.spec, debian.tar.gz, myapps.dsc
  - **Automation:** Version und Changelog werden automatisch aus pyproject.toml und WHATS_NEW.md geladen

- **v0.2.1 Release** (27.12.2024)
  - **Basis-Verzeichnis-Fix:** /usr/share/myapps wird korrekt erkannt
  - **GTK4 SearchEntry Fix:** placeholder_text als Parameter statt Methode
  - **AUR PKGBUILD Fix:** Fallback für alte Dateinamen
  - **Automatisierung:** Version und Changelog aus Dateien gelesen

- **v0.2.0 Release** vollständig
  - DEB-Paket gebaut und zu GitHub Release hinzugefügt
  - Flatpak-Manifest, Desktop Entry und MetaInfo XML erstellt
  - Searchbar implementiert (Issue #2)
  - Screenshots erstellt (4 Stück: main-window, table-view, search-demo, dark-mode)

- **OBS (openSUSE Build Service)** ✅ KOMPLETT
  - Account: https://build.opensuse.org
  - Projekt: home:nicoletta:myapps
  - **11 Distributionen erfolgreich gebaut:**
    - Fedora 41, 42, 43
    - openSUSE Leap 16, Slowroll, Tumbleweed
    - Debian 12 (Bookworm), 13 (Trixie)
    - Ubuntu 22.04 LTS, 24.04 LTS, 25.10
  - **Download-Portal:** https://software.opensuse.org//download.html?project=home%3Anicoletta%3Amyapps&package=myapps
  - **Behobene Probleme:**
    - Menu-Integration mit %post/%postun Scripts (RPM) und postinst/postrm (DEB)
    - Icon-Deinstallation explizit in postrm implementiert
    - Locales-Fehler behoben (aus myapps.install entfernt)
    - Icon-Verzeichnisse mit hicolor-icon-theme dependency + %dir Direktiven

- **AUR (Arch User Repository)** ✅ KOMPLETT
  - **Live:** https://aur.archlinux.org/packages/myapps
  - PKGBUILD + .SRCINFO hochgeladen
  - **Tarball-Dateinamen-Problem behoben (27.12.2024):**
    - v0.2.0 GitHub-Tarball enthält alte Dateinamen (de.pc-wittfoot.myapps.*)
    - PKGBUILD nutzt if/else Fallback für Kompatibilität
    - Installiert korrekt als io.github.nicolettas-muggelbude.myapps.*
  - Erfolgreich getestet mit makepkg -si (yay -S myapps)

- **Flathub Submission** ❌ ABGELEHNT
  - Pull Request: https://github.com/flathub/flathub/pull/7404
  - Grund: /var/lib Zugriff wird generell nicht gewährt (Sicherheitspolitik)
  - Alternative: OBS-Pakete (native System-Integration)
  - PR sauber geschlossen am 26.12.2024

- **Packaging-Strategie festgelegt:**
  - **Production (Empfohlen):** OBS (11 Distros) + AUR (Arch)
  - **Testing Only:** GitHub DEB (bundelt Pillow, nicht für Production)
  - **Nicht verfügbar:** Flatpak (Flathub abgelehnt)

- **Dokumentation vollständig überarbeitet:**
  - README.md + README.en.md: OBS + AUR als primäre Installationsmethoden
  - build-deb.sh: Warnhinweise für Testing-Only-Status hinzugefügt
  - GitHub Release Notes v0.2.0 aktualisiert
  - OBS-Links auf benutzerfreundliches Download-Portal geändert (software.opensuse.org)

- **Bug-Reports bearbeitet:**
  - Issue #13, #14 (Pillow-Import-Fehler) → auf OBS-Pakete verwiesen
  - Menu-Integration-Problem (Mint) → behoben in build-deb.sh + OBS debian/
  - Icon-Deinstallation (Debian) → behoben mit explizitem rm -f in postrm
  - AUR Installation-Fehler (CachyOS) → PKGBUILD Fallback für alte Dateinamen (27.12.2024)

### 🔄 Aktuell laufend
- **Community Testing** (v0.2.3):
  - Testing auf verschiedenen Systemen
  - Feedback sammeln via GitHub Issues
  - Bug-Reports bearbeiten
  - **Performance-Feedback:** User mit Mint (~400 Apps) berichten von langsamen Seitenwechseln

### 📋 Roadmap

#### **v0.2.4 - Performance-Release** (NÄCHSTE VERSION)
**Issue #17** - Performance-Optimierungen (kritisch!)

**Problem:** User mit Mint (~2000 Pakete, ~400 gefilterte Apps) berichten:
- Seitenwechsel spürbar langsam
- App-Start dauert zu lange

**Geplante Fixes:**
1. **Icon-Caching** (größter Impact)
   - Icons nur einmal laden, dann cachen
   - ~80% schnellerer Seitenwechsel
2. **Sortierung optimieren**
   - Nur einmal nach Filterung sortieren
   - 5-10x schnellerer Seitenwechsel
3. **Event Handler Cleanup**
   - Context Menu in `setup` statt `bind`
   - Memory Leak beheben

**Aufwand:** 2-3h Implementierung + 1h Testing
**Priorität:** KRITISCH - muss vor v0.3.0 (Scope-Dropdown)

---

#### **v0.3.0 - Such-Scope & Features**
**Issue #16** - Scope-Dropdown für Suche

**Features:**
1. **Scope-Dropdown vor Suchfeld**
   - "Nur User-Apps" (Standard) → ~800 Apps
   - "Alle Pakete" → ~2000+ Pakete
   - Nur aktiv bei Liste/Tabelle View
2. **Mindestens 5 Zeichen für Suche**
   - Schränkt Ergebnisse deutlich ein
3. **Pagination im Suchmodus**
   - Funktioniert bereits ✅
4. **Tooltips im Suchmodus**
   - Funktioniert bereits ✅

**Voraussetzung:** v0.2.4 Performance-Fixes fertig!

---

#### **v0.3.1 - Desktop Apps View**
**Issue #4** - .desktop-only View

**Features:**
1. **Neue Ansicht:** Desktop Apps (neben Liste & Tabelle)
2. **Desktop-App-Erkennung (Option B):**
   - Parse `/usr/share/applications/`
   - Parse `~/.local/share/applications/`
   - Flatpak/Snap-spezifische Pfade
3. **Scope-Integration:**
   - Bei Desktop Apps View: Scope deaktiviert
   - Suche beschränkt sich automatisch auf Desktop Apps

---

#### **v0.4.0 - Weitere Features**
- **Issue #5:** Größen-Information für Pakete
- Virtual Scrolling (echtes ListView-Scrolling, weg von Pagination)
- Icon-Anzeige in ListView/ColumnView (aktuell nur Platzhalter)

#### **v1.0.0 - Stable Release**
- Nach umfangreichem Community-Testing
- Alle kritischen Bugs behoben
- Performance optimiert

#### **v2.0.0 - Major Features**
- Deinstallations-Funktion
- Update-Benachrichtigungen
