# controllers/auth_controller.py
import hashlib
from config.database import DatabaseConnection

class AuthController:
    @staticmethod
    def hash_password(password):
        """
        Hash password menggunakan SHA-256
        """
        return hashlib.sha256(password.encode()).hexdigest()

    @staticmethod
    def register(data):
        """
        Mendaftarkan pengguna baru
        """
        # Validasi input
        required_fields = ['username', 'password', 'nama_lengkap', 'email']
        for field in required_fields:
            if not data.get(field):
                return False, f"{field.replace('_', ' ').title()} harus diisi"
        
        # Koneksi database
        db = DatabaseConnection()
        
        # Periksa apakah username atau email sudah ada
        check_query = "SELECT * FROM pengguna WHERE username = %s OR email = %s"
        existing_user = db.fetch_one(check_query, (data['username'], data['email']))
        
        if existing_user:
            return False, "Username atau email sudah terdaftar"
        
        # Hash password
        hashed_password = AuthController.hash_password(data['password'])
        
        # Query insert
        insert_query = """
        INSERT INTO pengguna 
        (username, password, nama_lengkap, email, no_telepon, role) 
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        
        # Siapkan parameter
        params = (
            data['username'], 
            hashed_password, 
            data['nama_lengkap'], 
            data['email'], 
            data.get('no_telepon', ''),
            data.get('role', 'penyewa')
        )
        
        # Eksekusi query
        result = db.execute_query(insert_query, params)
        
        if result:
            return True, "Registrasi berhasil"
        else:
            return False, "Gagal mendaftarkan pengguna"

    @staticmethod
    def login(username, password):
        """
        Proses login pengguna
        """
        # Hash password yang diinput
        hashed_password = AuthController.hash_password(password)
        
        # Koneksi database
        db = DatabaseConnection()
        
        # Query untuk mencari pengguna
        query = "SELECT * FROM pengguna WHERE username = %s AND password = %s"
        user = db.fetch_one(query, (username, hashed_password))
        
        # Validasi user
        if user:
            # Periksa status akun
            if user.get('status') == 'nonaktif':
                return None, "Akun Anda tidak aktif"
            
            return user, "Login berhasil"
        
        return None, "Username atau password salah"