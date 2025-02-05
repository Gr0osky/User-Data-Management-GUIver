# This is the main application file. The functions from the others files are called here and then used. It controls the changing of windows, working of buttons, showing data to the user and stuff. Basically, the frontend stuff.
# IMPORTING THINGS
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo
from tkinter import messagebox
from user_data_manager import hash_string, save_credentials, verify_credentials, load_data, save_data, save_password, get_passwords
import os

# Some other stuff


# MAIN APPLICATION INTERFACE
class Application(tk.Tk):
    def __init__(self):
        super().__init__() #intialisation

        # window conifg
        self.title("User Data Management App") 
        self.geometry('640x480')
        self.configure(bg="gray")

        #button styles
        style = ttk.Style()
        style.configure('TButton',background='green', foreground='green', font=('Arial', 24), borderwidth=20 )
       
        # Welcome user 
        self.label = ttk.Label(self, text="Welcome to User Data Management APP", font=("Arial", 30))
        self.label.pack(pady=(100, 0))

        # Sign up button and calling out the funcition it performs
        self.SignUpHead = ttk.Button(self, text="Sign Up", command=self.button_clickedUp, width = 20, style="TButton", padding=(10,5))
        self.SignUpHead.pack(pady = 2)

        # Sign up button and calling out the funcition it performs
        self.SignInHead = ttk.Button(self, text="Sign In", command=self.button_clickedIn, width = 20, style="TButton", padding=(10, 5))
        self.SignInHead.pack(pady = 2)
        
        #encrypts the entire Data.json file if it already exists
        if os.path.exists('Data.json'):
            print("Encrypting existing data...")
            self.file_manager.encrypt_existing_file('Data.json')

    
    # Functions to be performed on clicking the button.
    def button_clickedUp(self):
            SignUpWindow(self)
            

    def button_clickedIn(self):
            SignInWindow(self)


# Sign-Up window (for account creation)
class SignUpWindow:
    def __init__(self, master):

        # Window configuration
        self.window = tk.Toplevel(master)
        self.window.title("Sign Up")
        self.window.geometry("400x300")
        
        # Direction to the user
        tk.Label(self.window, text="Sign Up Here", font=('Arial', 16)).pack(pady=20)
        
        # Username entry field
        tk.Label(self.window, text="username:").pack(pady=5)
        self.username_entry = tk.Entry(self.window)
        self.username_entry.pack(pady=5)

        # Password entry field
        tk.Label(self.window, text="Password:").pack(pady=5)
        self.password_entry = tk.Entry(self.window, show='*')
        self.password_entry.pack(pady=5)

        #Submit button
        submit_button = ttk.Button(self.window, text="Submit", command=self.submit)
        submit_button.pack(pady=20)

    # Performed when submit button is clicked. (saves the data only if all the entry fields are filled)
    def submit(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username and password:
            if save_credentials(username, password): # refer to line 48 of the user_data_manager.py to understand working of this function. (save_credentials)
                messagebox.showinfo("Success", "Sign up successful!")
                self.window.destroy() # destroys itself
            else:
                messagebox.showwarning("Error", "Username already exists!") # Shows warning if user tries to create multiple accounts on same client,
        else:
            messagebox.showwarning("Input Error", "Please enter both username and password.") # Shots warning if all fields are not filled.


# Sign-in Window (or login window, whatever you say)
class SignInWindow:
    def __init__(self, master):

        # Window Congiguration
        self.master = master
        self.window = tk.Toplevel(master)
        self.window.title("Login")
        self.window.geometry("400x300")

        # Directions for the user
        tk.Label(self.window, text = "Login Here", font=("Arial", 16)).pack(pady=20)

        # Username entry field
        tk.Label(self.window, text="Username:").pack(pady=5)
        self.username_entry = ttk.Entry(self.window)
        self.username_entry.pack(pady=5)

        # Password entry field
        tk.Label(self.window, text="Password:").pack(pady=5)
        self.password_entry = ttk.Entry(self.window, show='*')
        self.password_entry.pack(pady=5)


        # A button to toggle the visibily of password entered by the user (Show/Hide)
        self.toggle_button = ttk.Button(self.window, text="Show password", command=self.toggle_passVisib)
        self.toggle_button.pack(pady=3)

        # Final sign in button
        SignIn_button = ttk.Button(self.window, text="Sign In", command=self.SignIn)
        SignIn_button.pack(pady=10)

    # The function that responsible for toggling password visibility. (Also changes the text written on the button)
    def toggle_passVisib(self):
        if self.password_entry.cget('show') == '*':
            self.password_entry.config(show='')
            self.toggle_button.config(text="Hide Password")
        else:
            self.password_entry.config(show='*')
            self.toggle_button.config(text="Show password")

    # Main function to sign-in the user
    def SignIn(self):
        username = self.username_entry.get() # gets username from entry field
        password = self.password_entry.get() # gets password from entry field

        if username and password:
            if verify_credentials(username, password): # refer to line 65 of the user_data_manager.py to understand working of this function. (verify_credentials)
                messagebox.showinfo("Success", "Login Successful!")
                
                DataManagerWindow(self.master) # Opens the main password manager / Data Manager window.
                self.window.destroy() # Destroys itself

            else:
                messagebox.showwarning("Error", "Incorrect username or password!") # Shows error if incorrect password is entered,
        else:
            messagebox.showwarning("Input Error", "Please enter both username and password.") # Shows error if one field is left empty

# The main password manager window.
class DataManagerWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master) #intialising its master file

        # Window configuration
        self.master = master
        self.window = tk.Toplevel(master)
        self.window.title("Password Manager")
        self.window.geometry("640x480")

        self.data = get_passwords() #  refer to line 79 of ther user_data_manager.py to understand the working of this function (get_passwords)
        
        # Frame for an organised user interface.
        self.button_frame = tk.Frame(self.window)
        self.button_frame.pack(pady=10)

        self.populate_buttons() # refer to line 175.

        # Button to save new data and open a separate window for the process.
        save_new_button = ttk.Button(self.window, text="Save New Data", command=lambda: NewDataWindow(self.window))
        save_new_button.pack(pady=10)

    # populate button --> displays the buttons with application name on it. Which when clicked trigger the show_password function.
    def populate_buttons(self):
        for app_name in self.data:
            button = ttk.Button(self.button_frame, text=app_name, command=lambda app=app_name: self.show_password(app)) # refer to line 189 to understand show password function
            button.pack(pady=5)

    def update_data(self): # Was meant to update the data in real time, anyhow this doesn't work. Please provide a fix if you have one.
        for widget in getattr(self.button_frame, "winfo_children", []):
            widget.destroy()

        self.data = get_passwords()
        self.populate_buttons()

    # Shows the saved username and password of the particular app whose repective button is clicked by the user.
    def show_password(self, app_name):
        username_display = self.data[app_name]["username"] # self.data is a list returned by the get_passwords function, called in line 164.
        password_display = self.data[app_name]["password"] # The password and username are stored in the json in file in a formation {appname: username, password}

        if hasattr(self, 'username_entry') and hasattr(self, 'password_entry'): # clear the entry fields if data isn't available
            self.username_entry.delete(0, tk.END)
            self.password_entry.delete(0, tk.END)

       
        if not hasattr(self,'username_entry'): # if data is avaiable, then create entry fields.
            tk.Label(self.window,text='Username/username').pack()
            self.username_entry=tk.Entry(self.window)
            self.username_entry.pack()
           
            tk.Label(self.window,text='Password').pack()
            self.password_entry=tk.Entry(self.window)
            self.password_entry.pack()

       # show the username and data from the entry field.
        self.username_entry.insert(0, username_display) 
        self.password_entry.insert(0, password_display) 

