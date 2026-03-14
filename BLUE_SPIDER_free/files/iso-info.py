import os
import time
from tabulate import tabulate 

   
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

def display_os_ratings_text():
    """
    Displays a structured table of OSs with text ratings for Use Case, Stability, and Difficulty.
    Text ratings represent the color requested: Easy (Green), Moderate (Yellow), Difficult (Red).
    """
    
    os_data = [
        
        ("Windows 11", "FOR PLAY / WORK", "MODERATE", "EASY"), 
        ("Windows 10", "FOR PLAY / WORK", "EASY", "EASY"),
        ("macOS Sonoma", "FOR PLAY / WORK / CREATION", "EASY", "EASY"), 
        
        
        ("Ubuntu Desktop", "FOR WORK / ALL-AROUND", "EASY", "EASY"),
        ("Debian", "FOR SERVER / STABILITY", "EASY", "MODERATE"), 
        ("Fedora Workstation", "FOR DEVELOPMENT / MODERN", "MODERATE", "MODERATE"),
        ("Linux Mint", "FOR BEGINNERS / PLAY", "EASY", "EASY"),
        ("Pop!_OS", "FOR PLAY / DEVELOPMENT", "MODERATE", "MODERATE"),
        ("Zorin OS", "FOR BEGINNERS / LOOKS", "EASY", "EASY"),
        
        
        ("Arch Linux", "FOR CUSTOMIZATION / ADVANCED", "DIFFICULT", "DIFFICULT"), 
        ("Kali Linux", "FOR SECURITY / PENTESTING", "MODERATE", "MODERATE"), 
        ("Manjaro Linux", "FOR ARCH EASE / PLAY", "MODERATE", "MODERATE"),
        ("CentOS Stream", "FOR SERVER / DEVELOPMENT", "MODERATE", "MODERATE"),
        ("openSUSE Tumbleweed", "FOR CUTTING-EDGE / DEV", "MODERATE", "MODERATE"),
        ("Elementary OS", "FOR LOOKS / SIMPLE", "MODERATE", "EASY"),
        ("Deepin", "FOR AESTHETICS / WORK", "MODERATE", "MODERATE"),
        ("Alpine Linux", "FOR CONTAINERS / SMALL", "EASY", "DIFFICULT"), 
        ("Raspbian (Pi OS)", "FOR DIY / EMBEDDED", "EASY", "MODERATE"),
        ("Tails", "FOR ANONYMITY / SECURITY", "MODERATE", "MODERATE"), 
        ("Parrot OS", "FOR SECURITY / PENTESTING", "MODERATE", "MODERATE"), 
        ("Devuan", "FOR INIT FREEDOM / STABILITY", "EASY", "MODERATE"),
        ("Red Hat Enterprise Linux", "FOR BUSINESS / SERVER", "EASY", "MODERATE"),
        
        
        ("pfSense", "FOR FIREWALL / ROUTING", "EASY", "DIFFICULT"), 
        ("Proxmox VE", "FOR VIRTUALIZATION / SERVER", "EASY", "DIFFICULT"), 
        ("ESXi (VMware)", "FOR VIRTUALIZATION / SERVER", "EASY", "DIFFICULT"), 
        ("FreeBSD", "FOR SERVER / STABILITY", "EASY", "DIFFICULT"), 
        ("OpenBSD", "FOR SECURITY / MINIMALISM", "EASY", "DIFFICULT"), 
        ("Haiku OS", "FOR DEVELOPMENT / LEGACY", "DIFFICULT", "MODERATE"),
        ("Solaris (Oracle)", "FOR ENTERPRISE / LEGACY", "EASY", "DIFFICULT"), 
        ("ReactOS", "FOR DEVELOPMENT / WINDOWS COMPAT", "DIFFICULT", "DIFFICULT"),
    ]

    
    headers = ["ID", "OPERATING SYSTEM", "MAIN USE CASE", "STABILITY", "DIFFICULTY"]
    
    
    table_data = []
    for i, (name, use, stab, diff) in enumerate(os_data, 1):
        
        number_str = f"{i:02d}" 
        table_data.append([number_str, name, use, stab, diff])

    
    print("\n" + "=" * 80)
    print("CLASSIFIED OPERATING SYSTEM LIST")
    print("Stability/Difficulty Ratings: EASY (Green) | MODERATE (Yellow) | DIFFICULT (Red)")
    print("=" * 80)
    
    
    print(tabulate(table_data, headers=headers, tablefmt="grid"))
    
    print("\n--- Official Download Information ---")
    
    
    id_to_os = {f"{i:02d}": name for i, (name, _, _, _) in enumerate(os_data, 1)}
    
    return id_to_os

def retrieve_os_info_no_links(id_to_os):
    """
    Asks the user to choose an OS by ID and advises them to search for the official link.
    """

    max_id = len(id_to_os)
    choice_id = input(f"Enter the ID (01 to {max_id:02d}) of the OS to get download advice: ").strip()

    if choice_id in id_to_os:
        os_name = id_to_os[choice_id]

        print("\n--- Official Download Advice ---")
        print(f"You selected: {os_name.upper()}")
        print("To download this operating system,")
        print("you must visit the  website of the vendor (e.g., Microsoft.com, ubuntu.com, archlinux.org).")
        print(f"Please manually search for the download link for '{os_name}'.")
        print("\nThis ensures you get the latest file.")
        print("-" * 50)
        
    else:
        print(f"Error: The ID '{choice_id}' is not valid. Please enter a number between 01 and {max_id:02d}.")


if __name__ == "__main__":
    
    try:
        os_mapping = display_os_ratings_text()
        retrieve_os_info_no_links(os_mapping)
    except ImportError:
        print("\nERROR: The 'tabulate' library is required to display the table properly.")
        print("Please install it by running: pip install tabulate")