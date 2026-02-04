import os
from cryptogrphy.fernet import fernet

#key gen
def key_gen():
    key = Fernet.genrate_key()
#key save
    with open("secret.key", "wb") as key_file:
        key_file.write(key)

#fetching key
def load_key():
    return open("secret.key", "rb").read()

#encrypting the file
def enryptor(filename, key):
    f = Fernet(key) #here we are using farnet with our key to create encrptor f to encypt files
    with open(filename, "rb") as file:
        file_data = file.read()
        encrypted_data = f.encrypt(file_data)
        with open(filename, "wb") as file:
            file.write(encrypted_data)

#decrypting the file

def decryptor(filename, key):
    f = Fernet(key)
    with open(filename, "rb") as file:
        file_data = file.read()
        decrypted_data = f.decrypt(file_data)
    with open(filename, "wb") as file:
        file.write(decrypted_data)

if __name__ == "__main__":
    choice = input("Enter mode (1==gen/2==enc/3==dec): ")



