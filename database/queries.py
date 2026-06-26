# database/queries.py
import sqlite3
import os

DB_PATH = os.path.join("storage", "app_data.db")

def verify_user(username, password):
    """Cerca nel database se esiste la combinazione username/password."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Usiamo i placeholders (?) per evitare SQL Injection (sicurezza)
    cursor.execute("SELECT * FROM utenti WHERE username = ? AND password = ?", (username, password))
    utente = cursor.fetchone()
    
    conn.close()
    
    # Se trova una riga ritorna True, altrimenti False
    return utente is not None

# In fondo a database/queries.py

def ottieni_id_utente(username):
    """Prende l'ID dell'utente partendo dal suo username."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM utenti WHERE username = ?", (username,))
    risultato = cursor.fetchone()
    conn.close()
    return risultato[0] if risultato else None

def salva_misurazione_db(username, sistolica, diastolica, pulsazioni):
    """Salva i dati della pressione legandoli all'utente loggato."""
    utente_id = ottieni_id_utente(username)
    if not utente_id:
        return False
        
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO misurazioni (utente_id, sistolica, diastolica, pulsazioni)
            VALUES (?, ?, ?, ?)
        """, (utente_id, int(sistolica), int(diastolica), int(pulsazioni)))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Errore nel salvataggio: {e}")
        return False

def ottieni_storico_db(username):
    """Recupera tutte le misurazioni dell'utente ordinate dalla più recente."""
    utente_id = ottieni_id_utente(username)
    if not utente_id:
        return []
        
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Selezioniamo i dati ordinandoli per data decrescente (DESC)
    cursor.execute("""
        SELECT sistolica, diastolica, pulsazioni, data_ora 
        FROM misurazioni 
        WHERE utente_id = ? 
        ORDER BY data_ora DESC
    """, (utente_id,))
    
    cronologia = cursor.fetchall()
    conn.close()
    return cronologia  # Ritorna una lista di tuple [(120, 80, 72, '2026-...'), ...]