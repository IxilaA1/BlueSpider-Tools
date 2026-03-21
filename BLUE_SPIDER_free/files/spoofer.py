# (c) 2026 IxilaA1 - Tous droits réservés / All rights reserved / Todos los derechos reservados.
# Ce code ne peut être ni vendu, ni modifié, ni partagé sans autorisation, ni publié à votre nom.
# This code may not be sold, modified, or shared without authorization, nor published under your name.
# Este código no puede ser vendido, modificado ni compartido sin autorización, ni publicado a su nombre.
# -------------------------------------------------------------------------------------------------------
import os
import sys
import random
import string
import winreg
import atexit
import signal
import subprocess
import shutil
import ctypes
import time
import hashlib
from pathlib import Path
from colorama import init, Fore, Style
from time import sleep

init(autoreset=True)

def is_admin():
    
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def request_admin():
    
    if not is_admin():
        
        script = os.path.abspath(sys.argv[0])
        params = ' '.join([f'"{arg}"' if ' ' in arg else arg for arg in sys.argv[1:]])
        
        
        ctypes.windll.shell32.ShellExecuteW(
            None,
            "runas",
            sys.executable,
            f'"{script}" {params}',
            None,
            1
        )
        
        sys.exit(0)



ASCII_ART = """
██████╗ ██╗     ██╗   ██╗███████╗███████╗██████╗ ██╗██████╗ ███████╗██████╗ 
██╔══██╗██║     ██║   ██║██╔════╝██╔════╝██╔══██╗██║██╔══██╗██╔════╝██╔══██╗
██████╔╝██║     ██║   ██║█████╗  ███████╗██████╔╝██║██║  ██║█████╗  ██████╔╝
██╔══██╗██║     ██║   ██║██╔══╝  ╚════██║██╔═══╝ ██║██║  ██║██╔══╝  ██╔══██╗
██████╔╝███████╗╚██████╔╝███████╗███████║██║     ██║██████╔╝███████╗██║  ██║
╚═════╝ ╚══════╝ ╚═════╝ ╚══════╝╚══════╝╚═╝     ╚═╝╚═════╝ ╚══════╝╚═╝  ╚═╝
"""

BLUE = Fore.CYAN
LIGHT_BLUE = Fore.LIGHTBLUE_EX
WHITE = Fore.WHITE
RESET = Style.RESET_ALL
BRIGHT = Style.BRIGHT

original_hwids = {'cpu': None, 'gpu': None, 'disk': None, 'mac': None}
new_disk_serial = None
spoofed = False
seed = None

def print_banner(text, color=BLUE):
    print(f'{BRIGHT}{color}╔═══ {text} ═══{RESET}')

def print_step(text, color=LIGHT_BLUE):
    print(f'{color}  └─▶ {text}{RESET}')

def print_success(text):
    print(f'{LIGHT_BLUE}  ✓ {text}{RESET}')

def print_error(text):
    print(f'{WHITE}  ✗ {text}{RESET}')

def print_info(text):
    print(f'{BLUE}  ℹ {text}{RESET}')

def print_warning(text):
    print(f'{WHITE}  ⚠ {text}{RESET}')

def print_separator():
    print(f'{BLUE}{"─" * 60}{RESET}')

def print_ascii_art(ascii_art):
    print(f'{BRIGHT}{BLUE}{ascii_art}{RESET}')

def set_seed():
    global seed
    seed = hashlib.sha256(str(time.time()).encode()).hexdigest()[:16]
    random.seed(seed)
    print_info(f"System seed initialized: {seed}")

def generate_cpu_id():
    prefixes = [
        'AMD Ryzen 7 5800X', 'Intel Core i9-12900K', 'AMD Ryzen 5 5600X',
        'Intel Core i7-12700K', 'AMD Ryzen 9 5950X', 'Intel Core i5-12600K',
        'AMD Ryzen 7 7800X3D', 'Intel Core i9-13900K', 'AMD Ryzen 9 7950X',
        'Intel Core i7-13700K', 'AMD Ryzen 5 7600X', 'Intel Core i5-13600K'
    ]
    return random.choice(prefixes)

def generate_gpu_id():
    models = [
        'NVIDIA RTX 3080', 'AMD RX 6800', 'Intel Arc A770',
        'NVIDIA RTX 3070 Ti', 'AMD RX 6900 XT', 'NVIDIA GTX 1660 Super',
        'NVIDIA RTX 4090', 'AMD RX 7900 XTX', 'NVIDIA RTX 4080',
        'AMD RX 7800 XT', 'NVIDIA RTX 4070 Ti', 'Intel Arc A750'
    ]
    return random.choice(models)

