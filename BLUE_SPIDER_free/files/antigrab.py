# (c) 2026 IxilaA1 - Tous droits réservés / All rights reserved / Todos los derechos reservados.
# Ce code ne peut être ni vendu, ni modifié, ni partagé sans autorisation, ni publié à votre nom.
# This code may not be sold, modified, or shared without authorization, nor published under your name.
# Este código no puede ser vendido, modificado ni compartido sin autorización, ni publicado a su nombre.
# -------------------------------------------------------------------------------------------------------
import os
import sys
import time
import ctypes
from colorama import Fore, Style, init
import msvcrt
from typing import List

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

init(autoreset=True)

class AntiGrabber:
    def __init__(self):
        self.locked_files: List[tuple] = []  # Stocke (handle, path)
        
    def print_blue(self, text: str):
        """Affiche du texte en bleu ciel"""
        print(Fore.LIGHTCYAN_EX + text + Style.RESET_ALL)

    def is_admin(self) -> bool:
        """Vérifie si le programme a les droits admin"""
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False

    def relaunch_as_admin(self):
        """Relance le programme avec les droits admin"""
        try:
            params = ' '.join([f'"{arg}"' for arg in sys.argv])
            ctypes.windll.shell32.ShellExecuteW(
                None, 'runas', sys.executable, params, None, 1
            )
            sys.exit(0)
        except Exception as e:
            self.print_blue(f"[!] Erreur lors du relancement admin: {e}")
            sys.exit(1)

    def lock_file(self, path: str) -> bool:
        """Tente de verrouiller un fichier"""
        try:
            if not os.path.exists(path):
                return False
                
            f = open(path, 'rb')
            msvcrt.locking(f.fileno(), msvcrt.LK_NBLCK, os.path.getsize(path))
            self.locked_files.append((f, path))
            return True
        except (OSError, IOError):
            return False

    def unlock_all_files(self):
        """Libère tous les fichiers verrouillés"""
        for f, path in self.locked_files:
            try:
                f.close()
            except:
                pass
        self.locked_files.clear()

    def protect_discord(self):
        """Protège les fichiers Discord"""
        base = os.getenv('APPDATA')
        if not base:
            return
            
        leveldb = os.path.join(base, 'discord', 'Local Storage', 'leveldb')
        if os.path.exists(leveldb):
            count = 0
            for file in os.listdir(leveldb):
                if file.endswith(('.ldb', '.log')):
                    if self.lock_file(os.path.join(leveldb, file)):
                        count += 1
            self.print_blue(f"[+] Anti-Grabb Discord activé ({count} fichiers)")

    def protect_telegram(self):
        """Protège les fichiers Telegram"""
        base = os.getenv('APPDATA')
        if not base:
            return
            
        tdata = os.path.join(base, 'Telegram Desktop', 'tdata')
        if os.path.exists(tdata):
            count = 0
            for root, _, files in os.walk(tdata):
                for f in files:
                    if self.lock_file(os.path.join(root, f)):
                        count += 1
            self.print_blue(f"[+] Anti-Grabb Telegram activé ({count} fichiers)")

    def protect_browsers(self):
        """Protège les fichiers des navigateurs"""
        localappdata = os.getenv('LOCALAPPDATA', '')
        
        browsers = {
            'Chrome': os.path.join(localappdata, 'Google', 'Chrome', 'User Data', 'Default'),
            'Edge': os.path.join(localappdata, 'Microsoft', 'Edge', 'User Data', 'Default'),
            'Brave': os.path.join(localappdata, 'BraveSoftware', 'Brave-Browser', 'User Data', 'Default')
        }
        
        targets = ['Login Data', 'History', 'Cookies', 'Web Data']
        total_locked = 0
        
        for browser_name, path in browsers.items():
            if os.path.exists(path):
                browser_count = 0
                for target in targets:
                    full_path = os.path.join(path, target)
                    if self.lock_file(full_path):
                        browser_count += 1
                        total_locked += 1
                if browser_count > 0:
                    self.print_blue(f"[+] {browser_name}: {browser_count} fichiers protégés")
        
        if total_locked > 0:
            self.print_blue(f"[+] Anti-Grabb Navigateurs activé ({total_locked} fichiers)")

    def show_menu(self):
        """Affiche le menu"""
        self.print_blue("\n╔════════════════════════════════╗")
        self.print_blue("║     ANTI-GRABB TOOL v2.0      ║")
        self.print_blue("╠════════════════════════════════╣")
        self.print_blue("║  [1] Anti-Grabb Discord       ║")
        self.print_blue("║  [2] Anti-Grabb Telegram      ║")
        self.print_blue("║  [3] Anti-Grabb Navigateurs   ║")
        self.print_blue("║  [4] Anti-Grabb TOUT          ║")
        self.print_blue("║  [0] Quitter                  ║")
        self.print_blue("╚════════════════════════════════╝")
        
        try:
            return input(Fore.LIGHTCYAN_EX + "\nSélectionnez une option: ").strip()
        except:
            return "0"

    def run(self):
        """Fonction principale"""
        try:
            # Vérification admin
            if not self.is_admin():
                self.print_blue("[*] Droits administrateur requis, relancement...")
                self.relaunch_as_admin()
                return

            # Nettoyage de l'écran
            os.system('cls' if os.name == 'nt' else 'clear')
            
            # Menu
            choice = self.show_menu()
            
            # Traitement du choix
            if choice == '1':
                self.protect_discord()
            elif choice == '2':
                self.protect_telegram()
            elif choice == '3':
                self.protect_browsers()
            elif choice == '4':
                self.protect_discord()
                self.protect_telegram()
                self.protect_browsers()
                self.print_blue("[+] ANTI-GRABB TOUT ACTIVÉ")
            elif choice == '0':
                self.print_blue("[+] Au revoir!")
                return
            else:
                self.print_blue("[!] Option invalide")
                time.sleep(1.5)
                return

            # Message de confirmation
            self.print_blue("\n[+] Anti-Grabb actif - Fermez l'outil pour restaurer le système")
            self.print_blue("[+] Appuyez sur Ctrl+C pour arrêter")
            
            # Boucle principale
            while True:
                time.sleep(1)
                
        except KeyboardInterrupt:
            self.print_blue("\n[+] Arrêt demandé...")
        except Exception as e:
            self.print_blue(f"[!] Erreur inattendue: {e}")
        finally:
            # Nettoyage
            self.unlock_all_files()
            self.print_blue("[+] Anti-Grabb désactivé, système restauré")
            time.sleep(1.5)

def main():
    """Point d'entrée"""
    grabber = AntiGrabber()
    grabber.run()

if __name__ == "__main__":
    main()