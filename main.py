# IMPORTING THINGS
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo
from tkinter import messagebox
from user_data_manager import hash_string, save_credentials, verify_credentials, load_data, save_data, save_password, get_passwords

# Some other stuff


# MAIN APPLICATION INTERFACE
class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("User Data Management App")
        self.geometry('640x480')
        self.configure(bg="gray")
        style = ttk.Style()
        style.configure('TButton',background='green', foreground='green', font=('Arial', 24), borderwidth=20 )
        # Welcome user 
        self.label = ttk.Label(self, text="Welcome to User Data Management APP", font=("Arial", 30))
        self.label.pack(pady=(100, 0))

        self.SignUpHead = ttk.Button(self, text="Sign Up", command=self.button_clickedUp, width = 20, style="TButton", padding=(10,5))
        self.SignUpHead.pack(pady = 2)

        self.SignInHead = ttk.Button(self, text="Sign In", command=self.button_clickedIn, width = 20, style="TButton", padding=(10, 5))
        self.SignInHead.pack(pady = 2)

    def button_clickedUp(self):
            SignUpWindow(self)
            

    def button_clickedIn(self):
            SignInWindow(self)


class SignUpWindow:
    def __init__(self, master):
        self.window = tk.Toplevel(master)
        self.window.title("Sign Up")
        self.window.geometry("400x300")
        tk.Label(self.window, text="Sign Up Here", font=('Arial', 16)).pack(pady=20)
        
        tk.Label(self.window, text="username:").pack(pady=5)
        self.username_entry = tk.Entry(self.window)
        self.username_entry.pack(pady=5)

        tk.Label(self.window, text="Password:").pack(pady=5)
        self.password_entry = tk.Entry(self.window, show='*')
        self.password_entry.pack(pady=5)

        submit_button = ttk.Button(self.window, text="Submit", command=self.submit)
        submit_button.pack(pady=20)

    def submit(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username and password:
            if save_credentials(username, password):
                messagebox.showinfo("Success", "Sign up successful!")
                self.window.destroy()
            else:
                messagebox.showwarning("Error", "Username already exists!")
        else:
            messagebox.showwarning("Input Error", "Please enter both username and password.")



class SignInWindow:
    def __init__(self, master):
        self.master = master
        self.window = tk.Toplevel(master)
        self.window.title("Login")
        self.window.geometry("400x300")

        tk.Label(self.window, text = "Login Here", font=("Arial", 16)).pack(pady=20)

        tk.Label(self.window, text="Username:").pack(pady=5)
        self.username_entry = ttk.Entry(self.window)
        self.username_entry.pack(pady=5)

        tk.Label(self.window, text="Password:").pack(pady=5)
        self.password_entry = ttk.Entry(self.window, show='*')
        self.password_entry.pack(pady=5)

        SignIn_button = ttk.Button(self.window, text="Sign In", command=self.SignIn)
        SignIn_button.pack(pady=10)

    def SignIn(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username and password:
            if verify_credentials(username, password):
                messagebox.showinfo("Success", "Login Successful!")
                
                DataManagerWindow(self.master)
                self.window.destroy()

            else:
                messagebox.showwarning("Error", "Incorrect username or password!")
        else:
            messagebox.showwarning("Input Error", "Please enter both username and password.")

class DataManagerWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.window = tk.Toplevel(master)
        self.window.title("Password Manager")
        self.window.geometry("640x480")

        self.data = get_passwords()
        
        self.button_frame = tk.Frame(self.window)
        self.button_frame.pack(pady=10)

        self.populate_buttons()

        save_new_button = ttk.Button(self.window, text="Save New Data", command=lambda self=self: NewDataWindow(self, self.update_data))
        save_new_button.pack(pady=10)

    def populate_buttons(self):
        for app_name in self.data:
            button = ttk.Button(self.button_frame, text=app_name, command=lambda app=app_name: self.show_password(app))
            button.pack(pady=5)

    def update_data(self):
        for widget in self.button_frame.winfo_children():
            widget.destroy()

        self.data = get_passwords()
        self.populate_buttons()

    def show_password(self, app_name):
        username_hash = self.data[app_name]["username"]
        password_hash = self.data[app_name]["password"]

        if hasattr(self, 'username_entry') and hasattr(self, 'password_entry'):
            self.username_entry.delete(0, tk.END)
            self.password_entry.delete(0, tk.END)


        username_display = username_hash  
        password_display = password_hash  
       
        if not hasattr(self,'username_entry'):
            tk.Label(self.window,text='Username/username').pack()
            self.username_entry=tk.Entry(self.window)
            self.username_entry.pack()
           
            tk.Label(self.window,text='Password').pack()
            self.password_entry=tk.Entry(self.window)
            self.password_entry.pack()

       
        self.username_entry.insert(0, username_display)  
        self.password_entry.insert(0,password_display)


class NewDataWindow:
    def __init__(self, master, update_callback):
        self.window = tk.Toplevel(master)
        self.window.title("Save New Data")
        self.window.geometry("300x300")
        
        tk.Label(self.window, text="Application Name:").pack(pady=5)
        self.app_entry = tk.Entry(self.window)
        self.app_entry.pack(pady=5)

        tk.Label(self.window, text="Username/username:").pack(pady=5)
        self.username_entry = tk.Entry(self.window)
        self.username_entry.pack(pady=5)

        tk.Label(self.window, text="Password:").pack(pady=5)
        self.password_entry = tk.Entry(self.window, show='*')
        self.password_entry.pack(pady=5)

        self.submit_button = ttk.Button(self.window, text="Submit", command= lambda: self.save_data(update_callback))
        self.submit_button.pack(pady=10)

    def save_data(self):
        app_name = self.app_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()

        if app_name and username and password:
            save_password(app_name, username, password)

            self.app_entry.delete(0, tk.END)
            self.username_entry.delete(0, tk.END)
            self.password_entry.delete(0, tk.END)

            messagebox.showinfo("Success", "Data saved successfully!")
            self.window.destroy()
        else:
            messagebox.showwarning("Input Error", "Please enter all fields.")
        
if __name__ == "__main__":
    app = Application()
    app.mainloop()




