from config.database import DatabaseConnection

class VehicleType:
    def __init__(self, nama=None, deskripsi=None):
        self.id = None
        self.nama = nama
        self.deskripsi = deskripsi
        self.db = DatabaseConnection()

    def tambah_jenis_kendaraan(self):
        """Menambahkan jenis kendaraan baru"""
        query = """
        INSERT INTO jenis_kendaraan 
        (nama, deskripsi) 
        VALUES (%s, %s)
        """
        params = (self.nama, self.deskripsi)

        try:
            cursor = self.db.execute_query(query, params)
            if cursor:
                self.id = cursor.lastrowid
                return True
            return False
        except Exception as e:
            print(f"Error tambah jenis kendaraan: {e}")
            return False

    def update_jenis_kendaraan(self):
        """Memperbarui data jenis kendaraan"""
        query = """
        UPDATE jenis_kendaraan 
        SET nama = %s, deskripsi = %s 
        WHERE id = %s
        """
        params = (
            self.nama, 
            self.deskripsi, 
            self.id
        )

        try:
            cursor = self.db.execute_query(query, params)
            return cursor is not None
        except Exception as e:
            print(f"Error update jenis kendaraan: {e}")
            return False

    def hapus_jenis_kendaraan(self, jenis_id):
        """Menghapus jenis kendaraan"""
        query = "DELETE FROM jenis_kendaraan WHERE id = %s"
        params = (jenis_id,)

        try:
            cursor = self.db.execute_query(query, params)
            return cursor is not None
        except Exception as e:
            print(f"Error hapus jenis kendaraan: {e}")
            return False

    def get_jenis_kendaraan_by_id(self, jenis_id):
        """Mendapatkan detail jenis kendaraan berdasarkan ID"""
        query = "SELECT * FROM jenis_kendaraan WHERE id = %s"
        params = (jenis_id,)

        try:
            cursor = self.db.execute_query(query, params)
            if cursor:
                return cursor.fetchone()
            return None
        except Exception as e:
            print(f"Error ambil jenis kendaraan: {e}")
            return None

    def list_jenis_kendaraan(self):
        """Mendapatkan daftar semua jenis kendaraan"""
        query = """
        SELECT jk.*, COUNT(k.id) as jumlah_kendaraan 
        FROM jenis_kendaraan jk
        LEFT JOIN kendaraan k ON jk.id = k.jenis_id
        GROUP BY jk.id, jk.nama, jk.deskripsi
        """

        try:
            cursor = self.db.execute_query(query)
            if cursor:
                return cursor.fetchall()
            return []
        except Exception as e:
            print(f"Error list jenis kendaraan: {e}")
            return []

    def cek_kendaraan_by_jenis(self, jenis_id):
        """
        Mengecek apakah ada kendaraan dengan jenis tertentu
        Berguna sebelum menghapus jenis kendaraan
        """
        query = """
        SELECT COUNT(*) as jumlah 
        FROM kendaraan 
        WHERE jenis_id = %s
        """
        params = (jenis_id,)

        try:
            cursor = self.db.execute_query(query, params)
            if cursor:
                result = cursor.fetchone()
                return result['jumlah'] > 0
            return False
        except Exception as e:
            print(f"Error cek kendaraan by jenis: {e}")
            return False

    def validasi_nama_unik(self, nama):
        """
        Memastikan nama jenis kendaraan unik
        """
        query = "SELECT COUNT(*) as jumlah FROM jenis_kendaraan WHERE nama = %s"
        params = (nama,)

        try:
            cursor = self.db.execute_query(query, params)
            if cursor:
                result = cursor.fetchone()
                return result['jumlah'] == 0
            return False
        except Exception as e:
            print(f"Error validasi nama jenis kendaraan: {e}")
            return False