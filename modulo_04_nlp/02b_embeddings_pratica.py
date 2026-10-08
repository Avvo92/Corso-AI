"""
============================================================================
MODULO 4 — CAPITOLO 02b (parte pratica)
Embeddings: farli funzionare con sentence-transformers
============================================================================

DA DOVE VIENI
-------------
In 02a hai CALCOLATO una mappa da 30 documenti: co-occorrenze → PPMI → SVD.
Quattro numeri per parola, zero download. Ha mostrato il fenomeno.
Qui usi un modello già addestrato su miliardi di frasi. Le dimensioni
non le scegli tu (qui 384). Non hanno un nome. La qualità dipende dalla
lingua del modello: uno solo inglese sull'italiano peggiora in silenzio.

PRIMA DI APRIRE QUESTO FILE
---------------------------
Nel venv del corso:

    pip install sentence-transformers>=3.3

(già in `requirements.txt`). Farlo PRIMA della sessione. Il primo
`encode()` scarica il modello (qualche centinaio di MB) e lo mette in
cache. I giri dopo sono locali e veloci.

Hardware: CPU va benissimo. MiniLM è piccolo. La 3060 non serve.
Privacy: solo `dati/note_documenti.csv` (testo sintetico). Nessun OCR reale.

L'ANALOGIA
----------
02a = disegnare tu una cartina di 30 strade.
02b = aprire Google Maps: qualcuno ha già misurato il mondo.
Tu chiedi l'indirizzo di una frase e ti arrivano 384 numeri.

📚 LETTURA PARALLELA — [ALAMMAR cap. 2–3] / [NLP-TRANS cap. 5]
Preso: `encode()` su frasi, vettore di lunghezza fissa, modello
multilingua. Scartato: addestrare sentence-transformers da zero.
"""

from __future__ import annotations

import time
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

from testo_utils import (
    DIM,
    PERCORSO_DATI,
    carica_mappa,
    coseno,
    tokenizza,
    vettore_frase,
)

QUI = Path(__file__).resolve().parent
MODELLO_ST = "paraphrase-multilingual-MiniLM-L12-v2"
# MiniLM multilingua: italiano compreso. ~384 numeri per frase.


# ==========================================================================
# QUIZ D'INGRESSO — sul 02a. Rispondi prima di scendere.
# ==========================================================================
#
# Q1. `costruisci_mappa` è più vicina a `fit` o a `transform`? E `vettore_frase`?
# Q2. Vero o falso: se ricostruisco la mappa con dim=8, i vettori a 4 numeri
#     già in database restano confrontabili col coseno.
# Q3. Una frase di sole parole sconosciute: `vettore_frase` cosa restituisce,
#     e il coseno con una frase vera quanto fa?
# Q4. Perché in produzione si fa `carica_mappa` e non `costruisci_mappa`
#     a ogni query?
# Q5. Completa: le dimensioni della SVD (e quelle di un modello vero) hanno
#     un nome di parola? Sì / no, in una riga.
# Q6. Tre job, tre righe (Pattern #6): (a) cosa guadagni con la mappa rispetto
#     al full-text; (b) cosa NON guadagni; (c) un caso in cui vince il match
#     esatto (CF, IBAN, …).
# Q7. Type hint: il tipo di un vettore NumPy è `np.array` o `np.ndarray`?
#
# TUE RISPOSTE:
#


# ==========================================================================
# 🔁 RIPASSO PROPOSITIVO — 02a + cap.01 (servono tutti e due)
# ==========================================================================
# 1) Coseno = quanto due frecce puntano nella stessa direzione. 1 = stesso
#    verso, 0 = indipendenti (o guardia: una delle due è tutta zeri).
# 2) TF-IDF = scheda pesata. Niente parole in comune → coseno 0, anche se
#    le due frasi dicono la stessa cosa con sinonimi.
# 3) `costruisci_mappa` = fit (impari lo spazio). `vettore_frase` = transform
#    (leggi lo spazio già fatto). Il contratto annota `mappa_dim`: 4 e 8
#    non si mischiano.
# 4) La media dei punti-parola perde l'ordine (#62). Resta vero anche qui:
#    `encode()` di una frase INTERA invece tiene conto del contesto interno
#    — è il salto di questo capitolo, non lo diamo per magia.


