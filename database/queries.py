# database/queries.py
import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join("storage", "app_data.db")

def verifica_utente_db(username, password):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM utenti WHERE username = ? AND password = ?", (username, password))
    utente = cursor.fetchone()
    conn.close()
    return utente is not None

def ottieni_id_utente(username):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM utenti WHERE username = ?", (username,))
    risultato = cursor.fetchone()
    conn.close()
    return risultato[0] if risultato else None

def salva_misurazione_db(username, sistolica, diastolica, pulsazioni):
    utente_id = ottieni_id_utente(username)
    if not utente_id:
        return False
        
    # Genera data con precisione millimetrica (%f = microsecondi, troncata a ms)
    data_ora_ms = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO misurazioni (utente_id, sistolica, diastolica, pulsazioni, data_ora)
            VALUES (?, ?, ?, ?, ?)
        """, (utente_id, int(sistolica), int(diastolica), int(pulsazioni), data_ora_ms))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Errore nel salvataggio: {e}")
        return False

def ottieni_storico_db(username):
    utente_id = ottieni_id_utente(username)
    if not utente_id:
        return []
        
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT sistolica, diastolica, pulsazioni, data_ora 
        FROM misurazioni 
        WHERE utente_id = ? 
        ORDER BY data_ora DESC
    """, (utente_id,))
    cronologia = cursor.fetchall()
    conn.close()
    return cronologia

def ottieni_dati_grafico_db(username):
    """Estrazione ordinata per data crescente (necessaria per il grafico continuo)"""
    utente_id = ottieni_id_utente(username)
    if not utente_id:
        return []
        
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT sistolica, diastolica, pulsazioni, data_ora 
        FROM misurazioni 
        WHERE utente_id = ? 
        ORDER BY data_ora ASC
    """, (utente_id,))
    dati = cursor.fetchall()
    conn.close()
    return dati