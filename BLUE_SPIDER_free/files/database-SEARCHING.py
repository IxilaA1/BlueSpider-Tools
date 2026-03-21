# (c) 2026 IxilaA1 - Tous droits réservés / All rights reserved / Todos los derechos reservados.
# Ce code ne peut être ni vendu, ni modifié, ni partagé sans autorisation, ni publié à votre nom.
# This code may not be sold, modified, or shared without authorization, nor published under your name.
# Este código no puede ser vendido, modificado ni compartido sin autorización, ni publicado a su nombre.
# -------------------------------------------------------------------------------------------------------
import os
import sys
from datetime import datetime
import tkinter as tk
from tkinter import filedialog

class color:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    RESET = '\033[0m'

red = color.RED
green = color.GREEN
yellow = color.YELLOW
blue = color.BLUE
magenta = color.MAGENTA
cyan = color.CYAN
white = color.WHITE
reset = color.RESET
BEFORE = f"{red}["
AFTER = f"{red}]"
INPUT = f"{green}[INPUT]{reset}"
INFO = f"{cyan}[INFO]{reset}"
ERROR = f"{red}[ERROR]{reset}"
WAIT = f"{yellow}[WAIT]{reset}"

def current_time_hour():
    return datetime.now().strftime("%H:%M:%S")

def Title(text):
    if sys.platform.startswith("win"):
        os.system(f"title {text}")
    print(f"{red}[{white}{text}{red}]{reset}")

def Error(error):
    print(f"{BEFORE}{current_time_hour()}{AFTER} {ERROR} {error}")
    Continue()
    Reset()

def ErrorModule(error):
    print(f"{BEFORE}{current_time_hour()}{AFTER} {ERROR} Module error: {error}")
    Continue()
    Reset()

def Continue():
    input(f"{BEFORE}{current_time_hour()}{AFTER} {INPUT} Press Enter to continue...")

def Reset():
    os.system("cls" if sys.platform.startswith("win") else "clear")
    sys.exit()

try:
    Title("Search DataBase")

    def ChooseFolder():
        try:
            print(f"\n{BEFORE + current_time_hour() + AFTER} {INPUT} Enter database folder path -> {reset}")
            if sys.platform.startswith("win"):
                root = tk.Tk()
                root.withdraw()
                root.attributes('-topmost', True)
                folder_database = filedialog.askdirectory(parent=root, title="Search DataBase - Choose a folder")
            else:
                folder_database = filedialog.askdirectory(title="Search DataBase - Choose a folder")
            
            if not folder_database:
                folder_database = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Enter database folder path manually -> {reset}")
            
            print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Folder path: {white}{folder_database}{reset}")
        except:
            folder_database = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Enter database folder path -> {reset}")

        return folder_database

    folder_database = ChooseFolder()
    
    if not os.path.exists(folder_database):
        print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Folder does not exist!")
        Continue()
        Reset()
    
    search = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Search term -> {reset}")

    if not search:
        print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Search term cannot be empty!")
        Continue()
        Reset()

    print(f"{BEFORE + current_time_hour() + AFTER} {WAIT} Searching in database...")

    def TitleSearch(files_searched, element):
        Title(f"Search DataBase - Files: {files_searched} - Current: {element}")

    try:
        files_searched = 0
        results_found = False
        
        def SearchInFolder(folder):
            global files_searched, results_found
            try:
                folder = os.path.join(folder)
                print(f"{BEFORE + current_time_hour() + AFTER} {WAIT} Searching in {white}{folder}{reset}")
                
                for element in os.listdir(folder):
                    element_path = os.path.join(folder, element)
                    
                    if os.path.isdir(element_path):
                        SearchInFolder(element_path)
                    elif os.path.isfile(element_path):
                        try:
                            
                            encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
                            file_read = False
                            
                            for encoding in encodings:
                                try:
                                    with open(element_path, 'r', encoding=encoding) as file:
                                        files_searched += 1
                                        TitleSearch(files_searched, element)
                                        line_number = 0
                                        
                                        for line in file:
                                            line_number += 1
                                            if search.lower() in line.lower():
                                                results_found = True
                                                line_info = line.strip().replace(search, f"{color.YELLOW}{search}{white}")
                                                print(f"""{red}
- Folder : {white}{folder}{red}
- File   : {white}{element}{red}
- Line   : {white}{line_number}{red}
- Result : {white}{line_info}{reset}
""")
                                        file_read = True
                                        break
                                except UnicodeDecodeError:
                                    continue
                            
                            if not file_read:
                                print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Cannot read file: {white}{element}{reset}")
                                
                        except Exception as e:
                            print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Error with file {white}{element}{reset}: {e}")
                            
            except PermissionError:
                print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Permission denied for folder: {white}{folder}{reset}")
            except Exception as e:
                print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Error accessing folder: {e}")

        SearchInFolder(folder_database)
        
        if not results_found:
            print(f"{BEFORE + current_time_hour() + AFTER} {INFO} No results found for \"{white}{search}{reset}\".")
        else:
            print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Search completed!")

        print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Total files searched: {white}{files_searched}{reset}")

    except Exception as e:
        print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Error during search: {white}{e}{reset}")

    Continue()
    Reset()
    
except Exception as e:
    Error(e)