# MyApps 📦

> Tool for listing and managing installed Linux applications

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
[![Status](https://img.shields.io/badge/status-alpha-orange.svg)](https://github.com/YOURUSERNAME/myapps)

**English** | [Deutsch](README.md)

## About MyApps

MyApps is a user-friendly tool for Linux that displays all installed applications in a clean interface - without system clutter. It was developed at the request of the [Linux Guides DE Community](https://t.me/YOURGROUP).

### Features

✨ **Multi-Distribution Support**
- Debian, Ubuntu, Linux Mint
- Arch Linux, Manjaro
- Fedora, RHEL, CentOS
- Solus
- openSUSE
- Snap & Flatpak (cross-distribution)

🎨 **Modern Interface**
- Dark Mode (ttkbootstrap)
- Table view (file manager style)
- List view (with icons)
- Switchable with one click

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

*Coming soon - Screenshots will be added after the first release*

## Installation

### From DEB Package (Debian/Ubuntu/Mint)

```bash
# Download DEB package (will be provided soon)
sudo dpkg -i myapps_0.1.0_all.deb

# Launch
myapps
```

### As AppImage (all distributions)

```bash
# Download AppImage (will be provided soon)
chmod +x MyApps-0.1.0-x86_64.AppImage

# Launch
./MyApps-0.1.0-x86_64.AppImage
```

### From Source (Development)

```bash
# Clone repository
git clone https://github.com/YOURUSERNAME/myapps.git
cd myapps

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Launch app
python3 -m myapps.main
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

Found system packages that aren't filtered? Open an [Issue](https://github.com/YOURUSERNAME/myapps/issues)!

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

- Developed for the [Linux Guides DE Community](https://t.me/YOURGROUP)
- Icons from system themes
- UI based on [ttkbootstrap](https://github.com/israel-dryer/ttkbootstrap)

## Support

- 🐛 [Report Bug](https://github.com/YOURUSERNAME/myapps/issues)
- 💡 [Suggest Feature](https://github.com/YOURUSERNAME/myapps/issues)
- 💬 [Community Chat](https://t.me/YOURGROUP)

---

Made with ❤️ for the Linux Community
