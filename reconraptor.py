
import socket

ip = ""
port = ""

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
    print(f"\nDEBUG: Starting scan on IP: '{target_ip}'") # Debug line
    print(f"Scanning ports {start_port} to {end_port}...")
    print("PORT\tSTATUS\tERROR CODE") # Added Error Code column
    print("-" * 30)
    
    for p in range(start_port, end_port + 1):
        # We call check_port, but we also want to see the result code!
        # So let's reproduce the check logic here temporarily for debugging
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1) # Increased timeout to 1 second
        
        result = sock.connect_ex((target_ip, p))
        sock.close()
        
        if result == 0:
            print(f"{p}\tOPEN\t{result}")
        else:
            # This will show us WHY it failed (111=Closed, 11=Timeout)
            print(f"{p}\tCLOSED\t{result}")

def portt():
    global port
    x = input("Enter port to scan (1-65535): ").strip()
    if x.isdigit():
        port = int(x)
        if port in range(1, 65536):
            run_single_port_scan(port, ip)
        else:
            print("Error: Port out of range (1-65535)")
            portt()
    else:
        print("Error: Please enter digits only")
        portt()

def validate_ip(ip):
    if not ip or ip.strip() == "":
        return False
    try:
        socket.inet_aton(ip)
        return True
    except socket.error:
        return False

def range_scan_menu():
    global ip
    
    # Safety Check: Did we get the IP?
    if ip == "":
        print("DEBUG ERROR: IP variable is empty!")
        return

    choice = input("Enter port range (e.g. 20-80): ").strip()
    try:
        ports = choice.split("-")
        start_port = int(ports[0])
        end_port = int(ports[1])
        
        if start_port > end_port:
            print("Error: Start port must be smaller than end port.")
            range_scan_menu()
        else:
            # PASS THE IP HERE explicitly
            run_range_scan(ip, start_port, end_port)
    except Exception as e:
        print(f"ERROR: {e}")
        range_scan_menu()

def scan_menu():
    global ip
    print("\nCHOOSE A SCAN TYPE:")
    print("1) SYN Scan")
    print("2) Stealth Scan")
    print("3) Aggressive Scan")
    print("4) Back")
    
    raw_choice = input("Enter choice (1-4): ").strip()
    
    if raw_choice.isdigit():
        choice = int(raw_choice)
        
        if choice == 1:
            temp_ip = input("Enter your IPv4: ").strip()
            if validate_ip(temp_ip) == True:
                ip = temp_ip
                portt()
            else:
                print("Error: Enter a valid IPv4 address.")
                scan_menu()
                
        elif choice in range(2, 4):
             print("Coming soon...")
             scan_menu()
             
        elif choice == 4:
             show_main_menu()
        else:
             print("Error: Select 1-4.")
             scan_menu()
    else:
        print("Error: Please enter a number.")
        scan_menu()

def show_main_menu():
    global ip
    print("=============================")
    print("      RECON RAPTOR v1.2      ") 
    print("=============================")
    print("1) Single Port Scan")
    print("2) Port Range Scan")
    print("3) Single IP Scan")
    print("5) Domain Scan")
    print("6) Exit")
    print("")
    
    raw_choice = input("Enter your choice: ").strip()
    
    if raw_choice.isdigit():
        choice = int(raw_choice)
        
        if choice == 1:
            scan_menu()
        elif choice == 2:
            if ip == "":
                ip = input("Enter Target IP: ").strip()
            range_scan_menu()
        elif choice in range(3, 6): 
            print("Coming soon... Please enter 1 or 2 to scan.")
            show_main_menu()
        elif choice == 6:
            print("Exiting...")
            return
        else:
            print("Enter correct choice 1-6")
            show_main_menu()
    else:
        print("Error: Please enter a number.")
        show_main_menu()

if __name__ == "__main__":
    show_main_menu()