# MyApps - Roadmap

Dieser Plan zeigt die geplante Entwicklung von MyApps.

---

## 📍 Aktueller Stand

**Aktuelle Version:** v0.4.0
**Status:** Performance-Release — Virtual Scrolling + Update-Benachrichtigung
**Verfügbar:** OBS (11 Distributionen), AUR (Arch Linux)

---

## 🚀 Releases

### v0.4.0 - Virtual Scrolling + Update-Benachrichtigung ⚡
**Status:** ✅ Fertig (12.04.2026)

#### Features

1. **Virtual Scrolling (weg von Pagination)**
   - Alle Apps in einer Liste ohne Seitenumbruch
   - GTK4 `Gtk.ListView` rendert nur sichtbare Elemente
   - Auch bei 2000+ Paketen performant
   - Sort-Bar ersetzt Pagination-Bar (übersichtlicher)

2. **Update-Benachrichtigung**
   - Prüft GitHub Releases API beim Start im Hintergrund
   - `Adw.Banner` wenn neue Version verfügbar
   - Hinweis: "v0.4.x verfügbar — via apt upgrade / pacman -Syu installierbar"
   - Klick auf "Changelog" öffnet GitHub Releases

#### Technische Details
- Keine `current_page`/`items_per_page` Variablen mehr
- `_create_pagination_bar()` → `_create_sort_bar()`
- `_update_pagination_controls()` → `_update_count_label()`
- Update-Check: `urllib.request` + GitHub API, Timeout 5s, daemon=True

---

### v0.2.4 - Performance-Release ⚡
**Status:** ✅ Fertig (26.01.2026)

- Icon-Caching implementiert
- Sortierung optimiert (einmal nach Filterung)
- Memory Leak behoben (Event Handler in setup statt bind)
- Export-Format-Bug behoben

---

### v0.3.0 - Such-Scope & Features 🔍
**Status:** ✅ Fertig (08.03.2026)

- Scope-Dropdown "Nur User-Apps" / "Alle Pakete" (Issue #16)
- Installierte Größe in Liste und Tabelle (Issue #5)
- Installationsdatum in Liste und Tabelle (Issue #10)
- Sortierfunktion 7 Optionen (Issue #11)
- Mindestens 5 Zeichen für Suche
- Performance-Fix: kein Einfrieren beim View-Wechsel

---

### v0.3.1 - Desktop Apps View 🖥️
**Status:** ✅ Fertig (31.03.2026)

- Desktop-Apps-Ansicht — dritter Tab (Issue #4)
- DesktopFileManager parst .desktop-Dateien
- Lokalisierte Namen/Beschreibungen, 48px Icons

---

### v1.0.0 - Stable Release 🎉

**Priorität:** 🔴 Kritisch (für Production)
**Status:** Nach Community-Testing

#### Voraussetzungen für v1.0.0

- ✅ Alle kritischen Bugs behoben
- ✅ Performance optimiert (v0.2.4 + v0.4.0)
- ✅ Scope-Dropdown (v0.3.0)
- ✅ Desktop Apps View (v0.3.1)
- ✅ Virtual Scrolling (v0.4.0)
- ✅ Update-Benachrichtigung (v0.4.0)
- Umfangreiches Testing auf verschiedenen Distros
- Dokumentation vollständig

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

##### 2. Paket-Details-Ansicht
- Ausführliche Infos zu jedem Paket
- Abhängigkeiten anzeigen
- Installierte Dateien auflisten

##### 3. Icon-Anzeige in ListView/ColumnView
- Aktuell: Platzhalter (icons werden geladen aber nicht immer angezeigt)
- Geplant: Zuverlässige echte Icons

---

## 🎯 Meilensteine

| Version | Fokus | Status | Datum |
|---------|-------|--------|-------|
| v0.2.4 | ⚡ Performance (Icons, Memory) | ✅ Fertig | 26.01.2026 |
| v0.3.0 | 🔍 Scope, Größe, Datum, Sort | ✅ Fertig | 08.03.2026 |
| v0.3.1 | 🖥️ Desktop Apps View | ✅ Fertig | 31.03.2026 |
| v0.4.0 | ⚡ Virtual Scrolling + Updates | ✅ Fertig | 12.04.2026 |
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

Vorschläge und Feedback sind willkommen:

- **Issues:** https://github.com/nicolettas-muggelbude/myapps/issues
- **Discussions:** Für Feature-Diskussionen
- **Pull Requests:** Contributions willkommen!

---

**Letzte Aktualisierung:** 12. April 2026
**Nächstes Review:** Nach v0.4.0 Community-Testing
