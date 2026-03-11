import os
from bs4 import BeautifulSoup
import requests
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
    from bs4 import BeautifulSoup
    import requests
except ImportError as e:

    print(f"Error importing modules: {e}")
   
    exit(1)




def instagram(email):
    """Checks if the given email is associated with an Instagram account."""
    try:
        
        global user_agent 
        session = requests.Session()
        headers = {
            'User-Agent': user_agent,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Origin': 'https://www.instagram.com',
            'Connection': 'keep-alive',
            'Referer': 'https://www.instagram.com/'
        }

        data = {"email": email}

        
        response = session.get("https://www.instagram.com/accounts/emailsignup/", headers=headers)
        if response.status_code != 200:
            return f"Error: Status Code {response.status_code} in Step 1."

        token = session.cookies.get('csrftoken')
        if not token:
            return "Error: CSRF Token Not Found."

        headers["x-csrftoken"] = token
        headers["Referer"] = "https://www.instagram.com/accounts/emailsignup/"

        
        response = session.post(
            url="https://www.instagram.com/api/v1/web/accounts/web_create_ajax/attempt/",
            headers=headers,
            data=data
        )
        
        if response.status_code == 200:
            
            response_text = response.text
            if "Another account is using the same email." in response_text or "email_is_taken" in response_text:
                return True
            return False
        
        return f"Error: Status Code {response.status_code} in Step 2."
    
    except Exception as e:
        return f"Error: {e}"

def twitter(email):
    """Checks if the given email is associated with a Twitter (X) account."""
    try:
        session = requests.Session()
        
        response = session.get(
            url="https://api.twitter.com/i/users/email_available.json",
            params={"email": email}
        )
        if response.status_code == 200:
            return response.json().get("taken", False)
        return f"Error: Status Code {response.status_code}"
    except Exception as e:
        return f"Error: {e}"

def pinterest(email):
    """Checks if the given email is associated with a Pinterest account."""
    try:
        session = requests.Session()

        data_param = '{"options": {"email": "' + email + '"}, "context": {}}'
        
        response = session.get(
            "https://www.pinterest.com/_ngjs/resource/EmailExistsResource/get/",
            params={"source_url": "/", "data": data_param}
        )

        if response.status_code == 200:
            data = response.json().get("resource_response", {})
            message = data.get("message")
            if message == "Invalid email.":
                return False
            
            return data.get("data") is not False
        
        return f"Error: Status Code {response.status_code}"
    except Exception as e:
        return f"Error: {e}"

def imgur(email):
    """Checks if the given email is associated with an Imgur account."""
    try:
        global user_agent
        session = requests.Session()
        headers = {
            'User-Agent': user_agent,
            'Accept': '*/*',
            'Accept-Language': 'en,en-US;q=0.5',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Origin': 'https://imgur.com',
            'DNT': '1',
            'Connection': 'keep-alive',
            'TE': 'Trailers',
        }

        
        session.get("https://imgur.com/register?redirect=%2Fuser", headers=headers)

        headers["X-Requested-With"] = "XMLHttpRequest"

        data = {'email': email}
        
        response = session.post('https://imgur.com/signin/ajax_email_available', headers=headers, data=data)

        if response.status_code == 200:
            data = response.json().get('data', {})
            
            if data.get("available") is True:
                return False
            if "Invalid email domain" in response.text:
                return False 
            return True 
        
        return f"Error: Status Code {response.status_code}"
    except Exception as e:
        return f"Error: {e}"

def patreon(email):
    """Checks if the given email is associated with a Plurk account (Original script used Plurk URL)."""


    try:
        global user_agent
        session = requests.Session()
        headers = {
            'User-Agent': user_agent,
            'Accept': '*/*',
            
            'Accept-Language': 'en-US,en;q=0.5',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'X-Requested-With': 'XMLHttpRequest',
            
            'Origin': 'https://www.plurk.com',
            'DNT': '1',
            'Connection': 'keep-alive',
        }

        data = {'email': email}
       
        response = session.post('https://www.plurk.com/Users/isEmailFound', headers=headers, data=data)
        
        if response.status_code == 200:
            
            return "True" in response.text
        
        return f"Error: Status Code {response.status_code}"
    except Exception as e:
        return f"Error: {e}"