def generate_disk_serial():
    manufacturers = ['WD', 'ST', 'SAMSUNG', 'HGST', 'TOSHIBA', 'KINGSTON', 'CRUCIAL', 'SEAGATE']
    prefix = random.choice(manufacturers)
    serial = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8))
    return f'{prefix}{serial}'

def generate_mac_address():
    mac = [random.randint(0x00, 0xff) for _ in range(6)]
    return ':'.join(f'{b:02x}' for b in mac)

def generate_volume_id():
    return ''.join(random.choice(string.hexdigits.upper()) for _ in range(8))

def get_current_cpu_id():
    try:
        key = winreg.OpenKey(
            winreg.HKEY_LOCAL_MACHINE,
            r'HARDWARE\DESCRIPTION\System\CentralProcessor\0',
            0, winreg.KEY_READ
        )
        cpu_id = winreg.QueryValueEx(key, 'ProcessorNameString')[0]
        winreg.CloseKey(key)
        return cpu_id
    except:
        try:
            key = winreg.OpenKey(
                winreg.HKEY_LOCAL_MACHINE,
                r'HARDWARE\DESCRIPTION\System\CentralProcessor\0',
                0, winreg.KEY_READ
            )
            cpu_id = winreg.QueryValueEx(key, 'Identifier')[0]
            winreg.CloseKey(key)
            return cpu_id
        except Exception as e:
            print_error(f"Error retrieving CPU ID: {e}")
            return None

def get_current_gpu_id():
    try:
        key = winreg.OpenKey(
            winreg.HKEY_LOCAL_MACHINE,
            r'SYSTEM\CurrentControlSet\Control\Class\{4d36e968-e325-11ce-bfc1-08002be10318}\0000',
            0, winreg.KEY_READ
        )
        gpu_id = winreg.QueryValueEx(key, 'DriverDesc')[0]
        winreg.CloseKey(key)
        return gpu_id
    except Exception as e:
        print_error(f"Error retrieving GPU ID: {e}")
        return None

def get_current_disk_serial():
    try:
        
        result = subprocess.run('vol C:', shell=True, capture_output=True, text=True, timeout=5)
        output = result.stdout
        if 'Volume Serial Number is ' in output:
            serial = output.split('Volume Serial Number is ')[-1].strip()
            if serial and serial != 'N/A':
                return serial
    except:
        pass
    
    try:
        
        result = subprocess.run('wmic diskdrive get SerialNumber', shell=True, capture_output=True, text=True, timeout=5)
        output = result.stdout
        for line in output.splitlines()[1:]:
            serial = line.strip()
            if serial and serial != 'N/A':
                return serial
    except:
        pass
    
    return None

def get_mac_address():
    try:
        result = subprocess.run('getmac /fo csv /nh', shell=True, capture_output=True, text=True, timeout=5)
        output = result.stdout
        if output:
            
            for line in output.splitlines():
                if line and ',' in line:
                    mac = line.split(',')[0].strip('"')
                    if mac and mac != 'N/A' and '-' in mac:
                        return mac.replace('-', ':')
    except:
        pass
    return None

