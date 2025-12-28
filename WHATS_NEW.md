# MyApps - What's New

Dieses Dokument enthält die Changelog-Informationen für den About-Dialog.

## v0.2.3
- Fix: Version 0.0.0 in System-Installationen behoben
- Fix: Changelog nicht verfügbar in System-Installationen behoben
- pyproject.toml und WHATS_NEW.md werden jetzt installiert
- About-Dialog zeigt korrekte Version und Features

## v0.2.2
- Fix: NameError auf Systemen ohne tkinter (OBS-Pakete)
- Fix: ImageTk Type Hints als String-Literale
- Betrifft alle 11 OBS-Distributionen

## v0.2.1
- Fix: Basis-Verzeichnis-Erkennung für /usr/share/myapps
- Fix: GTK4 SearchEntry placeholder Kompatibilität
- Fix: AUR PKGBUILD Fallback für alte Dateinamen
- Feature: Automatische Versionserkennung aus pyproject.toml

## v0.2.0
- GTK4 + Libadwaita GUI (kompletter Rewrite)
- Native GNOME Integration mit Dark Mode
- Searchbar mit Live-Suche (Name + Beschreibung)
- Pagination (100 Apps pro Seite)
- Verbesserte Performance
- Export respektiert Suchergebnisse
- Deutsche Beschreibungen in Listenansicht

## v0.1.3
- Bug-Fixes für tkinter GUI
- Verbessertes Icon-Handling

## v0.1.0
- Erste stabile Version
- Multi-Distribution Support
- ttkbootstrap GUI
- Export-Funktionen (TXT, CSV, JSON)
