
"""
DNS Jumper - Terminal Edition
A command-line DNS management tool for Windows/Linux/macOS
"""

import subprocess
import sys
import os
import platform
import socket
import time
import struct


class Colors:
    RESET = '\033[0m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'

        
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


os.system('cls' if os.name == 'nt' else 'clear')


print(logo_ascii)


time.sleep(2)



DNS_SERVERS = {
    "1": {"name": "Google DNS", "primary": "8.8.8.8", "secondary": "8.8.4.4"},
    "2": {"name": "Cloudflare DNS", "primary": "1.1.1.1", "secondary": "1.0.0.1"},
    "3": {"name": "OpenDNS", "primary": "208.67.222.222", "secondary": "208.67.220.220"},
    "4": {"name": "Quad9 DNS", "primary": "9.9.9.9", "secondary": "149.112.112.112"},
    "5": {"name": "Comodo Secure DNS", "primary": "8.26.56.26", "secondary": "8.20.247.20"},
    "6": {"name": "AdGuard DNS", "primary": "94.140.14.14", "secondary": "94.140.15.15"},
    "7": {"name": "CleanBrowsing DNS", "primary": "185.228.168.9", "secondary": "185.228.169.9"},
    "8": {"name": "Alternate DNS", "primary": "76.76.19.19", "secondary": "76.223.122.150"},
    "9": {"name": "DNS.Watch", "primary": "84.200.69.80", "secondary": "84.200.70.40"},
    "10": {"name": "Verisign DNS", "primary": "64.6.64.6", "secondary": "64.6.65.6"},
    "11": {"name": "Level3 DNS", "primary": "209.244.0.3", "secondary": "209.244.0.4"},
    "12": {"name": "Norton ConnectSafe", "primary": "199.85.126.10", "secondary": "199.85.127.10"},
    "13": {"name": "GreenTeam DNS", "primary": "81.218.119.11", "secondary": "209.88.198.133"},
    "14": {"name": "SafeDNS", "primary": "195.46.39.39", "secondary": "195.46.39.40"},
    "15": {"name": "Dyn DNS", "primary": "216.146.35.35", "secondary": "216.146.36.36"},
    "16": {"name": "FreeDNS", "primary": "45.33.32.156", "secondary": "172.104.237.57"},
    "17": {"name": "Yandex DNS", "primary": "77.88.8.8", "secondary": "77.88.8.1"},
    "18": {"name": "UncensoredDNS", "primary": "91.239.100.100", "secondary": "89.233.43.71"},
    "19": {"name": "Hurricane Electric", "primary": "74.82.42.42", "secondary": "74.82.42.42"},
    "20": {"name": "puntCAT DNS", "primary": "109.69.8.51", "secondary": "109.69.8.51"},
}

def clear_screen():
    os.system('cls' if platform.system() == 'Windows' else 'clear')

def print_banner():
    banner = f"""
{Colors.CYAN}{Colors.BOLD}
  ____  _   _ ____       _ _   _ __  __ ____  _____ ____  
 |  _ \\| \\ | / ___|     | | | | |  \\/  |  _ \\| ____|  _ \\ 
 | | | |  \\| \\___ \\ _   | | | | | |\\/| | |_) |  _| | |_) |
 | |_| | |\\  |___) | |__| | |_| | |  | |  __/| |___|  _ < 
 |____/|_| \\_|____/ \\____/ \\___/|_|  |_|_|   |_____|_| \\_\\
                                                          
{Colors.RESET}{Colors.YELLOW}            Terminal Edition v1.0{Colors.RESET}
{Colors.WHITE}     Fast DNS Changer for Windows/Linux/macOS{Colors.RESET}
"""
    print(banner)

def print_separator():
    print(f"{Colors.BLUE}{'='*60}{Colors.RESET}")

def get_os_type():
    return platform.system()

