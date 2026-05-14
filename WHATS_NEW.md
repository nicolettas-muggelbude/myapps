# MyApps - What's New

Dieses Dokument enthält die Changelog-Informationen für den About-Dialog.

## v1.0.1
- Fix: Auto-Updater führt apt update vor Install aus (verhindert Endlosschleife)
- Fix: Korrekte Erkennung ob apt wirklich aktualisiert hat

## v1.0.0
- Stable Release nach Community-Testing
- Feature: UPDATE-Badge neben App-Namen in Liste und Tabelle
- Feature: apt-get update via pkexec vor dem Paket-Update-Check (immer aktueller Cache)
- Fix: Update-Meldungen klarer formuliert ("Paket-Updates verfügbar")

## v0.4.1
- Feature: Update-Status — Icon zeigt in Liste und Tabelle welche Pakete ein Update haben
- Feature: Desktop-Benachrichtigungen — notify-send wenn Updates verfügbar (opt-in, Standard: aktiv)
- Feature: Auto-Updater — MyApps aktualisiert sich selbst via pkexec (apt/dnf/zypper)
- Fix: Benachrichtigungs-Toggle im Menü, gespeichert in ~/.config/myapps/settings.json

## v0.4.0
- Performance: Virtual Scrolling — keine Pagination mehr, alle Apps in einer Liste
- GTK4 rendert nur sichtbare Elemente (schnell auch bei 2000+ Paketen)
- Feature: Update-Benachrichtigung — neues Banner wenn neue Version verfügbar
- Fix: Sort-Bar ersetzt Pagination-Bar (übersichtlicher)

## v0.3.1
- Feature: Desktop-Apps-Ansicht — zeigt installierte .desktop-Anwendungen (Issue #4)
- Neue Registerkarte "Desktop" neben Liste und Tabelle
- Erkennt Apps aus /usr/share/applications, ~/.local/share/applications, Flatpak, Snap
- Lokalisierte App-Namen und Beschreibungen (Name[de], Comment[de])
- Icons aus .desktop Icon=-Feld, 48px Darstellung
- Suche und Sortierung funktionieren auch in der Desktop-Ansicht

## v0.3.0
- Feature: Sortierfunktion — Name, Größe, Installationsdatum (Issue #11)
- Feature: Scope-Dropdown "Nur User-Apps" / "Alle Pakete" (Issue #16)
- Feature: Mindestens 5 Zeichen für Suche (schränkt Ergebnisse ein)
- Feature: Installierte Größe angezeigt in Liste und Tabelle (Issue #5)
- Feature: Installationsdatum angezeigt in Liste und Tabelle (Issue #10)
- Größen-Unterstützung: dpkg, rpm, pacman, flatpak, snap
- Datums-Unterstützung: dpkg (dpkg.log), rpm (%{INSTALLTIME}), pacman (pacman -Qi), flatpak/snap (Filesystem)
- Suche durchsucht jetzt optional alle installierten Pakete (~2000+)
- Statusbar zeigt Gesamt-Paketanzahl beim Start

## v0.2.4
- Performance: Icon-Caching implementiert (Icons werden nur einmal geladen)
- Performance: Sortierung optimiert (nur einmal nach Filterung)
- Fix: Memory Leak bei vielen Seitenwechseln behoben
- Fix: Export-Format-Bug behoben (CSV/JSON funktionieren korrekt)
- Seitenwechsel deutlich schneller und flüssiger

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
