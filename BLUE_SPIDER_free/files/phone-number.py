# (c) 2026 IxilaA1 - Tous droits réservés / All rights reserved / Todos los derechos reservados.
# Ce code ne peut être ni vendu, ni modifié, ni partagé sans autorisation, ni publié à votre nom.
# This code may not be sold, modified, or shared without authorization, nor published under your name.
# Este código no puede ser vendido, modificado ni compartido sin autorización, ni publicado a su nombre.
# -------------------------------------------------------------------------------------------------------
import requests
from bs4 import BeautifulSoup
import re
import webbrowser
import os
import sys
import subprocess
from colorama import init, Fore, Back, Style
from urllib.parse import urlparse
import time
from pystyle import Colors, Colorate, Write, Center, Box
import phonenumbers
from phonenumbers import carrier, geocoder
import json

init(autoreset=True)

WEB_API_URL = "https://htmlweb.ru/geo/api.php?json&telcod="

def install_libraries():
    """Install required libraries if missing"""
    libraries = ['requests', 'bs4', 'colorama', 'urllib3', 'pystyle', 'phonenumbers']
    for lib in libraries:
        try:
            __import__(lib)
        except ImportError:
            print(f"{Fore.CYAN}Installing {lib}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", lib])

def get_web_data(phone_number):
    """Gets additional data about the number from external API"""
    try:
        clean_number = phone_number.replace("+", "").replace("-", "").replace(" ", "")

        response = requests.get(
            f"{WEB_API_URL}{clean_number}",
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            },
            timeout=10
        )

        if response.status_code == 200:
            return response.json()
        return {}
    except Exception as e:
        print(f"Error fetching web data: {e}")
        return {}

class PhoneAnalyzer:
    def __init__(self, phone_number):
        self.phone_number = phone_number
        self.results = {
            "basic_info": {},
            "web_info": {}
        }
        self.parsed_number = None

    def validate_and_parse(self):
        """Validation and basic number analysis"""
        try:
            cleaned_number = re.sub(r'[^\d+]', '', self.phone_number)

            
            if cleaned_number.startswith('0') and len(cleaned_number) == 10:
                cleaned_number = '+33' + cleaned_number[1:]
            
            elif cleaned_number.startswith('8') and len(cleaned_number) == 11:
                cleaned_number = '+7' + cleaned_number[1:]

            self.parsed_number = phonenumbers.parse(cleaned_number, None)

            if not phonenumbers.is_valid_number(self.parsed_number):
                return False

            country = geocoder.description_for_number(self.parsed_number, "en")
            operator = carrier.name_for_number(self.parsed_number, "en")

            self.results["basic_info"] = {
                "is_valid": True,
                "country": country if country else "Unknown",
                "operator": operator if operator else "Unknown",
                "national_format": phonenumbers.format_number(
                    self.parsed_number, phonenumbers.PhoneNumberFormat.NATIONAL
                ),
                "international_format": phonenumbers.format_number(
                    self.parsed_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL
                ),
                "e164_format": phonenumbers.format_number(
                    self.parsed_number, phonenumbers.PhoneNumberFormat.E164
                )
            }
            return True
        except phonenumbers.NumberParseException as e:
            print(f"Error parsing number: {e}")
            return False
        except Exception as e:
            print(f"Unexpected error: {e}")
            return False

    def check_web_info(self):
        """Gets additional information from external API and translates to English"""
        try:
            web_data = get_web_data(self.phone_number)
            if web_data:
                
                region_name = web_data.get("region", {}).get("name", "Unknown")
                country_name = web_data.get("country", {}).get("name", "Unknown")
                capital_name = web_data.get("capital", {}).get("name", "Unknown")
                
                
                translations = {
                    "Москва": "Moscow",
                    "Санкт-Петербург": "Saint Petersburg",
                    "Париж": "Paris",
                    "Франция": "France",
                    "Россия": "Russia",
                    "Лондон": "London",
                    "Берлин": "Berlin",
                    "Мадрид": "Madrid",
                    "Рим": "Rome",
                    "Амстердам": "Amsterdam",
                    "Брюссель": "Brussels"
                }
                
                self.results["web_info"] = {
                    "postal": web_data.get("0", {}).get("post", "Unknown"),
                    "region": translations.get(region_name, region_name),
                    "autocod": web_data.get("region", {}).get("autocod", "Unknown"),
                    "operator": web_data.get("0", {}).get("oper", "Unknown"),
                    "brand": web_data.get("0", {}).get("oper_brand", "Unknown"),
                    "latitude": web_data.get("0", {}).get("latitude", "Unknown"),
                    "longitude": web_data.get("0", {}).get("longitude", "Unknown"),
                    "capital": translations.get(capital_name, capital_name),
                    "country": translations.get(country_name, country_name)
                }
                return True
        except Exception as e:
            print(f"Error checking web info: {e}")
        return False

    def run_analysis(self):
        """Runs complete analysis"""
        if not self.validate_and_parse():
            return False

        self.check_web_info()
        return True

