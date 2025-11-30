import customtkinter as ctk 
import tkinter as tk
from tkinter import ttk, messagebox

class sign_in(tk.Tk):
    def show_password(self):
        if self.show_var.get():
            self.password_entry.config(show="")
        else:
            self.password_entry.config(show="*")     
    def __init__(self):
        super().__init__()
        self.title("creation de compte")
        self.geometry("400x500")
        self.iconbitmap("education.ico")
        self.resizable(True, True)
        container = tk.Frame(self)
        container.grid(row=0, column=0, sticky="nsew")
        style = ttk.Style()
        style.configure("blue_under.TEntry", padding=5, relief="raised", borderwidth=2)
        for i in range(10):
            self.grid_rowconfigure(i, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.title_label = tk.Label(self,
                               font=("Britannic Bold",35),
                               text="creer un compte",
                               fg="black")
        self.title_label.grid(row=0, column=0, columnspan=2, pady=5)
        self.title_label = tk.Label(self,
                               font=("arial",18),
                               text="*veillez renseigner tous les champs",
                               fg="black")
        self.title_label.grid(row=1, column=0, columnspan=2, pady=5)  
        self.firstname_label= tk.Label(self,
                             font=("Arial", 18),
                             text="prenom",
                             fg="black")
        self.firstname_label.grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.entry=ttk.Entry(self,
                            style="blue_under.TEntry",
                            font=("Arial", 18),
                            width=30)
        self.entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")
        self.nom_label= tk.Label(self,
                             font=("Arial", 18),
                             text="nom",
                             fg="black")
        self.nom_label.grid(row=3, column=0, padx=10, pady=5, sticky="e")
        self.entry=ttk.Entry(self,
                            style="blue_under.TEntry",
                            font=("Arial", 18),
                            width=30)
        self.entry.grid(row=3, column=1, padx=10, pady=5, sticky="w")
        self.mail_label= tk.Label(self,
                             font=("Arial", 18),
                             text="email",
                             fg="black")
        self.mail_label.grid(row=4, column=0, padx=10, pady=5, sticky="e")
        self.entry=ttk.Entry(self,
                            style="blue_under.TEntry",
                            font=("Arial", 18),
                            width=30)
        self.entry.grid(row=4, column=1, padx=10, pady=5, sticky="w")
        self.password_label= tk.Label(self,
                                      font=("Arial", 18),
                                      text="mot de passe",
                                        fg="black")
        self.password_label.grid(row=5, column=0, padx=10, pady=5, sticky="e")
        self.password_entry=ttk.Entry(self,
                                      style="blue_under.TEntry",
                                      font=("Arial", 18),
                                      width=30,
                                      show="*")
        self.password_entry.grid(row=5, column=1, padx=10, pady=5, sticky="w")
        self.show_var = tk.BooleanVar()  # use tk.BooleanVar()
        self.show_checkbox = tk.Checkbutton(self,
                                              text="Show password",
                                                variable=self.show_var,
                                                command=self.show_password)
        self.show_checkbox.grid(row=6, column=1, padx=10, pady=5, sticky="w")
        self.checkpassword_label= tk.Label(self,
                                      font=("Arial", 18),
                                      text="reecrire mot de passe",
                                        fg="black")
        self.checkpassword_label.grid(row=7, column=0, padx=10, pady=5, sticky="e")
        self.checkpassword_entry=ttk.Entry(self,
                                      style="blue_under.TEntry",
                                      font=("Arial", 18),
                                      width=30,
                                      show="*")
        self.checkpassword_entry.grid(row=7, column=1, padx=10, pady=5, sticky="w")
        ctk.set_appearance_mode("light")
        self.filliaire_label = tk.Label(self, font=("Arial", 18), text="filliaire", fg="black")
        self.filliaire_label.grid(row=8, column=0, padx=10, pady=5, sticky="e")
        self.filliere_combo = ctk.CTkComboBox(self,
                                              values=["SEECS", "GI", "RSSP", "GIL", "GCDSTE"],
                                              font=("Arial", 16))

        self.filliere_combo.set("choisir filliere")
        self.filliere_combo.grid(row=8, column=1, padx=10, pady=5, sticky="w")
        self.genre = tk.StringVar()
        tk.Radiobutton(self, text="1ere année", value="1", variable=self.genre).grid(row=9, column=1, padx=10, pady=5, sticky="w")
        tk.Radiobutton(self, text="2emme année", value="2", variable=self.genre).grid(row=10, column=1, padx=10, pady=5, sticky="w")
        tk.Radiobutton(self, text="3emme année", value="3", variable=self.genre).grid(row=11, column=1, padx=10, pady=5, sticky="w")         
        btn3 = ctk.CTkButton(
            self,
            text="cree un compte",
            font=("Arial", 22),
            corner_radius=10,
            width=200,
            height=45,
            command=lambda: print("cree un compte clicked"))
        btn3.grid(row=12, column=0, columnspan=2, pady=5)
       
app = sign_in()
app.mainloop()