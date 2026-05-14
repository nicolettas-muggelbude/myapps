Name:           myapps
Version:        1.0.5
Release:        1%{?dist}
Summary:        Linux package manager overview with GTK4 + Libadwaita

License:        GPL-3.0-or-later
URL:            https://github.com/nicolettas-muggelbude/myapps
Source0:        myapps-%{version}.tar.gz

BuildArch:      noarch

# Build Dependencies
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools >= 40.0

# Runtime Dependencies
Requires:       python3 >= 3.8
Requires:       python3-gobject
Requires:       gtk4
Requires:       libadwaita
Requires:       python3-pillow
Requires:       hicolor-icon-theme

%description
MyApps is a user-friendly tool for Linux that displays all installed
applications in a clean interface - without system clutter.

Features:
- Multi-distribution support (Debian, Ubuntu, Arch, Fedora, etc.)
- Modern GTK4 + Libadwaita interface with native dark mode
- Search function (name + description)
- Export functions (TXT, CSV, JSON)
- Multilingual (German, English)

%prep
%autosetup -n myapps-%{version}

# Generate setup.py from pyproject.toml (for compatibility)
cat > setup.py << 'EOF'
#!/usr/bin/env python3
from setuptools import setup
setup()
EOF

%build
# Build using setuptools (reads pyproject.toml via setup.py)
python3 setup.py build

%install
# Install using setuptools
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot} --optimize=1

# Install desktop file
install -Dm644 io.github.nicolettas-muggelbude.myapps.desktop \
    %{buildroot}%{_datadir}/applications/io.github.nicolettas-muggelbude.myapps.desktop

# Install metainfo
install -Dm644 io.github.nicolettas-muggelbude.myapps.metainfo.xml \
    %{buildroot}%{_datadir}/metainfo/io.github.nicolettas-muggelbude.myapps.metainfo.xml

# Install icon
install -Dm644 assets/icons/io.github.nicolettas-muggelbude.myapps.svg \
    %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/io.github.nicolettas-muggelbude.myapps.svg

