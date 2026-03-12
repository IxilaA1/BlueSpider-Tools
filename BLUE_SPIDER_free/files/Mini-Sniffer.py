from scapy.all import sniff, IP, TCP, UDP, ARP, DNS, Ether
from collections import Counter
import sys
import time
import os
from datetime import datetime


GREEN = '\033[92m'
YELLOW = '\033[93m'
CYAN = '\033[96m'
BLUE = '\033[94m'
RED = '\033[91m'
MAGENTA = '\033[95m'
RESET = '\033[0m'

    
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



captured_packets = []
protocol_stats = Counter()
start_time = None
bytes_captured = 0



def get_protocol_info(packet):
    """Determines the main protocol, color, and summary information."""
    
    color = RESET
    protocol = "Other"
    info = ""
    
    if IP in packet:
        
        if TCP in packet:
            protocol = "TCP"
            color = GREEN
            flags = packet[TCP].sprintf('%TCP.flags%')
            info = f"SrcPort:{packet[TCP].sport} -> DstPort:{packet[TCP].dport} | Flags:{flags}"
            
            if packet[TCP].dport == 80 or packet[TCP].sport == 80:
                 protocol = "HTTP"
                 color = MAGENTA
            if packet[TCP].dport == 443 or packet[TCP].sport == 443:
                 protocol = "TLSv1.2"
                 color = MAGENTA
                 
        elif UDP in packet:
            protocol = "UDP"
            color = YELLOW
            info = f"SrcPort:{packet[UDP].sport} -> DstPort:{packet[UDP].dport}"
            
            
            if DNS in packet:
                protocol = "DNS"
                color = CYAN
                
                try:
                    qname = packet[DNS].qd.qname.decode().rstrip('.')
                except AttributeError:
                    qname = 'N/A'
                info = f"ID:{packet[DNS].id} | QName: {qname}"
                
        elif packet[IP].proto == 1:
            protocol = "ICMP"
            color = CYAN
            info = f"Type:{packet[IP].payload.type} | Code:{packet[IP].payload.code}"
            
        else:
            protocol = f"IP ({packet[IP].proto})"
            color = BLUE
            
    elif ARP in packet:
        protocol = "ARP"
        color = BLUE
        op = 'Request' if packet[ARP].op == 1 else 'Reply'
        info = f"{op}: Who has {packet[ARP].pdst}?"
        
    
    protocol_stats[protocol] += 1
    
    return protocol, color, info


def analyze_packet(packet):
    """Analyzes and displays captured packet details with coloring."""
    global bytes_captured
    
    protocol, color, info = get_protocol_info(packet)
    

    timestamp = datetime.now().strftime('%H:%M:%S.%f')[:-3]
    
    
    src = packet[Ether].src if Ether in packet else 'N/A'
    dst = packet[Ether].dst if Ether in packet else 'N/A'
    
    if IP in packet:
        src = packet[IP].src
        dst = packet[IP].dst
        
    length = len(packet)
    bytes_captured += length
    
    
    print(f"[{timestamp}] "
          f"{color}{protocol:10}{RESET} "
          f"{src:15} -> {dst:15} "
          f"| {length:5} Bytes | "
          f"{info}")

    
    captured_packets.append(packet)



def display_stats():
    """Calculates and displays current capture statistics."""
    
    if not start_time:
         print(f"\n{YELLOW}No capture data available. Please start a capture first.{RESET}")
         return

    elapsed = time.time() - start_time
    total_packets = sum(protocol_stats.values())
    
    if total_packets == 0:
        print(f"\n{YELLOW}No packets captured during the session.{RESET}")
        return
        
    rate = total_packets / elapsed if elapsed > 0 else 0
    avg_byte_rate = (bytes_captured / elapsed) / 1024 if elapsed > 0 else 0
    
    print("\n" + "="*60)
    print(f"{BLUE}--- Capture Statistics ---{RESET}")
    print(f"Total Packets: {total_packets}")
    print(f"Total Bytes:   {bytes_captured} ({bytes_captured / 1024 / 1024:.2f} MB)")
    print(f"Time Elapsed:  {elapsed:.2f} seconds")
    print(f"Packet Rate:   {rate:.2f} pkts/sec")
    print(f"Throughput:    {avg_byte_rate:.2f} KB/sec")
    
    print("\nProtocol Distribution:")
    for proto, count in protocol_stats.most_common():
        percentage = (count / total_packets) * 100
        print(f"  - {proto:10}: {count:5} ({percentage:.2f}%)")
        
    print("="*60)



def export_pcap(filename):
    """Exports all captured packets to a pcap file."""
    try:
        from scapy.all import wrpcap
        wrpcap(filename, captured_packets)
        print(f"\n{GREEN}*** Success: {len(captured_packets)} packets exported to '{filename}'. ***{RESET}")
    except Exception as e:
        print(f"\n{RED}*** Error exporting PCAP: {e} ***{RESET}")


