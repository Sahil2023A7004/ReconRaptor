#!/usr/bin/env python3
from scapy.all import IP, TCP, sr1, send
import socket


# ─────────────────────────────────────────
#  CORE UTILITIES
# ─────────────────────────────────────────

def validate_port():
    while True:
        port = input("Enter the target port number (1-65535): ").strip()
        if "-" in port:
            parts = port.split("-")
            if len(parts) == 2 and all(p.isdigit() for p in parts):
                start_port, end_port = int(parts[0]), int(parts[1])
                if 1 <= start_port <= 65535 and 1 <= end_port <= 65535 and start_port < end_port:
                    return start_port, end_port
                else:
                    print("Port numbers must be between 1 and 65535, and start must be less than end.")
            else:
                print("Invalid format. Use 20-80 format for ranges.")
        elif port.isdigit():
            port_num = int(port)
            if 1 <= port_num <= 65535:
                return port_num
            else:
                print("Port number must be between 1 and 65535.")
        else:
            print("Invalid input. Use 80 for single port or 20-80 for range.")
                    

def validate_ip():
    while True:
        ip = input("Enter the target IPv4 address:").strip()
        try:
            socket.inet_aton(ip)
            port = validate_port()
            scan_menu(ip, port)
            return 
        except socket.error:
            print("Invalid IP address format. Please enter a valid IPv4 address.")

def validate_domain():
    while True:
        domain = input("Enter the target domain name:").strip()
        try:
            ip = socket.gethostbyname(domain)
            print(f"Domain {domain} resolved to IP: {ip}")
            port = validate_port()
            scan_menu(ip, port)
            return 
        except socket.gaierror:
            print("Invalid domain name. Please enter a valid domain.")


def stealth_scan(target_ip, port):
    timeout = 1
    packet = IP(dst=target_ip) / TCP(dport=port, flags="S")
    response = sr1(packet, timeout=timeout, verbose=0)

    if response is None:
        print("PORT is FILTERED")
    elif response.haslayer(TCP):
        flags = response.getlayer(TCP).flags

        if flags == 0x12:
            rst = TCP(dport=port, flags="R")
            close = IP(dst=target_ip) / rst
            send(close, verbose=0)
            print("PORT is OPEN")

        elif flags == 0x14:
            print("PORT is CLOSED")


def check_port(target_ip, port_num):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.5)
    result = sock.connect_ex((target_ip, port_num))
    sock.close()
    return result == 0


def run_range_scan(target_ip, start_port, end_port):
    print(f"\nScanning {target_ip} — ports {start_port} to {end_port}...")
    print(f"{'PORT':<10}{'STATUS':<10}")
    print("-" * 20)

    for p in range(start_port, end_port + 1):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((target_ip, p))
        sock.close()

        if result == 0:
            print(f"{p:<10}OPEN")
        else:
            print(f"{p:<10}CLOSED")

def scan_menu(target_ip, port):
    print("------------------------------------")
print("⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡")
print("_-_-_🦕🦖🛜 SCAN TYPE 🦕🦖🛜 _-_-_")
print("-----------------------------------")
print(" Enter 1 for SYN Scan ")
print(" Enter 2 for Stealth Scan ")
while True:
  choice = input("Enter your choice: ")
  if choice.isdigit() and int(choice) in [1, 2]:
    choice = int(choice)
    if choice == 1:
     #inclomplete functionality for SYN scan, will be added in future updates
     print("SYN Scan is currently under development. Please choose Stealth Scan.")
      
     def main_menu():
        print("------------------------------------")
        print("⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡")
        print("_-_-_🦕🦖🛜RECONRAPTOR🦕🦖🛜 _-_-_")
        print("-----------------------------------")
        print(" Enter 1 for IP ")
        print(" Enter 2 for Domain ")
        while True:
          choice = input("Enter your choice: ")
          if choice.isdigit() and int(choice) in [1, 2]:
            choice = int(choice)
            if choice == 1:
             validate_ip()
            elif choice == 2:
              validate_domain()
          else:
            print("Invalid choice. Please enter 1 or 2.")
         
                 

if __name__ == "__main__":
    pass  # new menu flow goes here