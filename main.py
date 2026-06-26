# main.py
import customtkinter as ctk
from database.db_manager import inizializza_db
from ui.login import mostra_schermata_login

# 1. Inizializza il Database (crea cartella storage, tabelle e utente test)
inizializza_db()

# 2. Configura l'aspetto globale dell'interfaccia
ctk.set_appearance_mode("System")  
ctk.set_default_color_theme("blue")

# 3. Avvia la schermata di login (Entry Point dell'applicazione)
if __name__ == "__main__":
    mostra_schermata_login()