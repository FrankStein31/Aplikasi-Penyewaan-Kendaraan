# controllers/user_controller.py
from models.user import User
from models.rental import Rental
from models.payment import Payment
from models.vehicle import Vehicle
from controllers.rental_controller import RentalController

class UserController:
    @staticmethod
    def get_profile(user_id):
        """
        Mendapatkan profil pengguna
        """
        user = User.get_by_id(user_id)
        if not user:
            return None, "Pengguna tidak ditemukan"
        
        return user, "Profil berhasil diambil"

    @staticmethod
    def update_profile(user_id, username=None, full_name=None, 
                       email=None, phone_number=None):
        """
        Memperbarui profil pengguna
        """
        user = User.get_by_id(user_id)
        if not user:
            return False, "Pengguna tidak ditemukan"
        
        # Validasi input
        if username:
            user.username = username
        if full_name:
            user.nama_lengkap = full_name
        if email:
            user.email = email
        if phone_number:
            user.no_telepon = phone_number
        
        # Update profil
        result = user.update()
        
        if result:
            return True, "Profil berhasil diperbarui"
        return False, "Gagal memperbarui profil"

    @staticmethod
    def get_available_vehicles(vehicle_type_id=None, start_date=None, end_date=None):
        """
        Mendapatkan kendaraan yang tersedia untuk disewa
        """
        # Konversi input tanggal jika diperlukan
        if isinstance(start_date, str):
            from datetime import datetime
            start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
        if isinstance(end_date, str):
            from datetime import datetime
            end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
        
        # Ambil semua kendaraan tersedia menggunakan list_kendaraan()
        vehicle_obj = Vehicle()
        vehicles = vehicle_obj.list_kendaraan(filter_status='tersedia')
        
        # Filter berdasarkan tipe kendaraan jika dipilih
        if vehicle_type_id:
            vehicles = [v for v in vehicles if v['jenis_id'] == vehicle_type_id]
        
        # Filter berdasarkan ketersediaan di rentang tanggal
        if start_date and end_date:
            available_vehicles = []
            for vehicle in vehicles:
                if vehicle_obj.cek_ketersediaan(vehicle['id'], start_date, end_date):
                    available_vehicles.append(vehicle)
                
            return available_vehicles
        
        return vehicles
    
    # Add these methods to the UserController class in user_controller.py

    @staticmethod
    def get_active_rentals(user_id):
        """
        Mendapatkan daftar pemesanan aktif pengguna
        """
        from models.rental import Rental
        return Rental.get_active_rentals(user_id)
    
    @staticmethod
    def get_vehicle_details(vehicle_ids):
        """
        Mengambil detail kendaraan berdasarkan ID
        """
        vehicles = []
        for vehicle_id in vehicle_ids:
            vehicle = Vehicle.get_by_id(vehicle_id)
            if vehicle:
                vehicles.append({
                    'id': vehicle.id,
                    'nama': vehicle.nama,
                    'plat_nomor': vehicle.plat_nomor,
                    'harga_sewa': vehicle.harga_sewa
                })
        return vehicles

    @staticmethod
    def cancel_rental(rental_id):
        """
        Membatalkan pemesanan
        
        :param rental_id: ID pemesanan yang akan dibatalkan
        :return: Boolean yang menunjukkan keberhasilan pembatalan
        """
        from models.rental import Rental
        return Rental.cancel_rental(rental_id)

    @staticmethod
    def get_rental_history(user_id):
        """
        Mendapatkan riwayat pemesanan pengguna
        """
        return Rental.get_user_rentals(user_id)

    @staticmethod
    def get_payment_history(user_id):
        """
        Mendapatkan riwayat pembayaran pengguna
        """
        return Payment.get_user_payments(user_id)

    @staticmethod
    def create_multiple_rentals(user_id, rental_details):
        """
        Membuat beberapa pemesanan sekaligus
        
        rental_details: List of dict dengan keys:
        - vehicle_id
        - start_date
        - end_date
        """
        successful_rentals = []
        failed_rentals = []
        
        for rental_info in rental_details:
            try:
                rental, message = RentalController.create_rental(
                    user_id, 
                    rental_info['vehicle_id'], 
                    rental_info['start_date'], 
                    rental_info['end_date']
                )
                
                if rental:
                    successful_rentals.append(rental)
                else:
                    failed_rentals.append({
                        'vehicle_id': rental_info['vehicle_id'],
                        'error': message
                    })
            except Exception as e:
                failed_rentals.append({
                    'vehicle_id': rental_info['vehicle_id'],
                    'error': str(e)
                })
        
        return successful_rentals, failed_rentals
    
    @staticmethod
    def create_rental(rental_data):
        """
        Membuat pemesanan baru
        
        :param rental_data: Dictionary berisi detail pemesanan
        - pengguna_id: ID pengguna
        - vehicle_ids: Daftar ID kendaraan
        - tanggal_mulai: Tanggal mulai sewa
        - tanggal_selesai: Tanggal selesai sewa
        - total_biaya: Total biaya sewa
        :return: Hasil pembuatan pemesanan
        """
        from controllers.rental_controller import RentalController
        
        try:
            # Buat pemesanan untuk setiap kendaraan
            successful_rentals = []
            for vehicle_id in rental_data['vehicle_ids']:
                rental, message = RentalController.create_rental(
                    rental_data['pengguna_id'], 
                    vehicle_id, 
                    rental_data['tanggal_mulai'], 
                    rental_data['tanggal_selesai']
                )
                
                if not rental:
                    # Jika gagal membuat salah satu pemesanan, batalkan semua
                    for successful_rental in successful_rentals:
                        RentalController.cancel_rental(successful_rental.id)
                    return False
                
                successful_rentals.append(rental)
            
            return True
        
        except Exception as e:
            print(f"Error creating rental: {e}")
            return False
        
    def get_vehicle_name(self, vehicle_id):
        """
        Get the name of a vehicle by its ID
        """
        from models.vehicle import Vehicle
        vehicle = Vehicle.get_by_id(vehicle_id)
        return vehicle.nama if vehicle else "Kendaraan Tidak Dikenal"