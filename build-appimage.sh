#!/bin/bash
# MyApps AppImage Build-Script

set -e

# Farben
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

# Version
VERSION=${1:-$(grep '^version = ' pyproject.toml | cut -d'"' -f2)}
APPIMAGE_NAME="MyApps-${VERSION}-x86_64.AppImage"

echo -e "${BLUE}=== MyApps AppImage Builder ===${NC}"
echo -e "Version: ${GREEN}${VERSION}${NC}"
echo ""

# Cleanup
echo -e "${BLUE}[1/7]${NC} Räume auf..."
rm -rf AppDir/
rm -f MyApps-*.AppImage

# Erstelle AppDir-Struktur
echo -e "${BLUE}[2/7]${NC} Erstelle AppDir-Struktur..."
mkdir -p AppDir/usr/bin
mkdir -p AppDir/usr/share/myapps
mkdir -p AppDir/usr/share/applications
mkdir -p AppDir/usr/share/icons/hicolor/256x256/apps

# Kopiere Projektdateien
echo -e "${BLUE}[3/7]${NC} Kopiere Projektdateien..."
cp -r src filters assets locales AppDir/usr/share/myapps/

# Kopiere Icon
cp assets/icons/default-app.png AppDir/usr/share/icons/hicolor/256x256/apps/myapps.png
cp assets/icons/default-app.png AppDir/myapps.png  # Root-Icon für AppImage

# Erstelle .desktop-Datei
echo -e "${BLUE}[4/7]${NC} Erstelle .desktop-Datei..."
cat > AppDir/myapps.desktop << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=MyApps
GenericName=Paketmanager-Übersicht
Comment=Installierte Anwendungen anzeigen und verwalten
Exec=myapps
Icon=myapps
Terminal=false
Categories=System;PackageManager;
Keywords=package;apps;software;installer;
StartupNotify=true
EOF

cp AppDir/myapps.desktop AppDir/usr/share/applications/

# Installiere Python-Dependencies in AppDir
echo -e "${BLUE}[5/7]${NC} Installiere Python-Dependencies..."
# Nur ttkbootstrap bündeln (Pure Python) ohne Dependencies
# Pillow hat native Extensions und muss auf dem System installiert sein
python3 -m pip install --target=AppDir/usr/share/myapps/vendor --no-deps ttkbootstrap

# Erstelle AppRun-Script
echo -e "${BLUE}[6/7]${NC} Erstelle AppRun-Script..."
cat > AppDir/AppRun << 'EOF'
#!/bin/bash
# MyApps AppRun

HERE="$(dirname "$(readlink -f "${0}")")"
export PYTHONPATH="${HERE}/usr/share/myapps:${HERE}/usr/share/myapps/vendor:${PYTHONPATH}"

# Prüfe Python3
if ! command -v python3 &> /dev/null; then
    echo "Fehler: Python 3 ist nicht installiert!"
    exit 1
fi

# Prüfe python3-tk
if ! python3 -c "import tkinter" 2>/dev/null; then
    echo "Fehler: python3-tk ist nicht installiert!"
    echo "Bitte installieren:"
    echo "  Debian/Ubuntu: sudo apt install python3-tk python3-pil"
    echo "  Arch: sudo pacman -S tk python-pillow"
    echo "  Fedora: sudo dnf install python3-tkinter python3-pillow"
    exit 1
fi

# Prüfe python3-pil (Pillow)
if ! python3 -c "from PIL import Image" 2>/dev/null; then
    echo "Fehler: python3-pil (Pillow) ist nicht installiert!"
    echo "Bitte installieren:"
    echo "  Debian/Ubuntu: sudo apt install python3-pil python3-pil.imagetk"
    echo "  Arch: sudo pacman -S python-pillow"
    echo "  Fedora: sudo dnf install python3-pillow python3-pillow-tk"
    exit 1
fi

# Starte MyApps
cd "${HERE}/usr/share/myapps"
exec python3 -m src.myapps.main "$@"
EOF

chmod +x AppDir/AppRun

# Baue AppImage
echo -e "${BLUE}[7/7]${NC} Baue AppImage..."
if [ -d "appimagetool-extracted" ]; then
    # Verwende extrahiertes appimagetool (für WSL/Systeme ohne FUSE)
    ARCH=x86_64 ./appimagetool-extracted/AppRun AppDir "${APPIMAGE_NAME}"
else
    # Verwende normales appimagetool
    ARCH=x86_64 ./appimagetool AppDir "${APPIMAGE_NAME}"
fi

# Ergebnis
echo ""
echo -e "${GREEN}✅ AppImage erfolgreich erstellt!${NC}"
echo ""
ls -lh "${APPIMAGE_NAME}"
echo ""
echo -e "${GREEN}Verwendung:${NC}"
echo "  chmod +x ${APPIMAGE_NAME}"
echo "  ./${APPIMAGE_NAME}"
echo ""
echo -e "${GREEN}Hinweis:${NC}"
echo "  python3, python3-tk und python3-pil müssen im System installiert sein!"
echo ""
echo -e "${GREEN}Installation der Dependencies:${NC}"
echo "  Debian/Ubuntu: sudo apt install python3 python3-tk python3-pil python3-pil.imagetk"
echo "  Arch: sudo pacman -S python tk python-pillow"
echo "  Fedora: sudo dnf install python3 python3-tkinter python3-pillow python3-pillow-tk"
