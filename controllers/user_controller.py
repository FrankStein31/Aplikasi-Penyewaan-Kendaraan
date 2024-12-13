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
        
        # Ambil semua kendaraan tersedia
        vehicles = Vehicle.get_all(status='tersedia')
        
        # Filter berdasarkan tipe kendaraan jika dipilih
        if vehicle_type_id:
            vehicles = [v for v in vehicles if v.jenis_id == vehicle_type_id]
        
        # Filter berdasarkan ketersediaan di rentang tanggal
        if start_date and end_date:
            available_vehicles = []
            for vehicle in vehicles:
                if not RentalController.check_vehicle_availability(vehicle.id, start_date, end_date):
                    available_vehicles.append(vehicle)
            
            return available_vehicles
        
        return vehicles

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