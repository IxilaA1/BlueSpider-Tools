import requests
import time
import sys
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




class Color:
    """A placeholder class for text color constants."""
    RESET = '\033[0m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    
color = Color()
BEFORE = f"[{color.YELLOW}Time{color.RESET}] "
AFTER = ""
INPUT = f"[{color.GREEN}INPUT{color.RESET}]"
INFO = f"[{color.GREEN}INFO{color.RESET}]"
ERROR = f"[{color.RED}ERROR{color.RESET}]"

def current_time_hour():
    """Placeholder for getting the current time in HH:MM:SS format."""
    return time.strftime("%H:%M:%S")

def Title(text):
    """Placeholder function to set the console title or print a banner."""
    if os.name == 'nt':
        os.system(f"title {text}")
    print(f"\n{color.YELLOW}--- {text} ---{color.RESET}")

def CheckWebhook(url):
    """
    Placeholder function to validate if the URL is a correct webhook format.
    Replace 'True' with your actual validation logic.
    """
    if "discord.com/api/webhooks" in url:
        return True
    return False

def ErrorWebhook():
    """Placeholder function to handle and display a webhook error message."""
    print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Invalid Webhook URL or deletion failed (e.g., 404 Not Found).")
    Continue()

def Continue():
    """Placeholder function to prompt the user to continue."""
    input(f"\n{BEFORE + current_time_hour() + AFTER} {INFO} Press ENTER to continue...{color.RESET}")

def Reset():
    """Placeholder function to exit the script (assuming 'Reset' means end/exit)."""
    sys.exit()

def Error(e):
    """Placeholder function to handle and display a general exception."""
    print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} An unexpected error occurred: {e}{color.RESET}")
    sys.exit()
    


Title("Discord Webhook Delete")

try:
    
    webhook_url = input(f"\n{BEFORE + current_time_hour() + AFTER} {INPUT} Webhook URL -> {color.RESET}")
    
    
    if CheckWebhook(webhook_url) == False:
        ErrorWebhook() 
        
    else:
        
        try:
            print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Attempting to delete webhook...")
            
            response = requests.delete(webhook_url)
            response.raise_for_status()
            
            
            print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Webhook successfully Deleted.")
            Continue() 
            Reset() 
            
        except requests.exceptions.RequestException as e:
            
            ErrorWebhook()
            
except Exception as e:
    
    Error(e)