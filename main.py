# IMPORTING THINGS
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo
import os

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
            pass

    def button_clickedIn(self):
            pass


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

        username_entry = ttk.Entry(self.window)
        username_entry.pack(pady=5)

        password_label = ttk.Label(self.window, text="Password: ")
        password_label.pack(pady=5)

        password_entry = ttk.Entry(self.window, show="*")
        password_entry.pack(pady = 5)

        submit_button = ttk.Button(self.window, text="Submit", command=self.submit)
        submit_button.pack(pady=5)

    def close_window(self):
        self.window.destroy()

    def submit(self):
        submit_label = ttk.Label(self.window, text="Submitted!", foreground="green", font=("Arial", 15))
        submit_label.pack()

        
if __name__ == "__main__":
    app = Application()
    app.mainloop()




