"""
============================================================================
MODULO 4 — CAPITOLO 02b (parte pratica)
Embeddings: farli funzionare davvero con sentence-transformers
============================================================================

⚠️ PLACEHOLDER — capitolo NON ancora scritto.
   Seconda metà del cap.02 (vedi `02a_embeddings_concetto.py` per il perché
   dello split). Da aprire solo dopo aver chiuso 02a.

----------------------------------------------------------------------------
PERCHÉ ESISTE QUESTA SECONDA PARTE
----------------------------------------------------------------------------
In 02a hai capito l'idea con embedding giocattolo disegnati a mano.
Qui si passa a un modello vero, e cambiano tre cose:
  - le dimensioni non le scegli tu (384, 768…) e non sono interpretabili
  - il modello va scaricato, messo in cache, e la prima esecuzione è lenta
  - la qualità dipende dalla lingua: un modello solo inglese sull'italiano
    dà risultati mediocri in silenzio (di nuovo: il bug che non crasha)

----------------------------------------------------------------------------
CONTENUTO PREVISTO
----------------------------------------------------------------------------
  Sez. 1  Installazione e primo `encode()`: cosa succede davvero al primo
          avvio (download, cache locale, tempo). Dichiarare i MB PRIMA
  Sez. 2  La shape dell'output: ogni frase, corta o lunga, diventa un
          vettore di dimensione FISSA. Confronto con la matrice sparsa
          del cap.01, che invece cresce col vocabolario
  Sez. 3  Modelli multilingua: perché per l'italiano serve il modello
          giusto, e come si legge la scheda del modello per capirlo
  Sez. 4  Confronto diretto sullo stesso corpus `dati/note_documenti.csv`:
          TF-IDF vs embeddings, a parità di query
  Sez. 5  Il caso in cui TF-IDF VINCE: parola rara e letterale (un codice,
          una sigla). Serve per non innamorarsi dello strumento nuovo
  Sez. 6  Normalizzazione dei vettori e coseno: quando i vettori sono
          normalizzati, il dot product È già il coseno

----------------------------------------------------------------------------
DEFINITION OF DONE (provvisoria)
----------------------------------------------------------------------------
  1) Generare embedding di frasi italiane e stampare la shape
  2) Mostrare che due frasi con parole diverse ma stesso senso hanno
     coseno alto, mentre con TF-IDF il punteggio crolla
  3) Esibire un caso concreto in cui TF-IDF batte gli embeddings
  4) Misurare il tempo del primo `encode()` e di quelli successivi
  5) Consegnare il deliverable di prodotto (sotto)

----------------------------------------------------------------------------
PREREQUISITI E VINCOLI
----------------------------------------------------------------------------
  Prima di aprirlo: **02a chiuso** e installazione già fatta:
      pip install transformers sentence-transformers tokenizers
  Farla PRIMA della sessione, non durante. Se il download fallisce, si
  risolve il download — non si studia il concetto arrabbiati.

  Hardware: CPU. Modello piccolo e multilingua, es.
  `paraphrase-multilingual-MiniLM-L12-v2`. Primo `encode()` = download da
  qualche centinaio di MB: avvisare in testa al capitolo.

  ⚠️ Privacy: si entra in contatto con servizi esterni (download modelli).
  Nessun testo di documento reale, nemmeno "per provare".
  Solo `dati/note_documenti.csv`, che è sintetico.

  🔁 Ripassi Regola 43 obbligatori: coseno e norma (cap.01 Sez. 4 —
     lacuna **#59**), TF-IDF e i suoi limiti (cap.01 Sez. 3 e 5),
     cold start e cache (M3 cap.10, qui in versione download modelli).

  📚 Libri: [NLP-TRANS] cap. 2 per il lato tokenizer/modello.

  🏗️ Progetto (ramo testuale): embeddare le note del corpus e verificare
     che documenti dello stesso tipo finiscano vicini. Prima misura
     quantitativa del ramo semantico, che il cap.03 trasformerà in
     decisione con una soglia.

  Esercizi obbligatori (qui, non in 02a): 🎯 COLLOQUIO ("cos'è un
  embedding?" è domanda da colloquio quasi garantita), 🔧 REFACTORING,
  🔍 DEBUG, 🧠 RETRIEVAL, 🔀 INTERLEAVING.
  Quiz di verifica del capitolo 02 completo (02a + 02b) con 1 💬 Feynman.

  Dopo la chiusura: popolare il bridge
  `M04_R01_after_C01_before_C02_testo_to_embeddings.md`? NO —
  il bridge R01 va popolato alla chiusura del **cap.01**. Qui si popola
  `M04_R02_after_C02_before_C03_embeddings_to_similarita.md`.

============================================================================
"""

if __name__ == "__main__":
    print("Capitolo 02b non ancora scritto: completa prima il cap.02a.")
