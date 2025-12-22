#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk, scrolledtext
import subprocess

def is_user_app(package_name):
    """Filtert System-Apps und Bibliotheken heraus."""
    # Liste von Schlüsselwörtern, die auf System-Apps hinweisen
    system_keywords = [
    "-dev", "-log", "accountsservice", "acl", "acpid", "acronym", "adduser", "adwaita-icon-theme",
    "alsa", "amavisd", "amsbsy", "amscd", "amsgen", "amsmath", "amsmidx", "amssymb", "amstext",
    "amsthm", "amsxtra", "anacron", "apache", "apdemon-", "apg", "apparmor", "appstream", "apt",
    "aptdaemon-", "aptitude-", "apturl-", "apt-utils", "arj", "array", "article", "ascmac", "aspell",
    "aspnetcore-", "asymptote", "at", "attr", "authblk", "autobreak", "autofs", "avahi", "baobab",
    "babel", "backref", "balance", "bar", "bash", "basque-date", "bbding", "bbm", "bc", "beamer",
    "beamerarticle", "beamerswitch", "binutils", "bind9", "blt", "bluetooth", "bluez", "bluez-obexd",
    "bolt", "bridge-utils", "brltty", "bsdextrautils", "bsdutils", "bubblewrap", "build-essential",
    "bulky", "bzip2", "cabextract", "cacache", "cairomm", "captain", "caribou", "casper", "celluloid",
    "cifs-utils", "cinnamon", "circle-flags-svg", "cjs", "clamav", "colord", "common", "console",
    "consolekit", "containerd", "coreutils", "cpio", "cpp", "cpp-13", "cron", "crda", "cryptsetup",
    "cscope", "cyrus", "dash", "dconf-", "ddcutil", "deb", "dev", "dhcp", "dialog", "diffutils",
    "dirmngr", "djvulibre", "dmeventd", "dmidecode", "dmraid", "dmsetup", "dmz-cursor-theme",
    "dnsmasq", "doc", "doc-base", "docbook", "dosfstools", "dracut-install", "dpkg", "drm",
    "dsfont", "dvipng", "dvisvgm", "e2fsprogs", "ecryptfs-utils", "ed", "edquota", "efi", "eject",
    "euler", "exif", "exim4", "fail2ban", "fancontrol", "fakeroot", "fdisk", "ffmpeg", "ffmpegthumbnailer",
    "fig", "file", "finalrd", "findutils", "firmware", "fish", "flash-kernel", "folder-color-switcher",
    "foomatic", "font", "fprintd", "friendly-recovery", "ftp", "fuse3", "fwupd", "g++", "gamemode",
    "gcc", "gconf", "gcr", "gdisk", "gdb", "geoclue", "genisoimage", "ghostscript", "gh", "gir",
    "gnome-", "gnupg", "gnuplot", "gpg", "gpg-agent", "gpgsm", "gpgv", "grep", "groff", "grub",
    "gsettings", "gstreamer", "gtk", "gucharmap", "gyp", "gzip", "haproxy", "hdparm", "heimdal",
    "heif-gdk-pixbuf:amd64", "hfsprogs", "hicolor-icon-theme", "hunspell-", "hyphen", "i18n",
    "i2c-tools", "i965-va-driver", "id3", "ifuse", "iio-sensor-proxy", "inetutils-telnet", "info",
    "init", "initramfs", "intl", "iproute2", "iptables", "iputils", "isc-dhcp", "iso-", "iw",
    "jack", "java", "jfs", "jfsutils", "kbd", "kerneloops", "kde", "keyboard", "keyboxd", "keyutils",
    "kmod", "kpartx", "kpartx-boot", "krb5", "ksh", "laptop-detect", "latex", "latex2mathml", "ldap",
    "less", "lib", "lightdm", "lighttpd", "linux", "linux-firmware", "locale", "login", "logrotate",
    "logsave", "lp-solve", "lsb-release", "lshw", "lsof", "lto-disabled-list", "ltrace", "lvm2",
    "lzma", "lzop", "m4", "mailcap", "make", "makeindex", "man", "marvosym", "mathjax", "mathpazo",
    "mawk", "mdadm", "media-types", "memcached", "mesa", "meson", "metacity", "microcode", "mint-",
    "mokutil", "mount", "mscompress", "msam", "msbm", "mscorefonts", "mtpro2", "muffin", "mtools",
    "mtr-tiny", "mysql", "mythes-", "nano", "nemo-", "net-tools", "netbase", "netplan", "netstandard-",
    "nfs-", "nginx", "nilfs-tools", "node-", "nopt", "nss", "nspr", "ntfs-3g", "nvidia-", "odt2txt",
    "onboard", "openprinting-ppds", "open-vm-tools", "openssh", "openssl", "openvpn", "openldap",
    "orca", "os-prober", "p11", "p7zip", "packagekit", "pam", "pango", "papirus-icon-theme",
    "parted", "passwd", "patch", "pci.ids", "pciutils", "pcmciautils", "pcscd", "perl", "php",
    "pigz", "pinentry-curses", "pinentry-gnome3", "pipewire", "pk", "playerctl", "plymouth",
    "pm-utils", "policykit", "polkitd", "poppler", "postfix", "postgresql", "powermgmt-base",
    "ppp", "printer-driver-", "procmail", "procps", "psf", "psmisc", "psmisc", "publicsuffix",
    "punycode", "python", "qemu", "qt5-", "quota", "raspi-firmware", "readline", "redis", "rename",
    "reiserfs", "repquota", "rfkill", "rhythmbox-plugin", "rpcsvc-proto", "runc", "rsfs", "rsync",
    "rsyslog", "ruby", "samba", "sane", "sassc", "sbsigntool", "scdaemon", "sddm", "seahorse",
    "sensible-utils", "simple-scan", "slick-greeter", "slapd", "smartmontools", "smbclient",
    "snapd", "socat", "spamassassin", "sqlite", "squashfs-tools", "ssl", "sticky", "stmaryrd",
    "strace", "streamer", "sudo", "switcheroo-control", "sysv", "systemd", "system-tools-backends",
    "tar", "tcpdump", "tcl", "teckit", "tex", "tex4ht", "texlive", "t1utils", "telnet", "terser",
    "thermald", "tipa", "tk", "tinfo", "tnftp", "touchegg", "trayicon", "ttf", "txfonts", "ubuntu-",
    "ucf", "udev", "udisks2", "ufw", "unace", "unrar", "unshield", "unzip", "upower", "upstart",
    "ure", "usb-modeswitch", "usb.ids", "usbmuxd", "user-setup", "usbutils", "util-linux",
    "uuid-runtime", "va-driver-all:amd64", "varnish", "vf", "vim", "wamerican", "wbritish",
    "wasy", "wayland", "webassemblyjs", "webp-pixbuf-loader:amd64", "webpack", "wget", "whiptail",
    "wireshark", "wireless-", "wireplumber", "wpa-supplicant", "wswiss", "x11", "xapp-", "xauth",
    "xawtv-plugins:amd64", "xbitmaps", "xbrlapi", "xcvt", "xdg-", "xfs", "xfsprogs", "xindy",
    "xinput", "xml", "xorriso", "xslt", "xviewer-", "xz", "yfonts", "yelp", "yelp-xsl", "zip",
    "zlib", "zsh", "zstd"
]

    # Prüfe, ob der Paketname auf eine System-App hinweist
    package_name_lower = package_name.lower()
    return not any(keyword in package_name_lower for keyword in system_keywords)

