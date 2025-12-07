import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog
import json, os

# Configuration globale
COLORS = {"bg": "#f0f0f0", "text": "#FFFFFF"}

# Palette de couleurs pour les modules (Format: "Couleur Normale", "Couleur Survol")
MODULE_PALETTE = [
    ("#1B5886", "#2A7BB6"), # Bleu (Classique)
    ("#2E7D32", "#43A047"), # Vert Forêt
    ("#C62828", "#E53935"), # Rouge Brique
    ("#6A1B9A", "#8E24AA"), # Violet
    ("#E65100", "#EF6C00"), # Orange Foncé
    ("#00695C", "#00897B"), # Sarcelle (Teal)
    ("#455A64", "#607D8B"), # Gris Bleu
]

class Document:
    def __init__(self, title, desc, path, user):
        self.title, self.description, self.file_path = title, desc, path
        self.uploaded_by, self.date = user, "Today"

class Module:
    def __init__(self, name):
        self.name = name
        self.documents = []
    def add_doc(self, title, desc, path, user):
        self.documents.append(Document(title, desc, path, user))

class ModuleFrame(tk.Frame):
    def __init__(self, parent, module, user, colors, open_cb, edit_cb):
        # On récupère la paire de couleurs (bg_color, hover_color)
        self.bg_col, self.hover_col = colors
        
        super().__init__(parent, relief=tk.RAISED, borderwidth=2, bg=self.bg_col, cursor="hand2", width=200, height=120)
        self.pack_propagate(False); self.grid_propagate(False)
        self.module = module
        
        container = tk.Frame(self, bg=self.bg_col)
        container.pack(expand=True, fill=tk.BOTH, padx=5, pady=5)
        
        edit_btn = tk.Label(container, text="✏️", bg=self.bg_col, fg=COLORS["text"], font=('Arial', 8), cursor="hand2")
        edit_btn.place(relx=1.0, rely=0.0, x=-5, y=5, anchor="ne")
        edit_btn.bind("<Button-1>", lambda e: (e.widget.master.focus_set(), edit_cb(module)))
        
        lbl = tk.Label(container, text=module.name, font=('Arial', 10, 'bold'), bg=self.bg_col, fg=COLORS["text"], wraplength=170, justify=tk.CENTER)
        lbl.place(relx=0.5, rely=0.5, anchor="center")
        
        for w in (self, container, lbl): w.bind("<Button-1>", lambda e: open_cb(module))
        
        # Fonction locale pour gérer le changement de couleur au survol
        def on_hover(is_hovering):
            c = self.hover_col if is_hovering else self.bg_col
            self.config(bg=c, relief=tk.SUNKEN if is_hovering else tk.RAISED)
            container.config(bg=c)
            lbl.config(bg=c)
            edit_btn.config(bg=c)
            
        for w in (self, container, lbl, edit_btn):
            w.bind("<Enter>", lambda e: on_hover(True))
            w.bind("<Leave>", lambda e: on_hover(False))