def display_phone_results(results):
    """Displays analysis results in console with blue/white theme"""
    basic = results["basic_info"]
    web_info = results.get("web_info", {})

    if not basic:
        Write.Print("\n" + "═" * 60 + "\n", Colors.blue_to_cyan, interval=0.01)
        Write.Print("❌ INVALID PHONE NUMBER\n", Colors.red_to_blue, interval=0.01)
        Write.Print("═" * 60 + "\n", Colors.blue_to_cyan, interval=0.01)
        return

    Write.Print("\n" + "═" * 60 + "\n", Colors.blue_to_cyan, interval=0.01)
    Write.Print("📱 PHONE NUMBER ANALYSIS\n", Colors.blue_to_cyan, interval=0.01)
    Write.Print("═" * 60 + "\n", Colors.blue_to_cyan, interval=0.01)
    
    Write.Print("BASIC INFORMATION:\n", Colors.cyan_to_blue, interval=0.01)
    print(Colorate.Horizontal(Colors.blue_to_cyan, f"• Number: {basic.get('international_format', 'N/A')}", 1))
    print(Colorate.Horizontal(Colors.blue_to_cyan, f"• Local format: {basic.get('national_format', 'N/A')}", 1))
    print(Colorate.Horizontal(Colors.blue_to_cyan, f"• Country: {basic.get('country', 'N/A')}", 1))
    print(Colorate.Horizontal(Colors.blue_to_cyan, f"• Carrier: {basic.get('operator', 'N/A')}", 1))
    print(Colorate.Horizontal(Colors.blue_to_cyan, f"• Valid: {'Yes' if basic.get('is_valid') else 'No'}", 1))

    if web_info:
        Write.Print("\nDETAILED INFORMATION (htmlweb.ru):\n", Colors.cyan_to_blue, interval=0.01)
        
        if web_info.get('region') != "Unknown":
            print(Colorate.Horizontal(Colors.blue_to_cyan, f"• Region: {web_info['region']}", 1))
        
        if web_info.get('postal') != "Unknown":
            print(Colorate.Horizontal(Colors.blue_to_cyan, f"• Postal code: {web_info['postal']}", 1))
        
        if web_info.get('autocod') != "Unknown":
            print(Colorate.Horizontal(Colors.blue_to_cyan, f"• Region code: {web_info['autocod']}", 1))
        
        if web_info.get('operator') != "Unknown":
            print(Colorate.Horizontal(Colors.blue_to_cyan, f"• Operator: {web_info['operator']}", 1))
        
        if web_info.get('brand') != "Unknown":
            print(Colorate.Horizontal(Colors.blue_to_cyan, f"• Brand: {web_info['brand']}", 1))
        
        if web_info.get('latitude') != "Unknown" and web_info.get('longitude') != "Unknown":
            print(Colorate.Horizontal(Colors.blue_to_cyan, f"• Coordinates: {web_info['latitude']}, {web_info['longitude']}", 1))
            maps_url = f"https://www.google.com/maps?q={web_info['latitude']},{web_info['longitude']}"
            print(Colorate.Horizontal(Colors.cyan_to_blue, f"• Maps link: {maps_url}", 1))
        
        if web_info.get('capital') != "Unknown":
            print(Colorate.Horizontal(Colors.blue_to_cyan, f"• Capital: {web_info['capital']}", 1))
        
        if web_info.get('country') != "Unknown":
            print(Colorate.Horizontal(Colors.blue_to_cyan, f"• Country: {web_info['country']}", 1))

    Write.Print("\nUSEFUL LINKS:\n", Colors.cyan_to_blue, interval=0.01)
    e164_clean = basic.get('e164_format', '').replace('+', '')
    if e164_clean:
        print(Colorate.Horizontal(Colors.blue_to_cyan, f"• WhatsApp: https://wa.me/{e164_clean}", 1))
        print(Colorate.Horizontal(Colors.blue_to_cyan, f"• Viber: https://viber.click/{e164_clean}", 1))
        print(Colorate.Horizontal(Colors.blue_to_cyan, f"• Telegram: https://t.me/{e164_clean}", 1))
    
    Write.Print("\n" + "═" * 60 + "\n", Colors.blue_to_cyan, interval=0.01)

