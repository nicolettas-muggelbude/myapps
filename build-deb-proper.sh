#!/bin/bash
# MyApps Proper Debian Package Builder
# Verwendet debhelper für standards-konformes Packaging

set -e

# Farben
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

# Version
VERSION=$(grep '^version = ' pyproject.toml | cut -d'"' -f2)

echo -e "${BLUE}=== MyApps Proper DEB-Paket Builder ===${NC}"
echo -e "Version: ${GREEN}${VERSION}${NC}"
echo ""

# Prüfe Dependencies
echo -e "${BLUE}[1/3]${NC} Prüfe Build-Dependencies..."
if ! command -v debuild &> /dev/null; then
    echo -e "${RED}Fehler: debuild nicht gefunden!${NC}"
    echo "Installiere: sudo apt install devscripts debhelper dh-python"
    exit 1
fi

# Cleanup
echo -e "${BLUE}[2/3]${NC} Räume auf..."
debclean 2>/dev/null || true

# Baue Paket
echo -e "${BLUE}[3/3]${NC} Baue DEB-Paket..."
debuild -us -uc -b

# Ergebnis
echo ""
echo -e "${GREEN}✅ DEB-Paket erfolgreich erstellt!${NC}"
echo ""
ls -lh ../myapps_${VERSION}_*.deb 2>/dev/null || ls -lh ../myapps_*.deb
echo ""
echo -e "${GREEN}Installation:${NC}"
echo "  sudo dpkg -i ../myapps_${VERSION}_all.deb"
echo "  sudo apt-get install -f  # Falls Dependencies fehlen"