# ==========================================================================
# 🔁 RINFORZO MIRATO — Pattern #6 (E5 02a, esame 7/10: tre job, due coperti)
# ==========================================================================
# In E5 ti ho chiesto: cosa guadagni, cosa NON guadagni, quando vince il
# full-text. Hai coperto guadagno e full-text. Manca il "non guadagni"
# (cifre, IBAN, negazione, spiegabilità).
#
# Antidoto, prima di scrivere: tre righe vuote numerate, poi le riempi.
#
# 🧩 Micro #6 — Senza codice. Tre righe:
#     1) Guadagno embedding vs TF-IDF
#     2) Cosa NON ti dà l'embedding
#     3) Un caso in cui il full-text vince
# TUA RISPOSTA:
#


# ==========================================================================
# 🔁 RINFORZO MIRATO — direzione senza nome (T5 02a tolto: noioso)
# ==========================================================================
# In 02a le 4 dimensioni della SVD non si chiamano "stipendio" o "IRPEF".
# MiniLM ne ha 384: stesso discorso. All'operatore puoi dire «questo
# documento punta vicino alla query». Non puoi dire «ha deciso la parola X»
# come facevi con `parole_decisive`.
#
# 🧩 Mini 0.1 — Una riga all'operatore quando la ricerca restituisce una nota,
#     e una riga su cosa NON prometti.
# TUA RISPOSTA:
#


# ==========================================================================
# SEZIONE 1 — Primo encode()
# ==========================================================================
# `SentenceTransformer` è una classe: carichi un nome di modello, poi
# `.encode(testo)` restituisce un array. La prima volta scarica i pesi.
# Le altre volte legge la cache sul disco (come `node_modules` già pieno).

def carica_modello_frasi(nome: str = MODELLO_ST):
    """Carica il modello. Import dentro la funzione: l'import del capitolo
    non deve scaricare 400 MB se stai solo leggendo i quiz.
    """
    from sentence_transformers import SentenceTransformer
    return SentenceTransformer(nome)


def embedda(testi, modello) -> np.ndarray:
    """Una frase → una riga di 384 numeri. Lista di frasi → matrice."""
    if isinstance(testi, str):
        testi = [testi]
    vettori = modello.encode(testi, convert_to_numpy=True, show_progress_bar=False)
    return np.asarray(vettori)


# 🧩 Mini 1.1 — Due print, dopo aver caricato il modello una volta:
#     shape di embedda("cedolino di marzo", modello) e tempo del SECONDO
#     encode della stessa frase (non il primo: quello include il download).
# TUO CODICE:


# ==========================================================================
# SEZIONE 2 — Shape fissa
# ==========================================================================
# 🔁 RIPASSO PROPOSITIVO — scheda TF-IDF del cap.01
# La scheda ha tante caselle quante parole del vocabolario. Un documento
# nuovo con una parola nuova non apre una casella: OOV, si scarta.
# L'embedding di frase ha SEMPRE la stessa lunghezza, corta o lunga che sia
# la frase. 384 e basta. È il punto fisso che nel M6 finisce in pgvector.
#
# 🧩 Mini 2.1 — embedda una frase di 3 parole e una di 40. Le due shape
#     della riga (dopo encode di una frase sola: (1, dim) o (dim,)) sono
#     uguali o diverse? Una riga.
# TUA RISPOSTA:
#


# ==========================================================================
# SEZIONE 3 — Italiano: il modello giusto
# ==========================================================================
# Un MiniLM addestrato solo sull'inglese "capisce" l'italiano per analogia
# debole, o non lo capisce. Non crasha: i numeri escono comunque, il coseno
# è basso o casuale. Bug silenzioso, stessa famiglia del mean/std sbagliato
# nel contratto visivo del M3.
#
# `paraphrase-multilingual-MiniLM-L12-v2` è addestrato su più lingue.
# Sulla scheda del modello (Hugging Face) cerchi "languages" / "multilingual".
#
# 🧩 Mini 3.1 — Dove leggi, in una riga, se un modello parla italiano
#     PRIMA di scaricarlo?
# TUA RISPOSTA:
#


# ==========================================================================
# SEZIONE 4 — Stesso corpus, due motori
# ==========================================================================
# Stesse due frasi del 02a: "prospetto paga di aprile" e "cedolino di marzo".
# TF-IDF: parole diverse → coseno ~0.
# MiniLM: stesso mestiere (busta) → coseno alto.
# La mappa 02a già dava ~0.96. Qui verifichi che il modello vero fa lo stesso
# salto, senza SVD fatta in casa.

