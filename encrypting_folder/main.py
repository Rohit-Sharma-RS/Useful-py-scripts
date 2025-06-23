import os
import base64
import json
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
    if not os.path.isfile(file_path):
        print(f"Skipping non-file: {file_path}")
        return
    fernet = Fernet(key)
    try:
        with open(file_path, "rb") as file:
            data = file.read()
        encrypted_data = fernet.encrypt(data)
        with open(file_path, "wb") as file:
            file.write(encrypted_data)
        print(f"Encrypted: {file_path}")
    except PermissionError:
        print(f"🚫 Permission denied: {file_path}")

def decrypt_file(file_path, key):
    fernet = Fernet(key)
    try:
        with open(file_path, "rb") as file:
            encrypted_data = file.read()
        decrypted_data = fernet.decrypt(encrypted_data)
        with open(file_path, "wb") as file:
            file.write(decrypted_data)
        print(f"Decrypted: {file_path}")
    except Exception as e:
        print(f"Failed to decrypt {file_path}: {e}")

def encrypt_folder(folder_path, key):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            encrypt_file(file_path, key)
    print(f"All files in '{folder_path}' have been encrypted.")

def decrypt_folder(folder_path, key):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            decrypt_file(file_path, key)
    print(f"All files in '{folder_path}' have been decrypted.")

def encrypt_folder_names(folder_path, key):
    fernet = Fernet(key)
    folder_map = {}
    for root, dirs, _ in os.walk(folder_path, topdown=False):  # bottom-up
        for d in dirs:
            original_path = os.path.join(root, d)
            encrypted_name = fernet.encrypt(d.encode()).decode()
            encrypted_name = base64.urlsafe_b64encode(encrypted_name.encode()).decode()[:20]
            new_path = os.path.join(root, encrypted_name)
            os.rename(original_path, new_path)
            folder_map[new_path] = original_path
    with open(os.path.join(folder_path, "folder_name_map.json"), "w") as f:
        json.dump(folder_map, f)
    print("✅ Folder names encrypted and mapping saved.")

def decrypt_folder_names(folder_path, key):
    fernet = Fernet(key)
    map_path = os.path.join(folder_path, "folder_name_map.json")
    if not os.path.exists(map_path):
        print("❌ No folder map found.")
        return
    with open(map_path, "r") as f:
        folder_map = json.load(f)
    for enc, orig in sorted(folder_map.items(), key=lambda x: -len(x[0])):  # longest path first
        if os.path.exists(enc):
            os.rename(enc, orig)
    os.remove(map_path)
    print("✅ Folder names decrypted.")

if __name__ == "__main__":
    folder_path = input("Enter the path to the folder: ").strip()
    mode = input("Do you want to (E)ncrypt or (D)ecrypt the folder? ").lower()
    password = getpass("Enter your password: ")
    key = generate_key_from_password(password)

    folder_rename = input("Encrypt/decrypt folder names too? (y/n): ").lower()

    if mode == "e":
        encrypt_folder(folder_path, key)
        if folder_rename == "y":
            encrypt_folder_names(folder_path, key)
    elif mode == "d":
        decrypt_folder(folder_path, key)
        if folder_rename == "y":
            decrypt_folder_names(folder_path, key)
    else:
        print("Invalid option. Please choose 'E' or 'D'.")
