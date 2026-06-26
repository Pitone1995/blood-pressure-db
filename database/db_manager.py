# database/db_manager.py
import sqlite3
import os

DB_PATH = os.path.join("storage", "app_data.db")

def inizializza_db():
    """Crea la cartella storage e le tabelle se non esistono."""
    if not os.path.exists("storage"):
        os.makedirs("storage")
        
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 1. Tabella Utenti
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS utenti (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)
    
    # 2. Tabella Misurazioni Pressione (supporto millisecondi stringa)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS misurazioni (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            utente_id INTEGER NOT NULL,
            sistolica INTEGER NOT NULL,
            diastolica INTEGER NOT NULL,
            pulsazioni INTEGER NOT NULL,
            data_ora TEXT NOT NULL,
            FOREIGN KEY(utente_id) REFERENCES utenti(id)
        )
    """)
    
    # Utente di test predefinito
    cursor.execute("SELECT COUNT(*) FROM utenti")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO utenti (username, password) VALUES (?, ?)", ("pitone", "1234"))
        conn.commit()
        
    conn.close()