def spotify(email):
    """Checks if the given email is associated with a Spotify account."""

    try:
        global user_agent
        session = requests.Session()
        headers = {
            'User-Agent': user_agent,
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.5',
            'DNT': '1',
            'Connection': 'keep-alive',
        }
        
        params = {'validate': '1', 'email': email}
        
        response = session.get('https://spclient.wg.spotify.com/signup/public/v1/account',
                                headers=headers,
                                params=params)
        
        if response.status_code == 200:
            
            status = response.json().get("status")
            return status == 20
        
        return f"Error: Status Code {response.status_code}"
    except Exception as e:
        return f"Error: {e}"

def firefox(email):
    """Checks if the given email is associated with a Firefox account."""
    try:
        session = requests.Session()
        data = {"email": email}
        response = session.post("https://api.accounts.firefox.com/v1/account/status", data=data)

        if response.status_code == 200:

            return "false" not in response.text
        
        return f"Error: Status Code {response.status_code}"
    except Exception as e:
        return f"Error: {e}"

def last_pass(email):
    """Checks if the given email is associated with a LastPass account."""
    try:
        global user_agent
        session = requests.Session()
        headers = {
            'User-Agent': user_agent,
            'Accept': '*/*',
            'Accept-Language': 'en,en-US;q=0.5',
            'Referer': 'https://lastpass.com/',
            'X-Requested-With': 'XMLHttpRequest',
            'DNT': '1',
            'Connection': 'keep-alive',
            'TE': 'Trailers',
        }
        
        
        params = {
            'check': 'avail',
            'skipcontent': '1',
            'mistype': '1',
            'username': email,
        }
        

        response = session.get(
            'https://lastpass.com/create_account.php',
            params=params,
            headers=headers
        )
        
        if response.status_code == 200:

            if "no" in response.text:
                return True
            return False
        
        return f"Error: Status Code {response.status_code}"
    except Exception as e:
        return f"Error: {e}"

def archive(email):
    """Checks if the given email is associated with an Archive.org account."""
    try:
        global user_agent
        session = requests.Session()


        headers = {
            'User-Agent': user_agent,
            'Accept': '*/*',
            'Accept-Language': 'en,en-US;q=0.5',
            
            'Content-Type': 'multipart/form-data; boundary=---------------------------', 
            'Origin': 'https://archive.org',
            'Connection': 'keep-alive',
            'Referer': 'https://archive.org/account/signup',
            'Sec-GPC': '1',
            'TE': 'Trailers',
        }


        boundary = '---------------------------'
        data_body = (
            f'{boundary}\r\nContent-Disposition: form-data; name="input_name"\r\n\r\nusername\r\n'
            f'{boundary}\r\nContent-Disposition: form-data; name="input_value"\r\n\r\n{email}\r\n'
            f'{boundary}\r\nContent-Disposition: form-data; name="input_validator"\r\n\r\ntrue\r\n'
            f'{boundary}\r\nContent-Disposition: form-data; name="submit_by_js"\r\n\r\ntrue\r\n'
            f'{boundary}--\r\n'
        )
        
        
        headers['Content-Type'] = f'multipart/form-data; boundary={boundary.strip("-")}'

        response = session.post('https://archive.org/account/signup', headers=headers, data=data_body)
        
        if response.status_code == 200:
            
            return "is already taken." in response.text
        
        return f"Error: Status Code {response.status_code}"
    except Exception as e:
        return f"Error: {e}"