def get_installed_apps():
    """Ermittelt installierte Anwendungen nach Paketformat."""
    apps = {"deb": [], "snap": [], "flatpak": []}

    # DEB-Pakete (dpkg)
    try:
        deb_output = subprocess.check_output(
            ["dpkg", "--list"], universal_newlines=True
        ).splitlines()
        for line in deb_output[5:]:  # Überspringe Header
            if line.strip():
                parts = line.split()
                if len(parts) >= 3 and parts[0] == "ii":
                    package_name = parts[1]
                    if is_user_app(package_name):
                        apps["deb"].append(package_name)
    except subprocess.CalledProcessError:
        pass

    # Snap-Pakete (nur wenn Snap installiert ist)
    try:
        snap_output = subprocess.check_output(
            ["snap", "list"], universal_newlines=True
        ).splitlines()
        for line in snap_output[1:]:  # Überspringe Header
            if line.strip():
                app = line.split()[0]
                if is_user_app(app):
                    apps["snap"].append(app)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Snap ist nicht installiert oder nicht verfügbar.")

    # Flatpak-Pakete (nur wenn Flatpak installiert ist)
    try:
        flatpak_output = subprocess.check_output(
            ["flatpak", "list", "--app"], universal_newlines=True
        ).splitlines()
        for line in flatpak_output:
            if line.strip():
                app = line.split("\t")[0]
                if is_user_app(app):
                    apps["flatpak"].append(app)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Flatpak ist nicht installiert oder nicht verfügbar.")

    return apps

def display_apps():
    """Zeigt die installierten Apps in der GUI an."""
    apps = get_installed_apps()
    text_area.delete(1.0, tk.END)

    for pkg_type, app_list in apps.items():
        if app_list:  # Nur anzeigen, wenn Apps vorhanden sind
            text_area.insert(tk.END, f"\n--- {pkg_type.upper()} Pakete ---\n")
            for app in sorted(app_list):
                text_area.insert(tk.END, f"{app} ({pkg_type})\n")

# GUI erstellen
root = tk.Tk()
root.title("Installierte Anwendungen (gefiltert)")

frame = ttk.Frame(root, padding="10")
frame.pack(fill=tk.BOTH, expand=True)

text_area = scrolledtext.ScrolledText(frame, wrap=tk.WORD, width=80, height=25)
text_area.pack(fill=tk.BOTH, expand=True)

button = ttk.Button(frame, text="Apps auflisten", command=display_apps)
button.pack(pady=10)

root.mainloop()
