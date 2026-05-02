#!/usr/bin/env python3
from scapy.all import IP, TCP, sr1, send
import socket
import random
import time
import sys


#BANNERS FOR FUN

QUOTES = [
    "The quieter you become, the more you can hear.",
    "Know your enemy and know yourself.",
    "Every port is a door. Some are just unlocked.",
    "Reconnaissance is the art of knowing before striking.",
    "Information is ammunition.",
]

RAPTORS = [
r"""
    .~))>>
   .~)>>
  .~))))>>>
.~))>>        ___
 ~))>>       \   \
  ))>>   .    \   \
   )>   .  .   \___\
""",
r"""
     __
  .'`  `'--.
 /  __   __  \
( (o) | (o)   )
 \  \_v_/   /
  '-._____.-'
   |  RAPTOR |
""",
r"""
    ,_,
   (O,O)
   (   )   SYSTEMS
  --"-"--  ONLINE
""",
r"""
                                    01001000
               __________      0110        01
              | 01001000  |--<  10  01101   10
              | 10110101  |      011      1001
          ____|___________|____
         |                     |
    _____|__             _______|
   |  T-REX  \          | 0110  |
   |  HUNGRY  >-----<   | 1001  |>
   |__________|          |______|
      ||    ||             PREY
""",
r"""
   10110101 01001000 11001010
        \     |     /
   01    \    |    /    10
    0   __\   |   /__   1
       /   \     /   \
      | T   \   / REX |
      |      \ /      |
   01  \      V      / 10
        \__       __/
    1001   \_____/   0110
         nom nom nom
      [ 0 1 0 1 0 1 0 1 ]
""",
r"""
                    .
    1 0 1 0 1 0    /|
    0 1 0 1 0 1   / |
    1 0 1 0 -->  /  |
               _/_ /
              |   |>==------<
              |___|  T-REX
              // \\
""",
]


def show_banner():
    raptor = random.choice(RAPTORS)
    quote = random.choice(QUOTES)
    print("\033[92m")
    print(raptor)
    print("=" * 45)
    print("  ⚡  R E C O N  R A P T O R  v1.2  ⚡")
    print("=" * 45)
    print(f'  "{quote}"')
    print("=" * 45)
    print("\033[0m")
    time.sleep(0.5)



#CORE UTILITIES AND DATA VALIDATION

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
        ip = input("Enter the target IPv4 address: ").strip()
        try:
            socket.inet_pton(socket.AF_INET, ip)
            port = validate_port()
            scan_menu(ip, port)
            return
        except socket.error:
            print("Invalid IP address format. Please enter a valid IPv4 address.")


def validate_domain():
    while True:
        domain = input("Enter the target domain name: ").strip()
        try:
            ip = socket.gethostbyname(domain)
            print(f"Domain {domain} resolved to IP: {ip}")
            port = validate_port()
            scan_menu(ip, port)
            return
        except socket.gaierror:
            print("Invalid domain name. Please enter a valid domain.")



#CORE SCANNING LOGIC
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


def stealth_range_scan(target_ip, start_port, end_port):
    print(f"\nStealth scanning {target_ip} — ports {start_port} to {end_port}...")
    print(f"{'PORT':<10}{'STATUS':<10}")
    print("-" * 20)

    for p in range(start_port, end_port + 1):
        packet = IP(dst=target_ip) / TCP(dport=p, flags="S")
        response = sr1(packet, timeout=1, verbose=0)

        if response is None:
            print(f"{p:<10}FILTERED BY FIREWALL")
        elif response.haslayer(TCP):
            flags = response.getlayer(TCP).flags

            if flags == 0x12:
                rst = TCP(dport=p, flags="R")
                close = IP(dst=target_ip) / rst
                send(close, verbose=0)
                print(f"{p:<10}OPEN")

            elif flags == 0x14:
                print(f"{p:<10}CLOSED")

#MENUS

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
                if isinstance(port, tuple):
                    run_range_scan(target_ip, port[0], port[1])
                else:
                    if check_port(target_ip, port):
                        print("PORT is OPEN")
                    else:
                        print("PORT is CLOSED")
            elif choice == 2:
                if isinstance(port, tuple):
                    stealth_range_scan(target_ip, port[0], port[1])
                else:
                    stealth_scan(target_ip, port)
            while True:
                again = input("\nScan again? (y/n): ").strip().lower()
                if again == "y":
                    main_menu()
                    return
                elif again == "n":
                    print("\n\033[92m[ ReconRaptor signing off... stay stealthy 🦖 ]\033[0m\n")
                    sys.exit(0)
                else:
                    print("Please enter y or n.")
        else:
            print("Invalid choice. Please enter 1 or 2.")


def main_menu():
    show_banner()
    print("------------------------------------")
    print("⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡")
    print("_-_-_🦕🦖🛜RECONRAPTOR🦕🦖🛜 _-_-_")
    print("-----------------------------------")
    print(" Enter 1 for IP ")
    print(" Enter 2 for Domain ")
    print(" Enter 3 to Exit ")
    while True:
        choice = input("Enter your choice: ")
        if choice.isdigit() and int(choice) in [1, 2, 3]:
            choice = int(choice)
            if choice == 1:
                validate_ip()
            elif choice == 2:
                validate_domain()
            elif choice == 3:
                print("\n\033[92m[ ReconRaptor signing off... stay stealthy 🦖 ]\033[0m\n")
                break
        else:
            print("Invalid choice. Please enter 1, 2 or 3.")


if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\n\n\033[92m[ Ctrl+C detected — ReconRaptor out 🦖 ]\033[0m\n")
