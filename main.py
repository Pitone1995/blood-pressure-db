import customtkinter as ctk

from ui.auth import do_login

ctk.set_appearance_mode("System")  
ctk.set_default_color_theme("blue")

login_win = ctk.CTk()
login_win.title("Login - Blood pressure DB")
login_win.geometry("400x200")
login_win.resizable(False, False)

entry_user = ctk.CTkEntry(login_win, placeholder_text="Username", width=250)
entry_user.pack(pady=20)

entry_pwd = ctk.CTkEntry(login_win, placeholder_text="Password", show="*", width=250)
entry_pwd.pack(pady=5)

# NOTA: Usiamo lambda per passare i parametri correttamente senza eseguire la funzione all'avvio
btn_login = ctk.CTkButton(
    login_win, 
    text="Login", 
    command=lambda: do_login(entry_user, entry_pwd, login_win), 
    width=250
)
btn_login.pack(pady=20)

login_win.bind("<Return>", lambda event: do_login(entry_user, entry_pwd, login_win))

login_win.mainloop()