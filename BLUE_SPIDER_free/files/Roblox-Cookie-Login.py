# (c) 2026 IxilaA1 - Tous droits réservés / All rights reserved / Todos los derechos reservados.
# Ce code ne peut être ni vendu, ni modifié, ni partagé sans autorisation, ni publié à votre nom.
# This code may not be sold, modified, or shared without authorization, nor published under your name.
# Este código no puede ser vendido, modificado ni compartido sin autorización, ni publicado a su nombre.
# -------------------------------------------------------------------------------------------------------
import sys
import time
import os
from selenium import webdriver
from selenium.common.exceptions import WebDriverException, SessionNotCreatedException

   
logo_ascii = """
                                                         .+#%@@%#+.                                     
                                                    .#@@@@@@@@@@@@@@@@#.                                
                                                  +@@@@@@@@@@@@@@@@@@@@@@*                              
                                                .%@@@@@@@@@@@@@@@@@@@@@@@@%.                            
                                                %@@@@@@@@@@@@@@@@@@@@@@@@@@%                            

                                               %@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#                          
                                                -..........................-.                           
                                                %@@@@@@00@@@@@@@@@@@%@@@@@@%                            
                                                %@@@#     .%@@@@%.     *@@@%                            
                                                . :+00+--+%@#::#@%*--+00+: .                            
                                                                           .                            
                                                 :                        :                             
                                                  -                      =                              
                                                    -                  -                                
                                                       -=          --                                   
                                               -+#%@@@@@@=        =@@@@@@%#+-                           
                                            *@@@@@@@@@@@@=        =@@@@@@@@@@@@*                        
                                          *@@@@@@@@@@@@@@+        +@@@@@@@@@@@@@@#                      
                                         *@@@@@@@@@@@@@@@@%=    -%@@@@@@@@@@@@@@@@#                     
                                        -@@@@@@@@@@@@@@@@@@@%#*0@@@@@@@@@@@@@@@@@@@-                    
                                        -@@@@@@@@@@@@@@@@@@@%::%@@@@@@@@@@@@@@@@@@@-                    
                                        -@@@@@@@@@@@@@@@@@@@%::%@@@@@@@@@@@@@@@@@@@-                    
                                        -@@@@@@@@@@@@@@@@@@@%::%@@@@@@@@@@@@@@@@@@@-
"""


os.system('cls' if os.name == 'nt' else 'clear')


print(logo_ascii)


time.sleep(2)





BEFORE = "[ "
AFTER = " ]"
INPUT = ">>"
WAIT = "(+)"
INFO = "(*)"
ERROR = "(!)"
white = "\033[97m" 
blue = "\033[94m"   
reset = "\033[0m" 


def current_time_hour():
    return time.strftime("%H:%M:%S")

def Title(text):
    print(f"\n--- {text} ---")
    
def ErrorModule(e):
    print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Module error at startup: {e}{reset}")
    sys.exit(1)

def Continue():
    input("\nPress ENTER to continue...")

def Reset():

    global driver 
    if 'driver' in globals() and driver is not None:
        try:
            driver.quit()
        except:
            pass
    sys.exit(0)

def OnlyLinux():
    print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} This browser is not supported by this script on Linux.{reset}")
    Continue()
    Reset()

def ErrorChoice():
    print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Invalid browser choice.{reset}")
    Continue()
    Reset()

def Error(e):
    print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} An unexpected error occurred: {e}{reset}")
   
    global driver 
    if 'driver' in globals() and driver is not None:
        try:
            driver.quit()
        except:
            pass
    sys.exit(1)




try:
    
    Title("Roblox Cookie Login")
    
    
    driver = None
    navigator = None

    cookie = input(f"\n{BEFORE + current_time_hour() + AFTER} {INPUT} Cookie -> {white}")
    
    if not cookie:
        print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} The cookie cannot be empty.{reset}")
        Continue()
        Reset()
        
    print(f"""
{BEFORE}01{AFTER}{white} Chrome (Windows / Linux)
{BEFORE}02{AFTER}{white} Edge (Windows)
{BEFORE}03{AFTER}{white} Firefox (Windows)
    """)
    browser = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Browser -> {reset}")
 
    try:
        if browser in ['1', '01']:
            navigator = "Chrome"
            print(f"{BEFORE + current_time_hour() + AFTER} {WAIT} {navigator} Starting..{blue}")
            driver = webdriver.Chrome()
            print(f"{BEFORE + current_time_hour() + AFTER} {INFO} {navigator} Ready!{blue}")

        elif browser in ['2', '02']:
            if sys.platform.startswith("linux"):
                OnlyLinux()
            else:
                navigator = "Edge"
                print(f"{BEFORE + current_time_hour() + AFTER} {WAIT} {navigator} Starting..{blue}")
                driver = webdriver.Edge()
                print(f"{BEFORE + current_time_hour() + AFTER} {INFO} {navigator} Ready!{blue}")

        elif browser in ['3', '03']:
            if sys.platform.startswith("linux"):
                OnlyLinux()
            else:
                navigator = "Firefox"
                print(f"{BEFORE + current_time_hour() + AFTER} {WAIT} {navigator} Starting..{blue}")
                driver = webdriver.Firefox()
                print(f"{BEFORE + current_time_hour() + AFTER} {INFO} {navigator} Ready!{blue}")
        else:
            ErrorChoice()
            

    
    except (WebDriverException, SessionNotCreatedException) as e:
        print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} {navigator} not installed or driver not up to date. Details: {e}{reset}")
        Continue()
        Reset()
    
    
    if driver:
        try:
            driver.get("https://www.roblox.com/Login")
            print(f"{BEFORE + current_time_hour() + AFTER} {WAIT} Cookie Connection..{blue}")
            
            
            driver.add_cookie({"name" : ".ROBLOSECURITY", "value" : cookie})
            
            print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Connected Cookie!{blue}")
            print(f"{BEFORE + current_time_hour() + AFTER} {WAIT} Refreshing The Page..{blue}")
            
            driver.refresh()
            
            
            time.sleep(1) 
            
            
            driver.get("https://www.roblox.com/users/profile")
            
            
            if "/login" in driver.current_url.lower():
                 
                 print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Connection failed. Invalid or expired cookie.{reset}")
            else:
                 
                 print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Connected!{blue}")
                 print(f"{BEFORE + current_time_hour() + AFTER} {INFO} If you close the tool, {navigator} will close!{blue}")
            
            Continue()
            Reset()
            
        except Exception as e:
            
            print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Connection/navigation error: {e}{reset}")
            Continue()
            Reset()
            
except Exception as e:
    Error(e)