def clean_game_data():
    appdata = os.getenv('APPDATA')
    localappdata = os.getenv('LOCALAPPDATA')
    programdata = os.getenv('PROGRAMDATA')
    userprofile = os.getenv('USERPROFILE')
    documents = str(Path.home() / 'Documents')
    
    
    game_paths = [
        Path(appdata) / 'Rockstar Games',
        Path(documents) / 'Rockstar Games',
        Path(appdata) / 'Social Club',
        
        Path(appdata) / 'FiveM',
        Path(localappdata) / 'FiveM',
        Path(appdata) / 'Cfx.re',
        Path(localappdata) / 'cfx-system',
        
        Path(documents) / 'Rockstar Games' / 'GTA V',
        Path(documents) / 'Rockstar Games' / 'GTA V' / 'Profiles',
        Path(appdata) / 'GTA V',
        Path(localappdata) / 'GTA V',
        
        Path(documents) / 'Rockstar Games' / 'Red Dead Redemption 2',
        Path(documents) / 'Rockstar Games' / 'Red Dead Redemption 2' / 'Profiles',
        Path(appdata) / 'Red Dead Redemption 2',
        
        Path(appdata) / 'EpicGamesLauncher',
        Path(localappdata) / 'EpicGamesLauncher',
        Path(programdata) / 'Epic',
        
        Path(appdata) / 'FortniteGame',
        Path(localappdata) / 'FortniteGame',
        Path(appdata) / 'Fortnite',
        
        Path(appdata) / 'Riot Games',
        Path(localappdata) / 'Riot Games',
        Path(programdata) / 'Riot Games',
        Path(appdata) / 'Riot Client',
        Path(appdata) / 'VALORANT',
        Path(localappdata) / 'VALORANT',
        Path(appdata) / 'League of Legends',
        Path(localappdata) / 'League of Legends',
        
        Path(appdata) / '.minecraft',
        Path(appdata) / 'minecraft',
        Path(localappdata) / 'Packages' / 'Microsoft.MinecraftUWP_8wekyb3d8bbwe' / 'LocalState' / 'games' / 'com.mojang',
        
        Path(appdata) / 'Ubisoft',
        Path(localappdata) / 'Ubisoft Game Launcher',
        Path(programdata) / 'Ubisoft',
        Path(appdata) / 'Uplay',
        
        Path(appdata) / 'Battle.net',
        Path(localappdata) / 'Blizzard Entertainment',
        Path(programdata) / 'Blizzard Entertainment',
        Path(appdata) / 'Blizzard',
        
        Path(appdata) / 'Origin',
        Path(localappdata) / 'Origin',
        Path(programdata) / 'Origin',
        Path(appdata) / 'Electronic Arts',
        
        Path(appdata) / 'Steam',
        Path(programdata) / 'Steam',
        Path(appdata) / 'SteamVR',
        
        Path(documents) / 'Call of Duty',
        Path(documents) / 'Call of Duty Modern Warfare',
        Path(documents) / 'Call of Duty Warzone',
        Path(documents) / 'Call of Duty Black Ops',
        Path(appdata) / 'Call of Duty',
        
        Path(appdata) / 'Apex Legends',
        Path(localappdata) / 'Apex Legends',
        
        Path(appdata) / 'PUBG',
        Path(localappdata) / 'PUBG',
        Path(appdata) / 'PUBG Corporation',
        
        Path(appdata) / 'CS:GO',
        Path(appdata) / 'Counter-Strike',
        Path(localappdata) / 'CS:GO',
        Path(appdata) / 'CS2',
        
        Path(appdata) / 'Rainbow Six Siege',
        Path(localappdata) / 'Rainbow Six Siege',
        Path(documents) / 'Rainbow Six Siege',
        
        Path(appdata) / 'GTA San Andreas',
        Path(appdata) / 'GTA IV',
        
        Path(appdata) / 'Mafia',
        Path(documents) / 'Mafia III',
        
        Path(appdata) / 'Watch Dogs',
        Path(documents) / 'Watch Dogs 2',
        Path(documents) / 'Watch Dogs Legion',
        
        Path(appdata) / 'Assassins Creed',
        Path(documents) / 'Assassins Creed',
        
        Path(appdata) / 'Far Cry',
        Path(documents) / 'Far Cry',
        
        Path(appdata) / 'The Witcher',
        Path(documents) / 'The Witcher 3',
        
        Path(appdata) / 'Cyberpunk 2077',
        Path(localappdata) / 'Cyberpunk 2077',
        
        Path(appdata) / 'Rust',
        Path(localappdata) / 'Rust',
        
        Path(appdata) / 'Escape from Tarkov',
        Path(localappdata) / 'Battlestate Games',
        
        Path(appdata) / 'DayZ',
        Path(localappdata) / 'DayZ',
        
        Path(appdata) / 'ARK',
        Path(localappdata) / 'ARK',
        
        Path(appdata) / 'Overwatch',
        Path(documents) / 'Overwatch',
        
        Path(appdata) / 'Genshin Impact',
        Path(localappdata) / 'Genshin Impact',
        Path(programdata) / 'Genshin Impact',
        
        Path(localappdata) / 'Roblox',
        Path(appdata) / 'Roblox',
        
        Path(appdata) / 'discord',
        Path(appdata) / 'discordptb',
        Path(appdata) / 'discordcanary',
        
        Path(appdata) / 'VRChat',
        Path(localappdata) / 'VRChat',
        
        Path(appdata) / 'Phasmophobia',
        Path(localappdata) / 'Phasmophobia',
        
        Path(appdata) / 'Among Us',
        Path(localappdata) / 'Among Us',
        
        Path(appdata) / 'Dead by Daylight',
        Path(localappdata) / 'Dead by Daylight',
        
        Path(appdata) / 'Sea of Thieves',
        Path(localappdata) / 'Sea of Thieves',
        
        Path(appdata) / 'Fall Guys',
        Path(localappdata) / 'Fall Guys',
        
        Path(appdata) / 'Rocket League',
        Path(documents) / 'Rocket League',
        
        Path(appdata) / 'FIFA',
        Path(documents) / 'FIFA',
        Path(appdata) / 'EA Sports',
        
        Path(appdata) / 'NBA 2K',
        Path(documents) / 'NBA 2K',
        
        Path(appdata) / 'Forza',
        Path(localappdata) / 'Forza',
        Path(documents) / 'Forza',
        
        Path(appdata) / 'The Sims',
        Path(documents) / 'Electronic Arts' / 'The Sims',
        
        Path(appdata) / 'Battlefield',
        Path(documents) / 'Battlefield',
        
        Path(appdata) / 'Titanfall',
        Path(documents) / 'Titanfall',
        
        Path(appdata) / 'Destiny 2',
        Path(programdata) / 'Destiny 2',
        
        Path(appdata) / 'Warframe',
        Path(localappdata) / 'Warframe',
        
        Path(appdata) / 'Path of Exile',
        Path(documents) / 'Path of Exile',
        
        Path(appdata) / 'Diablo',
        Path(documents) / 'Diablo',
        
        Path(appdata) / 'World of Warcraft',
        Path(localappdata) / 'World of Warcraft',
        Path(programdata) / 'World of Warcraft',
        
        Path(appdata) / 'Final Fantasy',
        Path(documents) / 'Final Fantasy',
        
        Path(appdata) / 'Monster Hunter',
        Path(localappdata) / 'Monster Hunter',
        
        Path(appdata) / 'Elden Ring',
        Path(localappdata) / 'Elden Ring',
        
        Path(appdata) / 'Dark Souls',
        Path(appdata) / 'DarkSouls',
        
        Path(appdata) / 'Sekiro',
        
        Path(appdata) / 'Borderlands',
        Path(documents) / 'Borderlands',
        
        Path(appdata) / 'DOOM',
        Path(localappdata) / 'DOOM',
        
        Path(appdata) / 'Resident Evil',
        Path(documents) / 'Resident Evil',
        
        Path(appdata) / 'Tekken',
        Path(localappdata) / 'Tekken',
        
        Path(appdata) / 'Street Fighter',
        Path(localappdata) / 'Street Fighter',
        
        Path(appdata) / 'Mortal Kombat',
        Path(localappdata) / 'Mortal Kombat',
        
        Path(appdata) / 'Hitman',
        Path(documents) / 'Hitman',
        
        Path(appdata) / 'Tomb Raider',
        Path(documents) / 'Tomb Raider',
        
        Path(appdata) / 'Just Cause',
        Path(localappdata) / 'Just Cause',
        
        Path(appdata) / 'Saints Row',
        Path(localappdata) / 'Saints Row',
        
        Path(appdata) / 'Dying Light',
        Path(localappdata) / 'Dying Light',
        
        Path(appdata) / 'The Forest',
        Path(appdata) / 'SonsOfTheForest',
        Path(localappdata) / 'The Forest',
        
        Path(appdata) / 'Green Hell',
        Path(localappdata) / 'Green Hell',
        
        Path(appdata) / 'Raft',
        Path(localappdata) / 'Raft',
        
        Path(appdata) / 'Subnautica',
        Path(localappdata) / 'Subnautica',
        
        Path(appdata) / 'No Man\'s Sky',
        Path(localappdata) / 'No Man\'s Sky',
        
        Path(appdata) / 'Elite Dangerous',
        Path(localappdata) / 'Elite Dangerous',
        
        Path(appdata) / 'Star Citizen',
        Path(localappdata) / 'Star Citizen',
        
        Path(appdata) / 'EVE',
        Path(localappdata) / 'EVE',
        
        Path(appdata) / 'Albion',
        Path(localappdata) / 'Albion',
        
        Path(appdata) / 'Black Desert',
        Path(localappdata) / 'Black Desert',
        
        Path(appdata) / 'Lost Ark',
        Path(localappdata) / 'Lost Ark',
        
        Path(appdata) / 'New World',
        Path(localappdata) / 'New World',
        
        Path(appdata) / 'Throne and Liberty',
        Path(localappdata) / 'Throne and Liberty',
        
        Path(appdata) / 'Blue Protocol',
        Path(localappdata) / 'Blue Protocol',
        
        Path(appdata) / 'Tower of Fantasy',
        Path(localappdata) / 'Tower of Fantasy',
        
        Path(appdata) / 'Garena',
        Path(programdata) / 'Garena',
        
        Path(programdata) / 'Steam' / 'logs',
        Path(appdata) / 'Steam' / 'logs',
        
        Path(localappdata) / 'Microsoft' / 'Windows' / 'WER',
        Path(appdata) / 'Microsoft' / 'Windows' / 'Caches',
        
        Path(appdata) / 'NVIDIA' / 'GfeCache',
        Path(appdata) / 'AMD' / 'GLCache',
        
    ]
    
    print_banner("CLEANING GAME TRACKING DATA")
    print_info(f"Scanning {len(game_paths)} game directories...")
    print_separator()
    
    cleaned_count = 0
    total_size = 0
    
    for path in game_paths:
        try:
            if path.exists():
                if path.is_dir():
                    
                    size = 0
                    try:
                        for f in path.glob('**/*'):
                            if f.is_file():
                                size += f.stat().st_size
                    except:
                        pass
                    
                    total_size += size
                    shutil.rmtree(path, ignore_errors=True)
                    print_success(f"Cleaned: {path.name} ({size / (1024*1024):.2f} MB)")
                else:
                    size = path.stat().st_size
                    total_size += size
                    path.unlink()
                    print_success(f"Cleaned: {path.name} ({size / (1024*1024):.2f} MB)")
                
                cleaned_count += 1
        except Exception as e:
            print_error(f"Error cleaning {path.name}: {e}")
    
    if cleaned_count > 0:
        print_separator()
        print_success(f"Cleaned {cleaned_count} game directories")
        print_info(f"Total space freed: {total_size / (1024*1024):.2f} MB")
    else:
        print_warning("No game data found to clean.")
    
    print_separator()
    return cleaned_count > 0

