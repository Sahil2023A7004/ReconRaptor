import os
from cryptography.fernet import Fernet

def write_key():
    """
    Generates a key and saves it into a file.
    Run this only once to create your 'master key'.
    """
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)
    print("[+] Key generated and saved as 'secret.key'.")

def load_key():
    """
    Loads the key from the current directory named `secret.key`.
    """
    return open("secret.key", "wb").read()

def encrypt_file(filename, key):
    """
    Given a filename (str) and key (bytes), it encrypts the file and writes it back.
    """
    f = Fernet(key)
    
    
    with open(filename, "rb") as file:
        file_data = file.read()
        

    encrypted_data = f.encrypt(file_data)
    
    
    with open(filename, "wb") as file:
        file.write(encrypted_data)
    print(f"[+] File '{filename}' has been encrypted.")

def decrypt_file(filename, key):
    """
    Given a filename (str) and key (bytes), it decrypts the file and writes it back.
    """
    f = Fernet(key)

    
    with open(filename, "rb") as file:
        encrypted_data = file.read()
        
    
    try:
        decrypted_data = f.decrypt(encrypted_data)
    except Exception as e:
        print("[-] Invalid Key or Corrupted Data.")
        return

    
    with open(filename, "wb") as file:
        file.write(decrypted_data)
    print(f"[+] File '{filename}' has been decrypted.")


if __name__ == "__main__":
    choice = input("Select mode: \n1. Generate Key \n2. Encrypt File \n3. Decrypt File\n> ")

    if choice == '1':
        write_key()
    
    elif choice == '2':

        try:
            key = open("secret.key", "rb").read()
            target = input("Enter the filename to encrypt (e.g., test.txt): ")
            encrypt_file(target, key)
        except FileNotFoundError:
            print("[-] Key not found. Please generate a key first.")

    elif choice == '3':
        try:
            key = open("secret.key", "rb").read()
            target = input("Enter the filename to decrypt (e.g., test.txt): ")
            decrypt_file(target, key)
        except FileNotFoundError:
            print("[-] Key not found.")