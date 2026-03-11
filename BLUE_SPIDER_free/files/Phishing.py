import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re
import os
import concurrent.futures

try:
    
    def ErrorModule(e):
        print(f"Error: {e}")

    def Title(text):
        print(f"=== {text} ===")

    def ChoiceUserAgent():
        import random
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
            "Mozilla/5.0 (X11; Linux x86_64)"
        ]
        return random.choice(user_agents)

    def Slow(text):
        print(f"[SLOW] {text}")

    def Censored(text):
        print(f"[CENSORED] {text}")

    def Continue():
        input("Press Enter to continue...")

    def Reset():
        print("Resetting...")

    def ErrorUrl():
        print("Invalid or unreachable URL.")

    def Error(e):
        print(f"Error: {e}")

    def current_time_hour():
        from datetime import datetime
        return datetime.now().strftime("%H:%M:%S")

    
    BEFORE = ""
    AFTER = ""
    INFO = "[INFO]"
    WAIT = "[WAIT]"
    ERROR = "[ERROR]"
    red = "\033[91m"
    white = "\033[97m"
    reset = "\033[0m"

    
    INPUT = "[INPUT]"

    
    Title("Phishing Attack")

    
    user_agent = ChoiceUserAgent()
    headers = {"User-Agent": user_agent}

    Slow("Starting script...")
    print(f"{BEFORE + current_time_hour() + AFTER} {INFO} User-Agent: {white + user_agent}")

    
    website_url = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Website URL -> {reset}")
    Censored(website_url)

    
    if not website_url.startswith(("http://", "https://")):
        website_url = "https://" + website_url

    def CssAndJs(html_content, base_url):
        soup = BeautifulSoup(html_content, 'html.parser')

        
        print(f"{BEFORE + current_time_hour() + AFTER} {WAIT} Retrieving CSS...")
        css_links = soup.find_all('link', rel='stylesheet')
        css_urls = [urljoin(base_url, link['href']) for link in css_links if 'href' in link.attrs]
        css_urls = [url for url in css_urls if not url.startswith('data:')]
        all_css = []

        
        with concurrent.futures.ThreadPoolExecutor() as executor:
            css_responses = list(executor.map(requests.get, css_urls))
            for resp in css_responses:
                if resp.status_code == 200:
                    all_css.append(resp.text)
                else:
                    print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Failed to retrieve CSS.")

        
        if all_css:
            style_tag = soup.new_tag('style')
            style_tag.string = "\n".join(all_css)
            if soup.head:
                soup.head.append(style_tag)
            else:
                soup.insert(0, style_tag)
            
            for link in css_links:
                link.decompose()

        
        print(f"{BEFORE + current_time_hour() + AFTER} {WAIT} Retrieving JavaScript...")
        script_links = soup.find_all('script', src=True)
        js_urls = [urljoin(base_url, script['src']) for script in script_links if 'src' in script.attrs]
        js_urls = [url for url in js_urls if not url.startswith('data:')]
        all_js = []

        
        with concurrent.futures.ThreadPoolExecutor() as executor:
            js_responses = list(executor.map(requests.get, js_urls))
            for resp in js_responses:
                if resp.status_code == 200:
                    all_js.append(resp.text)
                else:
                    print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Failed to retrieve JS.")

        
        if all_js:
            script_tag = soup.new_tag('script')
            script_tag.string = "\n".join(all_js)
            if soup.body:
                soup.body.append(script_tag)
            else:
                soup.insert(len(soup.contents), script_tag)
            
            for script in script_links:
                script.decompose()

        return soup.prettify()

    
    print(f"{BEFORE + current_time_hour() + AFTER} {WAIT} Retrieving HTML...")
    session = requests.Session()
    response = session.get(website_url, headers=headers, timeout=5)

    if response.status_code == 200:
        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')
        title_str = soup.title.string if soup.title else 'Phishing'
        file_name = re.sub(r'[\\/:*?"<>|]', '-', title_str)

        
        output_path = os.path.expandvars(r"%USERPROFILE%\OneDrive\Bureau\BLUE_SPIDER_free\1-Output\PhishingAttack")
        os.makedirs(output_path, exist_ok=True)
        file_html = os.path.join(output_path, f"{file_name}.html")

        
        final_html = CssAndJs(html_content, website_url)

        
        with open(file_html, 'w', encoding='utf-8') as f:
            f.write(final_html)

        print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Phishing successful. File saved here: \"{file_html}\"")
        Continue()
        Reset()
    else:
        ErrorUrl()

except Exception as e:
    Error(e)