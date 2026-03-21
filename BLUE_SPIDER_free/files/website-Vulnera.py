# (c) 2026 IxilaA1 - Tous droits réservés / All rights reserved / Todos los derechos reservados.
# Ce code ne peut être ni vendu, ni modifié, ni partagé sans autorisation, ni publié à votre nom.
# This code may not be sold, modified, or shared without authorization, nor published under your name.
# Este código no puede ser vendido, modificado ni compartido sin autorización, ni publicado a su nombre.
# -------------------------------------------------------------------------------------------------------
import requests
import time
import os
import random
import sys


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


def Title(title_text):
    """Sets a title for the script's output."""
    print(f"\n{'='*50}\n{title_text}\n{'='*50}")

def ChoiceUserAgent():
    """Returns a generic user agent string."""
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0"
    ]
    return random.choice(user_agents)

def current_time_hour():
    """Returns the current time in HH:MM:SS format."""
    return time.strftime("%H:%M:%S")

def log_output(log_type, vulnerability_name, status, details=""):
    """Standardized logging function."""
    time_str = current_time_hour()
    if log_type == "VALID":
        print(f"[{time_str}] [  +  ] Vulnerability: {vulnerability_name} | Status: True | {details}")
    elif log_type == "ERROR":
        print(f"[{time_str}] [  -  ] Vulnerability: {vulnerability_name} | Status: False | {details}")
    elif log_type == "INFO":
        print(f"[{time_str}] [  * ] {vulnerability_name}")
    elif log_type == "INPUT":
        return input(f"[{time_str}] [  ?  ] {vulnerability_name} -> ")
    elif log_type == "WAIT":
        print(f"[{time_str}] [  ~  ] {vulnerability_name}")
    else:
        print(f"[{time_str}] [  !  ] {vulnerability_name}: {details}")



try:
   
    pass

except ImportError as e:
    
    print(f"Error: The 'requests' library is not installed. Please run 'pip install requests'")
    sys.exit(1)

Title("SQL Vulnerability Scanner (Educational)")

try:
    
    user_agent = ChoiceUserAgent()
    headers = {"User-Agent": user_agent}

    def InterestingPath(url):
        """Checks for common configuration and backup paths."""
        paths = [
            "admin", "admin/", "admin/index.php", "admin/login.php",
            "backup", "backup/db.sql", "private/.env", "uploads/file.txt",
            "api/v1/status", "logs/error.log", "cache/temp/", "server-status"
        ]
        CheckPaths(url, paths, "Interesting Path Exposure")

    def SensitiveFile(url):
        """Checks for paths that may expose sensitive server files (Local File Inclusion/Traversal)."""
        
        files = [
            "etc/passwd", "etc/shadow", "www/html/wp-config.php", "proc/self/environ"
        ]
        CheckPaths(url, files, "Sensitive File Exposure (LFI/LFD)")

    def Xss(url):
        """Tests for Cross-Site Scripting (XSS) vulnerabilities."""
        
        payloads = [
            "<script>alert('XssFound')</script>",
            "<img src=x onerror=alert('XssFound')>",
            "<svg/onload=alert('XssFound')>"
        ]
        indicators = ["<script>", "alert(", "onerror=", "<svg", "javascript:"]
        TestPayloads(url, payloads, indicators, "Cross-Site Scripting (XSS)")

    def Sql(url):
        """Tests for SQL Injection (SQLi) vulnerabilities."""
        
        payloads = [
            "'", '"', "''", "' OR '1'='1' --", "' OR 1=1 /*",
            "' UNION SELECT NULL, NULL, NULL --", "admin'--", "' OR 1=1#"
        ]
       
        indicators = [
            "SQL syntax", "SQL error", "MySQL", "Unclosed quotation mark",
            "SQLSTATE", "syntax error", "ORA-", "Incorrect syntax near"
        ]
        TestPayloads(url, payloads, indicators, "SQL Injection (SQLi)")

    def CheckPaths(url, paths, vulnerability_name):
        """Helper function to check for path/file existence (200 status code)."""
        try:
            
            if not url.endswith("/"):
                url += "/"
            
            found = False
            for path in paths:
                
                full_url = url + path
                response = requests.get(full_url, timeout=10, headers=headers)
                
                if response.status_code == 200:
                    found = True
                    log_output("VALID", vulnerability_name, "True", f"Path Found: {path}")
            
            if not found:
                log_output("ERROR", vulnerability_name, "False", "No common paths found.")
        
        except requests.exceptions.RequestException:
            log_output("ERROR", vulnerability_name, "Error", "Network or connection error during testing.")
        except Exception:
            log_output("ERROR", vulnerability_name, "Error", "Unknown error during testing.")

    def TestPayloads(url, payloads, indicators, vulnerability_name):
        """Helper function to test payloads and check for reflection or error indicators."""
        try:
           
            baseline_response = requests.get(url, timeout=10, headers=headers)
            
            
            found = False
            for payload in payloads:
                test_url = url.split('?')[0] + "/" + payload.replace(" ", "%20")
                
                response = requests.get(test_url, timeout=10, headers=headers)
                response_text = response.text.lower()
                

                

                if response.status_code == 200 and response_text != baseline_response.text.lower():
                    for indicator in indicators:
                        if indicator.lower() in response_text:
                            found = True
                            log_output("VALID", vulnerability_name, "True", f"Payload: {payload} | Indicator: {indicator}")
                            break 

            if not found:
                log_output("ERROR", vulnerability_name, "False", "No positive indicators found.")
        
        except requests.exceptions.RequestException:
            log_output("ERROR", vulnerability_name, "Error", "Network or connection error during testing.")
        except Exception:
            log_output("ERROR", vulnerability_name, "Error", "Unknown error during testing.")


    log_output("INFO", f"Selected User-Agent: {user_agent}", "")
    website_url = log_output("INPUT", "Target URL (e.g., https://example.com)", "")


    if not website_url.startswith(("https://", "http://")):
        website_url = "https://" + website_url

    log_output("WAIT", "Starting vulnerability scan...", "")


    Sql(website_url)
    Xss(website_url)
    InterestingPath(website_url)
    SensitiveFile(website_url)
    
    
    log_output("INFO", "Scan completed.", "")

except Exception as e:
    
    log_output("FATAL", "An unexpected error occurred", str(e))