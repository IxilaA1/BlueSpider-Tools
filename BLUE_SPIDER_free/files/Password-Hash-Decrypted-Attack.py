import bcrypt
import hashlib
import random
import string
import time
import base64
import os
import sys
from concurrent.futures import ThreadPoolExecutor
from hashlib import pbkdf2_hmac

logo_ascii = """
                                         ^M@@@@@@@@@v                                    
                                      v@@@@@@@@@@@@@@@@@                                 
                                    _@@@@@@@}    ;a@@@@@@@                               
                                   M@@@@@            @@@@@@                              
                                  ;@@@@@              O@@@@@                             
                                  @@@@@v               @@@@@                             
                                  @@@@@;               @@@@@                             
                                  @@@@@;                                                 
                                  @@@@@;        v@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@         
                                              @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@       
                                             @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@      
                                             @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@      
                                             @@@@@@@@@@@@@@@@j     @@@@@@@@@@@@@@@@      
                                             @@@@@@@@@@@@@@@        @@@@@@@@@@@@@@@      
                                             @@@@@@@@@@@@@@@v       @@@@@@@@@@@@@@@      
                                             @@@@@@@@@@@@@@@@@    @@@@@@@@@@@@@@@@@      
                                             @@@@@@@@@@@@@@@@@    @@@@@@@@@@@@@@@@@      
                                             @@@@@@@@@@@@@@@@@_   @@@@@@@@@@@@@@@@@      
                                             @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@      
                                              @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@|      
                                               ^@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@O  
"""


os.system('cls' if os.name == 'nt' else 'clear')


print(logo_ascii)


time.sleep(2)




BEFORE = "[>] "
AFTER = " <"
ERROR = "[ERROR]"
INPUT = "[INPUT]"
WAIT = "[WAIT]"
ADD = "[SUCCESS]"
INFO = "[INFO]"
white = ""
red = ""   
reset = "" 
decrypted_banner = "PASSWORD DECRYPTOR TOOL"
tool_path = "."

def ErrorModule(e):
    """Handles error logging/handling specific to module imports."""
    print(f"ERROR: Failed to import module or module setup: {e}")
    sys.exit(1)

def Title(text):
    """Placeholder for setting a title/header."""
    print(f"--- {text} ---")

def current_time_hour():
    """Placeholder for formatted current time."""
    return time.strftime("%H:%M:%S")

def Continue():
    """Pauses the script, waiting for user input."""
    input("Press Enter to continue...")

def Reset():
    """Placeholder for system reset (e.g., clearing the console or restarting flow)."""
    
    print("--- Flow Reset/Returning to Menu ---")
    
    sys.exit(0)

def ErrorNumber():
    """Handles invalid number input."""
    print(f"{BEFORE}{current_time_hour()}{AFTER} {ERROR} Invalid number input. Please try again.")
    Continue()
    Reset()

def ErrorChoice():
    """Handles invalid method choice."""
    print(f"{BEFORE}{current_time_hour()}{AFTER} {ERROR} Invalid choice. Please try again.")
    Continue()
    Reset()

def Error(e):
    """General error handler."""
    print(f"AN UNEXPECTED ERROR OCCURRED: {e}")

def Slow(text, delay=0.005):
    """
    FIXED: Prints text with a slight delay, simulating a 'slow' type effect.
    This function was missing and caused the 'NameError'.
    """
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()


