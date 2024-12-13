# models/payment.py
from config.database import DatabaseConnection
from datetime import datetime

class Payment:
    def __init__(self, id=None, rental_id=None, amount=None, 
                 payment_date=None, payment_method=None, 
                 status='menunggu', late_fee=0):
        self.id = id
        self.rental_id = rental_id
        self.amount = amount
        self.payment_date = payment_date or datetime.now()
        self.payment_method = payment_method
        self.status = status
        self.late_fee = late_fee

    def save(self):
        """
        Menyimpan data pembayaran ke database
        """
        db = DatabaseConnection()
        query = """
        INSERT INTO pembayaran 
        (pemesanan_id, jumlah, tanggal_pembayaran, metode_pembayaran, status, denda) 
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        params = (
            self.rental_id, 
            self.amount, 
            self.payment_date, 
            self.payment_method, 
            self.status,
            self.late_fee
        )
        
        cursor = db.execute_query(query, params)
        if cursor:
            self.id = cursor.lastrowid
            return self.id
        return None

    @classmethod
    def get_by_id(cls, payment_id):
        """
        Mengambil data pembayaran berdasarkan ID
        """
        db = DatabaseConnection()
        query = "SELECT * FROM pembayaran WHERE id = %s"
        cursor = db.execute_query(query, (payment_id,))
        
        if cursor:
            result = cursor.fetchone()
            if result:
                return cls(
                    id=result['id'],
                    rental_id=result['pemesanan_id'],
                    amount=result['jumlah'],
                    payment_date=result['tanggal_pembayaran'],
                    payment_method=result['metode_pembayaran'],
                    status=result['status'],
                    late_fee=result['denda']
                )
        return None

    @classmethod
    def get_user_payments(cls, user_id):
        """
        Mengambil semua pembayaran milik seorang pengguna
        """
        db = DatabaseConnection()
        query = """
        SELECT p.* FROM pembayaran p
        JOIN pemesanan pe ON p.pemesanan_id = pe.id
        WHERE pe.pengguna_id = %s
        """
        cursor = db.execute_query(query, (user_id,))
        
        payments = []
        if cursor:
            results = cursor.fetchall()
            for result in results:
                payment = cls(
                    id=result['id'],
                    rental_id=result['pemesanan_id'],
                    amount=result['jumlah'],
                    payment_date=result['tanggal_pembayaran'],
                    payment_method=result['metode_pembayaran'],
                    status=result['status'],
                    late_fee=result['denda']
                )
                payments.append(payment)
        
        return payments

    @classmethod
    def get_all_payments(cls):
        """
        Mengambil semua pembayaran (untuk admin)
        """
        db = DatabaseConnection()
        query = "SELECT * FROM pembayaran ORDER BY tanggal_pembayaran DESC"
        cursor = db.execute_query(query)
        
        payments = []
        if cursor:
            results = cursor.fetchall()
            for result in results:
                payment = cls(
                    id=result['id'],
                    rental_id=result['pemesanan_id'],
                    amount=result['jumlah'],
                    payment_date=result['tanggal_pembayaran'],
                    payment_method=result['metode_pembayaran'],
                    status=result['status'],
                    late_fee=result['denda']
                )
                payments.append(payment)
        
        return payments

    def verify_payment(self, status):
        """
        Memverifikasi status pembayaran (untuk admin)
        """
        db = DatabaseConnection()
        query = "UPDATE pembayaran SET status = %s WHERE id = %s"
        cursor = db.execute_query(query, (status, self.id))
        
        if cursor:
            self.status = status
            return True
        return False