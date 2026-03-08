# MyApps v0.3.0 - Scope, Größe, Datum & Sortierung! 🎉

Hallo liebe MyApps-Community!

Großes Update heute: **MyApps v0.3.0** ist da – und bringt gleich vier neue Features auf einmal mit!

## Was ist neu?

### 🔭 Scope-Dropdown: Endlich alle Pakete sichtbar!

Bisher habt ihr manchmal gefragt: "Wo ist mein Paket XY?" – und es war einfach gefiltert worden, weil unser Algorithmus es als System-Paket erkannt hat. Das war manchmal frustrierend.

Jetzt gibt es neben dem Suchfeld ein **Scope-Dropdown**:
- **"Nur User-Apps"** (Standard): Die gewohnte gefilterte Ansicht mit ~150-800 Apps
- **"Alle Pakete"**: Alles, wirklich alles – alle 1000-3000+ installierten Pakete

So findet ihr auch Pakete, die sonst versteckt wären. Kein Rätselraten mehr!

### 📏 Installierte Größe: Endlich wisst ihr, was Platz braucht

Jede App zeigt jetzt die **tatsächlich installierte Größe** an – nicht nur einen Schätzwert, sondern den echten Wert vom Paketmanager:

- **Debian/Ubuntu**: `dpkg-query --show` mit `${Installed-Size}`
- **Fedora/openSUSE**: `rpm -qa` mit `%{SIZE}`
- **Arch Linux**: `pacman -Qi` mit "Installed Size"
- **Flatpak**: `flatpak list --columns=installed-size`
- **Snap**: `du -sb` aller Snap-Verzeichnisse (ein einziger Batch-Aufruf!)

In der **Listenansicht** erscheint die Größe am rechten Rand jeder Zeile.
In der **Tabellenansicht** gibt es eine eigene "Größe"-Spalte.

### 📅 Installationsdatum: Wann habt ihr das installiert?

Manchmal will man wissen: "Wann habe ich dieses Paket eigentlich installiert?" Ab jetzt könnt ihr das sehen!

- **Debian/Ubuntu**: Liest alle `dpkg.log` und `dpkg.log.*.gz` Dateien
- **Fedora/openSUSE**: `rpm -qa` mit `%{INSTALLTIME}` (Unix-Timestamp)
- **Arch Linux**: `pacman -Qi` mit "Install Date"
- **Flatpak/Snap**: Filesystem-Zeitstempel des App-Verzeichnisses

Das Datum wird **sprachgerecht** angezeigt:
- **Deutsch**: "26. Dez. 2024"
- **Englisch**: "Dec 26, 2024"

### 🔢 Sortierfunktion: Bringt eure Pakete in Ordnung

Ein neues Dropdown in der Navigationsleiste bietet **7 Sortieroptionen**:

| Sortierung | Beschreibung |
|-----------|--------------|
| Standard | Nach Pakettyp, dann alphabetisch |
| Name A-Z | Alphabetisch aufsteigend |
| Name Z-A | Alphabetisch absteigend |
| Größte zuerst | Größte Pakete oben |
| Kleinste zuerst | Kleinste Pakete oben |
| Neueste zuerst | Zuletzt installierte oben |
| Älteste zuerst | Älteste Installationen oben |

Pakete ohne Größe oder Datum erscheinen dabei am Ende der Liste.

### 🔍 Suche: Mindestens 5 Zeichen

Um zu viele Treffer zu vermeiden, filtert die Suche jetzt erst ab **5 Zeichen**. Bei weniger zeigt die Statusbar einen freundlichen Hinweis.

## Performance: Kein Einfrieren mehr!

Beim Wechsel von Tabellen- zu Listenansicht gab es früher manchmal bis zu 7 Sekunden Wartezeit (auf Systemen mit vielen dpkg-Paketen). Das ist jetzt Geschichte:

- Listenansicht rendert **sofort** mit gecachten oder englischen Beschreibungen
- Lokalisierte Beschreibungen werden **im Hintergrund** nachgeladen
- **Kein Einfrieren** der Oberfläche mehr

## Installation

### OBS-Pakete (Empfohlen)

Die gewohnten OBS-Pakete werden in Kürze verfügbar sein:

**Debian/Ubuntu:**
```bash
# Debian 12 (Bookworm)
echo "deb https://download.opensuse.org/repositories/home:/nicoletta:/myapps/Debian_12/ /" | sudo tee /etc/apt/sources.list.d/myapps.list
wget -qO- https://download.opensuse.org/repositories/home:/nicoletta:/myapps/Debian_12/Release.key | sudo gpg --dearmor -o /etc/apt/trusted.gpg.d/myapps.gpg
sudo apt update && sudo apt install myapps
```

**Oder:** https://software.opensuse.org//download.html?project=home%3Anicoletta%3Amyapps&package=myapps

### Arch Linux (AUR)

```bash
yay -S myapps
# oder: paru -S myapps
```

## Feedback

Wie immer: Bugs, Ideen und Feedback sind herzlich willkommen!
- GitHub Issues: https://github.com/nicolettas-muggelbude/myapps/issues
- Telegram: https://t.me/LinuxGuidesDECommunity

Danke an alle, die v0.2.4 getestet und Feedback gegeben haben! 💙

---

*MyApps ist Open Source (GPLv3) und wird von der Linux Guides DE Community entwickelt.*
