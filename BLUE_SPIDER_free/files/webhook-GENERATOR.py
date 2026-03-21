# (c) 2026 IxilaA1 - Tous droits réservés / All rights reserved / Todos los derechos reservados.
# Ce code ne peut être ni vendu, ni modifié, ni partagé sans autorisation, ni publié à votre nom.
# This code may not be sold, modified, or shared without authorization, nor published under your name.
# Este código no puede ser vendido, modificado ni compartido sin autorización, ni publicado a su nombre.
# -------------------------------------------------------------------------------------------------------
import string
import requests
import json
import random
import threading
import time
import sys
import os
from typing import Optional

    
logo_ascii = """
                                              @@@@                @%@@                                      
                                       @@@@@@@@@@@@               @@@@@@@@@@%                               
                                  @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                          
                                 @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%                         
                                %@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                        
                               @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                       
                              @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                      
                             @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                     
                            @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%                    
                           @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                   
                          %@@@@@@@@@@@@@@@@@@    @@@@@@@@@@@@@@@@@@    @@@@@@@@@@@@@@@@@@%                  
                          %@@@@@@@@@@@@@@@@        %@@@@@@@@@@@%@        @@@@@@@@@@@@@@@@@                  
                          %@@@@@@@@@@@@@@@          @@@@@@@@@@@@          @@@@@@@@@@@@@@@%                  
                         %@@@@@@@@@@@@@@@@          @@@@@@@@@@@%          %@@@@@@@@@@@@@@@@                 
                         @@@@@@@@@@@@@@@@@%         @@@@@@@@@@@%         %@@@@@@@@@@@@@@@@@                 
                         @@@@@@@@@@@@@@@@@@@      %@@@@@@@@@@@@@@@      @@@@@@@@@@@@@@@@@@%                 
                         %@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%                 
                         @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%                 
                         @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                 
                         @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%                 
                           @%@@@@@@@@@@@@@%@@   @@@@%@@@@@@@@@%%%@%@@  @@@@@@@@@@@@@@@@@@                   
                              @@%@@@@@@@@@@@@@                        @%@@@@@@@@@@@%@@                      
                                   @%@@@@@@@                            @@@@@@%%@                           
                                         @@                              @@             

"""


os.system('cls' if os.name == 'nt' else 'clear')


print(logo_ascii)


time.sleep(2)




def get_time_str():
    """Returns a formatted timestamp for console output."""
    return time.strftime("[%H:%M:%S]")


GREEN = '\033[92m'
RED = '\033[91m'
WHITE = '\033[97m'
RESET = '\033[0m'
INPUT_PROMPT = f"{get_time_str()} [INPUT]"
STATUS_VALID = f"{GREEN}VALID{RESET}"
STATUS_INVALID = f"{RED}INVALID{RESET}"
STATUS_ERROR = f"{RED}ERROR{RESET}"


USERNAME_WEBHOOK = "Webhook Checker Bot"
AVATAR_WEBHOOK = "https://i.imgur.com/your-avatar-here.png"
COLOR_WEBHOOK = 3066993


WEBHOOK_URL_NOTIFY: Optional[str] = None
THREADS_NUMBER = 0

def handle_error(e: Exception, context: str = "Script"):
    """Handles exceptions gracefully and exits if critical."""
    print(f"{get_time_str()} {RED}[ERROR]{RESET} {context} failed: {e}")
    if context == "Module Import":
        sys.exit(1)

def is_valid_notify_webhook(url: str) -> bool:
    """Checks if the provided notification webhook URL is valid."""
    if not url.startswith("https://discord.com/api/webhooks/"):
        return False
    try:
        response = requests.head(url, timeout=5)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False



def send_notification_webhook(embed_content: dict):
    """Sends a notification to the configured webhook URL."""
    if not WEBHOOK_URL_NOTIFY:
        return

    payload = {
        'embeds': [embed_content],
        'username': USERNAME_WEBHOOK,
        'avatar_url': AVATAR_WEBHOOK
    }

    headers = {
        'Content-Type': 'application/json'
    }

    try:
        requests.post(WEBHOOK_URL_NOTIFY, data=json.dumps(payload), headers=headers, timeout=5)
    except requests.exceptions.RequestException as e:
        print(f"{get_time_str()} {RED}[ERROR]{RESET} Failed to send notification: {e}")

