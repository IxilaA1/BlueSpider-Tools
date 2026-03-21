# (c) 2026 IxilaA1 - Tous droits réservés / All rights reserved / Todos los derechos reservados.
# Ce code ne peut être ni vendu, ni modifié, ni partagé sans autorisation, ni publié à votre nom.
# This code may not be sold, modified, or shared without authorization, nor published under your name.
# Este código no puede ser vendido, modificado ni compartido sin autorización, ni publicado a su nombre.
# -------------------------------------------------------------------------------------------------------
import requests
import time
import os
import sys
import ipaddress 
from requests.exceptions import ConnectionError, Timeout, HTTPError

   
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


TIMEOUT_SECONDS = 5
DEFAULT_PROTOCOL = 'http://'
# ---------------------

def is_valid_ip(address):
    """Checks if the given string is a valid IPv4 or IPv6 address."""
    try:
        
        ipaddress.ip_address(address)
        return True
    except ValueError:
        return False

def check_website_status(url, timeout):
    """Checks the status and response time of a website."""

    
    target = url.strip().rstrip('/')
    
    
    if is_valid_ip(target):
        
        if not target.startswith(('http://', 'https://')):
            url_to_check = DEFAULT_PROTOCOL + target
            print(f"INFO: Input is an IP address. Trying with protocol: {url_to_check}")
        else:
            url_to_check = target
    
    
    elif not target.startswith(('http://', 'https://')):
        
        url_to_check = 'https://' + target
        print(f"INFO: Automatically trying URL as: {url_to_check}")
    else:
        
        url_to_check = target
        
    print(f"\n--- Starting Health Check ---")
    print(f"Target URL: {url_to_check}")
    print(f"Timeout set to: {timeout} seconds")
    
    
    print("Checking website status...")
    
    try:
       
        start_time = time.time()
        
        
        response = requests.get(url_to_check, timeout=timeout)
        
        
        end_time = time.time()
        
        
        response_time = end_time - start_time
        
        print("\n[RESULT]")
        
        
        if response.status_code == 200:
            print("STATUS: The website is CONNECTED and running WELL.")
            print(f"HTTP Status Code: {response.status_code} (OK)")
        else:
            print(f"STATUS: The website is CONNECTED but returned an ERROR.")
            print(f"HTTP Status Code: {response.status_code} (Problem! Check the error code)")
            
        
        print(f"Response Time: {response_time:.2f} seconds.")

        
        if response_time > 3.0:
            print("\nWARNING: This time is very SLOW! A slow response can be a sign of **HIGH LOAD** or an attack like DDoS.")
        elif response_time > 1.0:
            print("\nNOTE: The time is a bit slow. The server might be busy (high traffic).")
        else:
            print("\nNOTE: The time is very fast. The server is likely very healthy and handling traffic easily.")
            
    except Timeout:
        print("\nCRITICAL FAILURE:")
        print(f"STATUS: TIMEOUT! The website took longer than {timeout} seconds to answer.")
        print(f"This is a strong sign of a MAJOR PROBLEM or a DDoS attack that is overloading the server.")
    except ConnectionError:
        print("\nCRITICAL FAILURE:")
        print("STATUS: NOT CONNECTED! The website address is unreachable.")
        print("The site is likely DOWN (off or completely overloaded/broken).")
    except HTTPError as e:
        print(f"\nCRITICAL FAILURE: An HTTP error occurred: {e}")
    except Exception as e:
        print(f"\nUNEXPECTED ERROR: An unexpected error occurred: {e}")
    
    print("\n--- Check Complete ---")



if __name__ == "__main__":
    
    
    try:
        import ipaddress
    except ImportError:
        print("\n**ERROR**: The 'ipaddress' module is required. Please install it using: pip install ipaddress")
        sys.exit(1)
        
    
    target_input = input("Please enter the website URL (google.com) or IP address (192.168.1.1): ")
    
    
    if not target_input:
        print("\nERROR: No URL or IP entered. Exiting program.")
        sys.exit(1)
        
    
    check_website_status(target_input, TIMEOUT_SECONDS)