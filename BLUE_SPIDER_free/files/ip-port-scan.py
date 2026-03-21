# (c) 2026 IxilaA1 - Tous droits réservés / All rights reserved / Todos los derechos reservados.
# Ce code ne peut être ni vendu, ni modifié, ni partagé sans autorisation, ni publié à votre nom.
# This code may not be sold, modified, or shared without authorization, nor published under your name.
# Este código no puede ser vendido, modificado ni compartido sin autorización, ni publicado a su nombre.
# -------------------------------------------------------------------------------------------------------
import socket
import concurrent.futures
import time
from datetime import datetime

print("="*60)
print("SCAN DE PORTS PROFESSIONNEL v2.0")
print("="*60)

# Demande l'IP
ip = input("Adresse IP à scanner : ")

# Demande la plage de ports
print("\nOptions de scan :")
print("1 - Ports courants (1-1024) - Rapide")
print("2 - Tous les ports (1-65535) - Lent mais complet")
print("3 - Ports spécifiques (ex: 21,22,80,443)")
print("4 - Plage personnalisée")
choix = input("\nVotre choix (1-4) : ")

ports_a_scanner = []

if choix == "1":
    ports_a_scanner = range(1, 1025)
    print(f"Scan des ports 1-1024 sélectionné")
elif choix == "2":
    ports_a_scanner = range(1, 65536)
    print(f"Scan de TOUS les ports (1-65535) - Cela peut prendre du temps!")
elif choix == "3":
    ports_list = input("Entrez les ports (séparés par des virgules) : ")
    try:
        ports_a_scanner = [int(p.strip()) for p in ports_list.split(',')]
        print(f"Scan des ports: {ports_a_scanner}")
    except:
        print("Erreur de format, scan des ports 1-1024")
        ports_a_scanner = range(1, 1025)
elif choix == "4":
    plage = input("Entrez la plage (ex: 1000-2000) : ")
    try:
        debut, fin = map(int, plage.split('-'))
        ports_a_scanner = range(debut, fin + 1)
        print(f"Scan des ports {debut}-{fin}")
    except:
        print("Erreur de format, scan des ports 1-1024")
        ports_a_scanner = range(1, 1025)
else:
    ports_a_scanner = range(1, 1025)

# Demande le niveau de détail
print("\nNiveau de détail:")
print("1 - Normal (afficher seulement les ports ouverts)")
print("2 - Détaillé (afficher tout, lent)")
detail = input("Votre choix (1 ou 2) : ")

# Variables pour les résultats
ports_ouverts = []
start_time = time.time()
total_ports = len(ports_a_scanner)

print(f"\nDébut du scan de {ip}...")
print(f"Total de ports à scanner: {total_ports}")
print("-" * 60)

def scan_port(port):
    """Fonction de scan pour un port"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.3)
        result = sock.connect_ex((ip, port))
        
        if result == 0:
            # Essayer d'obtenir le nom du service
            try:
                service = socket.getservbyport(port)
            except:
                service = "inconnu"
            
            result_str = f"✓ Port {port:5} OUVERT | Service: {service}"
            
            # Tentative de banner grabbing basique
            if port in [21, 25, 80, 110, 143, 443, 8080, 22]:
                try:
                    if port in [80, 8080, 443]:
                        sock.send(b"HEAD / HTTP/1.0\r\n\r\n")
                    elif port == 21:
                        sock.send(b"HELP\r\n")
                    elif port == 22:
                        time.sleep(0.1)
                    elif port == 25:
                        sock.send(b"EHLO scan.local\r\n")
                    
                    banner = sock.recv(256).decode('utf-8', errors='ignore').strip()
                    if banner:
                        result_str += f"\n    └─ Banner: {banner[:80]}"
                except:
                    pass
            
            print(result_str)
            sock.close()
            return port
        else:
            if detail == "2":  # Mode détaillé
                print(f"✗ Port {port:5} FERMÉ")
        
        sock.close()
    except Exception as e:
        if detail == "2":
            print(f"! Port {port:5} ERREUR: {e}")
    
    return None

# Scan avec ThreadPoolExecutor
with concurrent.futures.ThreadPoolExecutor(max_workers=200) as executor:
    # Créer les futures
    futures = {executor.submit(scan_port, port): port for port in ports_a_scanner}
    
    # Attendre les résultats
    for future in concurrent.futures.as_completed(futures):
        result = future.result()
        if result:
            ports_ouverts.append(result)

# Calcul du temps
end_time = time.time()
scan_duration = end_time - start_time

# Résumé final
print("\n" + "="*60)
print("RÉSUMÉ DU SCAN")
print("="*60)
print(f"Cible: {ip}")
print(f"Ports scannés: {total_ports}")
print(f"Ports ouverts: {len(ports_ouverts)}")
print(f"Temps d'exécution: {scan_duration:.2f} secondes")

if ports_ouverts:
    print("\nPORTS OUVERTS (triés):")
    for port in sorted(ports_ouverts):
        try:
            service = socket.getservbyport(port)
        except:
            service = "inconnu"
        print(f"  • {port}/tcp - {service}")

# Sauvegarder dans un fichier
try:
    filename = f"scan_{ip}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(filename, 'w') as f:
        f.write(f"Scan de {ip}\n")
        f.write(f"Date: {datetime.now()}\n")
        f.write(f"Ports ouverts: {len(ports_ouverts)}\n\n")
        for port in sorted(ports_ouverts):
            try:
                service = socket.getservbyport(port)
            except:
                service = "inconnu"
            f.write(f"Port {port}: {service}\n")
    
    print(f"\nRésultats sauvegardés dans: {filename}")
except:
    pass

print("\n" + "="*60)
input("Appuyez sur Entrée pour quitter...")