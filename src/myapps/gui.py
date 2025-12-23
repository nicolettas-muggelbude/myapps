"""
GUI-Modul für MyApps mit ttkbootstrap
Bietet Tabellen- und Listenansicht mit Dark Mode
"""

import logging
import threading
import webbrowser
from pathlib import Path
from tkinter import filedialog, messagebox
from typing import List, Optional

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox
from ttkbootstrap.tooltip import ToolTip

from .package_manager import Package, PackageManagerFactory
from .filters import FilterManager
from .icons import IconManager
from .export import Exporter
from .distro_detect import get_distro_info, get_filter_files
from .i18n import _

logger = logging.getLogger(__name__)

# Version (wird aus pyproject.toml gelesen oder manuell gesetzt)
VERSION = "0.1.0-alpha"


class MyAppsGUI:
    """Hauptfenster der MyApps-Anwendung"""

    def __init__(self, base_dir: str):
        """
        Initialisiert die GUI

        Args:
            base_dir: Basis-Verzeichnis der Anwendung
        """
        self.base_dir = Path(base_dir)
        self.packages: List[Package] = []
        self.filtered_packages: List[Package] = []
        self.current_view = "list"  # "table" oder "list"

        # Initialisiere Manager
        self.distro_info = get_distro_info()
        self.filter_manager = FilterManager(str(self.base_dir / "filters"))
        self.icon_manager = IconManager(
            icon_size=32,
            fallback_dir=str(self.base_dir / "assets" / "icons")
        )

        # Cache für Paketbeschreibungen (lazy loading)
        self.description_cache = {}

        # Lade Filter
        filter_files = get_filter_files()
        self.filter_manager.load_filters(filter_files)

        # Erstelle Hauptfenster
        self.root = ttk.Window(
            title=f"MyApps v{VERSION} - " + _("Installierte Anwendungen"),
            themename="darkly",  # Dark Mode Theme
            size=(1200, 850)
        )

        self._build_gui()
        self._load_packages_async()

    def _build_gui(self) -> None:
        """Baut die GUI-Struktur auf"""

        # Toolbar
        self._build_toolbar()

        # Hauptbereich (mit Frame für View-Wechsel)
        self.main_frame = ttk.Frame(self.root, padding=10)
        self.main_frame.pack(fill=BOTH, expand=YES)

        # Erstelle beide Views (aber zeige nur eine)
        self.table_view = self._create_table_view()
        self.list_view = self._create_list_view()

        # Zeige initial Listenansicht
        self.list_view.pack(fill=BOTH, expand=YES)

        # Statusleiste
        self._build_statusbar()

    def _build_toolbar(self) -> None:
        """Erstellt die Toolbar"""
        toolbar = ttk.Frame(self.root, padding=5)
        toolbar.pack(fill=X, side=TOP)

        # Linke Seite - Haupt-Buttons
        left_frame = ttk.Frame(toolbar)
        left_frame.pack(side=LEFT, fill=X, expand=YES)

        ttk.Button(
            left_frame,
            text=_("Aktualisieren"),
            command=self._refresh_packages,
            bootstyle=PRIMARY
        ).pack(side=LEFT, padx=5)

        ttk.Button(
            left_frame,
            text=_("Exportieren"),
            command=self._show_export_dialog,
            bootstyle=SUCCESS
        ).pack(side=LEFT, padx=5)

        ttk.Button(
            left_frame,
            text=_("Ansicht wechseln"),
            command=self._toggle_view,
            bootstyle=INFO
        ).pack(side=LEFT, padx=5)

        # Rechte Seite - Info
        right_frame = ttk.Frame(toolbar)
        right_frame.pack(side=RIGHT)

        info_btn = ttk.Button(
            right_frame,
            text="ⓘ " + _("Info"),
            command=self._show_about_dialog,
            bootstyle=SECONDARY
        )
        info_btn.pack(side=RIGHT, padx=5)
        ToolTip(info_btn, text=_("Über MyApps"))

        # Distro-Info
        distro_label = ttk.Label(
            right_frame,
            text=f"🐧 {self.distro_info.pretty_name}",
            bootstyle=SECONDARY
        )
        distro_label.pack(side=RIGHT, padx=10)

    def _build_statusbar(self) -> None:
        """Erstellt die Statusleiste"""
        statusbar = ttk.Frame(self.root, relief=SUNKEN)
        statusbar.pack(fill=X, side=BOTTOM)

        self.status_label = ttk.Label(
            statusbar,
            text=_("Bereit"),
            anchor=W
        )
        self.status_label.pack(side=LEFT, fill=X, expand=YES, padx=5, pady=2)

        # Progressbar (initial versteckt)
        self.progress = ttk.Progressbar(
            statusbar,
            mode='indeterminate',
            bootstyle=PRIMARY
        )

    def _create_table_view(self) -> ttk.Frame:
        """
        Erstellt die Tabellenansicht

        Returns:
            Frame mit Tabellenansicht
        """
        frame = ttk.Frame(self.main_frame)

        # Scrollbars
        y_scrollbar = ttk.Scrollbar(frame, orient=VERTICAL)
        y_scrollbar.pack(side=RIGHT, fill=Y)

        x_scrollbar = ttk.Scrollbar(frame, orient=HORIZONTAL)
        x_scrollbar.pack(side=BOTTOM, fill=X)

        # Treeview (Tabelle)
        self.tree = ttk.Treeview(
            frame,
            columns=("name", "version", "type", "description"),
            show="tree headings",
            yscrollcommand=y_scrollbar.set,
            xscrollcommand=x_scrollbar.set,
            bootstyle=PRIMARY
        )

        # Configure scrollbars
        y_scrollbar.config(command=self.tree.yview)
        x_scrollbar.config(command=self.tree.xview)

        # Spalten-Konfiguration
        self.tree.heading("#0", text="🖼️")  # Icon-Spalte
        self.tree.heading("name", text=_("Name"))
        self.tree.heading("version", text=_("Version"))
        self.tree.heading("type", text=_("Typ"))
        self.tree.heading("description", text=_("Beschreibung"))

        self.tree.column("#0", width=50, stretch=NO)
        self.tree.column("name", width=250)
        self.tree.column("version", width=120)
        self.tree.column("type", width=80)
        self.tree.column("description", width=400)

        self.tree.pack(fill=BOTH, expand=YES)

        # Kontextmenü
        self.tree.bind("<Button-3>", self._show_context_menu)

        return frame

    def _create_list_view(self) -> ttk.Frame:
        """
        Erstellt die Listenansicht

        Returns:
            Frame mit Listenansicht
        """
        frame = ttk.Frame(self.main_frame)

        # Scrollbar
        scrollbar = ttk.Scrollbar(frame, orient=VERTICAL)
        scrollbar.pack(side=RIGHT, fill=Y)

        # Canvas für scrollbare Liste
        self.list_canvas = ttk.Canvas(frame, yscrollcommand=scrollbar.set)
        self.list_canvas.pack(side=LEFT, fill=BOTH, expand=YES)

        scrollbar.config(command=self.list_canvas.yview)

        # Frame innerhalb des Canvas
        self.list_inner_frame = ttk.Frame(self.list_canvas)
        self.list_canvas_window = self.list_canvas.create_window(
            0, 0,
            window=self.list_inner_frame,
            anchor=NW
        )

        # Update scroll region beim Größenänderung
        self.list_inner_frame.bind("<Configure>", self._on_list_configure)
        self.list_canvas.bind("<Configure>", self._on_canvas_configure)

        # Mausrad-Scrolling aktivieren (auf Canvas)
        self._bind_mousewheel(self.list_canvas)

        return frame

    def _on_list_configure(self, event) -> None:
        """Update scroll region der Liste"""
        self.list_canvas.configure(scrollregion=self.list_canvas.bbox("all"))

    def _on_canvas_configure(self, event) -> None:
        """Update width des inner frame beim Canvas-Resize"""
        self.list_canvas.itemconfig(self.list_canvas_window, width=event.width)

    def _bind_mousewheel(self, widget) -> None:
        """
        Bindet Mausrad-Scrolling rekursiv an Widget und alle Kinder

        Args:
            widget: Widget zum Binden
        """
        widget.bind("<MouseWheel>", self._on_mousewheel)
        widget.bind("<Button-4>", self._on_mousewheel)
        widget.bind("<Button-5>", self._on_mousewheel)

        # Rekursiv für alle Kinder
        for child in widget.winfo_children():
            self._bind_mousewheel(child)

    def _on_mousewheel(self, event) -> None:
        """Behandelt Mausrad-Scrolling"""
        if event.num == 4 or event.delta > 0:
            # Scroll up (Linux Button-4 oder Windows/Mac positive delta)
            self.list_canvas.yview_scroll(-1, "units")
        elif event.num == 5 or event.delta < 0:
            # Scroll down (Linux Button-5 oder Windows/Mac negative delta)
            self.list_canvas.yview_scroll(1, "units")

    def _toggle_view(self) -> None:
        """Wechselt zwischen Tabellen- und Listenansicht"""
        if self.current_view == "table":
            # Wechsel zu Liste
            self.table_view.pack_forget()
            self.list_view.pack(fill=BOTH, expand=YES)
            self.current_view = "list"
            self._populate_list_view()
        else:
            # Wechsel zu Tabelle
            self.list_view.pack_forget()
            self.table_view.pack(fill=BOTH, expand=YES)
            self.current_view = "table"
            self._populate_table_view()

        logger.info(f"Ansicht gewechselt zu: {self.current_view}")

    def _load_packages_async(self) -> None:
        """Lädt Pakete asynchron"""
        self._set_status(_("Lade Pakete..."), show_progress=True)

        def load_worker():
            try:
                # Lade Pakete
                package_managers = self.distro_info.package_managers
                self.packages = PackageManagerFactory.get_all_packages(package_managers)

                # Filtere System-Apps
                self._set_status(_("Filtere System-Apps..."))
                self.filtered_packages = self.filter_manager.filter_packages(self.packages)

                # Icon-Preloading deaktiviert (verursacht X-Server Memory-Fehler bei vielen Paketen)
                # Icons werden lazy on-demand geladen via get_icon() mit Cache
                # self.icon_manager.preload_icons(self.filtered_packages)

                # Update GUI im Hauptthread
                self.root.after(0, self._update_display)

            except Exception as e:
                logger.error(f"Fehler beim Laden der Pakete: {e}")
                self.root.after(0, lambda: self._set_status(f"Fehler: {e}", show_progress=False))

        thread = threading.Thread(target=load_worker, daemon=True)
        thread.start()

    def _update_display(self) -> None:
        """Aktualisiert die Anzeige mit geladenen Paketen"""
        if self.current_view == "table":
            self._populate_table_view()
        else:
            self._populate_list_view()

        # Update Status
        count = len(self.filtered_packages)
        self._set_status(_("Bereit") + f" - {count} Apps", show_progress=False)

    def _populate_table_view(self) -> None:
        """Füllt die Tabellenansicht mit Daten"""
        # Leere bestehende Einträge
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Füge Pakete hinzu
        for pkg in sorted(self.filtered_packages, key=lambda p: (p.package_type, p.name)):
            icon = self.icon_manager.get_icon(pkg.name, pkg.package_type)

            self.tree.insert(
                "",
                END,
                image=icon,
                values=(pkg.name, pkg.version, pkg.package_type.upper(), pkg.description or ""),
                tags=(pkg.package_type,)
            )

        # Behalte Icon-Referenzen (wichtig für tkinter)
        self.tree.image_references = [
            self.icon_manager.get_icon(pkg.name, pkg.package_type)
            for pkg in self.filtered_packages
        ]

    def _populate_list_view(self) -> None:
        """Füllt die Listenansicht mit Daten"""
        # Leere bestehende Widgets
        for widget in self.list_inner_frame.winfo_children():
            widget.destroy()

        # Gruppiere nach Typ
        grouped = {}
        for pkg in self.filtered_packages:
            if pkg.package_type not in grouped:
                grouped[pkg.package_type] = []
            grouped[pkg.package_type].append(pkg)

        # Erstelle Einträge gruppiert
        for pkg_type, pkgs in sorted(grouped.items()):
            # Gruppen-Header (minimalistisch)
            header_label = ttk.Label(
                self.list_inner_frame,
                text=f"{pkg_type.upper()} • {len(pkgs)} Apps",
                font=("TkDefaultFont", 9, "bold"),
                foreground="#888888"
            )
            header_label.pack(anchor=W, padx=15, pady=(15, 5))

            # Pakete in dieser Gruppe
            for pkg in sorted(pkgs, key=lambda p: p.name):
                self._create_list_item(pkg)

        # Update scroll region nach dem Füllen
        self.list_inner_frame.update_idletasks()
        self.list_canvas.configure(scrollregion=self.list_canvas.bbox("all"))

        # Binde Mausrad-Events an alle neuen Widgets
        self._bind_mousewheel(self.list_inner_frame)

    def _create_list_item(self, pkg: Package) -> None:
        """
        Erstellt ein List-Item für ein Paket (Messenger-Stil)

        Args:
            pkg: Package-Objekt
        """
        # Container für Hover-Effekt
        item_container = ttk.Frame(self.list_inner_frame)
        item_container.pack(fill=X, padx=0, pady=0)

        # Hauptframe (transparent, kein Hintergrund)
        item_frame = ttk.Frame(item_container)
        item_frame.pack(fill=X, padx=10, pady=8)

        # Icon
        icon = self.icon_manager.get_icon(pkg.name, pkg.package_type)
        icon_label = ttk.Label(item_frame, image=icon)
        icon_label.image = icon  # Behalte Referenz
        icon_label.pack(side=LEFT, padx=(0, 12))

        # Text-Info Container
        text_frame = ttk.Frame(item_frame)
        text_frame.pack(side=LEFT, fill=X, expand=YES)

        # Name (groß, fett, gut lesbar)
        name_label = ttk.Label(
            text_frame,
            text=pkg.name,
            font=("TkDefaultFont", 11)
        )
        name_label.pack(anchor=W)

        # Version & Typ (klein, grau, diskret)
        info_label = ttk.Label(
            text_frame,
            text=f"{pkg.version}  •  {pkg.package_type.upper()}",
            font=("TkDefaultFont", 9),
            foreground="#888888"
        )
        info_label.pack(anchor=W, pady=(2, 0))

        # Dünne Trennlinie (sehr dezent)
        separator = ttk.Separator(item_container, orient="horizontal")
        separator.pack(fill=X, padx=20)

        # Binde Rechtsklick für alle Widgets
        for widget in [item_frame, icon_label, text_frame, name_label, info_label]:
            widget.bind("<Button-3>", lambda e, p=pkg: self._show_item_context_menu(e, p))

        # Tooltip mit lazy-loaded Beschreibung (nur auf Name)
        self._bind_tooltip(name_label, pkg)

    def _show_context_menu(self, event) -> None:
        """Zeigt Kontextmenü für Tabellenansicht"""
        item = self.tree.identify_row(event.y)
        if not item:
            return

        self.tree.selection_set(item)
        values = self.tree.item(item, "values")
        if not values:
            return

        package_name = values[0]

        # Erstelle Kontextmenü
        menu = ttk.Menu(self.root)
        menu.add_command(
            label=_("Als System-App markieren"),
            command=lambda: self._hide_package(package_name)
        )
        menu.add_command(
            label=_("Namen kopieren"),
            command=lambda: self._copy_to_clipboard(package_name)
        )

        menu.post(event.x_root, event.y_root)

    def _show_item_context_menu(self, event, pkg: Package) -> None:
        """Zeigt Kontextmenü für Listenansicht"""
        menu = ttk.Menu(self.root)
        menu.add_command(
            label=_("Als System-App markieren"),
            command=lambda: self._hide_package(pkg.name)
        )
        menu.add_command(
            label=_("Namen kopieren"),
            command=lambda: self._copy_to_clipboard(pkg.name)
        )

        menu.post(event.x_root, event.y_root)

    def _hide_package(self, package_name: str) -> None:
        """Markiert ein Paket als System-App (filtert es)"""
        if self.filter_manager.save_user_filter(package_name):
            Messagebox.show_info(
                f"'{package_name}' wurde zur Filterliste hinzugefügt.",
                title="Filter hinzugefügt"
            )
            self._refresh_packages()
        else:
            Messagebox.show_error(
                "Fehler beim Hinzufügen des Filters",
                title="Fehler"
            )

    def _copy_to_clipboard(self, text: str) -> None:
        """Kopiert Text in die Zwischenablage"""
        self.root.clipboard_clear()
        self.root.clipboard_append(text)
        self._set_status(f"'{text}' in Zwischenablage kopiert")

    def _refresh_packages(self) -> None:
        """Aktualisiert die Paketliste"""
        self.icon_manager.clear_cache()
        self._load_packages_async()

    def _show_export_dialog(self) -> None:
        """Zeigt modernen Export-Dialog"""
        if not self.filtered_packages:
            Messagebox.show_warning(
                "Keine Pakete zum Exportieren vorhanden",
                title=_("Export")
            )
            return

        # Erstelle modernen Export-Dialog
        dialog = ttk.Toplevel(self.root)
        dialog.title("Exportieren")
        dialog.geometry("500x500")
        dialog.resizable(False, False)

        # Zentriere Dialog
        dialog.transient(self.root)
        dialog.grab_set()

        # Hauptframe
        main_frame = ttk.Frame(dialog, padding=20)
        main_frame.pack(fill=BOTH, expand=YES)

        # Header
        ttk.Label(
            main_frame,
            text="Paketliste exportieren",
            font=("TkDefaultFont", 14, "bold")
        ).pack(pady=(0, 5))

        ttk.Label(
            main_frame,
            text=f"{len(self.filtered_packages)} Pakete werden exportiert",
            bootstyle=SECONDARY
        ).pack(pady=(0, 20))

        # Format-Auswahl
        ttk.Label(
            main_frame,
            text="Format wählen:",
            font=("TkDefaultFont", 10, "bold")
        ).pack(anchor=W, pady=(0, 10))

        format_var = ttk.StringVar(value="txt")
        format_frame = ttk.Frame(main_frame)
        format_frame.pack(fill=X, pady=(0, 20))

        # Format-Buttons (Radio-Style aber als schöne Buttons)
        formats = [
            ("txt", "Text (.txt)", "Einfache Textdatei, gut lesbar"),
            ("csv", "CSV (.csv)", "Für Excel/LibreOffice"),
            ("json", "JSON (.json)", "Für Scripts/Programme")
        ]

        for fmt, label, desc in formats:
            btn_frame = ttk.Frame(format_frame)
            btn_frame.pack(fill=X, pady=5)

            ttk.Radiobutton(
                btn_frame,
                text=label,
                variable=format_var,
                value=fmt,
                bootstyle="toolbutton"
            ).pack(side=LEFT, fill=X, expand=YES)

            ttk.Label(
                btn_frame,
                text=desc,
                font=("TkDefaultFont", 8),
                foreground="#888888"
            ).pack(side=LEFT, padx=(10, 0))

        # Dateiname
        ttk.Label(
            main_frame,
            text="Dateiname:",
            font=("TkDefaultFont", 10, "bold")
        ).pack(anchor=W, pady=(0, 5))

        filename_frame = ttk.Frame(main_frame)
        filename_frame.pack(fill=X, pady=(0, 20))

        filename_var = ttk.StringVar(value="myapps-export")
        filename_entry = ttk.Entry(
            filename_frame,
            textvariable=filename_var,
            font=("TkDefaultFont", 11)
        )
        filename_entry.pack(side=LEFT, fill=X, expand=YES, padx=(0, 10))

        # Speicherort
        location_var = ttk.StringVar(value=str(Path.home() / "Downloads"))

        def browse_location():
            from tkinter import filedialog
            folder = filedialog.askdirectory(
                title="Speicherort wählen",
                initialdir=location_var.get()
            )
            if folder:
                location_var.set(folder)

        ttk.Button(
            filename_frame,
            text="Ordner wählen...",
            command=browse_location,
            bootstyle=SECONDARY
        ).pack(side=LEFT)

        # Speicherort-Anzeige
        ttk.Label(
            main_frame,
            text="Speicherort:",
            font=("TkDefaultFont", 10, "bold")
        ).pack(anchor=W, pady=(0, 5))

        location_label = ttk.Label(
            main_frame,
            textvariable=location_var,
            bootstyle=INFO,
            font=("TkDefaultFont", 9)
        )
        location_label.pack(anchor=W, pady=(0, 20))

        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=X)

        def do_export():
            fmt = format_var.get()
            filename = filename_var.get()
            location = location_var.get()

            if not filename:
                Messagebox.show_warning("Bitte einen Dateinamen eingeben", parent=dialog)
                return

            # Füge Erweiterung hinzu wenn nicht vorhanden
            if not filename.endswith(f".{fmt}"):
                filename = f"{filename}.{fmt}"

            full_path = Path(location) / filename

            # Export durchführen
            success = Exporter.export(self.filtered_packages, str(full_path), fmt)

            if success:
                dialog.destroy()
                Messagebox.show_info(
                    f"Export erfolgreich!\n\n{full_path}",
                    title="Export erfolgreich"
                )
            else:
                Messagebox.show_error(
                    "Fehler beim Exportieren",
                    title="Fehler",
                    parent=dialog
                )

        ttk.Button(
            button_frame,
            text="Abbrechen",
            command=dialog.destroy,
            bootstyle=SECONDARY,
            width=15
        ).pack(side=RIGHT, padx=(10, 0))

        ttk.Button(
            button_frame,
            text="Exportieren",
            command=do_export,
            bootstyle=SUCCESS,
            width=15
        ).pack(side=RIGHT)

    def _show_about_dialog(self) -> None:
        """Zeigt Über-Dialog mit Version und Links"""
        dialog = ttk.Toplevel(self.root)
        dialog.title(_("Über MyApps"))
        dialog.geometry("550x700")
        dialog.resizable(True, True)

        # Zentriere Dialog
        dialog.transient(self.root)
        dialog.grab_set()

        # Hauptframe - direkt ohne Canvas
        main_frame = ttk.Frame(dialog, padding=20)
        main_frame.pack(fill=BOTH, expand=YES)

        # Logo/Titel
        ttk.Label(
            main_frame,
            text="MyApps",
            font=("TkDefaultFont", 24, "bold")
        ).pack(pady=(0, 5))

        # Version
        ttk.Label(
            main_frame,
            text=f"Version {VERSION}",
            font=("TkDefaultFont", 12),
            bootstyle=SECONDARY
        ).pack(pady=(0, 20))

        # Beschreibung
        ttk.Label(
            main_frame,
            text=_("Tool zum Auflisten und Verwalten installierter Linux-Anwendungen"),
            font=("TkDefaultFont", 10),
            wraplength=400,
            justify=CENTER
        ).pack(pady=(0, 30))

        # Links-Sektion (ohne Emojis)
        links_frame = ttk.LabelFrame(
            main_frame,
            text=_("Links"),
            padding=15
        )
        links_frame.pack(fill=X, pady=(0, 20))

        links = [
            ("GitHub Repository", "https://github.com/nicolettas-muggelbude/myapps"),
            ("Dokumentation", "https://github.com/nicolettas-muggelbude/myapps#readme"),
            ("Fehler melden", "https://github.com/nicolettas-muggelbude/myapps/issues"),
            ("Telegram Community", "https://t.me/LinuxGuidesDECommunity"),
        ]

        for label, url in links:
            link_btn = ttk.Button(
                links_frame,
                text=label,
                command=lambda u=url: webbrowser.open(u),
                bootstyle="info-link",
                cursor="hand2"
            )
            link_btn.pack(fill=X, pady=3)

        # Credits
        credits_frame = ttk.LabelFrame(
            main_frame,
            text=_("Credits"),
            padding=15
        )
        credits_frame.pack(fill=X, pady=(0, 20))

        ttk.Label(
            credits_frame,
            text="Entwickelt für die Linux Guides DE Community",
            font=("TkDefaultFont", 9),
            wraplength=400
        ).pack(pady=3)

        ttk.Label(
            credits_frame,
            text="UI basiert auf ttkbootstrap",
            font=("TkDefaultFont", 9),
            bootstyle=SECONDARY
        ).pack(pady=3)

        # Lizenz
        ttk.Label(
            main_frame,
            text="Lizenziert unter GNU General Public License v3.0",
            font=("TkDefaultFont", 8),
            bootstyle=SECONDARY
        ).pack(pady=(0, 20))

        # Schließen-Button
        ttk.Button(
            main_frame,
            text=_("Schließen"),
            command=dialog.destroy,
            bootstyle=PRIMARY,
            width=20
        ).pack(pady=(0, 10))

    def _bind_tooltip(self, widget, pkg: Package) -> None:
        """
        Bindet Tooltip mit lazy-loaded Beschreibung an ein Widget

        Args:
            widget: tkinter Widget
            pkg: Package-Objekt
        """
        tooltip_window = None

        def show_tooltip(event):
            nonlocal tooltip_window

            # Hole Beschreibung (lazy loading mit cache)
            description = self._get_package_description(pkg)
            if not description:
                return

            # Erstelle Tooltip-Fenster
            tooltip_window = ttk.Toplevel(self.root)
            tooltip_window.wm_overrideredirect(True)
            tooltip_window.wm_geometry(f"+{event.x_root + 10}+{event.y_root + 10}")

            # Tooltip-Label
            label = ttk.Label(
                tooltip_window,
                text=description,
                padding=10,
                bootstyle="inverse-dark",
                wraplength=400
            )
            label.pack()

        def hide_tooltip(event):
            nonlocal tooltip_window
            if tooltip_window:
                tooltip_window.destroy()
                tooltip_window = None

        widget.bind("<Enter>", show_tooltip)
        widget.bind("<Leave>", hide_tooltip)

    def _get_package_description(self, pkg: Package) -> Optional[str]:
        """
        Holt Beschreibung für Paket (mit Caching)

        Args:
            pkg: Package-Objekt

        Returns:
            Beschreibung oder None
        """
        cache_key = f"{pkg.package_type}:{pkg.name}"

        # Prüfe Cache
        if cache_key in self.description_cache:
            return self.description_cache[cache_key]

        # Lade Beschreibung je nach Pakettyp
        description = None

        if pkg.package_type == "deb":
            from .package_manager import DpkgPackageManager
            pm = DpkgPackageManager()
            description = pm.get_package_description(pkg.name)
        # Weitere Pakettypen können hier hinzugefügt werden

        # Cache it
        self.description_cache[cache_key] = description
        return description

    def _set_status(self, text: str, show_progress: bool = False) -> None:
        """
        Setzt den Statustext

        Args:
            text: Statustext
            show_progress: Progressbar anzeigen?
        """
        self.status_label.config(text=text)

        if show_progress:
            self.progress.pack(side=RIGHT, padx=5, pady=2)
            self.progress.start(10)
        else:
            self.progress.stop()
            self.progress.pack_forget()

    def run(self) -> None:
        """Startet die GUI"""
        self.root.mainloop()
