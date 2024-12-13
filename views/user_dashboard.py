from models.vehicle import Vehicle
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from controllers.user_controller import UserController
from views.rental_views import RentalView

class UserDashboard:
    def __init__(self, root, user):
        self.root = root
        self.root.title(f"Penyewa Dashboard - {user['nama_lengkap']}")
        self.root.geometry("800x600")
        
        self.user = user
        self.user_controller = UserController()
        
        # Create notebook (tabbed interface)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill='both', padx=10, pady=10)
        
        # Create tabs
        self.create_vehicle_selection_tab()
        self.create_rental_tab()
        self.create_payment_history_tab()
        self.create_personal_rental_history_tab()
    
    def create_vehicle_selection_tab(self):
        # Vehicle Selection Tab
        vehicle_frame = ttk.Frame(self.notebook)
        self.notebook.add(vehicle_frame, text="Pilih Kendaraan")
        
        # Treeview for available vehicles
        columns = ('ID', 'Jenis', 'Nama', 'Plat Nomor', 'Harga Sewa')
        self.vehicle_tree = ttk.Treeview(vehicle_frame, columns=columns, show='headings')
        for col in columns:
            self.vehicle_tree.heading(col, text=col)
        self.vehicle_tree.pack(expand=True, fill='both', padx=10, pady=10)
        
        # Refresh and Rent buttons
        btn_frame = tk.Frame(vehicle_frame)
        btn_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Button(btn_frame, text="Refresh", command=self.load_available_vehicles).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Sewa Kendaraan", command=self.open_rental_view).pack(side='left', padx=5)
        
        # Load initial data
        self.load_available_vehicles()
    
    def load_available_vehicles(self):
        # Clear existing items
        for i in self.vehicle_tree.get_children():
            self.vehicle_tree.delete(i)
        
        # Fetch and populate available vehicles
        vehicles = self.user_controller.get_available_vehicles()
        for vehicle in vehicles:
            self.vehicle_tree.insert('', 'end', values=(
                vehicle['id'], 
                vehicle['jenis_nama'], 
                vehicle['nama'], 
                vehicle['plat_nomor'], 
                f"Rp {vehicle['harga_sewa']:,.2f}"
            ))
    
    def open_rental_view(self):
        # Open rental view for selected vehicles
        selected_vehicles = self.vehicle_tree.selection()
        if not selected_vehicles:
            messagebox.showwarning("Peringatan", "Pilih kendaraan yang akan disewa")
            return
        
        # Collect selected vehicle IDs
        vehicle_ids = [self.vehicle_tree.item(item)['values'][0] for item in selected_vehicles]
        
        # Open rental view
        rental_window = tk.Toplevel(self.root)
        RentalView(rental_window, self.user, vehicle_ids, self.user_controller)
    
    def create_rental_tab(self):
        # Active Rentals Tab
        rental_frame = ttk.Frame(self.notebook)
        self.notebook.add(rental_frame, text="Pemesanan Aktif")
        
        # Treeview for active rentals
        columns = ('ID', 'Kendaraan', 'Tanggal Mulai', 'Tanggal Selesai', 'Status')
        self.active_rental_tree = ttk.Treeview(rental_frame, columns=columns, show='headings')
        for col in columns:
            self.active_rental_tree.heading(col, text=col)
        self.active_rental_tree.pack(expand=True, fill='both', padx=10, pady=10)
        
        # Buttons
        btn_frame = tk.Frame(rental_frame)
        btn_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Button(btn_frame, text="Refresh", command=self.load_active_rentals).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Batalkan Pesanan", command=self.cancel_rental).pack(side='left', padx=5)
        
        # Load initial data
        self.load_active_rentals()

    def load_active_rentals(self):
        # Clear existing items
        for i in self.active_rental_tree.get_children():
            self.active_rental_tree.delete(i)
        
        # Fetch active rentals for this user
        rentals = self.user_controller.get_active_rentals(self.user['id'])
        for rental in rentals:
            # Get vehicle name from user controller or pass it separately
            vehicle_name = self.user_controller.get_vehicle_name(rental.vehicle_id)
            
            self.active_rental_tree.insert('', 'end', values=(
                rental.id, 
                vehicle_name, 
                rental.start_date, 
                rental.end_date, 
                rental.status
            ))
    
    def cancel_rental(self):
        # Get selected rental
        selected = self.active_rental_tree.selection()
        if not selected:
            messagebox.showwarning("Peringatan", "Pilih pemesanan yang akan dibatalkan")
            return
        
        # Confirm cancellation
        if messagebox.askyesno("Konfirmasi", "Yakin ingin membatalkan pemesanan ini?"):
            rental_id = self.active_rental_tree.item(selected[0])['values'][0]
            result = self.user_controller.cancel_rental(rental_id)
            
            if result:
                messagebox.showinfo("Sukses", "Pemesanan berhasil dibatalkan")
                self.load_active_rentals()
            else:
                messagebox.showerror("Gagal", "Gagal membatalkan pemesanan")
    
    def create_payment_history_tab(self):
        # Payment History Tab
        payment_frame = ttk.Frame(self.notebook)
        self.notebook.add(payment_frame, text="Riwayat Pembayaran")
        
        # Treeview for payment history
        columns = ('ID', 'Pesanan', 'Jumlah', 'Tanggal', 'Metode', 'Status', 'Denda')
        self.payment_history_tree = ttk.Treeview(payment_frame, columns=columns, show='headings')
        for col in columns:
            self.payment_history_tree.heading(col, text=col)
        self.payment_history_tree.pack(expand=True, fill='both', padx=10, pady=10)
        
        # Refresh button
        btn_frame = tk.Frame(payment_frame)
        btn_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Button(btn_frame, text="Refresh", command=self.load_payment_history).pack(side='left', padx=5)
        
        # Load initial data
        self.load_payment_history()
    
    def load_payment_history(self):
        # Clear existing items
        for i in self.payment_history_tree.get_children():
            self.payment_history_tree.delete(i)
        
        # Fetch payment history for this user
        payments = self.user_controller.get_payment_history(self.user['id'])
        for payment in payments:
            self.payment_history_tree.insert('', 'end', values=(
                payment['id'], 
                payment['pemesanan_id'], 
                f"Rp {payment['jumlah']:,.2f}", 
                payment['tanggal_pembayaran'], 
                payment['metode_pembayaran'], 
                payment['status'],
                f"Rp {payment['denda']:,.2f}" if payment['denda'] else "Rp 0"
            ))
    
    def create_personal_rental_history_tab(self):
        # Personal Rental History Tab
        history_frame = ttk.Frame(self.notebook)
        self.notebook.add(history_frame, text="Riwayat Pemesanan")
        
        # Treeview for rental history
        columns = ('ID', 'Kendaraan', 'Tanggal Mulai', 'Tanggal Selesai', 'Total Biaya', 'Status')
        self.rental_history_tree = ttk.Treeview(history_frame, columns=columns, show='headings')
        for col in columns:
            self.rental_history_tree.heading(col, text=col)
        self.rental_history_tree.pack(expand=True, fill='both', padx=10, pady=10)
        
        # Refresh button
        btn_frame = tk.Frame(history_frame)
        btn_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Button(btn_frame, text="Refresh", command=self.load_rental_history).pack(side='left', padx=5)
        
        # Load initial data
        self.load_rental_history()
    
    def load_rental_history(self):
        # Clear existing items
        for i in self.rental_history_tree.get_children():
            self.rental_history_tree.delete(i)
        
        # Fetch rental history for this user
        rentals = self.user_controller.get_rental_history(self.user['id'])
        
        # Tambahkan join dengan tabel kendaraan untuk mendapatkan nama kendaraan
        for rental in rentals:
            # Ambil nama kendaraan menggunakan vehicle_id
            vehicle = Vehicle.get_by_id(rental.vehicle_id)
            
            self.rental_history_tree.insert('', 'end', values=(
                rental.id, 
                vehicle.nama if vehicle else 'Kendaraan Tidak Tersedia', 
                rental.start_date, 
                rental.end_date, 
                f"Rp {rental.total_cost:,.2f}", 
                rental.status
            ))