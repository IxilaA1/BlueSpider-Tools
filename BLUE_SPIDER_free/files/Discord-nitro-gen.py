

try:
    import random
    import string
    import json
    import requests
    import threading
    import time
    import os
    from datetime import datetime
except Exception as e:
    print(f"Error importing modules: {e}")
    exit()

            
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


class Config:
    
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    RESET = '\033[0m'
    
    
    BEFORE = BLUE
    AFTER = BLUE
    BEFORE_GREEN = GREEN
    AFTER_GREEN = GREEN
    INPUT = YELLOW
    GEN_VALID = GREEN
    GEN_INVALID = RED


color_webhook = 3066993
username_webhook = "Nitro Generator"
avatar_webhook = "https://cdn.discordapp.com/attachments/1188169139748126830/1188169140385673327/discord-avatar-512-YT0PN.png"


discord_banner = """
                   .ed$$$$$$e.
                 .$$$$$$$$$$$$c
                .$$$$$$$$$$$$$$$
                d$$$$$$$$$$$$$$$
                $$$$$$$$$$$$$$$$
                $$$$$$$$$$$$$$$$
                $$$$$$$$$$$$$$$$
                '$$$$$$$$$$$$$$'
                 '$$$$$$$$$$$$'
                   '*$$$$$$$*'
                      '*$$*'
"""


def current_time_hour():
    return datetime.now().strftime("%H:%M:%S")

def Slow(text):
    for line in text.split('\n'):
        print(line)
        time.sleep(0.1)

def ErrorModule(e):
    print(f"{Config.RED}Error importing modules: {e}{Config.RESET}")
    exit()

def ErrorNumber():
    print(f"{Config.RED}Error: Please enter a valid number{Config.RESET}")
    exit()

def Error(e):
    print(f"{Config.RED}Error: {e}{Config.RESET}")
    exit()

def CheckWebhook(webhook_url):
    try:
        response = requests.get(webhook_url)
        if response.status_code != 200:
            print(f"{Config.RED}Error: Invalid webhook URL{Config.RESET}")
            return False
        return True
    except:
        print(f"{Config.RED}Error: Invalid webhook URL{Config.RESET}")
        return False

def Title(title):
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"{Config.CYAN}{'='*50}{Config.RESET}")
    print(f"{Config.CYAN}{title:^50}{Config.RESET}")
    print(f"{Config.CYAN}{'='*50}{Config.RESET}")


def main():
    Title("Discord Nitro Generator")
    
    try:
        Slow(discord_banner)
        webhook = input(f"{Config.BEFORE + current_time_hour() + Config.AFTER} {Config.INPUT} Webhook ? (y/n) -> {Config.RESET}")
        webhook_url = None
        if webhook.lower() in ['y', 'yes']:
            webhook_url = input(f"{Config.BEFORE + current_time_hour() + Config.AFTER} {Config.INPUT} Webhook Url -> {Config.RESET}")
            if not CheckWebhook(webhook_url):
                return

        try:
            threads_number = int(input(f"{Config.BEFORE + current_time_hour() + Config.AFTER} {Config.INPUT} Threads Number -> {Config.RESET}"))
        except:
            ErrorNumber()

        def send_webhook(url_nitro):
            payload = {
                'embeds': [{
                    'title': 'Nitro Valid !',
                    'description': f"**Nitro:**\n```{url_nitro}```",
                    'color': color_webhook,
                    'footer': {
                        "text": username_webhook,
                        "icon_url": avatar_webhook,
                    }
                }],
                'username': username_webhook,
                'avatar_url': avatar_webhook
            }

            headers = {
                'Content-Type': 'application/json'
            }

            try:
                requests.post(webhook_url, data=json.dumps(payload), headers=headers, timeout=5)
            except:
                pass

        def nitro_check():
            code_nitro = ''.join([random.choice(string.ascii_uppercase + string.digits) for _ in range(16)])
            url_nitro = f'https://discord.gift/{code_nitro}'
            try:
                response = requests.get(f'https://discordapp.com/api/v6/entitlements/gift-codes/{code_nitro}?with_application=false&with_subscription_plan=true', timeout=5)
                if response.status_code == 200:
                    if webhook_url:
                        send_webhook(url_nitro)
                    print(f"{Config.BEFORE_GREEN + current_time_hour() + Config.AFTER_GREEN} {Config.GEN_VALID} Status:  {Config.WHITE}Valid{Config.GREEN}  Nitro: {Config.WHITE}{url_nitro}{Config.RESET}")
                else:
                    print(f"{Config.BEFORE + current_time_hour() + Config.AFTER} {Config.GEN_INVALID} Status: {Config.WHITE}Invalid{Config.RED} Nitro: {Config.WHITE}{url_nitro}{Config.RESET}")
            except requests.RequestException:
                print(f"{Config.BEFORE + current_time_hour() + Config.AFTER} {Config.GEN_INVALID} Status: {Config.WHITE}Error{Config.RED}   Nitro: {Config.WHITE}{url_nitro}{Config.RESET}")
        
        def request():
            threads = []
            try:
                for _ in range(int(threads_number)):
                    t = threading.Thread(target=nitro_check)
                    t.daemon = True
                    t.start()
                    threads.append(t)
            except:
                ErrorNumber()

            for thread in threads:
                thread.join()

        while True:
            request()

    except KeyboardInterrupt:
        print(f"\n{Config.YELLOW}Script interrupted by user.{Config.RESET}")
    except Exception as e:
        Error(e)

if __name__ == "__main__":
    main()