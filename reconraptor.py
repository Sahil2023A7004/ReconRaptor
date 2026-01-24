#ReconRaptor v1.0
import socket

# --- 1. THE ENGINE ---
def testconnection(ip, port):
    print(f"Testing connection to {ip}:{port}...\n")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(2)
    result = sock.connect_ex((ip, port))
    if result == 0:
        print(f"port : {port} is OPEN")
    else:
        print(f"port : {port} is CLOSED")
    sock.close()
    return result

# --- 2. THE VALIDATORS ---
def validate_single_port(port):
    clean_port = port.strip()
    if clean_port == "":
        return False
    if not clean_port.isdigit():
        return False
    port_num = int(clean_port)
    if 1 <= port_num <= 65535:
        return True
    else:
        return False

def validate_ip(ip):
    if not ip or ip.strip() == "":
        return False
    try:
        socket.inet_aton(ip)
        return True
    except socket.error:
        return False

# --- 3. THE HANDLERS (The Bridge) ---
def handle_single_port_ui():
    print("\n--- SINGLE PORT SCAN MODE ---")
    
    target_ip = ""
    
    # Loop for IP
    while True:
        user_ip = input("Enter Target IP: ").strip()
        # FIXED: Added colon ':' and fixed indentation
        if validate_ip(user_ip):
            target_ip = user_ip
            break
        else:
            print(f"--> ERROR: {user_ip} is invalid. Enter a valid IPv4.\n")

    target_port = 0
    
    # Loop for Port
    while True:
        port_input = input("Enter Port (1-65535): ").strip()
        if validate_single_port(port_input):
            target_port = int(port_input)
            break
        else:
            print(f"ERROR {port_input} is invalid.\n")

    print(f"\n[*] Starting Scan on {target_ip}:{target_port}...\n")
    
    # Call the Engine
    testconnection(target_ip, target_port)
    
    input("\nPress Enter to return to menu...")

# --- 4. THE MENUS ---
def show_main_menu():
    print("=============================")
    print("      RECON RAPTOR v1.0      ") 
    print("=============================")
    print("1) Single Port Scan")
    print("2) Port Range Scan")
    print("3) Single IP Scan")
    print("4) IP Range Scan")
    print("5) Domain Scan")
    print("6) Exit")
    print("")

def get_user_input(prompt):
    user_input = input(prompt)
    user_input = user_input.strip()
    return user_input

def main_menu():
    while True:
        show_main_menu()
        choice = get_user_input("Enter choice: ")

        if not choice.isdigit():
            print("Invalid input — please enter a number from 1 to 6.\n")
            continue

        choice = int(choice)

        if choice == 1:
            # CONNECTED: This now calls your function!
            handle_single_port_ui()
        elif choice == 2:
            print("Port Range Scan coming soon...")
        elif choice == 3:
            print("Single IP Scan coming soon...")
        elif choice == 4:
            print("IP Range Scan coming soon...")
        elif choice == 5:
            print("Domain Scan coming soon...")
        elif choice == 6:
            print("Exiting Recon Raptor. Goodbye!")
            break  # This is the only place we break the main loop
        else:
            print("Invalid choice — please enter a number from 1 to 6.\n")

# --- ENTRY POINT ---
main_menu()