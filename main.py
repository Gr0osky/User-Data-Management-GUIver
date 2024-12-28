# IMPORTING THINGS
import os
import tkinter as tk


# MAIN WINDOW
root = tk.Tk()
root.title("User Data Management APP.")
root.geometry("640x480")

# DEFINING THINGS

# variables (inital)
User_Login_Success = False
LoginSuccess = False
categories_list = []

# FUNCTIONS

def createNewFile(x, y):
    with open("Data/User_Data_Categories.key", "a+") as file:
        file.writelines(f"{x}\n")

    
    with open("Data/User_Data_Value.key", "a+") as file_value:
        file_value.writelines(f"{y}\n")

def checkForUserLogin(x, y):
    with open("Data/Login_Data.key", "w") as file_for_login:
        file_for_login.writelines(f"{x}\n")
        file_for_login.writelines(f"{y}\n")

def welcome():
    try:
        with open("Data/Login_Data.key", "r") as file_To_Check_Login:
            NameCheck = file_To_Check_Login.readline().strip()
            PasswordCheck = file_To_Check_Login.readline().strip()
            label2 = tk.Label(root, text="Try to login to your account", font=("Arial", 14))
    except:
        pass
    pass

# Initial Layout

label = tk.Label(root, text="Welcome to User Data Management APP", font=("Arial", 28))
label.pack(pady=10) 

# mainloop
root.mainloop()


