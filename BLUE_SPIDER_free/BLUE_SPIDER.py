# multitool_bluespider.py
# -*- coding: utf-8 -*-
"""
Multitool "Bluepider" — logo rouge, texte blanc/rouge, fond noir
"""
import os
import sys
import subprocess
import traceback
import shutil
import re
from pathlib import Path
import webbrowser
import datetime
import time
import colorama
# Initialisation de Colorama pour Windows
colorama.init()

# Couleurs
BLUE_RGB = (135, 206, 235)
WHITE_RGB = (255, 255, 255)
RESET = "\033[0m"

# Fonction RGB nécessaire dès le début
def rgb(r, g, b): 
    return f"\033[38;2;{r};{g};{b}m"

# --- FONCTIONS D'ANIMATION ---
def animate_text(text):
    """Affiche le texte caractère par caractère."""
    sys.stdout.write(rgb(*BLUE_RGB))
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.02) 
    sys.stdout.write(RESET + '\n')

def show_entrance_animation():
    """Crée l'animation de démarrage en bleu ciel."""
    animate_text(" Welcome to Blue Spider ")
    animate_text("(by IxilaA)")
    time.sleep(0.5)
    
    # On utilise print (qui est maintenant ta fonction timed_print)
    print("Loading scripts...")
    time.sleep(0.3)
    print("Checking files...")
    time.sleep(0.3)
    print("Execution ready.")
    time.sleep(0.5)
    
    print("\nInitialization in progress:")
    for i in range(11):
        # Utilisation de \r pour rafraîchir la ligne
        sys.stdout.write(f"{rgb(*BLUE_RGB)}[{'#' * i}{' ' * (10 - i)}] {i*10}% \r{RESET}")
        sys.stdout.flush()
        time.sleep(0.1)
    print("\n" * 2)



show_entrance_animation()

# ---------------------------
# CONFIG: MENUS
original_print = print

def timed_print(*args, **kwargs):
    now = datetime.datetime.now()
    hour_str = f"{now.hour:02d}"
    minute_str = f"{now.minute:02d}"
    second_str = f"{now.second:02d}"
    
    # Utilisation de rgb(*BLUE_RGB) pour les crochets
    blue_color = rgb(*BLUE_RGB)
    
    time_prefix = (
        f"{blue_color}[{RESET}"                    # [ bleu
        f"\033[38;2;255;255;255m{hour_str}\033[0m" # heures blanches
        f"\033[38;2;255;255;255m:\033[0m"
        f"\033[38;2;255;255;255m{minute_str}\033[0m" # minutes blanches
        f"\033[38;2;255;255;255m:\033[0m"
        f"\033[38;2;255;255;255m{second_str}\033[0m" # secondes blanches
        f"{blue_color}]{RESET}"                    # ] bleu
    )
    
    plus_prefix = (
        f"{blue_color}[{RESET}"                    # [ bleu
        f"\033[38;2;255;255;255m+\033[0m"         # + blanc
        f"{blue_color}]{RESET}"                    # ] bleu
    )
    
    prefix = f"{time_prefix} {plus_prefix} "
    # ... le reste du code de la fonction reste identique
    
    sep = kwargs.get('sep', ' ')
    end = kwargs.get('end', '\n')
    text = sep.join(str(a) for a in args)
    original_print(f"{prefix}{text}", end=end)

print = timed_print

# Exemple
print("Ceci est un test")

