# MyApps v0.3.0 — Scope, Größe, Datum & Sortierung

**Das größte Feature-Update seit der GTK4-Migration!**

---

## ✨ Neue Features

### 🔭 Scope-Dropdown (Issue #16)
- **"Nur User-Apps"** (Standard): Gefilterte Ansicht wie bisher
- **"Alle Pakete"**: Alle installierten Pakete (~1000-3000+), ungefiltert
- Suche und Sortierung funktionieren in beiden Scopes

### 📏 Installierte Größe (Issue #5)
- ✅ dpkg — `${Installed-Size}` (KB)
- ✅ rpm/dnf — `%{SIZE}` (Bytes)
- ✅ pacman — `pacman -Qi` "Installed Size"
- ✅ flatpak — `flatpak list --columns=installed-size`
- ✅ snap — `du -sb` (Batch-Aufruf)
- Anzeige in Listenansicht (rechter Rand) und Tabellenansicht (Spalte)

### 📅 Installationsdatum (Issue #10)
- ✅ dpkg — `/var/log/dpkg.log*` (inkl. gzip-Archive)
- ✅ rpm — `%{INSTALLTIME}` (Unix-Timestamp)
- ✅ pacman — `pacman -Qi` "Install Date"
- ✅ flatpak/snap — Filesystem-Zeitstempel
- Sprachgerechte Anzeige: "26. Dez. 2024" (DE) / "Dec 26, 2024" (EN)

### 🔢 Sortierfunktion (Issue #11)
7 Optionen im Dropdown:
- Standard (Typ + Alphabetisch)
- Name A→Z / Z→A
- Größte / Kleinste zuerst
- Neueste / Älteste zuerst
- Pakete ohne Größe/Datum erscheinen am Ende

### 🔍 Mindest-Zeichen für Suche
- Suche startet erst ab **5 Zeichen**
- Statusbar zeigt Hinweis bei weniger Zeichen

---

## 🚀 Performance

- **Kein Einfrieren** beim Wechsel Tabelle → Liste (früher bis zu 7s Wartezeit)
- Listenansicht rendert sofort mit gecachten Beschreibungen
- Lokalisierte apt-Beschreibungen werden im Hintergrund nachgeladen

---

## 📦 Installation

### **OBS-Pakete** — Empfohlen ✅

<a href="https://software.opensuse.org//download.html?project=home%3Anicoletta%3Amyapps&package=myapps"><img src="https://img.shields.io/badge/Download-OBS_Pakete-73BA25?style=for-the-badge&logo=opensuse&logoColor=white" alt="OBS Download"></a>

**Debian 12 (Bookworm):**
```bash
echo "deb https://download.opensuse.org/repositories/home:/nicoletta:/myapps/Debian_12/ /" | sudo tee /etc/apt/sources.list.d/myapps.list
wget -qO- https://download.opensuse.org/repositories/home:/nicoletta:/myapps/Debian_12/Release.key | sudo gpg --dearmor -o /etc/apt/trusted.gpg.d/myapps.gpg
sudo apt update && sudo apt install myapps
```

**Ubuntu 24.04 LTS:**
```bash
echo "deb https://download.opensuse.org/repositories/home:/nicoletta:/myapps/Ubuntu_24.04/ /" | sudo tee /etc/apt/sources.list.d/myapps.list
wget -qO- https://download.opensuse.org/repositories/home:/nicoletta:/myapps/Ubuntu_24.04/Release.key | sudo gpg --dearmor -o /etc/apt/trusted.gpg.d/myapps.gpg
sudo apt update && sudo apt install myapps
```

**Fedora 42:**
```bash
sudo dnf config-manager --add-repo https://download.opensuse.org/repositories/home:/nicoletta:/myapps/Fedora_42/home:nicoletta:myapps.repo
sudo dnf install myapps
```

**openSUSE Tumbleweed:**
```bash
sudo zypper addrepo https://download.opensuse.org/repositories/home:/nicoletta:/myapps/openSUSE_Tumbleweed/home:nicoletta:myapps.repo
sudo zypper refresh && sudo zypper install myapps
```

---

### **AUR-Paket** — Arch Linux ✅

<a href="https://aur.archlinux.org/packages/myapps"><img src="https://img.shields.io/badge/Download-AUR-1793D1?style=for-the-badge&logo=archlinux&logoColor=white" alt="AUR Download"></a>

```bash
yay -S myapps
# oder: paru -S myapps
```

---

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

**Changelog:** https://github.com/nicolettas-muggelbude/myapps/compare/v0.2.4...v0.3.0
