"""
============================================================================
MODULO 4 — CAPITOLO 07b (ULTIMO DEL MODULO, parte 2)
Progetto: interfaccia Streamlit, deploy e confronto finale — portfolio #3
============================================================================

⚠️ PLACEHOLDER — capitolo NON ancora scritto.
   Si apre SOLO quando la DoD di `07a_progetto_core_testuale.py` è verde:
   il core deve già funzionare da riga di comando.

----------------------------------------------------------------------------
LEZIONE DAL M3 CAP.10 — DA APPLICARE PRIMA DI SCRIVERE IL CAPITOLO
----------------------------------------------------------------------------
Nel M3 il pacchetto per la demo era pronto e corretto, poi la policy
Hugging Face 2026 ha bloccato tutto: gli Space Gradio girano su compute e
richiedono un piano a pagamento. Risultato: portfolio #2 ancora senza URL.

Regola operativa non negoziabile per questo capitolo:
**verificare la fattibilità del deploy PRIMA di far costruire il pacchetto.**
Il giorno in cui si scrive il capitolo, controllare che Streamlit Community
Cloud sia ancora gratuito e utilizzabile. Non darlo per scontato perché lo
era l'anno scorso.

Piano B dichiarato in anticipo: se il modello scelto è troppo pesante per
il tier gratuito, si ripiega sulla baseline TF-IDF del cap.01. Una demo che
funziona batte una demo perfetta che non parte.

----------------------------------------------------------------------------
CONTENUTO PREVISTO
----------------------------------------------------------------------------
  Sez. 0  Verifica di fattibilità del deploy (vedi sopra) — prima di tutto
  Sez. 1  L'app Streamlit: input testo, output categoria + punteggio +
          parole decisive. L'app chiama `analizza_testo()` di 07a e basta:
          nessuna logica duplicata
  Sez. 2  Caricare il modello una volta sola (cache) e perché la prima
          richiesta dopo il deploy è lenta — il **cold start** del M3
  Sez. 3  README e model card con le 6 voci del contratto
  Sez. 4  Deploy, verifica a freddo, misura della latenza
  Sez. 5  🔄 **CONFRONTO PRIMA/DOPO** (Regola 16, obbligatorio nell'ultimo
          capitolo del modulo): riscrivere il TODO 1 del cap.01 con quello
          che sai adesso, e commentare cosa è cambiato nel modo di pensarci
  Sez. 6  🌊 [REAL-WORLD]: consegna vaga ("fammi qualcosa che analizzi
          questi testi") e discussione delle scelte fatte

----------------------------------------------------------------------------
DEFINITION OF DONE (provvisoria)
----------------------------------------------------------------------------
  1) App funzionante in locale, che usa il core di 07a senza riscriverlo
  2) **URL pubblico** funzionante → portfolio #3
  3) Model card con le 6 voci del contratto
  4) Latenza prima chiamata / chiamate successive annotata
  5) Sezione 🔄 CONFRONTO PRIMA/DOPO completata
  6) Riga Portfolio aggiornata in CONTESTO_CORSO.md

----------------------------------------------------------------------------
PREREQUISITI E VINCOLI
----------------------------------------------------------------------------
  Prima di aprirlo: **07a chiuso con DoD verde**.
  Hardware: CPU.

  ⚠️ Privacy — bloccante: la demo è PUBBLICA. Solo esempi sintetici.
     Nessun testo di documento reale, nemmeno anonimizzato. Stessa regola
     del TODO 6 del M3 cap.10.

  🔁 Ripassi Regola 43 obbligatori: lazy loading e cold start (M3 cap.10),
     contratto di inferenza (07a), baseline TF-IDF del cap.01 — che serve
     sia come piano B sia come termine di paragone nel CONFRONTO.

----------------------------------------------------------------------------
PROTOCOLLO FINE MODULO (dopo la chiusura di 07b)
----------------------------------------------------------------------------
  1) Protocollo FINE CAPITOLO completo (correzione, voto difficoltà,
     aggiornamento CONTESTO, commit)
  2) Verificare che 🔄 CONFRONTO PRIMA/DOPO sia stato fatto
  3) Verificare che la demo sia deployata e raggiungibile
  4) Aggiornare la tabella Portfolio con l'URL
  5) Scommentare le dipendenze del M5 in `requirements.txt`
  6) Creare `archivi/ARCHIVIO_MODULO_04.md`

  ⚠️ Promemoria: l'**archivio del M3 è ancora aperto** (portfolio #2 senza
     URL, cap.12 Grad-CAM da svolgere, TODO 7 e confronto prima/dopo del
     cap.10). Se nel frattempo non è stato chiuso, decidere qui: chiuderlo
     o archiviarlo dichiarando il residuo.

============================================================================
"""

if __name__ == "__main__":
    print("Capitolo 07b non ancora scritto: completa prima il cap.07a.")
