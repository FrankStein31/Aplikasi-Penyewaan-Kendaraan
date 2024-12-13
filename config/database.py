import mysql.connector
from mysql.connector import Error

class DatabaseConnection:
    def __init__(self):
        self.host = "localhost"
        self.user = "root"
        self.password = ""  # Ganti dengan password MySQL Anda
        self.database = "rental_kendaraan"

    def connect(self):
        try:
            connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            return connection
        except Error as e:
            print(f"Error koneksi database: {e}")
            return None

    def execute_query(self, query, params=None):
        connection = None
        cursor = None
        try:
            connection = self.connect()
            if connection:
                cursor = connection.cursor(dictionary=True)
                
                # Execute query with or without parameters
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)
                
                query_type = query.strip().upper().split()[0]
                
                if query_type == 'SELECT':
                    results = cursor.fetchall()
                    return results
                
                elif query_type in ['INSERT', 'UPDATE', 'DELETE']:
                    connection.commit()
                    
                    if query_type == 'INSERT':
                        return cursor
                    
                    return True
                
                return True
        
        except Error as e:
            print(f"Error eksekusi query: {e}")
            if connection:
                connection.rollback()
            return None
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
        
        return None

    def fetch_one(self, query, params=None):
        connection = None
        cursor = None
        try:
            connection = self.connect()
            if connection:
                cursor = connection.cursor(dictionary=True)
                
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)
                
                return cursor.fetchone()
        
        except Error as e:
            print(f"Error fetch query: {e}")
            return None
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    def get_last_insert_id(self):
        """
        Helper method to get the last inserted ID
        """
        connection = None
        cursor = None
        try:
            connection = self.connect()
            if connection:
                cursor = connection.cursor(dictionary=True)
                cursor.execute("SELECT LAST_INSERT_ID() as last_id")
                result = cursor.fetchone()
                return result['last_id'] if result else None
        except Error as e:
            print(f"Error getting last insert ID: {e}")
            return None
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

def create_database_and_tables():
    db = DatabaseConnection()
    connection = mysql.connector.connect(
        host=db.host,
        user=db.user,
        password=db.password
    )
    cursor = connection.cursor()

    # Membuat database
    cursor.execute("CREATE DATABASE IF NOT EXISTS rental_kendaraan")
    cursor.execute("USE rental_kendaraan")

    # Tabel Tipe Kendaraan
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS jenis_kendaraan (
        id INT AUTO_INCREMENT PRIMARY KEY,
        nama VARCHAR(50) NOT NULL,
        deskripsi TEXT
    )
    """)

    # Tabel Kendaraan
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS kendaraan (
        id INT AUTO_INCREMENT PRIMARY KEY,
        jenis_id INT,
        nama VARCHAR(100) NOT NULL,
        plat_nomor VARCHAR(20) UNIQUE NOT NULL,
        harga_sewa DECIMAL(10,2) NOT NULL,
        status ENUM('tersedia', 'disewa') DEFAULT 'tersedia',
        FOREIGN KEY (jenis_id) REFERENCES jenis_kendaraan(id)
    )
    """)

    # Tabel Pengguna
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS pengguna (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(50) UNIQUE NOT NULL,
        password VARCHAR(255) NOT NULL,
        nama_lengkap VARCHAR(100) NOT NULL,
        email VARCHAR(100) UNIQUE NOT NULL,
        no_telepon VARCHAR(20),
        role ENUM('admin', 'penyewa') NOT NULL,
        status ENUM('aktif', 'nonaktif') DEFAULT 'aktif'
    )
    """)

    # Tabel Pemesanan
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS pemesanan (
        id INT AUTO_INCREMENT PRIMARY KEY,
        pengguna_id INT,
        kendaraan_id INT,
        tanggal_mulai DATE NOT NULL,
        tanggal_selesai DATE NOT NULL,
        total_biaya DECIMAL(10,2) NOT NULL,
        status ENUM('menunggu', 'disetujui', 'ditolak', 'selesai') DEFAULT 'menunggu',
        FOREIGN KEY (pengguna_id) REFERENCES pengguna(id),
        FOREIGN KEY (kendaraan_id) REFERENCES kendaraan(id)
    )
    """)

    # Tabel Pembayaran
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS pembayaran (
        id INT AUTO_INCREMENT PRIMARY KEY,
        pemesanan_id INT,
        jumlah DECIMAL(10,2) NOT NULL,
        tanggal_pembayaran DATETIME NOT NULL,
        metode_pembayaran VARCHAR(50) NOT NULL,
        status ENUM('menunggu', 'berhasil', 'gagal') DEFAULT 'menunggu',
        denda DECIMAL(10,2) DEFAULT 0,
        FOREIGN KEY (pemesanan_id) REFERENCES pemesanan(id)
    )
    """)

    connection.commit()
    cursor.close()
    connection.close()
    print("Database dan tabel berhasil dibuat!")

# create_database_and_tables()