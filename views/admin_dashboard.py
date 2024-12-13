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
            
            # Tambahkan validasi input
            if not nama:
                messagebox.showerror("Error", "Nama jenis kendaraan tidak boleh kosong")
                return
            
            self.admin_controller.add_vehicle_type(nama, deskripsi)
            messagebox.showinfo("Sukses", f"Jenis kendaraan '{nama}' berhasil ditambahkan")
            self.load_vehicle_types()
        else:
            messagebox.showerror("Gagal", "Gagal menambahkan jenis kendaraan. Nama mungkin sudah ada.")
    
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
            result = self.admin_controller.update_vehicle_type(current_values[0], nama, deskripsi)
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
        # Vehicle Management Tab
        vehicle_frame = ttk.Frame(self.notebook)
        self.notebook.add(vehicle_frame, text="Kendaraan")
        
        # Treeview for vehicles
        columns = ('ID', 'Jenis', 'Nama', 'Plat Nomor', 'Harga Sewa', 'Status')
        self.vehicle_tree = ttk.Treeview(vehicle_frame, columns=columns, show='headings')
        for col in columns:
            self.vehicle_tree.heading(col, text=col)
            
            # Set column widths
            if col == 'ID':
                self.vehicle_tree.column(col, width=50, anchor='center')
            elif col == 'Harga Sewa':
                self.vehicle_tree.column(col, width=100, anchor='e')
            elif col == 'Status':
                self.vehicle_tree.column(col, width=100, anchor='center')
        
        self.vehicle_tree.pack(expand=True, fill='both', padx=10, pady=10)
        
        # Buttons
        btn_frame = tk.Frame(vehicle_frame)
        btn_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Button(btn_frame, text="Tambah", command=self.add_vehicle).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Edit", command=self.edit_vehicle).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Hapus", command=self.delete_vehicle).pack(side='left', padx=5)
        
        # Load initial data
        self.load_vehicles()
        
    def load_vehicles(self):
        # Clear existing items
        for i in self.vehicle_tree.get_children():
            self.vehicle_tree.delete(i)
        
        # Fetch and populate vehicles
        vehicles = self.admin_controller.get_all_vehicles()
        for vehicle in vehicles:
            self.vehicle_tree.insert('', 'end', values=(
                vehicle['id'], 
                vehicle['jenis_nama'], 
                vehicle['nama'], 
                vehicle['plat_nomor'], 
                f"Rp {vehicle['harga_sewa']:,.2f}", 
                vehicle['status']
            ))
    
    def add_vehicle(self):
        # Get vehicle types for dropdown
        vehicle_types = self.admin_controller.get_vehicle_types()
        
        # Create a custom dialog
        add_dialog = tk.Toplevel(self.root)
        add_dialog.title("Tambah Kendaraan")
        add_dialog.geometry("400x300")
        
        # Vehicle Type Selection
        tk.Label(add_dialog, text="Jenis Kendaraan").pack(pady=(10,0))
        vehicle_type_var = tk.StringVar()
        vehicle_type_dropdown = ttk.Combobox(add_dialog, textvariable=vehicle_type_var)
        vehicle_type_dropdown['values'] = [f"{vtype['id']} - {vtype['nama']}" for vtype in vehicle_types]
        vehicle_type_dropdown.pack(pady=(0,10), padx=20)
        
        # Name Entry
        tk.Label(add_dialog, text="Nama Kendaraan").pack()
        nama_entry = tk.Entry(add_dialog, width=30)
        nama_entry.pack(pady=(0,10))
        
        # Plate Number Entry
        tk.Label(add_dialog, text="Nomor Plat").pack()
        plat_entry = tk.Entry(add_dialog, width=30)
        plat_entry.pack(pady=(0,10))
        
        # Rental Price Entry
        tk.Label(add_dialog, text="Harga Sewa").pack()
        harga_entry = tk.Entry(add_dialog, width=30)
        harga_entry.pack(pady=(0,10))
        
        def submit():
            try:
                # Validate inputs
                if not vehicle_type_var.get():
                    messagebox.showerror("Error", "Pilih jenis kendaraan")
                    return
                
                vehicle_type_id = int(vehicle_type_var.get().split(' - ')[0])
                nama = nama_entry.get().strip()
                plat_nomor = plat_entry.get().strip()
                harga_sewa = float(harga_entry.get())
                
                if not nama or not plat_nomor:
                    messagebox.showerror("Error", "Nama dan Nomor Plat harus diisi")
                    return
                
                # Call controller method to add vehicle
                result = self.admin_controller.add_vehicle(
                    vehicle_type_id, nama, plat_nomor, harga_sewa
                )
                
                if result:
                    messagebox.showinfo("Sukses", "Kendaraan berhasil ditambahkan")
                    add_dialog.destroy()
                    self.load_vehicles()
                else:
                    messagebox.showerror("Error", "Gagal menambahkan kendaraan")
            
            except ValueError:
                messagebox.showerror("Error", "Harga sewa harus berupa angka")
            except Exception as e:
                messagebox.showerror("Error", str(e))
        
        # Submit Button
        submit_btn = tk.Button(add_dialog, text="Simpan", command=submit)
        submit_btn.pack(pady=10)

    def edit_vehicle(self):
        # Get selected item
        selected = self.vehicle_tree.selection()
        if not selected:
            messagebox.showwarning("Peringatan", "Pilih kendaraan yang akan diedit")
            return
        
        # Get current values
        current_values = self.vehicle_tree.item(selected[0])['values']
        
        # Get vehicle types for dropdown
        vehicle_types = self.admin_controller.get_vehicle_types()
        
        # Create edit dialog
        edit_dialog = tk.Toplevel(self.root)
        edit_dialog.title("Edit Kendaraan")
        edit_dialog.geometry("400x300")
        
        # Vehicle Type Selection
        tk.Label(edit_dialog, text="Jenis Kendaraan").pack(pady=(10,0))
        vehicle_type_var = tk.StringVar(value=f"{current_values[1]}")
        vehicle_type_dropdown = ttk.Combobox(edit_dialog, textvariable=vehicle_type_var)
        vehicle_type_dropdown['values'] = [f"{vtype['id']} - {vtype['nama']}" for vtype in vehicle_types]
        vehicle_type_dropdown.pack(pady=(0,10), padx=20)
        
        # Name Entry
        tk.Label(edit_dialog, text="Nama Kendaraan").pack()
        nama_entry = tk.Entry(edit_dialog, width=30)
        nama_entry.insert(0, current_values[2])
        nama_entry.pack(pady=(0,10))
        
        # Plate Number Entry
        tk.Label(edit_dialog, text="Nomor Plat").pack()
        plat_entry = tk.Entry(edit_dialog, width=30)
        plat_entry.insert(0, current_values[3])
        plat_entry.pack(pady=(0,10))
        
        # Rental Price Entry
        tk.Label(edit_dialog, text="Harga Sewa").pack()
        harga_entry = tk.Entry(edit_dialog, width=30)
        # Remove 'Rp' and formatting before inserting
        harga_entry.insert(0, current_values[4].replace('Rp ', '').replace(',', ''))
        harga_entry.pack(pady=(0,10))
        
        def submit():
            try:
                # Validate inputs
                if not vehicle_type_var.get():
                    messagebox.showerror("Error", "Pilih jenis kendaraan")
                    return
                
                vehicle_type_id = int(vehicle_type_var.get().split(' - ')[0])
                nama = nama_entry.get().strip()
                plat_nomor = plat_entry.get().strip()
                harga_sewa = float(harga_entry.get())
                
                if not nama or not plat_nomor:
                    messagebox.showerror("Error", "Nama dan Nomor Plat harus diisi")
                    return
                
                # Call controller method to update vehicle
                result = self.admin_controller.update_vehicle(
                    current_values[0],  # vehicle ID
                    vehicle_type_id, 
                    nama, 
                    plat_nomor, 
                    harga_sewa
                )
                
                if result:
                    messagebox.showinfo("Sukses", "Kendaraan berhasil diupdate")
                    edit_dialog.destroy()
                    self.load_vehicles()
                else:
                    messagebox.showerror("Error", "Gagal mengupdate kendaraan")
            
            except ValueError:
                messagebox.showerror("Error", "Harga sewa harus berupa angka")
            except Exception as e:
                messagebox.showerror("Error", str(e))
        
        # Submit Button
        submit_btn = tk.Button(edit_dialog, text="Simpan", command=submit)
        submit_btn.pack(pady=10)

    def delete_vehicle(self):
        # Get selected item
        selected = self.vehicle_tree.selection()
        if not selected:
            messagebox.showwarning("Peringatan", "Pilih kendaraan yang akan dihapus")
            return
        
        # Confirm deletion
        if messagebox.askyesno("Konfirmasi", "Yakin ingin menghapus kendaraan ini?"):
            current_values = self.vehicle_tree.item(selected[0])['values']
            result = self.admin_controller.delete_vehicle(current_values[0])
            
            if result:
                messagebox.showinfo("Sukses", "Kendaraan berhasil dihapus")
                self.load_vehicles()

    def create_user_tab(self):
        # User Management Tab (similar to previous tabs)
        user_frame = ttk.Frame(self.notebook)
        self.notebook.add(user_frame, text="Pengguna")
        
        # Implement CRUD operations for users
    
    def create_pemesanan_tab(self):
        # User Management Tab (similar to previous tabs)
        pemesanan_frame = ttk.Frame(self.notebook)
        self.notebook.add(pemesanan_frame, text="Validasi Pemesanan")
        
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