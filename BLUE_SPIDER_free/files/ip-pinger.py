# (c) 2026 IxilaA1 - Tous droits réservés / All rights reserved / Todos los derechos reservados.
# Ce code ne peut être ni vendu, ni modifié, ni partagé sans autorisation, ni publié à votre nom.
# This code may not be sold, modified, or shared without authorization, nor published under your name.
# Este código no puede ser vendido, modificado ni compartido sin autorización, ni publicado a su nombre.
# -------------------------------------------------------------------------------------------------------
import concurrent.futures
import time
import socket
import sys
import os



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


class Colors:
    RESET = '\033[0m'
    RED = '\033[91m'
    WHITE = '\033[97m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    
    BEFORE = "" 
    AFTER = " "
    ADD = "[SUCCESS]"
    ERROR = "[ERROR]"
    INPUT = "[INPUT]"


def current_time_hour():
    return time.strftime("[%H:%M:%S]")

def Error(e):
    print(f"{current_time_hour()} {Colors.RED}[FATAL ERROR]{Colors.RESET} : {e}", file=sys.stderr)
    sys.exit(1)

def ErrorNumber():
    print(f"{current_time_hour()} {Colors.RED}[INPUT ERROR]{Colors.RESET} : Please enter a valid number for the port and bytes.")
    
def Title(text):
    print(f"\n--- {text} ---")



Title("Ip Pinger")
print("Operation Mode: Repetitive TCP connection attempt (Port Scan).")

def PingIp(hostname, port, bytes_to_send=64):
    """
    Attempts to establish a TCP connection to hostname:port and send a small packet.
    """
    try:
        
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            
            sock.settimeout(1) 
            start_time = time.time()
            
            
            sock.connect((hostname, port))
            
            
            data = b'\x00' * bytes_to_send
            sock.sendall(data)
            
            end_time = time.time()
            elapsed_time = (end_time - start_time) * 1000
            
            
            output = (
                f"{Colors.BEFORE}{current_time_hour()}{Colors.AFTER} {Colors.ADD} "
                f"Hostname: {Colors.WHITE}{hostname}{Colors.RESET} "
                f"time: {Colors.WHITE}{elapsed_time:.2f}ms{Colors.RESET} "
                f"port: {Colors.WHITE}{port}{Colors.RESET} "
                f"bytes: {Colors.WHITE}{bytes_to_send}{Colors.RESET} "
                f"status: {Colors.GREEN}succeed{Colors.RESET}"
            )
            print(output)
            
    except socket.timeout:
        
        output = (
            f"{Colors.BEFORE}{current_time_hour()}{Colors.AFTER} {Colors.ERROR} "
            f"Hostname: {Colors.WHITE}{hostname}{Colors.RESET} "
            f"time: {Colors.WHITE}0ms{Colors.RESET} "
            f"port: {Colors.WHITE}{port}{Colors.RESET} "
            f"bytes: {Colors.WHITE}{bytes_to_send}{Colors.RESET} "
            f"status: {Colors.RED}fail (Timeout){Colors.RESET}"
        )
        print(output)
        
    except ConnectionRefusedError:
         
        output = (
            f"{Colors.BEFORE}{current_time_hour()}{Colors.AFTER} {Colors.ERROR} "
            f"Hostname: {Colors.WHITE}{hostname}{Colors.RESET} "
            f"time: {Colors.WHITE}0ms{Colors.RESET} "
            f"port: {Colors.WHITE}{port}{Colors.RESET} "
            f"bytes: {Colors.WHITE}{bytes_to_send}{Colors.RESET} "
            f"status: {Colors.YELLOW}fail (Refused){Colors.RESET}"
        )
        print(output)
        
    except Exception as e:
        
        output = (
            f"{Colors.BEFORE}{current_time_hour()}{Colors.AFTER} {Colors.ERROR} "
            f"Hostname: {Colors.WHITE}{hostname}{Colors.RESET} "
            f"time: {Colors.WHITE}0ms{Colors.RESET} "
            f"port: {Colors.WHITE}{port}{Colors.RESET} "
            f"bytes: {Colors.WHITE}{bytes_to_send}{Colors.RESET} "
            f"status: {Colors.RED}fail ({e}){Colors.RESET}"
        )
        print(output)



try:
    
    hostname = input(f"{Colors.BEFORE}{current_time_hour()}{Colors.AFTER} {Colors.INPUT} Ip -> {Colors.RESET}")
    
    
    port_input = input(f"{Colors.BEFORE}{current_time_hour()}{Colors.AFTER} {Colors.INPUT} Port (enter for default 80) -> {Colors.RESET}")
    try:
        port = int(port_input) if port_input else 80
    except ValueError:
        ErrorNumber()
        sys.exit(1)
        
    
    bytes_input = input(f"{Colors.BEFORE}{current_time_hour()}{Colors.AFTER} {Colors.INPUT} Bytes (enter for default 64) -> {Colors.RESET}")
    try:
        bytes_to_send = int(bytes_input) if bytes_input else 64
    except ValueError:
        ErrorNumber()
        sys.exit(1)

    print(f"\n{current_time_hour()} [INFO] Starting Pinger on {hostname}:{port} (Repeating every 2 seconds).")
    
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        while True:
            
            executor.submit(PingIp, hostname, port, bytes_to_send)
            
            
            time.sleep(2) 

except KeyboardInterrupt:
    print(f"\n{current_time_hour()} [INFO] Stopped by user.")
    sys.exit(0)
    
except Exception as e:
    Error(e)