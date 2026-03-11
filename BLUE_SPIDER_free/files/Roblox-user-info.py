import requests
import sys
import os
import time
import datetime

   
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


BEFORE = "[ "
AFTER = " ]"
INFO = "INFO"
WAIT = "WAIT"
INPUT_PROMPT = "INPUT"
INFO_ADD = "INFO"
white = Colors.WHITE
red = Colors.RED
reset = Colors.RESET
color = Colors()

def current_time_hour():
    return datetime.datetime.now().strftime("%H:%M:%S")

def ErrorModule(e):
    
    print(f"Module Error: {e}")

def Title(title_text):
    
    print(f"\n--- {title_text} ---\n")

def ChoiceUserAgent():
    
    return "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36"

def ErrorUsername():
    
    print(f"{BEFORE}{current_time_hour()}{AFTER} ERROR: Username not found or an API error occurred.")

def Error(e):
    
    print(f"{BEFORE}{current_time_hour()}{AFTER} GENERAL ERROR: {e}")

def Continue():
    
    input("\nPress Enter to continue...")

def Reset():
    
    print("\n--- Process Finished ---\n")



Title("Roblox User Info")

try:
    
    user_agent = ChoiceUserAgent()
    headers = {"User-Agent": user_agent}

    print(f"\n{BEFORE}{current_time_hour()}{AFTER} {INFO} Selected User-Agent: {white}{user_agent}{color.RESET}")
    
    
    username_input = input(f"{BEFORE}{current_time_hour()}{AFTER} {INPUT_PROMPT} Enter Username -> {color.RESET}")
    
    print(f"{BEFORE}{current_time_hour()}{AFTER} {WAIT} Information Retrieval In Progress...{reset}")

    
    try:
        
        lookup_response = requests.post(
            "https://users.roblox.com/v1/usernames/users",
            headers=headers,
            json={
                "usernames": [username_input],
                "excludeBannedUsers": True
            }
        )
        
        lookup_response.raise_for_status()
        
        lookup_data = lookup_response.json()

        
        if not lookup_data.get('data'):
            ErrorUsername()
            
            sys.exit() 
            
        user_id = lookup_data['data'][0]['id']

        
        info_response = requests.get(f"https://users.roblox.com/v1/users/{user_id}", headers=headers)
        
        info_response.raise_for_status()
        
        user_api_data = info_response.json()

        
        userid = user_api_data.get('id', "N/A")
        display_name = user_api_data.get('displayName', "N/A")
        username = user_api_data.get('name', "N/A")
        
        description = user_api_data.get('description', "N/A").replace('\n', ' ') 
        created_at = user_api_data.get('created', "N/A")
        is_banned = user_api_data.get('isBanned', "N/A")
        external_app_display_name = user_api_data.get('externalAppDisplayName', "N/A")
        has_verified_badge = user_api_data.get('hasVerifiedBadge', "N/A")

        
        print(f"""
{white}────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
 {INFO_ADD} Username           : {white}{username}{red}
 {INFO_ADD} User ID            : {white}{userid}{red}
 {INFO_ADD} Display Name       : {white}{display_name}{red}
 {INFO_ADD} Description        : {white}{description}{red}
 {INFO_ADD} Created At         : {white}{created_at}{red}
 {INFO_ADD} Banned             : {white}{is_banned}{red}
 {INFO_ADD} External App Name  : {white}{external_app_display_name}{red}
 {INFO_ADD} Verified Badge     : {white}{has_verified_badge}{red}
{white}────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
        """)
        
        Continue()
        Reset()
        
    
    except requests.exceptions.RequestException as req_e:
        print(f"{BEFORE}{current_time_hour()}{AFTER} API ERROR: {req_e}")
        ErrorUsername() 
    except KeyError:
        
        ErrorUsername() 


except Exception as e:
    Error(e)