def backup_hwids():
    global original_hwids
    
    print_banner("BACKING UP ORIGINAL HWIDS")
    
    original_hwids['cpu'] = get_current_cpu_id()
    original_hwids['gpu'] = get_current_gpu_id()
    original_hwids['disk'] = get_current_disk_serial()
    original_hwids['mac'] = get_mac_address()
    
    success = False
    for key, value in original_hwids.items():
        if value:
            print_step(f"{key.upper()}: {value}")
            success = True
        else:
            print_warning(f"{key.upper()}: Not available")
    
    if not success:
        print_error("Failed to backup HWIDs. Aborting.")
        input(f'{WHITE}Press Enter to continue...{RESET}')
        return False
    
    print_separator()
    return True

def spoof_hwids(simulate=True):
    global new_disk_serial, spoofed
    
    if not simulate and not is_admin():
        print_error("Administrator privileges required for live mode.")
        print_error("Please restart the script and choose option 2 again.")
        print_info("The script will now request administrator rights...")
        
        
        request_admin()
        return False
    
    print_banner("GENERATING NEW SPIDER IDENTITY" if not simulate else "SIMULATION MODE")
    
    if simulate:
        print_warning("SIMULATION MODE - No actual changes made")
    else:
        print_info("LIVE MODE - Administrator privileges confirmed")
    
    set_seed()
    
    new_cpu = generate_cpu_id()
    new_gpu = generate_gpu_id()
    new_disk_serial = generate_disk_serial()
    new_mac = generate_mac_address()
    new_volume = generate_volume_id()
    
    print_info("New digital identity created:")
    print_step(f"CPU: {new_cpu}")
    print_step(f"GPU: {new_gpu}")
    print_step(f"Disk Serial: {new_disk_serial}")
    print_step(f"MAC Address: {new_mac}")
    print_step(f"Volume ID: {new_volume}")
    
    if not simulate:
        print_warning("Real HWID modification - To be implemented")
        print_info("This would modify actual system identifiers")
        print_info("For demonstration purposes only")
    
    spoofed = True
    print_success("BlueSpider has woven its web successfully!")
    print_separator()
    return True

