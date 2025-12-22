#!/bin/bash

# Prüfe, ob Python 3 installiert ist
if ! command -v python3 &> /dev/null; then
    echo "Fehler: Python 3 ist nicht installiert. Bitte installiere Python 3."
    exit 1
fi

# Prüfe, ob python3-tk installiert ist
if ! dpkg -s python3-tk &> /dev/null; then
    echo "python3-tk ist nicht installiert. Installiere es jetzt..."
    sudo apt update
    sudo apt install -y python3-tk
    if [ $? -ne 0 ]; then
        echo "Fehler: Installation von python3-tk fehlgeschlagen."
        exit 1
    fi
fi

# Pfad zum Python-Skript (relativ oder absolut)
SCRIPT_PATH="app_lister_filtered.py"

# Prüfe, ob das Python-Skript existiert
if [ ! -f "$SCRIPT_PATH" ]; then
    echo "Fehler: Das Python-Skript '$SCRIPT_PATH' wurde nicht gefunden."
    exit 1
fi

# Führe das Python-Skript aus
python3 "$SCRIPT_PATH"
