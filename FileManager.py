from cryptography.fernet import Fernet
import json
import os

class FileManager:
    def __init__(self, key_file='secret.key'):
        self.key_file = key_file
        self.key = self.load_or_generate_key()

    def load_or_generate_key(self):
        if os.path.exists(self.key_file):
            with open(self.key_file, 'rb') as file:
                return file.read()
        else:
            key = Fernet.generate_key()
            with open(self.key_file, 'wb') as file:
                file.write(key)
            return key

    def encrypt_data(self, data):
        fernet = Fernet(self.key)
        json_data = json.dumps(data).encode()  
        encrypted_data = fernet.encrypt(json_data)
        return encrypted_data

    def decrypt_data(self, encrypted_data):
        fernet = Fernet(self.key)
        decrypted_data = fernet.decrypt(encrypted_data)
        return json.loads(decrypted_data.decode())  

    def save_encrypted_json(self, data, filename='data.json'):
        encrypted_data = self.encrypt_data(data)
        with open(filename, 'wb') as file:
            file.write(encrypted_data)

    def load_encrypted_json(self, filename='data.json'):
        if not os.path.exists(filename):
            return {}
        
        with open(filename, 'rb') as file:
            encrypted_data = file.read()
        
        return self.decrypt_data(encrypted_data)

    def encrypt_existing_file(self, filename='data.json'):
        existing_data = self.load_encrypted_json(filename) 
        self.save_encrypted_json(existing_data, filename)

if __name__ == "__main__":
    manager = FileManager()

    manager.encrypt_existing_file('data.json')


        
