# Beiträge zu MyApps

Vielen Dank für dein Interesse an MyApps! Wir freuen uns über Beiträge aus der Community.

## Wie kann ich beitragen?

### Filter-Keywords vorschlagen

Wenn du System-Pakete findest, die nicht gefiltert werden sollten, kannst du neue Filter-Keywords vorschlagen:

1. Öffne ein [Issue](https://github.com/nicolettas-muggelbude/myapps/issues/new)
2. Verwende den Titel: "Filter-Vorschlag: [Paketname]"
3. Gib folgende Informationen an:
   - Paketname
   - Distribution (z.B. Ubuntu 22.04)
   - Warum es ein System-Paket ist
   - Vorgeschlagenes Filter-Keyword

### Bugs melden

1. Prüfe ob der Bug bereits gemeldet wurde
2. Öffne ein neues Issue mit:
   - Klarer Beschreibung des Problems
   - Schritte zur Reproduktion
   - Erwartetes vs. tatsächliches Verhalten
   - System-Informationen (Distribution, Version)
   - Log-Ausgaben (falls vorhanden)

### Features vorschlagen

1. Öffne ein Issue mit dem Label "enhancement"
2. Beschreibe das gewünschte Feature
3. Erkläre den Anwendungsfall
4. Wir diskutieren die Machbarkeit

### Code beitragen

1. Fork das Repository
2. Erstelle einen Feature-Branch (`git checkout -b feature/MeinFeature`)
3. Committe deine Änderungen (`git commit -m 'Füge MeinFeature hinzu'`)
4. Push zum Branch (`git push origin feature/MeinFeature`)
5. Öffne einen Pull Request

## Entwicklungsumgebung einrichten

```bash
# Repository klonen
git clone https://github.com/nicolettas-muggelbude/myapps.git
cd myapps

# Virtual Environment erstellen
python3 -m venv venv
source venv/bin/activate

# Dependencies installieren
pip install -r requirements.txt

# App starten
python3 -m src.myapps.main
```

## Pakete bauen und testen

Wenn du Änderungen an der Paketierung vornimmst, kannst du die Pakete lokal bauen:

### DEB-Paket

```bash
# DEB bauen
./build-deb.sh

# Installieren und testen
sudo dpkg -i myapps_0.1.0_all.deb
myapps

# Deinstallieren
sudo dpkg -r myapps
```

### AppImage

```bash
# appimagetool herunterladen (einmalig)
wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage
chmod +x appimagetool-x86_64.AppImage
mv appimagetool-x86_64.AppImage appimagetool

# Für WSL/Systeme ohne FUSE
./appimagetool --appimage-extract
mv squashfs-root appimagetool-extracted

# AppImage bauen
./build-appimage.sh

# Testen
chmod +x MyApps-0.1.0-x86_64.AppImage
./MyApps-0.1.0-x86_64.AppImage
```

## Code-Stil

- **Sprache**: Code-Kommentare und Docstrings auf Deutsch
- **Commit-Messages**: Auf Deutsch
- **Python**: PEP 8 Richtlinien befolgen
- **Type Hints**: Verwenden für alle Funktionen
- **Logging**: `logging`-Modul verwenden (nicht `print()`)

Beispiel:
```python
def meine_funktion(param: str) -> bool:
    """
    Beschreibung der Funktion

    Args:
        param: Beschreibung des Parameters

    Returns:
        True bei Erfolg, False bei Fehler
    """
    logger.info(f"Funktion aufgerufen mit: {param}")
    return True
```

## Testing

Bevor du einen Pull Request erstellst:

1. Teste die App auf deiner Distribution
2. Prüfe ob alle Features funktionieren
3. Füge Screenshots bei GUI-Änderungen hinzu

## Distro-Testing

Wir suchen Tester für verschiedene Distributionen:

- [ ] Debian
- [ ] Ubuntu
- [ ] Linux Mint
- [ ] Arch Linux
- [ ] Manjaro
- [ ] Fedora
- [ ] Solus
- [ ] openSUSE

Wenn du eine dieser Distributionen verwendest, teste MyApps und melde Bugs oder bestätige dass es funktioniert!

## Übersetzungen

Aktuell werden Deutsch und Englisch unterstützt. Weitere Sprachen sind willkommen!

1. Kopiere `locales/de/LC_MESSAGES/myapps.po`
2. Übersetze die Strings
3. Erstelle einen Pull Request

## Community-Richtlinien

- Sei respektvoll und konstruktiv
- Hilf anderen Community-Mitgliedern
- Halte Diskussionen themenrelevant
- Keine Diskriminierung oder Belästigung

## Fragen?

Bei Fragen kannst du:
- Ein Issue öffnen
- Eine Diskussion im Discussions-Bereich starten
- Die Community im [Linux Guides DE Telegram-Chat](https://t.me/LinuxGuidesDECommunity) fragen

Vielen Dank für deine Unterstützung! 🎉
