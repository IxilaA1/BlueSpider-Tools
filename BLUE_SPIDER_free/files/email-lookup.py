import dns.resolver
import requests
import re
import sys
from typing import Dict, Any, Tuple, Optional, List
import os
import time

   
logo_ascii = """
                                          ...:----:...                                              
                                     .:=#@@@@@@@@@@@@@@%*-..                                        
                                  .:#@@@@@@@%#*****#%@@@@@@@+..                                     
                               ..-@@@@@%-...... ........+@@@@@@..                                   
                               :%@@@@=..   .#@@@@@@@@#=....+@@@@*.                                  
                             .+@@@@=.      .*@@@%@@@@@@@@=...*@@@@:.                                
                            .#@@@%.                 .=@@@@@=. .@@@@-.                               
                           .=@@@#.                    .:%@@@*. -@@@%:.                              
                           .%@@@-                       .*@@*. .+@@@=.                              
                           :@@@#.                              .-@@@#.                              
                           -@@@#                                :%@@@.                              
                           :@@@#.                              .-@@@#.                              
                           .%@@@-.                             .+@@@=.                              
                           .+@@@#.                             -@@@%:.                              
                            .*@@@%.                          .:@@@@-.                               
                             .+@@@@=..                     ..*@@@@:.                                
                               :%@@@@-..                ...+@@@@*.                                  
                               ..-@@@@@%=...         ...*@@@@@@@@#.                                 
                                  .:*@@@@@@@%*++++**@@@@@@@@=:*@@@@#:.                              
                                     ..=%@@@@@@@@@@@@@@%#-.   ..*@@@@%:.                            
                                        .....:::::::....       ...+@@@@%:                           
                                                                  ..+@@@@%-.                        
                                                                    ..=@@@@%-.                      
                                                                      ..=@@@@@=.                    
                                                                         .=%@@@@=.                  
                                                                          ..-%@@@-.                 
                                                                             .... 

"""


os.system('cls' if os.name == 'nt' else 'clear')


print(logo_ascii)


time.sleep(2)


try:
    
    import dns.resolver
except ImportError:
    print("Error: The 'dnspython' library is required.")
    print("Please install it using: pip install dnspython")
    sys.exit(1)



def get_email_info(email: str) -> Tuple[Dict[str, Any], Optional[str], Optional[str], Optional[str], Optional[str]]:
    """
    Retrieves information about an email (domain, MX, SPF, DMARC, etc.).
    """
    info: Dict[str, Any] = {}
    
    
    try:
        parts = email.split('@')
        if len(parts) != 2:
            print("Error: Invalid email format.")
            return info, None, None, None, None
            
        name: Optional[str] = parts[0]
        domain_all: Optional[str] = parts[1] 
        

        match = re.search(r"([^@.]+)\.([^.]+)$", domain_all)
        domain: Optional[str] = match.group(1) if match else None
        
        
        tld: Optional[str] = f".{match.group(2)}" if match else None
        
    except Exception:
        name, domain_all, domain, tld = None, None, None, None

    if not domain_all:
        return info, domain_all, domain, tld, name

    print(f"-> Searching DNS records for domain: {domain_all}")
    
    
    mx_servers: List[str] = []
    try:
        mx_records = dns.resolver.resolve(domain_all, 'MX')

        mx_servers = [record.exchange.to_text() for record in mx_records]
        info["mx_servers"] = mx_servers
    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
        info["mx_servers"] = None
    except Exception as e:
        print(f"Error during MX lookup: {e}")
        info["mx_servers"] = None


    try:

        spf_records = dns.resolver.resolve(domain_all, 'TXT')

        info["spf_records"] = [str(record) for record in spf_records if 'v=spf1' in str(record)]
        if not info["spf_records"]:
             info["spf_records"] = None
    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
        info["spf_records"] = None
    except Exception as e:
        print(f"Error during SPF lookup: {e}")
        info["spf_records"] = None
        

    try:
        dmarc_records = dns.resolver.resolve(f'_dmarc.{domain_all}', 'TXT')
    
        info["dmarc_records"] = [str(record) for record in dmarc_records if 'v=DMARC1' in str(record)]
        if not info["dmarc_records"]:
             info["dmarc_records"] = None
    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
        info["dmarc_records"] = None
    except Exception as e:
        print(f"Error during DMARC lookup: {e}")
        info["dmarc_records"] = None
        
   
    if mx_servers:
        info["google_workspace"] = any("google.com" in server for server in mx_servers)
        info["microsoft_365"] = any("outlook.com" in server or "protection.outlook.com" in server for server in mx_servers)

    return info, domain_all, domain, tld, name

def main():
    """
    Main function for script execution.
    """
    print("\n---  Email Lookup Tool ---")
    
    
    email = input("Enter the Email address to analyze -> ").strip()
    
    if not email:
        print("Operation cancelled. No email address provided.")
        return

    print("--- Retrieving Information... ---")
    
    
    info, domain_all, domain, tld, name = get_email_info(email)

    
    mx_servers = info.get("mx_servers")
    mx_display = ' / '.join(mx_servers) if mx_servers else "N/A"
    
    spf_records = info.get("spf_records")
    spf_display = ' / '.join(spf_records) if spf_records else "N/A"
    
    dmarc_records = info.get("dmarc_records")
    dmarc_display = ' / '.join(dmarc_records) if dmarc_records else "N/A"
    
    google_workspace = info.get("google_workspace", False)
    microsoft_365 = info.get("microsoft_365", False)
    
    print("\n" + "="*80)
    print("                            Analysis Result ")
    print("="*80)
    print(f"  [+] Full Email         : {email}")
    print(f"  [+] Name/Local Part    : {name}")
    print(f"  [+] Full Domain        : {domain_all}")
    print(f"  [+] Second-Level Domain: {domain}")
    print(f"  [+] TLD                : {tld}")
    print("-" * 80)
    print(f"  [+] MX Servers (Mail Exchange)  : {mx_display}")
    print(f"  [+] SPF Records                 : {spf_display}")
    print(f"  [+] DMARC Records               : {dmarc_display}")
    print("-" * 80)
    print(f"  [+] Google Workspace : {'YES' if google_workspace else 'NO'}")
    print(f"  [+] Microsoft 365    : {'YES' if microsoft_365 else 'NO'}")
    print("="*80)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")