class HomePage(tk.Tk):
    def __init__(self, user):
        super().__init__()
        self.user, self.modules, self.widgets = user, [], []
        self.title("School Organizer"); self.geometry("500x600"); self.configure(bg=COLORS["bg"])
        self.load_data()
        
        head = tk.Frame(self, bg=COLORS["bg"]); head.pack(fill=tk.X, padx=20, pady=15)
        tk.Label(head, text=f"Hello {user}!", font=('Arial', 18, 'bold'), bg=COLORS["bg"]).pack(side=tk.LEFT)
        tk.Button(head, text="+ Add Module", bg="#1B5886", fg="white", command=self.add_mod).pack(side=tk.RIGHT)
        tk.Frame(self, height=2, bg="#cccccc").pack(fill=tk.X, padx=20, pady=10)
        
        container = tk.Frame(self, bg=COLORS["bg"])
        container.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        self.canvas = tk.Canvas(container, bg=COLORS["bg"], highlightthickness=0)
        scr = ttk.Scrollbar(container, command=self.canvas.yview)
        self.frame = tk.Frame(self.canvas, bg=COLORS["bg"])
        
        self.frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scr.set)
        
        self.canvas.pack(side="left", fill="both", expand=True); scr.pack(side="right", fill="y")
        self.canvas.bind_all("<MouseWheel>", lambda e: self.canvas.yview_scroll(int(-1*(e.delta/120)), "units"))
        self.canvas.bind("<Configure>", self.on_resize)
        
        self.refresh()

    def load_data(self):
        if os.path.exists("modules.json"):
            try:
                with open("modules.json", "r", encoding='utf-8') as f:
                    for m in json.load(f).get("modules", []): self.modules.append(Module(m))
            except: pass
        if not self.modules:
            for n in ["Crypto & PKI", "Data Analysis", "Unix OS", "Python OOP", "Network", "Signal Proc.", "TEC"]:
                self.modules.append(Module(n))

    def save_data(self):
        with open("modules.json", "w", encoding='utf-8') as f:
            json.dump({"modules": [m.name for m in self.modules]}, f, indent=2)

    def refresh(self):
        for w in self.frame.winfo_children(): w.destroy()
        self.widgets = []
        
        # --- MODIFICATION ICI : On attribue les couleurs ---
        for i, m in enumerate(self.modules):
            # On utilise le modulo (%) pour boucler sur la palette si on a plus de modules que de couleurs
            colors = MODULE_PALETTE[i % len(MODULE_PALETTE)]
            self.widgets.append(ModuleFrame(self.frame, m, self.user, colors, self.open_mod, self.edit_mod))
            
        self.update_idletasks(); self.rearrange(self.canvas.winfo_width())

    def on_resize(self, event): self.rearrange(event.width)

    def rearrange(self, width):
        cols = max(1, width // 230)
        for i, w in enumerate(self.widgets):
            w.grid_forget()
            w.grid(row=i//cols, column=i%cols, padx=15, pady=15)
            self.frame.grid_columnconfigure(i%cols, weight=1)

    def open_mod(self, m): ModuleWindow(self, m, self.user)
    
    def edit_mod(self, m):
        if (n := simpledialog.askstring("Edit", "Name:", initialvalue=m.name)):
            m.name = n.strip(); self.save_data(); self.refresh()

    def add_mod(self):
        if (n := simpledialog.askstring("Add", "Name:")):
            self.modules.append(Module(n.strip())); self.save_data(); self.refresh()

class ModuleWindow(tk.Toplevel):
    def __init__(self, parent, module, user):
        super().__init__(parent); self.module = module; self.user = user
        self.title(module.name); self.geometry("800x500"); self.configure(bg=COLORS["bg"])
        
        head = tk.Frame(self, bg=COLORS["bg"]); head.pack(fill=tk.X, padx=20, pady=10)
        tk.Label(head, text=module.name, font=('Arial', 14, 'bold'), bg=COLORS["bg"]).pack(side=tk.LEFT)
        tk.Button(head, text="+ Doc", bg="#1B5886", fg="white", command=self.add).pack(side=tk.RIGHT)
        tk.Frame(self, height=2, bg="#ccc").pack(fill=tk.X, padx=20, pady=5)
        
        cols = ("Title", "Desc", "File", "User", "Date")
        self.tree = ttk.Treeview(self, columns=cols, show="headings", height=15)
        for c, w in zip(cols, [150, 200, 150, 100, 80]): 
            self.tree.heading(c, text=c); self.tree.column(c, width=w)
        
        scr = ttk.Scrollbar(self, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scr.set)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(20,0), pady=10)
        scr.pack(side=tk.RIGHT, fill=tk.Y, pady=10, padx=(0,20))
        self.tree.bind("<Double-1>", self.open_file)
        self.load()

    def load(self):
        self.tree.delete(*self.tree.get_children())
        if not self.module.documents: self.tree.insert("", "end", values=("No docs", "Click + Doc", "", "", ""))
        for d in self.module.documents:
            self.tree.insert("", "end", values=(d.title, d.description, os.path.basename(d.file_path), d.uploaded_by, d.date))

    def add(self):
        d = AddDocDialog(self); self.wait_window(d)
        if d.res: self.module.add_doc(*d.res, self.user); self.load()

    def open_file(self, e):
        if (sel := self.tree.selection()):
            t = self.tree.item(sel[0])['values'][0]
            if t != "No docs":
                for d in self.module.documents:
                    if d.title == t:
                        try: os.startfile(d.file_path)
                        except Exception as x: messagebox.showerror("Err", str(x))

class AddDocDialog(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent); self.res = None
        self.title("Add Doc"); self.geometry("450x400"); self.configure(bg=COLORS["bg"])
        self.transient(parent); self.grab_set()
        
        f = tk.Frame(self, bg=COLORS["bg"]); f.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        tk.Label(f, text="Title:", bg=COLORS["bg"], font=('Arial',10,'bold')).grid(row=0, sticky="w")
        self.e_title = tk.Entry(f, width=40); self.e_title.grid(row=0, column=1, pady=5)
        
        tk.Label(f, text="Desc:", bg=COLORS["bg"], font=('Arial',10,'bold')).grid(row=1, sticky="nw", pady=10)
        self.e_desc = tk.Text(f, width=30, height=4); self.e_desc.grid(row=1, column=1, pady=10)
        
        tk.Label(f, text="File:", bg=COLORS["bg"], font=('Arial',10,'bold')).grid(row=2, sticky="w")
        self.path = tk.StringVar()
        self.lbl_file = tk.Label(f, text="None", bg="white", width=30, anchor="w")
        self.lbl_file.grid(row=2, column=1, sticky="ew"); 
        tk.Button(f, text="Browse", command=self.browse).grid(row=3, column=1, sticky="w", pady=5)
        
        tk.Button(f, text="Add", bg="#1B5886", fg="white", command=self.save).grid(row=4, column=0, columnspan=2, pady=20)

    def browse(self):
        if p := filedialog.askopenfilename():
            self.path.set(p); self.lbl_file.config(text=os.path.basename(p))
            if not self.e_title.get(): self.e_title.insert(0, os.path.splitext(os.path.basename(p))[0])

    def save(self):
        if self.e_title.get() and self.path.get() and os.path.exists(self.path.get()):
            self.res = (self.e_title.get(), self.e_desc.get("1.0", "end").strip(), self.path.get())
            self.destroy()
        else: messagebox.showerror("Error", "Missing title or file")

if __name__ == "__main__": HomePage("Test User").mainloop()