def generate_and_check_webhook():
    """Generates a random webhook URL and checks its status."""

    first_part = ''.join([str(random.randint(0, 9)) for _ in range(19)])
    

    token_chars = string.ascii_letters + string.digits + '-' + '_'
    second_part = ''.join(random.choice(token_chars) for _ in range(68))
    
    webhook_test_code = f"{first_part}/{second_part}"
    webhook_test_url = f"https://discord.com/api/webhooks/{webhook_test_code}"

    try:

        response = requests.head(webhook_test_url, timeout=5) 
        status_code = response.status_code
        
        if status_code == 200:
            print(f"{get_time_str()} {GREEN}[FOUND]{RESET} Status: {STATUS_VALID} Webhook: {WHITE}{webhook_test_url}{RESET}")
            
            if WEBHOOK_URL_NOTIFY:
                embed_content = {
                    'title': 'Webhook Found!',
                    'description': f"**Valid Webhook:**\n```{webhook_test_url}```",
                    'color': COLOR_WEBHOOK,
                    'footer': {
                        "text": USERNAME_WEBHOOK,
                        "icon_url": AVATAR_WEBHOOK,
                    }
                }
                send_notification_webhook(embed_content)
        else:
            
            print(f"{get_time_str()} {RED}[CHECK]{RESET} Status: {STATUS_INVALID} Webhook: {WHITE}{webhook_test_code}{RESET} (Code: {status_code})")
    except requests.exceptions.RequestException:
        print(f"{get_time_str()} {RED}[CHECK]{RESET} Status: {STATUS_ERROR} Webhook: {WHITE}{webhook_test_code}{RESET} (Connection Error)")

def run_generator():
    """Manages the thread pool for checking webhooks."""
    threads = []
    
    print(f"\n{get_time_str()} [INFO] Starting generator with {THREADS_NUMBER} threads...")
    
    try:
        for _ in range(THREADS_NUMBER):
            t = threading.Thread(target=generate_and_check_webhook)
            t.daemon = True
            t.start()
            threads.append(t)
            
        
        while True:

            time.sleep(1) 
    except KeyboardInterrupt:
        print(f"\n{get_time_str()} [INFO] Generator stopped by user.")
    except Exception as e:
        handle_error(e, "Generator Loop")



if __name__ == "__main__":
    print("\n\n" + "="*40)
    print("      Discord Webhook Generator/Checker")
    print("="*40 + "\n")
    
    try:
        
        webhook_notify_choice = input(f"{INPUT_PROMPT} Do you want to send valid webhooks to a notification webhook? (y/n) -> {RESET}").strip().lower()
        
        if webhook_notify_choice in ['y', 'yes']:
            while True:
                webhook_url_input = input(f"{INPUT_PROMPT} Notification Webhook URL -> {RESET}").strip()
                if is_valid_notify_webhook(webhook_url_input):
                    WEBHOOK_URL_NOTIFY = webhook_url_input
                    print(f"{get_time_str()} {GREEN}[INFO]{RESET} Notification webhook confirmed.")
                    break
                else:
                    print(f"{get_time_str()} {RED}[ERROR]{RESET} Invalid or unreachable webhook URL.")
        
        
        while True:
            try:
                threads_number_input = input(f"{INPUT_PROMPT} Number of Threads -> {RESET}").strip()
                THREADS_NUMBER = int(threads_number_input)
                if THREADS_NUMBER > 0:
                    break
                else:
                    print(f"{get_time_str()} {RED}[ERROR]{RESET} Please enter a number greater than 0.")
            except ValueError:
                print(f"{get_time_str()} {RED}[ERROR]{RESET} Invalid input. Please enter an integer.")

        
        run_generator()

    except Exception as e:
        handle_error(e, "Main Execution")