import webbrowser
import time
import os 

    
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
    print(f"[ERREUR MODULE] {e}")

def Title(text):
    print(f"======== {text} ========")

def Slow(text):
    
    print(text)
    time.sleep(0.5)

def current_time_hour():
   
    return time.strftime("%H:%M")

def Censored(text):
    
    print(f"[CENSURE] Recherche '{text}' acceptée.")

def Reset():
    
    print("[RESET] Retour au menu principal (Sortie ici pour la simulation).")
    exit()

def ErrorChoice():
    
    print("[ERREUR CHOIX] Choix non valide.")

def Error(e):
    print(f"[ERREUR GLOBALE] Une erreur s'est produite : {e}")


dox_banner = "--- Dox Tracker v1.0 ---"
BEFORE = "["
AFTER = "]"
white = "" 
INPUT = ">>>"
reset = ""
color = type('obj', (object,), {'RESET' : ""})


try:
    Slow(f"""{dox_banner}
{BEFORE}00{AFTER} Retour
{BEFORE}01{AFTER}{white} Nom d'utilisateur
{BEFORE}02{AFTER}{white} Nom, Prénom
{BEFORE}03{AFTER}{white} Autre
    """)

    search_type = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Type de recherche -> {reset}")

    if search_type in ['00', '0']:
        Reset() 

    if search_type in ['01', '1']:
        search = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Nom d'utilisateur -> {reset}")
        Censored(search)
            
    elif search_type in ['02', '2']:
        name = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Nom de famille -> {reset}")
        first_name = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Prénom -> {reset}")
        Censored(name)
        Censored(first_name)
        
    elif search_type in ['03', '3']:
        search = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Recherche -> {reset}")
        Censored(search)
    else:
        ErrorChoice()

    
    if search_type in ['1', '01','2','02','3','03']:
        print(f"""
{BEFORE}00{AFTER} Retour
{BEFORE}01{AFTER}{white} Facebook.com
{BEFORE}02{AFTER}{white} Youtube.com
{BEFORE}03{AFTER}{white} Twitter.com
{BEFORE}04{AFTER}{white} Tiktok.com
{BEFORE}05{AFTER}{white} Peekyou.com
{BEFORE}06{AFTER}{white} Tumblr.com
{BEFORE}07{AFTER}{white} PagesJaunes.fr
        """)
        
        while True:
            
            if search_type in ['1', '01','2','02','3','03']:
                choice = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Site -> {color.RESET}")

                if choice in ['0', '00']:
                    break 

                
                base_url = ""
                query = ""
                
                
                if search_type in ['01', '1', '3', '03']:
                    
                    query = search
                elif search_type in ['02', '2']:
                    
                    if choice == '05' or choice == '5': 
                         query = f"{name}_{first_name}"
                    elif choice == '07' or choice == '7':
                        query = f"{name} {first_name}"
                    else: 
                        query = f"{name}%20{first_name}" 

                
                if choice in ['01', '1']:
                    base_url = "https://www.facebook.com/search/top/?init=quick&q="
                elif choice in ['02', '2']:
                    base_url = "https://www.youtube.com/results?search_query="
                elif choice in ['03', '3']:
                    base_url = "https://twitter.com/search?f=users&vertical=default&q="
                elif choice in ['04', '4']:
                    base_url = "https://www.tiktok.com/search?q="
                elif choice in ['05', '5']:
                    base_url = "https://www.peekyou.com/"
                elif choice in ['06', '6']:
                    base_url = "https://www.tumblr.com/search/"
                elif choice in ['07', '7']:
                    base_url = "https://www.pagesjaunes.fr/pagesblanches/recherche?quoiqui="
                
                
                if base_url:
                    full_url = f"{base_url}{query}"
                    print(f"Ouverture de : {full_url}")
                    webbrowser.open(full_url)
                else:
                    ErrorChoice() 

except Exception as e:
    Error(e)