try:
    Title(f"Password Decryptor")

   
    choice = None
    encrypted_password = None
    
    salt = "this_is_a_salt".encode('utf-8')
    password = False

    def ErrorDecrypted():
        """Handles errors when the hash format is incorrect for the chosen method."""
        encryption_map = {
            '1': 'BCRYPT', '2': 'MD5', '3': 'SHA-1', '4': 'SHA-256', '5': 'PBKDF2 (SHA-256)', '6': 'Base64 Decode'
        }
        encryption = encryption_map.get(choice, "Unknown")
        print(f'{BEFORE}{current_time_hour()}{AFTER} {ERROR} The hash "{white}{encrypted_password}{red}" is not accepted by the "{white}{encryption}{red}" method.')
        Continue()
        Reset()

    def CheckPassword(password_test):
        """Checks if a given plaintext password matches the global encrypted_password."""
        
        try:
            methods = {
                
                '1': lambda pwd: bcrypt.checkpw(pwd.encode('utf-8'), encrypted_password.encode('utf-8')),
                
                '2': lambda pwd: hashlib.md5(pwd.encode('utf-8')).hexdigest() == encrypted_password,
                '3': lambda pwd: hashlib.sha1(pwd.encode('utf-8')).hexdigest() == encrypted_password,
                '4': lambda pwd: hashlib.sha256(pwd.encode('utf-8')).hexdigest() == encrypted_password,
                
                '5': lambda pwd: pbkdf2_hmac('sha256', pwd.encode('utf-8'), salt, 100000).hex() == encrypted_password,
                
                '6': lambda pwd: base64.b64decode(encrypted_password.encode('utf-8')).decode('utf-8') == pwd
            }
            
            return methods.get(choice, lambda _: False)(password_test)
        except Exception:
            
            ErrorDecrypted()
            return False 

    def RandomCharacter():
        """Performs a brute-force attack using random character generation."""
        global password, salt
        
        try:
            threads_number = int(input(f"{BEFORE}{current_time_hour()}{AFTER} {INPUT} Number of Threads -> {white}"))
            characters_number_min = int(input(f"{BEFORE}{current_time_hour()}{AFTER} {INPUT} Minimum Password Length -> {white}"))
            characters_number_max = int(input(f"{BEFORE}{current_time_hour()}{AFTER} {INPUT} Maximum Password Length -> {white}"))
        except ValueError:
            ErrorNumber()
            return

        password = False 
        generated_passwords = set() 
        salt = "this_is_a_salt".encode('utf-8')
        all_characters = string.ascii_letters + string.digits + string.punctuation

        def GeneratePassword():
            """Generates a random password within the defined length range."""
            length = random.randint(characters_number_min, characters_number_max)
            return ''.join(random.choices(all_characters, k=length))
            
        def TestDecrypted():
            """Worker function for the thread pool to test a single generated password."""
            global password
            while not password:
                password_test = GeneratePassword()
                
                if password_test not in generated_passwords:
                    generated_passwords.add(password_test)
                    
                    if CheckPassword(password_test):
                        password = True 
                        time.sleep(0.5) 
                        print(f'{BEFORE}{current_time_hour()}{AFTER} {ADD} Password found: {white}{password_test}{reset}')
                        time.sleep(1)
                        Continue()
                        Reset()
                        return

        def Request():
            """Manages the thread pool execution."""
            try:
                with ThreadPoolExecutor(max_workers=threads_number) as executor:
                    executor.map(lambda _: TestDecrypted(), range(threads_number))
            except Exception:
                ErrorNumber()

        print(f"{BEFORE}{current_time_hour()}{AFTER} {WAIT} Brute-force password cracking in progress... (This can take a long time){reset}")
        while not password:
            Request()

    def WorldList():
        """Performs a dictionary (wordlist) attack."""
        path_folder_worldlist = os.path.join(tool_path, "2-Input", "WorldList")
        
        if not os.path.isdir(path_folder_worldlist):
            print(f"{BEFORE}{current_time_hour()}{AFTER} {ERROR} WordList folder not found at: {white}{path_folder_worldlist}{reset}")
            Continue()
            Reset()
            return

        print(f"{BEFORE}{current_time_hour()}{AFTER} {INFO} Add more lists to folder: {white}{path_folder_worldlist}")
        print(f"{BEFORE}{current_time_hour()}{AFTER} {WAIT} Password cracking by wordlist in progress... (This can take a long time){reset}")
        
        for file_name in os.listdir(path_folder_worldlist):
            file_path = os.path.join(path_folder_worldlist, file_name)
            if not os.path.isfile(file_path):
                continue
            
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    print(f"{BEFORE}{current_time_hour()}{AFTER} {INFO} Checking file: {white}{file_name}{reset}")

                    for line in f:
                        password_test = line.strip()
                        if CheckPassword(password_test):
                            print(f"{BEFORE}{current_time_hour()}{AFTER} {ADD} Password found: {white}{password_test}{reset}")
                            Continue()
                            Reset()
                            return
            except Exception as e:
                print(f"{BEFORE}{current_time_hour()}{AFTER} {ERROR} Could not read or process file {file_name}: {e}{reset}")
                pass
                
        
        print(f"{BEFORE}{current_time_hour()}{AFTER} {INFO} The entire wordlist has been checked and no passwords match.")
        Continue()
        Reset()
        
    
    
    
    Slow(f"""{decrypted_banner}
{BEFORE}01{AFTER}{white} BCRYPT
{BEFORE}02{AFTER}{white} MD5
{BEFORE}03{AFTER}{white} SHA-1
{BEFORE}04{AFTER}{white} SHA-256
{BEFORE}05{AFTER}{white} PBKDF2 (SHA-256)
{BEFORE}06{AFTER}{white} Base64 Decode
    """)
    
    choice = input(f"{BEFORE}{current_time_hour()}{AFTER} {INPUT} Encryption Method -> {reset}").strip()

    
    if choice in ['1', '01']: choice = '1'
    elif choice in ['2', '02']: choice = '2'
    elif choice in ['3', '03']: choice = '3'
    elif choice in ['4', '04']: choice = '4'
    elif choice in ['5', '05']: choice = '5'
    elif choice in ['6', '06']: choice = '6'
    
    if choice not in ['1', '2', '3', '4', '5', '6']:
        ErrorChoice()

    encrypted_password = input(f"{BEFORE}{current_time_hour()}{AFTER} {INPUT} Encrypted Hash/Password -> {white}").strip()
    Title(f"Password Decryptor - Hash: {encrypted_password}")

    
    print(f"""
{BEFORE}01{AFTER}{white} Random Character (Brute Force)
{BEFORE}02{AFTER}{white} Word List (Dictionary Attack)
""")

    method = input(f"{BEFORE}{current_time_hour()}{AFTER} {INPUT} Cracking Method -> {white}").strip()

    if method in ["01", "1"]:
        RandomCharacter()
    elif method in ["02", "2"]:
        WorldList()
    else:
        ErrorChoice()

except Exception as e:
    Error(e)