def confronto_due_frasi(modello) -> dict[str, float]:
    """Coseno TF-IDF vs coseno MiniLM sulle due parafrasi del 02a."""
    a = "prospetto paga di aprile"
    b = "cedolino di marzo"
    vec = TfidfVectorizer(tokenizer=tokenizza, token_pattern=None, lowercase=False)
    X = vec.fit_transform([a, b]).toarray()
    cos_tfidf = float(coseno(X[0], X[1]))
    E = embedda([a, b], modello)
    cos_st = float(coseno(E[0], E[1]))
    return {"tfidf": round(cos_tfidf, 3), "minilm": round(cos_st, 3)}


# 🧩 Mini 4.1 — Lancia confronto_due_frasi e scrivi i due numeri.
# TUA RISPOSTA:
#


# ==========================================================================
# SEZIONE 5 — Quando TF-IDF vince
# ==========================================================================
# Query: un codice fiscale, un IBAN, un numero di pratica. L'embedding
# "arrotonda" il senso. Il full-text (o TF-IDF sulla stringa esatta) trova
# la riga giusta. Nella torre: ricerca IBRIDA (M6) = lessicale + semantica.
#
# 🧩 Mini 5.1 — Una query (inventata, sintetica) per cui useresti il match
#     esatto e non MiniLM. Una riga.
# TUA RISPOSTA:
#


# ==========================================================================
# SEZIONE 6 — Vettori già lunghi 1: il dot È il coseno
# ==========================================================================
# Molti `encode(..., normalize_embeddings=True)` restituiscono vettori
# di norma 1. Allora coseno(a,b) = a @ b. Niente divisioni.
#
# 🧩 Mini 6.1 — Se norma(a)==1 e norma(b)==1, perché a@b basta?
#     Una riga.
# TUA RISPOSTA:
#


def demo() -> None:
    """Primo giro visibile. Non gira all'import."""
    print("Carico il modello (primo giro: download possibile)…")
    t0 = time.perf_counter()
    modello = carica_modello_frasi()
    t1 = time.perf_counter()
    print(f"  load: {t1 - t0:.1f} s")
    v = embedda("cedolino di marzo", modello)
    t2 = time.perf_counter()
    _ = embedda("cedolino di marzo", modello)
    t3 = time.perf_counter()
    print(f"  shape: {v.shape}  encode1: {t2 - t1:.3f}s  encode2: {t3 - t2:.3f}s")
    print("  confronto parafrasi:", confronto_due_frasi(modello))
    mappa = carica_mappa()
    giocattolo = vettore_frase("cedolino di marzo", mappa)
    print(f"  mappa 02a: shape {giocattolo.shape} (DIM={DIM}) — NON confrontare con i 384")


# ==========================================================================
# QUIZ DI VERIFICA
# ==========================================================================
#
# V1. Prevedi: encode di una frase. Quante dimensioni ha il vettore MiniLM
#     di questo capitolo?
# V2. Vero o falso: il primo encode è lento perché ricalcola la SVD sui 30
#     documenti.
# V3. Trova l'errore: salvo i vettori MiniLM (384) e li confronto col coseno
#     ai vettori della mappa 02a (4).
# V4. Completa: se i vettori sono normalizzati a norma 1, il coseno è ____.
# V5. Un modello inglese su note italiane: crasha o peggiora in silenzio?
# V6. Pattern #6, tre bullet: guadagno / non guadagno / quando TF-IDF.
# V7. Type hint del vettore: np.ndarray, non np.array. Vero o falso?
# V8. 💬 Spiega con parole tue (niente codice): perché encode di una FRASE
#     intera non è la media dei punti-parola del 02a.
#
# TUE RISPOSTE:
#


