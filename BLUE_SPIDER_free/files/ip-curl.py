import requests
import sys
import datetime
import os
import time

    
logo_ascii = """
                                      :**+ :::+*@@.                                                         
                              +: @ = =.  :#@@@@@@@@                 :     .=*@@#     -                      
                 @@@@-. :=: +@@.:% *=@@:   @@@@@@          :#=::     .:@=@@@@@@@@@@@@@@@@@@@@--.-:          
             .#@@@@@@@@@@@@@@@@@@:# .@@   #@@    :@-     +@@:@@@+@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@*        
             #*   :%@@@@@@@@@@:   .@@#*              ..  ##@ *#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@-:- %=         
                   *@@@@@@@@@@@@%@@@@@@@            = @=+@@@@%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@+   #.        
                   #@@@@@@@@@##@@@@@= =#              #@@@#@@@@%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@=            
                  @@@@@@@@@@@#+#@@=                 :@@@-.#-*#@.  .@@.=%@@@@%@@@@@@@@@@@@@@@@@=  +          
                 :@@@@@@@@@@@@@@:                   :@@    # - @@@@@@@ =@@@*#*@@@@@@@@@@@@@=.=-  #:         
                  :@@@@@@@@@@@+                     @@@@@@@: :    @@@@@@@@@@@@@@@@@@@@@@@@@@@               
                   #@@@@@    @                     #%@@@@@@@@@@@@@@@@@:@@@@@@@@@@@@#@@@@@@@@@:              
                     @@@     .                    @@@@@@@@@@@@@@@@-%@@@%@#   @@@@@@#=@#@@@@@==              
                     =@@##@   =:*.                @@@@@@*@@@@@@@@@@-=@@@@.    +@@@:  %#@@#=   :             
                         .=@.                     #@@@@@@@@#@@@@@@@@+#:        %@      *%@=                 
                            . @@@@@@               @#@@*@@@@@@@@@@@@@@@=        :-     -       =.           
                             :@@@@@@@#=                   @@@@@@@@@@@@-               :+%  .@=              
                            -@@@@@@@@@@@@                 @+@@@@*+@@#                   @. @@.#   # :       
                             @@@@@@@@@@@@@@@               @@@@@*@@@                     :=.        @@@.    
                              @@@@@@@@@@@@@                #@@@@@@%@.                             :  :      
                               *@@@@@@@@@@%               :@@@@@@@@@ @@.                      .@@@@=:@      
                                :@@@@@@@@@                 #@@@@@@   @:                    .#@@@@@@@@@@     
                                :@@@@%@@                   .@@@@@-   .                     @@@@@@@@@@@@*    
                                :@@@@@@.                    *@@@-                          @@@@#@@@@@@@     
                                .@@@@@                                                           =@@@:    @=
                                 =@@                                                              =    #+   
                                  @%      

"""


os.system('cls' if os.name == 'nt' else 'clear')


print(logo_ascii)


time.sleep(2)





class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    WHITE = '\033[97m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'

def get_current_time():
    """Returns the current time in HH:MM:SS format."""
    return datetime.datetime.now().strftime("%H:%M:%S")


def Error(e):
    print(f"\n{Colors.RED}[!] ERROR at {get_current_time()}: {e}{Colors.RESET}")
    sys.exit(1)

def Continue():
    input(f"\n{Colors.YELLOW}[?] Press ENTER to continue...{Colors.RESET}")



def ip_lookup_tool():
    """
    Performs an IP address lookup using the ip-api.com service.
    """
    print(f"{Colors.BLUE}--- IP Lookup Tool ---{Colors.RESET}")
    
    try:
        
        ip = input(f"\n{Colors.BLUE}[{get_current_time()}] {Colors.YELLOW}INPUT{Colors.RESET} Ip -> {Colors.WHITE}")
        print(f"{Colors.BLUE}[{get_current_time()}] {Colors.YELLOW}WAIT{Colors.RESET} Searching for information...")

        
        response = requests.get(f"http://ip-api.com/json/{ip}", timeout=5)
        response.raise_for_status()
        
        
        api = response.json()

        
        status = "Valid" if api.get('status') == "success" else "Invalid"
        
        
        country = api.get('country', "None")
        country_code = api.get('countryCode', "None")
        region = api.get('regionName', "None")
        region_code = api.get('region', "None")
        zip_code = api.get('zip', "None")
        city = api.get('city', "None")
        latitude = api.get('lat', "None")
        longitude = api.get('lon', "None")
        timezone = api.get('timezone', "None")
        isp = api.get('isp', "None")
        org = api.get('org', "None")
        as_host = api.get('as', "None")
        
        
        status_color = Colors.GREEN if status == "Valid" else Colors.RED
        
        
        print(f"""
{Colors.WHITE}──────────────────────────────────────────────────────────────────
 {Colors.BLUE} IP: {Colors.WHITE}{ip}{Colors.RESET}
 {Colors.BLUE} Status      : {status_color}{status}{Colors.RESET}
 {Colors.BLUE} Country     : {Colors.WHITE}{country} ({country_code}){Colors.RESET}
 {Colors.BLUE} Region      : {Colors.WHITE}{region} ({region_code}){Colors.RESET}
 {Colors.BLUE} City        : {Colors.WHITE}{city}{Colors.RESET}
 {Colors.BLUE} Zip Code    : {Colors.WHITE}{zip_code}{Colors.RESET}
 {Colors.BLUE} Latitude    : {Colors.WHITE}{latitude}{Colors.RESET}
 {Colors.BLUE} Longitude   : {Colors.WHITE}{longitude}{Colors.RESET}
 {Colors.BLUE} Timezone    : {Colors.WHITE}{timezone}{Colors.RESET}
 {Colors.BLUE} ISP         : {Colors.WHITE}{isp}{Colors.RESET}
 {Colors.BLUE} Organization: {Colors.WHITE}{org}{Colors.RESET}
 {Colors.BLUE} AS Host     : {Colors.WHITE}{as_host}{Colors.RESET}
{Colors.WHITE}──────────────────────────────────────────────────────────────────
""")

        Continue()
        
    except requests.exceptions.RequestException as e:
        
        Error(f"Request failed. Check IP or network: {e}")
    except Exception as e:
        
        Error(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    ip_lookup_tool()