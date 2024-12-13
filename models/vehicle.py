from config.database import DatabaseConnection

class Vehicle:
    def __init__(self, jenis_id=None, nama=None, plat_nomor=None, harga_sewa=None, status='tersedia'):
        self.id = None
        self.jenis_id = jenis_id
        self.nama = nama
        self.plat_nomor = plat_nomor
        self.harga_sewa = harga_sewa
        self.status = status
        self.db = DatabaseConnection()

    def tambah_kendaraan(self):
        """Menambahkan kendaraan baru"""
        query = """
        INSERT INTO kendaraan 
        (jenis_id, nama, plat_nomor, harga_sewa, status) 
        VALUES (%s, %s, %s, %s, %s)
        """
        params = (
            self.jenis_id, 
            self.nama, 
            self.plat_nomor, 
            self.harga_sewa, 
            self.status
        )

        try:
            cursor = self.db.execute_query(query, params)
            if cursor:
                self.id = cursor.lastrowid
                return True
            return False
        except Exception as e:
            print(f"Error tambah kendaraan: {e}")
            return False

    def update_kendaraan(self):
        """Memperbarui data kendaraan"""
        query = """
        UPDATE kendaraan 
        SET jenis_id = %s, nama = %s, plat_nomor = %s, 
        harga_sewa = %s, status = %s 
        WHERE id = %s
        """
        params = (
            self.jenis_id, 
            self.nama, 
            self.plat_nomor, 
            self.harga_sewa, 
            self.status,
            self.id
        )

        try:
            cursor = self.db.execute_query(query, params)
            return cursor is not None
        except Exception as e:
            print(f"Error update kendaraan: {e}")
            return False

    def hapus_kendaraan(self, kendaraan_id):
        """Menghapus kendaraan"""
        query = "DELETE FROM kendaraan WHERE id = %s"
        params = (kendaraan_id,)

        try:
            cursor = self.db.execute_query(query, params)
            return cursor is not None
        except Exception as e:
            print(f"Error hapus kendaraan: {e}")
            return False

    def get_kendaraan_by_id(self, kendaraan_id):
        """Mendapatkan detail kendaraan berdasarkan ID"""
        query = """
        SELECT k.*, jk.nama as jenis_nama 
        FROM kendaraan k
        JOIN jenis_kendaraan jk ON k.jenis_id = jk.id
        WHERE k.id = %s
        """
        params = (kendaraan_id,)

        try:
            cursor = self.db.execute_query(query, params)
            if cursor:
                return cursor.fetchone()
            return None
        except Exception as e:
            print(f"Error ambil kendaraan: {e}")
            return None

    def list_kendaraan(self, filter_status=None, filter_jenis=None):
        """
        Mendapatkan daftar kendaraan dengan optional filter
        - filter_status: tersedia/disewa
        - filter_jenis: ID jenis kendaraan
        """
        query = """
        SELECT k.*, jk.nama as jenis_nama 
        FROM kendaraan k
        JOIN jenis_kendaraan jk ON k.jenis_id = jk.id
        WHERE 1=1
        """
        params = []

        if filter_status:
            query += " AND k.status = %s"
            params.append(filter_status)

        if filter_jenis:
            query += " AND k.jenis_id = %s"
            params.append(filter_jenis)

        try:
            cursor = self.db.execute_query(query, tuple(params) if params else None)
            if cursor:
                return cursor.fetchall()
            return []
        except Exception as e:
            print(f"Error list kendaraan: {e}")
            return []

    def cek_ketersediaan(self, kendaraan_id, tanggal_mulai, tanggal_selesai):
        """
        Mengecek ketersediaan kendaraan untuk rentang tanggal tertentu
        """
        query = """
        SELECT COUNT(*) as konflik 
        FROM pemesanan 
        WHERE kendaraan_id = %s 
        AND (
            (tanggal_mulai <= %s AND tanggal_selesai >= %s)
            OR (tanggal_mulai <= %s AND tanggal_selesai >= %s)
            OR (tanggal_mulai >= %s AND tanggal_selesai <= %s)
        )
        AND status IN ('menunggu', 'disetujui')
        """
        params = (
            kendaraan_id, 
            tanggal_mulai, tanggal_mulai,
            tanggal_selesai, tanggal_selesai,
            tanggal_mulai, tanggal_selesai
        )

        try:
            cursor = self.db.execute_query(query, params)
            if cursor:
                result = cursor.fetchone()
                return result['konflik'] == 0
            return False
        except Exception as e:
            print(f"Error cek ketersediaan: {e}")
            return False