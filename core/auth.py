# core/auth.py
from tkinter import messagebox
from ui.dashboard import main_window
from database.queries import verifica_utente_db 

def effettua_login(entry_user, entry_pwd, login_win):
    username = entry_user.get()
    password = entry_pwd.get()
    
    if verifica_utente_db(username, password):
        login_win.destroy()  
        main_window(username)  
    else:
        messagebox.showerror("Errore", "Username o Password errati!")