def display_summary(filter_proto=""):
    """Displays a summary of captured packets, optionally filtered by protocol."""
    
    if not captured_packets:
        print(f"\n{YELLOW}No packets have been captured yet.{RESET}")
        return

    filtered_packets = []
    if filter_proto:
        for p in captured_packets:
            protocol, _, _ = get_protocol_info(p)
            if protocol.upper() == filter_proto.upper():
                filtered_packets.append(p)
    else:
        filtered_packets = captured_packets

    if not filtered_packets:
         print(f"\n{YELLOW}No packets found matching the filter: {filter_proto}.{RESET}")
         return

    print("\n" + "="*60)
    print(f"{BLUE}--- Captured Packet Summary (Showing {min(len(filtered_packets), 20)}/{len(captured_packets)}) ---{RESET}")
    for i, packet in enumerate(filtered_packets[:20]):
        protocol, color, info = get_protocol_info(packet)
        src = packet[IP].src if IP in packet else (packet[Ether].src if Ether in packet else 'N/A')
        dst = packet[IP].dst if IP in packet else (packet[Ether].dst if Ether in packet else 'N/A')
        
        print(f"{i+1:3}: [{color}{protocol:5}{RESET}] {src:15} -> {dst:15} | {len(packet)} Bytes")
    
    if len(filtered_packets) > 20:
        print("...")
        
    print("="*60)
    

def start_capture(bpf_filter, iface=None):
    """Starts packet capture with the specified BPF filter."""
    global captured_packets, protocol_stats, start_time, bytes_captured
    
    
    captured_packets = []
    protocol_stats = Counter()
    bytes_captured = 0
    start_time = time.time()
    
    print(f"\n{BLUE}--- Starting Capture (Filter: '{bpf_filter}') ---{RESET}")
    print(f"Press {YELLOW}Ctrl+C{RESET} to stop the capture and return to the menu.")
    print("--------------------------------------------------")
    
    try:

        sniff(prn=analyze_packet, filter=bpf_filter, store=False, iface=iface)
        
    except KeyboardInterrupt:
        print(f"\n{GREEN}*** Capture stopped by user (Ctrl+C). ***{RESET}")
        display_stats()
    except Exception as e:
        print(f"\n{RED}*** Capture Error: {e} ***{RESET}")


def display_menu():
    """Displays the interactive menu to the user."""
    print("\n" + "="*60)
    print("                Mini-Sniffer")
    print("="*60)
    print("--- Network Analysis ---")
    print(f"  {CYAN}1{RESET}. Start Capture (All IP Traffic)")
    print(f"  {CYAN}2{RESET}. Start Capture (TCP Only - Web, Email, FTP)")
    print(f"  {CYAN}3{RESET}. Start Capture (ICMP Only - Ping)")
    print(f"  {CYAN}4{RESET}. Start Capture (Custom BPF Filter)")
    print("--- Post-Capture Tools (Requires captured data) ---")
    print(f"  {CYAN}5{RESET}. Show {BLUE}Statistics{RESET} (Protocols, Rates, Bytes)")
    print(f"  {CYAN}6{RESET}. Show {BLUE}Summary{RESET} of Captured Packets")
    print(f"  {CYAN}7{RESET}. Export Captured Packets to {BLUE}PCAP File{RESET}")
    print(f"  {CYAN}0{RESET}. Quit")
    print("="*60)

if __name__ == "__main__":
    
    while True:
        display_menu()
        choice = input("Enter your choice (0-7): ").strip()
        
        bpf_filter = ""
        
        if choice == '1':
            bpf_filter = "ip"
            start_capture(bpf_filter)
        elif choice == '2':
            bpf_filter = "tcp"
            start_capture(bpf_filter)
        elif choice == '3':
            bpf_filter = "icmp"
            start_capture(bpf_filter)
        elif choice == '4':
            bpf_filter = input(f"Enter your custom BPF filter (e.g., host 192.168.1.1) : ").strip()
            if bpf_filter:
                start_capture(bpf_filter)
            else:
                 print(f"\n{YELLOW}Filter cannot be empty. Returning to menu.{RESET}")
        
        
        elif choice == '5':
            display_stats()
        
        elif choice == '6':
            display_summary()
            
        elif choice == '7':
            if captured_packets:
                filename = input("Enter filename to save as (e.g., capture.pcap): ").strip() or "capture.pcap"
                export_pcap(filename)
            else:
                 print(f"\n{YELLOW}No packets to export. Please perform a capture first.{RESET}")
                 
        elif choice == '0':
            print(f"\n{GREEN}Thank you for using the Mini-Sniffer. Goodbye!{RESET}")
            sys.exit(0)
            
        else:
            print(f"\n{YELLOW}Invalid choice. Please select an option from 0 to 7.{RESET}")
            continue