def search_phone_number(phone_number):
    """Searches for phone number on Google with better headers and delay"""
    url = f"https://www.google.com/search?q={phone_number}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Cache-Control": "max-age=0",
        "Referer": "https://www.google.com/",
    }
    
    try:
        
        Write.Print("⏳ Waiting 2 seconds to avoid rate limiting...\n", Colors.cyan_to_blue, interval=0.01)
        time.sleep(2)
        
        
        session = requests.Session()
        
        
        session.get("https://www.google.com", headers=headers, timeout=10)
        
        
        response = session.get(url, headers=headers, timeout=15)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            
            search_results = []
            
            
            for link in soup.find_all('a', href=True):
                href = link.get('href', '')
                if '/url?q=' in href:
                    
                    match = re.search(r'/url\?q=(https?://[^&]+)', href)
                    if match:
                        url_link = match.group(1)
                        
                        url_link = re.sub(r'%([0-9A-Fa-f]{2})', lambda m: chr(int(m.group(1), 16)), url_link)
                        parsed_url = urlparse(url_link)
                        
                        excluded_domains = ['google.com', 'yandex.ru', 'bing.com', 'maps.google.com', 
                                          'support.google.com', 'accounts.google.com', 'webcache.googleusercontent.com']
                        if not any(domain in parsed_url.netloc for domain in excluded_domains):
                            if url_link not in search_results:
                                search_results.append(url_link)
            
            
            if not search_results:
                excluded_domains = ['google.com', 'yandex.ru', 'bing.com', 'maps.google.com']
                for link in soup.find_all('a', href=True):
                    href = link.get('href', '')
                    if href.startswith('http') and not any(domain in href for domain in excluded_domains):
                        if href not in search_results:
                            search_results.append(href)
            
            
            unique_links = list(set(search_results))
            
            if unique_links:
                Write.Print(f"✅ Found {len(unique_links)} links!\n", Colors.green_to_blue, interval=0.01)
                return unique_links
            else:
                Write.Print(f"⚠️ No links found in search results\n", Colors.cyan_to_blue, interval=0.01)
                Write.Print(f"💡 Try searching manually: {url}\n", Colors.blue_to_cyan, interval=0.01)
                return []
        else:
            error_msg = f"Google returned status code: {response.status_code}"
            Write.Print(f"❌ {error_msg}\n", Colors.red_to_blue, interval=0.01)
            Write.Print(f"💡 Try searching manually: {url}\n", Colors.blue_to_cyan, interval=0.01)
            return []
            
    except requests.RequestException as e:
        error_msg = f"Error during request: {str(e)}"
        Write.Print(f"❌ {error_msg}\n", Colors.red_to_blue, interval=0.01)
        Write.Print(f"💡 Try searching manually: {url}\n", Colors.blue_to_cyan, interval=0.01)
        return []

