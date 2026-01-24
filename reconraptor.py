#ReconRaptor v1.0
import socket
def testconnection(ip, port):

  print(f"Testing connection to {ip}:{port}...\n")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(2)
    result = sock.connect_ex((ip,port))
    if result == 0:
        print(f"port : {port} is OPEN")
    else:
        print(f"port :{port} is CLOSED")
    sock.close()
    return result


def main_menu():

    while True:
        show_main_menu()   # Print the menu
        choice = get_user_input("Enter choice: ")

        if not choice.isdigit():
            print("Invalid input — please enter a number from 1 to 6.\n")
            continue

        choice = int(choice)

        if choice < 1 or choice > 6:
            print("Invalid choice — please enter a number from 1 to 6.\n")
            continue

        print(f"You selected option {choice}")
        break


def show_main_menu():
    # This function will display the main menu options
    print("=============================")
    print("      RECON RAPTOR v1.0      ") 
    print("=============================")
    print("1) Single Port Scan")
    print("2) Port Range Scan")
    print("3) Single IP Scan")
    print("4) IP Range Scan")
    print("5) Domain Scan")
    print("6) Exit")
    print("")

def scan_menu():
    # This function will show port scan types (syn, aggressive, stealth)
    print("CHOOSE A SCAN TYPE:(1-4) ")
    print("                    ")
    print("1) SYN Scan")
    print("2) Stealth Scan")
    print("3) Agressive Scan")
    print("4) Back")


def get_user_input(prompt):
    # This function will take input from user
    user_input = input(prompt)
    user_input = user_input.strip()
    return user_input


def validate_single_port(port):
    # This function will check if a single port is valid (1-65535)

    #Step 1:-  Strip whitespaces
    clean_port = port.strip()

    #Step 2:- Check if port is empty
    if clean_port == "":
        return False
        
    #Step 3:- Chcek if the port input is digits only
    if not clean_port.isdigit():
        return False

    #Step 4:- Convert to integer becuse python takes input as string only
    port_num = int(clean_port)

    #Step 5:- Check Range 
    if 1 <= port_num <= 65535:
        return True
    else:
        return False

def validate_ip(ip):
    # Quick check for empty string
    if not ip or ip.strip() == "":
        return False
    try:
        # We use the socket library itself to check if the IP is valid!
        socket.inet_aton(ip)
        return True
    except socket.error:
        # If socket throws an error, it's not a valid IPv4 address
        return False          

def run_single_port_scan(port, scan_type):
    # This function will perform single port scan (later)
    pass


def show_results(result):
    # This function will show scan results
    pass

def ask_for_ip():
    #Will ask ip from user
    pass

def ask_for_port():
    #Asks for port
    pass



def henadle_single_port_ui(port):
    # This function will check if a single port is valid (1-65535)

    print("\n---SINGLE PORT SCAN MODE ---")
    target_ip = ""
    while True:
        user_ip =input("Enter Target IP: ").strip()
        if validate_ip(user_ip)
        target_ip = user_ip
        break
        else:
            print(f"--> ERROR: {user_ip} is invalid. Enter a valid IPv4.\n")
    target_port = 0
    while True:
        port_input = input("Enter Port (1-65535): ").strip()
        if validate_single_port(port_input):
            target_port = int(port_input)
            break
    
        else:
            print(f"ERROR {port_input} is invalid.\n")

    print(f"\n[*] Starting Scan on {target_ip}:{target_port}...\n")
    testconnection(target_ip, target_port)
    input("\nPress Enter to return to menu...")













# Entry point — run the program
main_menu()
 this is the code 