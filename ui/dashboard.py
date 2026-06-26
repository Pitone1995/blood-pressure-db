# ui/dashboard.py
import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from database.queries import salva_misurazione_db, ottieni_storico_db, ottieni_dati_grafico_db

def main_window(user):
    app = ctk.CTk()
    app.title(f"@{user} - Blood pressure DB")
    app.geometry("700x700")
    app.resizable(False, False)
    
    def apri_finestra_grafico():
        dati = ottieni_dati_grafico_db(user)
        
        if not dati or len(dati) < 2:
            messagebox.showwarning("Attenzione", "Inserisci almeno 2 misurazioni per generare il grafico!")
            return
            
        lista_sys = []
        lista_dias = []
        lista_hr = []
        lista_date = []
        
        for sys, dia, puls, data_ora in dati:
            lista_sys.append(sys)
            lista_dias.append(dia)
            lista_hr.append(puls)
            
            # PARSING AD ALTA PRECISIONE: Trasformiamo in oggetto datetime completo di millisecondi
            oggetto_data = datetime.strptime(data_ora, "%Y-%m-%d %H:%M:%S.%f")
            lista_date.append(oggetto_data)
            
        finestra_grafico = ctk.CTkToplevel(app)
        finestra_grafico.title(f"Grafico Andamento - @{user}")
        finestra_grafico.geometry("800x500")
        finestra_grafico.after(100, lambda: finestra_grafico.focus())
        
        fig, ax = plt.subplots(figsize=(8, 5), dpi=100)
        
        # Plotting continuo basato sul tempo reale
        ax.plot(lista_date, lista_sys, marker='o', color='#E63946', linewidth=2, label='SYS (Massima)')
        ax.plot(lista_date, lista_dias, marker='s', color='#457B9D', linewidth=2, label='DIAS (Minima)')
        ax.plot(lista_date, lista_hr, marker='^', color='#E9C46A', linewidth=1.5, linestyle='--', label='HR (Battiti)')
        
        # Formattazione dell'asse X tramite mdates per gestire la linea del tempo senza accavallare i punti
        formato_data = mdates.DateFormatter('%H:%M:%S')
        ax.xaxis.set_major_formatter(formato_data)
        
        ax.set_title("Andamento Temporale ad Alta Precisione", fontsize=14, fontweight='bold', pad=15)
        ax.set_xlabel("Orario di registrazione", fontsize=11, labelpad=10)
        ax.set_ylabel("Valori (mmHg / bpm)", fontsize=11, labelpad=10)
        ax.grid(True, linestyle=':', alpha=0.6)
        ax.legend(loc="upper left")
        
        plt.xticks(rotation=25, ha="right")
        plt.tight_layout()
        
        canvas = FigureCanvasTkAgg(fig, master=finestra_grafico)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=15, pady=15)

    def aggiorna_visualizzazione_storico():
        for widget in frame_storico.winfo_children():
            widget.destroy()
            
        storico = ottieni_storico_db(user)
        if not storico:
            label_vuoto = ctk.CTkLabel(frame_storico, text="Nessuna misurazione registrata.", font=("Arial", 13, "italic"))
            label_vuoto.pack(pady=20)
            return
            
        for sys, dia, puls, data_ora in storico:
            # Tagliamo via i millisecondi lasciando visibili i secondi nello storico visivo
            data_pulita = data_ora[:19]
            testo_riga = f"📅 {data_pulita}  |  MAX: {sys} mmHg  |  MIN: {dia} mmHg  |  💓 {puls} bpm"
            
            lbl_riga = ctk.CTkLabel(frame_storico, text=testo_riga, font=("Courier New", 13), anchor="w")
            lbl_riga.pack(fill="x", padx=10, pady=5)
            separatore = ctk.CTkFrame(frame_storico, height=1, fg_color="gray30")
            separatore.pack(fill="x", padx=10)

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
            aggiorna_visualizzazione_storico()
        else:
            messagebox.showerror("Errore", "Impossibile salvare i dati.")

    # --- GRAPHICS CONTENT ---
    label_titolo = ctk.CTkLabel(app, text="Gestione Pressione Sanguigna", font=("Arial", 22, "bold"))
    label_titolo.pack(pady=15)
    
    entry_sis = ctk.CTkEntry(app, placeholder_text="Pressione Sistolica (Massima) es. 120", width=350)
    entry_sis.pack(pady=8)
    
    entry_dia = ctk.CTkEntry(app, placeholder_text="Pressione Diastolica (Minima) es. 80", width=350)
    entry_dia.pack(pady=8)
    
    entry_puls = ctk.CTkEntry(app, placeholder_text="Pulsazioni (Battiti al minuto) es. 72", width=350)
    entry_puls.pack(pady=8)
    
    btn_salva = ctk.CTkButton(app, text="Salva nel Database", command=inserisci_dati, width=350, fg_color="green", hover_color="darkgreen")
    btn_salva.pack(pady=10)
    
    btn_grafico = ctk.CTkButton(app, text="📊 Mostra Grafico Andamento", command=apri_finestra_grafico, width=350, fg_color="#457B9D", hover_color="#1D3557")
    btn_grafico.pack(pady=5)
    
    label_titolo_storico = ctk.CTkLabel(app, text="Cronologia Misurazioni", font=("Arial", 16, "bold"))
    label_titolo_storico.pack(pady=(15, 5))
    
    frame_storico = ctk.CTkScrollableFrame(app, width=500, height=180, label_text=None)
    frame_storico.pack(pady=10)
    
    aggiorna_visualizzazione_storico()
    
    label_footer = ctk.CTkLabel(app, text=f"Utente attivo: {user}", font=("Arial", 11, "italic"))
    label_footer.pack(side="bottom", pady=5)
    
    app.mainloop()