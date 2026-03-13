import requests
import time
import os


red = '\033[91m'
white = '\033[97m'
reset = '\033[0m'

INFO_ADD = "" 
BEFORE = "" 
AFTER = ""
INPUT = ">"

    
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



try:

    pass 
except Exception as e:

    pass 



try:

    

    invite = input(f"Enter the Discord Server Invitation -> ")
    
    try:
        
        invite_code = invite.split("/")[-1]
    except Exception:
        
        invite_code = invite

    
    response = requests.get(f"https://discord.com/api/v9/invites/{invite_code}")

    if response.status_code == 200:
        api = response.json()

        
        
        type_value = api.get('type', "None")
        code_value = api.get('code', "None")
        expires_at = api.get('expires_at', "None")
        flags = api.get('flags', "None")
        
        
        inviter_info = api.get('inviter', {})
        inviter_id = inviter_info.get('id', "None")
        inviter_username = inviter_info.get('username', "None")
        inviter_avatar = inviter_info.get('avatar', "None")
        inviter_discriminator = inviter_info.get('discriminator', "None")
        inviter_public_flags = inviter_info.get('public_flags', "None")
        inviter_flags = inviter_info.get('flags', "None")
        inviter_banner = inviter_info.get('banner', "None")
        inviter_accent_color = inviter_info.get('accent_color', "None")
        inviter_global_name = inviter_info.get('global_name', "None")
        inviter_banner_color = inviter_info.get('banner_color', "None")
        
        
        server_info = api.get('guild', {})
        server_id = server_info.get('id', "None")
        server_name = server_info.get('name', "None")
        server_icon = server_info.get('icon', "None")
        server_features = server_info.get('features', "None")
        
        
        server_description = server_info.get('description', "None")
        
        server_verification_level = server_info.get('verification_level', "None")
        server_nsfw_level = server_info.get('nsfw_level', "None")
        server_nsfw = server_info.get('nsfw', "None")
        server_premium_subscription_count = server_info.get('premium_subscription_count', "None")
        
        
        if isinstance(server_features, list): 
            server_features = ' / '.join(server_features)
        
        
        channel_info = api.get('channel', {})
        channel_id = channel_info.get('id', "None")
        channel_type = channel_info.get('type', "None")
        channel_name = channel_info.get('name', "None")
        

        

        
        output_invitation = f"""
{red}Invitation Information:{reset}
{white}────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────{reset}
  {INFO_ADD} Invitation                        : {white}{invite}{red}{reset}
  {INFO_ADD} Type                              : {white}{type_value}{red}{reset}
  {INFO_ADD} Code                              : {white}{code_value}{red}{reset}
  {INFO_ADD} Expires At                        : {white}{expires_at}{red}{reset}
  {INFO_ADD} Server ID                         : {white}{server_id}{red}{reset}
  {INFO_ADD} Server Name                       : {white}{server_name}{red}{reset}
  {INFO_ADD} Channel ID                        : {white}{channel_id}{red}{reset}
  {INFO_ADD} Channel Name                      : {white}{channel_name}{red}{reset}
  {INFO_ADD} Channel Type                      : {white}{channel_type}{red}{reset}
  {INFO_ADD} Server Description                : {white}{server_description}{red}{reset}
  {INFO_ADD} Server Icon                       : {white}{server_icon}{red}{reset}
  {INFO_ADD} Server Features                   : {white}{server_features}{red}{reset}
  {INFO_ADD} Server NSFW Level                 : {white}{server_nsfw_level}{red}{reset}
  {INFO_ADD} Server NSFW                       : {white}{server_nsfw}{red}{reset}
  {INFO_ADD} Flags                             : {white}{flags}{red}{reset}
  {INFO_ADD} Server Verification Level         : {white}{server_verification_level}{red}{reset}
  {INFO_ADD} Server Premium Subscription Count : {white}{server_premium_subscription_count}{red}{reset}
{white}────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────{reset}
"""
        try:
            Slow(output_invitation)
        except NameError:
            print(output_invitation)
            
        if inviter_info:
            output_inviter = f"""{red}Inviter Information:{reset}
{white}────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────{reset}
  {INFO_ADD} ID                                : {white}{inviter_id}{red}{reset}
  {INFO_ADD} Username                          : {white}{inviter_username}{red}{reset}
  {INFO_ADD} Global Name                       : {white}{inviter_global_name}{red}{reset}
  {INFO_ADD} Avatar                            : {white}{inviter_avatar}{red}{reset}
  {INFO_ADD} Discriminator                     : {white}{inviter_discriminator}{red}{reset}
  {INFO_ADD} Public Flags                      : {white}{inviter_public_flags}{red}{reset}
  {INFO_ADD} Flags                             : {white}{inviter_flags}{red}{reset}
  {INFO_ADD} Banner                            : {white}{inviter_banner}{red}{reset}
  {INFO_ADD} Accent Color                      : {white}{inviter_accent_color}{red}{reset}
  {INFO_ADD} Banner Color                      : {white}{inviter_banner_color}{red}{reset}
{white}────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────{reset}
"""
            try:
                Slow(output_inviter)
            except NameError:
                print(output_inviter)
            
    else:
        
        print("Error: Could not retrieve invitation information (status code:", response.status_code, ")")
        

    
except requests.exceptions.RequestException as req_e:

    print(f"Request Error: {req_e}")
except Exception as e:

    print(f"An unexpected error occurred: {e}")