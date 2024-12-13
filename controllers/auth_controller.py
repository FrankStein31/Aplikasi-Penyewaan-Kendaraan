# controllers/auth_controller.py
import hashlib
from models.user import User
from config.database import DatabaseConnection

class AuthController:
    @staticmethod
    def hash_password(password):
        """
        Hash password menggunakan SHA-256
        """
        return hashlib.sha256(password.encode()).hexdigest()

    @staticmethod
    def register(username, password, full_name, email, phone_number, role='penyewa'):
        """
        Mendaftarkan pengguna baru
        """
        # Validasi input
        if not all([username, password, full_name, email]):
            return None, "Semua field wajib diisi"
        
        # Periksa apakah username atau email sudah ada
        existing_user = User.get_by_username_or_email(username, email)
        if existing_user:
            return None, "Username atau email sudah terdaftar"
        
        # Hash password
        hashed_password = AuthController.hash_password(password)
        
        # Buat user baru
        user = User(
            username=username,
            password=hashed_password,
            nama_lengkap=full_name,
            email=email,
            no_telepon=phone_number,
            role=role
        )
        
        user_id = user.save()
        
        if user_id:
            return user, "Registrasi berhasil"
        else:
            return None, "Gagal mendaftarkan pengguna"

    @staticmethod
    def login(username, password):
        """
        Proses login pengguna
        """
        # Hash password yang diinput
        hashed_password = AuthController.hash_password(password)
        
        # Cari pengguna berdasarkan username
        user = User.get_by_username(username)
        
        # Validasi password
        if user and user.password == hashed_password:
            # Periksa status akun
            if user.status == 'nonaktif':
                return None, "Akun Anda tidak aktif"
            
            return user, "Login berhasil"
        
        return None, "Username atau password salah"

    @staticmethod
    def change_password(user_id, current_password, new_password):
        """
        Mengubah password pengguna
        """
        # Validasi input
        if not all([user_id, current_password, new_password]):
            return False, "Semua field wajib diisi"
        
        # Ambil user
        user = User.get_by_id(user_id)
        
        if not user:
            return False, "Pengguna tidak ditemukan"
        
        # Validasi password saat ini
        current_hashed_password = AuthController.hash_password(current_password)
        if current_hashed_password != user.password:
            return False, "Password saat ini salah"
        
        # Hash password baru
        new_hashed_password = AuthController.hash_password(new_password)
        
        # Update password
        result = user.update_password(new_hashed_password)
        
        if result:
            return True, "Password berhasil diubah"
        else:
            return False, "Gagal mengubah password"

    @staticmethod
    def reset_password(email):
        """
        Mengatur ulang password (dalam implementasi nyata, 
        akan menggunakan email recovery)
        """
        user = User.get_by_email(email)
        
        if not user:
            return False, "Email tidak terdaftar"
        
        # Generate temporary password (dalam implementasi nyata, 
        # gunakan metode yang lebih aman)
        import random
        import string
        
        temp_password = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        hashed_temp_password = AuthController.hash_password(temp_password)
        
        # Update password
        result = user.update_password(hashed_temp_password)
        
        if result:
            return True, temp_password
        else:
            return False, "Gagal mereset password"