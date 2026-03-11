import socket
import concurrent.futures
import sys
import argparse
import time
import os
from datetime import datetime

   
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


TIMEOUT = 0.5
MAX_WORKERS = 100
DEFAULT_PORTS = range(1, 1025)


PORT_PROTOCOL_MAP = {
    21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS", 69: "TFTP",
    80: "HTTP", 110: "POP3", 123: "NTP", 143: "IMAP", 194: "IRC", 389: "LDAP",
    443: "HTTPS", 161: "SNMP", 3306: "MySQL", 5432: "PostgreSQL", 6379: "Redis",
    1521: "Oracle DB", 3389: "RDP", 8080: "HTTP-Alt"
}



def get_current_time():
    """Returns the current time formatted as HH:MM:SS."""
    return datetime.now().strftime("%H:%M:%S")

def identify_protocol(port):
    """Identifies the protocol based on the well-known port number."""
    return PORT_PROTOCOL_MAP.get(port, "Unknown")

def scan_port(ip, port):
    """Attempts to connect to a given port and prints the result if open."""
    try:
        
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(TIMEOUT)
            
            
            result = sock.connect_ex((ip, port))
            
            if result == 0:
                protocol = identify_protocol(port)
               
                print(f"[{get_current_time()}] [OPEN] Port: {port:<5} | Protocol: {protocol}")
                return True
                
    except socket.gaierror:
        
        print(f"[{get_current_time()}] [ERROR] Address resolution failed for scanning.")
        sys.exit(1)
    except Exception:
        
        pass



def port_scanner(ip, ports_to_scan):
    """
    Manages the port scanning process using a thread pool for concurrency.
    """
    print(f"\n[{get_current_time()}] [INFO] Starting port scan on target: {ip}")
    print(f"[{get_current_time()}] [INFO] Scanning {len(ports_to_scan)} port(s) with {MAX_WORKERS} threads.")
    
    start_time = time.time()
    open_ports_count = 0

    try:
        
        target_ip = socket.gethostbyname(ip)
    except socket.gaierror:
        print(f"[{get_current_time()}] [ERROR] Hostname or IP could not be resolved: {ip}")
        return

    
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        
        results = executor.map(lambda port: scan_port(target_ip, port), ports_to_scan)

        
        open_ports_count = sum(1 for result in results if result)

    end_time = time.time()
    
    print(f"[{get_current_time()}] [DONE] Scan finished. {open_ports_count} open port(s) found.")
    print(f"[{get_current_time()}] [INFO] Total time taken: {end_time - start_time:.2f} seconds.")



if __name__ == "__main__":
    
    
    parser = argparse.ArgumentParser(
        description="A simple, fast, multithreaded TCP Port Scanner.",
        usage="%(prog)s [-h] [-p PORTS] ip"
    )
    parser.add_argument("ip", help="The target IP address or hostname to scan.")
    parser.add_argument("-p", "--ports", 
                        help="Port range or list to scan (e.g., 1-1000 or 80,443,8080).", 
                        default=None)
    
    args = parser.parse_args()
    
    
    scan_ports = []
    
    if args.ports:
        
        if '-' in args.ports:
            try:
                start, end = map(int, args.ports.split('-'))
                scan_ports = list(range(start, end + 1))
            except ValueError:
                print(f"[{get_current_time()}] [ERROR] Invalid port range format. Use X-Y (e.g., 1-1000).")
                sys.exit(1)
        
        else:
            try:
                scan_ports = [int(p.strip()) for p in args.ports.split(',')]
            except ValueError:
                print(f"[{get_current_time()}] [ERROR] Invalid port list format. Use comma-separated ports (e.g., 80,443).")
                sys.exit(1)
    else:
        
        scan_ports = list(DEFAULT_PORTS)
        
    
    port_scanner(args.ip, scan_ports)