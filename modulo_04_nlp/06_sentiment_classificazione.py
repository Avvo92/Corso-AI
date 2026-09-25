"""
============================================================================
MODULO 4 — CAPITOLO 06
Classificare testo davvero: sentiment, categorie, baseline vs modello
============================================================================

⚠️ PLACEHOLDER — capitolo NON ancora scritto.

----------------------------------------------------------------------------
PERCHÉ ESISTE QUESTO CAPITOLO
----------------------------------------------------------------------------
È il capitolo in cui il M4 chiude il cerchio con il M2: stesso mestiere
(classificare), materia prima diversa (testo invece di colonne).

Il punto didattico centrale non è "usare un modello grosso": è il
**confronto onesto**. Da un lato la baseline TF-IDF + regressione logistica
del cap.01, dall'altro un modello pre-addestrato. Se il modello grosso non
batte la baseline, la notizia è quella — e saperla leggere è una competenza
da senior, non da junior.

----------------------------------------------------------------------------
CONTENUTO PREVISTO
----------------------------------------------------------------------------
  Sez. 1  Tre modi di classificare testo, in ordine di costo crescente:
          baseline TF-IDF → embeddings + classificatore semplice →
          modello pre-addestrato fine-tunato (che è M8, qui solo nominato)
  Sez. 2  Sentiment analysis con `pipeline()`: cosa restituisce, cosa
          significa davvero quel punteggio di confidenza
  Sez. 3  Zero-shot classification: classificare in categorie che il
          modello non ha mai visto in training. Utile e sopravvalutato
  Sez. 4  Metriche per il testo: le stesse del M2 cap.04, ma con classi
          quasi sempre sbilanciate e confini sfumati
  Sez. 5  Analisi degli errori: leggere i testi sbagliati uno per uno.
          Nel testo è più informativo di qualunque metrica aggregata
  Sez. 6  Il modello sbaglia o l'etichetta è sbagliata? Ambiguità delle
          annotazioni, e perché due persone etichettano diversamente

----------------------------------------------------------------------------
DEFINITION OF DONE (provvisoria)
----------------------------------------------------------------------------
  1) Una baseline TF-IDF misurata, con numeri scritti
  2) Un modello pre-addestrato misurato sugli STESSI dati e split
  3) Una tabella di confronto con costo (tempo, dipendenze) oltre alla metrica
  4) Almeno 5 errori letti a mano e commentati
  5) Una raccomandazione motivata: quale dei due metteresti in produzione

----------------------------------------------------------------------------
PREREQUISITI E VINCOLI
----------------------------------------------------------------------------
  Prima di aprirlo: cap.05 chiuso, bridge R05 completato.
  Hardware: CPU per l'inferenza. Nessun fine-tuning qui (è M8).

  🔁 Ripassi Regola 43 obbligatori — è il capitolo con più richiami:
     - metriche, precision/recall, classi sbilanciate (M2 cap.04) → lacuna
       🟡 **#53** ancora aperta: qui va chiusa con numeri ASSOLUTI, non solo
       percentuali, e con la leva soglia esplicitata
     - train/test split stratificato e leakage (M2 cap.05)
     - baseline TF-IDF (cap.01 M4)

  ⚠️ Attenzione al riuso del cap.01: la baseline del TODO 1 del cap.01 è il
     punto di partenza. Va ripresa con ripasso propositivo, non citata a freddo.

  📚 Libri: [NLP-TRANS] cap. 2 (text classification end-to-end) e cap. 5.

  🏗️ Progetto (ramo testuale) — versione definitiva del pezzo:
     `prob_tipo_doc_testuale` che diventa una feature del modello M2,
     accanto a `prob_busta_paga_visivo` del M3. Qui i tre rami si
     incontrano davvero, ed è il momento giusto per un 🔀 INTERLEAVING
     serio sui tre segnali in disaccordo (ripreso dal TODO 6 del cap.01).

  Esercizi obbligatori: 🎯 COLLOQUIO, 🔧 REFACTORING, 🔍 DEBUG,
  🧠 RETRIEVAL, 🔀 INTERLEAVING. Quiz ingresso + verifica con 1 💬 Feynman.

============================================================================
"""

if __name__ == "__main__":
    print("Capitolo 06 non ancora scritto: completa prima il cap.05.")