def save_links_to_html(links, phone_number, analysis_results, filename="search_results.html"):
    """Saves search results to HTML file with permission error handling"""
    
    
    possible_paths = []
    
    
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        if script_dir and os.access(script_dir, os.W_OK):
            possible_paths.append(os.path.join(script_dir, filename))
    except:
        pass
    
    
    try:
        desktop = os.path.join(os.path.expanduser("~"), "Desktop")
        if os.path.exists(desktop) and os.access(desktop, os.W_OK):
            possible_paths.append(os.path.join(desktop, filename))
    except:
        pass
    
  
    try:
        documents = os.path.join(os.path.expanduser("~"), "Documents")
        if os.path.exists(documents) and os.access(documents, os.W_OK):
            possible_paths.append(os.path.join(documents, filename))
    except:
        pass
    
    
    try:
        home = os.path.expanduser("~")
        if os.access(home, os.W_OK):
            possible_paths.append(os.path.join(home, filename))
    except:
        pass
    
    
    try:
        if os.access(".", os.W_OK):
            possible_paths.append(filename)
        else:
            
            temp_filename = f"temp_{int(time.time())}_{filename}"
            if os.access(".", os.W_OK):
                possible_paths.append(temp_filename)
    except:
        pass
    
    
    try:
        temp_dir = os.environ.get('TEMP', os.environ.get('TMP', '/tmp'))
        if os.path.exists(temp_dir) and os.access(temp_dir, os.W_OK):
            possible_paths.append(os.path.join(temp_dir, filename))
    except:
        pass
    
    
    safe_filename = None
    for path in possible_paths:
        try:
            
            test_file = os.path.join(os.path.dirname(path), ".test_write")
            with open(test_file, 'w') as f:
                f.write("test")
            os.remove(test_file)
            safe_filename = path
            break
        except:
            continue
    
    if not safe_filename:
        
        safe_filename = filename
        Write.Print(f"⚠️ Warning: Could not find writable directory, trying current directory...\n", Colors.yellow_to_blue, interval=0.01)
    
    css_styles = """
        <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { 
            font-family: 'Segoe UI', Tahoma, sans-serif; 
            background: linear-gradient(135deg, #0a2b3e 0%, #0a1a2a 100%);
            color: #ffffff;
            min-height: 100vh;
        }
        .container { 
            max-width: 900px; 
            margin: 0 auto; 
            padding: 40px 20px;
        }
        h1 { 
            text-align: center; 
            margin-bottom: 30px; 
            font-size: 2.5em; 
            color: #4ec0e9;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
        }
        .phone-info {
            text-align: center;
            margin-bottom: 30px;
            padding: 20px;
            background: rgba(78, 192, 233, 0.1);
            border-radius: 8px;
            border: 1px solid #4ec0e9;
        }
        .analysis-section {
            margin-bottom: 30px;
            padding: 20px;
            background: rgba(78, 192, 233, 0.05);
            border-radius: 8px;
            border: 1px solid #4ec0e9;
        }
        .analysis-section h3 {
            color: #4ec0e9;
            margin-bottom: 15px;
        }
        .analysis-item {
            margin-bottom: 8px;
            padding: 5px 0;
            color: #ffffff;
        }
        .stats {
            text-align: center;
            margin-bottom: 20px;
            font-size: 1.1em;
            color: #b0e0ff;
        }
        .link-list { 
            list-style-type: none; 
        }
        .link-item { 
            margin-bottom: 15px; 
            padding: 20px; 
            background: rgba(78, 192, 233, 0.1);
            border: 1px solid #4ec0e9;
            border-radius: 8px;
            transition: all 0.3s ease;
        }
        .link-item:hover { 
            transform: translateY(-3px);
            background: rgba(78, 192, 233, 0.2);
            box-shadow: 0 5px 15px rgba(78, 192, 233, 0.3);
        }
        .link-item a { 
            display: block; 
            color: #4ec0e9; 
            text-decoration: none; 
            font-size: 1.1em;
            font-weight: 500;
            transition: color 0.3s ease;
        }
        .link-item a:hover { 
            color: #7ec8e0; 
        }
        .domain {
            font-size: 0.9em;
            color: #b0e0ff;
            margin-top: 5px;
        }
        .timestamp {
            text-align: center;
            margin-top: 30px;
            color: #4ec0e9;
            font-style: italic;
        }
        </style>
    """

    analysis_html = ""
    if analysis_results and "basic_info" in analysis_results and analysis_results["basic_info"]:
        basic = analysis_results["basic_info"]
        web_info = analysis_results.get("web_info", {})
        
        analysis_html = f"""
        <div class="analysis-section">
            <h3>📱 Phone Number Analysis</h3>
            <div class="analysis-item"><strong>Number:</strong> {basic.get('international_format', 'N/A')}</div>
            <div class="analysis-item"><strong>Country:</strong> {basic.get('country', 'N/A')}</div>
            <div class="analysis-item"><strong>Carrier:</strong> {basic.get('operator', 'N/A')}</div>
            <div class="analysis-item"><strong>Valid:</strong> {'Yes' if basic.get('is_valid') else 'No'}</div>
        """
        
        if web_info:
            if web_info.get('region') != "Unknown":
                analysis_html += f'<div class="analysis-item"><strong>Region:</strong> {web_info["region"]}</div>'
            
            if web_info.get('postal') != "Unknown":
                analysis_html += f'<div class="analysis-item"><strong>Postal code:</strong> {web_info["postal"]}</div>'
            
            if web_info.get('autocod') != "Unknown":
                analysis_html += f'<div class="analysis-item"><strong>Region code:</strong> {web_info["autocod"]}</div>'
            
            if web_info.get('operator') != "Unknown":
                analysis_html += f'<div class="analysis-item"><strong>Operator (API):</strong> {web_info["operator"]}</div>'
            
            if web_info.get('brand') != "Unknown":
                analysis_html += f'<div class="analysis-item"><strong>Brand:</strong> {web_info["brand"]}</div>'
            
            if web_info.get('latitude') != "Unknown" and web_info.get('longitude') != "Unknown":
                analysis_html += f'<div class="analysis-item"><strong>Coordinates:</strong> {web_info["latitude"]}, {web_info["longitude"]}</div>'
                maps_url = f"https://www.google.com/maps?q={web_info['latitude']},{web_info['longitude']}"
                analysis_html += f'<div class="analysis-item"><strong>Maps:</strong> <a href="{maps_url}" target="_blank">{maps_url}</a></div>'
            
            if web_info.get('capital') != "Unknown":
                analysis_html += f'<div class="analysis-item"><strong>Capital:</strong> {web_info["capital"]}</div>'
        
        analysis_html += "</div>"

    if links:
        links_html = ''.join([
            f'<li class="link-item"><a href="{link}" target="_blank">{link}</a>'
            f'<div class="domain">Domain: {urlparse(link).netloc}</div></li>'
            for link in links
        ])
    else:
        links_html = '<div class="stats">No links found in search results. Try searching manually on Google.</div>'
    
    html_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Phone Number Search Results</title>
    {}
