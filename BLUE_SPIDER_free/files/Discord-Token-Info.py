# (c) 2026 IxilaA1 - Tous droits réservés / All rights reserved / Todos los derechos reservados.
# Ce code ne peut être ni vendu, ni modifié, ni partagé sans autorisation, ni publié à votre nom.
# This code may not be sold, modified, or shared without authorization, nor published under your name.
# Este código no puede ser vendido, modificado ni compartido sin autorización, ni publicado a su nombre.
# -------------------------------------------------------------------------------------------------------
import requests
import json
from datetime import datetime, timezone
import time
import os
import sys 

    
logo_ascii = """
                                              @@@@                @%@@                                      
                                       @@@@@@@@@@@@               @@@@@@@@@@%                               
                                  @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                          
                                 @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%                         
                                %@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                        
                               @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                       
                              @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                      
                             @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                     
                            @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%                    
                           @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                   
                          %@@@@@@@@@@@@@@@@@@    @@@@@@@@@@@@@@@@@@    @@@@@@@@@@@@@@@@@@%                  
                          %@@@@@@@@@@@@@@@@        %@@@@@@@@@@@%@        @@@@@@@@@@@@@@@@@                  
                          %@@@@@@@@@@@@@@@          @@@@@@@@@@@@          @@@@@@@@@@@@@@@%                  
                         %@@@@@@@@@@@@@@@@          @@@@@@@@@@@%          %@@@@@@@@@@@@@@@@                 
                         @@@@@@@@@@@@@@@@@%         @@@@@@@@@@@%         %@@@@@@@@@@@@@@@@@                 
                         @@@@@@@@@@@@@@@@@@@      %@@@@@@@@@@@@@@@      @@@@@@@@@@@@@@@@@@%                 
                         %@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%                 
                         @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%                 
                         @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                 
                         @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%                 
                           @%@@@@@@@@@@@@@%@@   @@@@%@@@@@@@@@%%%@%@@  @@@@@@@@@@@@@@@@@@                   
                              @@%@@@@@@@@@@@@@                        @%@@@@@@@@@@@%@@                      
                                   @%@@@@@@@                            @@@@@@%%@                           
                                         @@                              @@             

"""


os.system('cls' if os.name == 'nt' else 'clear')


print(logo_ascii)


time.sleep(2)



def ErrorModule(e):
    """Placeholder for module-level error handling."""
    print(f"[!] Import/Initialization Error: {e}", file=sys.stderr)

def Title(text):
    """Placeholder for setting the title."""
    print(f"\n--- {text} ---")

def Slow(text):
    """Placeholder for slow output printing."""
    print(text)

def Choice1TokenDiscord():
    """Placeholder for getting the Discord token (Simulates user input)."""
   
    return input("Please enter your Discord token (for personal use only): ")

def current_time_hour():
    """Placeholder for the current time."""
    return datetime.now().strftime("%H:%M:%S")


BEFORE, AFTER, WAIT, reset = "", "", "", "\033[0m"
ERROR, white, INFO_ADD, red = "[ERROR]", "\033[1;37m", "[+]", "\033[91m"

def Continue():
    """Placeholder for continuing."""
    input("Press Enter to continue...")

def Reset():
    """Placeholder for resetting."""
    pass

def Error(e):
    """Placeholder for final error handling."""
    print(f"[CRITICAL] An error occurred: {e}", file=sys.stderr)


try:
    import requests
    from datetime import datetime, timezone
except Exception as e:
    ErrorModule(e)
    sys.exit(1)
    
Title("Discord Token Info")

