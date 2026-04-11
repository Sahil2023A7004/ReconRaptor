#!/usr/bin/env python3
from scapy.all import IP, TCP, ICMP, sr1, send
import socket
import sys


def stealth_scan(target_ip, port):
    timeout = 1
    packet = IP(dst=target_ip)/TCP(dport=port, flags="S")
    response = sr1(packet, timeout=timeout, verbose=0)

    if response is None:
        print("PORT is FILTERED")
    elif response.haslayer(TCP):
        flags = response.getlayer(TCP).flags

        if flags == 0x12:
            rst = TCP(dport=port, flags="R")
            close = IP(dst=target_ip)/rst
            send(close, verbose=0)
            print("PORT is OPEN")

        elif flags == 0x14:
            print("PORT is CLOSED")


def check_port(target_ip, port_num):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.5)
    result = sock.connect_ex((target_ip, port_num))
    sock.close()
    if result == 0:
        return True
    else:
        return False


def run_single_port_scan(target_port, target_ip):
    print(f"Testing connection to {target_ip}:{target_port}...\n")
    if check_port(target_ip, target_port):
        print(f"Port {target_port} is OPEN")
    else:
        print(f"Port {target_port} is CLOSED")


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


def portt1(target_ip):
    while True:
        x = input("Enter port to scan (1-65535): ").strip()
        if not x.isdigit():
            print("Error: Please enter digits only.")
            continue
        port = int(x)
        if port not in range(1, 65536):
            print("Error: Port out of range (1-65535).")
            continue
        run_single_port_scan(port, target_ip)
        break


def portt2(target_ip):
    while True:
        x = input("Enter port to scan (1-65535): ").strip()
        if not x.isdigit():
            print("Error: Please enter digits only.")
            continue
        port = int(x)
        if port not in range(1, 65536):
            print("Error: Port out of range (1-65535).")
            continue
        stealth_scan(target_ip, port)
        break


def validate_ip(ip):
    if not ip or ip.strip() == "":
        return False
    try:
        socket.inet_aton(ip)
        return True
    except socket.error:
        return False


def range_scan_menu():
    target_ip = input("Enter Target IP: ").strip()
    if not validate_ip(target_ip):
        print("Error: Enter a valid IPv4 address.")
        range_scan_menu()
        return

    while True:
        choice = input("Enter port range (e.g. 20-80): ").strip()
        try:
            parts = choice.split("-")
            start_port = int(parts[0])
            end_port = int(parts[1])
            if start_port > end_port:
                print("Error: Start port must be smaller than end port.")
                continue
            run_range_scan(target_ip, start_port, end_port)
            break
        except (IndexError, ValueError):
            print("Error: Use format 20-80.")


def scan_menu():
    print("\nCHOOSE A SCAN TYPE:")
    print("1) SYN Scan")
    print("2) Stealth Scan")
    print("3) Back")

    raw_choice = input("Enter choice (1-3): ").strip()

    if not raw_choice.isdigit():
        print("Error: Please enter a number.")
        scan_menu()
        return

    choice = int(raw_choice)

    if choice == 1:
        temp_ip = input("Enter your IPv4: ").strip()
        if validate_ip(temp_ip):
            portt1(temp_ip)
        else:
            print("Error: Enter a valid IPv4 address.")
            scan_menu()

    elif choice == 2:
        temp_ip = input("Enter your IPv4: ").strip()
        if validate_ip(temp_ip):
            portt2(temp_ip)
        else:
            print("Error: Enter a valid IPv4 address.")
            scan_menu()

    elif choice == 3:
        show_main_menu()

    else:
        print("Error: Select 1-3.")
        scan_menu()


def show_main_menu():
    print("=============================")
    print("      RECON RAPTOR v1.2      ")
    print("=============================")
    print("1) Single Port Scan")
    print("2) Port Range Scan")
    print("3) Domain Scan")
    print("5) Exit")
    print("")

    raw_choice = input("Enter your choice: ").strip()

    if not raw_choice.isdigit():
        print("Error: Please enter a number.")
        show_main_menu()
        return

    choice = int(raw_choice)

    if choice == 1:
        scan_menu()
    elif choice == 2:
        range_scan_menu()
    elif choice in (3, 4):
        print("Coming soon...")
        show_main_menu()
    elif choice == 5:
        print("Exiting...")
        return
    else:
        print("Enter correct choice 1-5.")
        show_main_menu()


if __name__ == "__main__":
    show_main_menu()