</head>
<body>
    <div class="container">
        <h1>🔍 Search Results</h1>
        <div class="phone-info">
            <h3>Number Analysis: {}</h3>
        </div>
        {}
        <div class="stats">Links found: {}</div>
        <ul class="link-list">
            {}
        </ul>
        <div class="timestamp">Report created: {}</div>
    </div>
</body>
</html>"""
    
    html_content = html_template.format(
        css_styles, 
        phone_number,
        analysis_html,
        len(links) if links else 0, 
        links_html,
        time.strftime("%Y-%m-%d %H:%M:%S")
    )
    
    try:
        with open(safe_filename, "w", encoding="utf-8") as f:
            f.write(html_content)
        Write.Print(f"✅ Results saved to {safe_filename}\n", Colors.green_to_blue, interval=0.01)
        return safe_filename
    except PermissionError as e:
        Write.Print(f"❌ Permission denied: Cannot write to {safe_filename}\n", Colors.red_to_blue, interval=0.01)
        Write.Print(f"💡 Try running the script as administrator or save to a different location\n", Colors.blue_to_cyan, interval=0.01)
        
        
        try:
            import tempfile
            temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8')
            temp_file.write(html_content)
            temp_file.close()
            Write.Print(f"✅ Results saved to temporary file: {temp_file.name}\n", Colors.green_to_blue, interval=0.01)
            return temp_file.name
        except:
            Write.Print(f"❌ Could not save file at all. Please check your permissions.\n", Colors.red_to_blue, interval=0.01)
            return None
    except Exception as e:
        Write.Print(f"❌ Error saving HTML file: {e}\n", Colors.red_to_blue, interval=0.01)
        return None

def clear_console():
    """Clears the console"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    """Prints the program banner"""
    banner = r"""
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
    
    print(Colorate.Horizontal(Colors.blue_to_cyan, banner, 1))
    print()

