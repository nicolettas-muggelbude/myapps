<div align="center">
  <img src="assets/icons/io.github.nicolettas-muggelbude.myapps.svg" width="128" alt="MyApps Logo">

  # MyApps

  > Tool zum Auflisten und Verwalten installierter Linux-Anwendungen

  [![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
  [![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
  [![Version](https://img.shields.io/badge/version-0.3.0-green.svg)](https://github.com/nicolettas-muggelbude/myapps/releases)
  [![Status](https://img.shields.io/badge/status-beta-orange.svg)](https://github.com/nicolettas-muggelbude/myapps)
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

🔍 **Suche & Filter**
- Scope-Dropdown: "Nur User-Apps" oder "Alle Pakete"
- Live-Suche in Name + Beschreibung (ab 5 Zeichen)
- Automatische Erkennung von System-Apps
- Distro-spezifische Filter
- Eigene Filter hinzufügen (Rechtsklick)

📊 **Paket-Informationen**
- Installierte Größe (dpkg, rpm, pacman, flatpak, snap)
- Installationsdatum (dpkg, rpm, pacman, flatpak, snap)
- Sortierfunktion: Name, Größe, Datum (auf- und absteigend)

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

**MyApps benötigt GTK4 + Libadwaita als System-Pakete:**

```bash
# Debian 12 / Linux Mint
sudo apt install python3-gi python3-gi-cairo gir1.2-gtk-4.0 gir1.2-adw-1 python3-pil

# Ubuntu 24.04 LTS (python3-pil wurde zu python3-pillow umbenannt)
sudo apt install python3-gi python3-gi-cairo gir1.2-gtk-4.0 gir1.2-adw-1 python3-pillow

# Arch/Manjaro
sudo pacman -S python-gobject gtk4 libadwaita python-pillow

# Fedora/RHEL/CentOS
sudo dnf install python3-gobject gtk4 libadwaita python3-pillow

# openSUSE
sudo zypper install python3-gobject python3-gobject-Gdk typelib-1_0-Gtk-4_0 typelib-1_0-Adw-1 python3-Pillow
```

> **Hinweis Ubuntu 24.04:** Das Paket `python3-pil` existiert dort nicht mehr — bitte `python3-pillow` verwenden.

### Aus OBS (Empfohlen - Debian/Ubuntu/Fedora/openSUSE)

**📦 Professionelle Pakete für 11 Distributionen über openSUSE Build Service:**

[![OBS](https://img.shields.io/badge/OBS-MyApps-73BA25?style=for-the-badge&logo=opensuse&logoColor=white)](https://software.opensuse.org//download.html?project=home%3Anicoletta%3Amyapps&package=myapps)

**Debian/Ubuntu:**
```bash
# Debian 12 (Bookworm)
echo "deb https://download.opensuse.org/repositories/home:/nicoletta:/myapps/Debian_12/ /" | sudo tee /etc/apt/sources.list.d/myapps.list
wget -qO- https://download.opensuse.org/repositories/home:/nicoletta:/myapps/Debian_12/Release.key | sudo gpg --dearmor -o /etc/apt/trusted.gpg.d/myapps.gpg
sudo apt update && sudo apt install myapps

# Ubuntu 24.04 LTS
echo "deb https://download.opensuse.org/repositories/home:/nicoletta:/myapps/Ubuntu_24.04/ /" | sudo tee /etc/apt/sources.list.d/myapps.list
wget -qO- https://download.opensuse.org/repositories/home:/nicoletta:/myapps/Ubuntu_24.04/Release.key | sudo gpg --dearmor -o /etc/apt/trusted.gpg.d/myapps.gpg
sudo apt update && sudo apt install myapps
```

**Fedora:**
```bash
# Fedora 41
sudo dnf config-manager --add-repo https://download.opensuse.org/repositories/home:/nicoletta:/myapps/Fedora_41/home:nicoletta:myapps.repo
sudo dnf install myapps
```

**openSUSE:**
```bash
# openSUSE Tumbleweed
sudo zypper addrepo https://download.opensuse.org/repositories/home:/nicoletta:/myapps/openSUSE_Tumbleweed/home:nicoletta:myapps.repo
sudo zypper refresh && sudo zypper install myapps
```

**Weitere verfügbare Distributionen:**
- Debian 13 (Trixie)
- Ubuntu 22.04 LTS, 25.10
- Fedora 42, 43
- openSUSE Leap 16, Slowroll

[Alle OBS-Pakete ansehen →](https://software.opensuse.org//download.html?project=home%3Anicoletta%3Amyapps&package=myapps)

---

### Aus AUR (Empfohlen - Arch Linux)

[![AUR Version](https://img.shields.io/badge/AUR-myapps-1793D1?style=for-the-badge&logo=archlinux&logoColor=white)](https://aur.archlinux.org/packages/myapps)

```bash
# Mit AUR Helper (z.B. yay)
yay -S myapps

# Oder mit paru
paru -S myapps

# Manuell
git clone https://aur.archlinux.org/myapps.git
cd myapps
makepkg -si
```

### Aus GitHub DEB-Paket (⚠️ Nur für Testing)

**⚠️ WARNUNG:** Dieses Paket ist NUR für Testing/Development gedacht!

**Für Production bitte OBS-Pakete nutzen** (siehe oben).

```bash
# Nach dem Download installieren
sudo dpkg -i myapps_0.3.0_all.deb

# Falls Dependencies fehlen
sudo apt-get install -f

# Starten
myapps
```

### ~~Als Flatpak~~ (Nicht verfügbar)

**Flathub hat MyApps abgelehnt** aufgrund benötigter `/var/lib` Zugriffe für Paketmanager-Datenbanken.

**Alternative:** Nutze **OBS-Pakete** (siehe oben) - diese bieten native System-Integration ohne Sandbox-Einschränkungen.

### ~~Als AppImage~~ (discontinued ab v0.2.0)

AppImage wird ab v0.2.0 nicht mehr angeboten, da GTK4-System-Dependencies schwer zu bundeln sind.

### Aus Quellcode (Development)

```bash
# Repository klonen
git clone https://github.com/nicolettas-muggelbude/myapps.git
cd myapps

# 1. System-Pakete installieren (PFLICHT - GTK4 kann nicht via pip gebaut werden!)
# Ubuntu 24.04:
sudo apt install python3-gi python3-gi-cairo gir1.2-gtk-4.0 gir1.2-adw-1 python3-pillow
# Ubuntu 22.04 / Debian 12:
sudo apt install python3-gi python3-gi-cairo gir1.2-gtk-4.0 gir1.2-adw-1 python3-pil

# 2. venv MIT --system-site-packages (damit python3-gi verfügbar ist)
python3 -m venv --system-site-packages venv
source venv/bin/activate

# 3. Nur Pillow via pip (PyGObject kommt vom System)
pip install -e . --no-deps
pip install Pillow

# 4. App starten
python3 -m myapps.main
# oder einfach:
./run-dev.sh
```

> **Wichtig:** `pip install -e .` **ohne** `--no-deps` schlägt fehl, weil pip versucht PyGObject zu kompilieren — das benötigt `pkg-config` + `libcairo2-dev`. GTK-Bindings müssen als System-Paket kommen.

## Pakete selbst bauen

### DEB-Paket bauen

```bash
# Build-Script ausführen
./build-deb.sh

# Optional: Spezifische Version
./build-deb.sh 0.3.0

# Installieren
sudo dpkg -i myapps_0.3.0_all.deb
```

## Verwendung

1. **App starten**: Öffne MyApps aus dem Anwendungsmenü oder Terminal
2. **Pakete laden**: Beim Start werden automatisch alle User-Apps geladen
3. **Scope wechseln**: Dropdown neben der Suche → "Nur User-Apps" oder "Alle Pakete"
4. **Suchen**: Mindestens 5 Zeichen eingeben für Live-Suche
5. **Sortieren**: Dropdown in der Navigationsleiste → nach Name, Größe oder Datum
6. **Ansicht wechseln**: Buttons oben → Liste oder Tabelle
7. **Exportieren**: Klicke auf "Exportieren" und wähle das Format (TXT/CSV/JSON)
8. **Filtern**: Rechtsklick auf ein Paket → "Als System-App markieren"

## Unterstützte Paketmanager

| Paketmanager | Distributionen | Größe | Datum |
|--------------|----------------|-------|-------|
| dpkg | Debian, Ubuntu, Mint | ✅ | ✅ |
| pacman | Arch, Manjaro | ✅ | ✅ |
| rpm/dnf | Fedora, RHEL, CentOS | ✅ | ✅ |
| rpm/zypper | openSUSE | ✅ | ✅ |
| flatpak | Alle | ✅ | ✅ |
| snap | Alle | ✅ | ✅ |
| eopkg | Solus | — | — |

## Roadmap

### v0.1.x (Stable - tkinter) ✅
- [x] Multi-Distro-Support
- [x] Moderne GUI mit Dark Mode
- [x] Export-Funktionen
- [x] Mehrsprachigkeit (DE/EN)

### v0.2.x (GTK4 Migration) ✅
- [x] GTK4 + Libadwaita GUI
- [x] Virtual Scrolling
- [x] Suchfunktion
- [x] OBS-Pakete (11 Distributionen)
- [x] AUR-Paket
- [x] Performance-Optimierungen (Icon-Cache, Memory Leak Fix)

### v0.3.0 (Aktuell) ✅
- [x] Scope-Dropdown: User-Apps vs. Alle Pakete
- [x] Installierte Größe (dpkg, rpm, pacman, flatpak, snap)
- [x] Installationsdatum (dpkg, rpm, pacman, flatpak, snap)
- [x] Sortierfunktion (Name, Größe, Datum)
- [x] Mindest-Zeichen für Suche (5 Zeichen)

### v0.3.1 (Geplant)
- [ ] Desktop Apps View (.desktop-Dateien)

### v0.4.0 (Geplant)
- [ ] Update-Status prüfen
- [ ] Benachrichtigungen für Updates

### v1.0.0 (Stable)
- [ ] Community-Testing abgeschlossen
- [ ] Stabile Version

### v2.0.0 (Zukunft)
- [ ] Deinstallations-Funktion

## Häufige Fragen

**Q: Warum werden manche Apps nicht angezeigt?**
A: Sie wurden wahrscheinlich als System-Apps gefiltert. Wechsle im Scope-Dropdown zu "Alle Pakete" oder passe eigene Filter in `~/.config/myapps/user-filters.json` an.

**Q: `pip install -e .` schlägt fehl mit pycairo-Fehler?**
A: GTK-Bindings können nicht via pip kompiliert werden. Installiere `python3-gi` als System-Paket und nutze `pip install -e . --no-deps`. Siehe Abschnitt "Aus Quellcode" oben.

**Q: Ubuntu 24.04: `python3-pil` nicht gefunden?**
A: In Ubuntu 24.04 wurde das Paket zu `python3-pillow` umbenannt. Nutze `sudo apt install python3-pillow`.

**Q: Wird meine Distribution unterstützt?**
A: Siehe "Unterstützte Paketmanager" oben. Weitere Distributionen können hinzugefügt werden.

**Q: Ist MyApps sicher?**
A: MyApps ist Open Source (GPLv3) und führt nur lesende Operationen aus (kein `sudo` nötig).

## Beitragen

Beiträge sind herzlich willkommen! Siehe [CONTRIBUTING.md](CONTRIBUTING.md) für Details.

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