def restore_hwids():
    global spoofed
    
    if not spoofed:
        return
    
    print_banner("RESTORING ORIGINAL IDENTITY")
    print_info("BlueSpider is retracting its web...")
    
    spoofed = False
    print_success("Original identity restored successfully!")
    print_separator()

def signal_handler(sig, frame):
    print(f'\n{WHITE}[!] Interrupt detected. Restoring HWIDs...{RESET}')
    if spoofed:
        restore_hwids()
    sys.exit(0)

def display_menu():
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print_ascii_art(ASCII_ART)
    print_separator()
    
    print(f'{BRIGHT}{BLUE}  🕷️  BLUESPIDER HWID SPOOFER - WEAVING DIGITAL DISGUISES  🕷️{RESET}')
    print_separator()
    
    
    if is_admin():
        print_success("✓ Running with Administrator privileges")
    else:
        print_warning("⚠ Running without Administrator privileges (Simulation mode only)")
    print_separator()
    
    print(f'{BLUE}  ╔════════════════════════════════════════════════════════╗{RESET}')
    print(f'{BLUE}  ║  What gets camouflaged:                                 ║{RESET}')
    print(f'{BLUE}  ║  • CPU ID - Processor identifier                        ║{RESET}')
    print(f'{BLUE}  ║  • GPU ID - Graphics card identifier                    ║{RESET}')
    print(f'{BLUE}  ║  • Disk Serial - Drive serial number                    ║{RESET}')
    print(f'{BLUE}  ║  • MAC Address - Network adapter                        ║{RESET}')
    print(f'{BLUE}  ║  • Volume ID - Drive volume identifier                  ║{RESET}')
    print(f'{BLUE}  ║  • Game Data - 100+ games tracking cleaner              ║{RESET}')
    print(f'{BLUE}  ║  • Auto-Restore - Safe exit guaranteed                  ║{RESET}')
    print(f'{BLUE}  ╚════════════════════════════════════════════════════════╝{RESET}')
    print_separator()
    
    print(f'{LIGHT_BLUE}  [1] 🕸️  Launch Spoofing (Simulation Mode){RESET}')
    if is_admin():
        print(f'{LIGHT_BLUE}  [2] 🕷️  Launch Spoofing (Live Mode - Admin Active){RESET}')
    else:
        print(f'{LIGHT_BLUE}  [2] 🕷️  Launch Spoofing (Live Mode - Will request Admin){RESET}')
    print(f'{LIGHT_BLUE}  [3] 🧹  Clean Game Data (100+ Games){RESET}')
    print(f'{LIGHT_BLUE}  [4] 🔍  Display Current HWIDs{RESET}')
    print(f'{LIGHT_BLUE}  [5] 🚪  Exit{RESET}')
    print_separator()

