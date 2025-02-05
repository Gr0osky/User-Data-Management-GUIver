# This file includes all the code for processing user data recieved from the main file.

# Importing stuff
import json
import os
import bcrypt
import hashlib
from cryptography.fernet import Fernet

# Files to be intialised
DATA_FILE = 'Data/data.json' # Data file
KEY_FILE = 'Data/secret.key' # File that contains key to decrypt data file

def createDataFold(): # Create the data folder if it does not exist
    if not os.path.exists("Data"): 
        os.mkdir("Data")

def generate_key(): # Generatees key to encrypt the Data file.
    createDataFold()
    key = Fernet.generate_key()
    with open(KEY_FILE, 'wb') as key_file:
        key_file.write(key)
 
def load_key(): # loads the key and returns its value (the key itself)
    return open(KEY_FILE, 'rb').read()

def encrypt_data(data): # encrypts the entire data in the Data file and returns encrypted data,
    fernet = Fernet(load_key())
    json_data = json.dumps(data).encode()
    encrypted_data = fernet.encrypt(json_data)
    return encrypted_data

def decrypt_data(encrypted_data): # Decrypts the entire data in the encrypted Data file and returns the data.
    fernet = Fernet(load_key())
    decrypted_data = fernet.decrypt(encrypted_data)
    return json.loads(decrypted_data.decode())

def hash_string(input_string): # hashes the data
    return hashlib.sha256(input_string.encode()).hexdigest()

def load_data(): # uses the decrypted data returned from the decrypted data to return the data to the program in a more organised form 
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            encrypted_data = f.read()
            return decrypt_data(encrypted_data)
    return {"credentials": {}, "passwords": {}}

def save_data(data): # encrypts the recieved data and dumps it in the Data File.
    encrypted_data = encrypt_data(data)
    with open(DATA_FILE, 'wb') as f:
        f.write(encrypted_data)

def save_credentials(username, password): # saves the encrypted user credentials in such a way that they cannot be decrypted
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

def verify_credentials(username, password): # verifies the credentials entered by the user in login window (checks if they are correct to let the user login)
    hashed_username = hash_string(username)
    data = load_data()
    
    if hashed_username in data["credentials"]:
        return bcrypt.checkpw(password.encode(), data["credentials"][hashed_username].encode())
    
    return False

def save_password(app_name, username, password): # saves the user data recieved from the NewDataWindow in main.py
    data = load_data()
    data["passwords"][app_name] = {"username": username, "password": password}
    save_data(data)

def get_passwords(): # loads the saved user data to be displayed in the DataManagerWindow in main.py and returns it in an organised format.
    data = load_data()
    
    return {app: {"username": app_data["username"], "password": app_data["password"]}
            for app, app_data in data["passwords"].items()}

if not os.path.exists(KEY_FILE): # if key file doesn't exist then generate a key and store it in the key file.
    generate_key()



