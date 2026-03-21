# (c) 2026 IxilaA1 - All rights reserved / Tous droits réservés / Todos los derechos reservados.
# This code may not be sold, modified, or shared without authorization, nor published under your name.
# -------------------------------------------------------------------------------------------------------
import subprocess
import sys
import importlib
import os

def install_package(package_name, module_name=None):
    """Checks if a module is installed; if not, installs it via pip."""
    if module_name is None:
        module_name = package_name
    try:
        importlib.import_module(module_name)
        print(f" {module_name} is already installed.")
    except ImportError:
        print(f" Installing {package_name}...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
        except Exception as e:
            print(f" Error installing {package_name}: {e}")

def get_requirements_from_file(filename="requirements.txt"):
    """Reads requirements.txt and returns a list of (package, module) tuples."""
    file_reqs = []
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                
                if line and not line.startswith("#"):
                    
                    package = line.split("==")[0].split(">=")[0].split("<=")[0].strip()
                    
                    file_reqs.append((package, package))
    return file_reqs


requirements = [
    ("auto-py-to-exe", "auto_py_to_exe"),
    ("bcrypt", "bcrypt"),
    ("beautifulsoup4", "bs4"),
    ("browser-cookie3", "browser_cookie3"),
    ("colorama", "colorama"),
    ("cryptography", "cryptography"),
    ("requests", "requests"),
    ("requests-toolbelt", "requests_toolbelt"),
    ("deep-translator", "deep_translator"),
    ("httpagentparser", "httpagentparser"),
    ("edge-tts", "edge_tts"),
    ("discord.py", "discord"), 
    ("dnspython", "dns"),
    ("exifread", "exifread"),
    ("pystyle", "pystyle"),
    ("tqdm", "tqdm"),
    ("customtkinter", "customtkinter"),
    ("argon2-cffi", "argon2"),
    ("pyautogui", "pyautogui"),
    ("pycryptodome", "Crypto"), 
    ("pyinstaller", "PyInstaller"),
    ("pyqt5", "PyQt5"),
    ("pyqtwebengine", "PyQtWebEngine"),
    ("pywin32", "win32api"),
    ("pyzipper", "pyzipper"),
    ("rarfile", "rarfile"),
    ("screeninfo", "screeninfo"),
    ("selenium", "selenium"),
    ("setuptools", "setuptools"),
    ("urllib3", "urllib3"),
    ("whois", "whois"),
    ("whoiam", "whoiam"),
    ("phonenumbers", "phonenumbers"),
    ("instaloader", "instaloader"),
    ("pwinput", "pwinput"),
    ("piexif", "piexif"),
    ("scapy", "scapy"),
    ("tabulate", "tabulate"),
]


external_reqs = get_requirements_from_file()
if external_reqs:
    print(f"--- Scanning requirements.txt ({len(external_reqs)} found) ---")
    
    existing_packages = {r[0].lower() for r in requirements}
    for req in external_reqs:
        if req[0].lower() not in existing_packages:
            requirements.append(req)


print(" Checking dependencies...\n")
for package, module in requirements:
    install_package(package, module)

print("\n All necessary packages are installed and ready to use.")