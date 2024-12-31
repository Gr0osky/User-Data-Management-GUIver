import json
import os
import bcrypt
import hashlib

DATA_FILE = 'Data/data.json'

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

def save_credentials(email, password):
    hashed_email = hash_string(email)
    data = load_data()
    
    if hashed_email in data["credentials"]:
        return False

    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    data["credentials"][hashed_email] = hashed_password
    save_data(data)
    return True

def verify_credentials(email, password):
    hashed_email = hash_string(email)
    data = load_data()
    if hashed_email in data["credentials"]:
        return bcrypt.checkpw(password.encode(), data["credentials"][hashed_email].encode())
    return False


def save_password(app_name, username, password):
    hashed_app_name = hash_string(app_name)  # Hash the application name
    hashed_username = hash_string(username)  # Hash the username
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()  # Hash and decode the password
    data = load_data()
    data["passwords"][hashed_app_name] = {"username": hashed_username, "password": hashed_password}
    save_data(data)

def get_passwords():
    data = load_data()
    return {app: {"username": app_data["username"], "password": app_data["password"]}
            for app, app_data in data["passwords"].items()}