# ---------------------------
# CONFIG: MENUS
MENU = [
    {"name": "Password", "items": [
        {"file": "mdp-tool.bat", "title": "Password Bruteforce Attack"},
        {"file": "Password-Hash-Decrypted-Attack.py", "title": "Password Hash Decrypted Attack"},
        {"file": "MDP-wifi.py", "title": "Password Wifi Finder"},
        {"file": "Password-Hash-Encrypted.py", "title": "Password Hash Encrypted"},
        {"file": "encrypt-decrypt-message.py", "title": "Message Encrypt-Decrypt"},
    ]},
    {"name": "Osint", "items": [
        {"file": "phone-number.py", "title": "Phone Number Lookup"},
        {"file": "username-tracker.py", "title": "Username Tracker"},
        {"file": "email-lookup.py", "title": "Email Lookup"},
        {"file": "email-tracker.py", "title": "Email Tracker"},
        {"file": "Instagram-Account.py", "title": "Instagram Account"},
        {"file": "dox-create.py", "title": "DOX Create"},
        {"file": "dox-tracker.py", "title": "DOX Tracker"},
    ]},
    {"name": "Discord", "items": [
        {"file": "Discord-nitro-gen.py", "title": "Discord Nitro Generator"},
        {"file": "Discord-Token-Info.py", "title": "Discord Token Info"},
        {"file": "bot-nuke.py", "title": "Create Discord Nuke Bot"},
        {"file": "Bot-Invite-server.py", "title": "Discord Invite Bot ID Generator"},
        {"file": "Discord-server-info.py", "title": "Discord Server Info"},
        {"file": "webhook-delete.py", "title": "Discord Webhook Delete"},
        {"file": "webhook-info.py", "title": "Discord Webhook Info"},
        {"file": "webhook-Spammer.py", "title": "Discord Webhook Spammer"},
        {"file": "webhook-GENERATOR.py", "title": "Discord Webhook Generator"},
    ]},
    
    {"name": "Network Scan", "items": [
        {"file": "ip-curl.py", "title": "Ip Geolocate"},
        {"file": "ip-scan.py", "title": "Ip Scanner"},
        {"file": "ip-port-scan.py", "title": "Ip Ports Scan"},
        {"file": "ip-pinger.py", "title": "Ip Pinger"},
        {"file": "website-scan.py", "title": "Website Scanner"},
        {"file": "website-info.py", "title": "Website Info Scanner"},
        {"file": "website-Vulnera.py", "title": "Website Vulnerability Scanner"},
        {"file": "dns-jumper.py", "title": "Dns Utilities Scanner"},
    ]},
    {"name": "Utilities", "items": [
        {"file": "Website-test.py", "title": "Website Test Connection"},
        {"file": "ddos.py", "title": "DDoS attack"},
        {"file": "Phishing.py", "title": "Phishing attack"},
        {"file": "ip-gen.py", "title": "Ip Generator"},
        {"file": "Email-Sender.py", "title": "Email SPAM Sender"},
        {"file": "Dark-Web-Links.py", "title": "Dark Web Links"},
        {"file": "Get-Image-Exif.py", "title": "Get Image Exif"},
        {"file": "Mini-Sniffer.py", "title": "Wire Shark Update"},
    ]},
]

# Nouvelle catégorie
SUB_MENU = [
    {"name": "Discord", "items": [
        {"file": "Discord-Token-Generator.py", "title": "Discord Token Generator"},
        {"file": "Discord-Token-Info.py", "title": "Discord Token Infos"},
        {"file": "Discord-Token-Login.py", "title": "Discord Token Login"},
        {"file": "discord-token-raid.py", "title": "Discord Token Raid"},
        {"file": "Discord-token-mass-dm.py", "title": "Discord Token Mass Dm"},
    ]},
    {"name": "Roblox", "items": [
        {"file": "Roblox-Cookie-Info.py", "title": "Roblox Cookie Info"},
        {"file": "Roblox-Cookie-Login.py", "title": "Roblox Cookie Login"},
        {"file": "Roblox-id-info.py", "title": "Roblox Id Info"},
        {"file": "Roblox-user-info.py", "title": "Roblox User Info"},
    ]},
    {"name": "Os", "items": [
        {"file": "iso-download.py", "title": "Iso Download Links"},
        {"file": "iso-info.py", "title": "Iso Infos"},
    ]},
]

ALL_MENUS = {
    "Windows-Menu 1": MENU,
    "Windows-Menu 2": SUB_MENU
}

# ---------------------------

