<div align="center">
  <img src="assets/icons/io.github.nicolettas-muggelbude.myapps.svg" width="128" alt="MyApps Logo">

  # MyApps

  > Tool for listing and managing installed Linux applications

  [![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
  [![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
  [![Version](https://img.shields.io/badge/version-0.3.0-green.svg)](https://github.com/nicolettas-muggelbude/myapps/releases)
  [![Status](https://img.shields.io/badge/status-beta-orange.svg)](https://github.com/nicolettas-muggelbude/myapps)
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

🔍 **Search & Filter**
- Scope dropdown: "User Apps only" or "All Packages"
- Live search in name + description (5+ characters)
- Automatic detection of system apps
- Distribution-specific filters
- Add custom filters (right-click)

📊 **Package Information**
- Installed size (dpkg, rpm, pacman, flatpak, snap)
- Installation date (dpkg, rpm, pacman, flatpak, snap)
- Sort function: Name, Size, Date (ascending and descending)

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

**MyApps requires GTK4 + Libadwaita as system packages:**

```bash
# Debian 12 / Linux Mint
sudo apt install python3-gi python3-gi-cairo gir1.2-gtk-4.0 gir1.2-adw-1 python3-pil

# Ubuntu 24.04 LTS (python3-pil was renamed to python3-pillow)
sudo apt install python3-gi python3-gi-cairo gir1.2-gtk-4.0 gir1.2-adw-1 python3-pillow

# Arch/Manjaro
sudo pacman -S python-gobject gtk4 libadwaita python-pillow

# Fedora/RHEL/CentOS
sudo dnf install python3-gobject gtk4 libadwaita python3-pillow

# openSUSE
sudo zypper install python3-gobject python3-gobject-Gdk typelib-1_0-Gtk-4_0 typelib-1_0-Adw-1 python3-Pillow
```

> **Ubuntu 24.04 note:** The package `python3-pil` no longer exists — use `python3-pillow` instead.

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

### From GitHub DEB Package (⚠️ Testing Only)

**⚠️ WARNING:** This package is for Testing/Development only!

**For production use OBS packages** (see above).

```bash
# Install after download
sudo dpkg -i myapps_0.3.0_all.deb

# If dependencies are missing
sudo apt-get install -f

# Launch
myapps
```

### ~~As Flatpak~~ (Not Available)

**Flathub rejected MyApps** due to required `/var/lib` access for package manager databases.

**Alternative:** Use **OBS packages** (see above) - native system integration without sandbox restrictions.

### ~~As AppImage~~ (discontinued since v0.2.0)

AppImage is no longer offered since v0.2.0, as GTK4 system dependencies are difficult to bundle.

### From Source (Development)

```bash
# Clone repository
git clone https://github.com/nicolettas-muggelbude/myapps.git
cd myapps

# 1. Install system packages (REQUIRED - GTK4 cannot be built via pip!)
# Ubuntu 24.04:
sudo apt install python3-gi python3-gi-cairo gir1.2-gtk-4.0 gir1.2-adw-1 python3-pillow
# Ubuntu 22.04 / Debian 12:
sudo apt install python3-gi python3-gi-cairo gir1.2-gtk-4.0 gir1.2-adw-1 python3-pil

# 2. Create venv WITH --system-site-packages (so python3-gi is accessible)
python3 -m venv --system-site-packages venv
source venv/bin/activate

# 3. Install only Pillow via pip (PyGObject comes from system)
pip install -e . --no-deps
pip install Pillow

# 4. Launch app
python3 -m myapps.main
# or simply:
./run-dev.sh
```

> **Important:** `pip install -e .` **without** `--no-deps` will fail because pip tries to compile PyGObject — which requires `pkg-config` + `libcairo2-dev`. GTK bindings must come as system packages.

## Building Packages

### Build DEB Package

```bash
# Run build script
./build-deb.sh

# Optional: Specify version
./build-deb.sh 0.3.0

# Install
sudo dpkg -i myapps_0.3.0_all.deb
```

## Usage

1. **Launch app**: Open MyApps from application menu or terminal
2. **Load packages**: All user apps are loaded automatically on start
3. **Change scope**: Dropdown next to search → "User Apps only" or "All Packages"
4. **Search**: Enter at least 5 characters for live search
5. **Sort**: Dropdown in the navigation bar → by Name, Size or Date
6. **Switch view**: Buttons at top → List or Table
7. **Export**: Click "Export" and choose format (TXT/CSV/JSON)
8. **Filter**: Right-click on a package → "Mark as System App"

## Supported Package Managers

| Package Manager | Distributions | Size | Date |
|-----------------|---------------|------|------|
| dpkg | Debian, Ubuntu, Mint | ✅ | ✅ |
| pacman | Arch, Manjaro | ✅ | ✅ |
| rpm/dnf | Fedora, RHEL, CentOS | ✅ | ✅ |
| rpm/zypper | openSUSE | ✅ | ✅ |
| flatpak | All | ✅ | ✅ |
| snap | All | ✅ | ✅ |
| eopkg | Solus | — | — |

## Roadmap

### v0.1.x (Stable - tkinter) ✅
- [x] Multi-distribution support
- [x] Modern GUI with Dark Mode
- [x] Export functions
- [x] Multilingual (DE/EN)

### v0.2.x (GTK4 Migration) ✅
- [x] GTK4 + Libadwaita GUI
- [x] Virtual scrolling
- [x] Search function
- [x] OBS packages (11 distributions)
- [x] AUR package
- [x] Performance optimizations

### v0.3.0 (Current) ✅
- [x] Scope dropdown: User Apps vs. All Packages
- [x] Installed size (dpkg, rpm, pacman, flatpak, snap)
- [x] Installation date (dpkg, rpm, pacman, flatpak, snap)
- [x] Sort function (Name, Size, Date)
- [x] Minimum characters for search (5 characters)

### v0.3.1 (Planned)
- [ ] Desktop Apps view (.desktop files)

### v0.4.0 (Planned)
- [ ] Check update status
- [ ] Update notifications

### v1.0.0 (Stable)
- [ ] Community testing complete
- [ ] Stable release

### v2.0.0 (Future)
- [ ] Uninstall function

## FAQ

**Q: Why aren't some apps shown?**
A: They were probably filtered as system apps. Switch the scope dropdown to "All Packages" or customize filters in `~/.config/myapps/user-filters.json`.

**Q: `pip install -e .` fails with a pycairo error?**
A: GTK bindings cannot be compiled via pip. Install `python3-gi` as a system package and use `pip install -e . --no-deps`. See "From Source" section above.

**Q: Ubuntu 24.04: `python3-pil` not found?**
A: In Ubuntu 24.04 the package was renamed to `python3-pillow`. Use `sudo apt install python3-pillow`.

**Q: Is my distribution supported?**
A: See "Supported Package Managers" above. More distributions can be added.

**Q: Is MyApps safe?**
A: MyApps is Open Source (GPLv3) and only performs read operations (no `sudo` needed).

## Contributing

Contributions are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## License

MyApps is licensed under the [GNU General Public License v3.0](LICENSE).

## Credits

- Developed for the [Linux Guides DE Community](https://t.me/LinuxGuidesDECommunity)
- Icons from system themes
- UI based on [GTK4](https://gtk.org/) and [Libadwaita](https://gnome.pages.gitlab.gnome.org/libadwaita/)

## 💝 Support This Project

If MyApps helps you, consider supporting the development:

[![Donate via PayPal](https://img.shields.io/badge/PayPal-Donate-00457C?style=for-the-badge&logo=paypal&logoColor=white)](https://www.paypal.com/ncp/payment/UYJ73YNEZ3KHL)

**Donations go to:** PC-Wittfoot UG (donation manager)
**Used for:** Server costs, hardware, developer time for MyApps

**Note:** Development is done by the Linux Guides DE Community (Open Source).
PC-Wittfoot UG only manages donations, but is NOT the developer.

**Legal:**
[Impressum](https://nicolettas-muggelbude.github.io/myapps/impressum) | [Privacy Policy](https://nicolettas-muggelbude.github.io/myapps/datenschutz)

## Support

- 🐛 [Report Bug](https://github.com/nicolettas-muggelbude/myapps/issues)
- 💡 [Suggest Feature](https://github.com/nicolettas-muggelbude/myapps/issues)
- 💬 [Community Chat](https://t.me/LinuxGuidesDECommunity)

---

Made with ❤️ for the Linux Community
