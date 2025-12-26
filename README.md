<div align="center">
  <img src="assets/icons/io.github.nicolettas-muggelbude.myapps.svg" width="128" alt="MyApps Logo">

  # MyApps

  > Tool zum Auflisten und Verwalten installierter Linux-Anwendungen

  [![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
  [![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
  [![Status](https://img.shields.io/badge/status-beta-green.svg)](https://github.com/nicolettas-muggelbude/myapps)
</div>

[English](README.en.md) | **Deutsch**

## Über MyApps

MyApps ist ein benutzerfreundliches Tool für Linux, das alle installierten Anwendungen übersichtlich darstellt - ohne System-Clutter. Es wurde auf Wunsch der Community [Linux Guides DE](https://t.me/LinuxGuidesDECommunity) entwickelt.

### Features

✨ **Multi-Distribution-Support**
- Debian, Ubuntu, Linux Mint
- Arch Linux, Manjaro
- Fedora, RHEL, CentOS
- Solus
- openSUSE
- Snap & Flatpak (distributionsübergreifend)

🎨 **Moderne Oberfläche**
- Native GTK4 + Libadwaita Integration
- Dark Mode (folgt System-Theme)
- Virtual Scrolling (10.000+ Pakete kein Problem)
- Tabellenansicht & Listenansicht
- Umschaltbar per Knopfdruck

🔍 **Intelligentes Filtern**
- Automatische Erkennung von System-Apps
- Distro-spezifische Filter
- Eigene Filter hinzufügen (Rechtsklick)
- Community-erweiterbar

📤 **Export-Funktionen**
- Text (TXT)
- CSV (für Excel/LibreOffice)
- JSON (für Scripte)

🌍 **Mehrsprachig**
- Deutsch
- Englisch
- Weitere Sprachen willkommen!

## Screenshots

### Hauptfenster (Listenansicht)
<img src="docs/screenshots/main-window.png" width="800" alt="MyApps Hauptfenster">

### Tabellenansicht
<img src="docs/screenshots/table-view.png" width="800" alt="MyApps Tabellenansicht">

### Suchfunktion
<img src="docs/screenshots/search-demo.png" width="800" alt="MyApps Suchfunktion">

### Dark Mode
<img src="docs/screenshots/dark-mode.png" width="800" alt="MyApps Dark Mode">

## Installation

### Voraussetzungen

**Ab Version 0.2.0 benötigt MyApps GTK4 + Libadwaita:**

```bash
# Debian/Ubuntu/Mint
sudo apt install python3-gi python3-gi-cairo gir1.2-gtk-4.0 gir1.2-adw-1 python3-pil

# Arch/Manjaro
sudo pacman -S python-gobject gtk4 libadwaita python-pillow

# Fedora/RHEL/CentOS
sudo dnf install python3-gobject gtk4 libadwaita python3-pillow

# openSUSE
sudo zypper install python3-gobject python3-gobject-Gdk typelib-1_0-Gtk-4_0 typelib-1_0-Adw-1 python3-Pillow
```

### Aus DEB-Paket (Debian/Ubuntu/Mint)

```bash
# Download des DEB-Pakets aus dem Release
sudo dpkg -i myapps_0.2.0_all.deb

# Starten
myapps
```

### Als Flatpak (empfohlen - alle Distributionen)

**Ab Version 0.2.0 empfohlen:**

```bash
# Flatpak installieren (falls nicht vorhanden)
# Debian/Ubuntu: sudo apt install flatpak
# Arch: sudo pacman -S flatpak
# Fedora: sudo dnf install flatpak

# MyApps installieren (noch nicht verfügbar - Release kommt bald)
# flatpak install flathub de.pc-wittfoot.myapps

# Starten
# flatpak run de.pc-wittfoot.myapps
```

### ~~Als AppImage~~ (discontinued ab v0.2.0)

**Hinweis:** AppImage wird ab v0.2.0 nicht mehr angeboten, da GTK4-System-Dependencies schwer zu bundeln sind. Nutze stattdessen DEB-Paket oder Flatpak.

### Aus Quellcode (Development)

```bash
# Repository klonen
git clone https://github.com/nicolettas-muggelbude/myapps.git
cd myapps

# System-Dependencies installieren (siehe oben unter "Voraussetzungen")
# Debian/Ubuntu/Mint:
sudo apt install python3-gi python3-gi-cairo gir1.2-gtk-4.0 gir1.2-adw-1 python3-pil

# Virtual Environment erstellen (optional)
python3 -m venv venv
source venv/bin/activate

# Python-Dependencies installieren
pip install -e .

# App starten
python3 -m myapps.main
```

## Pakete selbst bauen

### DEB-Paket bauen

```bash
# Build-Script ausführen
./build-deb.sh

# Optinal: Spezifische Version
./build-deb.sh 0.1.0

# Installieren
sudo dpkg -i myapps_0.1.0_all.deb
```

### AppImage bauen

```bash
# appimagetool herunterladen (einmalig)
wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage
chmod +x appimagetool-x86_64.AppImage
mv appimagetool-x86_64.AppImage appimagetool

# Für WSL/Systeme ohne FUSE: Tool extrahieren
./appimagetool --appimage-extract
mv squashfs-root appimagetool-extracted

# Build-Script ausführen
./build-appimage.sh

# Optinal: Spezifische Version
./build-appimage.sh 0.1.0

# Ausführen
chmod +x MyApps-0.1.0-x86_64.AppImage
./MyApps-0.1.0-x86_64.AppImage
```

## Verwendung

1. **App starten**: Öffne MyApps aus dem Anwendungsmenü oder Terminal
2. **Pakete laden**: Beim Start werden automatisch alle Pakete geladen
3. **Ansicht wechseln**: Klicke auf "Ansicht wechseln" für Tabelle ↔ Liste
4. **Exportieren**: Klicke auf "Exportieren" und wähle das Format
5. **Filtern**: Rechtsklick auf ein Paket → "Als System-App markieren"

## Unterstützte Paketmanager

| Paketmanager | Distributionen | Status |
|--------------|----------------|--------|
| dpkg | Debian, Ubuntu, Mint | ✅ |
| pacman | Arch, Manjaro | ✅ |
| rpm/dnf | Fedora, RHEL, CentOS | ✅ |
| rpm/zypper | openSUSE | ✅ |
| eopkg | Solus | ✅ |
| snap | Alle | ✅ |
| flatpak | Alle | ✅ |

## Beitragen

Beiträge sind herzlich willkommen! Siehe [CONTRIBUTING.md](CONTRIBUTING.md) für Details.

### Filter-Keywords vorschlagen

Findest du System-Pakete die nicht gefiltert werden? Öffne ein [Issue](https://github.com/nicolettas-muggelbude/myapps/issues)!

### Tester gesucht!

Wir brauchen Community-Tester für verschiedene Distributionen:
- Debian
- Ubuntu & Varianten
- Arch Linux & Derivate
- Fedora
- Solus
- openSUSE

## Roadmap

### v0.1.x (Stable - tkinter) ✅
- [x] Multi-Distro-Support
- [x] Moderne GUI mit Dark Mode
- [x] Icons mit Fallback
- [x] Export-Funktionen
- [x] Mehrsprachigkeit (DE/EN)
- [x] Distro-spezifische Filter
- [x] User-Filter
- [x] Pagination (100 Apps/Seite)

### v0.2.0 (Aktuell - GTK4 Migration) ⏳
- [x] GTK4 + Libadwaita GUI
- [x] Virtual Scrolling (10.000+ Pakete)
- [x] Kein X-Server BadAlloc mehr
- [x] Native GNOME Integration
- [ ] Community Testing

### v0.3.0 (Geplant)
- [ ] Installationsdatum anzeigen
- [ ] Sortier-Funktionen

### v0.4.0 (Geplant)
- [ ] Update-Status prüfen
- [ ] Benachrichtigungen für Updates

### v1.0.0 (Stable)
- [ ] Community-Testing abgeschlossen
- [ ] Bug-Fixes
- [ ] Stabile Version

### v2.0.0 (Zukunft)
- [ ] Deinstallations-Funktion
- [ ] Paket-Details-Ansicht

## Häufige Fragen

**Q: Warum werden manche Apps nicht angezeigt?**
A: Sie wurden wahrscheinlich als System-Apps gefiltert. Du kannst eigene Filter in `~/.config/myapps/user-filters.json` anpassen.

**Q: Wird meine Distribution unterstützt?**
A: Siehe "Unterstützte Paketmanager" oben. Weitere Distributionen können hinzugefügt werden.

**Q: Kann ich zur Filterliste beitragen?**
A: Ja! Öffne ein Issue mit deinen Filter-Vorschlägen.

**Q: Ist MyApps sicher?**
A: MyApps ist Open Source (GPLv3) und führt nur lesende Operationen aus (kein `sudo` nötig). Der Code kann überprüft werden.

## Lizenz

MyApps ist unter der [GNU General Public License v3.0](LICENSE) lizenziert.

## Credits

- Entwickelt für die [Linux Guides DE Community](https://t.me/LinuxGuidesDECommunity)
- Icons aus System-Themes
- UI basiert auf [GTK4](https://www.gtk.org/) und [Libadwaita](https://gnome.pages.gitlab.gnome.org/libadwaita/)

## 💝 Unterstütze dieses Projekt

Wenn dir MyApps hilft, kannst du die Entwicklung unterstützen:

[![Spenden via PayPal](https://img.shields.io/badge/PayPal-Spenden-00457C?style=for-the-badge&logo=paypal&logoColor=white)](https://www.paypal.com/ncp/payment/UYJ73YNEZ3KHL)

**Spenden gehen an:** PC-Wittfoot UG (Spendenverwalter)
**Verwendung:** Serverkosten, Hardware, Entwicklerzeit für MyApps

**Hinweis:** Die Entwicklung erfolgt durch die Linux Guides DE Community (Open Source).
PC-Wittfoot UG verwaltet nur die Spenden, ist aber NICHT der Entwickler.

**Rechtliches:**
[Impressum](https://nicolettas-muggelbude.github.io/myapps/impressum) | [Datenschutz](https://nicolettas-muggelbude.github.io/myapps/datenschutz)

## Support

- 🐛 [Bug melden](https://github.com/nicolettas-muggelbude/myapps/issues)
- 💡 [Feature vorschlagen](https://github.com/nicolettas-muggelbude/myapps/issues)
- 💬 [Community-Chat](https://t.me/LinuxGuidesDECommunity)

---

*Gemacht mit ❤️ für die Linux-Community*
