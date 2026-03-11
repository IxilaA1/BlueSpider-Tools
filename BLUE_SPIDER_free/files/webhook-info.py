import requests
import sys
import time
from datetime import datetime
import os

    
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




class CustomColors:
    """Minimal class to simulate custom color variables."""
    RESET = "\033[0m"
    RED = "\033[91m"
    WHITE = "\033[97m"


red = CustomColors.RED
white = CustomColors.WHITE
INFO_ADD = "[+]"
BEFORE = "["
AFTER = "]"
INPUT = ">>"

def Title(text):
    """Simulates a custom function to set the terminal title."""
    print(f"\n--- {text} ---")

def Slow(text):
    """Simulates a function for slow/typewriter-style printing."""
    
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        
    print()

def current_time_hour():
    """Simulates a function to get the current time (e.g., [HH:MM])."""
    return datetime.now().strftime("%H:%M")

def CheckWebhook(url):
    """Simulates a custom function to validate the webhook URL format."""
    
    return "discord.com/api/webhooks" in url or "discordapp.com/api/webhooks" in url

def Error(message):
    """Simulates a custom error reporting function."""
    print(f"{CustomColors.RED}ERROR: {message}{CustomColors.RESET}")
    sys.exit(1)

def ErrorWebhook():
    """Simulates a custom function for invalid webhook error."""
    Error("Invalid Webhook URL format.")

def Continue():
    """Simulates a function to pause and wait for user input."""
    input("\nPress Enter to continue...")

def Reset():
    """Simulates a function to restart or reset the state."""
    print("Resetting script state...")
    


def ErrorModule(e):
    """Placeholder for the original ErrorModule function."""
    Error(f"Module Import Error: {e}")
    




Title("Discord Webhook Info")

try:
    def get_webhook_info(webhook_url):
        """Fetches and displays information about a Discord webhook."""
        
        headers = {
            'Content-Type': 'application/json',
        }

       
        response = requests.get(webhook_url, headers=headers)
        response.raise_for_status()
        
        webhook_info = response.json()

        webhook_id = webhook_info.get('id', "None")
        webhook_token = webhook_info.get('token', "None")
        webhook_name = webhook_info.get('name', "None")
        webhook_avatar = webhook_info.get('avatar', "None")
        
        
        webhook_type = "Bot" if webhook_info.get('type') == 1 else "User Webhook" 
        
        channel_id = webhook_info.get('channel_id', "None")
        guild_id = webhook_info.get('guild_id', "None") 

        Slow(f"""
{white}────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
 {INFO_ADD} ID         : {white}{webhook_id}{red}
 {INFO_ADD} Token      : {white}{webhook_token}{red}
 {INFO_ADD} Name       : {white}{webhook_name}{red}
 {INFO_ADD} Avatar     : {white}{webhook_avatar}{red}
 {INFO_ADD} Type       : {white}{webhook_type}{red}
 {INFO_ADD} Channel ID : {white}{channel_id}{red}
 {INFO_ADD} Server ID  : {white}{guild_id}{red}
{white}────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
""")

        if 'user' in webhook_info:
            user_info = webhook_info['user']
            
            user_id = user_info.get('id', "None")
            username = user_info.get('username', "None")
            display_name = user_info.get('global_name', "None") 
            discriminator = user_info.get('discriminator', "None") 
            user_avatar = user_info.get('avatar', "None")
            user_flags = user_info.get('flags', "None")
            accent_color = user_info.get('accent_color', "None")
            avatar_decoration = user_info.get('avatar_decoration_data', "None")
            banner_color = user_info.get('banner_color', "None")

            Slow(f"""{red}User information associated with the Webhook:
{white}────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
 {INFO_ADD} ID          : {white}{user_id}{red}
 {INFO_ADD} Username    : {white}{username}{red}
 {INFO_ADD} Display Name: {white}{display_name}{red}
 {INFO_ADD} Discriminator: {white}{discriminator}{red}
 {INFO_ADD} Avatar      : {white}{user_avatar}{red}
 {INFO_ADD} Public Flags: {white}{user_flags}{red} 
 {INFO_ADD} Accent Color: {white}{accent_color}{red}
 {INFO_ADD} Decoration  : {white}{avatar_decoration}{red}
 {INFO_ADD} Banner Color: {white}{banner_color}{red}
{white}────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
    """)

    
    webhook_url = input(f"\n{BEFORE + current_time_hour() + AFTER} {INPUT} Webhook URL -> {CustomColors.RESET}")
    
    if not CheckWebhook(webhook_url):
        ErrorWebhook() 
    
    get_webhook_info(webhook_url)
    Continue()
    Reset()

except requests.exceptions.HTTPError as errh:
    
    Error(f"HTTP Error: {errh}")
except requests.exceptions.RequestException as err:
    
    Error(f"Request Error: {err}")
except Exception as e:
    
    Error(e)