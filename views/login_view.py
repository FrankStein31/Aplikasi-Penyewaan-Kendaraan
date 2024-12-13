import tkinter as tk
from tkinter import messagebox, simpledialog
from controllers.auth_controller import AuthController

class LoginView:
    def __init__(self, root):
        self.root = root
        self.root.title("Rental Kendaraan - Login")
        self.root.geometry("400x300")
        
        self.auth_controller = AuthController()
        
        self.create_widgets()
    
    def create_widgets(self):
        # Username Label and Entry
        tk.Label(self.root, text="Username", font=("Arial", 12)).pack(pady=(20, 5))
        self.username_entry = tk.Entry(self.root, font=("Arial", 12), width=30)
        self.username_entry.pack(pady=5)
        
        # Password Label and Entry
        tk.Label(self.root, text="Password", font=("Arial", 12)).pack(pady=(10, 5))
        self.password_entry = tk.Entry(self.root, show="*", font=("Arial", 12), width=30)
        self.password_entry.pack(pady=5)
        
        # Login Button
        login_button = tk.Button(self.root, text="Login", command=self.login, font=("Arial", 12))
        login_button.pack(pady=20)
        
        # Register Button
        register_button = tk.Button(self.root, text="Register", command=self.open_register, font=("Arial", 12))
        register_button.pack()
    
    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        # Validate input
        if not username or not password:
            messagebox.showerror("Error", "Username dan password harus diisi!")
            return
        
        # Attempt login
        user = self.auth_controller.login(username, password)
        if user:
            # Close login window
            self.root.destroy()
            
            # Open appropriate dashboard based on user role
            if user['role'] == 'admin':
                from views.admin_dashboard import AdminDashboard
                admin_root = tk.Tk()
                AdminDashboard(admin_root, user)
                admin_root.mainloop()
            else:
                from views.user_dashboard import UserDashboard
                user_root = tk.Tk()
                UserDashboard(user_root, user)
                user_root.mainloop()
        else:
            messagebox.showerror("Login Gagal", "Username atau password salah!")
    
    def open_register(self):
        # Open registration dialog
        register_window = tk.Toplevel(self.root)
        register_window.title("Registrasi Pengguna")
        register_window.geometry("400x500")
        
        # Registration fields
        fields = [
            ("Nama Lengkap", "nama_lengkap"),
            ("Username", "username"),
            ("Email", "email"),
            ("No Telepon", "no_telepon"),
            ("Password", "password", "password"),
            ("Konfirmasi Password", "konfirmasi_password", "password")
        ]
        
        entry_vars = {}
        
        for i, (label_text, field_name, *entry_type) in enumerate(fields):
            tk.Label(register_window, text=label_text, font=("Arial", 10)).pack(pady=(10 if i==0 else 5, 2))
            
            # Determine entry type (normal or password)
            entry_type = entry_type[0] if entry_type else "normal"
            
            var = tk.StringVar()
            entry = tk.Entry(
                register_window, 
                font=("Arial", 10), 
                width=30, 
                textvariable=var,
                show="*" if entry_type == "password" else ""
            )
            entry.pack(pady=2)
            entry_vars[field_name] = var
        
        def submit_registration():
            # Collect registration data
            reg_data = {
                field: var.get() 
                for field, var in entry_vars.items() 
                if field != "konfirmasi_password"
            }
            
            # Validate password match
            if entry_vars['password'].get() != entry_vars['konfirmasi_password'].get():
                messagebox.showerror("Error", "Password tidak cocok!")
                return
            
            # Attempt registration
            result = self.auth_controller.register(reg_data)
            if result:
                messagebox.showinfo("Sukses", "Registrasi berhasil!")
                register_window.destroy()
            else:
                messagebox.showerror("Gagal", "Registrasi gagal. Coba lagi.")
        
        # Submit button
        submit_btn = tk.Button(
            register_window, 
            text="Daftar", 
            command=submit_registration, 
            font=("Arial", 10)
        )
        submit_btn.pack(pady=20)