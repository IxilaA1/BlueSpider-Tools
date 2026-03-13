import concurrent.futures
import random
import subprocess
import sys
import os
import requests
import json
import threading
import time

    
logo_ascii = """
                                                 @@@@@@@@@@@@@@@@@@@                                 
                                         @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                         
                                    @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                    
                                @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                
                             @@@@@@@@@@@@@@@@@@                       @@@@@@@@@@@@@@@@@@             
                           @@@@@@@@@@@@@@                                   @@@@@@@@@@@@@@@          
                        @@@@@@@@@@@@@              @@@@@@@@@@@@@@@              @@@@@@@@@@@@@        
                       @@@@@@@@@@@          @@@@@@@@@@@@@@@@@@@@@@@@@@@@@          @@@@@@@@@@@       
                       @@@@@@@@         @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@         @@@@@@@@       
                        @@@@@        @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@        @@@@@        
                                  @@@@@@@@@@@@@@@                   @@@@@@@@@@@@@@@                  
                                @@@@@@@@@@@@@                           @@@@@@@@@@@@@                
                               @@@@@@@@@@            @@@@@@@@@@@            @@@@@@@@@@               
                                @@@@@@@         @@@@@@@@@@@@@@@@@@@@@         @@@@@@@                
                                            @@@@@@@@@@@@@@@@@@@@@@@@@@@@@                            
                                          @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                          
                                         @@@@@@@@@@@             @@@@@@@@@@@                         
                                        @@@@@@@@@                   @@@@@@@@@                        
                                         @@@@@@        @@@@@@@        @@@@@@                         
                                                    @@@@@@@@@@@@@                                    
                                                   @@@@@@@@@@@@@@@                                   
                                                  @@@@@@@@@@@@@@@@@                                  
                                                  @@@@@@@@@@@@@@@@@                                  
                                                   @@@@@@@@@@@@@@@                                   
                                                    @@@@@@@@@@@@@                                    
                                                       @@@@@@@     
"""


os.system('cls' if os.name == 'nt' else 'clear')


print(logo_ascii)


time.sleep(2)




reset = '\033[0m'
green = '\033[92m'
red = '\033[91m'
white = '\033[97m'
BEFORE = f"[{white}INFO{reset}]"
AFTER = f"{white}|{reset}"
BEFORE_GREEN = f"[{green}SUCCESS{reset}]"
AFTER_GREEN = f"{green}|{reset}"
GEN_VALID = f"[{green}VALID{reset}]"
GEN_INVALID = f"[{red}INVALID{reset}]"
INPUT = f"[{white}INPUT{reset}]"


username_webhook = "IP Checker Bot"
avatar_webhook = "" 
color_webhook = 3066993

def current_time_hour():
    """Simulates the time function for display."""
    return time.strftime("%H:%M:%S")

def Title(text):
    """Simulates the function to change the console title."""
    sys.stdout.write(f"\033]0;{text}\a")
    sys.stdout.flush()

def ErrorModule(e):
    """Simulates import error handling."""
    print(f"Import Error: {e}")
    sys.exit(1)

def CheckWebhook(url):
    """Simulates webhook validation."""
    
    pass 

def ErrorNumber():
    """Simulates thread number error handling."""
    print(f"\n{BEFORE}{AFTER} {red}Error: Invalid Threads Number.{reset}")
    sys.exit(1)

def ErrorPlateform():
    """Simulates platform error handling."""
    print(f"\n{BEFORE}{AFTER} {red}Error: Unsupported Platform.{reset}")
    sys.exit(1)

def Error(e):
    """Simulates general error handling."""
    print(f"\n{BEFORE}{AFTER} {red}General Error: {e}{reset}")
    sys.exit(1)


Title("Ip Generator")

try:
    
    webhook = input(f"\n{BEFORE + current_time_hour() + AFTER} {INPUT} Webhook ? (y/n) -> {reset}")
    if webhook.lower() in ['y', 'yes']:
        webhook_url = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Webhook URL -> {reset}")
        CheckWebhook(webhook_url)
    else:
        webhook_url = None

    try:
        
        threads_number = int(input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Threads Number -> {reset}"))
        if threads_number <= 0:
             raise ValueError
    except ValueError:
        ErrorNumber()

    
    def SendWebhook(embed_content):
        if not webhook_url:
            return 
            
        payload = {
            'embeds': [embed_content],
            'username': username_webhook,
            'avatar_url': avatar_webhook
        }

        headers = {'Content-Type': 'application/json'}

        try:
            
            response = requests.post(webhook_url, data=json.dumps(payload), headers=headers, timeout=5)
            response.raise_for_status() 
        except requests.RequestException as e:
            
            print(f"\n{BEFORE + current_time_hour() + AFTER} {red}Error sending webhook: {e}{reset}")
    
   
    lock = threading.Lock()
    number_valid = 0
    number_invalid = 0

    
    def IpCheck():
        global number_valid, number_invalid

        
        with lock:
            current_valid = number_valid
            current_invalid = number_invalid
            
        ip = ".".join(str(random.randint(1, 255)) for _ in range(4))

        
        PING_TIMEOUT = 1 
        
        try:
            if sys.platform.startswith("win"):
                
                result = subprocess.run(['ping', '-n', '1', '-w', str(int(PING_TIMEOUT*1000)), ip], capture_output=True, text=True, timeout=PING_TIMEOUT + 0.5)
            elif sys.platform.startswith("linux"):
                
                result = subprocess.run(['ping', '-c', '1', '-W', str(PING_TIMEOUT), ip], capture_output=True, text=True, timeout=PING_TIMEOUT + 0.5)
            else:
                ErrorPlateform()

            if result.returncode == 0:
                with lock:
                    number_valid += 1
                
                
                if webhook.lower() in ['y', 'yes']:
                    embed_content = {
                        'title': 'Ip Valid !',
                        'description': f"**Ip:**\n```{ip}```",
                        'color': color_webhook,
                        'footer': {
                            "text": username_webhook,
                            "icon_url": avatar_webhook,
                        }
                    }
                    SendWebhook(embed_content) 
                    
                
                print(f"{BEFORE_GREEN + current_time_hour() + AFTER_GREEN} {GEN_VALID} Logs: {white}{current_invalid} invalid - {current_valid + 1} valid{green} Status:  {white}Valid{green}  Ip: {white}{ip}{green}")
            else:
                with lock:
                    number_invalid += 1
                
                print(f"{BEFORE + current_time_hour() + AFTER} {GEN_INVALID} Logs: {white}{current_invalid + 1} invalid - {current_valid} valid{red} Status: {white}Invalid{red} Ip: {white}{ip}{red}")
                
        except (subprocess.TimeoutExpired, Exception) as e:
           
            with lock:
                number_invalid += 1
            
            print(f"{BEFORE + current_time_hour() + AFTER} {GEN_INVALID} Logs: {white}{current_invalid + 1} invalid - {current_valid} valid{red} Status: {white}Error/Invalid{red} Ip: {white}{ip}{red} ({e.__class__.__name__})")
            
        
        Title(f"Ip Generator - Invalid: {number_invalid} - Valid: {number_valid}")
        
   
    def run_ip_check_loop():
        """Function executed by each thread in an infinite loop."""
        while True:
            IpCheck()
            

    
    def Request():
        """Manages the creation and lifetime of the worker threads."""
        threads = []
        for _ in range(threads_number):
            
            t = threading.Thread(target=run_ip_check_loop, daemon=True)
            threads.append(t)
            t.start()
            

        for t in threads:
            t.join() 
            
    
    Request()
        
except Exception as e:
    Error(e)