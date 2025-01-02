import json
import os
import bcrypt
import hashlib
from cryptography.fernet import Fernet

DATA_FILE = 'Data/data.json'
KEY_FILE = 'Data/secret.key'

def createDataFold():
    if not os.path.exists("Data"):
        os.mkdir("Data")

def generate_key():
    key = Fernet.generate_key()
    with open(KEY_FILE, 'wb') as key_file:
        key_file.write(key)

def load_key():
    return open(KEY_FILE, 'rb').read()

def encrypt_data(data):
    fernet = Fernet(load_key())
    json_data = json.dumps(data).encode()
    encrypted_data = fernet.encrypt(json_data)
    return encrypted_data

def decrypt_data(encrypted_data):
    fernet = Fernet(load_key())
    decrypted_data = fernet.decrypt(encrypted_data)
    return json.loads(decrypted_data.decode())

def hash_string(input_string):
    return hashlib.sha256(input_string.encode()).hexdigest()

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            encrypted_data = f.read()
            return decrypt_data(encrypted_data)
    return {"credentials": {}, "passwords": {}}

def save_data(data):
    encrypted_data = encrypt_data(data)
    with open(DATA_FILE, 'wb') as f:
        f.write(encrypted_data)

def save_credentials(username, password):
    createDataFold()
    hashed_username = hash_string(username)
    data = load_data()
    
    print(f"Checking for existing username: {hashed_username}")
    
    if hashed_username in data["credentials"]:
        print("username already exists.")
        return False

    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    data["credentials"][hashed_username] = hashed_password
    print(f"Saving new credentials: {hashed_username}")
    save_data(data)
    return True

def verify_credentials(username, password):
    hashed_username = hash_string(username)
    data = load_data()
    
    if hashed_username in data["credentials"]:
        return bcrypt.checkpw(password.encode(), data["credentials"][hashed_username].encode())
    
    return False

def save_password(app_name, username, password):
    data = load_data()
    data["passwords"][app_name] = {"username": username, "password": password}
    save_data(data)

def get_passwords():
    data = load_data()
    
    return {app: {"username": app_data["username"], "password": app_data["password"]}
            for app, app_data in data["passwords"].items()}

if not os.path.exists(KEY_FILE):
    generate_key()