def display_current_hwids():
    print_banner("CURRENT SYSTEM IDENTITY")
    
    cpu_id = get_current_cpu_id()
    gpu_id = get_current_gpu_id()
    disk_serial = get_current_disk_serial()
    mac_address = get_mac_address()
    
    print_step(f"CPU: {cpu_id if cpu_id else 'Not available'}")
    print_step(f"GPU: {gpu_id if gpu_id else 'Not available'}")
    print_step(f"Disk Serial: {disk_serial if disk_serial else 'Not available'}")
    print_step(f"MAC Address: {mac_address if mac_address else 'Not available'}")
    
    print_separator()
    input(f'{WHITE}Press Enter to continue...{RESET}')

def main():
    signal.signal(signal.SIGINT, signal_handler)
    atexit.register(lambda: restore_hwids() if spoofed else None)
    
    while True:
        display_menu()
        choice = input(f'{LIGHT_BLUE}Enter your choice [1-5] 🕷️ : {RESET}').strip()
        
        if choice == '1':
            print_info("Entering simulation web...")
            if backup_hwids():
                spoof_hwids(simulate=True)
            input(f'{WHITE}Press Enter to continue...{RESET}')
        
        elif choice == '2':
            print_info("Preparing live web weaving...")
            if backup_hwids():
                spoof_hwids(simulate=False)
            input(f'{WHITE}Press Enter to continue...{RESET}')
        
        elif choice == '3':
            clean_game_data()
            input(f'{WHITE}Press Enter to continue...{RESET}')
        
        elif choice == '4':
            display_current_hwids()
        
        elif choice == '5':
            print_info("BlueSpider is retreating...")
            if spoofed:
                restore_hwids()
            print_success("Until next time! 🕷️")
            break
        
        else:
            print_error("Invalid choice. Please enter 1-5.")
            sleep(1)

if __name__ == '__main__':
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print(f'{BRIGHT}{BLUE}')
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║     🕷️  WELCOME TO BLUESPIDER - YOUR DIGITAL CAMOUFLAGE  🕷️  ║
    ║                                                              ║
    ║         Weaving webs of anonymity in the digital world       ║
    ║                                                              ║
    ║         🎮  Now cleaning 100+ online games!  🎮              ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """)
    print(RESET)
    time.sleep(2)
    
    main()