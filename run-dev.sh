#!/bin/bash
# MyApps Development Launcher
# Erstellt/aktiviert venv mit System-Site-Packages (für python3-gi)
# und startet die App direkt aus dem Quellcode.

set -e

GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Prüfe ob System-Abhängigkeiten vorhanden sind
if ! python3 -c "import gi" 2>/dev/null; then
    echo -e "${RED}Fehler: python3-gi nicht gefunden!${NC}"
    echo ""
    echo "Bitte System-Pakete installieren:"
    echo -e "  ${YELLOW}sudo apt install python3-gi python3-gi-cairo gir1.2-gtk-4.0 gir1.2-adw-1 python3-pillow${NC}"
    exit 1
fi

# venv mit --system-site-packages (damit python3-gi verfügbar ist)
if [ ! -d "venv" ]; then
    echo -e "${BLUE}Erstelle venv (mit System-Site-Packages)...${NC}"
    python3 -m venv --system-site-packages venv
    source venv/bin/activate
    echo -e "${BLUE}Installiere Python-Dependencies...${NC}"
    pip install -e . --no-deps  # --no-deps: PyGObject kommt vom System
    pip install Pillow
else
    source venv/bin/activate
fi

echo -e "${GREEN}Starte MyApps...${NC}"
python3 -m myapps.main
