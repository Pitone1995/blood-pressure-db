# dahboard.py

import customtkinter as ctk

def main_window(user):
    app = ctk.CTk()
    app.title(f"@{user} - Blood pressure DB")
    app.geometry("600x400")
    
    label_titolo = ctk.CTkLabel(app, text=f"Welcome {user} to your Blood Pressure DB", font=("Arial", 20, "bold"))
    label_titolo.pack(pady=30)
        
    app.mainloop()