# ==========================================================================
# ESERCIZI
# ==========================================================================
#
# E1  🔧 [REFACTORING] — Questo pezzo funziona ma è brutto: encode in un
#     ciclo Python, un vettore alla volta. Riscrivi con un solo encode
#     sulla lista. Stessa shape in uscita (n_doc, 384).
#
#         modello = carica_modello_frasi()
#         testi = pd.read_csv(PERCORSO_DATI)["testo"].tolist()
#         righe = []
#         for t in testi:
#             righe.append(embedda(t, modello)[0])
#         M = np.stack(righe)
#
# TUO CODICE:
#
#
# E2  🔍 [DEBUG] — Lo studente ha questo traceback. Trova il bug da solo.
#     (Il mentor non usa la scala progressiva.)
#
#         v_query = embedda("cedolino", modello)[0]
#         v_mappa = vettore_frase("cedolino", carica_mappa())
#         print(coseno(v_query, v_mappa))
#
#     ValueError: Shape di a: [...] != Shape di b: [...]
#
# TUA RISPOSTA (una frase: qual è il bug, non come silenziare l'errore):
#
#
# E3  🧠 [RETRIEVAL] — A freddo, senza scorrere 02a: scrivi 4 righe che
#     caricano la mappa giocattolo e stampano il coseno di una frase con
#     se stessa. Deve essere ~1.
#
# TUO CODICE:
#
#
# E4  🔀 [INTERLEAVING] — Ripasso: TF-IDF del cap.01 + encode di ora.
#     Stessa query "accredito stipendio". Trova l'indice del documento
#     con TF-IDF massimo e quello con MiniLM massimo. Sono lo stesso
#     indice? Due numeri e una riga di commento.
#
# TUO CODICE:
#
#
# E5  🎯 [COLLOQUIO] — «Cos'è un embedding?» in 4-6 righe, tono da
#     colloquio (niente emoji). Deve entrare: vettore, vicinanza = senso
#     simile, non è un conteggio di parole. Opzionale: differenza 02a vs
#     modello preaddestrato.
#
# TUA RISPOSTA:
#


# ==========================================================================
# 🏗️ PROGETTO INCREMENTALE
# ==========================================================================
# Componente: ramo testuale della torre — primi vettori "veri" delle note.
# Deliverable: in `testo_utils.py` (o un piccolo `embed_utils.py` se preferisci
# non ingrossare il modulo): funzione `embedda_note(percorso, modello) ->
# np.ndarray` shape (n_doc, 384), salvataggio `dati/mappe/note_minilm.pkl`,
# e nel contratto `mappa_dim_minilm=384` (chiave NUOVA, non sovrascrivere
# `mappa_dim` della SVD a 4).
# DoD: `carica` i 30 vettori senza ricalcolare encode; `v.shape[1] == 384`.
# Non mischiare questi vettori con `mappa.pkl` del 02a.
#
#   [ ] T1 — encode batch delle 30 note, dump, load, assert shape.
#   [ ] T2 — una riga di commento sul contratto: perché 384 e 4 non si
#            confrontano.


# ==========================================================================
# DEFINITION OF DONE
# ==========================================================================
# [ ] Quiz ingresso e verifica (V8 Feynman compreso)
# [ ] Mini 0.1, #6, 1.1–6.1
# [ ] E1–E5
# [ ] T1–T2 progetto
# [ ] demo() gira (dopo l'installazione)


# ==========================================================================
# SOLUZIONI — dopo il tentativo
# ==========================================================================
# Q1  costruisci_mappa = fit; vettore_frase = transform.
# Q2  Falso. Forma diversa; anche a parità di n, assi SVD diversi.
# Q3  Zeri; coseno 0.0 (guardia).
# Q4  Ricostruire cambia lo spazio e costa. Load = stesso spazio.
# Q5  No.
# Q6  (a) parafrasi; (b) cifre/IBAN/negazione/nome della dimensione;
#     (c) CF o IBAN.
# Q7  np.ndarray.
#
# V2  Falso: è il download / il load dei pesi.
# V3  384 vs 4: il coseno richiede la stessa shape.
# V4  il prodotto scalare (dot / @).
# V5  Peggiora in silenzio.
# V8  encode guarda la frase intera (contesto). La media 02a somma punti
#     di parole già calcolate, commutative: l'ordine sparisce.
#
# E1  M = embedda(testi, modello)  # già accetta una lista
# E2  Stai confrontando 384 con 4. Due spazi diversi.
# T2  Commento: dim diversa ⇒ forma; modelli/SVD diversi ⇒ assi diversi.


if __name__ == "__main__":
    try:
        demo()
    except ImportError:
        print(
            "Installa prima: pip install sentence-transformers\n"
            "Poi rilancia. I quiz sopra si compilano anche senza."
        )
