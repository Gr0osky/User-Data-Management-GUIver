import json
import bcrypt
import os

CREDENTIALS_FILE = 'Data/credentials.json'

def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def create_data_folder():
    if not os.path.exists('Data'):
        os.mkdir('Data')

def save_credentials(username, hashed_password):
    create_data_folder()
    
    credentials = {}

    try:
        with open(CREDENTIALS_FILE, 'r') as f:
            credentials = json.load(f)
    except FileNotFoundError:
        pass

    if username in credentials:
        return False
    
    credentials[username] = hashed_password
    with open(CREDENTIALS_FILE, 'w') as f:
        json.dump(credentials, f)

    return True

def verify_credentials(username, password):
    try:
        with open(CREDENTIALS_FILE, 'r') as f:
            credentials = json.load(f)

        if username in credentials:
            return bcrypt.checkpw(password.encode(), credentials[username].encode())
        else:
            return False
        
    except FileNotFoundError:
        return False


