#!/bin/bash
# MyApps DEB-Paket Build-Script
# ⚠️  WARNUNG: Dieses Paket ist NUR für Testing/Development!
# ⚠️  Für Production bitte OBS-Pakete nutzen: https://build.opensuse.org/package/show/home:nicoletta:myapps/myapps

set -e

# Farben für Output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Version aus pyproject.toml lesen oder als Parameter
VERSION=${1:-$(grep '^version = ' pyproject.toml | cut -d'"' -f2)}
PACKAGE_NAME="myapps_${VERSION}_all.deb"

echo -e "${BLUE}=== MyApps DEB-Paket Builder ===${NC}"
echo -e "${YELLOW}⚠️  WARNING: This package is for TESTING/DEVELOPMENT only!${NC}"
echo -e "${YELLOW}⚠️  For production use: https://build.opensuse.org/package/show/home:nicoletta:myapps/myapps${NC}"
echo ""
echo -e "Version: ${GREEN}${VERSION}${NC}"
echo ""

# Cleanup alte Builds
echo -e "${BLUE}[1/7]${NC} Räume alte Builds auf..."
rm -rf debian/
rm -f myapps_*.deb

# Erstelle Verzeichnisstruktur
echo -e "${BLUE}[2/7]${NC} Erstelle Paket-Struktur..."
mkdir -p debian/DEBIAN
mkdir -p debian/usr/bin
mkdir -p debian/usr/share/myapps/vendor
mkdir -p debian/usr/share/applications
mkdir -p debian/usr/share/icons/hicolor/scalable/apps

# Installiere Python-Dependencies in vendor/
echo -e "${BLUE}[3/7]${NC} Installiere Python-Dependencies..."
python3 -m pip install --target=debian/usr/share/myapps/vendor Pillow

# Erstelle control-Datei
echo -e "${BLUE}[4/7]${NC} Erstelle control-Datei..."
cat > debian/DEBIAN/control << EOF
Package: myapps
Version: ${VERSION}
Section: utils
Priority: optional
Architecture: all
Depends: python3 (>= 3.8), python3-gi, python3-gi-cairo, gir1.2-gtk-4.0, gir1.2-adw-1, python3-pil
Recommends: libadwaita-1-0
Maintainer: nicolettas-muggelbude <noreply@github.com>
Description: Tool zum Auflisten und Verwalten installierter Linux-Anwendungen
 MyApps ist ein benutzerfreundliches Tool für Linux, das alle installierten
 Anwendungen übersichtlich darstellt - ohne System-Clutter.
 .
 Features:
  - Multi-Distribution-Support (Debian, Ubuntu, Mint, Arch, Fedora, etc.)
  - Moderne GTK4 + Libadwaita GUI mit nativem Dark Mode
  - Virtual Scrolling für 10.000+ Pakete ohne Performance-Probleme
  - Intelligente Filterung von System-Apps
  - Icons für Apps mit System-Integration
  - Suchfunktion (Name + Beschreibung)
  - Export-Funktionen (TXT, CSV, JSON)
  - Mehrsprachig (Deutsch, Englisch)
 .
 Ab Version 0.2.0 nutzt MyApps GTK4 + Libadwaita für native
 GNOME-Integration und bessere Performance.
Homepage: https://github.com/nicolettas-muggelbude/myapps
EOF

# Erstelle Launcher-Script
echo -e "${BLUE}[5/7]${NC} Erstelle Launcher und Desktop-Datei..."
cat > debian/usr/bin/myapps << 'EOF'
#!/usr/bin/env python3
"""MyApps Launcher"""
import sys
sys.path.insert(0, '/usr/share/myapps/vendor')
sys.path.insert(0, '/usr/share/myapps')

from src.myapps.main import main

if __name__ == '__main__':
    main()
EOF
chmod 755 debian/usr/bin/myapps

# Kopiere .desktop-Datei (oder erstelle sie, falls nicht vorhanden)
if [ -f "io.github.nicolettas-muggelbude.myapps.desktop" ]; then
    cp io.github.nicolettas-muggelbude.myapps.desktop debian/usr/share/applications/