# Separate window to add new data in Password manager window.
class NewDataWindow:
    def __init__(self, master):
        #window config
        super().__init__()
        self.window = tk.Toplevel(master)
        self.window.title("Save New Data")
        self.window.geometry("300x300")
        
        # Asking the name of Application whose name the user wants to save. (The name that has to appear on the buttons.)
        tk.Label(self.window, text="Application Name:").pack(pady=5)
        self.app_entry = tk.Entry(self.window)
        self.app_entry.pack(pady=5)

        # Username entry field 
        tk.Label(self.window, text="Username/username:").pack(pady=5)
        self.username_entry = tk.Entry(self.window)
        self.username_entry.pack(pady=5)

        # Password entry field
        tk.Label(self.window, text="Password:").pack(pady=5)
        self.password_entry = tk.Entry(self.window, show='*')
        self.password_entry.pack(pady=5)

        # submit button
        self.submit_button = ttk.Button(self.window, text="Submit", command=self.save_data)
        self.submit_button.pack(pady=10)

    # saves the user data in the json file by calling functions from user_data_manager.py
    def save_data(self):
        # Gets data entered by the user in the entry fields.
        app_name = self.app_entry.get() 
        username = self.username_entry.get()
        password = self.password_entry.get()

        # save the data only if all entry fields are filled.
        if app_name and username and password:
            save_password(app_name, username, password) # refer to line 74 of the user_data_manager.py to understand the working of this function,(save_password)
            messagebox.showinfo("Success", "Data saved successfully! Restart the program to see changes.")
            if isinstance(master := NewDataWindow.__dict__.get('master'), DataManagerWindow):
                master.update_data()  # was meant to update the data in the DataManagerWindow in real time but it doesn't work so user will have to restart the application to see changes

            # Clear all the entry fields.
            self.app_entry.delete(0, tk.END)
            self.username_entry.delete(0, tk.END)
            self.password_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Input Error", "Please enter all fields.") # show warning if all fields are not filled.
        
# Starting the application
if __name__ == "__main__":
    app = Application() # Intitialising entry point
    
    app.mainloop() # keep the application running until closed by the user.




