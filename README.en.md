<div align="center">
  <img src="assets/icons/io.github.nicolettas-muggelbude.myapps.svg" width="128" alt="MyApps Logo">

  # MyApps

  > Tool for listing and managing installed Linux applications

  [![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
  [![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
  [![Status](https://img.shields.io/badge/status-beta-green.svg)](https://github.com/nicolettas-muggelbude/myapps)
</div>

**English** | [Deutsch](README.md)

## About MyApps

MyApps is a user-friendly tool for Linux that displays all installed applications in a clean interface - without system clutter. It was developed at the request of the [Linux Guides DE Community](https://t.me/LinuxGuidesDECommunity).

### Features

✨ **Multi-Distribution Support**
- Debian, Ubuntu, Linux Mint
- Arch Linux, Manjaro
- Fedora, RHEL, CentOS
- Solus
- openSUSE
- Snap & Flatpak (cross-distribution)

🎨 **Modern Interface**
- Native GTK4 + Libadwaita integration
- Dark Mode (follows system theme)
- Virtual scrolling (10,000+ packages no problem)
- Table view & List view
- Switchable with one click
- Search function (name + description)

🔍 **Smart Filtering**
- Automatic detection of system apps
- Distribution-specific filters
- Add custom filters (right-click)
- Community-extensible

📤 **Export Functions**
- Text (TXT)
- CSV (for Excel/LibreOffice)
- JSON (for scripts)

🌍 **Multilingual**
- German
- English
- More languages welcome!

## Screenshots

### Main Window (List View)
<img src="docs/screenshots/main-window.png" width="800" alt="MyApps Main Window">

### Table View
<img src="docs/screenshots/table-view.png" width="800" alt="MyApps Table View">

### Search Function
<img src="docs/screenshots/search-demo.png" width="800" alt="MyApps Search Function">

### Dark Mode
<img src="docs/screenshots/dark-mode.png" width="800" alt="MyApps Dark Mode">

## Installation

### Prerequisites

**Since version 0.2.0, MyApps requires GTK4 + Libadwaita:**

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

### From OBS (Recommended - Debian/Ubuntu/Fedora/openSUSE)

**📦 Professional packages for 11 distributions via openSUSE Build Service:**

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

**Additional supported distributions:**
- Debian 13 (Trixie)
- Ubuntu 22.04 LTS, 25.10
- Fedora 42, 43
- openSUSE Leap 16, Slowroll

[View all OBS packages →](https://software.opensuse.org//download.html?project=home%3Anicoletta%3Amyapps&package=myapps)

---

### From AUR (Recommended - Arch Linux)

[![AUR Version](https://img.shields.io/badge/AUR-myapps-1793D1?style=for-the-badge&logo=archlinux&logoColor=white)](https://aur.archlinux.org/packages/myapps)

```bash
# With AUR helper (e.g. yay)
yay -S myapps

# Or with paru
paru -S myapps

# Manual installation
git clone https://aur.archlinux.org/myapps.git
cd myapps
makepkg -si
```

### From OBS (Fedora/openSUSE/more distributions)

**MyApps is available via openSUSE Build Service for 11 distributions:**

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

# Fedora 42
sudo dnf config-manager --add-repo https://download.opensuse.org/repositories/home:/nicoletta:/myapps/Fedora_42/home:nicoletta:myapps.repo
sudo dnf install myapps
```

**openSUSE:**
```bash
# openSUSE Tumbleweed
sudo zypper addrepo https://download.opensuse.org/repositories/home:/nicoletta:/myapps/openSUSE_Tumbleweed/home:nicoletta:myapps.repo
sudo zypper refresh && sudo zypper install myapps

# openSUSE Leap 16
sudo zypper addrepo https://download.opensuse.org/repositories/home:/nicoletta:/myapps/openSUSE_Leap_16/home:nicoletta:myapps.repo
sudo zypper refresh && sudo zypper install myapps
```

**Additional supported distributions:**
- Debian 13 (Trixie)
- Ubuntu 22.04 LTS, 25.10
- Fedora 43
- openSUSE Slowroll

[View all OBS packages →](https://software.opensuse.org//download.html?project=home%3Anicoletta%3Amyapps&package=myapps)

### ~~As Flatpak~~ (Not Available)

**Flathub rejected MyApps** due to required `/var/lib` access for package manager databases.

**Alternative:** Use **OBS packages** (see above) - they provide native system integration without sandbox restrictions.

### ~~As AppImage~~ (discontinued since v0.2.0)

**Reason:** GTK4 dependencies are difficult to bundle in AppImage. Use DEB or Flatpak instead.

### From Source (Development)

```bash
# Clone repository
git clone https://github.com/nicolettas-muggelbude/myapps.git
cd myapps

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Launch app
python3 -m src.myapps.main
```

## Building Packages

### Build DEB Package

```bash
# Run build script
./build-deb.sh

# Optional: Specify version
./build-deb.sh 0.1.0

# Install
sudo dpkg -i myapps_0.1.0_all.deb
```

### Build AppImage

```bash
# Download appimagetool (one-time)
wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage
chmod +x appimagetool-x86_64.AppImage
mv appimagetool-x86_64.AppImage appimagetool

# For WSL/systems without FUSE: Extract tool
./appimagetool --appimage-extract
mv squashfs-root appimagetool-extracted

# Run build script
./build-appimage.sh

# Optional: Specify version
./build-appimage.sh 0.1.0

# Execute
chmod +x MyApps-0.1.0-x86_64.AppImage
./MyApps-0.1.0-x86_64.AppImage
```

## Usage

1. **Launch app**: Open MyApps from application menu or terminal
2. **Load packages**: All packages are loaded automatically on start
3. **Switch view**: Click "Switch View" for Table ↔ List
4. **Export**: Click "Export" and choose format
5. **Filter**: Right-click on a package → "Mark as System App"

## Supported Package Managers

| Package Manager | Distributions | Status |
|-----------------|---------------|--------|
| dpkg | Debian, Ubuntu, Mint | ✅ |
| pacman | Arch, Manjaro | ✅ |
| rpm/dnf | Fedora, RHEL, CentOS | ✅ |
| rpm/zypper | openSUSE | ✅ |
| eopkg | Solus | ✅ |
| snap | All | ✅ |
| flatpak | All | ✅ |

## Contributing

Contributions are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

### Suggest Filter Keywords

Found system packages that aren't filtered? Open an [Issue](https://github.com/nicolettas-muggelbude/myapps/issues)!

### Testers Wanted!

We need community testers for various distributions:
- Debian
- Ubuntu & variants
- Arch Linux & derivatives
- Fedora
- Solus
- openSUSE

## Roadmap

### v0.1.0 (Current - Alpha) ⏳
- [x] Multi-distribution support
- [x] Modern GUI with Dark Mode
- [x] Icons with fallback
- [x] Export functions
- [x] Multilingual (DE/EN)
- [x] Distribution-specific filters
- [x] User filters

### v0.2.0 (Planned)
- [ ] Show size information
- [ ] Performance optimizations

### v0.3.0 (Planned)
- [ ] Show installation date
- [ ] Sorting functions

### v0.4.0 (Planned)
- [ ] Check update status
- [ ] Update notifications

### v1.0.0 (Stable)
- [ ] Community testing completed
- [ ] Bug fixes
- [ ] Stable release

### v2.0.0 (Future)
- [ ] Uninstall function
- [ ] Package details view

## FAQ

**Q: Why aren't some apps shown?**
A: They were probably filtered as system apps. You can customize filters in `~/.config/myapps/user-filters.json`.

**Q: Is my distribution supported?**
A: See "Supported Package Managers" above. More distributions can be added.

**Q: Can I contribute to the filter list?**
A: Yes! Open an issue with your filter suggestions.

**Q: Is MyApps safe?**
A: MyApps is Open Source (GPLv3) and only performs read operations (no `sudo` needed). The code can be reviewed.

## License

MyApps is licensed under the [GNU General Public License v3.0](LICENSE).

## Credits

- Developed for the [Linux Guides DE Community](https://t.me/LinuxGuidesDECommunity)
- Icons from system themes
- UI based on [GTK4](https://gtk.org/) and [Libadwaita](https://gnome.pages.gitlab.gnome.org/libadwaita/)

## Support

- 🐛 [Report Bug](https://github.com/nicolettas-muggelbude/myapps/issues)
- 💡 [Suggest Feature](https://github.com/nicolettas-muggelbude/myapps/issues)
- 💬 [Community Chat](https://t.me/LinuxGuidesDECommunity)

## 💝 Support This Project

If MyApps helps you, consider supporting the development:

[![Donate via PayPal](https://img.shields.io/badge/PayPal-Donate-00457C?style=for-the-badge&logo=paypal&logoColor=white)](https://www.paypal.com/ncp/payment/UYJ73YNEZ3KHL)

**Donations go to:** PC-Wittfoot UG (donation manager)
**Used for:** Server costs, hardware, developer time for MyApps

**Note:** Development is done by the Linux Guides DE Community (Open Source).
PC-Wittfoot UG only manages donations, but is NOT the developer.

**Legal:**
[Impressum](https://nicolettas-muggelbude.github.io/myapps/impressum) | [Privacy Policy](https://nicolettas-muggelbude.github.io/myapps/datenschutz)

---

Made with ❤️ for the Linux Community
