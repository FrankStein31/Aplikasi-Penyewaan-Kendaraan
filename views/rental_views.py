import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from tkcalendar import DateEntry
from datetime import datetime, date

class RentalView:
    def __init__(self, root, user, vehicle_ids, user_controller):
        self.root = root
        self.root.title("Sewa Kendaraan")
        self.root.geometry("600x500")
        
        self.user = user
        self.vehicle_ids = vehicle_ids
        self.user_controller = user_controller
        
        # Create rental form
        self.create_rental_form()
    
    def create_rental_form(self):
        # Main frame
        main_frame = tk.Frame(self.root, padx=20, pady=20)
        main_frame.pack(expand=True, fill='both')
        
        # Selected Vehicles Display
        tk.Label(main_frame, text="Kendaraan yang Dipilih:", font=("Arial", 12, "bold")).pack(pady=(0, 10))
        
        # Treeview for selected vehicles
        columns = ('ID', 'Nama', 'Plat Nomor', 'Harga Sewa')
        self.selected_vehicles_tree = ttk.Treeview(main_frame, columns=columns, show='headings', height=3)
        for col in columns:
            self.selected_vehicles_tree.heading(col, text=col)
        self.selected_vehicles_tree.pack(fill='x', pady=(0, 10))
        
        # Load selected vehicles
        self.load_selected_vehicles()
        
        # Rental Period
        tk.Label(main_frame, text="Periode Sewa", font=("Arial", 12, "bold")).pack(pady=(10, 5))
        
        # Start Date
        start_frame = tk.Frame(main_frame)
        start_frame.pack(fill='x', pady=5)
        tk.Label(start_frame, text="Tanggal Mulai:").pack(side='left', padx=(0, 10))
        self.start_date = DateEntry(start_frame, width=12, background='darkblue', foreground='white', 
                                    date_pattern='y-mm-dd', mindate=date.today())
        self.start_date.pack(side='left')
        
        # End Date
        end_frame = tk.Frame(main_frame)
        end_frame.pack(fill='x', pady=5)
        tk.Label(end_frame, text="Tanggal Selesai:").pack(side='left', padx=(0, 10))
        self.end_date = DateEntry(end_frame, width=12, background='darkblue', foreground='white', 
                                  date_pattern='y-mm-dd', mindate=date.today())
        self.end_date.pack(side='left')
        
        # Total Cost Display
        self.total_cost_var = tk.StringVar()
        total_cost_frame = tk.Frame(main_frame)
        total_cost_frame.pack(fill='x', pady=(10, 5))
        tk.Label(total_cost_frame, text="Total Biaya:", font=("Arial", 12, "bold")).pack(side='left')
        tk.Label(total_cost_frame, textvariable=self.total_cost_var, font=("Arial", 12)).pack(side='left', padx=10)
        
        # Bind date selection to cost calculation
        self.start_date.bind('<<DateEntrySelected>>', self.calculate_total_cost)
        self.end_date.bind('<<DateEntrySelected>>', self.calculate_total_cost)
        
        # Confirm Rental Button
        confirm_btn = tk.Button(main_frame, text="Konfirmasi Sewa", command=self.confirm_rental)
        confirm_btn.pack(pady=20)
    
    def load_selected_vehicles(self):
        # Fetch details of selected vehicles
        vehicles = self.user_controller.get_vehicle_details(self.vehicle_ids)
        
        for vehicle in vehicles:
            self.selected_vehicles_tree.insert('', 'end', values=(
                vehicle['id'], 
                vehicle['nama'], 
                vehicle['plat_nomor'], 
                f"Rp {vehicle['harga_sewa']:,.2f}"
            ))
        
        # Calculate initial total cost
        self.calculate_total_cost()
    
    def calculate_total_cost(self, event=None):
        try:
            start = datetime.strptime(self.start_date.get(), '%Y-%m-%d').date()
            end = datetime.strptime(self.end_date.get(), '%Y-%m-%d').date()
            
            # Validate dates
            if end < start:
                messagebox.showerror("Error", "Tanggal selesai harus setelah tanggal mulai")
                return
            
            # Calculate rental duration
            rental_days = (end - start).days + 1
            
            # Calculate total cost
            total_cost = 0
            for item in self.selected_vehicles_tree.get_children():
                price = float(self.selected_vehicles_tree.item(item)['values'][3].replace('Rp ', '').replace(',', ''))
                total_cost += price * rental_days
            
            # Update total cost display
            self.total_cost_var.set(f"Rp {total_cost:,.2f}")
        
        except ValueError:
            # Handle potential date parsing errors
            self.total_cost_var.set("Rp 0")
    
    def confirm_rental(self):
        # Validate input
        try:
            start = datetime.strptime(self.start_date.get(), '%Y-%m-%d').date()
            end = datetime.strptime(self.end_date.get(), '%Y-%m-%d').date()
            
            if end < start:
                messagebox.showerror("Error", "Tanggal selesai harus setelah tanggal mulai")
                return
            
            # Confirm rental
            rental_data = {
                'pengguna_id': self.user['id'],
                'vehicle_ids': self.vehicle_ids,
                'tanggal_mulai': start,
                'tanggal_selesai': end,
                'total_biaya': float(self.total_cost_var.get().replace('Rp ', '').replace(',', ''))
            }
            
            # Call rental method
            result = self.user_controller.create_rental(rental_data)
            
            if result:
                messagebox.showinfo("Sukses", "Pemesanan berhasil dibuat!")
                self.root.destroy()
            else:
                messagebox.showerror("Gagal", "Gagal membuat pemesanan. Silakan coba lagi.")
        
        except Exception as e:
            messagebox.showerror("Error", f"Terjadi kesalahan: {str(e)}")