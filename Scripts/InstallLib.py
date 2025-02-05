"""This file automatically downloads the libraries required to run the program for noobs who dont know how to type terminal commands 
or people too lazy to download the requrired libraries manually."""
# Importing stuff
import subprocess # establishes connection with the terminal.
import sys # runs executable commands in the terminal
# import os --> not required   

# Function that installs a particular package
def install(package):
    
    # Checks if you are on python3 or older. pip3 is used specifically for python3 while pip is used for all versions of python.
    if sys.version_info[0] < 3: 
        pip_command = 'pip'
    else:  
        pip_command = 'pip3'

    # runs the pip command to install the particular package
    subprocess.check_call([sys.executable, '-m', pip_command, 'install', package])

# calls the install function only if the required package is not found.
def check_and_install_packages(required_packages):

    for package in required_packages:
        try:
            __import__(package)  
            print(f"{package} is already installed.")
        except ImportError:
            print(f"{package} is not installed. Installing...")
            install(package)

if __name__ == "__main__":
    
    # List of required packages
    required_packages = [
        'json',
        'bcrypt',
        'hashlib',
        'cryptography'
    ]

    check_and_install_packages(required_packages) # self explanatory