# Install filters
mkdir -p %{buildroot}%{_datadir}/myapps/filters
cp -r filters/* %{buildroot}%{_datadir}/myapps/filters/

# Install locales (if they exist)
if [ -d locales ] && [ "$(ls -A locales)" ]; then
    mkdir -p %{buildroot}%{_datadir}/myapps/locales
    cp -r locales/* %{buildroot}%{_datadir}/myapps/locales/
fi

# Install assets
mkdir -p %{buildroot}%{_datadir}/myapps/assets
cp -r assets/* %{buildroot}%{_datadir}/myapps/assets/

# Install pyproject.toml and WHATS_NEW.md for version/changelog info
install -Dm644 pyproject.toml %{buildroot}%{_datadir}/myapps/pyproject.toml
install -Dm644 WHATS_NEW.md %{buildroot}%{_datadir}/myapps/WHATS_NEW.md

%files
%license LICENSE
%doc README.md
%{_bindir}/myapps
%{python3_sitelib}/myapps/
%{python3_sitelib}/myapps-*.egg-info/
%{_datadir}/applications/io.github.nicolettas-muggelbude.myapps.desktop
%{_datadir}/metainfo/io.github.nicolettas-muggelbude.myapps.metainfo.xml
%dir %{_datadir}/icons/hicolor
%dir %{_datadir}/icons/hicolor/scalable
%dir %{_datadir}/icons/hicolor/scalable/apps
%{_datadir}/icons/hicolor/scalable/apps/io.github.nicolettas-muggelbude.myapps.svg
%{_datadir}/myapps/

%post
# OBS-Repo automatisch eintragen (nur beim ersten Install)
OBS_BASE="https://download.opensuse.org/repositories/home:/nicoletta:/myapps"
REPO_FILE=""

if command -v dnf >/dev/null 2>&1; then
    # Fedora
    REPO_FILE="/etc/yum.repos.d/myapps-obs.repo"
    if [ ! -f "$REPO_FILE" ]; then
        . /etc/os-release
        case "$VERSION_ID" in
            41) DIST="Fedora_41" ;;
            42) DIST="Fedora_42" ;;
            43) DIST="Fedora_43" ;;
            *)  DIST="Fedora_42" ;;
        esac
        cat > "$REPO_FILE" << EOF
[home_nicoletta_myapps]
name=MyApps (OBS)
baseurl=${OBS_BASE}/${DIST}/
enabled=1
gpgcheck=1
gpgkey=${OBS_BASE}/${DIST}/repodata/repomd.xml.key
EOF
    fi
elif command -v zypper >/dev/null 2>&1; then
    # openSUSE
    REPO_FILE="/etc/zypp/repos.d/myapps-obs.repo"
    if [ ! -f "$REPO_FILE" ]; then
        . /etc/os-release
        case "$VERSION_CODENAME" in
            Tumbleweed) DIST="openSUSE_Tumbleweed" ;;
            Slowroll)   DIST="openSUSE_Slowroll" ;;
            *)
                case "$VERSION_ID" in
                    16*) DIST="openSUSE_Leap_16" ;;
                    *)   DIST="openSUSE_Tumbleweed" ;;
                esac
                ;;
        esac
        zypper addrepo --gpgcheck --refresh \
            "${OBS_BASE}/${DIST}/" myapps-obs &>/dev/null || :
    fi
fi

# Update icon cache
if command -v gtk-update-icon-cache >/dev/null 2>&1; then
    gtk-update-icon-cache -f -t %{_datadir}/icons/hicolor &>/dev/null || :
fi

# Update desktop database
if command -v update-desktop-database >/dev/null 2>&1; then
    update-desktop-database -q %{_datadir}/applications &>/dev/null || :
fi

%postun
# OBS-Repo beim vollständigen Deinstallieren entfernen
if [ $1 -eq 0 ]; then
    rm -f /etc/yum.repos.d/myapps-obs.repo
    if command -v zypper >/dev/null 2>&1; then
        zypper removerepo myapps-obs &>/dev/null || :
    fi

    if command -v gtk-update-icon-cache >/dev/null 2>&1; then
        gtk-update-icon-cache -f -t %{_datadir}/icons/hicolor &>/dev/null || :
    fi
    if command -v update-desktop-database >/dev/null 2>&1; then
        update-desktop-database -q %{_datadir}/applications &>/dev/null || :
    fi
fi

%changelog
* Thu May 14 2026 MyApps Contributors <noreply@github.com> - 1.0.5-1
- Fix: UPDATE-Badge in Desktop-Ansicht ergaenzt

* Thu May 14 2026 MyApps Contributors <noreply@github.com> - 1.0.4-1
- Fix: LANG=C für apt-get damit Auto-Updater auf deutschen Systemen Erfolg korrekt meldet
- Fix: Filter Updates verfügbar zeigt in Desktop-Ansicht korrekte Apps (icon_name-Abgleich)

* Thu May 14 2026 MyApps Contributors <noreply@github.com> - 1.0.3-1
- Fix: UPDATE-Badge in Filter Updates verfügbar für alle Pakete sichtbar
- Fix: Desktop-Ansicht zeigt korrekt Pakete mit Updates an

* Wed May 14 2026 MyApps Contributors <noreply@github.com> - 1.0.2-1
- Feature: Filter "Updates verfügbar" im Scope-Dropdown

* Thu May 14 2026 MyApps Contributors <noreply@github.com> - 1.0.1-1
- Fix: Auto-Updater führt apt update vor Install aus (verhindert Endlosschleife)
- Fix: Korrekte Erkennung ob apt wirklich etwas aktualisiert hat

* Thu May 14 2026 MyApps Contributors <noreply@github.com> - 1.0.0-1
- Stable Release nach Community-Testing
- Feature: UPDATE-Badge neben App-Namen in Liste und Tabelle
- Feature: apt-get update via pkexec vor dem Paket-Update-Check
- Fix: Update-Meldungen klarer formuliert

* Wed Apr 29 2026 MyApps Contributors <noreply@github.com> - 0.4.1-1
- Feature: Update-Status — Icon in Liste/Tabelle für Pakete mit verfügbaren Updates
- Feature: Desktop-Benachrichtigungen via notify-send (opt-in, Standard: aktiv)
- Feature: Auto-Updater — MyApps via pkexec aktualisieren (apt/dnf/zypper); AUR-Hinweis für Arch
- Fix: Benachrichtigungs-Toggle im Menü, persistent in ~/.config/myapps/settings.json

* Sun Apr 12 2026 MyApps Contributors <noreply@github.com> - 0.4.0-1
- Performance: Virtual Scrolling — keine Pagination mehr, alle Apps in einer Liste
- GTK4 rendert nur sichtbare Elemente, performant bei 2000+ Paketen
- Feature: Update-Benachrichtigung via Adw.Banner wenn neue Version verfügbar
- Sort-Bar ersetzt Pagination-Bar

* Tue Mar 31 2026 MyApps Contributors <noreply@github.com> - 0.3.1-1
- Feature: Desktop-Apps-Ansicht (Issue #4) — zeigt .desktop-Anwendungen
- Neue Registerkarte "Desktop" neben Liste und Tabelle
- Erkennt Apps aus /usr/share/applications, ~/.local/share/applications, Flatpak, Snap
- Lokalisierte Namen und Beschreibungen (Name[de], Comment[de])
- Schließt Issue #4

* Sun Mar 08 2026 MyApps Contributors <noreply@github.com> - 0.3.0-1
- Feature: Sortierfunktion nach Name, Größe, Installationsdatum (Issue #11)
- Feature: Scope-Dropdown "Nur User-Apps" / "Alle Pakete" (Issue #16)
- Feature: Mindestens 5 Zeichen für Suche
- Feature: Installierte Größe in Liste und Tabelle (Issue #5)
- Feature: Installationsdatum in Liste und Tabelle (Issue #10)
- Größen-Unterstützung: dpkg, rpm, pacman, flatpak, snap
- Datums-Unterstützung: dpkg.log, rpm %{INSTALLTIME}, pacman -Qi, flatpak/snap Filesystem
- Closes #5, #10, #11, #16

* Mon Jan 27 2026 MyApps Contributors <noreply@github.com> - 0.2.4-1
- Performance-Release: Icon-Caching, Sortierung optimiert, Memory Leak behoben
- Deutlich schnellere Seitenwechsel (besonders bei vielen installierten Paketen)
- Stabiler Memory-Verbrauch auch bei vielen Seitenwechseln
- Fix: Export-Format-Bug (#15) - CSV/JSON Export funktionieren korrekt
- Fixes #17

* Fri Dec 27 2024 MyApps Contributors <noreply@github.com> - 0.2.3-1
- Fix: Version 0.0.0 in About dialog (all OBS/AUR packages)
- Fix: No changelog information available
- Install pyproject.toml and WHATS_NEW.md to /usr/share/myapps/
- About dialog now shows correct version and features

* Fri Dec 27 2024 MyApps Contributors <noreply@github.com> - 0.2.2-1
- Fix: NameError on systems without tkinter (all OBS packages)
- Fix: ImageTk type hints as string literals
- Critical bugfix for v0.2.1

* Fri Dec 27 2024 MyApps Contributors <noreply@github.com> - 0.2.1-1
- Fix: Base directory detection for /usr/share/myapps
- Fix: GTK4 SearchEntry placeholder compatibility
- Fix: Locales and filters not found on Ubuntu 22.04/Mint 21.3
- Fixes #13

* Thu Dec 26 2024 MyApps Contributors <noreply@github.com> - 0.2.0-1
- Initial OBS release
- GTK4 + Libadwaita migration
- Search function added
- Export improvements
- German and English UI
- Multi-architecture support (x86_64, i586, aarch64)
