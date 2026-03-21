# (c) 2026 IxilaA1 - Tous droits réservés / All rights reserved / Todos los derechos reservados.
# Ce code ne peut être ni vendu, ni modifié, ni partagé sans autorisation, ni publié à votre nom.
# This code may not be sold, modified, or shared without authorization, nor published under your name.
# Este código no puede ser vendido, modificado ni compartido sin autorización, ni publicado a su nombre.
# -------------------------------------------------------------------------------------------------------
import requests
import sys
import time
import os
from datetime import datetime

   
logo_ascii = """
                                                            >@@|                                                
                                                            >@@|                                                
                                                            >@@|                                                
                                                            >@@|                                                
                                                   >|a@@@@@@@@@|                                                
                                              }@@@@@@@@@@@@@@@@| 000M|                                          
                                          ;@@@@@@O  @@@@@@@@@@@|  j000000_                                      
                                       }@@@@@v   |@@@@@@@@@@@@@| 00J  |00000j                                   
                                     @@@@@_     @@@@@@@@@@@@@@@| 0000    ;00000^                                
                                  ;@@@@v       _@@@@@@@     >@@| 0000v      }0000_                              
                                ^@@@@_         @@@@@@@      ^O@| 00000        ;0000_                            
                                 @@@@;         @@@@@@@      ;p@| 00000         0000^                            
                                   @@@@p       >@@@@@@@^    >@@| 0000v      J0000;                              
                                     O@@@@|     M@@@@@@@@@@@@@@| 0000    >00000                                 
                                       ;@@@@@J^  }@@@@@@@@@@@@@| 00v  j00000}                                   
                                          >@@@@@@@_;@@@@@@@@@@@| ;M000000_                                      
                                              >@@@@@@@@@@@@@@@@| 00000}                                          
                                                   ^jpM@@@@@@@@|                                                
                                                            >@@|                                                
                                                            >@@|                                                
                                                            >@@|                                                
                                                            >@@|                                                
                                                            >@@| 
"""


os.system('cls' if os.name == 'nt' else 'clear')


print(logo_ascii)


time.sleep(2)





class Colors:
    
    RESET = '\033[0m'
    WHITE = '\033[97m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    
    
    INFO = f"[{BLUE}INFO{RESET}]"
    WAIT = f"[{YELLOW}WAIT{RESET}]"
    INPUT_PROMPT = f"[{CYAN}INPUT{RESET}]"
    INFO_ADD = f"[{GREEN}+{RESET}]"

def Title(text):
    """Placeholder for setting the script title."""
    print(f"\n--- {text} ---\n")

def ChoiceUserAgent():
    """Placeholder for choosing a User-Agent."""
    
    return "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36"

def current_time_hour():
    """Placeholder for current time."""
    return datetime.now().strftime("%H:%M:%S")

def log_message(prefix, message, color=""):
    """Simple logging function placeholder."""
    print(f"[{current_time_hour()}] {prefix}: {color}{message}{Colors.RESET}")



try:
    Title("Roblox User Info Checker")

    user_agent = ChoiceUserAgent()
    headers = {"User-Agent": user_agent}

    log_message(Colors.INFO, f"Selected User-Agent: {Colors.WHITE}{user_agent}", color=Colors.WHITE)
    
    try:
        
        user_id_input = input(f"{Colors.INPUT_PROMPT} Enter User ID -> {Colors.RESET}")
        user_id = int(user_id_input)
    except ValueError:
        log_message(f"[{Colors.RED}ERROR{Colors.RESET}]", "Invalid input: User ID must be a number.", color=Colors.RED)
        sys.exit(1)

    log_message(Colors.WAIT, "Retrieving Information...", color=Colors.WHITE)
    
    try:
        
        response = requests.get(f"https://users.roblox.com/v1/users/{user_id}", headers=headers)
        response.raise_for_status()
        user_data = response.json()

        
        fetched_user_id = user_data.get('id', "N/A")
        display_name = user_data.get('displayName', "N/A")
        username = user_data.get('name', "N/A")
        description = user_data.get('description', "N/A").replace('\n', ' ')
        created_at = user_data.get('created', "N/A")
        is_banned = user_data.get('isBanned', "N/A")
        external_app_display_name = user_data.get('externalAppDisplayName', "N/A")
        has_verified_badge = user_data.get('hasVerifiedBadge', "N/A")

        
        print(f"""
{Colors.WHITE}────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
 {Colors.INFO_ADD} Username         : {Colors.WHITE}{username}{Colors.RED}
 {Colors.INFO_ADD} Id               : {Colors.WHITE}{fetched_user_id}{Colors.RED}
 {Colors.INFO_ADD} Display Name     : {Colors.WHITE}{display_name}{Colors.RED}
 {Colors.INFO_ADD} Description      : {Colors.WHITE}{description}{Colors.RED}
 {Colors.INFO_ADD} Created At       : {Colors.WHITE}{created_at}{Colors.RED}
 {Colors.INFO_ADD} Banned           : {Colors.WHITE}{is_banned}{Colors.RED}
 {Colors.INFO_ADD} External Name    : {Colors.WHITE}{external_app_display_name}{Colors.RED}
 {Colors.INFO_ADD} Verified Badge   : {Colors.WHITE}{has_verified_badge}{Colors.RED}
{Colors.WHITE}────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
        """)
        
    except requests.exceptions.HTTPError as http_err:
        if response.status_code == 404:
            log_message(f"[{Colors.RED}ERROR{Colors.RESET}]", f"User not found for ID {user_id_input}. (HTTP 404)", color=Colors.RED)
        else:
            log_message(f"[{Colors.RED}ERROR{Colors.RESET}]", f"HTTP error occurred: {http_err}", color=Colors.RED)
    except requests.exceptions.RequestException as req_err:
        log_message(f"[{Colors.RED}ERROR{Colors.RESET}]", f"An error occurred during the request: {req_err}", color=Colors.RED)

except ImportError as e:
    log_message(f"[{Colors.RED}CRITICAL{Colors.RESET}]", f"Failed to import a required module: {e}. Please ensure 'requests' is installed (pip install requests).", color=Colors.RED)
    sys.exit(1)
except Exception as e:
    log_message(f"[{Colors.RED}CRITICAL{Colors.RESET}]", f"An unexpected error occurred: {e}", color=Colors.RED)
    sys.exit(1)