def print_links_to_console(links):
    """Prints search results to console"""
    if not links:
        Write.Print("❌ No links found\n", Colors.red_to_blue, interval=0.01)
        return
        
    Write.Print(f"\n🌐 Found {len(links)} unique links:\n", Colors.blue_to_cyan, interval=0.01)
    
    for i, link in enumerate(links, 1):
        domain = urlparse(link).netloc
        link_text = f"{i:2d}. {link}"
        domain_text = f"    Domain: {domain}"
        
        print(Colorate.Horizontal(Colors.blue_to_cyan, link_text, 1))
        print(Colorate.Horizontal(Colors.cyan_to_blue, domain_text, 1))
        print(Colorate.Horizontal(Colors.blue_to_cyan, "    " + "─" * 40, 1))

def open_html_report(filename):
    """Opens HTML report in browser"""
    if filename and os.path.exists(filename):
        try:
            webbrowser.open(f'file://{os.path.abspath(filename)}')
            Write.Print("✅ Report opened in browser\n", Colors.green_to_blue, interval=0.01)
        except Exception as e:
            Write.Print(f"❌ Error opening report: {e}\n", Colors.red_to_blue, interval=0.01)
    else:
        Write.Print("❌ Report file not found\n", Colors.red_to_blue, interval=0.01)

def main():
    """Main function"""
    install_libraries()
    
    while True:
        try:
            clear_console()
            print_banner()
            
            phone_number = Write.Input("📞 Enter phone number (e.g., +33612345678 or 0612345678): ", Colors.blue_to_cyan, interval=0.005, hide_cursor=False)
            
            if not phone_number:
                Write.Print("❌ Please enter a phone number\n", Colors.red_to_blue, interval=0.01)
                time.sleep(1)
                continue
            
            Write.Print("\n🔍 Analyzing number...\n", Colors.cyan_to_blue, interval=0.01)
            
            analyzer = PhoneAnalyzer(phone_number)
            if analyzer.run_analysis():
                display_phone_results(analyzer.results)
                analysis_results = analyzer.results
            else:
                Write.Print("❌ Invalid phone number\n", Colors.red_to_blue, interval=0.01)
                analysis_results = {"basic_info": {}, "web_info": {}}
                
            Write.Print("\n🔎 Searching for links on Google...\n", Colors.cyan_to_blue, interval=0.01)
            search_results = search_phone_number(phone_number)
            
            saved_filename = None
            
            if isinstance(search_results, list):
                if search_results:
                    print_links_to_console(search_results)
                saved_filename = save_links_to_html(search_results, phone_number, analysis_results)
                if saved_filename:
                    open_report = Write.Input("Open report in browser? (y/n): ", Colors.blue_to_cyan, interval=0.005, hide_cursor=False).lower()
                    if open_report == 'y':
                        open_html_report(saved_filename)
                else:
                    Write.Print("❌ Error saving report\n", Colors.red_to_blue, interval=0.01)
            else:
                Write.Print(f"❌ {search_results}\n", Colors.red_to_blue, interval=0.01)
            
            Write.Input("\nPress Enter to continue...", Colors.blue_to_cyan, interval=0.005, hide_cursor=False)
            
        except KeyboardInterrupt:
            Write.Print("\n\n👋 Program terminated\n", Colors.red_to_blue, interval=0.01)
            break
        except Exception as e:
            Write.Print(f"\n❌ An error occurred: {e}\n", Colors.red_to_blue, interval=0.01)
            Write.Input("\nPress Enter to continue...", Colors.blue_to_cyan, interval=0.005, hide_cursor=False)

if __name__ == "__main__":
    main()