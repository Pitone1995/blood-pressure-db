from tkinter import messagebox

from ui.dashboard import main_window

from database.queries import verify_user

def do_login(entry_user, entry_pwd, login_win):

    username = entry_user.get()
    password = entry_pwd.get()
    
    if verify_user(username, password):
        login_win.destroy()
        main_window(username)
    else:
        messagebox.showerror("Error", "Wrong username or password")