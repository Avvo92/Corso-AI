"""
============================================================================
MODULO 4 — CAPITOLO 03
Misurare la distanza fra significati: similarità, soglie, top-k
============================================================================

⚠️ PLACEHOLDER — capitolo NON ancora scritto.

----------------------------------------------------------------------------
PERCHÉ ESISTE QUESTO CAPITOLO
----------------------------------------------------------------------------
Il cap.02 produce vettori. Questo capitolo insegna a USARLI per decidere.
È il capitolo che rende operativa la ricerca semantica, ed è il mattone
diretto del RAG del M6: "recuperare i k documenti più simili alla domanda"
è letteralmente quello che si fa qui, in piccolo.

Il salto concettuale: passare da "quanto sono simili" (un numero) a
"sono la stessa cosa?" (una decisione). Serve una SOGLIA, e la soglia si
sceglie sui dati — esattamente come nel M2 cap.04 con il semaforo.

----------------------------------------------------------------------------
CONTENUTO PREVISTO
----------------------------------------------------------------------------
  Sez. 1  Coseno, distanza euclidea, dot product: quando coincidono e
          quando no (vettori normalizzati = dot product è già il coseno)
  Sez. 2  Top-k: trovare i k documenti più simili a una query, in modo
          vettorizzato (una matmul, non un ciclo)
  Sez. 3  La soglia: sopra quale punteggio dico "è un match"?
          Costruzione di una curva punteggio → decisione sui dati
  Sez. 4  Valutare una ricerca: precision@k, recall@k, e perché l'accuracy
          non ha senso qui
  Sez. 5  Falsi amici della similarità: frasi opposte con coseno alto
          (la negazione), testi corti, documenti quasi duplicati
  Sez. 6  Scalabilità a spanne: cosa succede con 10 documenti, 10.000,
          1.000.000 — e perché a un certo punto serve un vector DB (M6)

----------------------------------------------------------------------------
DEFINITION OF DONE (provvisoria)
----------------------------------------------------------------------------
  1) Calcolare la similarità di una query contro N documenti con UNA matmul
  2) Restituire i top-k con punteggio
  3) Scegliere una soglia guardando i dati e dichiarare il criterio
  4) Misurare precision@k e spiegare cosa NON dice
  5) Esibire un caso di falso positivo semantico e spiegarlo

----------------------------------------------------------------------------
PREREQUISITI E VINCOLI
----------------------------------------------------------------------------
  Prima di aprirlo: cap.02 chiuso, bridge R02 completato.
  Hardware: CPU, nessuna installazione nuova rispetto al cap.02.

  🔁 Ripassi Regola 43 obbligatori:
     - soglia e trade-off precision/recall (M2 cap.04): è lo stesso
       ragionamento del semaforo, applicato al matching
     - coseno (cap.01 M4)
     - shape e broadcasting (Ponte / M1 cap.07): la matmul query × documenti

  📚 Libri: [ALAMMAR] sulla semantic search.

  🏗️ Progetto (ramo testuale) — qui nasce il pezzo più utile del modulo:
     **matching cross-documento**. Data una pratica con più documenti,
     verificare che i campi corrispondano (il CF sulla busta paga è lo
     stesso della CU?). Attenzione: per i codici fiscali il confronto
     giusto è ESATTO, non semantico — è un ottimo esercizio di giudizio
     capire dove la similarità serve e dove è la scelta sbagliata.

  📐 Nota: [SYSTEM DESIGN] diventa obbligatorio dal M5, ma qui ci sta bene
     come esercizio facoltativo (come indicizzeresti 100k documenti?).

  Esercizi obbligatori: 🎯 COLLOQUIO, 🔧 REFACTORING, 🔍 DEBUG,
  🧠 RETRIEVAL, 🔀 INTERLEAVING. Quiz ingresso + verifica con 1 💬 Feynman.

============================================================================
"""

if __name__ == "__main__":
    print("Capitolo 03 non ancora scritto: completa prima il cap.02.")
