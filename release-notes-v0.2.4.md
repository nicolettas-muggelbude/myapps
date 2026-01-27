# MyApps v0.2.4 - Performance-Release ⚡

**Dieses Release konzentriert sich ausschließlich auf Performance-Optimierungen und macht MyApps deutlich schneller und stabiler!**

User mit vielen installierten Paketen (~400+ Apps) berichteten von langsamen Seitenwechseln und steigendem Memory-Verbrauch. v0.2.4 behebt alle identifizierten Performance-Probleme.

---

## 🚀 Performance-Optimierungen

### ✅ Icon-Caching implementiert
**Problem:** Icons wurden bei jedem Seitenwechsel neu geladen (100x pro Seite!)

**Lösung:**
- Icons werden nur einmal geladen und gecacht
- Cache shared zwischen allen Views
- Gecachte Seiten laden deutlich schneller

**Code:**
```python
# Icons nur einmal laden
self.icon_cache = {}
cache_key = f"{pkg.name}_{pkg.package_type}"
if cache_key not in self.icon_cache:
    self.icon_cache[cache_key] = self.icon_manager.get_icon(...)
```

**Commits:** `b0ff7e4`, `76edd05`

---

### ✅ Sortierung optimiert
**Problem:** Liste wurde bei jedem Seitenwechsel neu sortiert (unnötige Arbeit!)

**Lösung:**
- Sortierung nur EINMAL nach Filterung/Suche
- Kein Re-Sortieren bei Seitenwechsel
- Von O(n log n) zu O(1) bei jedem Klick

**Code:**
```python
# In _apply_search_filter() - nur einmal!
self.gui.search_filtered_packages = sorted(
    packages,
    key=lambda p: (p.package_type, p.name.lower())
)

# In _populate_list_view() - keine Sortierung mehr!
page_packages = self.gui.search_filtered_packages[start_idx:end_idx]
```

**Commit:** `873747c`

---

### ✅ Memory Leak behoben
**Problem:** Event Handler wurden bei jedem Seitenwechsel neu verbunden (Memory Leak!)

**Lösung:**
- Handler von `bind()` nach `setup()` verschoben
- Handler wird nur EINMAL pro Widget verbunden
- Stabiler Memory-Verbrauch auch bei vielen Seitenwechseln

**Code:**
```python
# In _on_list_setup() - nur einmal!
def on_right_click(gesture, n_press, x, y):
    pkg = list_item.get_item()  # Zur Laufzeit holen
    if pkg:
        self._show_context_menu(box, pkg, x, y)

gesture.connect("pressed", on_right_click)
```

**Commit:** `d95b3b5`

---

## 📊 Ergebnisse

**Performance:**
- ⚡ **Seitenwechsel deutlich schneller und flüssiger**
- ⚡ **Gecachte Seiten laden sehr schnell**
- ⚡ **App fühlt sich insgesamt performanter an**

**Memory:**
- 🧹 **Stabiler Verbrauch auch bei vielen Seitenwechseln**
- 🧹 **Kein kontinuierlicher Memory-Anstieg mehr**

**Dokumentation:**
- 📝 CLAUDE.md aktualisiert
- 📝 ROADMAP.md aktualisiert
- 📝 PLAN_v0.2.4.md erstellt

---

## 🐛 Bugfixes

### Issue #15: Export-Format-Bug behoben
- **Problem:** Export war immer .txt, auch wenn CSV/JSON gewählt wurde
- **Lösung:** Filter-basierte Format-Erkennung implementiert
- **Status:** ✅ Alle Formate (TXT/CSV/JSON) funktionieren korrekt
- **Commit:** `a7e9fb3`

---

## 📦 Installation

### **OBS-Pakete** - Empfohlen ✅

<a href="https://software.opensuse.org//download.html?project=home%3Anicoletta%3Amyapps&package=myapps"><img src="https://img.shields.io/badge/Download-OBS_Pakete-73BA25?style=for-the-badge&logo=opensuse&logoColor=white" alt="OBS Download"></a>

**Unterstützte Distributionen (11):**
- **Debian:** 12 (Bookworm), 13 (Trixie)
- **Ubuntu:** 22.04 LTS, 24.04 LTS, 25.10
- **Fedora:** 41, 42, 43
- **openSUSE:** Leap 16, Slowroll, Tumbleweed

**Installation (Beispiel Debian/Ubuntu):**
```bash
# Repo hinzufügen (einmalig)
echo "deb https://download.opensuse.org/repositories/home:/nicoletta:/myapps/Debian_12/ /" | sudo tee /etc/apt/sources.list.d/myapps.list
wget -qO- https://download.opensuse.org/repositories/home:/nicoletta:/myapps/Debian_12/Release.key | sudo gpg --dearmor -o /etc/apt/trusted.gpg.d/myapps.gpg
sudo apt update

# Installieren
sudo apt install myapps
```

Siehe [OBS Download-Portal](https://software.opensuse.org//download.html?project=home%3Anicoletta%3Amyapps&package=myapps) für andere Distributionen.

---

### **AUR-Paket** - Arch Linux ✅

<a href="https://aur.archlinux.org/packages/myapps"><img src="https://img.shields.io/badge/Download-AUR-1793D1?style=for-the-badge&logo=archlinux&logoColor=white" alt="AUR Download"></a>

**Installation:**
```bash
yay -S myapps
# oder
paru -S myapps
# oder
makepkg -si
```

---

## 🎯 Was kommt als Nächstes?

**v0.3.0 - Such-Scope & Features** (geplant)
- Scope-Dropdown für Suche ("Nur User-Apps" vs. "Alle Pakete")
- Mindestens 5 Zeichen für Suche
- Performance-Basis ist jetzt gelegt! ✅

**Siehe:** [Issue #16](https://github.com/nicolettas-muggelbude/myapps/issues/16)

---

## 🙏 Danke

An alle Community-Mitglieder, die Performance-Feedback gegeben haben und beim Testing geholfen haben!

Besonderer Dank an User mit Mint-Installationen, die das Performance-Problem gemeldet haben - ohne euer Feedback wäre dieses Release nicht entstanden!

---

## 💝 MyApps unterstützen

Dieses Projekt ist **Open Source** (GPLv3) und wird von der Community entwickelt!

<a href="https://www.paypal.com/ncp/payment/UYJ73YNEZ3KHL"><img src="https://img.shields.io/badge/PayPal-Spenden-00457C?style=for-the-badge&logo=paypal&logoColor=white" alt="Spenden via PayPal"></a>

**Spenden gehen an:** PC-Wittfoot UG (Spendenverwalter)
**Verwendung:** Serverkosten, Hardware, Entwicklerzeit für MyApps

**Hinweis:** Die Entwicklung erfolgt durch die Linux Guides DE Community (Open Source).
PC-Wittfoot UG verwaltet nur die Spenden, ist aber NICHT der Entwickler.

**Rechtliches:**
[Impressum](https://nicolettas-muggelbude.github.io/myapps/impressum) | [Datenschutz](https://nicolettas-muggelbude.github.io/myapps/datenschutz)

---

**Changelog:** https://github.com/nicolettas-muggelbude/myapps/compare/v0.2.3...v0.2.4