LOGO = r"""
 ▄▄▄▄    ██▓     █    ██ ▓█████      ██████  ██▓███   ██▓▓█████▄ ▓█████  ██▀███  
▓█████▄ ▓██▒     ██  ▓██▒▓█   ▀    ▒██    ▒ ▓██░  ██▒▓██▒▒██▀ ██▌▓█   ▀ ▓██ ▒ ██▒
▒██▒ ▄██▒██░    ▓██  ▒██░▒███      ░ ▓██▄   ▓██░ ██▓▒▒██▒░██   █▌▒███   ▓██ ░▄█ ▒
▒██░█▀  ▒██░    ▓▓█  ░██░▒▓█  ▄      ▒   ██▒▒██▄█▓▒ ▒░██░░▓█▄   ▌▒▓█  ▄ ▒██▀▀█▄  
░▓█  ▀█▓░██████▒▒▒█████▓ ░▒████▒   ▒██████▒▒▒██▒ ░  ░░██░░▒████▓ ░▒████▒░██▓ ▒██▒
░▒▓███▀▒░ ▒░▓  ░░▒▓▒ ▒ ▒ ░░ ▒░ ░   ▒ ▒▓▒ ▒ ░▒▓▒░ ░  ░░▓   ▒▒▓  ▒ ░░ ▒░ ░░ ▒▓ ░▒▓░
▒░▒   ░ ░ ░ ▒  ░░░▒░ ░ ░  ░ ░  ░   ░ ░▒  ░ ░░▒ ░      ▒ ░ ░ ▒  ▒  ░ ░  ░  ░▒ ░ ▒░
 ░    ░   ░ ░    ░░░ ░ ░    ░      ░  ░  ░  ░░        ▒ ░ ░ ░  ░    ░     ░░   ░ 
 ░          ░  ░   ░        ░  ░         ░            ░     ░       ░  ░   ░     
      ░                                                   ░                                        
"""

# ---------------------------
# Terminal color helpers
def enable_windows_ansi():
    if os.name != "nt":
        return
    try:
        import ctypes
        kernel32 = ctypes.windll.kernel32
        h = kernel32.GetStdHandle(-11)
        mode = ctypes.c_uint32()
        if kernel32.GetConsoleMode(h, ctypes.byref(mode)):
            ENABLE_VIRTUAL_TERMINAL_PROCESSING = 0x0004
            new_mode = mode.value | ENABLE_VIRTUAL_TERMINAL_PROCESSING
            kernel32.SetConsoleMode(h, new_mode)
    except Exception:
        pass

enable_windows_ansi()

try:
    import colorama
    colorama.init()
except Exception:
    pass

def rgb(r, g, b): return f"\033[38;2;{r};{g};{b}m"
RESET = "\033[0m"
BOLD = "\033[1m"
BLUE_RGB = (135, 206, 235)
WHITE_RGB = (255, 255, 255)

import shutil, re
ANSI_ESCAPE = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
def strip_ansi(s): return ANSI_ESCAPE.sub('', s)

def get_terminal_size_safe(default_columns=100, default_lines=30):
    try:
        size = shutil.get_terminal_size()
        return size.columns, size.lines
    except Exception:
        return default_columns, default_lines