def get_discord_info(token):
    """
    Core function to retrieve all Discord account information.
    Returns a dictionary with the data.
    """
    

    BASE_URL = 'https://discord.com/api/v9'
    HEADERS = {'Authorization': token, 'Content-Type': 'application/json'}
    
    data = {}
    
    
    try:
        user_response = requests.get(f'{BASE_URL}/users/@me', headers=HEADERS)
        user_api = user_response.json()
        
        if user_response.status_code == 200:
            data['status'] = "Valid"
            data['user_api'] = user_api
        else:
            data['status'] = f"Invalid (Code: {user_response.status_code})"
            
            return data
            
    except requests.exceptions.RequestException as e:
        print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Discord server connection error: {white}{e}{reset}")
        data['status'] = "Request Error"
        return data
        
    
    
    api = data['user_api']
    data['token_discord'] = token
    
    data['username_discord'] = f"{api.get('username', 'None')}#{api.get('discriminator', 'None')}" if api.get('discriminator', '0') != '0' else api.get('username', 'None')
    data['display_name_discord'] = api.get('global_name', "None")
    data['user_id_discord'] = api.get('id', "None")
    data['email_discord'] = api.get('email', "None")
    data['email_verified_discord'] = api.get('verified', "None")
    data['phone_discord'] = api.get('phone', "None")
    data['mfa_discord'] = api.get('mfa_enabled', "None")
    data['country_discord'] = api.get('locale', "None")
    data['avatar_discord'] = api.get('avatar', "None")
    data['avatar_decoration_discord'] = api.get('avatar_decoration_data', "None")
    data['public_flags_discord'] = api.get('public_flags', "None")
    data['flags_discord'] = api.get('flags', "None")
    data['banner_discord'] = api.get('banner', "None")
    data['banner_color_discord'] = api.get('banner_color', "None")
    data['accent_color_discord'] = api.get("accent_color", "None")
    data['nsfw_discord'] = api.get('nsfw_allowed', "None")

    
    try:
        if data['user_id_discord'] != "None":
            
            timestamp = ((int(data['user_id_discord']) >> 22) + 1420070400000) / 1000
            data['created_at_discord'] = datetime.fromtimestamp(timestamp, timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')
        else:
             data['created_at_discord'] = "None"
    except Exception:
        data['created_at_discord'] = "None"

    
    nitro_types = {0: 'False', 1: 'Nitro Classic', 2: 'Nitro Boosts', 3: 'Nitro Basic'}
    
    data['nitro_discord'] = nitro_types.get(api.get('premium_type', 0), 'False')
    
    
    data['avatar_url_discord'] = "None"
    if data['avatar_discord'] and data['user_id_discord'] != "None":
        gif_url = f"https://cdn.discordapp.com/avatars/{data['user_id_discord']}/{data['avatar_discord']}.gif"
        try:
           
            if requests.head(gif_url, timeout=5).status_code == 200:
                data['avatar_url_discord'] = gif_url
            else:
                data['avatar_url_discord'] = f"https://cdn.discordapp.com/avatars/{data['user_id_discord']}/{data['avatar_discord']}.png"
        except requests.exceptions.RequestException:
            data['avatar_url_discord'] = "URL Unavailable"


    
    bio = api.get('bio')
    data['bio_discord'] = bio if bio and bio.strip() else "None"

    
    try:
        guilds_response = requests.get(f'{BASE_URL}/users/@me/guilds?with_counts=true', headers=HEADERS)
        if guilds_response.status_code == 200:
            guilds = guilds_response.json()
            data['guild_count'] = len(guilds)
            
            owner_guilds = [g for g in guilds if g.get('owner')]
            data['owner_guild_count'] = f"({len(owner_guilds)})"
            
            owner_guilds_names = [f"{g.get('name', 'N/A')} ({g.get('id', 'N/A')})" for g in owner_guilds]
            data['owner_guilds_names'] = "\n" + "\n".join(owner_guilds_names) if owner_guilds_names else "None"
        else:
            data['guild_count'] = data['owner_guild_count'] = data['owner_guilds_names'] = "Access Denied/API Error"
    except Exception:
        data['guild_count'] = data['owner_guild_count'] = data['owner_guilds_names'] = "None"
        
    
    try:
        
        billing_response = requests.get(f'{BASE_URL}/users/@me/billing/payment-sources', headers=HEADERS)
        billing_discord = billing_response.json()
        
        if billing_response.status_code == 200 and billing_discord:
            payment_types = {1: 'CB', 2: 'Paypal'}
            payment_methods = [payment_types.get(method.get('type'), 'Other') for method in billing_discord]
            data['payment_methods_discord'] = ' / '.join(payment_methods)
        else:
            data['payment_methods_discord'] = "None"
    except Exception:
        data['payment_methods_discord'] = "None"

    
    try:
        
        friends_response = requests.get(f'{BASE_URL}/users/@me/relationships', headers=HEADERS)
        friends = friends_response.json()
        
        if friends_response.status_code == 200 and friends:
            friends_discord_list = []
            
            for friend in friends:
                
                if friend.get('type') == 1 and friend.get('user'):
                    user = friend['user']
                     
                    discriminator = f"#{user.get('discriminator', '0000')}" if user.get('discriminator', '0') != '0' else ''
                    
                    friend_data = f"{user.get('username', 'N/A')}{discriminator} ({user.get('id', 'N/A')})"

                    
                    if len('\n'.join(friends_discord_list)) + len(friend_data) >= 1024:
                        friends_discord_list.append("... and more")
                        break
                        
                    friends_discord_list.append(friend_data)

            data['friends_discord'] = '\n' + '\n'.join(friends_discord_list) if friends_discord_list else "None"
        else:
            data['friends_discord'] = "None"
    except Exception:
        data['friends_discord'] = "None"
        
    
    try:
        gift_codes_response = requests.get(f'{BASE_URL}/users/@me/outbound-promotions/codes', headers=HEADERS)
        gift_codes = gift_codes_response.json()
        
        if gift_codes_response.status_code == 200 and gift_codes:
            codes_data = []
            
            for gift in gift_codes:
                name = gift.get('promotion', {}).get('outbound_title', 'Unknown Title')
                code = gift.get('code', 'Unknown Code')
                data_entry = f"Gift: {name}\nCode: {code}"

                
                if len('\n\n'.join(codes_data)) + len(data_entry) >= 1024:
                    codes_data.append("... and more")
                    break
                    
                codes_data.append(data_entry)
                
            data['gift_codes_discord'] = '\n\n'.join(codes_data) if codes_data else "None"
        else:
            data['gift_codes_discord'] = "None"
    except Exception:
        data['gift_codes_discord'] = "None"
        
    
    data['linked_users_discord'] = "Not available via this API endpoint"
    data['authenticator_types_discord'] = "Not available via this API endpoint"
    
    return data


try:
    Slow("Starting token information retrieval.")
    token_discord = Choice1TokenDiscord()
    print(f"{BEFORE + current_time_hour() + AFTER} {WAIT} Retrieving information...{reset}")

    
    info_data = get_discord_info(token_discord)
    status = info_data.get('status', 'Unknown')

    if status != "Valid":
        print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} The token is {status}. Cannot retrieve details.{reset}")
    else:
        
        Slow(f"""
{white}────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
 {INFO_ADD} Status              : {white}{status}{red}
 {INFO_ADD} Token               : {white}{info_data['token_discord']}{red}
 {INFO_ADD} Username            : {white}{info_data['username_discord']}{red}
 {INFO_ADD} Display Name        : {white}{info_data['display_name_discord']}{red}
 {INFO_ADD} Id                  : {white}{info_data['user_id_discord']}{red}
 {INFO_ADD} Created             : {white}{info_data['created_at_discord']}{red}
 {INFO_ADD} Country             : {white}{info_data['country_discord']}{red}
 {INFO_ADD} Email               : {white}{info_data['email_discord']}{red}
 {INFO_ADD} Verified            : {white}{info_data['email_verified_discord']}{red}
 {INFO_ADD} Phone               : {white}{info_data['phone_discord']}{red}
 {INFO_ADD} Nitro               : {white}{info_data['nitro_discord']}{red}
 {INFO_ADD} Linked Users        : {white}{info_data['linked_users_discord']}{red}
 {INFO_ADD} Avatar Decor        : {white}{info_data['avatar_decoration_discord']}{red}
 {INFO_ADD} Avatar Hash         : {white}{info_data['avatar_discord']}{red}
 {INFO_ADD} Avatar URL          : {white}{info_data['avatar_url_discord']}{red}
 {INFO_ADD} Accent Color        : {white}{info_data['accent_color_discord']}{red}
 {INFO_ADD} Banner Hash         : {white}{info_data['banner_discord']}{red}
 {INFO_ADD} Banner Color        : {white}{info_data['banner_color_discord']}{red}
 {INFO_ADD} Flags               : {white}{info_data['flags_discord']}{red}
 {INFO_ADD} Public Flags        : {white}{info_data['public_flags_discord']}{red}
 {INFO_ADD} NSFW                : {white}{info_data['nsfw_discord']}{red}
 {INFO_ADD} MFA                 : {white}{info_data['mfa_discord']}{red}
 {INFO_ADD} Authenticator Type  : {white}{info_data['authenticator_types_discord']}{red}
 {INFO_ADD} Billing             : {white}{info_data['payment_methods_discord']}{red}
 {INFO_ADD} Gift Codes          : {white}{info_data['gift_codes_discord']}{red}
 {INFO_ADD} Guilds (Total)      : {white}{info_data['guild_count']}{red}
 {INFO_ADD} Owner Guilds        : {white}{info_data['owner_guild_count']}{info_data['owner_guilds_names']}{red}
 {INFO_ADD} Bio                 : {white}{info_data['bio_discord']}{red}
 {INFO_ADD} Friends (Top List)  : {white}{info_data['friends_discord']}{red}
{white}────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
    """)
    Continue()
    Reset()
    
except Exception as e:
    Error(e)