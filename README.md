# MyApps 📦

> Tool zum Auflisten und Verwalten installierter Linux-Anwendungen

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
[![Status](https://img.shields.io/badge/status-alpha-orange.svg)](https://github.com/nicolettas-muggelbude/myapps)

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
- Dark Mode (ttkbootstrap)
- Tabellenansicht (wie ein Dateimanager)
- Listenansicht (mit Icons)
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

*Coming soon - Screenshots werden nach dem ersten Release hinzugefügt*

## Installation

### Aus DEB-Paket (Debian/Ubuntu/Mint)

```bash
# Download des DEB-Pakets aus dem Release
sudo dpkg -i myapps_0.1.0_all.deb

# Starten
myapps
```

### Als AppImage (alle Distributionen)

```bash
# Download des AppImage aus dem Release
chmod +x MyApps-0.1.0-x86_64.AppImage

# Starten
./MyApps-0.1.0-x86_64.AppImage
```

**Hinweis:** Das AppImage benötigt `python3`, `python3-tk` und `python3-pil` auf dem System:
```bash
# Debian/Ubuntu/Mint
sudo apt install python3 python3-tk python3-pil python3-pil.imagetk

# Arch/Manjaro
sudo pacman -S python tk python-pillow

# Fedora
sudo dnf install python3 python3-tkinter python3-pillow python3-pillow-tk
```

### Aus Quellcode (Development)

```bash
# Repository klonen
git clone https://github.com/nicolettas-muggelbude/myapps.git
cd myapps

# Virtual Environment erstellen
python3 -m venv venv
source venv/bin/activate

# Dependencies installieren
pip install -r requirements.txt

# App starten
python3 -m src.myapps.main
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

### v0.1.0 (Aktuell - Alpha) ⏳
- [x] Multi-Distro-Support
- [x] Moderne GUI mit Dark Mode
- [x] Icons mit Fallback
- [x] Export-Funktionen
- [x] Mehrsprachigkeit (DE/EN)
- [x] Distro-spezifische Filter
- [x] User-Filter

### v0.2.0 (Geplant)
- [ ] Größen-Information anzeigen
- [ ] Performance-Optimierungen

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
- UI basiert auf [ttkbootstrap](https://github.com/israel-dryer/ttkbootstrap)

## 💙 Unterstütze dieses Projekt

MyApps ist Open Source und kostenlos. Wenn dir das Projekt hilft, freue ich mich über eine kleine Spende für die Weiterentwicklung!

<a href="https://www.paypal.com/ncp/payment/UYJ73YNEZ3KHL" target="_blank">
  <img
    src="https://www.paypalobjects.com/de_DE/DE/i/btn/btn_donateCC_LG.gif"
    alt="Über PayPal spenden"
  />
</a>

*Spenden werden von der PC-Wittfoot UG verwaltet und für Serverkosten, Hardware und Entwicklerzeit verwendet. Vielen Dank für deine Unterstützung!*

[Impressum](https://nicolettas-muggelbude.github.io/myapps/impressum) | [Datenschutz](https://nicolettas-muggelbude.github.io/myapps/datenschutz)

## Support

- 🐛 [Bug melden](https://github.com/nicolettas-muggelbude/myapps/issues)
- 💡 [Feature vorschlagen](https://github.com/nicolettas-muggelbude/myapps/issues)
- 💬 [Community-Chat](https://t.me/LinuxGuidesDECommunity)

---

*Gemacht mit ❤️ für die Linux-Community*
