"""
============================================================================
MODULO 4 — CAPITOLO 02
Embeddings: le coordinate del significato
============================================================================

⚠️ PLACEHOLDER — capitolo NON ancora scritto.
   Questo file esiste per fissare struttura, prerequisiti e vincoli.
   Il mentor lo sostituisce con il capitolo completo quando il cap.01 è chiuso.

----------------------------------------------------------------------------
PERCHÉ ESISTE QUESTO CAPITOLO
----------------------------------------------------------------------------
È IL capitolo più importante del modulo, e forse della seconda metà del
corso. Senza embeddings non esistono ricerca semantica, RAG (M6), memoria
degli agenti (M7). Se un capitolo del M4 va studiato due volte, è questo.

Il capitolo si apre come RISPOSTA ai tre limiti chiusi nel cap.01:
  - sinonimi ("cedolino" ≠ "busta paga" per TF-IDF)
  - ordine perso ("il netto supera il lordo" = "il lordo supera il netto")
  - fuori vocabolario (parola mai vista → ignorata in silenzio)

Non presentarli come tecnologia a sé: presentarli come la cosa che ripara
quei tre buchi.

----------------------------------------------------------------------------
CONTENUTO PREVISTO
----------------------------------------------------------------------------
  Sez. 1  Da "una casella per parola" a "un punto nello spazio":
          perché poche centinaia di dimensioni invece di migliaia di caselle
  Sez. 2  L'idea di Word2Vec: una parola è definita dalla compagnia che
          frequenta. Il famoso re - uomo + donna ≈ regina (con onestà su
          quanto funziona davvero e quanto è aneddoto)
  Sez. 3  Da parola a FRASE: perché la media degli embedding di parola è
          una baseline debole e cosa fanno i sentence-transformers
  Sez. 4  `sentence-transformers` in pratica: `encode()`, shape dell'output,
          modelli multilingua (l'italiano non è un dettaglio)
  Sez. 5  Cosa gli embedding NON catturano: negazione, numeri, entità
          specifiche. Serve per non promettere magia al capitolo 03
  Sez. 6  Confronto diretto sullo stesso corpus: TF-IDF vs embeddings,
          con un caso in cui TF-IDF vince (parola rara e letterale)

----------------------------------------------------------------------------
DEFINITION OF DONE (provvisoria)
----------------------------------------------------------------------------
  1) Spiegare con parole tue cos'è un embedding, senza dire "vettore"
  2) Generare embedding di frasi italiane con sentence-transformers
  3) Sapere che ogni frase, corta o lunga, diventa un vettore di dimensione FISSA
  4) Mostrare un caso in cui gli embedding battono TF-IDF e uno in cui no
  5) Elencare 2 cose che gli embedding non catturano

----------------------------------------------------------------------------
PREREQUISITI E VINCOLI
----------------------------------------------------------------------------
  Prima di aprirlo:
    - cap.01 chiuso (tokenizzazione, BoW, TF-IDF, coseno)
    - bridge `M04_R01_after_C01_before_C02_testo_to_embeddings.md` completato
    - INSTALLAZIONE: `pip install transformers sentence-transformers tokenizers`
      (già scommentate in requirements.txt — vanno installate PRIMA, non durante)

  Hardware: CPU. Usare modelli piccoli e multilingua, es.
    `paraphrase-multilingual-MiniLM-L12-v2`. Primo `encode()` = download
    di qualche centinaio di MB: avvisare, non lasciarlo scoprire a metà esercizio.

  🔁 Ripassi Regola 43 obbligatori: similarità coseno (cap.01 M4 / Ponte),
     i tre limiti della Sez. 5 del cap.01, normalizzazione dei vettori.

  📚 Libri: [ALAMMAR] cap. 2 (token ed embedding, figure) — è il capitolo
     dove il libro rende di più. [NLP-TRANS] cap. 2 per il lato tokenizer.

  🏗️ Progetto (ramo testuale): sostituire in `testo_utils.py` il confronto
     lessicale con uno semantico; embeddare le "note pratica" e verificare
     che documenti della stessa pratica finiscano vicini.

  Esercizi obbligatori: 🎯 COLLOQUIO ("cos'è un embedding?" è domanda da
  colloquio quasi garantita), 🔧 REFACTORING, 🔍 DEBUG, 🧠 RETRIEVAL,
  🔀 INTERLEAVING. Quiz ingresso + quiz verifica con almeno 1 💬 Feynman.

============================================================================
"""

if __name__ == "__main__":
    print("Capitolo 02 non ancora scritto: completa prima il cap.01.")
