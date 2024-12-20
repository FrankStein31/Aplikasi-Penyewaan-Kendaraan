from models.vehicle import Vehicle
from config.database import DatabaseConnection
from datetime import datetime, date

class Rental:
    def __init__(self, id=None, user_id=None, vehicle_id=None, 
                 start_date=None, end_date=None, total_cost=None, 
                 status='menunggu'):
        self.id = id
        self.user_id = user_id
        self.vehicle_id = vehicle_id
        self.start_date = start_date
        self.end_date = end_date
        self.total_cost = total_cost
        self.status = status

    @classmethod
    def get_active_rentals(cls, user_id):
        """
        Mengambil semua pemesanan aktif milik seorang pengguna
        """
        db = DatabaseConnection()
        query = "SELECT * FROM pemesanan WHERE pengguna_id = %s AND status IN ('menunggu', 'disetujui', 'sedang_berjalan')"
        
        # Handle both cursor and direct results
        results = db.execute_query(query, (user_id,))
        
        rentals = []
        if results:
            # If results is a cursor, use fetchall()
            if hasattr(results, 'fetchall'):
                results = results.fetchall()
            
            # Ensure results is a list of dictionaries
            if not isinstance(results, list):
                results = [results]
            
            for result in results:
                rental = cls(
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
    def calculate_total_cost(self, vehicle_price_per_day):
        """
        Menghitung total biaya berdasarkan harga kendaraan per hari
        """
        rental_days = (self.end_date - self.start_date).days + 1
        self.total_cost = rental_days * vehicle_price_per_day
        return self.total_cost

    def calculate_late_penalty(self, actual_return_date):
        """
        Menghitung denda keterlambatan
        """
        if actual_return_date > self.end_date:
            late_days = (actual_return_date - self.end_date).days
            # Misalnya denda 50% dari harga sewa per hari untuk setiap hari keterlambatan
            penalty_per_day = self.total_cost / ((self.end_date - self.start_date).days + 1) * 0.5
            return late_days * penalty_per_day
        return 0

    def save(self):
        """
        Menyimpan data pemesanan ke database
        """
        db = DatabaseConnection()
        query = """
        INSERT INTO pemesanan 
        (pengguna_id, kendaraan_id, tanggal_mulai, tanggal_selesai, total_biaya, status) 
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        params = (
            self.user_id, 
            self.vehicle_id, 
            self.start_date, 
            self.end_date, 
            self.total_cost, 
            self.status
        )
        
        cursor = db.execute_query(query, params)
        if cursor:
            self.id = cursor.lastrowid
            return self.id
        return None

    @classmethod
    # def get_by_id(cls, rental_id):
    #     """
    #     Mengambil data pemesanan berdasarkan ID
    #     """
    #     db = DatabaseConnection()
    #     query = "SELECT * FROM pemesanan WHERE id = %s"
    #     cursor = db.execute_query(query, (rental_id,))
        
    #     if cursor:
    #         result = cursor.fetchone()
    #         if result:
    #             return cls(
    #                 id=result['id'],
    #                 user_id=result['pengguna_id'],
    #                 vehicle_id=result['kendaraan_id'],
    #                 start_date=result['tanggal_mulai'],
    #                 end_date=result['tanggal_selesai'],
    #                 total_cost=result['total_biaya'],
    #                 status=result['status']
    #             )
    #     return None
    
    def get_by_id(cls, rental_id):
        """
        Mengambil data pemesanan berdasarkan ID
        """
        db = DatabaseConnection()
        query = "SELECT * FROM pemesanan WHERE id = %s"
        results = db.execute_query(query, (rental_id,))
        
        if results:
            result = results[0] if isinstance(results, list) else results
            return cls(
                id=result['id'],
                user_id=result['pengguna_id'],
                vehicle_id=result['kendaraan_id'],
                start_date=result['tanggal_mulai'],
                end_date=result['tanggal_selesai'],
                total_cost=result['total_biaya'],
                status=result['status']
            )
        return None

    @classmethod
    def get_user_rentals(cls, user_id):
        """
        Mengambil semua pemesanan milik seorang pengguna
        """
        db = DatabaseConnection()
        query = "SELECT * FROM pemesanan WHERE pengguna_id = %s"
        results = db.execute_query(query, (user_id,))
        
        rentals = []
        if results:
            # Pastikan results adalah list
            if not isinstance(results, list):
                results = [results]
            
            for result in results:
                rental = cls(
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

    def update_status(self, new_status):
        """
        Memperbarui status pemesanan
        """
        db = DatabaseConnection()
        query = "UPDATE pemesanan SET status = %s WHERE id = %s"
        cursor = db.execute_query(query, (new_status, self.id))
        
        if cursor:
            self.status = new_status
            return True
        return False
    
    @classmethod
    def cancel_rental(cls, rental_id):
        """
        Membatalkan pemesanan berdasarkan ID
        
        Args:
            rental_id (int): ID pemesanan yang akan dibatalkan
        
        Returns:
            bool: True jika pembatalan berhasil, False jika gagal
        """
        # Ambil objek rental
        rental = cls.get_by_id(rental_id)
        
        if not rental:
            return False
        
        # Cek apakah rental masih bisa dibatalkan
        if rental.status not in ['menunggu', 'disetujui']:
            return False, "Pemesanan tidak dapat dibatalkan"
        
        # Update status rental menjadi ditolak
        result = rental.update_status('ditolak')
        
        if result:
            # Kembalikan status kendaraan
            Vehicle.update_vehicle_status(rental.vehicle_id, 'tersedia')
            return True, "Pemesanan berhasil dibatalkan"
        
        return result