import subprocess
import sys
import importlib

def install_package(package_name, module_name=None):
    if module_name is None:
        module_name = package_name
    try:
        importlib.import_module(module_name)
        print(f"{module_name} is already installed.")
    except ImportError:
        print(f"Installing {package_name}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])


requirements = [
    ("auto-py-to-exe", "auto_py_to_exe"),
    ("bcrypt", "bcrypt"),
    ("beautifulsoup4", "bs4"),
    ("browser-cookie3", "browser_cookie3"),
    ("colorama", "colorama"),
    ("cryptography", "cryptography"),
    ("requests", "requests"),
    ("deep-translator", "deep_translator"),
    ("discord", "discord"),
    ("dnspython", "dns"),
    ("exifread", "exifread"),
    ("customtkinter", "customtkinter"),
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

for package, module in requirements:
    install_package(package, module)

print("All necessary packages are installed.")