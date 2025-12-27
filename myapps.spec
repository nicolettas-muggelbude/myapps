Name:           myapps
Version:        0.2.1
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
# Update icon cache
if command -v gtk-update-icon-cache >/dev/null 2>&1; then
    gtk-update-icon-cache -f -t %{_datadir}/icons/hicolor &>/dev/null || :
fi

# Update desktop database
if command -v update-desktop-database >/dev/null 2>&1; then
    update-desktop-database -q %{_datadir}/applications &>/dev/null || :
fi

%postun
# Update icon cache after removal
if [ $1 -eq 0 ]; then
    if command -v gtk-update-icon-cache >/dev/null 2>&1; then
        gtk-update-icon-cache -f -t %{_datadir}/icons/hicolor &>/dev/null || :
    fi

    if command -v update-desktop-database >/dev/null 2>&1; then
        update-desktop-database -q %{_datadir}/applications &>/dev/null || :
    fi
fi

%changelog
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
