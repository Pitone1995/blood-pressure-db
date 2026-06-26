# ui/dashboard.py
import customtkinter as ctk
from tkinter import messagebox
from database.queries import salva_misurazione_db, ottieni_storico_db

def main_window(user):
    app = ctk.CTk()
    app.title(f"@{user} - Blood pressure DB")
    app.geometry("800x600")  # Allargata leggermente per fare spazio allo storico
    app.resizable(False, False)
    
    # --- FUNZIONE PER AGGIORNARE LO STORICO A SCHERMO ---
    def aggiorna_visualizzazione_storico():
        # Cancella i vecchi elementi grafici dentro il frame scorrevole (se ce ne sono)
        for widget in frame_storico.winfo_children():
            widget.destroy()
            
        # Prende i dati aggiornati dal database
        storico = ottieni_storico_db(user)
        
        if not storico:
            label_vuoto = ctk.CTkLabel(frame_storico, text="Nessuna misurazione registrata.", font=("Arial", 13, "italic"))
            label_vuoto.pack(pady=20)
            return
            
        # Genera una riga visiva per ogni misurazione trovata
        for sis, dia, puls, data_ora in storico:
            # Formattiamo la data (SQLite salva in formato YYYY-MM-DD HH:MM:SS)
            # Tagliamo i secondi per renderla più pulita
            data_pulita = data_ora[:-3] 
            
            testo_riga = f"📅 {data_pulita}  |  MAX: {sis} mmHg  |  MIN: {dia} mmHg  |  💓 {puls} bpm"
            
            # Creiamo una label per questa specifica misurazione
            lbl_riga = ctk.CTkLabel(
                frame_storico, 
                text=testo_riga, 
                font=("Courier New", 13), # Font a larghezza fissa per tenere incolonnato
                anchor="w",
                justify="left"
            )
            lbl_riga.pack(fill="x", padx=10, pady=5)
            
            # Aggiungiamo una sottile linea di separazione visiva
            separatore = ctk.CTkFrame(frame_storico, height=1, fg_color="gray30")
            separatore.pack(fill="x", padx=10)

    # --- FUNZIONE INTERNA DI INSERIMENTO ---
    def inserisci_dati():
        sis = entry_sis.get()
        dia = entry_dia.get()
        puls = entry_puls.get()
        
        if not (sis.isdigit() and dia.isdigit() and puls.isdigit()):
            messagebox.showerror("Errore", "Inserisci solo numeri validi nei campi!")
            return
            
        if salva_misurazione_db(user, sis, dia, puls):
            messagebox.showinfo("Successo", "Misurazione salvata correttamente!")
            entry_sis.delete(0, 'end')
            entry_dia.delete(0, 'end')
            entry_puls.delete(0, 'end')
            
            # AGGIORNAMENTO IN TEMPO REALE: ricarica lo storico subito dopo il salvataggio!
            aggiorna_visualizzazione_storico()
        else:
            messagebox.showerror("Errore", "Impossibile salvare i dati.")

    # --- INTERFACCIA GRAFICA ---
    label_titolo = ctk.CTkLabel(app, text="Gestione Pressione Sanguigna", font=("Arial", 22, "bold"))
    label_titolo.pack(pady=15)
    
    # Sezione Input
    entry_sis = ctk.CTkEntry(app, placeholder_text="Pressione Sistolica (Massima) es. 120", width=350)
    entry_sis.pack(pady=8)
    
    entry_dia = ctk.CTkEntry(app, placeholder_text="Pressione Diastolica (Minima) es. 80", width=350)
    entry_dia.pack(pady=8)
    
    entry_puls = ctk.CTkEntry(app, placeholder_text="Pulsazioni (Battiti al minuto) es. 72", width=350)
    entry_puls.pack(pady=8)
    
    btn_salva = ctk.CTkButton(app, text="Salva nel Database", command=inserisci_dati, width=350, fg_color="green", hover_color="darkgreen")
    btn_salva.pack(pady=15)
    
    # Sezione Storico (Titolo + Frame Scorrevole)
    label_titolo_storico = ctk.CTkLabel(app, text="Cronologia Misurazioni", font=("Arial", 16, "bold"))
    label_titolo_storico.pack(pady=(10, 5))
    
    # CTkScrollableFrame crea automaticamente la barra di scorrimento se i dati eccedono l'altezza (200px)
    frame_storico = ctk.CTkScrollableFrame(app, width=580, height=200, label_text=None)
    frame_storico.pack(pady=10)
    
    # Primo caricamento dello storico all'apertura della finestra
    aggiorna_visualizzazione_storico()
    
    # Footer
    label_footer = ctk.CTkLabel(app, text=f"Utente attivo: {user}", font=("Arial", 11, "italic"))
    label_footer.pack(side="bottom", pady=5)
    
    app.mainloop()