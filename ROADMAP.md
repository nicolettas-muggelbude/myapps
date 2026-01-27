# MyApps - Roadmap

Dieser Plan zeigt die geplante Entwicklung von MyApps.

---

## 📍 Aktueller Stand

**Aktuelle Version:** v0.2.4
**Status:** Performance-Release - Testing läuft
**Verfügbar:** OBS (11 Distributionen), AUR (Arch Linux)

---

## 🚀 Geplante Releases

### v0.2.4 - Performance-Release ⚡

**Priorität:** 🔴 KRITISCH
**Status:** ✅ Fertig (26.01.2026)
**Issue:** [#17](https://github.com/nicolettas-muggelbude/myapps/issues/17)
**Aufwand:** ~4 Stunden (wie geplant)

#### Problem (gelöst)
User mit Mint (~2000 Pakete, ~400 gefilterte Apps) berichteten:
- Seitenwechsel spürbar langsam ✅ BEHOBEN
- App-Start dauert zu lange ✅ VERBESSERT
- 4 Seiten (100 Apps/Seite) fühlen sich träge an ✅ BEHOBEN

#### Implementierte Optimierungen

| Optimierung | Implementiert | Commits |
|-------------|---------------|---------|
| Icon-Cache Dictionary | ✅ | `b0ff7e4` |
| Icon-Caching in List View | ✅ | `76edd05` |
| Sortierung optimiert | ✅ | `873747c` |
| Memory Leak behoben | ✅ | `d95b3b5` |

#### Erreichte Verbesserungen

1. **Icon-Caching** ✅
   - Icons werden nur einmal geladen und gecacht
   - Cache shared zwischen allen Views
   - Cache-Key: `{pkg_name}_{pkg_type}`
   - Gecachte Seiten laden deutlich schneller

   ```python
   # Implementiert in MyAppsWindow
   self.icon_cache = {}  # Cache Dictionary

   # In _on_list_bind()
   cache_key = f"{pkg.name}_{pkg.package_type}"
   if cache_key not in self.icon_cache:
       self.icon_cache[cache_key] = self.gui.icon_manager.get_icon(...)
   pixbuf = self.icon_cache[cache_key]
   ```

2. **Sortierung optimiert** ✅
   - Sortierung nur EINMAL in `_apply_search_filter()`
   - Kein Re-Sortieren bei jedem Seitenwechsel
   - Von O(n log n) zu O(1) bei Seitenwechsel
   - Sortierung: Erst nach Typ (deb, flatpak, snap), dann alphabetisch

   ```python
   # In _apply_search_filter()
   self.gui.search_filtered_packages = sorted(
       packages,
       key=lambda p: (p.package_type, p.name.lower())
   )

   # In _populate_list_view() - keine Sortierung mehr!
   page_packages = self.gui.search_filtered_packages[start_idx:end_idx]
   ```

3. **Memory Leak behoben** ✅
   - Event Handler von `bind()` nach `setup()` verschoben
   - Handler wird nur EINMAL pro Widget verbunden
   - Handler nutzt `list_item.get_item()` zur Laufzeit
   - Stabiler Memory-Verbrauch

   ```python
   # In _on_list_setup() - nur einmal!
   def on_right_click(gesture, n_press, x, y):
       pkg = list_item.get_item()  # Zur Laufzeit holen
       if pkg:
           self._show_context_menu(box, pkg, x, y)

   gesture.connect("pressed", on_right_click)
   ```

#### Performance-Ergebnisse

**Seitenwechsel:**
- Deutlich schneller und flüssiger
- Gecachte Seiten laden sehr schnell
- App fühlt sich insgesamt performanter an

**Memory:**
- Stabiler Verbrauch auch bei vielen Seitenwechseln
- Kein kontinuierlicher Memory-Anstieg mehr

#### Warum wichtig?
**Voraussetzung für v0.3.0 erfüllt!** Die Performance-Basis ist gelegt. Das geplante Scope-Dropdown mit "Alle Pakete" (2000+) kann jetzt implementiert werden.

---

### v0.3.0 - Such-Scope & Features 🔍

**Priorität:** 🟡 Hoch
**Status:** Geplant
**Issue:** [#16](https://github.com/nicolettas-muggelbude/myapps/issues/16)
**Aufwand:** ~6-8 Stunden
**Voraussetzung:** v0.2.4 Performance-Fixes fertig

#### Features

##### 1. Scope-Dropdown für Suche
```
┌────────────────────┐  ┌──────────────────────────┐
│ Nur User-Apps    ▼ │  │ Apps durchsuchen...      │
└────────────────────┘  └──────────────────────────┘
 ↑ Such-Scope            ↑ min. 5 Zeichen
```

**Scope-Optionen:**
- **Nur User-Apps** (Standard)
  - Filtert System-Pakete aus
  - ~800 Apps durchsuchbar

- **Alle Pakete**
  - Inkl. System-Pakete
  - ~2000+ Pakete durchsuchbar

**Verhalten:**
- **Bei Liste/Tabelle:** Scope-Dropdown aktiv
- **Bei Desktop Apps View:** Scope-Dropdown deaktiviert (View filtert bereits)

##### 2. Mindestens 5 Zeichen für Suche
- Schränkt Ergebnisse deutlich ein
- Verhindert zu viele Treffer

##### 3. Pagination & Tooltips
- ✅ Funktioniert bereits im Suchmodus
- Keine Änderungen nötig

#### Technische Umsetzung

1. **UI-Komponenten** (~2h)
   - ComboBox (Scope-Dropdown) erstellen
   - Vor SearchEntry platzieren
   - Signal-Handler verbinden

2. **Such-Logik** (~3h)
   - Scope-Auswahl berücksichtigen
   - 5-Zeichen-Minimum implementieren
   - Cache für ungefilterte Pakete

3. **View-Integration** (~2h)
   - Scope bei Desktop Apps View deaktivieren
   - Scope-Änderung während Suche behandeln

4. **Testing** (~1h)
   - Verschiedene Scopes testen
   - Performance mit "Alle Pakete" prüfen

---

### v0.3.1 - Desktop Apps View 🖥️

**Priorität:** 🟢 Mittel
**Status:** Geplant
**Issue:** [#4](https://github.com/nicolettas-muggelbude/myapps/issues/4)
**Aufwand:** ~8-10 Stunden

#### Features

##### 1. Neue Ansicht: Desktop Apps
```
┌──────────────────────────────────────────────┐
│  [ 📋 Liste | 📊 Tabelle | 🖥️ Desktop Apps ] │
└──────────────────────────────────────────────┘
```

Zeigt **nur** Apps mit .desktop-Dateien:
- Höchste Relevanz für Endanwender
- Kleinste Auswahl (~50-100 Apps)
- Keine System-Tools/Libraries

##### 2. Desktop-App-Erkennung (Option B)

**Suchpfade:**
```python
DESKTOP_PATHS = [
    "/usr/share/applications/",              # System-Apps
    "~/.local/share/applications/",          # User-Apps
    "/var/lib/flatpak/exports/share/applications/",  # Flatpak
    "/var/lib/snapd/desktop/applications/",          # Snap
]
```

**Methode:**
- Parse .desktop-Dateien aus allen Pfaden
- Matche mit installierten Paketnamen
- Erstelle gefilterte Liste

**Performance:**
- Schnell (kein package-manager Query)
- Vollständig genug für 95% der Cases
- Guter Kompromiss zwischen Genauigkeit und Geschwindigkeit

##### 3. Scope-Integration

- **Bei Desktop Apps View:**
  - Scope-Dropdown automatisch deaktiviert
  - Suche beschränkt sich auf Desktop Apps
  - Keine "Alle Pakete" Option nötig

#### Technische Umsetzung

1. **.desktop Parser** (~3h)
   - Alle Desktop-Pfade durchsuchen
   - .desktop-Dateien parsen
   - Paketname aus Exec-Field extrahieren

2. **View erstellen** (~2h)
   - Gtk.Stack um dritte View erweitern
   - View-Switcher aktualisieren
   - ListView/ColumnView für Desktop Apps

3. **View-spezifische Logik** (~2h)
   - Scope-Dropdown bei Desktop Apps deaktivieren
   - Suche auf Desktop Apps beschränken
   - Filter-Integration

4. **Testing** (~1h)
   - .desktop-Erkennung testen
   - View-Switching testen
   - Suche in Desktop Apps View

---

### v0.4.0 - Weitere Features 📊

**Priorität:** 🟢 Mittel
**Status:** Ideen-Phase

#### Geplante Features

##### 1. Größen-Information für Pakete
**Issue:** [#5](https://github.com/nicolettas-muggelbude/myapps/issues/5)

- Spalte "Größe" in Tabellenansicht
- Größe in MB/GB anzeigen
- Sortierung nach Größe
- Summe aller installierten Pakete

##### 2. Virtual Scrolling
- Weg von Pagination (100 Apps/Seite)
- Echtes ListView-Scrolling
- Alle Apps in einer Liste
- Performance durch GTK4 Virtual Scrolling

##### 3. Icon-Anzeige in Views
- Aktuell: Nur Platzhalter
- Geplant: Echte Icons in ListView/ColumnView
- Mit Icon-Cache aus v0.2.4

---

### v1.0.0 - Stable Release 🎉

**Priorität:** 🔴 Kritisch (für Production)
**Status:** Nach Community-Testing

#### Voraussetzungen für v1.0.0

- ✅ Alle kritischen Bugs behoben
- ✅ Performance optimiert (v0.2.4)
- ✅ Scope-Dropdown funktioniert (v0.3.0)
- ✅ Desktop Apps View funktioniert (v0.3.1)
- ✅ Umfangreiches Testing auf verschiedenen Distros
- ✅ Dokumentation vollständig

#### Ziel
Erste **produktionsreife** Version für breite Nutzerbasis.

---

### v2.0.0 - Major Features 🚀

**Priorität:** 🟢 Niedrig (Zukunft)
**Status:** Langfristige Vision

#### Geplante Major Features

##### 1. Deinstallations-Funktion
- Pakete direkt aus MyApps deinstallieren
- Sicherheitsabfragen
- Abhängigkeiten-Warnung
- Integration mit package-manager (dpkg, pacman, etc.)

##### 2. Update-Benachrichtigungen
- Zeige verfügbare Updates
- "Update verfügbar" Badge
- Integration mit apt/pacman/dnf

##### 3. Paket-Details-Ansicht
- Ausführliche Infos zu jedem Paket
- Abhängigkeiten anzeigen
- Installierte Dateien auflisten
- Changelog anzeigen

---

## 🎯 Meilensteine

| Version | Fokus | Status | Datum |
|---------|-------|--------|-------|
| v0.2.4 | ⚡ Performance | ✅ Fertig | 26.01.2026 |
| v0.3.0 | 🔍 Such-Scope | 🟡 Geplant | Nach v0.2.4 |
| v0.3.1 | 🖥️ Desktop Apps | 🟡 Geplant | Nach v0.3.0 |
| v0.4.0 | 📊 Features | 💭 Ideen | TBD |
| v1.0.0 | 🎉 Stable | 💭 Zukunft | Nach Testing |
| v2.0.0 | 🚀 Major | 💭 Vision | Langfristig |

---

## 📝 Legende

### Priorität
- 🔴 **KRITISCH:** Blockiert andere Features / Major Bug
- 🟡 **Hoch:** Wichtiges Feature mit hohem User-Impact
- 🟢 **Mittel:** Nützliches Feature, nicht dringend
- ⚪ **Niedrig:** Nice-to-have, Zukunft

### Status
- ✅ **Fertig:** Implementiert und released
- 🔄 **In Arbeit:** Aktuell in Entwicklung
- 🟡 **Geplant:** Design fertig, bereit zur Implementierung
- 💭 **Ideen:** Konzept-Phase, noch nicht detailliert geplant

---

## 🤝 Mitwirken

Diese Roadmap ist nicht in Stein gemeißelt! Vorschläge und Feedback sind willkommen:

- **Issues:** https://github.com/nicolettas-muggelbude/myapps/issues
- **Discussions:** Für Feature-Diskussionen
- **Pull Requests:** Contributions willkommen!

---

**Letzte Aktualisierung:** 26. Januar 2026
**Nächstes Review:** Nach v0.3.0 Release
