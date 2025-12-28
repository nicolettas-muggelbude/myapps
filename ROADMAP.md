# MyApps - Roadmap

Dieser Plan zeigt die geplante Entwicklung von MyApps.

---

## 📍 Aktueller Stand

**Aktuelle Version:** v0.2.3
**Status:** Beta - Community Testing läuft
**Verfügbar:** OBS (11 Distributionen), AUR (Arch Linux)

---

## 🚀 Geplante Releases

### v0.2.4 - Performance-Release ⚡ (NÄCHSTE VERSION)

**Priorität:** 🔴 KRITISCH
**Status:** Geplant
**Issue:** [#17](https://github.com/nicolettas-muggelbude/myapps/issues/17)
**Aufwand:** ~4 Stunden

#### Problem
User mit Mint (~2000 Pakete, ~400 gefilterte Apps) berichten:
- Seitenwechsel spürbar langsam
- App-Start dauert zu lange
- 4 Seiten (100 Apps/Seite) fühlen sich träge an

#### Identifizierte Bottlenecks

| Bottleneck | Impact | Lösung | Verbesserung |
|------------|--------|--------|--------------|
| Icons bei jedem Seitenwechsel neu laden | 🔥🔥🔥 Kritisch | Icon-Cache implementieren | ~80% schneller |
| Sortierung bei jedem Seitenwechsel | 🔥🔥 Hoch | Einmal nach Filterung sortieren | 5-10x schneller |
| Event Handler Memory Leak | 🔥 Mittel | Handler in `setup` statt `bind` | Weniger RAM-Verbrauch |

#### Geplante Fixes

1. **Icon-Caching** (größter Impact)
   ```python
   # Icons nur einmal laden, dann cachen
   self.icon_cache = {}  # Package-Name -> GdkPixbuf

   if cache_key not in self.icon_cache:
       self.icon_cache[cache_key] = self.icon_manager.get_icon(...)
   ```

2. **Sortierung optimieren**
   ```python
   # Nach Filterung einmal sortieren und speichern
   def _on_packages_loaded(self, packages):
       self.search_filtered_packages = sorted(packages, ...)

   # Nicht mehr bei jedem Seitenwechsel sortieren
   ```

3. **Event Handler Cleanup**
   ```python
   # Context Menu nur in setup (einmal), nicht in bind
   def _on_list_setup(self, factory, list_item):
       gesture.connect("pressed", handler)
   ```

#### Warum zuerst?
**Voraussetzung für v0.3.0!** Das Scope-Dropdown fügt "Alle Pakete" (2000+) hinzu. Ohne Performance-Fixes wird das unerträglich langsam.

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

| Version | Fokus | Status | ETA |
|---------|-------|--------|-----|
| v0.2.4 | ⚡ Performance | 🟡 Geplant | TBD |
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

**Letzte Aktualisierung:** 28. Dezember 2024
**Nächstes Review:** Nach v0.2.4 Release
