import requests
import os
import time


   
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

def display_os_list(official_links):
    """
    Displays the list of OSs categorized and numbered.
    """
    
    categories = {
        "Microsoft and Apple": [
            ("windows 11", official_links["windows 11"]),
            ("windows 10", official_links["windows 10"]),
            ("macos sonoma", official_links["macos sonoma"]),
        ],
        "Mainstream Linux Distributions": [
            ("ubuntu desktop", official_links["ubuntu desktop"]),
            ("debian", official_links["debian"]),
            ("fedora workstation", official_links["fedora workstation"]),
            ("mint linux", official_links["mint linux"]),
            ("pop os", official_links["pop os"]),
            ("zorin os", official_links["zorin os"]),
        ],
        "Advanced and Specialized Linux": [
            ("arch linux", official_links["arch linux"]),
            ("kali linux", official_links["kali linux"]),
            ("manjaro linux", official_links["manjaro linux"]),
            ("centos stream", official_links["centos stream"]),
            ("opensuse tumbleweed", official_links["opensuse tumbleweed"]),
            ("elementary os", official_links["elementary os"]),
            ("deepin", official_links["deepin"]),
            ("alpine linux", official_links["alpine linux"]),
            ("raspbian (rasberry pi os)", official_links["raspbian (rasberry pi os)"]),
            ("tails", official_links["tails"]),
            ("parrot os", official_links["parrot os"]),
            ("devuan", official_links["devuan"]),
            ("red hat enterprise linux", official_links["red hat enterprise linux"]),
        ],
        "Server, BSD, and Other OSs": [
            ("pfsense", official_links["pfsense"]),
            ("proxmox ve", official_links["proxmox ve"]),
            ("esxi (vmware)", official_links["esxi (vmware)"]),
            ("freebsd", official_links["freebsd"]),
            ("openbsd", official_links["openbsd"]),
            ("haiku os", official_links["haiku os"]),
            ("solaris (oracle)", official_links["solaris (oracle)"]),
            ("reactos", official_links["reactos"]),
        ]
    }

    
    numbered_list = {}
    counter = 1
    
    print("---  Official OS Download List ---")
    
    for category, os_list in categories.items():
        print(f"\n## {category.upper()}")
        for os_name, url in os_list:
            
            number_str = f"{counter:02d}" 
            print(f"{number_str}. {os_name.title()}")
            numbered_list[number_str] = {"name": os_name, "url": url}
            counter += 1
            
    print("\n" + "-" * 50)
    return numbered_list

def download_iso_guide_structured():
    """
    Displays the structured OS list and allows the user to select one by number.
    """
    
    official_links = {
        "windows 11": "https://www.microsoft.com/en-us/software-download/windows11",
        "windows 10": "https://www.microsoft.com/en-us/software-download/windows10",
        "macos sonoma": "https://www.apple.com/macos/sonoma/", 
        "ubuntu desktop": "https://ubuntu.com/download/desktop",
        "debian": "https://www.debian.org/distrib/",
        "fedora workstation": "https://getfedora.org/en/workstation/download/",
        "mint linux": "https://linuxmint.com/download.php",
        "kali linux": "https://www.kali.org/get-kali/",
        "arch linux": "https://archlinux.org/download/",
        "centos stream": "https://www.centos.org/centos-stream/",
        "opensuse tumbleweed": "https://get.opensuse.org/tumbleweed/",
        "elementary os": "https://elementary.io/en/get-elementary",
        "pop os": "https://pop.system76.com/",
        "zorin os": "https://zorin.com/os/download/",
        "red hat enterprise linux": "https://www.redhat.com/en/technologies/linux-platforms/enterprise-linux",
        "manjaro linux": "https://manjaro.org/download/",
        "deepin": "https://www.deepin.org/en/download/",
        "freebsd": "https://www.freebsd.org/where-to-get/",
        "openbsd": "https://www.openbsd.org/faq/faq4.html#Download",
        "haiku os": "https://www.haiku-os.org/get-haiku/",
        "raspbian (rasberry pi os)": "https://www.raspberrypi.com/software/operating-systems/",
        "solaris (oracle)": "https://www.oracle.com/solaris/technologies/solaris-downloads.html",
        "alpine linux": "https://www.alpinelinux.org/downloads/",
        "pfsense": "https://www.pfsense.org/download/",
        "proxmox ve": "https://www.proxmox.com/en/downloads/category/iso-images-ve",
        "esxi (vmware)": "https://customerconnect.vmware.com/en/downloads/info/slug/datacenter_cloud_infrastructure/vmware_vsphere/8_0",
        "reactos": "https://www.reactos.org/download/",
        "tails": "https://tails.boum.org/install/index.en.html",
        "devuan": "https://www.devuan.org/os/download",
        "parrot os": "https://www.parrotsec.org/download/"
    }
    
    
    numbered_list = display_os_list(official_links)
    
    
    choice_number = input(f"Enter the number (01 to {len(numbered_list):02d}) of the OS you wish to download: ").strip()

    if choice_number in numbered_list:
        selected_os = numbered_list[choice_number]
        os_name = selected_os["name"]
        official_url = selected_os["url"]
        
        print("\n--- Official Download Link ---")
        print(f"You selected: {os_name.upper()}")
        print(f"The official URL to download this OS is:")
        print(f"{official_url}")
        print("\nReminder: Always use the official source for safety and compliance.")
        print("-" * 50)
        
    else:
        print(f"Error: The number '{choice_number}' is not valid. Please enter a number between 01 and {len(numbered_list):02d}.")


if __name__ == "__main__":
    download_iso_guide_structured()