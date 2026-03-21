# (c) 2026 IxilaA1 - Tous droits réservés / All rights reserved / Todos los derechos reservados.
# Ce code ne peut être ni vendu, ni modifié, ni partagé sans autorisation, ni publié à votre nom.
# This code may not be sold, modified, or shared without authorization, nor published under your name.
# Este código no puede ser vendido, modificado ni compartido sin autorización, ni publicado a su nombre.
# -------------------------------------------------------------------------------------------------------
import requests
import os
from colorama import Fore, init
from datetime import datetime


init()

logo = f"""{Fore.LIGHTBLUE_EX}
       ╔╦╗┬┌─┐┌─┐┌─┐┬─┐┌┬┐  
        ║║│└─┐│  │ │├┬┘ ││  
       ═╩╝┴└─┘└─┘└─┘┴└──┴┘
       ╦  ┌─┐┌─┐┬┌─┬ ┬┌─┐                     
       ║  │ ││ │├┴┐│ │├─┘                     
       ╩═╝└─┘└─┘┴ ┴└─┘┴
       {Fore.RED}|{Fore.WHITE}BLUESPIDER LOOKUP{Fore.RED}|
"""


API_URL = "https://japi.rest/discord/v1/user/"

def clear_screen():
    """Clear the screen based on operating system"""
    os.system("cls" if os.name == "nt" else "clear")

def get_user_info(user_id):
    """Retrieve Discord user information via the API"""
    try:
        response = requests.get(f"{API_URL}{user_id}", timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"{Fore.RED}\n[!] Connection error: {e}{Fore.RESET}")
        return None

def display_user_info(data):
    """Display formatted user information"""
    if not data or "data" not in data:
        print(f"{Fore.RED}[!] Invalid data format{Fore.RESET}")
        return

    user_data = data["data"]
    
    print(f"\n{Fore.GREEN}=== USER INFORMATION ==={Fore.RESET}")
    print(f"{Fore.CYAN}Username:{Fore.RESET} {user_data.get('username', 'Unknown')}")
    print(f"{Fore.CYAN}ID:{Fore.RESET} {user_data.get('id', 'Unknown')}")
    
    
    if "created_at" in user_data:
        try:
            
            created_at = datetime.fromisoformat(user_data["created_at"].replace('Z', '+00:00'))
            
            formatted_date = created_at.strftime('%d %B %Y at %H:%M:%S')
            
            days_elapsed = (datetime.now().astimezone() - created_at).days
            print(f"{Fore.CYAN}Account created:{Fore.RESET} {formatted_date}")
            print(f"{Fore.CYAN}Account age:{Fore.RESET} {days_elapsed} days")
        except:
            
            print(f"{Fore.CYAN}Account created:{Fore.RESET} {user_data['created_at']}")
    else:
        print(f"{Fore.CYAN}Account created:{Fore.RESET} Not available")
    
    
    global_name = user_data.get('global_name')
    if global_name:
        print(f"{Fore.CYAN}Global name:{Fore.RESET} {global_name}")
    
    
    avatar = user_data.get('avatar')
    if avatar and isinstance(avatar, str):
        avatar_url = f"https://cdn.discordapp.com/avatars/{user_data['id']}/{avatar}.png"
        print(f"{Fore.CYAN}Avatar:{Fore.RESET} {avatar_url}")
    elif isinstance(avatar, dict) and avatar.get('link'):
        print(f"{Fore.CYAN}Avatar:{Fore.RESET} {avatar['link']}")
    
    
    badges = user_data.get('badges')
    print(f"{Fore.CYAN}Badges (numbers):{Fore.RESET} {badges if badges is not None else 'None'}")
    
    
    if isinstance(badges, int) and badges > 0:
        badge_list = []
        if badges & 1: badge_list.append("Staff (1)")
        if badges & 2: badge_list.append("Partner (2)")
        if badges & 4: badge_list.append("HypeSquad Events (4)")
        if badges & 8: badge_list.append("Bug Hunter Level 1 (8)")
        if badges & 64: badge_list.append("HypeSquad Bravery (64)")
        if badges & 128: badge_list.append("HypeSquad Brilliance (128)")
        if badges & 256: badge_list.append("HypeSquad Balance (256)")
        if badges & 512: badge_list.append("Early Supporter (512)")
        if badges & 16384: badge_list.append("Bug Hunter Level 2 (16384)")
        if badge_list:
            print(f"{Fore.CYAN}Detailed badges:{Fore.RESET} {', '.join(badge_list)}")
    
    
    banner = user_data.get('banner')
    if banner:
        if isinstance(banner, dict):
            print(f"{Fore.CYAN}Banner:{Fore.RESET} {banner.get('link', 'Unknown')}")
            if banner.get('color'):
                print(f"{Fore.CYAN}Banner color:{Fore.RESET} {banner['color']}")
        elif isinstance(banner, str):
            banner_url = f"https://cdn.discordapp.com/banners/{user_data['id']}/{banner}.png"
            print(f"{Fore.CYAN}Banner:{Fore.RESET} {banner_url}")
    
    print(f"\n{Fore.GREEN}=== END OF INFORMATION ==={Fore.RESET}")

def main():
    clear_screen()
    print(logo)
    
    
    user_id = input(f"{Fore.YELLOW}Enter Discord account ID: {Fore.RESET}").strip()
    
    if not user_id:
        print(f"{Fore.RED}[!] No ID provided.{Fore.RESET}")
        return
    
    print(f"{Fore.CYAN}[~] Searching for information for ID: {user_id}...{Fore.RESET}")
    
    
    data = get_user_info(user_id)
    
    if data and "error" not in data:
        display_user_info(data)
    else:
        error_msg = data.get("error", "User not found or invalid ID") if data else "Unknown error"
        print(f"{Fore.RED}[!] {error_msg}{Fore.RESET}")
        print(f"{Fore.YELLOW}Check that the ID is correct and try again.{Fore.RESET}")

if __name__ == "__main__":
    main()