

import time
import sys
import os
from datetime import datetime


class colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

        
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


BEFORE = f"{colors.BOLD}{colors.WHITE}[{colors.RESET}{colors.BOLD}{colors.CYAN}"
AFTER = f"{colors.RESET}{colors.BOLD}{colors.WHITE}]{colors.RESET}"
INPUT = f"{colors.BOLD}{colors.WHITE}->{colors.RESET}"
WAIT = f"{colors.BOLD}{colors.YELLOW}~{colors.RESET}"
INFO = f"{colors.BOLD}{colors.BLUE}+{colors.RESET}"
ERROR = f"{colors.BOLD}{colors.RED}!{colors.RESET}"

white = colors.WHITE
blue = colors.BLUE
reset = colors.RESET


discord_banner = f"""
{colors.BLUE}
  ____  _                          _ 
 |  _ \(_)___  ___ ___  _ __   ___| |
 | | | | / __|/ __/ _ \| '_ \ / _ \ |
 | |_| | \__ \ (_| (_) | | | |  __/ |
 |____/|_|___/\___\___/|_| |_|\___|_|
{colors.RESET}
"""

def current_time_hour():
    return datetime.now().strftime("%H:%M:%S")

def Slow(text):
    for line in text.split('\n'):
        print(line)
        time.sleep(0.1)

def Title(title):
    os.system(f"title {title}" if os.name == 'nt' else f"echo -n '\033]0;{title}\007'")

def Choice1TokenDiscord():
    return input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Token -> {reset}")

def Continue():
    input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Press Enter to continue...")

def Reset():
    python = sys.executable
    os.execl(python, python, *sys.argv)

def OnlyLinux():
    print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} This browser is only available on Windows.")
    Continue()
    Reset()

def ErrorChoice():
    print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Invalid choice.")
    Continue()
    Reset()

def ErrorModule(e):
    print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Module error: {e}")
    print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Please install required modules: pip install selenium")
    Continue()
    sys.exit(1)

def Error(e):
    print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} An error occurred: {e}")
    Continue()
    Reset()


if __name__ == "__main__":
    Title("Discord Token Login")
    try:
        from selenium import webdriver
        from selenium.webdriver.common.by import By
    except Exception as e:
        ErrorModule(e)

    try:      
        Slow(discord_banner)
        token = Choice1TokenDiscord()

        print(f"""
 {BEFORE}01{AFTER}{white} Chrome (Windows / Linux)
 {BEFORE}02{AFTER}{white} Edge (Windows)
 {BEFORE}03{AFTER}{white} Firefox (Windows)
        """)
        browser = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Browser -> {reset}")
     
        driver = None
        navigator = ""
        
        if browser in ['1', '01']:
            try:
                navigator = "Chrome"
                print(f"{BEFORE + current_time_hour() + AFTER} {WAIT} {navigator} Starting..{blue}")
                driver = webdriver.Chrome()
                print(f"{BEFORE + current_time_hour() + AFTER} {INFO} {navigator} Ready !{blue}")
            except Exception as e:
                print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} {navigator} not installed or driver not up to date: {e}")
                Continue()
                Reset()

        elif browser in ['2', '02']:
            if sys.platform.startswith("linux"):
                OnlyLinux()
            else:
                try:
                    navigator = "Edge"
                    print(f"{BEFORE + current_time_hour() + AFTER} {WAIT} {navigator} Starting..{blue}")
                    driver = webdriver.Edge()
                    print(f"{BEFORE + current_time_hour() + AFTER} {INFO} {navigator} Ready !{blue}")
                except Exception as e:
                    print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} {navigator} not installed or driver not up to date: {e}")
                    Continue()
                    Reset()

        elif browser in ['3', '03']:
            if sys.platform.startswith("linux"):
                OnlyLinux()
            else:
                try:
                    navigator = "Firefox"
                    print(f"{BEFORE + current_time_hour() + AFTER} {WAIT} {navigator} Starting..{blue}")
                    driver = webdriver.Firefox()
                    print(f"{BEFORE + current_time_hour() + AFTER} {INFO} {navigator} Ready !{blue}")
                except Exception as e:
                    print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} {navigator} not installed or driver not up to date: {e}")
                    Continue()
                    Reset()
        else:
            ErrorChoice()
        
        if driver:
            try:
                script = """
                function login(token) {
                    setInterval(() => {
                        document.body.appendChild(document.createElement `iframe`).contentWindow.localStorage.token = `"${token}"`
                    }, 50);
                    setTimeout(() => {
                        location.reload();
                    }, 2500);
                }
                """
                
                driver.get("https://discord.com/login")
                print(f"{BEFORE + current_time_hour() + AFTER} {WAIT} Token Connection..{blue}")
                driver.execute_script(script + f'\nlogin("{token}")')
                time.sleep(4)
                print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Connected Token !{blue}")
                print(f"{BEFORE + current_time_hour() + AFTER} {INFO} If you leave the tool, the browser will close!{blue}")
                Continue()
                driver.quit()
                Reset()
            except Exception as e:
                print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Connection error: {e}")
                if driver:
                    driver.quit()
                Continue()
                Reset()
    except Exception as e:
        Error(e)