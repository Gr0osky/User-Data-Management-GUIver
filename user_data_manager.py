import json
import os
import bcrypt
import hashlib

DATA_FILE = 'Data/data.json'

def createDataFold():
    if not os.path.exists("Data"):
        os.mkdir("Data")

def hash_string(input_string):
    return hashlib.sha256(input_string.encode()).hexdigest()

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {"credentials": {}, "passwords": {}}

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f)

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
    hashed_app_name = hash_string(app_name)
    hashed_username = hash_string(username)
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    
    data = load_data()
    data["passwords"][hashed_app_name] = {"username": hashed_username, "password": hashed_password}
    
    print(f"Saving password for app: {hashed_app_name} with username: {hashed_username}")
    
    save_data(data)

def get_passwords():
    data = load_data()
    
    return {app: {"username": app_data["username"], "password": app_data["password"]}
            for app, app_data in data["passwords"].items()}