def pornhub(email):
    """Checks if the given email is associated with a PornHub account."""
    try:
        global user_agent
        session = requests.Session()
        headers = {
            'User-Agent': user_agent,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en,en-US;q=0.5',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        
        
        response = session.get("https://www.pornhub.com/signup", headers=headers)
        
        if response.status_code == 200:
            
            soup = BeautifulSoup(response.content, features="html.parser")
            token_tag = soup.find(attrs={"name": "token"})
            
            if token_tag is None:
                return "Error: Token Not Found."
            
            token = token_tag.get("value")
        else:
            return f"Error: Status Code {response.status_code} in Step 1."

       
        params = {'token': token}
        data = {'check_what': 'email', 'email': email}
        response = session.post('https://www.pornhub.com/user/create_account_check', headers=headers, params=params, data=data) 
        
        if response.status_code == 200:
            
            if response.json().get("error_message") == "Email has been taken.":
                return True
            return False
        
        return f"Error: Status Code {response.status_code} in Step 2."
    except Exception as e:
        return f"Error: {e}"

def xnxx(email):
    """Checks if the given email is associated with an XNXX account."""
    
    try:
        global user_agent
        session = requests.Session()
        headers = {
            'User-Agent': user_agent,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-en',
            'Host': 'www.xnxx.com',
            'Referer': 'https://www.google.com/',
            'Connection': 'keep-alive'
        }
        
        
        cookie_response = session.get('https://www.xnxx.com', headers=headers)

        if cookie_response.status_code != 200:
            return f"Error: Status Code {cookie_response.status_code} in Step 1."

       
        headers['Referer'] = 'https://www.xnxx.com/video-holehe/palenath_fucks_xnxx_with_holehe'
        headers['X-Requested-With'] = 'XMLHttpRequest'

        

        params = {'email': email}
        response = session.get(
            'https://www.xnxx.com/account/checkemail', 
            headers=headers, 
            params=params,
            cookies=cookie_response.cookies
        )
        
        if response.status_code == 200:
            try:
                response_json = response.json()
                
                if response_json.get('message') == "This email is already in use or its owner has excluded it from our website.":
                    return True
                
                elif response_json.get('message') == "Invalid email address.": 
                    return False
                
                
                if response_json.get('result') == "false":
                    return True
                elif response_json.get('code') == 1:
                    return True
                elif response_json.get('result') == "true":
                    return False
                elif response_json.get('code') == 0:
                    return False  
                else:
                    return False
            except requests.exceptions.JSONDecodeError:
                
                return f"Error: Invalid response format from XNXX."
        
        return f"Error: Status Code {response.status_code} in Step 2."
    except Exception as e:
        return f"Error: {e}"

def xvideo(email):
    """Checks if the given email is associated with an Xvideo account."""
    
    try:
        global user_agent
        session = requests.Session()
        headers = {
            'User-Agent': user_agent,
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'X-Requested-With': 'XMLHttpRequest',
            'Connection': 'keep-alive',
            'Referer': 'https://www.xvideos.com/',
        }

        params = {'email': email}
        response = session.get('https://www.xvideos.com/account/checkemail', headers=headers, params=params)
        
        if response.status_code == 200:
            try:
                response_json = response.json()
                
                if response_json.get('message') == "This email is already in use or its owner has excluded it from our website.": 
                    return True
                
                elif response_json.get('message') == "Invalid email address.": 
                    return False
                
                
                if response_json.get('result') == "false":
                    return True
                elif response_json.get('code') == 1:
                    return True
                elif response_json.get('result') == "true":
                    return False
                elif response_json.get('code') == 0:
                    return False  
                else:
                    return False
            except requests.exceptions.JSONDecodeError:
                
                return f"Error: Invalid response format from Xvideo."

        return f"Error: Status Code {response.status_code}"
    except Exception as e:
        return f"Error: {e}"



try:

    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36" # Placeholder


    print(f"Selected User-Agent: {user_agent}")
    

    email = input("Enter Email to check -> ")
    

    print("Scanning...")


   
    sites = [
        instagram, twitter, pinterest, imgur, patreon, spotify, firefox, last_pass, archive, pornhub, xnxx, xvideo
    ]
    
    site_founds = []
    found = 0
    not_found = 0
    unknown = 0
    error = 0

    print("\n--- Results ---")
    for site_func in sites:
        site_name = site_func.__name__.replace('_', ' ').title() 
        result = site_func(email)
        
        if result is True:
           
            print(f" {site_name}: Found")
            site_founds.append(site_name)
            found += 1
        elif result is False:
            
            print(f" {site_name}: Not Found")
            not_found += 1
        elif isinstance(result, str) and result.startswith("Error:"):
            
            print(f" {site_name}: Error ({result})")
            error += 1
        else:
            
            print(f" {site_name}: Unknown Result")
            unknown += 1

    print("\n--- Summary ---")
    if found:
        
        print(f"Total Found ({found}): {', '.join(site_founds)}")
    
    print(f"Not Found: {not_found}, Unknown: {unknown}, Error: {error}")
    

    
except Exception as e:
    
    print(f"An unexpected error occurred in the main process: {e}")