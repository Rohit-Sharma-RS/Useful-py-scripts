import os
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.hashes import SHA256
from cryptography.hazmat.backends import default_backend
from getpass import getpass

def generate_key_from_password(password):
    salt = b"default_fixed_salt_value"
    kdf = PBKDF2HMAC(
        algorithm=SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    return key

def encrypt_file(file_path, key):
    fernet = Fernet(key)
    with open(file_path, "rb") as file:
        data = file.read()
    encrypted_data = fernet.encrypt(data)
    with open(file_path, "wb") as file:
        file.write(encrypted_data)
    print(f"Encrypted: {file_path}")

def decrypt_file(file_path, key):
    fernet = Fernet(key)
    with open(file_path, "rb") as file:
        encrypted_data = file.read()
    decrypted_data = fernet.decrypt(encrypted_data)
    with open(file_path, "wb") as file:
        file.write(decrypted_data)
    print(f"Decrypted: {file_path}")

def encrypt_folder(folder_path, key):
    for root, _, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            encrypt_file(file_path, key)
    print(f"All files in '{folder_path}' have been encrypted.")

def decrypt_folder(folder_path, key):
    for root, _, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            decrypt_file(file_path, key)
    print(f"All files in '{folder_path}' have been decrypted.")

if __name__ == "__main__":
    folder_path = input("Enter the path to the folder: ").strip()
    mode = input("Do you want to (E)ncrypt or (D)ecrypt the folder? ").lower()
    password = getpass("Enter your password: ")
    key = generate_key_from_password(password)
    if mode == "e":
        encrypt_folder(folder_path, key)
    elif mode == "d":
        decrypt_folder(folder_path, key)
    else:
        print("Invalid option. Please choose 'E' or 'D'.")
