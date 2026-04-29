"""
GTK4 + Libadwaita GUI für MyApps
Native Linux Desktop Integration mit Virtual Scrolling
"""

import json
import locale
import logging
import subprocess
import threading
from datetime import datetime
from pathlib import Path
from typing import List, Optional

# GTK4 + Libadwaita
import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw, Gio, GLib, GdkPixbuf, GObject

# MyApps Modules (bleiben gleich!)
from .package_manager import Package, PackageManagerFactory, DesktopFileManager, UpdateChecker
from .filters import FilterManager
from .export import Exporter
from .distro_detect import get_distro_info
from .i18n import _
from .icons import IconManagerGTK

logger = logging.getLogger(__name__)


def get_version_from_pyproject() -> str:
    """
    Liest die Version aus pyproject.toml.
    Sucht zuerst in /usr/share/myapps/ (System-Installation),
    dann im Projekt-Root (Development).
    Fallback auf "0.0.0" wenn Datei nicht gefunden oder parsing fehlschlägt.
    """
    try:
        # Suchpfade in Prioritätsreihenfolge
        search_paths = [
            Path("/usr/share/myapps/pyproject.toml"),  # System-Installation (OBS/DEB)
            Path(__file__).parent.parent.parent / "pyproject.toml",  # Development
        ]

        pyproject_path = None
        for path in search_paths:
            if path.exists():
                pyproject_path = path
                break

        if not pyproject_path:
            logger.warning(f"pyproject.toml nicht gefunden in: {[str(p) for p in search_paths]}")
            return "0.0.0"

        # Parse pyproject.toml (einfaches String-Parsing)
        with open(pyproject_path, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip().startswith('version ='):
                    # Extrahiere Version: version = "0.2.1" -> 0.2.1
                    version = line.split('=')[1].strip().strip('"').strip("'")
                    logger.info(f"Version aus {pyproject_path} gelesen: {version}")
                    return version

        logger.warning(f"Keine version = Zeile in {pyproject_path} gefunden")
        return "0.0.0"

    except Exception as e:
        logger.error(f"Fehler beim Lesen der Version: {e}")
        return "0.0.0"


# Version automatisch aus pyproject.toml lesen
VERSION = get_version_from_pyproject()


def format_size(size_bytes: Optional[int]) -> str:
    """
    Formatiert Bytes in lesbare Größenangabe (Issue #5)

    Args:
        size_bytes: Größe in Bytes oder None

    Returns:
        Lesbarer String z.B. "12.3 MB", "456 KB", "" wenn None
    """
    if size_bytes is None or size_bytes <= 0:
        return ""
    if size_bytes >= 1024 ** 3:
        return f"{size_bytes / 1024**3:.1f} GB"
    elif size_bytes >= 1024 ** 2:
        return f"{size_bytes / 1024**2:.1f} MB"
    elif size_bytes >= 1024:
        return f"{size_bytes / 1024:.0f} KB"
    else:
        return f"{size_bytes} B"


def get_whats_new(version: str) -> List[str]:
    """
    Liest die What's New Features für eine Version aus WHATS_NEW.md.
    Sucht zuerst in /usr/share/myapps/ (System-Installation),
    dann im Projekt-Root (Development).

    Args:
        version: Version im Format "X.Y.Z"

    Returns:
        Liste von Feature-Strings, leer wenn Version nicht gefunden
    """
    try:
        # Suchpfade in Prioritätsreihenfolge
        search_paths = [
            Path("/usr/share/myapps/WHATS_NEW.md"),  # System-Installation (OBS/DEB)
            Path(__file__).parent.parent.parent / "WHATS_NEW.md",  # Development
        ]

        whats_new_path = None
        for path in search_paths:
            if path.exists():
                whats_new_path = path
                break

        if not whats_new_path:
            logger.warning(f"WHATS_NEW.md nicht gefunden in: {[str(p) for p in search_paths]}")
            return []

        # Parse WHATS_NEW.md
        features = []
        in_version_section = False
        version_header = f"## v{version}"

        with open(whats_new_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.rstrip()

                # Start der gesuchten Version
                if line.startswith(version_header):
                    in_version_section = True
                    continue

                # Ende der Sektion (nächste Version oder Ende)
                if in_version_section and line.startswith("## v"):
                    break

                # Features sammeln (Zeilen die mit "- " beginnen)
                if in_version_section and line.startswith("- "):
                    features.append(line[2:])  # Entferne "- " Präfix

        if features:
            logger.info(f"Gefundene Features für v{version}: {len(features)}")
        else:
            logger.warning(f"Keine Features für v{version} in WHATS_NEW.md gefunden")

        return features

    except Exception as e:
        logger.error(f"Fehler beim Lesen von WHATS_NEW.md: {e}")
        return []


def format_date(date_str: Optional[str]) -> str:
    """
    Formatiert ein ISO-Datum (YYYY-MM-DD) in ein lokalisiertes, lesbares Format.
    Erkennt die System-Sprache und gibt das Datum entsprechend aus:
      Deutsch:  "26. Dez. 2024"
      Englisch: "Dec 26, 2024"

    Args:
        date_str: Datum im Format "YYYY-MM-DD" oder None

    Returns:
        Lokalisierter Datumsstring oder "" wenn None
    """
    if not date_str:
        return ""
    try:
        d = datetime.strptime(date_str, "%Y-%m-%d")
        lang = (locale.getlocale()[0] or "").split("_")[0].lower()
        if lang == "de":
            return d.strftime("%-d. %b %Y")   # "26. Dez. 2024"
        else:
            return d.strftime("%b %-d, %Y")    # "Dec 26, 2024"
    except (ValueError, AttributeError):
        return date_str


class SettingsManager:
    """Verwaltet persistente App-Einstellungen in ~/.config/myapps/settings.json"""

    def __init__(self):
        self._config_dir = Path.home() / ".config" / "myapps"
        self._settings_file = self._config_dir / "settings.json"
        self._data: dict = {}
        self._load()

    def _load(self):
        try:
            if self._settings_file.exists():
                with open(self._settings_file, encoding="utf-8") as f:
                    self._data = json.load(f)
        except Exception as e:
            logger.debug(f"Einstellungen konnten nicht geladen werden: {e}")

    def get(self, key: str, default=None):
        return self._data.get(key, default)

    def set(self, key: str, value):
        self._data[key] = value
        self._save()

    def _save(self):
        try:
            self._config_dir.mkdir(parents=True, exist_ok=True)
            with open(self._settings_file, "w", encoding="utf-8") as f:
                json.dump(self._data, f, indent=2)
        except Exception as e:
            logger.warning(f"Einstellungen konnten nicht gespeichert werden: {e}")


class PackageItem(GObject.Object):
    """GObject-Wrapper für Package-Objekte (für Gio.ListStore)"""

    def __init__(self, package: Package):
        super().__init__()
        self.package = package

    @property
    def name(self) -> str:
        return self.package.name

    @property
    def version(self) -> str:
        return self.package.version

    @property
    def package_type(self) -> str:
        return self.package.package_type

    @property
    def description(self) -> str:
        return self.package.description or ""

    @property
    def size(self) -> Optional[int]:
        return self.package.size

    @property
    def size_formatted(self) -> str:
        return format_size(self.package.size)

    @property
    def install_date(self) -> str:
        return self.package.install_date or ""

    @property
    def icon_name(self) -> Optional[str]:
        return self.package.icon_name

    @property
    def update_available(self) -> bool:
        return self.package.update_available or False


class MyAppsGUI(Adw.Application):
    """GTK4 Hauptanwendung mit Libadwaita"""

    def __init__(self, base_dir: str):
        """
        Initialisiert die GTK4 Anwendung

        Args:
            base_dir: Basis-Verzeichnis der Anwendung
        """
        super().__init__(
            application_id='de.pc-wittfoot.myapps',
            flags=Gio.ApplicationFlags.FLAGS_NONE
        )

        self.base_dir = Path(base_dir)
        self.packages: List[Package] = []
        self.filtered_packages: List[Package] = []
        self.search_filtered_packages: List[Package] = []  # Nach Suche gefiltert

        # Desktop-Apps (v0.3.1, Issue #4)
        self.desktop_packages: List[Package] = []
        self.desktop_filtered_packages: List[Package] = []

        # Suche
        self.search_query = ""

        # Scope für Suche (v0.3.0): "user" = User-Apps, "all" = alle Pakete
        self.search_scope = "user"

        # Sortierung (v0.3.0 Issue #11): Schlüssel für aktuelle Sortierung
        # Mögliche Werte: "default", "name_asc", "name_desc",
        #                 "size_asc", "size_desc", "date_asc", "date_desc"
        self.sort_key = "default"

        # Manager initialisieren (UNVERÄNDERT!)
        self.distro_info = get_distro_info()
        self.filter_manager = FilterManager(str(self.base_dir / "filters"))

        # Filter laden
        from .distro_detect import get_filter_files
        filter_files = get_filter_files()
        self.filter_manager.load_filters(filter_files)

        # Icon Manager initialisieren
        self.icon_manager = IconManagerGTK(icon_size=32)

        # Einstellungen laden (Issue #8)
        self.settings = SettingsManager()

        logger.info(f"MyApps GTK4 {VERSION} initialisiert")

    def do_activate(self):
        """Wird aufgerufen wenn App aktiviert wird"""
        # Erstelle Hauptfenster
        self.win = MyAppsWindow(application=self, gui=self)
        self.win.present()

        # Lade Pakete asynchron
        GLib.idle_add(self._start_loading_packages)

    def _start_loading_packages(self):
        """Startet asynchrones Laden der Pakete"""
        thread = threading.Thread(target=self._load_packages_worker, daemon=True)
        thread.start()
        return GLib.SOURCE_REMOVE  # Nur einmal ausführen

    def _load_packages_worker(self):
        """Worker-Thread: Lädt Pakete im Hintergrund"""
        try:
            logger.info("Lade Pakete...")

            # Package Manager (UNVERÄNDERT!)
            package_managers = self.distro_info.package_managers
            self.packages = PackageManagerFactory.get_all_packages(package_managers)
            logger.info(f"{len(self.packages)} Pakete geladen")

            # Filtern (UNVERÄNDERT!)
            self.filtered_packages = self.filter_manager.filter_packages(self.packages)
            logger.info(f"{len(self.filtered_packages)} Apps nach Filterung")

            # Desktop-Apps laden (v0.3.1, Issue #4)
            self.desktop_packages = DesktopFileManager().get_installed_packages()

            # Update GUI im Main Thread
            GLib.idle_add(self.win._on_packages_loaded, self.filtered_packages)

        except Exception as e:
            logger.error(f"Fehler beim Laden der Pakete: {e}")
            GLib.idle_add(self.win._on_loading_error, str(e))


class MyAppsWindow(Adw.ApplicationWindow):
    """GTK4 Hauptfenster"""

    def __init__(self, application, gui):
        super().__init__(application=application)

        self.gui = gui  # Referenz zur App

        # Icon-Cache für Performance-Optimierung (v0.2.4)
        # Key: "pkg_name_pkg_type", Value: GdkPixbuf
        self.icon_cache = {}

        # Lokalisierte Beschreibungs-Cache (v0.3.0 Performance)
        # Key: pkg_name, Value: lokalisierte Beschreibung
        # Verhindert wiederholte apt-cache Aufrufe beim View-Wechsel
        self.localized_desc_cache: dict = {}

        # Auto-Updater (Issue #19)
        self._update_pm: Optional[str] = None    # erkannter PM ("apt", "dnf", ...)
        self._update_cmd: Optional[list] = None  # pkexec-Befehl oder None

        # Fenster-Einstellungen
        self.set_title(f"MyApps v{VERSION}")
        self.set_default_size(1200, 850)

        # CSS Styling laden
        self._load_css()

        # UI aufbauen
        self._build_ui()

        logger.info("Hauptfenster erstellt")

    def _load_css(self):
        """Lädt Custom CSS für Styling"""
        css_provider = Gtk.CssProvider()
        css = """
        /* MyApps GTK4 Custom Styles */

        /* Pagination Info */
        .pagination-info {
            opacity: 0.7;
        }
        """
        css_provider.load_from_data(css.encode())

        # Zu Display hinzufügen
        Gtk.StyleContext.add_provider_for_display(
            self.get_display(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )
        logger.info("CSS Styling geladen")

    def _build_ui(self):
        """Baut die GTK4 UI auf"""
        # Main Container
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        # Header Bar
        header = self._create_header_bar()
        main_box.append(header)

        # Update-Banner (v0.4.0) — initial versteckt
        self.update_banner = Adw.Banner()
        self.update_banner.set_button_label(_("Changelog"))
        self.update_banner.connect("button-clicked", self._on_update_banner_clicked)
        self.update_banner.set_revealed(False)
        main_box.append(self.update_banner)

        # Sort-Bar (v0.4.0: ersetzt Pagination-Bar)
        self.sort_bar = self._create_sort_bar()
        main_box.append(self.sort_bar)

        # Content Area (Stack für Views)
        self.stack = Gtk.Stack()
        self.stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        self.stack.set_transition_duration(250)
        self.stack.set_vexpand(True)
        self.stack.set_hexpand(True)

        # List View (DEFAULT)
        self.list_view_container = self._create_list_view()
        self.stack.add_titled(self.list_view_container, "list", _("Liste"))

        # Table View
        self.table_view_container = self._create_table_view()
        self.stack.add_titled(self.table_view_container, "table", _("Tabelle"))

        # Desktop View (v0.3.1, Issue #4)
        self.desktop_view_container = self._create_desktop_view()
        self.stack.add_titled(self.desktop_view_container, "desktop", _("Desktop"))

        # View-Switch Handler: Repopulate bei Ansichtswechsel
        self.stack.connect("notify::visible-child", lambda *_: self._populate_current_view())

        # View Switcher (für Stack)
        view_switcher = Gtk.StackSwitcher()
        view_switcher.set_stack(self.stack)
        view_switcher.set_halign(Gtk.Align.CENTER)

        switcher_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        switcher_box.set_halign(Gtk.Align.CENTER)
        switcher_box.set_margin_top(6)
        switcher_box.set_margin_bottom(6)
        switcher_box.append(view_switcher)
        main_box.append(switcher_box)

        main_box.append(self.stack)

        # Status Bar
        self.statusbar = Gtk.Statusbar()
        self.status_context = self.statusbar.get_context_id("main")
        main_box.append(self.statusbar)

        # Set Content
        self.set_content(main_box)

    def _create_header_bar(self):
        """Erstellt die Adwaita HeaderBar"""
        header = Adw.HeaderBar()

        # Toolbar Buttons (links)
        refresh_btn = Gtk.Button(label=_("Aktualisieren"))
        refresh_btn.set_icon_name("view-refresh-symbolic")
        refresh_btn.connect("clicked", self._on_refresh_clicked)
        header.pack_start(refresh_btn)

        export_btn = Gtk.Button(label=_("Exportieren"))
        export_btn.set_icon_name("document-save-symbolic")
        export_btn.connect("clicked", self._on_export_clicked)
        header.pack_start(export_btn)

        # Title Widget: Scope-Dropdown + SearchEntry (v0.3.0)
        title_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        title_box.set_halign(Gtk.Align.CENTER)

        # Scope Dropdown (Nur User-Apps / Alle Pakete)
        scope_model = Gtk.StringList.new([_("Nur User-Apps"), _("Alle Pakete")])
        self.scope_dropdown = Gtk.DropDown.new(scope_model, None)
        self.scope_dropdown.set_selected(0)  # Standard: Nur User-Apps
        self.scope_dropdown.connect("notify::selected", self._on_scope_changed)
        title_box.append(self.scope_dropdown)

        # Search Entry
        self.search_entry = Gtk.SearchEntry(placeholder_text=_("Suchen (mind. 5 Zeichen)..."))
        self.search_entry.set_size_request(280, -1)
        self.search_entry.connect("search-changed", self._on_search_changed)
        title_box.append(self.search_entry)

        header.set_title_widget(title_box)

        # Menu Button (rechts)
        menu_btn = Gtk.MenuButton()
        menu_btn.set_icon_name("open-menu-symbolic")
        menu_btn.set_menu_model(self._create_menu())
        header.pack_end(menu_btn)

        return header

    def _create_menu(self):
        """Erstellt das Hauptmenü"""
        menu = Gio.Menu()

        # Einstellungen-Sektion
        settings_section = Gio.Menu()
        settings_section.append(_("Benachrichtigungen bei Updates"), "app.notifications")
        menu.append_section(None, settings_section)

        # About + Quit
        menu.append(_("Über MyApps"), "app.about")
        menu.append(_("Beenden"), "app.quit")

        # Actions registrieren
        about_action = Gio.SimpleAction.new("about", None)
        about_action.connect("activate", self._on_about)
        self.gui.add_action(about_action)

        quit_action = Gio.SimpleAction.new("quit", None)
        quit_action.connect("activate", lambda *_: self.gui.quit())
        self.gui.add_action(quit_action)

        # Benachrichtigungs-Toggle (Issue #8)
        enabled = self.gui.settings.get("notifications_enabled", True)
        notif_action = Gio.SimpleAction.new_stateful(
            "notifications", None, GLib.Variant.new_boolean(enabled)
        )
        notif_action.connect("activate", self._on_notifications_toggle)
        self.gui.add_action(notif_action)

        return menu

    def _on_notifications_toggle(self, action, _param):
        """Schaltet Desktop-Benachrichtigungen ein/aus (Issue #8)"""
        new_state = not action.get_state().get_boolean()
        action.set_state(GLib.Variant.new_boolean(new_state))
        self.gui.settings.set("notifications_enabled", new_state)
        if new_state:
            self._set_status(_("Benachrichtigungen aktiviert"))
        else:
            self._set_status(_("Benachrichtigungen deaktiviert"))

    def _send_update_notification(self, count: int):
        """Sendet Desktop-Benachrichtigung wenn Updates verfügbar sind (Issue #8)"""
        try:
            subprocess.Popen([
                "notify-send",
                "--app-name", "MyApps",
                "--icon", "software-update-available",
                "--urgency", "normal",
                "--expire-time", "10000",
                _("Updates verfügbar"),
                f"{count} " + _("Pakete können aktualisiert werden"),
            ])
        except Exception as e:
            logger.debug(f"Desktop-Benachrichtigung fehlgeschlagen: {e}")

    # Sortieroptionen: (sort_key, Anzeigename)
    _SORT_OPTIONS = [
        ("default",   "Standard (Typ, Name)"),
        ("name_asc",  "Name A → Z"),
        ("name_desc", "Name Z → A"),
        ("size_asc",  "Größe ↑ (klein → groß)"),
        ("size_desc", "Größe ↓ (groß → klein)"),
        ("date_asc",  "Datum ↑ (älteste)"),
        ("date_desc", "Datum ↓ (neueste)"),
    ]

    def _create_sort_bar(self):
        """Erstellt die Sort-Bar (v0.4.0: Virtual Scrolling, kein Pagination mehr)"""
        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        box.set_margin_start(12)
        box.set_margin_end(12)
        box.set_margin_top(6)
        box.set_margin_bottom(6)

        # App-Anzahl Label (links)
        self.count_label = Gtk.Label(label="")
        self.count_label.add_css_class("dim-label")
        self.count_label.set_halign(Gtk.Align.START)
        box.append(self.count_label)

        # Spacer
        spacer = Gtk.Box()
        spacer.set_hexpand(True)
        box.append(spacer)

        # Sort-Dropdown (rechts) (v0.3.0 Issue #11)
        sort_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=4)
        sort_label = Gtk.Label(label=_("Sortieren:"))
        sort_label.add_css_class("dim-label")
        sort_box.append(sort_label)

        sort_labels = [label for _, label in self._SORT_OPTIONS]
        sort_model = Gtk.StringList.new(sort_labels)
        self.sort_dropdown = Gtk.DropDown.new(sort_model, None)
        self.sort_dropdown.set_selected(0)
        self.sort_dropdown.connect("notify::selected", self._on_sort_changed)
        sort_box.append(self.sort_dropdown)
        box.append(sort_box)

        return box

    def _create_list_view(self):
        """Erstellt die ListView mit Virtual Scrolling"""
        # Model: Gio.ListStore für PackageItem-Objekte
        self.list_store = Gio.ListStore.new(PackageItem)

        # Selection Model
        selection = Gtk.NoSelection.new(self.list_store)

        # Factory für Item-Rendering
        factory = Gtk.SignalListItemFactory()
        factory.connect("setup", self._on_list_setup)
        factory.connect("bind", self._on_list_bind)

        # ListView
        list_view = Gtk.ListView.new(selection, factory)
        list_view.set_single_click_activate(False)

        # ScrolledWindow
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_child(list_view)
        scrolled.set_vexpand(True)
        scrolled.set_hexpand(True)

        return scrolled

    def _on_list_setup(self, factory, list_item):
        """Setup: Erstellt Widget-Template für List Items"""
        # Main Container
        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        box.set_margin_start(12)
        box.set_margin_end(12)
        box.set_margin_top(8)
        box.set_margin_bottom(8)

        # Icon
        icon = Gtk.Image()
        icon.set_pixel_size(32)
        box.append(icon)

        # Text Container
        text_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        text_box.set_hexpand(True)

        # Name Label
        name_label = Gtk.Label()
        name_label.set_halign(Gtk.Align.START)
        name_label.add_css_class("title-4")
        name_label.set_ellipsize(3)  # ELLIPSIZE_END – verhindert Überlauf
        text_box.append(name_label)

        # Info Row: Version+Typ links, Größe+Datum rechts
        info_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        info_row.set_hexpand(True)  # MUSS expandieren damit Spacer wirkt!

        # Links: Version + Typ
        info_label = Gtk.Label()
        info_label.set_halign(Gtk.Align.START)
        info_label.add_css_class("dim-label")
        info_label.add_css_class("caption")
        info_row.append(info_label)

        # Spacer
        spacer = Gtk.Box()
        spacer.set_hexpand(True)
        info_row.append(spacer)

        # Rechts: Größe + Datum
        meta_label = Gtk.Label()
        meta_label.set_halign(Gtk.Align.END)
        meta_label.add_css_class("dim-label")
        meta_label.add_css_class("caption")
        info_row.append(meta_label)

        text_box.append(info_row)
        box.append(text_box)

        # Update-Icon rechts (Issue #7, standardmäßig unsichtbar)
        update_icon = Gtk.Image.new_from_icon_name("software-update-available-symbolic")
        update_icon.set_pixel_size(16)
        update_icon.set_valign(Gtk.Align.CENTER)
        update_icon.set_visible(False)
        box.append(update_icon)
        box.update_icon = update_icon

        # Context Menu Setup (einmalig!) - v0.2.4 Memory Leak Fix
        gesture = Gtk.GestureClick.new()
        gesture.set_button(3)  # Rechtsklick

        def on_right_click(gesture, n_press, x, y):
            # Hole aktuelles Package zur Laufzeit (nicht bei Setup!)
            pkg = list_item.get_item()
            if pkg:
                self._show_context_menu(box, pkg, x, y)

        gesture.connect("pressed", on_right_click)
        box.add_controller(gesture)

        # Store widgets für später
        box.icon = icon
        box.name_label = name_label
        box.info_label = info_label
        box.meta_label = meta_label

        list_item.set_child(box)

    def _on_list_bind(self, factory, list_item):
        """Bind: Verknüpft Package-Daten mit Widget"""
        pkg = list_item.get_item()  # PackageItem-Objekt
        box = list_item.get_child()

        # Icon-Caching: Nur einmal laden, dann aus Cache (v0.2.4)
        cache_key = f"{pkg.name}_{pkg.package_type}"
        if cache_key not in self.icon_cache:
            self.icon_cache[cache_key] = self.gui.icon_manager.get_icon(
                pkg.name, pkg.package_type
            )
        pixbuf = self.icon_cache[cache_key]
        box.icon.set_from_pixbuf(pixbuf)

        # Set Data
        box.name_label.set_text(pkg.name)

        # Links: Version + Typ
        box.info_label.set_text(f"{pkg.version}  •  {pkg.package_type.upper()}")

        # Rechts: Größe + lokalisiertes Datum
        meta_parts = []
        if pkg.size_formatted:
            meta_parts.append(pkg.size_formatted)
        if pkg.install_date:
            meta_parts.append(format_date(pkg.install_date))
        box.meta_label.set_text("  •  ".join(meta_parts))

        # Tooltip: Zeigt Paketbeschreibung (Funktion des Pakets)
        if pkg.description:
            # Beschreibung vorhanden: Zeige nur diese (Info ist bereits sichtbar in der Liste)
            tooltip = pkg.description
        else:
            # Keine Beschreibung: Zeige zumindest Paketname als Fallback
            tooltip = f"{pkg.name}\n(Keine Beschreibung verfügbar)"

        box.set_has_tooltip(True)
        box.set_tooltip_text(tooltip)

        # Update-Indikator anzeigen/verstecken (Issue #7)
        box.update_icon.set_visible(pkg.update_available)
        if pkg.update_available:
            box.update_icon.set_tooltip_text(_("Update verfügbar"))

        # Context Menu Handler ist bereits in setup() verbunden (v0.2.4)
        # Kein Handler-Setup in bind() nötig!

    def _create_table_view(self):
        """Erstellt die ColumnView (Table)"""
        # Model
        self.table_store = Gio.ListStore.new(PackageItem)
        selection = Gtk.NoSelection.new(self.table_store)

        # ColumnView
        column_view = Gtk.ColumnView.new(selection)

        # Spalten erstellen
        self._add_column(column_view, _("Name"), "name", expand=True)
        self._add_column(column_view, _("Version"), "version")
        self._add_update_column(column_view)
        self._add_column(column_view, _("Typ"), "package_type")
        self._add_column(column_view, _("Größe"), "size_formatted")
        self._add_column(column_view, _("Installiert am"), "install_date")
        self._add_column(column_view, _("Beschreibung"), "description", expand=True)

        # ScrolledWindow
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_child(column_view)
        scrolled.set_vexpand(True)
        scrolled.set_hexpand(True)

        return scrolled

    def _add_column(self, column_view, title, attr_name, expand=False):
        """Fügt eine Spalte zur ColumnView hinzu"""
        factory = Gtk.SignalListItemFactory()

        def on_setup(factory, list_item):
            label = Gtk.Label()
            label.set_halign(Gtk.Align.START)
            label.set_margin_start(6)
            label.set_margin_end(6)
            label.set_ellipsize(3)  # ELLIPSIZE_END
            list_item.set_child(label)

        def on_bind(factory, list_item):
            pkg = list_item.get_item()
            label = list_item.get_child()
            value = getattr(pkg, attr_name, "")

            if attr_name == "package_type":
                value = value.upper() if value else ""
            elif attr_name == "install_date":
                value = format_date(value) if value else ""

            label.set_text(str(value or ""))

            # Tooltip für Beschreibung
            if attr_name == "description" and value:
                label.set_tooltip_text(value)

        factory.connect("setup", on_setup)
        factory.connect("bind", on_bind)

        column = Gtk.ColumnViewColumn.new(title, factory)
        if expand:
            column.set_expand(True)
        column.set_resizable(True)

        column_view.append_column(column)

    def _add_update_column(self, column_view):
        """Fügt Update-Status-Spalte mit Icon zur ColumnView hinzu (Issue #7)"""
        factory = Gtk.SignalListItemFactory()

        def on_setup(factory, list_item):
            img = Gtk.Image.new_from_icon_name("software-update-available-symbolic")
            img.set_pixel_size(16)
            img.set_margin_start(6)
            img.set_margin_end(6)
            list_item.set_child(img)

        def on_bind(factory, list_item):
            pkg = list_item.get_item()
            img = list_item.get_child()
            img.set_visible(pkg.update_available)
            if pkg.update_available:
                img.set_tooltip_text(_("Update verfügbar"))

        factory.connect("setup", on_setup)
        factory.connect("bind", on_bind)

        column = Gtk.ColumnViewColumn.new(_("Update"), factory)
        column.set_resizable(False)
        column_view.append_column(column)

    def _create_desktop_view(self):
        """Erstellt die Desktop-Apps View (v0.3.1, Issue #4)"""
        self.desktop_store = Gio.ListStore.new(PackageItem)
        selection = Gtk.NoSelection.new(self.desktop_store)

        factory = Gtk.SignalListItemFactory()
        factory.connect("setup", self._on_desktop_setup)
        factory.connect("bind", self._on_desktop_bind)

        list_view = Gtk.ListView.new(selection, factory)
        list_view.set_single_click_activate(False)

        scrolled = Gtk.ScrolledWindow()
        scrolled.set_child(list_view)
        scrolled.set_vexpand(True)
        scrolled.set_hexpand(True)

        return scrolled

    def _on_desktop_setup(self, factory, list_item):
        """Setup: Erstellt Widget-Template für Desktop-App Items"""
        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        box.set_margin_start(12)
        box.set_margin_end(12)
        box.set_margin_top(8)
        box.set_margin_bottom(8)

        # Größeres Icon für Desktop-Apps (48px statt 32px)
        icon = Gtk.Image()
        icon.set_pixel_size(48)
        box.append(icon)

        # Text-Bereich
        text_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
        text_box.set_hexpand(True)

        name_label = Gtk.Label()
        name_label.set_halign(Gtk.Align.START)
        name_label.add_css_class("title-4")
        name_label.set_ellipsize(3)
        text_box.append(name_label)

        desc_label = Gtk.Label()
        desc_label.set_halign(Gtk.Align.START)
        desc_label.add_css_class("dim-label")
        desc_label.add_css_class("caption")
        desc_label.set_ellipsize(3)
        text_box.append(desc_label)

        box.append(text_box)

        # Typ-Badge (flatpak/snap) rechts
        type_label = Gtk.Label()
        type_label.set_halign(Gtk.Align.END)
        type_label.set_valign(Gtk.Align.CENTER)
        type_label.add_css_class("dim-label")
        type_label.add_css_class("caption")
        box.append(type_label)

        box.icon = icon
        box.name_label = name_label
        box.desc_label = desc_label
        box.type_label = type_label

        list_item.set_child(box)

    def _on_desktop_bind(self, factory, list_item):
        """Bind: Verknüpft Desktop-App-Daten mit Widget"""
        pkg = list_item.get_item()
        box = list_item.get_child()

        # Icon: icon_name aus .desktop bevorzugen, Fallback auf pkg.name
        icon_lookup = pkg.icon_name or pkg.name
        cache_key = f"desktop_{icon_lookup}"
        if cache_key not in self.icon_cache:
            self.icon_cache[cache_key] = self.gui.icon_manager.get_icon(
                icon_lookup, pkg.package_type
            )
        box.icon.set_from_pixbuf(self.icon_cache[cache_key])

        box.name_label.set_text(pkg.name)
        box.desc_label.set_text(pkg.description or "")

        # Typ nur anzeigen wenn nicht "desktop" (flatpak/snap sind interessant)
        pkg_type = pkg.package_type
        box.type_label.set_text(pkg_type.upper() if pkg_type != "desktop" else "")

        if pkg.description:
            box.set_has_tooltip(True)
            box.set_tooltip_text(pkg.description)
        else:
            box.set_has_tooltip(False)

    def _show_context_menu(self, widget, pkg, x, y):
        """Zeigt Kontextmenü für Package"""
        menu = Gio.Menu()
        menu.append(_("Als System-App markieren"), "win.mark-system")
        menu.append(_("Namen kopieren"), "win.copy-name")

        # Actions
        mark_action = Gio.SimpleAction.new("mark-system", None)
        mark_action.connect("activate", lambda *_: self._mark_as_system(pkg.name))
        self.add_action(mark_action)

        copy_action = Gio.SimpleAction.new("copy-name", None)
        copy_action.connect("activate", lambda *_: self._copy_to_clipboard(pkg.name))
        self.add_action(copy_action)

        # Popover
        popover = Gtk.PopoverMenu()
        popover.set_menu_model(menu)
        popover.set_parent(widget)
        popover.popup()

    def _mark_as_system(self, package_name):
        """Markiert Paket als System-App"""
        if self.gui.filter_manager.save_user_filter(package_name):
            self._set_status(f"'{package_name}' " + _("als System-App markiert"))
            # Neu laden
            self._on_refresh_clicked(None)
        else:
            self._set_status(_("Fehler beim Markieren"))

    def _copy_to_clipboard(self, text):
        """Kopiert Text in Zwischenablage"""
        clipboard = self.get_clipboard()
        clipboard.set(text)
        self._set_status(f"'{text}' " + _("kopiert"))

    def _on_packages_loaded(self, packages):
        """Callback wenn Pakete geladen sind"""
        self._apply_search_filter()
        self._update_count_label()
        self._populate_current_view()
        # Zeige Gesamtzahl (User-Apps), Vollinfo im Tooltip/Scope
        self._set_status(
            f"{len(packages)} " + _("User-Apps geladen") +
            f"  •  {len(self.gui.packages)} " + _("Pakete gesamt") +
            f"  •  {len(self.gui.desktop_packages)} " + _("Desktop-Apps")
        )
        # GitHub-Versions-Check (v0.4.0)
        self._check_for_updates()
        # Paket-Update-Check (Issue #7)
        self._check_package_updates()
        return GLib.SOURCE_REMOVE

    def _on_search_changed(self, search_entry):
        """Callback wenn Suchtext geändert wird"""
        query = search_entry.get_text().lower().strip()
        self.gui.search_query = query
        self._apply_search_filter()
        self._update_count_label()
        self._populate_current_view()

        # Status Update mit Mindest-Zeichen-Feedback (v0.3.0)
        if query and len(query) < 5:
            self._set_status(f"{_('Mindestens 5 Zeichen für Suche')} ({len(query)}/5)")
        elif query:
            self._set_status(f"{len(self.gui.search_filtered_packages)} " + _("Apps gefunden"))
        else:
            base = self.gui.packages if self.gui.search_scope == "all" else self.gui.filtered_packages
            self._set_status(f"{len(base)} " + _("Apps geladen"))

    def _on_sort_changed(self, dropdown, _pspec):
        """Callback wenn Sort-Dropdown geändert wird (v0.3.0 Issue #11)"""
        idx = dropdown.get_selected()
        self.gui.sort_key = self._SORT_OPTIONS[idx][0]
        self._apply_search_filter()
        self._update_count_label()
        self._populate_current_view()

    def _on_scope_changed(self, dropdown, _pspec):
        """Callback wenn Scope-Dropdown geändert wird (v0.3.0)"""
        self.gui.search_scope = "all" if dropdown.get_selected() == 1 else "user"
        self._apply_search_filter()
        self._update_count_label()
        self._populate_current_view()

        # Status Update
        base = self.gui.packages if self.gui.search_scope == "all" else self.gui.filtered_packages
        label = _("Alle Pakete") if self.gui.search_scope == "all" else _("User-Apps")
        self._set_status(f"{len(base)} {label} " + _("geladen"))

    def _apply_search_filter(self):
        """Wendet Scope + Suchfilter an (v0.3.0: Scope-Dropdown + mind. 5 Zeichen)"""
        # Basis-Liste je nach Scope (v0.3.0)
        if self.gui.search_scope == "all":
            base_packages = self.gui.packages
        else:
            base_packages = self.gui.filtered_packages

        query = self.gui.search_query

        # Suche: mindestens 5 Zeichen erforderlich (v0.3.0)
        if not query or len(query) < 5:
            # Kein Suchbegriff oder zu kurz: zeige Basis-Liste
            packages = base_packages
        else:
            # Suche in Name und Beschreibung
            matching = []
            for pkg in base_packages:
                if query in pkg.name.lower():
                    matching.append(pkg)
                    continue
                if pkg.description and query in pkg.description.lower():
                    matching.append(pkg)
                    continue
            packages = matching

        # Sortierung je nach gewähltem Sort-Key (v0.3.0 Issue #11)
        sk = self.gui.sort_key
        if sk == "name_asc":
            key_fn, reverse = lambda p: p.name.lower(), False
        elif sk == "name_desc":
            key_fn, reverse = lambda p: p.name.lower(), True
        elif sk == "size_asc":
            # None-Größe ans Ende (inf ist größer als alle echten Werte)
            key_fn, reverse = lambda p: (p.size if p.size is not None else float('inf')), False
        elif sk == "size_desc":
            # None-Größe ans Ende (bei desc: -1 ist kleiner als alle echten Werte)
            key_fn, reverse = lambda p: (p.size if p.size is not None else -1), True
        elif sk == "date_asc":
            # None-Datum ans Ende ("9999" > alle echten YYYY-MM-DD Strings)
            key_fn, reverse = lambda p: (p.install_date or "9999-99-99"), False
        elif sk == "date_desc":
            # None-Datum ans Ende (bei desc: "" < alle echten Datumstrings)
            key_fn, reverse = lambda p: (p.install_date or ""), True
        else:  # "default": Typ, dann alphabetisch
            key_fn, reverse = lambda p: (p.package_type, p.name.lower()), False

        self.gui.search_filtered_packages = sorted(packages, key=key_fn, reverse=reverse)

        # Desktop-Apps filtern (v0.3.1) — Scope gilt hier nicht
        if not query or len(query) < 5:
            desktop_base = self.gui.desktop_packages
        else:
            desktop_base = [
                pkg for pkg in self.gui.desktop_packages
                if query in pkg.name.lower() or
                   (pkg.description and query in pkg.description.lower())
            ]

        # Desktop: nur Name-Sortierung sinnvoll (keine Größe/Datum)
        if sk in ("name_desc",):
            self.gui.desktop_filtered_packages = sorted(
                desktop_base, key=lambda p: p.name.lower(), reverse=True
            )
        else:
            self.gui.desktop_filtered_packages = sorted(
                desktop_base, key=lambda p: p.name.lower()
            )

    def _on_loading_error(self, error_msg):
        """Callback bei Lade-Fehler"""
        self._set_status(f"Fehler: {error_msg}")
        return GLib.SOURCE_REMOVE

    def _check_for_updates(self):
        """Startet Update-Check im Hintergrund-Thread (v0.4.0)"""
        thread = threading.Thread(target=self._check_updates_worker, daemon=True)
        thread.start()

    def _check_updates_worker(self):
        """Prüft GitHub Releases API auf neue Version (v0.4.0)"""
        import urllib.request
        import json
        try:
            url = "https://api.github.com/repos/nicolettas-muggelbude/myapps/releases/latest"
            req = urllib.request.Request(
                url, headers={"User-Agent": f"MyApps/{VERSION}"}
            )
            with urllib.request.urlopen(req, timeout=5) as response:
                data = json.loads(response.read())
            latest_tag = data.get("tag_name", "").lstrip("v")
            if not latest_tag or latest_tag == VERSION:
                return
            # Semantische Versionsvergleich (tuple-Vergleich reicht für X.Y.Z)
            def parse_ver(v: str):
                try:
                    return tuple(int(x) for x in v.split("."))
                except ValueError:
                    return (0, 0, 0)
            if parse_ver(latest_tag) > parse_ver(VERSION):
                GLib.idle_add(self._show_update_banner, latest_tag)
        except Exception as e:
            logger.debug(f"Update-Check fehlgeschlagen: {e}")

    def _show_update_banner(self, latest_version: str):
        """Zeigt Update-Banner wenn neue Version verfügbar (v0.4.0 / Issue #19)"""
        self.update_banner.set_title(
            f"MyApps v{latest_version} " + _("ist verfügbar")
        )
        pm, cmd = self._detect_update_manager()
        self._update_pm = pm
        self._update_cmd = cmd
        if pm in ("apt", "dnf", "zypper"):
            self.update_banner.set_button_label(_("Aktualisieren"))
        else:
            self.update_banner.set_button_label(_("Changelog"))
        self.update_banner.set_revealed(True)
        return GLib.SOURCE_REMOVE

    def _detect_update_manager(self):
        """Erkennt den passenden Update-Befehl für MyApps (Issue #19)"""
        pm_names = self.gui.distro_info.package_managers
        if "dpkg" in pm_names:
            return "apt", ["pkexec", "apt-get", "install", "--only-upgrade", "-y", "myapps"]
        if "dnf" in pm_names:
            return "dnf", ["pkexec", "dnf", "upgrade", "-y", "myapps"]
        if "zypper" in pm_names:
            return "zypper", ["pkexec", "zypper", "--non-interactive", "update", "myapps"]
        if "pacman" in pm_names:
            return "pacman", None  # AUR: kein automatischer Update möglich
        return None, None

    def _on_update_banner_clicked(self, banner):
        """Reagiert auf Banner-Klick: Auto-Update oder Changelog (Issue #19)"""
        if self._update_pm in ("apt", "dnf", "zypper") and self._update_cmd:
            self._run_auto_update()
        elif self._update_pm == "pacman":
            self._show_arch_update_hint()
        else:
            import webbrowser
            webbrowser.open("https://github.com/nicolettas-muggelbude/myapps/releases/latest")

    def _run_auto_update(self):
        """Startet MyApps-Update im Hintergrund-Thread (Issue #19)"""
        self.update_banner.set_button_label("…")
        self._set_status(_("Aktualisierung wird durchgeführt…"))
        thread = threading.Thread(target=self._auto_update_worker, daemon=True)
        thread.start()

    def _auto_update_worker(self):
        """Führt pkexec-Upgrade-Befehl aus (Issue #19)"""
        try:
            result = subprocess.run(
                self._update_cmd,
                capture_output=True, text=True, timeout=120
            )
            success = result.returncode == 0
            output = (result.stdout + result.stderr).strip()
            GLib.idle_add(self._on_auto_update_done, success, output)
        except subprocess.TimeoutExpired:
            GLib.idle_add(self._on_auto_update_done, False, _("Zeitüberschreitung (>120 s)"))
        except Exception as e:
            GLib.idle_add(self._on_auto_update_done, False, str(e))

    def _on_auto_update_done(self, success: bool, output: str):
        """Zeigt Ergebnis des Auto-Updates (Issue #19)"""
        if success:
            self.update_banner.set_revealed(False)
            self._set_status(_("Aktualisierung erfolgreich – App neu starten"))
            dialog = Adw.MessageDialog.new(
                self,
                _("Aktualisierung erfolgreich"),
                _("MyApps wurde aktualisiert. Bitte die App neu starten.")
            )
        else:
            self.update_banner.set_button_label(_("Aktualisieren"))
            self._set_status(_("Aktualisierung fehlgeschlagen"))
            dialog = Adw.MessageDialog.new(
                self,
                _("Aktualisierung fehlgeschlagen"),
                output[:500] if output else _("Unbekannter Fehler")
            )
        dialog.add_response("ok", "OK")
        dialog.set_default_response("ok")
        dialog.present()
        return GLib.SOURCE_REMOVE

    def _show_arch_update_hint(self):
        """Zeigt Hinweis für Arch-Nutzer: Update über AUR-Helper (Issue #19)"""
        dialog = Adw.MessageDialog.new(
            self,
            _("AUR-Paket aktualisieren"),
            _("MyApps wird über das AUR verteilt.\nBitte den AUR-Helper verwenden:\n\nyay -S myapps\nparu -S myapps")
        )
        dialog.add_response("changelog", _("Changelog öffnen"))
        dialog.add_response("ok", "OK")
        dialog.set_default_response("ok")
        dialog.connect("response", self._on_arch_hint_response)
        dialog.present()

    def _on_arch_hint_response(self, dialog, response):
        """Öffnet Changelog wenn gewählt (Issue #19)"""
        if response == "changelog":
            import webbrowser
            webbrowser.open("https://github.com/nicolettas-muggelbude/myapps/releases/latest")

    def _check_package_updates(self):
        """Startet Paket-Update-Check im Hintergrund-Thread (Issue #7)"""
        thread = threading.Thread(target=self._check_package_updates_worker, daemon=True)
        thread.start()

    def _check_package_updates_worker(self):
        """Prüft via Paketmanager welche Pakete Updates haben (Issue #7)"""
        try:
            pm_names = self.gui.distro_info.package_managers
            updatable = UpdateChecker().get_updatable_packages(pm_names)
            GLib.idle_add(self._apply_update_status, updatable)
        except Exception as e:
            logger.debug(f"Paket-Update-Check fehlgeschlagen: {e}")

    def _apply_update_status(self, updatable: set):
        """Setzt update_available auf allen Paketen und aktualisiert View (Issue #7)"""
        if not updatable:
            return GLib.SOURCE_REMOVE

        count = 0
        for pkg in self.gui.packages:
            pkg.update_available = pkg.name in updatable
            if pkg.update_available:
                count += 1

        self._populate_current_view()

        if count > 0:
            self._set_status(f"{count} " + _("Updates verfügbar"))
            if self.gui.settings.get("notifications_enabled", True):
                self._send_update_notification(count)

        return GLib.SOURCE_REMOVE

    def _populate_current_view(self):
        """Füllt die aktuelle View mit allen Daten (Virtual Scrolling, v0.4.0)"""
        current_view = self.stack.get_visible_child_name()

        if current_view == "list":
            self._populate_list_view()
        elif current_view == "desktop":
            self._populate_desktop_view()
        else:
            self._populate_table_view()

    def _populate_list_view(self):
        """
        Füllt ListView mit allen gefilterten Apps — Virtual Scrolling (v0.4.0).
        GTK4 rendert nur sichtbare Elemente. Lokalisierte Beschreibungen
        werden asynchron nachgeladen.
        """
        self.list_store.remove_all()
        packages = self.gui.search_filtered_packages

        # SOFORT rendern: gecachte Beschreibung oder englischer Fallback
        from .package_manager import Package
        for pkg in packages:
            cached_desc = self.localized_desc_cache.get(pkg.name)
            if cached_desc:
                pkg = Package(
                    name=pkg.name, version=pkg.version,
                    package_type=pkg.package_type, description=cached_desc,
                    size=pkg.size, install_date=pkg.install_date
                )
            self.list_store.append(PackageItem(pkg))

        # Nur fehlende deb-Beschreibungen asynchron nachladen
        missing = [
            pkg for pkg in packages
            if pkg.package_type == "deb" and pkg.name not in self.localized_desc_cache
        ]
        if not missing:
            return  # Alles gecacht → fertig

        def _load_in_background():
            from concurrent.futures import ThreadPoolExecutor, as_completed
            results = {}
            with ThreadPoolExecutor(max_workers=10) as executor:
                future_to_name = {
                    executor.submit(self._get_localized_description, pkg.name): pkg.name
                    for pkg in missing
                }
                for future in as_completed(future_to_name):
                    pkg_name = future_to_name[future]
                    try:
                        desc = future.result()
                        if desc:
                            results[pkg_name] = desc
                    except Exception:
                        pass
            GLib.idle_add(self._apply_localized_descriptions, results)

        threading.Thread(target=_load_in_background, daemon=True).start()

    def _apply_localized_descriptions(self, new_descriptions: dict):
        """
        Callback nach asynchronem Laden: Cache füllen und aktive View aktualisieren.
        Beim erneuten Rendern sind alle Descriptions gecacht → kein weiterer Thread.
        """
        self.localized_desc_cache.update(new_descriptions)
        if not new_descriptions:
            return GLib.SOURCE_REMOVE

        current_view = self.stack.get_visible_child_name()
        if current_view == "list":
            self._populate_list_view()
        elif current_view == "table":
            self._populate_table_view()

        return GLib.SOURCE_REMOVE

    def _populate_table_view(self):
        """
        Füllt Table View mit allen gefilterten Apps — Virtual Scrolling (v0.4.0).
        Gecachte Beschreibungen sofort, fehlende werden asynchron nachgeladen.
        """
        self.table_store.remove_all()
        packages = self.gui.search_filtered_packages

        # Gecachte Beschreibungen sofort anwenden
        from .package_manager import Package
        for pkg in packages:
            cached_desc = self.localized_desc_cache.get(pkg.name)
            if cached_desc:
                pkg = Package(
                    name=pkg.name, version=pkg.version,
                    package_type=pkg.package_type, description=cached_desc,
                    size=pkg.size, install_date=pkg.install_date
                )
            self.table_store.append(PackageItem(pkg))

        # Fehlende deb-Beschreibungen asynchron nachladen
        missing = [
            pkg for pkg in packages
            if pkg.package_type == "deb" and pkg.name not in self.localized_desc_cache
        ]
        if not missing:
            return

        def _load_in_background():
            from concurrent.futures import ThreadPoolExecutor, as_completed
            results = {}
            with ThreadPoolExecutor(max_workers=10) as executor:
                future_to_name = {
                    executor.submit(self._get_localized_description, pkg.name): pkg.name
                    for pkg in missing
                }
                for future in as_completed(future_to_name):
                    pkg_name = future_to_name[future]
                    try:
                        desc = future.result()
                        if desc:
                            results[pkg_name] = desc
                    except Exception:
                        pass
            GLib.idle_add(self._apply_localized_descriptions, results)

        threading.Thread(target=_load_in_background, daemon=True).start()

    def _populate_desktop_view(self):
        """
        Füllt Desktop-Apps View mit allen gefilterten Desktop-Apps (v0.3.1, Issue #4).
        Kein Paging — Virtual Scrolling reicht für typisch 50–300 Apps.
        """
        self.desktop_store.remove_all()
        for pkg in self.gui.desktop_filtered_packages:
            self.desktop_store.append(PackageItem(pkg))

    def _get_localized_description(self, package_name: str) -> Optional[str]:
        """Holt lokalisierte Beschreibung via apt-cache (nur für List View)"""
        import subprocess
        try:
            result = subprocess.run(
                ["apt-cache", "show", package_name],
                capture_output=True,
                text=True,
                timeout=2  # Timeout nach 2 Sekunden
            )
            if result.returncode == 0:
                # Parse für Description (respektiert LANG)
                for line in result.stdout.splitlines():
                    if line.startswith("Description:") or line.startswith("Description-de:"):
                        desc = line.split(":", 1)[1].strip()
                        return desc if desc else None
        except Exception:
            pass  # Bei Fehler: Nutze englische Beschreibung als Fallback
        return None

    def _update_count_label(self):
        """Aktualisiert die App-Anzahl in der Sort-Bar (v0.4.0)"""
        current_view = self.stack.get_visible_child_name()
        if current_view == "desktop":
            count = len(self.gui.desktop_filtered_packages)
            self.count_label.set_text(f"{count} " + _("Desktop-Apps"))
        else:
            count = len(self.gui.search_filtered_packages)
            self.count_label.set_text(f"{count} " + _("Apps"))

    def _on_refresh_clicked(self, button):
        """Refresh Button Handler"""
        # Caches leeren bei Refresh (v0.2.4 + v0.3.0)
        self.icon_cache.clear()
        self.localized_desc_cache.clear()

        self._set_status(_("Aktualisiere") + "...")
        GLib.idle_add(self.gui._start_loading_packages)

    def _on_export_clicked(self, button):
        """Export Button Handler"""
        if not self.gui.search_filtered_packages:
            dialog = Adw.MessageDialog.new(self)
            dialog.set_heading(_("Keine Pakete"))
            dialog.set_body(_("Keine Pakete zum Exportieren vorhanden"))
            dialog.add_response("ok", "OK")
            dialog.present()
            return

        # GTK4 FileChooserDialog (ohne parent in Constructor)
        dialog = Gtk.FileChooserDialog(
            title=_("Paketliste exportieren"),
            action=Gtk.FileChooserAction.SAVE
        )
        dialog.set_transient_for(self)  # Setze parent NACH Erstellung
        dialog.set_modal(True)

        dialog.add_buttons(
            _("Abbrechen"), Gtk.ResponseType.CANCEL,
            _("Exportieren"), Gtk.ResponseType.ACCEPT
        )
        dialog.set_current_name("myapps-export")

        # Setze Default-Ordner auf HOME
        import os
        home_folder = Gio.File.new_for_path(os.path.expanduser("~"))
        dialog.set_current_folder(home_folder)

        # Format Filter
        filter_txt = Gtk.FileFilter()
        filter_txt.set_name("Text (.txt)")
        filter_txt.add_pattern("*.txt")
        dialog.add_filter(filter_txt)

        filter_csv = Gtk.FileFilter()
        filter_csv.set_name("CSV (.csv)")
        filter_csv.add_pattern("*.csv")
        dialog.add_filter(filter_csv)

        filter_json = Gtk.FileFilter()
        filter_json.set_name("JSON (.json)")
        filter_json.add_pattern("*.json")
        dialog.add_filter(filter_json)

        dialog.connect("response", self._on_export_response)
        dialog.present()

    def _on_export_response(self, dialog, response):
        """Export Dialog Response"""
        if response == Gtk.ResponseType.ACCEPT:
            file = dialog.get_file()
            if file:
                file_path = file.get_path()

                # Ermittle Format aus aktuellem Filter
                current_filter = dialog.get_filter()
                filter_name = current_filter.get_name() if current_filter else "Text (.txt)"

                # Bestimme Format und Dateiendung basierend auf Filter
                if "CSV" in filter_name:
                    fmt = "csv"
                    extension = ".csv"
                elif "JSON" in filter_name:
                    fmt = "json"
                    extension = ".json"
                else:
                    fmt = "txt"
                    extension = ".txt"

                # Füge Dateiendung hinzu falls sie fehlt
                if not file_path.endswith(extension):
                    # Entferne evtl. falsche Endung (.txt vom Default)
                    if file_path.endswith(".txt") or file_path.endswith(".csv") or file_path.endswith(".json"):
                        file_path = file_path.rsplit(".", 1)[0]
                    file_path = file_path + extension

                # Prüfe ob Datei existiert und frage nach
                from pathlib import Path
                if Path(file_path).exists():
                    overwrite_dialog = Adw.MessageDialog.new(self)
                    overwrite_dialog.set_heading(_("Datei überschreiben?"))
                    overwrite_dialog.set_body(f"{_('Die Datei existiert bereits')}: {Path(file_path).name}")
                    overwrite_dialog.add_response("cancel", _("Abbrechen"))
                    overwrite_dialog.add_response("overwrite", _("Überschreiben"))
                    overwrite_dialog.set_response_appearance("overwrite", Adw.ResponseAppearance.DESTRUCTIVE)
                    overwrite_dialog.connect("response", self._on_overwrite_response, file_path, fmt)
                    overwrite_dialog.present()
                else:
                    # Datei existiert nicht, direkt exportieren
                    self._do_export(file_path, fmt)

        dialog.destroy()

    def _on_overwrite_response(self, dialog, response, file_path, fmt):
        """Überschreiben-Dialog Response"""
        if response == "overwrite":
            self._do_export(file_path, fmt)
        dialog.destroy()

    def _do_export(self, file_path, fmt):
        """Führt Export durch"""
        success = Exporter.export(self.gui.search_filtered_packages, file_path, fmt)

        if success:
            self._set_status(f"{_('Exportiert')}: {file_path}")
        else:
            self._set_status(_("Export fehlgeschlagen"))

    def _on_about(self, action, param):
        """About Dialog - Alles auf einer Seite wie vorher!"""
        import webbrowser

        # Dialog-Fenster
        dialog = Gtk.Window()
        dialog.set_transient_for(self)
        dialog.set_modal(True)
        dialog.set_title(_("Über MyApps"))
        dialog.set_default_size(550, 780)

        # ScrolledWindow für Inhalt
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_vexpand(True)
        dialog.set_child(scrolled)

        # Hauptcontainer
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        main_box.set_margin_start(30)
        main_box.set_margin_end(30)
        main_box.set_margin_top(20)
        main_box.set_margin_bottom(20)
        scrolled.set_child(main_box)

        # === TITEL ===
        title_label = Gtk.Label(label="MyApps")
        title_label.add_css_class("title-1")
        title_label.set_margin_bottom(5)
        main_box.append(title_label)

        # Version
        version_label = Gtk.Label(label=f"Version {VERSION}")
        version_label.add_css_class("title-3")
        version_label.add_css_class("dim-label")
        version_label.set_margin_bottom(20)
        main_box.append(version_label)

        # Beschreibung
        desc_label = Gtk.Label(
            label=_("Tool zum Auflisten und Verwalten installierter Linux-Anwendungen")
        )
        desc_label.set_wrap(True)
        desc_label.set_max_width_chars(50)
        desc_label.set_justify(Gtk.Justification.CENTER)
        desc_label.set_margin_bottom(20)
        main_box.append(desc_label)

        # Separator
        main_box.append(Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL))

        # === LINKS ===
        links_label = Gtk.Label(label="Links:")
        links_label.add_css_class("title-4")
        links_label.set_halign(Gtk.Align.START)
        links_label.set_margin_top(15)
        links_label.set_margin_bottom(5)
        main_box.append(links_label)

        # Link-Buttons
        links = [
            ("GitHub Repository", "https://github.com/nicolettas-muggelbude/myapps"),
            ("Dokumentation", "https://github.com/nicolettas-muggelbude/myapps#readme"),
            ("Fehler melden", "https://github.com/nicolettas-muggelbude/myapps/issues"),
            ("Telegram Community", "https://t.me/LinuxGuidesDECommunity"),
        ]

        for link_text, url in links:
            btn = Gtk.Button(label=link_text)
            btn.connect("clicked", lambda b, u=url: webbrowser.open(u))
            btn.set_margin_start(20)
            btn.set_margin_end(20)
            btn.set_margin_top(2)
            btn.set_margin_bottom(2)
            main_box.append(btn)

        # Separator
        sep2 = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        sep2.set_margin_top(15)
        main_box.append(sep2)

        # === UNTERSTÜTZEN ===
        support_label = Gtk.Label(label="💙 Projekt unterstützen:")
        support_label.add_css_class("title-4")
        support_label.set_halign(Gtk.Align.START)
        support_label.set_margin_top(15)
        support_label.set_margin_bottom(5)
        main_box.append(support_label)

        support_text = Gtk.Label(
            label="Wenn dir MyApps hilft, freue ich mich über eine kleine Spende!"
        )
        support_text.set_wrap(True)
        support_text.set_max_width_chars(50)
        support_text.set_halign(Gtk.Align.START)
        support_text.set_margin_start(20)
        support_text.set_margin_bottom(10)
        main_box.append(support_text)

        # Spenden-Button
        donate_btn = Gtk.Button(label="💰 Über PayPal spenden")
        donate_btn.add_css_class("suggested-action")
        donate_btn.connect("clicked", lambda b: webbrowser.open("https://www.paypal.com/ncp/payment/UYJ73YNEZ3KHL"))
        donate_btn.set_margin_start(20)
        donate_btn.set_margin_end(20)
        donate_btn.set_margin_bottom(5)
        main_box.append(donate_btn)

        # Spenden-Hinweis
        donate_hint = Gtk.Label(
            label="Spenden werden von der PC-Wittfoot UG verwaltet."
        )
        donate_hint.add_css_class("caption")
        donate_hint.add_css_class("dim-label")
        donate_hint.set_halign(Gtk.Align.START)
        donate_hint.set_margin_start(20)
        main_box.append(donate_hint)

        # Separator
        sep3 = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        sep3.set_margin_top(15)
        main_box.append(sep3)

        # === CREDITS ===
        credits_label = Gtk.Label(label="Credits:")
        credits_label.add_css_class("title-4")
        credits_label.set_halign(Gtk.Align.START)
        credits_label.set_margin_top(15)
        credits_label.set_margin_bottom(5)
        main_box.append(credits_label)

        credit_items = [
            "Entwickelt für die Linux Guides DE Community",
            "UI basiert auf GTK4 + Libadwaita",
            "Danke an alle Beta-Tester und Contributors!"
        ]

        for credit in credit_items:
            credit_label = Gtk.Label(label=credit)
            credit_label.set_halign(Gtk.Align.START)
            credit_label.set_margin_start(20)
            credit_label.set_margin_top(2)
            main_box.append(credit_label)

        # Separator
        sep4 = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        sep4.set_margin_top(15)
        main_box.append(sep4)

        # === NEU IN AKTUELLER VERSION ===
        whats_new_label = Gtk.Label(label=f"✨ Neu in Version {VERSION}:")
        whats_new_label.add_css_class("title-4")
        whats_new_label.set_halign(Gtk.Align.START)
        whats_new_label.set_margin_top(15)
        whats_new_label.set_margin_bottom(5)
        main_box.append(whats_new_label)

        # Lade Features aus WHATS_NEW.md
        new_features = get_whats_new(VERSION)

        # Zeige Features (oder Fallback-Nachricht)
        if new_features:
            for feature in new_features:
                feature_label = Gtk.Label(label=f"• {feature}")
                feature_label.set_halign(Gtk.Align.START)
                feature_label.set_wrap(True)
                feature_label.set_max_width_chars(48)
                feature_label.set_margin_start(20)
                feature_label.set_margin_top(2)
                main_box.append(feature_label)
        else:
            # Fallback wenn keine Features gefunden
            no_info_label = Gtk.Label(label="Keine Changelog-Informationen verfügbar.")
            no_info_label.add_css_class("dim-label")
            no_info_label.set_halign(Gtk.Align.START)
            no_info_label.set_margin_start(20)
            main_box.append(no_info_label)

        # Danke-Text
        thanks_label = Gtk.Label(label="Danke fürs Testen! 🎉")
        thanks_label.set_halign(Gtk.Align.START)
        thanks_label.set_margin_start(20)
        thanks_label.set_margin_top(10)
        main_box.append(thanks_label)

        # Separator
        sep5 = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        sep5.set_margin_top(15)
        main_box.append(sep5)

        # === LIZENZ ===
        license_label = Gtk.Label(
            label="Lizenziert unter GNU General Public License v3.0"
        )
        license_label.add_css_class("dim-label")
        license_label.set_margin_top(15)
        license_label.set_margin_bottom(15)
        main_box.append(license_label)

        # === SCHLIESSEN-BUTTON ===
        close_btn = Gtk.Button(label=_("Schließen"))
        close_btn.add_css_class("pill")
        close_btn.set_halign(Gtk.Align.CENTER)
        close_btn.connect("clicked", lambda b: dialog.close())
        close_btn.set_size_request(200, -1)
        close_btn.set_margin_bottom(10)
        main_box.append(close_btn)

        dialog.present()

    def _set_status(self, message):
        """Setzt Statusbar Text"""
        self.statusbar.pop(self.status_context)
        self.statusbar.push(self.status_context, message)
