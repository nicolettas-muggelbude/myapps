#!/usr/bin/env python3
"""
MyApps - Haupteinstiegspunkt
Tool zum Auflisten und Verwalten installierter Linux-Anwendungen
"""

import sys
import logging
from pathlib import Path

# Setze Logging auf
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def main():
    """Hauptfunktion"""
    try:
        # Bestimme Basis-Verzeichnis (wo sich das Projekt befindet)
        # Im installierten Zustand: /usr/share/myapps oder ähnlich
        # Im Development: projekte/app_lister
        if getattr(sys, 'frozen', False):
            # PyInstaller/Frozen
            base_dir = Path(sys._MEIPASS)
        else:
            # Development oder installiert
            base_dir = Path(__file__).parent.parent.parent

        logger.info(f"MyApps startet...")
        logger.info(f"Basis-Verzeichnis: {base_dir}")

        # Importiere GUI-Modul
        from .gui_gtk import MyAppsGUI  # GTK4 GUI (v0.2.0+)
        from .i18n import init_i18n

        # Initialisiere i18n
        locale_dir = base_dir / "locales"
        _ = init_i18n(str(locale_dir))

        # Erstelle und starte GTK4 App
        app = MyAppsGUI(str(base_dir))
        app.run(sys.argv)

    except KeyboardInterrupt:
        logger.info("MyApps durch Benutzer beendet")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Kritischer Fehler: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
