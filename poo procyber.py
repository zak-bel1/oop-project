import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog
import json
import os

# Color scheme
MODULE_COLOR = "#1B5886"
MODULE_HOVER_COLOR = "#2A7BB6"
BG_COLOR = "#f0f0f0"
TEXT_COLOR = "#FFFFFF"

class Document:
    """Class representing a document"""
    def __init__(self, title, description, file_path, uploaded_by):
        self.title = title
        self.description = description
        self.file_path = file_path
        self.uploaded_by = uploaded_by
        self.date = "Today"

class Module:
    """Class representing a module/subject"""
    def __init__(self, name):
        self.name = name
        self.documents = []
    
    def add_document(self, title, description, file_path, uploaded_by):
        document = Document(title, description, file_path, uploaded_by)
        self.documents.append(document)
        return document

class ModuleFrame(tk.Frame):
    """Custom widget for displaying a module"""
    def __init__(self, parent, module, user_name, open_module_callback, edit_callback):
        super().__init__(parent, relief=tk.RAISED, borderwidth=2, 
                        bg=MODULE_COLOR, cursor="hand2")
        self.module = module
        self.user_name = user_name
        self.open_module_callback = open_module_callback
        self.edit_callback = edit_callback
        
        # Fixed size to prevent layout changes
        self.configure(width=200, height=120)
        self.pack_propagate(False)
        self.grid_propagate(False)
        
        self.setup_ui()
    
    def setup_ui(self):
        # Main container frame inside the module
        container = tk.Frame(self, bg=MODULE_COLOR)
        container.pack(expand=True, fill=tk.BOTH, padx=5, pady=5)
        
        # Edit button (always present but transparent initially)
        self.edit_button = tk.Label(
            container, 
            text="✏️", 
            bg=MODULE_COLOR,
            fg=TEXT_COLOR,
            font=('Arial', 8),
            cursor="hand2"
        )
        self.edit_button.place(relx=1.0, rely=0.0, x=-5, y=5, anchor="ne")
        self.edit_button.bind("<Button-1>", lambda e: self.edit_callback(self.module))
        
        # Module name label - centered
        self.name_label = tk.Label(
            container, 
            text=self.module.name, 
            font=('Arial', 10, 'bold'),
            bg=MODULE_COLOR,
            fg=TEXT_COLOR,
            wraplength=170,
            justify=tk.CENTER,
            cursor="hand2"
        )
        # Center the label
        self.name_label.place(relx=0.5, rely=0.5, anchor="center")
        
        # Clickable area - bind to the entire frame
        self.bind("<Button-1>", self.on_click)
        self.name_label.bind("<Button-1>", self.on_click)
        container.bind("<Button-1>", self.on_click)
        
        # Bind hover events
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        container.bind("<Enter>", self.on_enter)
        container.bind("<Leave>", self.on_leave)
        self.name_label.bind("<Enter>", self.on_enter)
        self.name_label.bind("<Leave>", self.on_leave)
        self.edit_button.bind("<Enter>", self.on_enter)
        self.edit_button.bind("<Leave>", self.on_leave)
    
    def on_click(self, event):
        # Don't trigger module open if edit button was clicked
        if event.widget == self.edit_button:
            event.widget.master.focus_set()  # Prevent event propagation
            return
        self.open_module_callback(self.module)
    
    def on_enter(self, event):
        self.configure(bg=MODULE_HOVER_COLOR, relief=tk.SUNKEN)
        self.name_label.configure(bg=MODULE_HOVER_COLOR)
        self.edit_button.configure(bg=MODULE_HOVER_COLOR)
    
    def on_leave(self, event):
        self.configure(bg=MODULE_COLOR, relief=tk.RAISED)
        self.name_label.configure(bg=MODULE_COLOR)
        self.edit_button.configure(bg=MODULE_COLOR)

