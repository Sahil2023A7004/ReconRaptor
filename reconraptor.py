#!/usr/bin/env python3
from scapy.all import IP, TCP, sr1, send
import socket


# ─────────────────────────────────────────
#  CORE UTILITIES
# ─────────────────────────────────────────

def validate_ip(ip):
    if not ip or ip.strip() == "":
        return False
    try:
        socket.inet_aton(ip)
        return True
    except socket.error:
        return False


# ─────────────────────────────────────────
#  CORE SCANNING LOGIC
# ─────────────────────────────────────────

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


# ─────────────────────────────────────────
#  ENTRY POINT  (placeholder for new menu)
# ─────────────────────────────────────────

if __name__ == "__main__":
    pass  # new menu flow goes here