def get_network_interfaces():
    """Get list of network interfaces"""
    interfaces = []
    os_type = get_os_type()
    
    try:
        if os_type == "Windows":
            result = subprocess.run(
                ['netsh', 'interface', 'show', 'interface'],
                capture_output=True, text=True, encoding='utf-8', errors='ignore'
            )
            lines = result.stdout.strip().split('\n')[3:]
            for line in lines:
                parts = line.split()
                if len(parts) >= 4:
                    name = ' '.join(parts[3:])
                    state = parts[1]
                    interfaces.append({"name": name, "state": state})
        
        elif os_type == "Linux":
            result = subprocess.run(['ip', 'link', 'show'], capture_output=True, text=True)
            lines = result.stdout.strip().split('\n')
            for line in lines:
                if ': ' in line and not line.startswith(' '):
                    parts = line.split(': ')
                    if len(parts) >= 2:
                        name = parts[1].split('@')[0]
                        if name != 'lo':
                            interfaces.append({"name": name, "state": "Unknown"})
        
        elif os_type == "Darwin":
            result = subprocess.run(['networksetup', '-listallnetworkservices'], capture_output=True, text=True)
            lines = result.stdout.strip().split('\n')[1:]
            for line in lines:
                if line and not line.startswith('*'):
                    interfaces.append({"name": line.strip(), "state": "Unknown"})
    except Exception as e:
        print(f"{Colors.RED}Error getting interfaces: {e}{Colors.RESET}")
    
    return interfaces

def get_current_dns(interface):
    """Get current DNS settings for an interface"""
    os_type = get_os_type()
    dns_servers = []
    
    try:
        if os_type == "Windows":
            result = subprocess.run(
                ['netsh', 'interface', 'ip', 'show', 'dns', interface],
                capture_output=True, text=True, encoding='utf-8', errors='ignore'
            )
            for line in result.stdout.split('\n'):
                line = line.strip()
                if 'Statically Configured DNS Servers' in line:
                    parts = line.split(':')
                    if len(parts) > 1 and parts[1].strip():
                        dns_servers.append(parts[1].strip())
                elif line and line[0].isdigit() and '.' in line:
                    dns_servers.append(line)
        
        elif os_type == "Linux":
            try:
                with open('/etc/resolv.conf', 'r') as f:
                    for line in f:
                        if line.startswith('nameserver'):
                            dns = line.split()[1]
                            dns_servers.append(dns)
            except:
                pass
        
        elif os_type == "Darwin":
            result = subprocess.run(
                ['networksetup', '-getdnsservers', interface],
                capture_output=True, text=True
            )
            for line in result.stdout.strip().split('\n'):
                if line and line[0].isdigit():
                    dns_servers.append(line)
    except Exception as e:
        print(f"{Colors.RED}Error getting DNS: {e}{Colors.RESET}")
    
    return dns_servers if dns_servers else ["DHCP (Automatic)"]

def set_dns(interface, primary, secondary=None):
    """Set DNS servers for an interface"""
    os_type = get_os_type()
    
    try:
        if os_type == "Windows":
            subprocess.run(
                ['netsh', 'interface', 'ip', 'set', 'dns', interface, 'static', primary],
                capture_output=True, check=True
            )
            if secondary:
                subprocess.run(
                    ['netsh', 'interface', 'ip', 'add', 'dns', interface, secondary, 'index=2'],
                    capture_output=True, check=True
                )
        
        elif os_type == "Linux":
            with open('/etc/resolv.conf', 'w') as f:
                f.write(f"nameserver {primary}\n")
                if secondary:
                    f.write(f"nameserver {secondary}\n")
        
        elif os_type == "Darwin":
            dns_cmd = [primary]
            if secondary:
                dns_cmd.append(secondary)
            subprocess.run(
                ['networksetup', '-setdnsservers', interface] + dns_cmd,
                capture_output=True, check=True
            )
        
        return True
    except Exception as e:
        print(f"{Colors.RED}Error setting DNS: {e}{Colors.RESET}")
        return False

def reset_dns_to_dhcp(interface):
    """Reset DNS to automatic (DHCP)"""
    os_type = get_os_type()
    
    try:
        if os_type == "Windows":
            subprocess.run(
                ['netsh', 'interface', 'ip', 'set', 'dns', interface, 'dhcp'],
                capture_output=True, check=True
            )
        
        elif os_type == "Linux":
            subprocess.run(['systemctl', 'restart', 'NetworkManager'], capture_output=True)
        
        elif os_type == "Darwin":
            subprocess.run(
                ['networksetup', '-setdnsservers', interface, 'Empty'],
                capture_output=True, check=True
            )
        
        return True
    except Exception as e:
        print(f"{Colors.RED}Error resetting DNS: {e}{Colors.RESET}")
        return False

def flush_dns():
    """Flush DNS cache"""
    os_type = get_os_type()
    
    try:
        if os_type == "Windows":
            subprocess.run(['ipconfig', '/flushdns'], capture_output=True, check=True)
        elif os_type == "Linux":
            subprocess.run(['systemd-resolve', '--flush-caches'], capture_output=True)
        elif os_type == "Darwin":
            subprocess.run(['dscacheutil', '-flushcache'], capture_output=True)
            subprocess.run(['killall', '-HUP', 'mDNSResponder'], capture_output=True)
        
        return True
    except:
        return False

