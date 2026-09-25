"""
============================================================================
MODULO 4 — CAPITOLO 05
HuggingFace: l'npm dell'AI
============================================================================

⚠️ PLACEHOLDER — capitolo NON ancora scritto.

----------------------------------------------------------------------------
PERCHÉ ESISTE QUESTO CAPITOLO
----------------------------------------------------------------------------
Da qui in poi, nel mondo reale, non scrivi modelli: ne scegli uno e lo
integri. HuggingFace è il registro pubblico dove stanno. Il parallelo con
npm regge quasi ovunque: cerchi un pacchetto, leggi la scheda, controlli
licenza e manutenzione, lo installi, lo usi.

E, come con npm, la competenza vera non è la sintassi: è **scegliere** e
**diffidare**. Un modello con 3 download e nessuna model card è la
dipendenza abbandonata da due anni che non metti in produzione.

----------------------------------------------------------------------------
CONTENUTO PREVISTO
----------------------------------------------------------------------------
  Sez. 1  L'Hub: modelli, dataset, Spaces. Come si legge una **model card**
          (e il collegamento diretto: la model card a 6 voci che hai scritto
          tu nel M3 cap.10 era esattamente questo)
  Sez. 2  `pipeline()`: la scorciatoia in tre righe. Cosa fa di nascosto
  Sez. 3  Aprire la scatola: `AutoTokenizer` + `AutoModel`.
          Tokenizzazione a sotto-parole vista sul serio — la risposta al
          LIMITE 3 (fuori vocabolario) del cap.01
  Sez. 4  Token speciali, `attention_mask`, padding e troncamento:
          i quattro dettagli che fanno sbagliare tutti la prima volta
  Sez. 5  Scegliere un modello: lingua (l'italiano!), dimensione, licenza,
          data, download. Checklist operativa
  Sez. 6  Cache locale, dimensione dei download, primo avvio lento
          (è il **cold start** del M3 cap.10, altra forma)

----------------------------------------------------------------------------
DEFINITION OF DONE (provvisoria)
----------------------------------------------------------------------------
  1) Usare `pipeline()` per almeno due compiti diversi
  2) Rifare lo stesso lavoro a mano con AutoTokenizer + AutoModel
  3) Spiegare cosa sono `input_ids` e `attention_mask`
  4) Mostrare come una parola inventata viene spezzata in sotto-parole
  5) Motivare la scelta di un modello con 3 criteri espliciti

----------------------------------------------------------------------------
PREREQUISITI E VINCOLI
----------------------------------------------------------------------------
  Prima di aprirlo: cap.04 chiuso, bridge R04 completato.

  Hardware: CPU. Regola ferrea del capitolo: modelli piccoli, preferibilmente
  multilingua o italiani. Dichiarare SEMPRE la dimensione del download prima
  di farlo partire. Colab solo se un esercizio lo richiede davvero.

  ⚠️ Privacy: qui si entra in contatto con servizi esterni. Nessun testo di
  documento reale, nemmeno "per provare". Solo `dati/note_documenti.csv`.

  🔁 Ripassi Regola 43 obbligatori:
     - tokenizzazione a parole e fuori vocabolario (cap.01 M4)
     - model card e contratto di inferenza (M3 cap.10): stessa disciplina
     - cold start (M3 cap.10)

  📚 Libri: [NLP-TRANS] cap. 2 (è letteralmente il libro degli autori della
     libreria) + [ALAMMAR].

  🏗️ Progetto (ramo testuale): primo tentativo di **estrazione campi** dal
     testo OCR con un modello pre-addestrato (NER — Named Entity
     Recognition, cioè "trova i nomi, le date, gli importi dentro la
     frase"). Confronto onesto con le regex del cap.01: dove vince l'una,
     dove vince l'altra. Spesso per un codice fiscale la regex vince.

  Esercizi obbligatori: 🎯 COLLOQUIO, 🔧 REFACTORING, 🔍 DEBUG,
  🧠 RETRIEVAL, 🔀 INTERLEAVING. Quiz ingresso + verifica con 1 💬 Feynman.

============================================================================
"""

if __name__ == "__main__":
    print("Capitolo 05 non ancora scritto: completa prima il cap.04.")
