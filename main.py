import tkinter as tk
from config.database import create_database_and_tables
from views.login_view import LoginView

def main():
    # create_database_and_tables()
    
    root = tk.Tk()
    
    window_width = 400
    window_height = 300
    
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)
    
    root.geometry(f'{window_width}x{window_height}+{x}+{y}')
    root.title("Rental Kendaraan - Login")
    
    LoginView(root)
    
    root.mainloop()

if __name__ == "__main__":
    main()