def ping_dns(dns_ip, count=4):
    """Ping a DNS server and return average response time"""
    os_type = get_os_type()
    
    try:
        if os_type == "Windows":
            result = subprocess.run(
                ['ping', '-n', str(count), dns_ip],
                capture_output=True, text=True, timeout=10
            )
            for line in result.stdout.split('\n'):
                if 'Average' in line or 'Moyenne' in line:
                    parts = line.split('=')
                    if len(parts) > 1:
                        return parts[-1].strip().replace('ms', '').strip()
        else:
            result = subprocess.run(
                ['ping', '-c', str(count), dns_ip],
                capture_output=True, text=True, timeout=10
            )
            for line in result.stdout.split('\n'):
                if 'avg' in line:
                    parts = line.split('/')
                    if len(parts) >= 5:
                        return parts[4]
        
        return "N/A"
    except:
        return "Timeout"

def dns_benchmark():
    """Benchmark all DNS servers"""
    print(f"\n{Colors.YELLOW}Running DNS Benchmark...{Colors.RESET}")
    print(f"{Colors.CYAN}Testing response times for all DNS servers{Colors.RESET}\n")
    
    results = []
    
    for key, dns in DNS_SERVERS.items():
        print(f"  Testing {dns['name']}...", end='', flush=True)
        response_time = ping_dns(dns['primary'], 2)
        results.append({
            "name": dns['name'],
            "ip": dns['primary'],
            "time": response_time
        })
        print(f" {Colors.GREEN}{response_time} ms{Colors.RESET}")
    
    print(f"\n{Colors.YELLOW}Benchmark Results (Sorted by Speed):{Colors.RESET}")
    print_separator()
    
    def sort_key(x):
        try:
            return float(x['time'])
        except:
            return 9999
    
    results.sort(key=sort_key)
    
    for i, r in enumerate(results, 1):
        color = Colors.GREEN if i <= 3 else Colors.WHITE
        print(f"  {color}{i:2}. {r['name']:<25} {r['ip']:<18} {r['time']} ms{Colors.RESET}")
    
    input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.RESET}")

def dns_lookup(domain):
    """Perform DNS lookup for a domain"""
    try:
        ip = socket.gethostbyname(domain)
        return ip
    except:
        return None

def show_dns_list():
    """Display available DNS servers"""
    print(f"\n{Colors.YELLOW}Available DNS Servers:{Colors.RESET}")
    print_separator()
    
    for key, dns in DNS_SERVERS.items():
        print(f"  {Colors.CYAN}{key:>2}{Colors.RESET}. {Colors.WHITE}{dns['name']:<22}{Colors.RESET} "
              f"{Colors.GREEN}Primary: {dns['primary']:<15}{Colors.RESET} "
              f"{Colors.BLUE}Secondary: {dns['secondary']}{Colors.RESET}")
    
    print_separator()

def select_interface(interfaces):
    """Let user select a network interface"""
    print(f"\n{Colors.YELLOW}Available Network Interfaces:{Colors.RESET}")
    print_separator()
    
    for i, iface in enumerate(interfaces, 1):
        state_color = Colors.GREEN if iface['state'] in ['Connected', 'Up'] else Colors.RED
        print(f"  {Colors.CYAN}{i}{Colors.RESET}. {Colors.WHITE}{iface['name']:<30}{Colors.RESET} "
              f"[{state_color}{iface['state']}{Colors.RESET}]")
    
    print_separator()
    
    while True:
        try:
            choice = input(f"{Colors.YELLOW}Select interface (1-{len(interfaces)}): {Colors.RESET}")
            idx = int(choice) - 1
            if 0 <= idx < len(interfaces):
                return interfaces[idx]['name']
        except ValueError:
            pass
        print(f"{Colors.RED}Invalid selection. Please try again.{Colors.RESET}")

