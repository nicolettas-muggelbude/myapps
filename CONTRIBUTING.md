# Beiträge zu MyApps

Vielen Dank für dein Interesse an MyApps! Wir freuen uns über Beiträge aus der Community.

## Wie kann ich beitragen?

### Filter-Keywords vorschlagen

Wenn du System-Pakete findest, die nicht gefiltert werden sollten, kannst du neue Filter-Keywords vorschlagen:

1. Öffne ein [Issue](https://github.com/nicolettas-muggelbude/myapps/issues/new)
2. Verwende den Titel: „Filter-Vorschlag: [Paketname]"
3. Gib folgende Informationen an:
   - Paketname
   - Distribution (z.B. Ubuntu 24.04)
   - Warum es ein System-Paket ist
   - Vorgeschlagenes Filter-Keyword

### Bugs melden

1. Prüfe ob der Bug bereits gemeldet wurde
2. Öffne ein neues Issue mit:
   - Klarer Beschreibung des Problems
   - Schritte zur Reproduktion
   - Erwartetes vs. tatsächliches Verhalten
   - System-Informationen (Distribution, Version)
   - Log-Ausgaben (falls vorhanden)

### Features vorschlagen

1. Öffne ein Issue mit dem Label „enhancement"
2. Beschreibe das gewünschte Feature
3. Erkläre den Anwendungsfall
4. Wir diskutieren die Machbarkeit

### Code beitragen

1. Fork das Repository
2. Erstelle einen Feature-Branch (`git checkout -b feature/MeinFeature`)
3. Committe deine Änderungen (`git commit -m 'Füge MeinFeature hinzu'`)
4. Push zum Branch (`git push origin feature/MeinFeature`)
5. Öffne einen Pull Request

---

## Entwicklungsumgebung einrichten

### Voraussetzungen — System-Pakete (PFLICHT)

**GTK4-Bindings können NICHT via pip installiert werden — nur als System-Pakete!**

```bash
# Ubuntu 24.04 LTS
sudo apt install python3-gi python3-gi-cairo gir1.2-gtk-4.0 gir1.2-adw-1 python3-pillow

# Ubuntu 22.04 / Debian 12 / Linux Mint
sudo apt install python3-gi python3-gi-cairo gir1.2-gtk-4.0 gir1.2-adw-1 python3-pil

# Arch/Manjaro
sudo pacman -S python-gobject gtk4 libadwaita python-pillow

# Fedora/RHEL/CentOS
sudo dnf install python3-gobject gtk4 libadwaita python3-pillow

# openSUSE
sudo zypper install python3-gobject python3-gobject-Gdk typelib-1_0-Gtk-4_0 typelib-1_0-Adw-1 python3-Pillow
```

> **Ubuntu 24.04:** Das Paket heißt `python3-pillow` (nicht mehr `python3-pil`).

### Installation (Entwicklungsumgebung)

```bash
# 1. Repository klonen
git clone https://github.com/nicolettas-muggelbude/myapps.git
cd myapps

# 2. venv MIT --system-site-packages erstellen
#    (damit python3-gi aus dem System verfügbar ist)
python3 -m venv --system-site-packages venv
source venv/bin/activate

# 3. Nur Pillow via pip installieren (PyGObject kommt vom System)
pip install -e . --no-deps
pip install Pillow

# 4. App starten
python3 -m myapps.main
# oder einfach:
./run-dev.sh
```

> **Warum `--no-deps`?**
> Ohne dieses Flag versucht pip PyGObject von PyPI zu bauen.
> Das schlägt fehl, weil `pkg-config` + `libcairo2-dev` als
> Compiler-Abhängigkeiten fehlen. GTK-Bindings kommen immer vom System.

---

## Pakete bauen und testen

### DEB-Paket

```bash
# DEB bauen
./build-deb.sh

# Installieren und testen
sudo dpkg -i myapps_0.3.0_all.deb
myapps

# Deinstallieren
sudo dpkg -r myapps
```

### ~~AppImage~~ (discontinued ab v0.2.0)

AppImage wird nicht mehr angeboten. GTK4-System-Dependencies lassen sich nicht sinnvoll in AppImage bundeln.

---

## Code-Stil

- **Sprache**: Code-Kommentare und Docstrings auf Deutsch
- **Commit-Messages**: Auf Deutsch
- **Python**: PEP 8 Richtlinien befolgen
- **Type Hints**: Verwenden für alle Funktionen
- **Logging**: `logging`-Modul verwenden (nicht `print()`)

Beispiel:
```python
def meine_funktion(param: str) -> bool:
    """
    Beschreibung der Funktion

    Args:
        param: Beschreibung des Parameters

    Returns:
        True bei Erfolg, False bei Fehler
    """
    logger.info(f"Funktion aufgerufen mit: {param}")
    return True
```

---

## Testing

Bevor du einen Pull Request erstellst, teste bitte alle relevanten Bereiche:

### Grundfunktionen
- [ ] App startet ohne Fehler
- [ ] Dark Mode funktioniert (folgt System-Theme)
- [ ] Pakete werden beim Start geladen
- [ ] Listenansicht: Icons, Beschreibungen, Tooltips
- [ ] Tabellenansicht: Alle Spalten sichtbar, Spalten sortierbar
- [ ] Ansicht wechseln (Liste ↔ Tabelle)
- [ ] Pagination: Vor/Zurück-Navigation funktioniert

### v0.3.0 Features
- [ ] Scope-Dropdown: "Nur User-Apps" zeigt gefilterte Liste
- [ ] Scope-Dropdown: "Alle Pakete" zeigt vollständige Paketliste
- [ ] Suche: unter 5 Zeichen → Statusbar-Hinweis, keine Filterung
- [ ] Suche: ab 5 Zeichen → Live-Filterung in Name + Beschreibung
- [ ] Größe wird in Listenansicht angezeigt (falls verfügbar)
- [ ] Größe-Spalte in Tabellenansicht
- [ ] Datum-Spalte in Tabellenansicht
- [ ] Sortierung: alle 7 Optionen funktionieren korrekt
- [ ] Sortierung nach Größe: Pakete ohne Größe erscheinen am Ende
- [ ] Sortierung nach Datum: Pakete ohne Datum erscheinen am Ende

### Export & Sonstiges
- [ ] Export TXT, CSV, JSON funktioniert
- [ ] Export respektiert aktive Suche und Scope
- [ ] Rechtsklick-Menü: „Als System-App markieren" funktioniert
- [ ] About-Dialog: korrekte Version + Changelog aus WHATS_NEW.md
- [ ] Performance: Seitenwechsel flüssig, kein Memory-Anstieg

---

## Distro-Testing

Wir suchen Tester für verschiedene Distributionen:

- [ ] Debian 12 (Bookworm)
- [ ] Debian 13 (Trixie)
- [ ] Ubuntu 22.04 LTS
- [ ] Ubuntu 24.04 LTS
- [ ] Linux Mint
- [ ] Arch Linux
- [ ] Manjaro
- [ ] Fedora 41/42/43
- [ ] openSUSE Tumbleweed
- [ ] openSUSE Leap 16
- [ ] Solus

Wenn du eine dieser Distributionen verwendest, teste MyApps und melde Bugs oder bestätige dass es funktioniert!

---

## Übersetzungen

Aktuell werden Deutsch und Englisch unterstützt. Weitere Sprachen sind willkommen!

1. Kopiere `locales/de/LC_MESSAGES/myapps.po`
2. Übersetze die Strings
3. Erstelle einen Pull Request

---

## Community-Richtlinien

- Sei respektvoll und konstruktiv
- Hilf anderen Community-Mitgliedern
- Halte Diskussionen themenrelevant
- Keine Diskriminierung oder Belästigung

## Fragen?

Bei Fragen kannst du:
- Ein Issue öffnen
- Eine Diskussion im Discussions-Bereich starten
- Die Community im [Linux Guides DE Telegram-Chat](https://t.me/LinuxGuidesDECommunity) fragen

Vielen Dank für deine Unterstützung!
