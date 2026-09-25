"""
============================================================================
MODULO 4 — CAPITOLO 07 (ULTIMO DEL MODULO)
Progetto: analizzatore di testi + demo Streamlit — portfolio #3
============================================================================

⚠️ PLACEHOLDER — capitolo NON ancora scritto.

----------------------------------------------------------------------------
PERCHÉ ESISTE QUESTO CAPITOLO
----------------------------------------------------------------------------
Capitolo di assemblaggio: prende tutto il modulo e ne fa una cosa sola che
si apre nel browser. Stesso ruolo del cap.10 nel M3 — e va gestito sapendo
com'è andata lì.

⚠️ LEZIONE DAL M3 CAP.10 (voto difficoltà 8.5, motivazione dello studente:
   "difficoltà di tenere mentalmente uniti i pezzi di tutta la pipeline").
   Due conseguenze operative, non opzionali:

   1. Il capitolo deve avere una **mappa della pipeline** all'inizio, con
      il disegno di cosa entra e cosa esce da ogni pezzo. Non alla fine.
   2. Il **deploy va verificato per fattibilità PRIMA** di far costruire il
      pacchetto. Nel M3 il pacchetto era pronto e corretto, poi la policy
      Hugging Face 2026 ha bloccato tutto (Gradio su compute richiede piano
      a pagamento). Qui la demo è **Streamlit Community Cloud**, che al
      momento è gratuito: verificarlo il giorno in cui si scrive il
      capitolo, non darlo per scontato.

----------------------------------------------------------------------------
CONTENUTO PREVISTO
----------------------------------------------------------------------------
  Sez. 1  Mappa della pipeline completa, in un colpo d'occhio
  Sez. 2  Il contratto di inferenza, versione testuale: modello, classi
          ordinate, tokenizer, versione, soglia. Stesse 6 voci del M3
          cap.10, tradotte al testo
  Sez. 3  Struttura del pacchetto: `app/` dedicata, `requirements.txt`
          pinnato, dati di esempio sintetici, README con model card
  Sez. 4  L'app Streamlit: input testo, output categoria + punteggio +
          parole decisive, caricamento del modello una volta sola
  Sez. 5  Deploy su Streamlit Community Cloud, verifica a freddo, latenza
  Sez. 6  🔄 CONFRONTO PRIMA/DOPO (Regola 16, obbligatorio nell'ultimo
          capitolo del modulo): riscrivere il TODO 1 del cap.01 con quello
          che sai adesso, e commentare cosa è cambiato nel modo di pensarci

----------------------------------------------------------------------------
DEFINITION OF DONE (provvisoria)
----------------------------------------------------------------------------
  1) App funzionante in locale
  2) Pacchetto deployabile completo e verificato (niente pesi enormi in git)
  3) **URL pubblico** funzionante → portfolio #3
  4) Model card con le 6 voci del contratto
  5) Sezione 🔄 CONFRONTO PRIMA/DOPO completata
  6) Riga Portfolio aggiornata in CONTESTO_CORSO.md

----------------------------------------------------------------------------
PREREQUISITI E VINCOLI
----------------------------------------------------------------------------
  Prima di aprirlo: cap.06 chiuso, bridge R06 completato.

  Hardware: CPU. Se il modello scelto è troppo pesante per il tier gratuito
  di Streamlit, ripiegare sulla baseline TF-IDF: una demo che funziona batte
  una demo perfetta che non parte.

  ⚠️ Privacy — bloccante: la demo è PUBBLICA. Solo esempi sintetici.
     Nessun testo di documento reale, nemmeno anonimizzato. Vale la stessa
     regola del TODO 6 del M3 cap.10.

  🔁 Ripassi Regola 43 obbligatori: contratto di inferenza (M3 cap.10),
     lazy loading e cold start (M3 cap.10), tutta la pipeline testuale
     dei capitoli 01-06 di questo modulo.

  🌊 [REAL-WORLD] obbligatorio dal M5, ma qui ci sta: consegna vaga del
     tipo "fammi qualcosa che analizzi questi testi" e discussione delle
     scelte.

  🏗️ Progetto (ramo testuale) — chiusura: il ramo testuale diventa un
     componente con interfaccia stabile, pronto per essere chiamato dal
     M5 (LLM) e dal M7 (orchestratore).

----------------------------------------------------------------------------
PROTOCOLLO FINE MODULO (dopo la chiusura del capitolo)
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
    print("Capitolo 07 non ancora scritto: completa prima il cap.06.")
