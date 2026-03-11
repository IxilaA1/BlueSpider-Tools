import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re
import time
import random
import sys
import os

   
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




def get_current_time_log():
    return f"[{time.strftime('%H:%M:%S')}]"


LOG_INFO = "[INFO]"
LOG_INPUT = "[INPUT]"
LOG_ADD = "[FOUND]"


def display_title(text):
    print(f"\n{'='*50}")
    print(f"** {text} **")
    print(f"{'='*50}\n")

def get_user_agent():
    
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36"
    ]
    return random.choice(user_agents)

def handle_error(e):
    print(f"\n[ERROR] An error occurred: {e}", file=sys.stderr)


display_title("Website URL Scanner")

try:
    all_links = set()
    
    user_agent = get_user_agent()
    headers = {"User-Agent": user_agent}

    def is_valid_extension(url):

        return re.search(r'\.(html|xhtml|php|js|css)$', url, re.IGNORECASE) or not re.search(r'\.\w+$', url)

    def extract_links(base_url, domain, tags):
        
        extracted_links = []
        for tag in tags:
            
            attr = tag.get('href') or tag.get('src') or tag.get('action')
            if attr:
                full_url = urljoin(base_url, attr)
                
                if full_url not in all_links and domain in full_url and is_valid_extension(full_url):
                    extracted_links.append(full_url)
                    all_links.add(full_url)
        return extracted_links

    def extract_links_from_script(scripts, domain):
        
        extracted_links = []
        for script in scripts:
           
            content = script.string or script.text
            if content:
                
                urls_in_script = re.findall(r'(https?://\S+)', content)
                for url in urls_in_script:
                    
                    if url not in all_links and domain in url and is_valid_extension(url):
                        extracted_links.append(url)
                        all_links.add(url)
        return extracted_links

    def find_urls(website_url, domain):
        
        try:
            
            response = requests.get(website_url, headers=headers, timeout=10)
        except requests.exceptions.RequestException as e:
           
            print(f"{get_current_time_log()} [WARNING] Could not access {website_url}: {e}")
            return

        if response.status_code != 200:
            return
        
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        
        tags = soup.find_all(['a', 'link', 'script', 'img', 'iframe', 'button', 'form'])
        
        extracted_links = extract_links(website_url, domain, tags)
        
        
        extracted_links.extend(extract_links_from_script(soup.find_all('script'), domain))
        
        for link in extracted_links:
            
            print(f"{get_current_time_log()} {LOG_ADD} URL: {link}")

    def crawl_website(website_url, domain):
        
        
        
        find_urls(website_url, domain)
        
        visited_links = {website_url}
        
        
        queue = list(all_links)
        
        while queue:
            
            link = queue.pop(0)
            
            
            if link in visited_links:
                continue

            
            visited_links.add(link)

            try:

                response = requests.head(link, headers=headers, timeout=5, allow_redirects=True)
                
                if response.status_code == 200:
                    
                    print(f"\n{get_current_time_log()} {LOG_INFO} Scanning new page: {link}")
                    
                    
                    find_urls(link, domain)

                    
                    newly_found = all_links - visited_links
                    queue.extend(list(newly_found))
                    
                else:
                    print(f"{get_current_time_log()} [SKIP] Cannot scan {link}. Status: {response.status_code}")

            except requests.exceptions.RequestException as e:
                
                pass


    
    print(f"{get_current_time_log()} {LOG_INFO} Selected User-Agent: {user_agent}")
    
    website_url = input(f"{get_current_time_log()} {LOG_INPUT} Website URL -> ")
    
    
    
    if not website_url.startswith(("https://", "http://")):
        website_url = "https://" + website_url
        

    domain = re.sub(r'^https?://', '', website_url).split('/')[0]
    
    print(f"""
{get_current_time_log()} 01 Only URL
{get_current_time_log()} 02 All Website
    """)
    
    choice = input(f"{get_current_time_log()} {LOG_INPUT} Choice -> ")
    
    if choice in ['1', '01']:
        
        find_urls(website_url, domain)
    elif choice in ['2', '02']:
       
        crawl_website(website_url, domain)
        

    
except Exception as e:
    handle_error(e)