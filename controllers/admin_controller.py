# controllers/admin_controller.py
from models.vehicle_type import VehicleType
from models.vehicle import Vehicle
from models.user import User
from models.rental import Rental
from models.payment import Payment
from config.database import DatabaseConnection

class AdminController:
    # Manajemen Jenis Kendaraan
    @staticmethod
    def add_vehicle_type(name, description):
        """
        Menambahkan jenis kendaraan baru
        """
        vehicle_type = VehicleType(nama=name, deskripsi=description)
        return vehicle_type.save()

    @staticmethod
    def update_vehicle_type(type_id, name=None, description=None):
        """
        Memperbarui jenis kendaraan
        """
        vehicle_type = VehicleType.get_by_id(type_id)
        if not vehicle_type:
            return False, "Jenis kendaraan tidak ditemukan"
        
        if name:
            vehicle_type.nama = name
        if description:
            vehicle_type.deskripsi = description
        
        return vehicle_type.update()

    @staticmethod
    def delete_vehicle_type(type_id):
        """
        Menghapus jenis kendaraan
        """
        vehicle_type = VehicleType.get_by_id(type_id)
        if not vehicle_type:
            return False, "Jenis kendaraan tidak ditemukan"
        
        return vehicle_type.delete()

    @staticmethod
    def get_all_vehicle_types():
        """
        Mendapatkan semua jenis kendaraan
        """
        return VehicleType.get_all()

    # Manajemen Kendaraan
    @staticmethod
    def add_vehicle(vehicle_type_id, name, plate_number, rental_price):
        """
        Menambahkan kendaraan baru
        """
        vehicle = Vehicle(
            jenis_id=vehicle_type_id, 
            nama=name, 
            plat_nomor=plate_number, 
            harga_sewa=rental_price
        )
        return vehicle.save()

    @staticmethod
    def update_vehicle(vehicle_id, vehicle_type_id=None, name=None, 
                       plate_number=None, rental_price=None):
        """
        Memperbarui data kendaraan
        """
        vehicle = Vehicle.get_by_id(vehicle_id)
        if not vehicle:
            return False, "Kendaraan tidak ditemukan"
        
        if vehicle_type_id:
            vehicle.jenis_id = vehicle_type_id
        if name:
            vehicle.nama = name
        if plate_number:
            vehicle.plat_nomor = plate_number
        if rental_price is not None:
            vehicle.harga_sewa = rental_price
        
        return vehicle.update()

    @staticmethod
    def delete_vehicle(vehicle_id):
        """
        Menghapus kendaraan
        """
        vehicle = Vehicle.get_by_id(vehicle_id)
        if not vehicle:
            return False, "Kendaraan tidak ditemukan"
        
        return vehicle.delete()

    @staticmethod
    def get_all_vehicles(status=None):
        """
        Mendapatkan semua kendaraan, dapat difilter berdasarkan status
        """
        return Vehicle.get_all(status)

    # Manajemen Pengguna
    @staticmethod
    def add_user(username, password, full_name, email, 
                 phone_number, role='penyewa'):
        """
        Menambahkan pengguna baru (untuk admin)
        """
        from controllers.auth_controller import AuthController
        
        return AuthController.register(
            username, password, full_name, 
            email, phone_number, role
        )

    @staticmethod
    def update_user(user_id, username=None, full_name=None, 
                    email=None, phone_number=None, status=None):
        """
        Memperbarui data pengguna
        """
        user = User.get_by_id(user_id)
        if not user:
            return False, "Pengguna tidak ditemukan"
        
        if username:
            user.username = username
        if full_name:
            user.nama_lengkap = full_name
        if email:
            user.email = email
        if phone_number:
            user.no_telepon = phone_number
        if status:
            user.status = status
        
        return user.update()

    @staticmethod
    def delete_user(user_id):
        """
        Menghapus pengguna
        """
        user = User.get_by_id(user_id)
        if not user:
            return False, "Pengguna tidak ditemukan"
        
        return user.delete()

    @staticmethod
    def get_all_users(role=None, status=None):
        """
        Mendapatkan semua pengguna, dapat difilter berdasarkan role dan status
        """
        return User.get_all(role, status)

    # Manajemen Pemesanan
    @staticmethod
    def get_all_rentals(status=None):
        """
        Mendapatkan semua pemesanan
        """
        db = DatabaseConnection()
        query = "SELECT * FROM pemesanan"
        params = []
        
        if status:
            query += " WHERE status = %s"
            params.append(status)
        
        cursor = db.execute_query(query, params)
        
        rentals = []
        if cursor:
            results = cursor.fetchall()
            for result in results:
                rental = Rental(
                    id=result['id'],
                    user_id=result['pengguna_id'],
                    vehicle_id=result['kendaraan_id'],
                    start_date=result['tanggal_mulai'],
                    end_date=result['tanggal_selesai'],
                    total_cost=result['total_biaya'],
                    status=result['status']
                )
                rentals.append(rental)
        
        return rentals

    # Manajemen Pembayaran
    @staticmethod
    def verify_payment(payment_id, status):
        """
        Memverifikasi status pembayaran
        """
        payment = Payment.get_by_id(payment_id)
        if not payment:
            return False, "Pembayaran tidak ditemukan"
        
        return payment.verify_payment(status)

    @staticmethod
    def get_all_payments(status=None):
        """
        Mendapatkan semua pembayaran
        """
        return Payment.get_all_payments()