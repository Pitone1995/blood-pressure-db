from tkinter import messagebox

from ui.dashboard import main_window

USER = "pitone"
PWD = "1234"

def do_login(entry_user, entry_pwd, login_win):

    username = entry_user.get()
    password = entry_pwd.get()
    
    # if verify_user_pwd(username, password):
    login_win.destroy()
    main_window(username)
    # else:
        # messagebox.showerror("Error", "Wrong username or password")

def verify_user_pwd(username, password):
    return username == USER and password == PWD