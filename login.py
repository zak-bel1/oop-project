import customtkinter as ctk 
import tkinter as tk
from tkinter import ttk, messagebox
from sign_in import open_sign_in



class log_in(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("identification")
        self.geometry("400x500")
        self.iconbitmap("education.ico")
        self.resizable(True, True)
        
        container = tk.Frame(self)
        container.grid(row=0, column=0, sticky="nsew")
        
        # style
        style = ttk.Style()
        style.configure("blue_under.TEntry", padding=5, relief="raised", borderwidth=2)
        
        # grid
        for i in range(6):
            self.grid_rowconfigure(i, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        # Title
        self.title_label = tk.Label(self,
                               font=("Britannic Bold",35),
                               text="sign in Page",
                               fg="blue")
        self.title_label.grid(row=0, column=0, columnspan=2, pady=30)
        
        # Email
        self.mail_label= tk.Label(self,
                             font=("Arial", 18),
                             text="email",
                             fg="black")
        self.mail_label.grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.entry=ttk.Entry(self,
                            style="blue_under.TEntry",
                            font=("Arial", 18),
                            width=30)
        self.entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")
        # Password
        self.password_label= tk.Label(self,
                                      font=("Arial", 18),
                                      text="password",
                                        fg="black")
        self.password_label.grid(row=2, column=0, padx=10, pady=10, sticky="e")
        self.password_entry=ttk.Entry(self,
                                      style="blue_under.TEntry",
                                      font=("Arial", 18),
                                      width=30,
                                      show="*")
        self.password_entry.grid(row=2, column=1, padx=10, pady=10, sticky="w")
        #button
        btn3 = ctk.CTkButton(
            self,
            text="sign in",
            font=("Arial", 22),
            corner_radius=10,
            width=200,
            height=45,
            command=lambda: print("sign in clicked"))
        btn3.grid(row=3, column=0, columnspan=2, pady=10)

        link_frame = tk.Frame(self)
        link_frame.grid(row=4, column=0, columnspan=2)
        self.title_label = tk.Label(link_frame,
                                    font=("arial",15),
                                    text="Pour creer un compte",
                                    fg="black")
        self.title_label.grid(row=4, column=0, pady=10, sticky="e")
        # sign up link
        label = tk.Label(link_frame, 
                         text="Click here", 
                         fg="blue", 
                         font=("Arial", 15),
                         cursor="hand2")
        label.grid(row=4, column=1, padx=5, sticky="w")
        label.bind("<Button-1>", lambda e: self.go_to_sign_in())
    def go_to_sign_in(self):
        self.destroy()   
        open_sign_in()   

app = log_in()
app.mainloop()