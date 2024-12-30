# IMPORTING THINGS
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo
from tkinter import messagebox
from user_data_manager import hash_password, save_credentials, verify_credentials

# MAIN APPLICATION INTERFACE
class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("User Data Management App")
        self.geometry('640x480')

        style = ttk.Style()
        style.configure('TButton',background='green', foreground='yellow', font=('Arial', 24), borderwidth=20 )
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
        self.window.geometry("640x480")
            
        self.back_button = ttk.Button(self.window, text="Back", command=self.close_window)
        self.back_button.pack(side=tk.TOP, anchor=tk.NE, padx=10, pady=10)

        sign_up_label = ttk.Label(self.window, text="Sign Up Here", font=("Arial", 16))
        sign_up_label.pack(pady=20)

        username_label = ttk.Label(self.window, text="Username: ")
        username_label.pack(pady=5)

        self.username_entry = ttk.Entry(self.window)
        self.username_entry.pack(pady=5)

        password_label = ttk.Label(self.window, text="Password: ")
        password_label.pack(pady=5)

        self.password_entry = ttk.Entry(self.window, show="*")
        self.password_entry.pack(pady = 5)

        submit_button = ttk.Button(self.window, text="Submit", command=self.submit)
        submit_button.pack(pady=5)

    def close_window(self):
        self.window.destroy()

    def submit(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username and password:
            if len(password) < 5:
                messagebox.showwarning("Input Error", "Password shall have more than five characters and shall not contain spaces.")
            elif " " in password:
                messagebox.showwarning("Input Error.", "Password shall have more than five characters and shall not contain spaces.")
            else:
                hashed_password = hash_password(password)

                if save_credentials(username, hashed_password):
                    messagebox.showinfo("Success", "Sign Up Successful!")
                    submitLable = ttk.Label(self.window, foreground="green", text="Submitted!", font=("Arial", 15))
                    submitLable.pack(pady=3)
                    self.window.destroy()
                else:
                     messagebox.showwarning("Error", "Username Already Exists.")
        else:
            messagebox.showwarning("Input Error", "Please enter both email and password.")

class SignInWindow:
    def __init__(self, master):
        self.window = tk.Toplevel(master)
        self.window.title("Login")
        self.window.geometry("400x300")

        tk.Label(self.window, text = "Login Here", font=("Arial", 16)).pack(pady=20)

        tk.Label(self.window, text="Username:").pack(pady=5)
        self.username_entry = tk.Entry(self.window)
        self.username_entry.pack(pady=5)

        tk.Label(self.window, text="Password:").pack(pady=5)
        self.password_entry = tk.Entry(self.window, show='*')
        self.password_entry.pack(pady=5)

        SignIn_button = ttk.Button(self.window, text="Sign In", command=self.SignIn)
        SignIn_button.pack(pady=10)

    def SignIn(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username and password:
            if verify_credentials(username, password):
                messagebox.showinfo("Success", "Login Successful!")
                self.window.destroy()

            else:
                messagebox.showwarning("Error", "Incorrect email or password!")
        else:
            messagebox.showwarning("Input Error", "Please enter both email and password.")

    


        
if __name__ == "__main__":
    app = Application()
    app.mainloop()