def apply_dns_menu(interfaces):
    """Menu for applying DNS settings"""
    clear_screen()
    print_banner()
    
    interface = select_interface(interfaces)
    
    current_dns = get_current_dns(interface)
    print(f"\n{Colors.MAGENTA}Current DNS for {interface}: {', '.join(current_dns)}{Colors.RESET}")
    
    show_dns_list()
    
    print(f"  {Colors.CYAN} 0{Colors.RESET}. {Colors.WHITE}Custom DNS{Colors.RESET}")
    print(f"  {Colors.CYAN}99{Colors.RESET}. {Colors.WHITE}Reset to DHCP (Automatic){Colors.RESET}")
    
    choice = input(f"\n{Colors.YELLOW}Select DNS server (0-20, 99): {Colors.RESET}")
    
    if choice == "99":
        print(f"\n{Colors.YELLOW}Resetting DNS to DHCP...{Colors.RESET}")
        if reset_dns_to_dhcp(interface):
            print(f"{Colors.GREEN}DNS reset to DHCP successfully!{Colors.RESET}")
        else:
            print(f"{Colors.RED}Failed to reset DNS.{Colors.RESET}")
    
    elif choice == "0":
        primary = input(f"{Colors.YELLOW}Enter Primary DNS: {Colors.RESET}")
        secondary = input(f"{Colors.YELLOW}Enter Secondary DNS (or press Enter to skip): {Colors.RESET}")
        
        print(f"\n{Colors.YELLOW}Applying custom DNS...{Colors.RESET}")
        if set_dns(interface, primary, secondary if secondary else None):
            print(f"{Colors.GREEN}Custom DNS applied successfully!{Colors.RESET}")
        else:
            print(f"{Colors.RED}Failed to apply DNS.{Colors.RESET}")
    
    elif choice in DNS_SERVERS:
        dns = DNS_SERVERS[choice]
        print(f"\n{Colors.YELLOW}Applying {dns['name']}...{Colors.RESET}")
        if set_dns(interface, dns['primary'], dns['secondary']):
            print(f"{Colors.GREEN}{dns['name']} applied successfully!{Colors.RESET}")
            print(f"  {Colors.WHITE}Primary:   {dns['primary']}{Colors.RESET}")
            print(f"  {Colors.WHITE}Secondary: {dns['secondary']}{Colors.RESET}")
        else:
            print(f"{Colors.RED}Failed to apply DNS. Make sure you run as Administrator/root.{Colors.RESET}")
    
    else:
        print(f"{Colors.RED}Invalid selection.{Colors.RESET}")
    
    input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.RESET}")

def show_current_dns_menu(interfaces):
    """Show current DNS settings"""
    clear_screen()
    print_banner()
    
    print(f"\n{Colors.YELLOW}Current DNS Settings:{Colors.RESET}")
    print_separator()
    
    for iface in interfaces:
        dns_servers = get_current_dns(iface['name'])
        print(f"\n  {Colors.CYAN}{iface['name']}{Colors.RESET}")
        for i, dns in enumerate(dns_servers):
            label = "Primary" if i == 0 else "Secondary" if i == 1 else f"DNS {i+1}"
            print(f"    {Colors.WHITE}{label}: {Colors.GREEN}{dns}{Colors.RESET}")
    
    print_separator()
    input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.RESET}")

def dns_tools_menu():
    """DNS Tools submenu"""
    while True:
        clear_screen()
        print_banner()
        
        print(f"\n{Colors.YELLOW}DNS Tools:{Colors.RESET}")
        print_separator()
        print(f"  {Colors.CYAN}1{Colors.RESET}. {Colors.WHITE}Flush DNS Cache{Colors.RESET}")
        print(f"  {Colors.CYAN}2{Colors.RESET}. {Colors.WHITE}DNS Lookup{Colors.RESET}")
        print(f"  {Colors.CYAN}3{Colors.RESET}. {Colors.WHITE}Ping DNS Server{Colors.RESET}")
        print(f"  {Colors.CYAN}4{Colors.RESET}. {Colors.WHITE}DNS Benchmark (Test All){Colors.RESET}")
        print(f"  {Colors.CYAN}0{Colors.RESET}. {Colors.WHITE}Back to Main Menu{Colors.RESET}")
        print_separator()
        
        choice = input(f"{Colors.YELLOW}Select option: {Colors.RESET}")
        
        if choice == "1":
            print(f"\n{Colors.YELLOW}Flushing DNS cache...{Colors.RESET}")
            if flush_dns():
                print(f"{Colors.GREEN}DNS cache flushed successfully!{Colors.RESET}")
            else:
                print(f"{Colors.RED}Failed to flush DNS cache.{Colors.RESET}")
            input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.RESET}")
        
        elif choice == "2":
            domain = input(f"\n{Colors.YELLOW}Enter domain name: {Colors.RESET}")
            ip = dns_lookup(domain)
            if ip:
                print(f"{Colors.GREEN}{domain} resolves to: {ip}{Colors.RESET}")
            else:
                print(f"{Colors.RED}Could not resolve {domain}{Colors.RESET}")
            input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.RESET}")
        
        elif choice == "3":
            show_dns_list()
            dns_choice = input(f"{Colors.YELLOW}Select DNS to ping (1-20) or enter IP: {Colors.RESET}")
            
            if dns_choice in DNS_SERVERS:
                ip = DNS_SERVERS[dns_choice]['primary']
                name = DNS_SERVERS[dns_choice]['name']
            else:
                ip = dns_choice
                name = dns_choice
            
            print(f"\n{Colors.YELLOW}Pinging {name} ({ip})...{Colors.RESET}")
            response = ping_dns(ip, 4)
            print(f"{Colors.GREEN}Average response time: {response} ms{Colors.RESET}")
            input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.RESET}")
        
        elif choice == "4":
            dns_benchmark()
        
        elif choice == "0":
            break

