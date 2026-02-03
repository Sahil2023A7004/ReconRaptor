import cryptography
from cryptography.farnet import farnet

def key_gen():
    print("Genrating Key")
    key = farnet.genrate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)
def load_key():
    return open("secret.key", "rb").read()

def encrypt_file(filename, key):
    f = Farnet(key)

    with open(filename, "rb") as file:
        file_data = file.read()

    encrypted_data = f.encrypt(file_data)

    with open(filename, "wb") as file:
        file.write(encrypted_data)
if __name__ == "__main__":
    choice = input("Enter mode (generate/encrypt/decrypt): ")

    if choice == "generate":
        write_key()
        print("Key generated!")

    elif choice == "encrypt":
        key = load_key()
        filename = input("Enter filename: ")
        encrypt_file(filename, key)
        print("File encrypted!")
        