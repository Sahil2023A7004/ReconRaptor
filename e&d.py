import os
from cryptography.fernet import Fernet

def key_gen():
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)

def load_key():
    return open("secret.key", "rb").read()

def encrypt_file(filename, key):
    f = Fernet(key)
    with open(filename, "rb") as file:
        file_data = file.read()
    
    encrypted_data = f.encrypt(file_data)
    
    with open(filename, "wb") as file:
        file.write(encrypted_data)

def decrypt_file(filename, key):
    f = Fernet(key)
    with open(filename, "rb") as file:
        file_data = file.read()
    
    decrypted_data = f.decrypt(file_data)
    
    with open(filename, "wb") as file:
        file.write(decrypted_data)

if __name__ == "__main__":
    choice = input("Enter mode (1==gen/2==enc/3==dec): ")

    if choice == "1":
        key_gen()
        print("Key generated successfully!")
        
        print("--- Auto-Starting Encryption ---")
        try:
            key = load_key()
            filename = input("Enter filename to encrypt: ")
            encrypt_file(filename, key)
            print("File encrypted!")
        except FileNotFoundError:
            print("Error: File not found.")

    elif choice == "2":
        try:
            key = load_key()
            filename = input("Enter filename to encrypt: ")
            encrypt_file(filename, key)
            print("File encrypted!")
        except FileNotFoundError:
            print("Error: Key not found or File not found.")

    elif choice == "3":
        try:
            key = load_key()
            filename = input("Enter filename to decrypt: ")
            decrypt_file(filename, key)
            print("File decrypted!")
        except FileNotFoundError:
            print("Error: Key not found or File not found.")

    else:
        print("Invalid choice.")