import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from controllers.admin_controller import AdminController

class AdminDashboard:
    def __init__(self, root, user):
        self.root = root
        self.root.title(f"Admin Dashboard - {user['nama_lengkap']}")
        self.root.geometry("800x600")
        
        self.user = user
        self.admin_controller = AdminController()
        
        # Create notebook (tabbed interface)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill='both', padx=10, pady=10)
        
        # Create tabs
        self.create_vehicle_type_tab()
        self.create_vehicle_tab()
        self.create_user_tab()
        self.create_payment_tab()
        self.create_rental_history_tab()
    
    def create_vehicle_type_tab(self):
        # Vehicle Type Management Tab
        vehicle_type_frame = ttk.Frame(self.notebook)
        self.notebook.add(vehicle_type_frame, text="Jenis Kendaraan")
        
        # Treeview for vehicle types
        columns = ('ID', 'Nama', 'Deskripsi')
        self.vehicle_type_tree = ttk.Treeview(vehicle_type_frame, columns=columns, show='headings')
        for col in columns:
            self.vehicle_type_tree.heading(col, text=col)
        self.vehicle_type_tree.pack(expand=True, fill='both', padx=10, pady=10)
        
        # Buttons
        btn_frame = tk.Frame(vehicle_type_frame)
        btn_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Button(btn_frame, text="Tambah", command=self.add_vehicle_type).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Edit", command=self.edit_vehicle_type).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Hapus", command=self.delete_vehicle_type).pack(side='left', padx=5)
        
        # Load initial data
        self.load_vehicle_types()
    
    def load_vehicle_types(self):
        # Clear existing items
        for i in self.vehicle_type_tree.get_children():
            self.vehicle_type_tree.delete(i)
        
        # Fetch and populate vehicle types
        vehicle_types = self.admin_controller.get_vehicle_types()
        for vtype in vehicle_types:
            self.vehicle_type_tree.insert('', 'end', values=(
                vtype['id'], vtype['nama'], vtype['deskripsi']
            ))
    
    def add_vehicle_type(self):
        # Open dialog for adding vehicle type
        nama = simpledialog.askstring("Tambah Jenis Kendaraan", "Nama Jenis Kendaraan:")
        if nama:
            deskripsi = simpledialog.askstring("Tambah Jenis Kendaraan", "Deskripsi:")
            result = self.admin_controller.add_vehicle_type(nama, deskripsi)
            if result:
                messagebox.showinfo("Sukses", "Jenis kendaraan berhasil ditambahkan")
                self.load_vehicle_types()
    
    def edit_vehicle_type(self):
        # Get selected item
        selected = self.vehicle_type_tree.selection()
        if not selected:
            messagebox.showwarning("Peringatan", "Pilih jenis kendaraan yang akan diedit")
            return
        
        # Get current values
        current_values = self.vehicle_type_tree.item(selected[0])['values']
        
        # Open edit dialogs
        nama = simpledialog.askstring("Edit Jenis Kendaraan", "Nama Jenis Kendaraan:", initialvalue=current_values[1])
        if nama:
            deskripsi = simpledialog.askstring("Edit Jenis Kendaraan", "Deskripsi:", initialvalue=current_values[2])
            result = self.admin_controller.edit_vehicle_type(current_values[0], nama, deskripsi)
            if result:
                messagebox.showinfo("Sukses", "Jenis kendaraan berhasil diupdate")
                self.load_vehicle_types()
    
    def delete_vehicle_type(self):
        # Get selected item
        selected = self.vehicle_type_tree.selection()
        if not selected:
            messagebox.showwarning("Peringatan", "Pilih jenis kendaraan yang akan dihapus")
            return
        
        # Confirm deletion
        if messagebox.askyesno("Konfirmasi", "Yakin ingin menghapus jenis kendaraan ini?"):
            current_values = self.vehicle_type_tree.item(selected[0])['values']
            result = self.admin_controller.delete_vehicle_type(current_values[0])
            if result:
                messagebox.showinfo("Sukses", "Jenis kendaraan berhasil dihapus")
                self.load_vehicle_types()
    
    def create_vehicle_tab(self):
        # Vehicle Management Tab (similar structure to vehicle type tab)
        vehicle_frame = ttk.Frame(self.notebook)
        self.notebook.add(vehicle_frame, text="Kendaraan")
        
        # Implement similar CRUD operations for vehicles
        # This would include methods like load_vehicles(), add_vehicle(), edit_vehicle(), delete_vehicle()
        # The implementation would be similar to vehicle type methods
    
    def create_user_tab(self):
        # User Management Tab (similar to previous tabs)
        user_frame = ttk.Frame(self.notebook)
        self.notebook.add(user_frame, text="Pengguna")
        
        # Implement CRUD operations for users
    
    def create_payment_tab(self):
        # Payment Management Tab
        payment_frame = ttk.Frame(self.notebook)
        self.notebook.add(payment_frame, text="Pembayaran")
        
        # Implement payment verification and listing
    
    def create_rental_history_tab(self):
        # Rental History Tab
        history_frame = ttk.Frame(self.notebook)
        self.notebook.add(history_frame, text="Riwayat Pemesanan")
        
        # Implement listing of all rental histories