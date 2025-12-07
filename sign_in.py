import customtkinter as ctk 
import tkinter as tk
from tkinter import ttk, messagebox

class sign_in(tk.Tk):
    def show_password(self):
        if self.show_var.get():
            self.password_entry.config(show="")
        else:
            self.password_entry.config(show="*") 

    def toggle_delegate_section(self):
        """Show/hide the delegate code field."""
        if self.delegate_visible:
            self.delegate_frame.grid_forget()
            self.delegate_visible = False
        else:
            self.delegate_frame.grid(row=12, column=0, columnspan=2, padx=5, pady=5, sticky="n")
            self.delegate_visible = True

    def check_if_full(self):
        if not self.firstname_entry.get():
            messagebox.showerror("Erreur", "Veuillez entrer votre prénom.")
            return
        if not self.nom_entry.get():
            messagebox.showerror("Erreur", "Veuillez entrer votre nom.")
            return
        if not self.mail_entry.get():
            messagebox.showerror("Erreur", "Veuillez entrer votre email.")
            return
        if not self.password_entry.get():
            messagebox.showerror("Erreur", "Veuillez entrer un mot de passe.")
            return
        if not self.checkpassword_entry.get():
            messagebox.showerror("Erreur", "Veuillez réécrire votre mot de passe.")
            return
        
        if self.password_entry.get() != self.checkpassword_entry.get():
            messagebox.showerror("Erreur", "Les mots de passe ne correspondent pas.")
            return

        if self.filliere_combo.get() == "choisir filliere":
            messagebox.showerror("Erreur", "Veuillez choisir une filière.")
            return

        if self.genre.get() not in ["1", "2", "3"]:
            messagebox.showerror("Erreur", "Veuillez choisir une année.")
            return
        if self.delegate_visible:
            secret = self.delegate_code_entry.get()
            if secret != "adminENSA":  
                messagebox.showerror("Erreur", "Code délégué incorrect.")
                return
        messagebox.showinfo("Succès", "Compte créé avec succès !")    
    def __init__(self):
        super().__init__()
        self.title("creation de compte")
        self.geometry("400x500")
        self.iconbitmap("education.ico")
        self.resizable(True, True)
        #the style
        style = ttk.Style()
        style.configure("blue_under.TEntry", padding=5, relief="raised", borderwidth=2)
        #make the grid
        for i in range(15):
            self.grid_rowconfigure(i, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        #the title
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
        #first name  
        self.firstname_label= tk.Label(self,
                             font=("Arial", 18),
                             text="prenom",
                             fg="black")
        self.firstname_label.grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.firstname_entry=ttk.Entry(self,
                            style="blue_under.TEntry",
                            font=("Arial", 18),
                            width=30)
        self.firstname_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")
        #LAST NAME
        self.nom_label= tk.Label(self,
                             font=("Arial", 18),
                             text="nom",
                             fg="black")
        self.nom_label.grid(row=3, column=0, padx=10, pady=5, sticky="e")
        self.nom_entry=ttk.Entry(self,
                            style="blue_under.TEntry",
                            font=("Arial", 18),
                            width=30)
        self.nom_entry.grid(row=3, column=1, padx=10, pady=5, sticky="w")
        #MAIL
        self.mail_label= tk.Label(self,
                             font=("Arial", 18),
                             text="email",
                             fg="black")
        self.mail_label.grid(row=4, column=0, padx=10, pady=5, sticky="e")
        self.mail_entry=ttk.Entry(self,
                            style="blue_under.TEntry",
                            font=("Arial", 18),
                            width=30)
        self.mail_entry.grid(row=4, column=1, padx=10, pady=5, sticky="w")
        #PASSWORD
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
        #SHOW THE PASSWORD
        self.show_var = tk.BooleanVar() 
        self.show_checkbox = tk.Checkbutton(self,
                                              text="Show password",
                                                variable=self.show_var,
                                                command=self.show_password)
        self.show_checkbox.grid(row=6, column=1, padx=10, pady=5, sticky="w")
        #REWRITE PASSWORD
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
        #SCROOL FOR FILLIERE
        self.filliere_label = tk.Label(self, font=("Arial", 18), text="filliere", fg="black")
        self.filliere_label.grid(row=8, column=0, padx=10, pady=5, sticky="e")
        self.filliere_combo = ctk.CTkComboBox(self,
                                              values=["SEECS", "GI", "RSSP", "GIL", "GCDSTE"],
                                              font=("Arial", 16))

        self.filliere_combo.set("choisir filliere")
        self.filliere_combo.grid(row=8, column=1, padx=10, pady=5, sticky="w")
        #RADIO BUTTON FOR YEAR
        self.genre = tk.StringVar()
        tk.Radiobutton(self, text="1ere année", value="1", variable=self.genre).grid(row=9, column=1, padx=10, pady=5, sticky="w")
        tk.Radiobutton(self, text="2emme année", value="2", variable=self.genre).grid(row=10, column=1, padx=10, pady=5, sticky="w")
        tk.Radiobutton(self, text="3emme année", value="3", variable=self.genre).grid(row=11, column=1, padx=10, pady=5, sticky="w")  
        #code de delegue
        self.delegate_visible = False

        self.delegate_button = ctk.CTkButton(
            self,
            text="Cliquez si vous êtes délégué",
            font=("Arial", 16),
            width=200,
            command=self.toggle_delegate_section)
        #place de code de delegue
        self.delegate_frame = tk.Frame(self)

        self.delegate_label = tk.Label(
            self.delegate_frame,
            text="Code secret délégué:",
            font=("Arial", 16)
        )
        self.delegate_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")

        self.delegate_code_entry = ttk.Entry(
            self.delegate_frame,
            style="blue_under.TEntry",
            font=("Arial", 16),
            width=20,
            show="*"
        )
        self.delegate_code_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")    
        self.delegate_button.grid(row=13, column=0, columnspan=2, pady=5)
        #BUTTON TO CREATE ACCOUNT       
        btn3 = ctk.CTkButton(
            self,
            text="cree un compte",
            font=("Arial", 22),
            corner_radius=10,
            width=200,
            height=45,
            command=self.check_if_full)
        btn3.grid(row=14, column=0, columnspan=2, pady=5)
def open_sign_in():
    app = sign_in()
    app.mainloop()
if __name__ == "__main__":
    app = sign_in()
    app.mainloop()