else
    # Fallback: Erstelle Desktop-Datei
    cat > debian/usr/share/applications/io.github.nicolettas-muggelbude.myapps.desktop << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=MyApps
GenericName=Package Manager Overview
GenericName[de]=Paketmanager-Übersicht
Comment=View and manage installed Linux applications
Comment[de]=Installierte Linux-Anwendungen anzeigen und verwalten
Exec=myapps
Icon=io.github.nicolettas-muggelbude.myapps
Terminal=false
Categories=System;PackageManager;GTK;
Keywords=package;apps;software;installer;dpkg;rpm;flatpak;snap;
Keywords[de]=Paket;Apps;Software;Installer;dpkg;rpm;flatpak;snap;
StartupNotify=true
StartupWMClass=io.github.nicolettas-muggelbude.myapps
EOF
fi

# Kopiere Projektdateien
echo -e "${BLUE}[6/7]${NC} Kopiere Projektdateien..."
cp -r src filters assets locales debian/usr/share/myapps/

# Installiere App-Icon (SVG bevorzugt, PNG als Fallback)
if [ -f "assets/icons/io.github.nicolettas-muggelbude.myapps.svg" ]; then
    cp assets/icons/io.github.nicolettas-muggelbude.myapps.svg \
       debian/usr/share/icons/hicolor/scalable/apps/
elif [ -f "assets/icons/default-app.png" ]; then
    # Fallback für ältere Versionen
    mkdir -p debian/usr/share/pixmaps
    cp assets/icons/default-app.png debian/usr/share/pixmaps/myapps.png
fi

# Erstelle postinst-Script (für Icon-Cache und Desktop-Database Update)
cat > debian/DEBIAN/postinst << 'EOF'
#!/bin/bash
set -e

# Icon-Cache aktualisieren
if command -v gtk-update-icon-cache >/dev/null 2>&1; then
    gtk-update-icon-cache -f -t /usr/share/icons/hicolor || true
fi

# Desktop-Database aktualisieren
if command -v update-desktop-database >/dev/null 2>&1; then
    update-desktop-database -q /usr/share/applications || true
fi

exit 0
EOF
chmod 755 debian/DEBIAN/postinst

# Erstelle postrm-Script (Cleanup nach Deinstallation)
cat > debian/DEBIAN/postrm << 'EOF'
#!/bin/bash
set -e

if [ "$1" = "remove" ] || [ "$1" = "purge" ]; then
    # Icon explizit löschen (falls dpkg es nicht entfernt)
    rm -f /usr/share/icons/hicolor/scalable/apps/io.github.nicolettas-muggelbude.myapps.svg || true

    # Leere Icon-Verzeichnisse aufräumen
    rmdir --ignore-fail-on-non-empty /usr/share/icons/hicolor/scalable/apps 2>/dev/null || true
    rmdir --ignore-fail-on-non-empty /usr/share/icons/hicolor/scalable 2>/dev/null || true

    # Icon-Cache aktualisieren
    if command -v gtk-update-icon-cache >/dev/null 2>&1; then
        gtk-update-icon-cache -f -t /usr/share/icons/hicolor || true
    fi

    # Desktop-Database aktualisieren
    if command -v update-desktop-database >/dev/null 2>&1; then
        update-desktop-database -q /usr/share/applications || true
    fi
fi

exit 0
EOF
chmod 755 debian/DEBIAN/postrm

# Baue DEB-Paket
echo -e "${BLUE}[7/7]${NC} Baue DEB-Paket..."
dpkg-deb --build debian "${PACKAGE_NAME}"

# Zeige Ergebnis
echo ""
echo -e "${GREEN}✅ DEB-Paket erfolgreich erstellt!${NC}"
echo ""
ls -lh "${PACKAGE_NAME}"
echo ""
dpkg-deb --info "${PACKAGE_NAME}" | head -20

echo ""
echo -e "${GREEN}Installation:${NC}"
echo "  sudo dpkg -i ${PACKAGE_NAME}"
echo "  sudo apt-get install -f  # Falls Dependencies fehlen"
echo ""
echo -e "${GREEN}Deinstallation:${NC}"
echo "  sudo apt-get remove myapps"