class HomePage(tk.Tk):
    """Main home page window"""
    def __init__(self, user_name):
        super().__init__()
        self.user_name = user_name
        self.modules = []
        
        self.title("School Document Organizer")
        self.geometry("900x600")
        self.configure(bg=BG_COLOR)
        
        # Try to load existing modules
        self.load_modules()
        
        # If no modules exist, create default ones
        if not self.modules:
            self.create_default_modules()
        
        self.setup_ui()
    
    def create_default_modules(self):
        """Create default modules"""
        default_modules = [
            "Cryptographie et pki (crypto+ mecanique quantique)",
            "Analyse de données",
            "Système d'exploitation unix",
            "POO Python",
            "Réseau",
            "Traitement de signale",
            "TEC"
        ]
        
        for module_name in default_modules:
            self.modules.append(Module(module_name))
        
        self.save_modules()
    
    def load_modules(self):
        """Load modules from file"""
        try:
            if os.path.exists("modules.json"):
                with open("modules.json", "r", encoding='utf-8') as f:
                    data = json.load(f)
                    for module_name in data.get("modules", []):
                        self.modules.append(Module(module_name))
        except Exception as e:
            print(f"Error loading modules: {e}")
    
    def save_modules(self):
        """Save modules to file"""
        try:
            data = {
                "modules": [module.name for module in self.modules]
            }
            with open("modules.json", "w", encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error saving modules: {e}")
    
    def setup_ui(self):
        # Header frame with welcome message
        header_frame = tk.Frame(self, bg=BG_COLOR)
        header_frame.pack(fill=tk.X, padx=20, pady=15)
        
        welcome_label = tk.Label(
            header_frame,
            text=f"Hello {self.user_name}!",
            font=('Arial', 18, 'bold'),
            bg=BG_COLOR
        )
        welcome_label.pack(side=tk.LEFT)
        
        # Add module button (for responsable)
        add_module_btn = tk.Button(
            header_frame,
            text="+ Add Module",
            bg=MODULE_COLOR,
            fg=TEXT_COLOR,
            font=('Arial', 10, 'bold'),
            relief=tk.RAISED,
            cursor="hand2",
            command=self.add_module
        )
        add_module_btn.pack(side=tk.RIGHT)
        
        # Separator
        separator = tk.Frame(self, height=2, bg="#cccccc")
        separator.pack(fill=tk.X, padx=20, pady=10)
        
        # Title for modules section
        modules_title = tk.Label(
            self,
            text="Your Modules",
            font=('Arial', 14, 'bold'),
            bg=BG_COLOR
        )
        modules_title.pack(pady=(0, 10))
        
        # Main container for modules
        container = tk.Frame(self, bg=BG_COLOR)
        container.pack(fill=tk.BOTH, expand=True, padx=40, pady=10)
        
        # Scrollable canvas for modules pour donner l utilisateure la possibilite d ajouter autres modules pour l admin ou bien des module personales.
        canvas = tk.Canvas(container, bg=BG_COLOR, highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        
        self.modules_frame = tk.Frame(canvas, bg=BG_COLOR)
        self.modules_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.modules_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Bind mouse wheel to scroll
        canvas.bind_all("<MouseWheel>", 
                       lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))
        
        self.display_modules()
    
    def display_modules(self):
        """Display all modules in a grid"""
        # Clear existing modules
        for widget in self.modules_frame.winfo_children():
            widget.destroy()
        
        # Create modules in a grid (3 columns)
        for i, module in enumerate(self.modules):
            row = i // 3
            col = i % 3
            
            module_frame = ModuleFrame(
                self.modules_frame,
                module,
                self.user_name,
                self.open_module,
                self.edit_module
            )
            module_frame.grid(row=row, column=col, padx=15, pady=15, sticky="nsew")
            
            # Configure grid to center modules
            self.modules_frame.grid_columnconfigure(col, weight=1, minsize=220)
            self.modules_frame.grid_rowconfigure(row, weight=1, minsize=140)
    
    def open_module(self, module):
        """Open module documents window"""
        ModuleWindow(self, module, self.user_name)
    
    def edit_module(self, module):
        """Edit module name"""
        new_name = simpledialog.askstring(
            "Edit Module",
            "Enter new module name:",
            initialvalue=module.name
        )
        
        if new_name and new_name.strip():
            module.name = new_name.strip()
            self.save_modules()
            self.display_modules()
    
    def add_module(self):
        """Add a new module"""
        new_name = simpledialog.askstring(
            "Add Module",
            "Enter module name:"
        )
        
        if new_name and new_name.strip():
            self.modules.append(Module(new_name.strip()))
            self.save_modules()
            self.display_modules()

class ModuleWindow(tk.Toplevel):
    """Window for viewing and adding documents to a module"""
    def __init__(self, parent, module, user_name):
        super().__init__(parent)
        self.module = module
        self.user_name = user_name
        
        self.title(f"{module.name} - Documents")
        self.geometry("800x500")
        self.configure(bg=BG_COLOR)
        
        self.setup_ui()
        self.load_documents()
    
    def setup_ui(self):
        # Header
        header_frame = tk.Frame(self, bg=BG_COLOR)
        header_frame.pack(fill=tk.X, padx=20, pady=10)
        
        title_label = tk.Label(
            header_frame,
            text=self.module.name,
            font=('Arial', 14, 'bold'),
            bg=BG_COLOR
        )
        title_label.pack(side=tk.LEFT)
        
        # Add document button
        add_doc_btn = tk.Button(
            header_frame,
            text="+ Add Document",
            bg=MODULE_COLOR,
            fg=TEXT_COLOR,
            font=('Arial', 10, 'bold'),
            relief=tk.RAISED,
            cursor="hand2",
            command=self.add_document
        )
        add_doc_btn.pack(side=tk.RIGHT)
        
        # Separator
        separator = tk.Frame(self, height=2, bg="#cccccc")
        separator.pack(fill=tk.X, padx=20, pady=5)
        
        # Documents list frame
        docs_frame = tk.Frame(self, bg=BG_COLOR)
        docs_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Title for documents
        docs_title = tk.Label(
            docs_frame,
            text="Module Documents",
            font=('Arial', 12, 'bold'),
            bg=BG_COLOR
        )
        docs_title.pack(anchor=tk.W, pady=(0, 10))
        
        # Create Treeview for documents
        style = ttk.Style()
        style.configure("Custom.Treeview", 
                       background="#FFFFFF", 
                       fieldbackground="#FFFFFF",
                       rowheight=25)
        style.configure("Custom.Treeview.Heading", 
                       font=('Arial', 10, 'bold'),
                       background=MODULE_COLOR,
                       foreground=TEXT_COLOR)
        
        columns = ("Title", "Description", "File Name", "Uploaded By", "Date")
        self.tree = ttk.Treeview(docs_frame, columns=columns, show="headings", 
                                style="Custom.Treeview", height=15)
        
        # Configure columns
        for col in columns:
            self.tree.heading(col, text=col)
        
        self.tree.column("Title", width=150)
        self.tree.column("Description", width=200)
        self.tree.column("File Name", width=150)
        self.tree.column("Uploaded By", width=120)
        self.tree.column("Date", width=80)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(docs_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack tree and scrollbar
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Double-click to open document
        self.tree.bind("<Double-1>", self.open_document)
    
    def load_documents(self):
        """Load and display documents in the treeview"""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Add documents
        for doc in self.module.documents:
            file_name = os.path.basename(doc.file_path) if doc.file_path else ""
            self.tree.insert("", tk.END, values=(
                doc.title,
                doc.description,
                file_name,
                doc.uploaded_by,
                doc.date
            ))
        
        # If no documents, show message
        if not self.module.documents:
            self.tree.insert("", tk.END, values=(
                "No documents yet",
                "Click 'Add Document' to upload",
                "",
                "",
                ""
            ))
    
    def add_document(self):
        """Open dialog to add a new document"""
        dialog = AddDocumentDialog(self, self.module, self.user_name)
        self.wait_window(dialog)
        
        if dialog.result:
            title, description, file_path = dialog.result
            self.module.add_document(title, description, file_path, self.user_name)
            self.load_documents()
    
    def open_document(self, event):
        """Handle document opening"""
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            title = item['values'][0]
            if title != "No documents yet":
                # Find the document
                for doc in self.module.documents:
                    if doc.title == title:
                        try:
                            # Try to open the file with default application
                            os.startfile(doc.file_path)
                        except Exception as e:
                            messagebox.showerror("Error", f"Cannot open file:\n{str(e)}")
                        break

class AddDocumentDialog(tk.Toplevel):
    """Dialog for adding a new document"""
    def __init__(self, parent, module, user_name):
        super().__init__(parent)
        self.module = module
        self.user_name = user_name
        self.result = None
        
        self.title(f"Add Document to {module.name}")
        self.geometry("450x400")
        self.configure(bg=BG_COLOR)
        self.transient(parent)
        self.grab_set()
        
        self.setup_ui()
    
    def setup_ui(self):
        main_frame = tk.Frame(self, bg=BG_COLOR)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        tk.Label(main_frame, text="Title:", bg=BG_COLOR, 
                font=('Arial', 10, 'bold')).grid(row=0, column=0, 
                sticky=tk.W, pady=(0, 5))
        self.title_entry = tk.Entry(main_frame, width=40, font=('Arial', 10))
        self.title_entry.grid(row=0, column=1, pady=(0, 5), padx=5)
        self.title_entry.focus_set()
        
        # Description
        tk.Label(main_frame, text="Description:", bg=BG_COLOR,
                font=('Arial', 10, 'bold')).grid(row=1, column=0, 
                sticky=tk.NW, pady=(10, 5))
        self.desc_text = tk.Text(main_frame, width=30, height=4, 
                                font=('Arial', 10))
        self.desc_text.grid(row=1, column=1, pady=(10, 5), padx=5)
        
        # File selection section
        tk.Label(main_frame, text="Select File:", bg=BG_COLOR,
                font=('Arial', 10, 'bold')).grid(row=2, column=0, 
                sticky=tk.W, pady=(10, 5))
        
        # Frame for file selection
        file_frame = tk.Frame(main_frame, bg=BG_COLOR)
        file_frame.grid(row=2, column=1, pady=(10, 5), padx=5, sticky=tk.W+tk.E)
        
        # File path display
        self.file_path_var = tk.StringVar()
        file_display_frame = tk.Frame(file_frame, bg=BG_COLOR, relief=tk.SUNKEN, borderwidth=1)
        file_display_frame.pack(fill=tk.X, expand=True, pady=(0, 5))
        
        self.file_label = tk.Label(file_display_frame, 
                                  text="No file selected",
                                  bg="#FFFFFF",
                                  fg="#666666",
                                  anchor=tk.W,
                                  relief=tk.FLAT,
                                  padx=5)
        self.file_label.pack(fill=tk.X, expand=True)
        
        # Browse button
        browse_btn = tk.Button(file_frame, text="Browse Files...", 
                              bg=MODULE_COLOR, fg=TEXT_COLOR,
                              font=('Arial', 10, 'bold'),
                              cursor="hand2",
                              command=self.browse_file)
        browse_btn.pack(pady=(5, 0))
        
        # File types filter - you can customize these
        self.filetypes = [
            ("All files", "*.*"),
            ("PDF files", "*.pdf"),
            ("Word documents", "*.doc *.docx"),
            ("Excel files", "*.xls *.xlsx"),
            ("PowerPoint files", "*.ppt *.pptx"),
            ("Text files", "*.txt"),
            ("Image files", "*.jpg *.jpeg *.png *.gif"),
            ("Python files", "*.py"),
        ]
        
        # Selected file info
        self.selected_file_info = tk.Label(main_frame, 
                                          text="",
                                          bg=BG_COLOR,
                                          fg="#666666",
                                          font=('Arial', 8))
        self.selected_file_info.grid(row=3, column=1, sticky=tk.W, padx=5)
        
        # Buttons frame
        button_frame = tk.Frame(main_frame, bg=BG_COLOR)
        button_frame.grid(row=4, column=0, columnspan=2, pady=20)
        
        add_btn = tk.Button(button_frame, text="Add Document", 
                           bg=MODULE_COLOR, fg=TEXT_COLOR,
                           font=('Arial', 10, 'bold'),
                           width=15, cursor="hand2",
                           command=self.add)
        add_btn.pack(side=tk.LEFT, padx=5)
        
        cancel_btn = tk.Button(button_frame, text="Cancel", 
                              bg="#cccccc", fg="#000000",
                              width=15, cursor="hand2",
                              command=self.cancel)
        cancel_btn.pack(side=tk.LEFT, padx=5)
    
    def browse_file(self):
        """Open file dialog to browse and select a file"""
        file_path = filedialog.askopenfilename(
            title="Select a document",
            initialdir="/",  # Start from root directory
            filetypes=self.filetypes
        )
        
        if file_path:
            # Display file name
            file_name = os.path.basename(file_path)
            self.file_label.config(text=file_name, fg="#000000")
            self.file_path_var.set(file_path)
            
            # Show file info
            try:
                file_size = os.path.getsize(file_path)
                file_size_str = self.format_file_size(file_size)
                self.selected_file_info.config(
                    text=f"File: {file_name} | Size: {file_size_str}"
                )
            except:
                self.selected_file_info.config(text=f"File: {file_name}")
            
            # Auto-fill title if empty
            if not self.title_entry.get().strip():
                # Use filename without extension as default title
                title = os.path.splitext(file_name)[0]
                self.title_entry.insert(0, title)
    
    def format_file_size(self, size_bytes):
        """Convert file size to human readable format"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.1f} TB"
    
    def add(self):
        """Add document with validation"""
        title = self.title_entry.get().strip()
        description = self.desc_text.get("1.0", tk.END).strip()
        file_path = self.file_path_var.get()
        
        if not title:
            messagebox.showerror("Error", "Please enter a document title")
            return
        
        if not file_path:
            messagebox.showerror("Error", "Please select a file")
            return
        
        # Check if file exists
        if not os.path.exists(file_path):
            messagebox.showerror("Error", f"File not found:\n{file_path}")
            return
        
        self.result = (title, description, file_path)
        self.destroy()
    
    def cancel(self):
        """Cancel adding document"""
        self.destroy()

# Main application entry point
def main(user_name):
    """Start the home page with the logged-in user's name"""
    app = HomePage(user_name)
    app.mainloop()

# For testing without your login system
if __name__ == "__main__":
    # Replace "Test User" with actual username from your login
    main("Test User")