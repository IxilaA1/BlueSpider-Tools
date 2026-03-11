import requests
import json
import sys
import time
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

def get_user_data_from_v2_api(user_id):
    """
    Retrieves additional information (Robux, Premium, etc.) 
    using the user ID.
    Returns an empty dictionary ({}) in case of failure to avoid 'NoneType' errors.
    """
    url = f"https://www.roblox.com/mobileapi/userinfo?userID={user_id}"
    try:
        
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            
            return {}
    except:
        
        return {}


def get_roblox_user_info(cookie):
    """
    Checks the validity of the cookie and retrieves user information.
    """
    
    auth_url = "https://users.roblox.com/v1/users/authenticated"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    cookies = {".ROBLOSECURITY": cookie}

    print("\n[INFO] Attempting to retrieve information...")

    try:
        
        response = requests.get(auth_url, headers=headers, cookies=cookies)

        if response.status_code == 200:
            user_data_v1 = response.json()
            user_id = user_data_v1.get('id')
            username = user_data_v1.get('name')

            if user_id and username:
                
                user_data_v2 = get_user_data_from_v2_api(user_id)
                
                return {
                    "Status": "Valid",
                    "Username": username,
                    "Id": user_id,
                    "Robux": user_data_v2.get("RobuxBalance", "N/A"),
                    "Premium": user_data_v2.get("IsPremium", "N/A"),
                    "Builders Club": user_data_v2.get("IsAnyBuildersClubMember", "N/A"),
                    "Avatar URL": user_data_v2.get("ThumbnailUrl", "N/A")
                }
            else:
                return {"Status": "Invalid (No User Data)", "Message": "Valid cookie, but no user data was returned."}

        elif response.status_code == 401:
            
             return {"Status": "Invalid (401 Unauthorized)", "Message": "The .ROBLOSECURITY cookie is invalid or has expired."}
        
        else:
            return {"Status": f"Invalid (HTTP {response.status_code})", "Message": f"HTTP request failed with status {response.status_code}."}
            
    except requests.exceptions.RequestException as e:
        return {"Status": "Error", "Message": f"Connection error: {e}"}
    except json.JSONDecodeError:
        return {"Status": "Error", "Message": "API response was not valid JSON."}
    except Exception as e:
        return {"Status": "Fatal Error", "Message": f"An internal error occurred: {e}"}


def display_info(data):
    """Displays the user information in a clear format."""
    print("\n" + "=" * 50)
    print("      Roblox Cookie Information")
    print("=" * 50)
    
    for key, value in data.items():
        print(f"[{key.upper().ljust(15)}] : {value}")

    print("=" * 50 + "\n")


if __name__ == "__main__":
    try:
        roblox_cookie = input("[INPUT] Please enter the .ROBLOSECURITY cookie: ").strip()
        
        if not roblox_cookie:
            print("[ERROR] The cookie cannot be empty.")
            sys.exit(1)
            
        if roblox_cookie.startswith("|WARNING"):
              roblox_cookie = roblox_cookie.split("|")[-1]
              print("[WARNING] The cookie warning prefix has been removed.")

        user_data = get_roblox_user_info(roblox_cookie)
        display_info(user_data)
        
    except ImportError as e:
        print(f"[CRITICAL ERROR] Required module is not installed: {e}")
        print("Please install dependencies with: pip install requests")
    except Exception as e:
        
        print(f"[FATAL ERROR] An unexpected error occurred: {e}")