# ui/login.py
import customtkinter as ctk
from core.auth import effettua_login

def mostra_schermata_login():
    login_win = ctk.CTk()
    login_win.title("Login - Blood pressure DB")
    login_win.geometry("400x350")
    login_win.resizable(False, False)

    label_login = ctk.CTkLabel(login_win, text="Accedi al Sistema", font=("Arial", 18, "bold"))
    label_login.pack(pady=(30, 20))

    entry_user = ctk.CTkEntry(login_win, placeholder_text="Username", width=250)
    entry_user.pack(pady=10)

    entry_pwd = ctk.CTkEntry(login_win, placeholder_text="Password", show="*", width=250)
    entry_pwd.pack(pady=10)

    btn_login = ctk.CTkButton(
        login_win, 
        text="Login", 
        command=lambda: effettua_login(entry_user, entry_pwd, login_win), 
        width=250
    )
    btn_login.pack(pady=20)

    # Associa la pressione del tasto "Invio" al login
    login_win.bind("<Return>", lambda event: effettua_login(entry_user, entry_pwd, login_win))

    login_win.mainloop()