def main_menu():
    """Main menu loop"""
    
    if platform.system() == "Windows":
        os.system('color')
    
    interfaces = get_network_interfaces()
    
    if not interfaces:
        print(f"{Colors.RED}No network interfaces found!{Colors.RESET}")
        return
    
    while True:
        clear_screen()
        print_banner()
        
        print(f"\n{Colors.YELLOW}Main Menu:{Colors.RESET}")
        print_separator()
        print(f"  {Colors.CYAN}1{Colors.RESET}. {Colors.WHITE}Apply DNS Server{Colors.RESET}")
        print(f"  {Colors.CYAN}2{Colors.RESET}. {Colors.WHITE}View Current DNS Settings{Colors.RESET}")
        print(f"  {Colors.CYAN}3{Colors.RESET}. {Colors.WHITE}DNS Tools{Colors.RESET}")
        print(f"  {Colors.CYAN}4{Colors.RESET}. {Colors.WHITE}View DNS Server List{Colors.RESET}")
        print(f"  {Colors.CYAN}5{Colors.RESET}. {Colors.WHITE}Quick Apply (Google DNS){Colors.RESET}")
        print(f"  {Colors.CYAN}6{Colors.RESET}. {Colors.WHITE}Quick Apply (Cloudflare DNS){Colors.RESET}")
        print(f"  {Colors.CYAN}0{Colors.RESET}. {Colors.WHITE}Exit{Colors.RESET}")
        print_separator()
        
        print(f"  {Colors.MAGENTA}System: {get_os_type()}{Colors.RESET}")
        print(f"  {Colors.MAGENTA}Interfaces found: {len(interfaces)}{Colors.RESET}")
        
        choice = input(f"\n{Colors.YELLOW}Select option: {Colors.RESET}")
        
        if choice == "1":
            apply_dns_menu(interfaces)
        
        elif choice == "2":
            show_current_dns_menu(interfaces)
        
        elif choice == "3":
            dns_tools_menu()
        
        elif choice == "4":
            clear_screen()
            print_banner()
            show_dns_list()
            input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.RESET}")
        
        elif choice == "5":
            interface = select_interface(interfaces)
            print(f"\n{Colors.YELLOW}Applying Google DNS...{Colors.RESET}")
            if set_dns(interface, "8.8.8.8", "8.8.4.4"):
                print(f"{Colors.GREEN}Google DNS applied successfully!{Colors.RESET}")
            else:
                print(f"{Colors.RED}Failed. Run as Administrator/root.{Colors.RESET}")
            input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.RESET}")
        
        elif choice == "6":
            interface = select_interface(interfaces)
            print(f"\n{Colors.YELLOW}Applying Cloudflare DNS...{Colors.RESET}")
            if set_dns(interface, "1.1.1.1", "1.0.0.1"):
                print(f"{Colors.GREEN}Cloudflare DNS applied successfully!{Colors.RESET}")
            else:
                print(f"{Colors.RED}Failed. Run as Administrator/root.{Colors.RESET}")
            input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.RESET}")
        
        elif choice == "0":
            clear_screen()
            print(f"\n{Colors.CYAN}Thank you for using DNS Jumper!{Colors.RESET}")
            print(f"{Colors.YELLOW}Goodbye!{Colors.RESET}\n")
            break

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Program interrupted. Goodbye!{Colors.RESET}")
        sys.exit(0)