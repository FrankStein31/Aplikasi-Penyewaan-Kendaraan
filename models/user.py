import bcrypt
from config.database import DatabaseConnection

class User:
    def __init__(self, username=None, password=None, nama_lengkap=None, email=None, no_telepon=None, role='penyewa', status='aktif'):
        self.id = None
        self.username = username
        self.password = password
        self.nama_lengkap = nama_lengkap
        self.email = email
        self.no_telepon = no_telepon
        self.role = role
        self.status = status
        self.db = DatabaseConnection()

    def hash_password(self, password):
        """Hash password menggunakan bcrypt"""
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt)

    def verify_password(self, input_password, stored_hash):
        """Verifikasi password"""
        return bcrypt.checkpw(input_password.encode('utf-8'), stored_hash.encode('utf-8'))

    def register(self):
        """Registrasi pengguna baru"""
        # Hash password sebelum disimpan
        hashed_password = self.hash_password(self.password)

        query = """
        INSERT INTO pengguna 
        (username, password, nama_lengkap, email, no_telepon, role, status) 
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        params = (
            self.username, 
            hashed_password.decode('utf-8'), 
            self.nama_lengkap, 
            self.email, 
            self.no_telepon, 
            self.role, 
            self.status
        )

        try:
            cursor = self.db.execute_query(query, params)
            if cursor:
                return True
            return False
        except Exception as e:
            print(f"Error registrasi: {e}")
            return False

    def login(self):
        """Proses login"""
        query = "SELECT * FROM pengguna WHERE username = %s"
        params = (self.username,)

        try:
            cursor = self.db.execute_query(query, params)
            if cursor:
                user = cursor.fetchone()
                if user and self.verify_password(self.password, user['password']):
                    # Set atribut pengguna
                    self.id = user['id']
                    self.nama_lengkap = user['nama_lengkap']
                    self.email = user['email']
                    self.no_telepon = user['no_telepon']
                    self.role = user['role']
                    self.status = user['status']
                    return True
            return False
        except Exception as e:
            print(f"Error login: {e}")
            return False

    def get_by_id(self, user_id):
        """Ambil data pengguna berdasarkan ID"""
        query = "SELECT * FROM pengguna WHERE id = %s"
        params = (user_id,)

        try:
            cursor = self.db.execute_query(query, params)
            if cursor:
                return cursor.fetchone()
            return None
        except Exception as e:
            print(f"Error mengambil pengguna: {e}")
            return None

    def update(self):
        """Update data pengguna"""
        query = """
        UPDATE pengguna 
        SET nama_lengkap = %s, email = %s, no_telepon = %s, status = %s 
        WHERE id = %s
        """
        params = (
            self.nama_lengkap, 
            self.email, 
            self.no_telepon, 
            self.status,
            self.id
        )

        try:
            cursor = self.db.execute_query(query, params)
            if cursor:
                return True
            return False
        except Exception as e:
            print(f"Error update pengguna: {e}")
            return False

    def delete(self, user_id):
        """Hapus pengguna"""
        query = "DELETE FROM pengguna WHERE id = %s"
        params = (user_id,)

        try:
            cursor = self.db.execute_query(query, params)
            if cursor:
                return True
            return False
        except Exception as e:
            print(f"Error hapus pengguna: {e}")
            return False

    def list_users(self, role=None):
        """Daftar pengguna, bisa disaring berdasarkan role"""
        query = "SELECT * FROM pengguna"
        params = None

        if role:
            query += " WHERE role = %s"
            params = (role,)

        try:
            cursor = self.db.execute_query(query, params)
            if cursor:
                return cursor.fetchall()
            return []
        except Exception as e:
            print(f"Error list pengguna: {e}")
            return []