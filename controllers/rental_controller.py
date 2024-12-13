# controllers/rental_controller.py
from models.rental import Rental
from models.vehicle import Vehicle
from models.payment import Payment
from config.database import DatabaseConnection
from datetime import date, datetime

class RentalController:
    @staticmethod
    def create_rental(user_id, vehicle_id, start_date, end_date):
        """
        Membuat pemesanan baru
        """
        # Validasi input
        if not all([user_id, vehicle_id, start_date, end_date]):
            return None, "Semua field harus diisi"
        
        # Konversi string ke date jika diperlukan
        if isinstance(start_date, str):
            start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
        if isinstance(end_date, str):
            end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
        
        # Validasi tanggal
        if start_date > end_date:
            return None, "Tanggal mulai tidak boleh lebih dari tanggal selesai"
        
        if start_date < date.today():
            return None, "Tanggal mulai tidak boleh di masa lalu"
        
        # Cek ketersediaan kendaraan
        vehicle = Vehicle.get_by_id(vehicle_id)
        if not vehicle:
            return None, "Kendaraan tidak ditemukan"
        
        if vehicle.status != 'tersedia':
            return None, "Kendaraan sudah tidak tersedia"
        
        # Cek konflik pemesanan
        if RentalController.check_vehicle_availability(vehicle_id, start_date, end_date):
            return None, "Kendaraan sudah dipesan pada tanggal tersebut"
        
        # Hitung total biaya
        rental_days = (end_date - start_date).days + 1
        total_cost = rental_days * vehicle.harga_sewa
        
        # Buat objek rental
        rental = Rental(
            user_id=user_id,
            vehicle_id=vehicle_id,
            start_date=start_date,
            end_date=end_date,
            total_cost=total_cost
        )
        
        # Simpan rental
        rental_id = rental.save()
        
        if rental_id:
            # Update status kendaraan
            Vehicle.update_vehicle_status(vehicle_id, 'disewa')
            return rental, "Pemesanan berhasil dibuat"
        
        return None, "Gagal membuat pemesanan"

    @staticmethod
    def check_vehicle_availability(vehicle_id, start_date, end_date):
        """
        Memeriksa apakah kendaraan tersedia pada rentang tanggal tertentu
        """
        db = DatabaseConnection()
        query = """
        SELECT COUNT(*) as conflict_count 
        FROM pemesanan 
        WHERE kendaraan_id = %s 
        AND status != 'ditolak' 
        AND (
            (tanggal_mulai BETWEEN %s AND %s) 
            OR (tanggal_selesai BETWEEN %s AND %s) 
            OR (%s BETWEEN tanggal_mulai AND tanggal_selesai)
        )
        """
        params = (
            vehicle_id, 
            start_date, end_date, 
            start_date, end_date,
            end_date
        )
        
        cursor = db.execute_query(query, params)
        
        if cursor:
            result = cursor.fetchone()
            return result['conflict_count'] > 0
        
        return False

    @staticmethod
    def create_payment(rental_id, payment_method):
        """
        Membuat pembayaran untuk pemesanan
        """
        # Ambil detail rental
        rental = Rental.get_by_id(rental_id)
        
        if not rental:
            return None, "Pemesanan tidak ditemukan"
        
        # Hitung keterlambatan (jika ada)
        late_fee = 0
        actual_return_date = date.today()
        if actual_return_date > rental.end_date:
            late_fee = rental.calculate_late_penalty(actual_return_date)
        
        # Buat objek pembayaran
        payment = Payment(
            rental_id=rental_id,
            amount=rental.total_cost,
            payment_method=payment_method,
            late_fee=late_fee
        )
        
        # Simpan pembayaran
        payment_id = payment.save()
        
        if payment_id:
            # Update status rental
            rental.update_status('selesai')
            # Update status kendaraan
            Vehicle.update_vehicle_status(rental.vehicle_id, 'tersedia')
            
            return payment, "Pembayaran berhasil"
        
        return None, "Gagal membuat pembayaran"

    @staticmethod
    def cancel_rental(rental_id, user_id):
        """
        Membatalkan pemesanan
        """
        # Ambil detail rental
        rental = Rental.get_by_id(rental_id)
        
        if not rental:
            return False, "Pemesanan tidak ditemukan"
        
        # Validasi apakah user berhak membatalkan
        if rental.user_id != user_id:
            return False, "Anda tidak memiliki izin membatalkan pemesanan ini"
        
        # Cek apakah rental masih bisa dibatalkan
        if rental.status not in ['menunggu', 'disetujui']:
            return False, "Pemesanan tidak dapat dibatalkan"
        
        # Update status rental
        result = rental.update_status('ditolak')
        
        if result:
            # Kembalikan status kendaraan
            Vehicle.update_vehicle_status(rental.vehicle_id, 'tersedia')
            return True, "Pemesanan berhasil dibatalkan"
        
        return False, "Gagal membatalkan pemesanan"

    @staticmethod
    def get_user_rentals(user_id):
        """
        Mendapatkan semua pemesanan milik pengguna
        """
        return Rental.get_user_rentals(user_id)