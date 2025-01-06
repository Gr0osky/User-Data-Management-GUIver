import subprocess
import sys
import os

def install(package):
    
    if sys.version_info[0] < 3: 
        pip_command = 'pip'
    else:  
        pip_command = 'pip3'

   
    subprocess.check_call([sys.executable, '-m', pip_command, 'install', package])

def check_and_install_packages(required_packages):

    for package in required_packages:
        try:
            __import__(package)  
            print(f"{package} is already installed.")
        except ImportError:
            print(f"{package} is not installed. Installing...")
            install(package)

if __name__ == "__main__":
    
    required_packages = [
        'json',
        'bcrypt',
        'hashlib',
        'cryptography'
    ]

    check_and_install_packages(required_packages)

