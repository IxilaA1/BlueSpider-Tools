# (c) 2026 IxilaA1 - Tous droits réservés / All rights reserved / Todos los derechos reservados.
# Ce code ne peut être ni vendu, ni modifié, ni partagé sans autorisation, ni publié à votre nom.
# This code may not be sold, modified, or shared without authorization, nor published under your name.
# Este código no puede ser vendido, modificado ni compartido sin autorización, ni publicado a su nombre.
# -------------------------------------------------------------------------------------------------------
import webbrowser
import requests
import time
import datetime
import sys
import os




BLUE = '\033[94m'
CYAN = '\033[96m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
WHITE = '\033[97m'
RESET = '\033[0m'


BEFORE = f"[{BLUE}SPIDER{RESET}]"
AFTER = f"{GREEN}>>{RESET}"
INPUT = f" {YELLOW}[?]{RESET} "
INFO = f" {CYAN}[i]{RESET} "
ERROR_TAG = f" {RED}[!]{RESET} "

discord_banner = f"""
{BLUE}
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
{RESET}
"""

def Title(text):
    """Sets the console window title (Windows only using os.system)."""
    if sys.platform.startswith('win'):
        import os
        os.system(f'title {text}')
    print(f"{GREEN}--- {text} ---{RESET}")

def Slow(text, delay=0.001):
    """Prints text slowly to simulate a vintage terminal effect."""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)

def current_time_hour():
    """Returns the current hour in HH:MM format."""
    return datetime.datetime.now().strftime("%H:%M")

def ErrorModule(e):
    """Handles errors during import."""
    print(f"\n{ERROR_TAG} {RED}FATAL: Failed to import a required module.{RESET}")
    print(f"{ERROR_TAG} Details: {e}")
    sys.exit(1)

def Error(e):
    """Handles general runtime errors."""
    print(f"\n{ERROR_TAG} {RED}An unexpected error occurred during execution.{RESET}")
    print(f"{ERROR_TAG} Details: {e}")
    Reset()

def ErrorId():
    """Handles invalid Bot ID input."""
    print(f"{ERROR_TAG} {RED}Invalid Bot ID. Please enter a numerical ID.{RESET}")

def Continue():
    """Pauses execution until the user presses Enter."""
    input(f"\n{BEFORE} {INPUT} Press {YELLOW}ENTER{RESET} to continue... {RESET}")

def Reset():
    """A mock function, typically used to clear the screen."""
    
    pass 



try:
    import webbrowser
    import requests
except Exception as e:
    ErrorModule(e)

Title("Discord Invite Bot ID Generator")

try:
    Slow(discord_banner)

    
    while True:
        try:
            bot_id_str = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Enter bot ID -> {RESET}")
            id_bot = int(bot_id_str)
            break
        except ValueError:
            ErrorId()


    invite_url = f'https://discord.com/oauth2/authorize?client_id={id_bot}&scope=bot&permissions=8'
    
    
    try:
        response = requests.get(invite_url)
        print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Invite URL: {WHITE + invite_url} (Status: {response.status_code})")
    except requests.exceptions.RequestException as req_e:
        print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Invite URL: {WHITE + invite_url} (Could not verify status: {req_e})")


    
    choice = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Open in browser? (y/n) -> {RESET}")
    
    if choice.lower() in ['y', 'yes']:
        webbrowser.open_new_tab(invite_url)
        print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Opening invite URL in browser...")
        Continue()
        Reset()
    else:
        print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Copy and paste the URL manually.")
        Continue()
        Reset()

except Exception as e:
    Error(e)
