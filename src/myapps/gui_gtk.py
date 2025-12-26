"""
GTK4 + Libadwaita GUI für MyApps
Native Linux Desktop Integration mit Virtual Scrolling
"""

import logging
import threading
from pathlib import Path
from typing import List, Optional

# GTK4 + Libadwaita
import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw, Gio, GLib, GdkPixbuf, GObject

# MyApps Modules (bleiben gleich!)
from .package_manager import Package, PackageManagerFactory
from .filters import FilterManager
from .export import Exporter
from .distro_detect import get_distro_info
from .i18n import _

logger = logging.getLogger(__name__)

# Version
VERSION = "0.2.0-dev"


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

        # Pagination (gleiche Logik wie tkinter)
        self.current_page = 0
        self.items_per_page = 100
        self.total_pages = 0

        # Manager initialisieren (UNVERÄNDERT!)
        self.distro_info = get_distro_info()
        self.filter_manager = FilterManager(str(self.base_dir / "filters"))

        # Filter laden
        from .distro_detect import get_filter_files
        filter_files = get_filter_files()
        self.filter_manager.load_filters(filter_files)

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

        # Pagination Bar
        self.pagination_bar = self._create_pagination_bar()
        main_box.append(self.pagination_bar)

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

        # Menu Button (rechts)
        menu_btn = Gtk.MenuButton()
        menu_btn.set_icon_name("open-menu-symbolic")
        menu_btn.set_menu_model(self._create_menu())
        header.pack_end(menu_btn)

        return header

    def _create_menu(self):
        """Erstellt das Hauptmenü"""
        menu = Gio.Menu()

        # About
        menu.append(_("Über MyApps"), "app.about")

        # Quit
        menu.append(_("Beenden"), "app.quit")

        # Actions registrieren
        about_action = Gio.SimpleAction.new("about", None)
        about_action.connect("activate", self._on_about)
        self.gui.add_action(about_action)

        quit_action = Gio.SimpleAction.new("quit", None)
        quit_action.connect("activate", lambda *_: self.gui.quit())
        self.gui.add_action(quit_action)

        return menu

    def _create_pagination_bar(self):
        """Erstellt die Pagination Navigation"""
        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        box.set_margin_start(12)
        box.set_margin_end(12)
        box.set_margin_top(6)
        box.set_margin_bottom(6)

        # Info Label (links)
        info_label = Gtk.Label(label="ℹ️  " + _("Zeigt 100 Apps pro Seite"))
        info_label.add_css_class("dim-label")
        info_label.set_halign(Gtk.Align.START)
        box.append(info_label)

        # Spacer
        spacer = Gtk.Box()
        spacer.set_hexpand(True)
        box.append(spacer)

        # Navigation (rechts)
        nav_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        nav_box.set_halign(Gtk.Align.END)

        self.prev_btn = Gtk.Button(label="◀ " + _("Zurück"))
        self.prev_btn.set_sensitive(False)
        self.prev_btn.connect("clicked", lambda *_: self._prev_page())
        nav_box.append(self.prev_btn)

        self.page_label = Gtk.Label(label=_("Seite 0 von 0"))
        self.page_label.add_css_class("title-4")
        self.page_label.set_margin_start(12)
        self.page_label.set_margin_end(12)
        nav_box.append(self.page_label)

        self.next_btn = Gtk.Button(label=_("Weiter") + " ▶")
        self.next_btn.set_sensitive(False)
        self.next_btn.connect("clicked", lambda *_: self._next_page())
        nav_box.append(self.next_btn)

        box.append(nav_box)

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

        # Text Container
        text_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        text_box.set_hexpand(True)

        # Name Label
        name_label = Gtk.Label()
        name_label.set_halign(Gtk.Align.START)
        name_label.add_css_class("title-4")
        text_box.append(name_label)

        # Info Label (Version + Typ)
        info_label = Gtk.Label()
        info_label.set_halign(Gtk.Align.START)
        info_label.add_css_class("dim-label")
        info_label.add_css_class("caption")
        text_box.append(info_label)

        box.append(text_box)

        # Context Menu Setup
        gesture = Gtk.GestureClick.new()
        gesture.set_button(3)  # Rechtsklick
        box.add_controller(gesture)

        # Store widgets für später
        box.name_label = name_label
        box.info_label = info_label
        box.gesture = gesture

        list_item.set_child(box)

    def _on_list_bind(self, factory, list_item):
        """Bind: Verknüpft Package-Daten mit Widget"""
        pkg = list_item.get_item()  # PackageItem-Objekt
        box = list_item.get_child()

        # Set Data
        box.name_label.set_text(pkg.name)
        box.info_label.set_text(f"{pkg.version}  •  {pkg.package_type.upper()}")

        # Tooltip: Zeigt Paketbeschreibung (Funktion des Pakets)
        if pkg.description:
            # Beschreibung vorhanden: Zeige nur diese (Info ist bereits sichtbar in der Liste)
            tooltip = pkg.description
        else:
            # Keine Beschreibung: Zeige zumindest Paketname als Fallback
            tooltip = f"{pkg.name}\n(Keine Beschreibung verfügbar)"

        box.set_has_tooltip(True)
        box.set_tooltip_text(tooltip)

        # Context Menu Handler
        def on_right_click(gesture, n_press, x, y):
            self._show_context_menu(box, pkg, x, y)

        box.gesture.connect("pressed", on_right_click)

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
        self._add_column(column_view, _("Typ"), "package_type")
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
        self._update_pagination_controls()
        self._populate_current_view()
        self._set_status(f"{len(packages)} Apps " + _("geladen"))
        return GLib.SOURCE_REMOVE

    def _on_loading_error(self, error_msg):
        """Callback bei Lade-Fehler"""
        self._set_status(f"Fehler: {error_msg}")
        return GLib.SOURCE_REMOVE

    def _populate_current_view(self):
        """Füllt die aktuelle View mit Daten (paginiert)"""
        current_view = self.stack.get_visible_child_name()

        if current_view == "list":
            self._populate_list_view()
        else:
            self._populate_table_view()

    def _populate_list_view(self):
        """Füllt ListView (paginiert) mit lokalisierten Beschreibungen"""
        # Clear
        self.list_store.remove_all()

        # Pagination Range
        start_idx = self.gui.current_page * self.gui.items_per_page
        end_idx = min(start_idx + self.gui.items_per_page, len(self.gui.filtered_packages))

        # Sortieren
        sorted_packages = sorted(self.gui.filtered_packages, key=lambda p: (p.package_type, p.name))
        page_packages = sorted_packages[start_idx:end_idx]

        # Hole lokalisierte Beschreibungen PARALLEL für dpkg-Pakete
        deb_packages = [pkg for pkg in page_packages if pkg.package_type == "deb"]
        localized_descriptions = {}

        if deb_packages:
            from concurrent.futures import ThreadPoolExecutor, as_completed
            with ThreadPoolExecutor(max_workers=10) as executor:
                # Starte parallele apt-cache Aufrufe
                future_to_pkg = {
                    executor.submit(self._get_localized_description, pkg.name): pkg.name
                    for pkg in deb_packages
                }

                # Sammle Ergebnisse
                for future in as_completed(future_to_pkg):
                    pkg_name = future_to_pkg[future]
                    try:
                        desc = future.result()
                        if desc:
                            localized_descriptions[pkg_name] = desc
                    except Exception:
                        pass  # Fallback auf englische Beschreibung

        # Add to Model (wrapped in PackageItem) mit lokalisierten Beschreibungen
        from .package_manager import Package
        for pkg in page_packages:
            # Nutze lokalisierte Beschreibung falls vorhanden
            if pkg.name in localized_descriptions:
                pkg = Package(
                    name=pkg.name,
                    version=pkg.version,
                    package_type=pkg.package_type,
                    description=localized_descriptions[pkg.name]
                )

            self.list_store.append(PackageItem(pkg))

    def _populate_table_view(self):
        """Füllt Table View (paginiert)"""
        # Clear
        self.table_store.remove_all()

        # Pagination Range
        start_idx = self.gui.current_page * self.gui.items_per_page
        end_idx = min(start_idx + self.gui.items_per_page, len(self.gui.filtered_packages))

        # Sortieren
        sorted_packages = sorted(self.gui.filtered_packages, key=lambda p: (p.package_type, p.name))
        page_packages = sorted_packages[start_idx:end_idx]

        # Add to Model (wrapped in PackageItem)
        for pkg in page_packages:
            self.table_store.append(PackageItem(pkg))

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

    def _update_pagination_controls(self):
        """Aktualisiert Pagination Controls"""
        if self.gui.filtered_packages:
            self.gui.total_pages = (len(self.gui.filtered_packages) + self.gui.items_per_page - 1) // self.gui.items_per_page
        else:
            self.gui.total_pages = 0

        # Adjust current page
        if self.gui.current_page >= self.gui.total_pages:
            self.gui.current_page = max(0, self.gui.total_pages - 1)

        # Update Label
        if self.gui.total_pages > 0:
            start_idx = self.gui.current_page * self.gui.items_per_page + 1
            end_idx = min((self.gui.current_page + 1) * self.gui.items_per_page, len(self.gui.filtered_packages))
            self.page_label.set_text(
                f"{_('Seite')} {self.gui.current_page + 1} {_('von')} {self.gui.total_pages}  •  "
                f"Apps {start_idx}-{end_idx} {_('von')} {len(self.gui.filtered_packages)}"
            )
        else:
            self.page_label.set_text(_("Keine Apps"))

        # Update Buttons
        self.prev_btn.set_sensitive(self.gui.current_page > 0)
        self.next_btn.set_sensitive(self.gui.current_page < self.gui.total_pages - 1)

    def _prev_page(self):
        """Vorherige Seite"""
        if self.gui.current_page > 0:
            self.gui.current_page -= 1
            self._update_pagination_controls()
            self._populate_current_view()

    def _next_page(self):
        """Nächste Seite"""
        if self.gui.current_page < self.gui.total_pages - 1:
            self.gui.current_page += 1
            self._update_pagination_controls()
            self._populate_current_view()

    def _on_refresh_clicked(self, button):
        """Refresh Button Handler"""
        self.gui.current_page = 0
        self._set_status(_("Aktualisiere") + "...")
        GLib.idle_add(self.gui._start_loading_packages)

    def _on_export_clicked(self, button):
        """Export Button Handler"""
        if not self.gui.filtered_packages:
            dialog = Adw.MessageDialog.new(self)
            dialog.set_heading(_("Keine Pakete"))
            dialog.set_body(_("Keine Pakete zum Exportieren vorhanden"))
            dialog.add_response("ok", "OK")
            dialog.present()
            return

        # File Chooser Dialog
        dialog = Gtk.FileChooserDialog(
            title=_("Paketliste exportieren"),
            parent=self,
            action=Gtk.FileChooserAction.SAVE
        )
        dialog.add_buttons(
            _("Abbrechen"), Gtk.ResponseType.CANCEL,
            _("Exportieren"), Gtk.ResponseType.ACCEPT
        )
        dialog.set_current_name("myapps-export.txt")

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

                # Format aus Dateiendung ermitteln
                fmt = "txt"
                if file_path.endswith(".csv"):
                    fmt = "csv"
                elif file_path.endswith(".json"):
                    fmt = "json"

                # Export durchführen
                success = Exporter.export(self.gui.filtered_packages, file_path, fmt)

                if success:
                    self._set_status(f"{_('Exportiert')}: {file_path}")
                else:
                    self._set_status(_("Export fehlgeschlagen"))

        dialog.destroy()

    def _on_about(self, action, param):
        """About Dialog"""
        about = Adw.AboutWindow()
        about.set_transient_for(self)
        about.set_application_name("MyApps")
        about.set_version(VERSION)
        about.set_developer_name("Linux Guides DE Community")
        about.set_license_type(Gtk.License.GPL_3_0)
        about.set_website("https://github.com/nicolettas-muggelbude/myapps")
        about.set_issue_url("https://github.com/nicolettas-muggelbude/myapps/issues")
        about.set_developers(["nicolettas-muggelbude", "Linux Guides DE Community Contributors"])
        about.set_comments(_("Tool zum Auflisten und Verwalten installierter Linux-Anwendungen"))

        # Spenden-Link (PC-Wittfoot UG verwaltet NUR Spenden, nicht Entwicklung!)
        about.add_link(_("Spenden via PayPal (verwaltet von PC-Wittfoot UG)"), "https://www.paypal.com/ncp/payment/UYJ73YNEZ3KHL")

        about.present()

    def _set_status(self, message):
        """Setzt Statusbar Text"""
        self.statusbar.pop(self.status_context)
        self.statusbar.push(self.status_context, message)