def center_block_lines(lines, max_width):
    centered = []
    for ln in lines:
        clean_len = len(strip_ansi(ln))
        pad = max((max_width - clean_len) // 2, 0)
        centered.append(" " * pad + ln)
    return centered

def get_centered_display_content(lines):
    logo_lines = [f"{rgb(*BLUE_RGB)}{line}{RESET}" for line in LOGO.strip().split("\n")]
    all_lines = logo_lines + ["", ""] + lines
    cols, rows = get_terminal_size_safe()
    centered_all = center_block_lines(all_lines, cols)
    block_height = len(centered_all)
    top_padding = max((rows - block_height) // 2, 0)
    return "\n" * top_padding + "\n".join(centered_all) + "\n"

def make_category_strip(categories):
    parts = []
    for i, cat in enumerate(categories, start=1):
        idx_label = f"[{str(i).zfill(2)}]"
        name = cat["name"]
        box_inner = f" {idx_label} {name} "
        boxed = f"{rgb(*BLUE_RGB)}┌{'─' * len(box_inner)}┐{RESET}\n" \
                f"{rgb(*BLUE_RGB)}│{RESET}{BOLD}{box_inner}{RESET}{rgb(*BLUE_RGB)}│{RESET}\n" \
                f"{rgb(*BLUE_RGB)}└{'─' * len(box_inner)}┘{RESET}"
        parts.append(boxed.splitlines())
    top_line = mid_line = bot_line = ""
    for i, b in enumerate(parts):
        if i > 0:
            top_line += "    "
            mid_line += "    "
            bot_line += "    "
        top_line += b[0]
        mid_line += b[1]
        bot_line += b[2]
    return [top_line, mid_line, bot_line]

def build_categories_panel(categories, menu_key):
    cat_strip = make_category_strip(categories)
    menu_label = f"[{menu_key.capitalize()}]"
    
    # Instructions pour naviguer entre les menus
    nav_inst = f"({rgb(*WHITE_RGB)}Ctrl+C exit{rgb(*BLUE_RGB)})"

    lines = [
        "",
        f"{BOLD}{rgb(*WHITE_RGB)}https://github.com/IxilaA1/BlueSpider-Tools {RESET}",
        "",
        f"{BOLD}{rgb(*WHITE_RGB)}  {menu_label} Choose a category {rgb(*BLUE_RGB)}{nav_inst}{RESET}",
        ""
    ]
    lines += cat_strip + ["", ""]
    return lines

def display_category_items_block(category, cat_index, total_cats, display_list):
    lines = [f"{BOLD}{rgb(*WHITE_RGB)} {category['name']} {rgb(*BLUE_RGB)}({cat_index+1}/{total_cats}){RESET}", ""]
    for i, item in enumerate(display_list, start=1):
        idx = f"{str(i).zfill(2)}"
        title = f"{item['title']}" + ("" if item["exists"] else " (missing)")
        # Correction des couleurs: Utilisation de BLUE_RGB et WHITE_RGB
        lines.append(f"{rgb(*BLUE_RGB)}[{rgb(*WHITE_RGB)}{idx}{rgb(*BLUE_RGB)}]{RESET} {rgb(*WHITE_RGB)}{title}{RESET}")
    # Correction des couleurs: Utilisation de BLUE_RGB et WHITE_RGB
    lines += ["", f"{rgb(*BLUE_RGB)}n{RESET}-{rgb(*WHITE_RGB)}next{RESET}  {rgb(*BLUE_RGB)}p{RESET}-{rgb(*WHITE_RGB)}prev{RESET}  {rgb(*BLUE_RGB)}b{RESET}-{rgb(*WHITE_RGB)}back{RESET}"]
    return lines

HERE = os.path.abspath(os.path.dirname(__file__))
FILES_DIR = os.path.join(HERE, "files")

def ensure_files_dir():
    if not os.path.isdir(FILES_DIR):
        os.makedirs(FILES_DIR, exist_ok=True)

def build_display_from_items(items_list):
    ensure_files_dir()
    display = []
    for item in items_list:
        path = os.path.join(FILES_DIR, item["file"])
        display.append({"file": item["file"], "title": item["title"], "exists": os.path.isfile(path)})
    return display

def run_py(path): subprocess.run([sys.executable, path], check=False)
def run_bat(path): subprocess.run(path, shell=True)
def show_txt_in_terminal(path):
    print(open(path, "r", encoding="utf-8", errors="ignore").read())

try:
    from PyQt6.QtWidgets import QApplication, QTextBrowser
    from PyQt6.QtGui import QPalette, QColor, QFont
    _PYQT6 = True
except Exception:
    _PYQT6 = False

def run_html_gui_with_pyqt(path):
    if not _PYQT6: raise RuntimeError("PyQt6 not available")
    app = QApplication(sys.argv)
    browser = QTextBrowser()
    browser.setWindowTitle(os.path.basename(path))
    pal = QPalette()
    pal.setColor(QPalette.ColorRole.Base, QColor(0, 0, 0))
    pal.setColor(QPalette.ColorRole.Text, QColor(255, 255, 255))
    browser.setPalette(pal)
    browser.setHtml(Path(path).read_text(errors="ignore"))
    browser.resize(1000, 700)
    browser.show()
    app.exec()

def run_html_fallback_open_browser(path):
    webbrowser.open_new_tab(Path(path).as_uri())
    input(f"{rgb(*BLUE_RGB)}\nPress Enter to return...{RESET}")

def run_in_cmd_for_item(item):
    path = os.path.join(FILES_DIR, item["file"])
    if not item["exists"]:
        input(f"{rgb(*BLUE_RGB)}Missing file. Press Enter...{RESET}")
        return
    ext = os.path.splitext(path)[1].lower()
    try:
        if ext == ".py":
            run_py(path)
            input(f"{rgb(*BLUE_RGB)}\nPress Enter...{RESET}")
        elif ext == ".txt":
            show_txt_in_terminal(path)
            input(f"{rgb(*BLUE_RGB)}\nPress Enter...{RESET}")
        elif ext == ".bat":
            run_bat(path)
            input(f"{rgb(*BLUE_RGB)}\nPress Enter...{RESET}")
        elif ext == ".html":
            try:
                run_html_gui_with_pyqt(path)
            except Exception:
                run_html_fallback_open_browser(path)
        else:
            input(f"{rgb(*BLUE_RGB)}Unsupported file type. Press Enter...{RESET}")
    except Exception:
        traceback.print_exc()
        input(f"{rgb(*BLUE_RGB)}Press Enter...{RESET}")

def display_categories_screen(categories, menu_key):
    os.system("cls" if os.name == "nt" else "clear")
    out = get_centered_display_content(build_categories_panel(categories, menu_key))
    sys.stdout.write(out)

def display_category_items_screen(category, cat_index, total_cats, display_list):
    os.system("cls" if os.name == "nt" else "clear")
    out = get_centered_display_content(display_category_items_block(category, cat_index, total_cats, display_list))
    sys.stdout.write(out)

def main():
    ensure_files_dir()
    current_menu_key = "Windows-Menu 1"
    
    while True:
        try:
            current_menu = ALL_MENUS[current_menu_key]
            
            
            menu_indicator = current_menu_key.capitalize()
            
            
            shell_line = f"{rgb(*BLUE_RGB)}({RESET}free-version{rgb(*BLUE_RGB)}@{rgb(*WHITE_RGB)}BlueSpider{rgb(*BLUE_RGB)})"
            prompt = f"{rgb(*BLUE_RGB)}>> ${RESET} "

            display_categories_screen(current_menu, current_menu_key)
            print(shell_line)
            ch = input(prompt).strip().lower()

            if ch in ("exit", "quit"): break
            
            
            if current_menu_key == "Windows-Menu 1" and ch == "n":
                current_menu_key = "Windows-Menu 2"
                continue
            elif current_menu_key == "Windows-Menu 2" and ch == "k":
                current_menu_key = "Windows-Menu 1"
                continue
            
            #
            if ch.isdigit():
                i = int(ch)-1
                if 0 <= i < len(current_menu):
                    cat_i = i
                    while True:
                        cat = current_menu[cat_i]
                        disp = build_display_from_items(cat["items"])
                        display_category_items_screen(cat, cat_i, len(current_menu), disp)
                        print(shell_line)
                        sub = input(prompt).strip().lower()
                        
                        if sub in ("b", "back"): break
                        if sub in ("exit", "quit"): return
                        
                        # Navigation entre les éléments de la catégorie (n et p)
                        if sub in ("n", "next"): cat_i = (cat_i+1)%len(current_menu); continue
                        if sub in ("p", "prev"): cat_i = (cat_i-1)%len(current_menu); continue
                        
                        # Sélection de l'élément (chiffre)
                        if sub.isdigit():
                            s = int(sub)-1
                            if 0 <= s < len(disp): run_in_cmd_for_item(disp[s])
                        else: 
                            input(f"{rgb(*BLUE_RGB)}Press Enter...{RESET}")
                else:
                    input(f"{rgb(*BLUE_RGB)}Press Enter...{RESET}")
            else:
                input(f"{rgb(*BLUE_RGB)}Press Enter...{RESET}")

        except KeyboardInterrupt:
            print(f"\n{rgb(*BLUE_RGB)}Exiting...{RESET}")
            break
        except Exception:
            traceback.print_exc()
            # Correction des couleurs: Utilisation de BLUE_RGB
            input(f"{rgb(*BLUE_RGB)}An unexpected error occurred. Press Enter...{RESET}")
            
if __name__ == "__main__":
    main()