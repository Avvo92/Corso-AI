# MODULO 4 — CAPITOLO 03: Misurare la distanza fra significati
# ==============================================================
#
# DA DOVE VIENI
# -------------
# Cap. 02b: hai dato una pagella al modello di embedding (MiniLM). Sai che ogni
# frase è un punto in uno spazio a 384 dimensioni, che le righe di `note_minilm.pkl`
# hanno tutte norma 1, e che `E @ q` con vettori normalizzati dà i coseni.
# Cap. 02a: hai scritto `coseno(a, b)` a mano su vettori TF-IDF.
#
# COSA IMPARI IN QUESTO CAPITOLO
# ------------------------------
# Nel 02b la ricerca era un sottoprogramma (`cerca_note` già pronta). Qui la SMONTI
# e la RICOSTRUISCI pezzo per pezzo, perché "cercare per significato" è il motore
# della torre di controllo:
#   1. I tre righelli per misurare la vicinanza: coseno, euclidea, dot product
#      (e perché con norme 1 il dot product È il coseno).
#   2. Il top-k vettorizzato: una matmul sola invece di 30 cicli.
#   3. La soglia di accettazione: quando la risposta giusta è "non lo so".
#   4. precision@k e recall@k: la pagella di una ricerca (e perché l'accuracy
#      qui non ha senso).
#   5. I falsi amici: negazioni, cifre, codici, testi corti — dove il coseno mente
#      e cosa usare invece (match esatto).
#   6. Scalabilità: da 30 note a un milione di documenti → vector DB (ponte M6).
#
# ANALOGIA GUIDA
# --------------
# Il classificatore del cap. 01 è uno scaffale: ogni pratica finisce in UN
# contenitore ("busta_paga", "cu"...). La ricerca semantica invece è un MAÎTRE
# D'HÔTEL: gli chiedi "qualcosa di simile a questo?" e lui ti porta i piatti più
# vicini, in ordine di somiglianza. Ma un maître onesto, quando niente assomiglia
# davvero a quello che chiedi, dice "non abbiamo niente del genere" invece di
# portarti il piatto meno lontano. La SOGLIA è la sua onestà.
#
# PONTE WEB
# ---------
# È la "ricerca nel catalogo" di un e-commerce: l'utente scrive "scarpe da corsa
# per principianti" e tu non cerchi le parole, cerchi i prodotti il cui *significato*
# è vicino. E sotto una certa somiglianza mostri "nessun risultato" invece di
# prodotti a caso.
#
# MAPPA DEL CAPITOLO
# ------------------
#   Quiz d'ingresso (su 02b) ................. Q1–Q8
#   Setup
#   1. Coseno, euclidea, dot: tre righelli
#   2. Top-k vettorizzato: una matmul sola
#   3. La soglia: quando rispondere "non lo so" (+ il grafico del trade-off)
#   4. precision@k e recall@k: la pagella della ricerca
#   5. Falsi amici: dove il coseno mente
#   6. Scalabilità: da 30 a un milione
#   Quiz di verifica .......................... V1–V10
#   Esercizi .................................. E1–E9
#   Progetto incrementale ..................... 🏗️ match_utils.py
#   Soluzioni (in fondo)
#
# PIPELINE DA TENERE A MEMORIA (Regola 44a)
# -----------------------------------------
#   P1  query → vettore:      q = embedda([query], modello, normalizza=True)[0]
#   P2  punteggi → risposta:  s = E @ q  →  vicini = top_k(s, k)  →  decidi_con_soglia
#   P3  pagella:              precision_su_k su un benchmark di query con risposta nota
#
# TERMINI NUOVI (li ritrovi dentro gli esercizi, Regola 44b)
# ---------------------------------------------------------
#   distanza euclidea · top-k (2ª volta) · soglia di accettazione · candidati ·
#   ranking · precision@k (2ª) · recall@k · falso positivo semantico ·
#   bi-encoder · cross-encoder · re-ranking · ANN · vector DB · match esatto
#
# REGOLA 45 — LE FUNZIONI CHE DECIDONO LE SCRIVI TU
# -------------------------------------------------
# Dopo un esempio guidato corto, scrivi da zero:
#   - `top_k(punteggi, k)`             (Sez. 2)
#   - `decidi_con_soglia(vicini, soglia)` (Sez. 3)
#   - `precision_su_k(tipi_vicini, tipo_atteso, k)` (Sez. 4)
# Pronte e riusabili (da capitoli precedenti, con ripasso): `embedda`,
# `carica_modello_frasi`, `carica_vettori` (embed_utils), `coseno` (testo_utils).
#
# PREREQUISITI: aver chiuso 02b; `dati/mappe/note_minilm.pkl` presente (30×384,
# norme 1); modello MiniLM in cache. Tutto CPU, nessuna installazione nuova.
#
# DEFINITION OF DONE
# ------------------
# [] Quiz d'ingresso corretto e registrato
# [ ] Mini-esercizi fatti (1.1 → 6.2)
# [ ] `top_k`, `decidi_con_soglia`, `precision_su_k` scritte da te e verificate
# [ ] Quiz di verifica ≥ 70% (voto primo tentativo nel diario)
# [ ] Esercizi E1–E9 fatti
# [ ] Progetto 🏗️: `match_utils.py` con assert di regressione verdi
# [ ] Voto difficoltà 1-10 comunicato


# =============================================================================
# QUIZ D'INGRESSO (sul cap. 02b — 8 domande)
# =============================================================================
# Regola: prima tentativo, senza rieseguire il 02b. Segna le risposte qui,
# correggi con le soluzioni in fondo, registra il voto nel diario.
#
# Q1 · Prevedi output:
#      q = embedda("cedolino di ottobre", modello)
#      print(q.shape)
#
# RISPOSTA:
# (1, 384)

#
# Q2 · Vero o Falso (spiega in una riga):
#      "Se le righe di E e la query q hanno tutte norma 1, allora E @ q dà
#       esattamente i coseni tra q e ogni riga di E."
#
# RISPOSTA:
# Vero
#
# Q3 · Trova l'errore:
#      for i in range(len(corpus)):                     # corpus: 30 righe, colonna 'id' da 1 a 30
#          testo = corpus[corpus['id'] == i]['testo']   # voglio la riga in posizione i
#
# RISPOSTA:
# id e indice non sono allineati (il primo parte da 1 e il secondo da 0). Per allinearli, basta fare i + 1. 

# Q4 · Definizione con parole tue: che differenza c'è tra TOKEN e SOTTOPAROLA?
# il token è l'unita' semantica che il modello calcola. La sotto parola è qualsiasi frammento di una parola, ma non necessariamente un token.

# RISPOSTA:
#
# Q5 · Completa il codice — normalizza q a mano (senza sklearn):
#      q = embedda(["cedolino"], modello)[0]
#      q_normalizzata = q / ______________________
#
# RISPOSTA:
# q_normalizzata = q / np.linalg.norm(q)
#
# Q6 · Prevedi output: una ricerca restituisce 3 vicini; 2 sono del tipo giusto.
#      Quanto vale precision@3? (scrivi anche la frazione)
#
# RISPOSTA:
# 2/3 -> 0.66 periodico
#
# Q7 · Vero o Falso (spiega in una riga):
#      "Due modelli di embedding diversi che producono entrambi vettori di 384
#       numeri generano punti che posso confrontare tra loro nello stesso spazio."
#
# RISPOSTA:
# Falso. Anche se il numero di coordinate per vettore è identico, quei numeri che lo compongono descrivono spazi diversi.
#
# Q8 · Trova l'errore:
#      q = embedda(["prospetto paga"], modello)[0]   # normalizza NON passato
#      punteggi = E @ q                              # E ha righe a norma 1
#      print(punteggi.max())                         # ci aspettiamo un coseno ≤ 1
#      Perché il massimo può venire maggiore di 1?
#
# RISPOSTA:
# perchè q non è stato normalizzato, e quindi il risultato prodotto dal dot product non è il coseno


# =============================================================================
# SETUP — carica mappa e testi (riuso dal 02b)
# =============================================================================

import os                                                      # percorsi file
import joblib                                                  # per leggere il contratto (Mini 2.4; salvato con joblib.dump)
import numpy as np                                             # vettori e matrici
import pandas as pd                                            # tabella delle note

from numpy.typing import NDArray                               # type hint vettori (come nel 02b)

from embed_utils import PERCORSO_VETTORI, carica_modello_frasi, embedda, carica_vettori  # utilities del 02b

# 🔁 RIPASSO PROPOSITIVO — `coseno(a, b)` (cap. 02a/02b, testo_utils)
# ------------------------------------------------------------------
# L'hai scritta tu due volte: dot(a,b) diviso il prodotto delle norme, con la
# guardia che restituisce 0.0 se una norma è zero. Vale per vettori 1D.
# In questo capitolo la usiamo come RIFERIMENTO per verificare che la versione
# veloce (matmul su vettori normalizzati) dia gli stessi numeri.
from testo_utils import coseno                                  # la tua funzione del 02a/02b

BASE_DIR = os.path.dirname(os.path.abspath(__file__))          # cartella di questo file
PERCORSO_CSV = os.path.join(BASE_DIR, "dati", "note_documenti.csv")        # i 30 testi
PERCORSO_CONTRATTO = os.path.join(BASE_DIR, "dati", "contratti", "contratto.pkl")  # etichetta mappa

note = pd.read_csv(PERCORSO_CSV)                               # tabella: colonne id, tipo, testo
testi = note["testo"].tolist()                                 # i testi come lista (stesso ordine di E)
E = carica_vettori()                                           # mappa salvata nel 02b: shape (30, 384)

print("note:", note.shape, "| E:", E.shape)                    # atteso: (30, 3) | (30, 384)
print("norme righe E: min", np.linalg.norm(E, axis=1).min(),   # atteso: 1.0
      "max", np.linalg.norm(E, axis=1).max())                  # atteso: 1.0

# Il modello serve SOLO per codificare query nuove (i documenti sono già in E).
# Caricalo quando arrivi alla Sez. 2 (prima query): è in cache, ~10 s.
modello = carica_modello_frasi()                               # MiniLM dalla cache del 02b


# =============================================================================
# SEZIONE 1 — Coseno, euclidea, dot product: tre righelli
# =============================================================================
#
# 🔁 RIPASSO PROPOSITIVO — coseno (Ponte Matematico + 02a + 02b)
# --------------------------------------------------------------
# Il coseno misura QUANTO DUE FRECCE PUNTANO NELLA STESSA DIREZIONE, ignorando
# quanto sono lunghe: 1 = stessa direzione, 0 = perpendicolari, -1 = opposte.
# Nel 02a lo calcolavi su vettori TF-IDF lunghi 4; nel 02b su frecce a 384
# dimensioni. La formula è la stessa, cambia solo la lunghezza delle frecce.
#
# 1.1 · TRE MODI DI DIRE "QUANTO SONO VICINI"
# -------------------------------------------
# Immagina due punti su una mappa (due frasi nello spazio):
#
#   • DISTANZA EUCLIDEA — "quanti metri a piedi": la lunghezza del segmento che
#     li unisce. Piccola = vicini. Occhio: conta anche la LUNGHEZZA delle frecce,
#     non solo la direzione. Due frasi uguali ma una "più intensa" (freccia più
#     lunga) risultano distanti anche se puntano uguale.
#       dist = np.linalg.norm(a - b)
#
#   • SIMILARITÀ COSENO — "quanto puntano nella stessa direzione": ignora la
#     lunghezza, guarda solo l'angolo. È il righello giusto per i SIGNIFICATI:
#     una frase corta e una lunga sullo stesso tema devono risultare vicine.
#       coseno(a, b) = dot(a, b) / (norma(a) * norma(b))
#
#   • DOT PRODUCT (prodotto scalare) — la versione "grezza": dot(a, b) = Σ aᵢ·bᵢ.
#     Da solo mescola direzione E lunghezza. MA se entrambe le frecce sono lunghe
#     1 (normalizzate), il denominatore del coseno vale 1 e sparisce:
#       norme 1  →  coseno(a, b) = dot(a, b)
#     È la scorciatoia che hai già verificato nel 02b con `E @ q`.
#
# Perché ci interessa così tanto la scorciatoia? Perché il dot product su righe
# di una matrice è UNA MATMUL: NumPy la fa in un colpo solo, in C, su tutti i
# core della CPU. Il coseno "con la formula intera" invece lo scriveresti con
# un ciclo. Stessi numeri, altra velocità.
#
# 1.2 · VERIFICA NUMERICA (piccola, a mano)
# -----------------------------------------
a_demo = np.array([0.6, 0.8])          # freccia corta 2D, norma: √(0.36+0.64) = 1
b_demo = np.array([0.8, 0.6])          # anche questa ha norma 1

dot_demo = float(np.dot(a_demo, b_demo))       # 0.6*0.8 + 0.8*0.6 = 0.96
cos_demo = coseno(a_demo, b_demo)              # la tua funzione: dot / (1*1) = 0.96
euclidea_demo = float(np.linalg.norm(a_demo - b_demo))  # √((−0.2)²+(0.2)²) ≈ 0.283

print("dot:", dot_demo, "| coseno:", cos_demo, "| euclidea:", round(euclidea_demo, 3))
# Atteso: dot e coseno identici (0.96) perché le norme sono 1.

# E ora sul corpus vero: prima riga di E contro la query "cedolino".
q_demo = embedda(["cedolino di ottobre"], modello, normalizza=True)[0]   # (384,) norma 1
s_demo = E @ q_demo                                                     # (30,) tutti i coseni
riga0 = E[0]                                                            # prima nota
print("E @ q [0]:", s_demo[0], "| coseno():", coseno(riga0, q_demo))    # devono coincidere

assert abs(s_demo[0] - coseno(riga0, q_demo)) < 1e-6                    # stessa cosa, due strade

# 1.3 · E ALLORA L'EUCLIDEA? Su vettori a norma 1 danno la STESSA classifica
# ---------------------------------------------------------------------------
# Domanda legittima: "se le frecce sono tutte lunghe 1, non posso misurare
# semplicemente i metri (euclidea)?" Sì — e c'è un legame esatto: con norme 1
#
#   distanza² = 2 − 2 · coseno
#
# cioè la distanza euclidea cresce esattamente quando il coseno scende: chi è
# più vicino per l'una è più simile per l'altro. Le CLASSIFICHE coincidono
# sempre. Verifica numerica:
a_check, b_check = E[3], E[7]                                  # due note a caso
dist2_check = float(np.sum((a_check - b_check) ** 2))          # distanza al quadrato
cos_check = float(a_check @ b_check)                           # coseno (norme 1: dot)
print("dist^2:", round(dist2_check, 6), "| 2 - 2*cos:", round(2 - 2 * cos_check, 6))
# Atteso: due numeri identici (1.604118, misurato il 19/10/2026).
#
# Allora perché il coseno e non l'euclidea? Per LEGGIBILTÀ: il coseno vive in
# [−1, 1] e ha un'interpretazione diretta ("quanta direzione condividono"), la
# distanza no. Ma sotto il cofano, chi ordina per euclidea su vettori
# normalizzati sta facendo la tua stessa identica ricerca.

# -----------------------------------------------------------------------------
# MINI-ESERCIZIO 1.1 — la matrice delle somiglianze
# -----------------------------------------------------------------------------
# `E @ E.T` dà S: S[i, j] = coseno tra la nota i e la nota j (tutte le coppie
# in una matmul sola).
#
# TODO 1: calcola S = E @ E.T e stampa S.shape.
# TODO 2: stampa S.diagonal() — che valori ti aspetti e perché?
# TODO 3: stampa S[0, 1] e S[1, 0]: devono essere uguali (il coseno è simmetrico).
# TODO 4 (chiudi il cerchio dei tre righelli): calcola s0 = E @ E[0] e
#         d0 = np.linalg.norm(E - E[0], axis=1); poi confronta np.argsort(-s0)
#         e np.argsort(d0) con (... == ...).all(). Cosa scopri?
#

print("\nMini-esercizio 1.1\n")

E = carica_vettori()
S = E @ E.T
assert np.allclose(S.diagonal(), 1), "Ops, qualcosa è andato storto con la diagonale!"
assert S.shape == (30, 30), "Ops, la shape non corrisponde a quella attesa!"
assert np.isclose(S[0, 1], S[1, 0]), "Ops, i coseni posti simmetricamente sulla tabella non coincidono!"
print(S.shape)
print(S.diagonal(), "\n")

s0 = np.argsort(-(E @ E[0]))
d0 = np.argsort(np.linalg.norm(E - E[0], axis=1))
for s, d in zip(s0, d0):
    print(f"s0: {s} -> d0: {d}")

# RISPOSTE:
# TODO 2 (a parole):
# mi aspetto che sulla diagonale, ossia dove ci sono i coseni di un vettore con se stesso, ci siano tutti 1.
# TODO 4 (a parole):
# Che la classifica restituita dai coseni e distanze eucliedee è di fatto identica.
# 
#

# -----------------------------------------------------------------------------
# 🔁 RINFORZO MIRATO — lacuna #66 (quiz ingresso 02b, lasciata in bianco)
# -----------------------------------------------------------------------------
# Nel 02b hai lasciato vuota la domanda su `embedda("una sola frase")`.
# Il punto: `embedda` restituisce SEMPRE UNA MATRICE (2D), una riga per testo,
# anche quando i testi sono UNO. È un CONTRATTO: chi la chiama sa già che forma
# arriva, senza if. "testo singolo" e "lista di un elemento" danno la STESSA
# forma: (1, 384).
#
#   embedda("ciao", modello).shape        → (1, 384)
#   embedda(["ciao"], modello).shape      → (1, 384)
#   embedda(["a", "b"], modello).shape    → (2, 384)
#
# Perché ci teniamo la matrice anche per UNA frase? Perché `E @ q` vuole forme
# chiare: E è (30, 384), q deve diventare (384,) con UN `[0]` esplicito — così
# il risultato è (30,), uno score per nota. Se la forma restasse ambigua, gli
# errori di broadcasting di NumPy sarebbero silenziosi e perfidi.
#
# MINI-ESERCIZIO 1.2 (rinforzo #66)
# ---------------------------------
# TODO 1: senza eseguire, prevedi le shape di:
#   embedda("prospetto paga", modello)
#   embedda(["prospetto paga"], modello)
#   embedda(["a", "b", "c"], modello)
# Poi eseguile e verifica.
# TODO 2: completa la frase — "Per passare dalla matrice (1, 384) alla singola
#         freccia (384,) scrivo ______________________"
#
# RISPOSTE TODO 1:
# (1, 384), (1, 384), (3, 384)
# RISPOSTA TODO 2:
# q[0]



# =============================================================================
# SEZIONE 2 — Top-k vettorizzato: una matmul sola
# =============================================================================
#
# 🔁 RIPASSO PROPOSITIVO — `cerca_note` e la pagella (cap. 02b)
# -------------------------------------------------------------
# Nel 02b la ricerca era `cerca_note(query, E, testi, modello, k)` dentro
# embed_utils: normalizzava la query, faceva `E @ q`, ordinava con argsort e
# restituiva gli indici dei k vicini. La pagella (Mini 5.1) chiamava coseno()
# su ogni riga con un ciclo — giusto ma lento. Qui rifai la stessa cosa in
# forma vettorizzata e la funzione chiave la scrivi TU.
#
# 2.1 · ESEMPIO GUIDATO (guarda, poi toccherà a te)
# -------------------------------------------------
query_guida = "stipendio e trattenute del mese"                       # frase con un po' di contesto
q_guida = embedda([query_guida], modello, normalizza=True)[0]         # (384,) norma 1 — vedi rinforzo 1.2
punteggi_guida = E @ q_guida                                          # (30,) un coseno per nota

# np.argsort restituisce gli INDICI che ordinerebbero l'array, dal più piccolo.
# Con il segno meno (-punteggi) l'ordine si rovescia: dal coseno PIÙ ALTO.
ordine_guida = np.argsort(-punteggi_guida)                            # indici, dal migliore al peggiore
primi3_guida = ordine_guida[:3]                                       # i primi 3 indici

for i in primi3_guida:                                                # stampa i 3 vicini
    print(round(float(punteggi_guida[i]), 3), note.loc[i, "tipo"], note.loc[i, "testo"][:50])
# Misurato il 19/10/2026 (±0.01 tra versioni):
#   0.701 busta_paga · 0.677 cu · 0.644 cu
# Nota bene: il 1° è una busta paga (ci sta), ma 2° e 3° sono CU — il tema
# "soldi del lavoro" accomuna tipi amministrativi diversi. Tienilo a mente:
# è esattamente il problema della Sez. 3 (soglia) e della Sez. 5 (falsi amici).
# Curiosità onesta: con la query cortissima "cedolino di ottobre" il 1° vicino
# NON è una busta paga e i punteggi crollano sotto 0.5 — Sez. 5.3 spiega perché.
#
# Osserva i TRE passi: matmul → argsort col meno → slice [:k].
# Tutta la ricerca semantica è qui dentro. Il resto è contorno.
#
# 🌉 PONTE JS/PHP (dove esiste un equivalente, il confronto è obbligatorio)
# In JavaScript, per tenere insieme indici e valori ordineresti le COPPIE:
#   punteggi.map((v, i) => [i, v]).sort((a, b) => b[1] - a[1]).slice(0, k)
# In PHP: usort($coppie, fn($a, $b) => $b[1] <=> $a[1]); poi array_slice(..., 0, $k).
# np.argsort(-punteggi)[:k] è la stessa idea, ma ti restituisce DIRETTAMENTE
# gli indici ordinati — e il lavoro sporco lo fa il C, non l'interprete.
#
# 2.2 · ORA LA SCRIVI TU — `top_k(punteggi, k)`  [REGOLA 45]
# ----------------------------------------------------------
# Consegna: una funzione che prende l'array dei punteggi (un coseno per nota)
# e k, e restituisce una LISTA DI COPPIE (indice, punteggio) dei k migliori,
# ordinata dal punteggio più alto.
#
#   def top_k(punteggi: NDArray[np.float64], k: int) -> list[tuple[int, float]]:
#
# Esempio: top_k(np.array([0.5, 0.9, 0.7]), 2) → [(1, 0.9), (2, 0.7)]
#
# Vincoli: niente cicli per ordinare (usa np.argsort); k può essere maggiore
# del numero di righe? (gestiscilo o documenta perché non serve).
#
# SCRIVILA QUI SOTTO:
#
def top_k(punteggi: NDArray[np.float64], k: int) -> list[tuple[int, float]]:
    if k > len(punteggi):
        raise ValueError(f"K non può essere maggiore della lunghezza di punteggi ({len(punteggi)})")
    idx_sorted = np.argsort(-punteggi)[:k]
    return [(int(idx), float(punteggi[idx])) for idx in idx_sorted]


# MINI-ESERCIZIO 2.1 — verifica la tua top_k
# ------------------------------------------
# TODO 1: top_k(np.array([0.5, 0.9, 0.7, 0.1]), 2) deve dare [(1, 0.9), (2, 0.7)]
# TODO 2: top_k(punteggi_guida, 3) deve dare gli stessi indici di primi3_guida
# TODO 3: scrivi un assert che controlla che i punteggi restituiti siano in
#         ordine decrescente.

print("\nMini-esercizio 2.1\n")

# TODO 1
todo_1 = top_k(np.array([0.5, 0.9, 0.7, 0.1]), 2)
assert np.allclose(todo_1, [(1, 0.9), (2, 0.7)]), "Ops, il todo 1 non è andata a buon fine!"
print(todo_1, "\n")

#TODO 2
todo_2 = np.array([i for i, v in top_k(punteggi_guida, 3)])
assert np.allclose(todo_2, primi3_guida), "Ops, il todo 2 non è andata a buon fine!"
print(todo_2, primi3_guida)

#TODO 3
for j, (i, v) in enumerate(todo_1):
    if j != len(todo_1) - 1:
        assert todo_1[j][1] >= todo_1[j + 1][1], "Ops, i valori non sono in ordine decrescente!"


# MINI-ESERCIZIO 2.2 — la query del prospetto
# --------------------------------------------
# TODO: embedda la query "prospetto paga di aprile" (normalizzata), calcola
# punteggi = E @ q, poi usa la TUA top_k(punteggi, 3) e stampa indice, tipo,
# punteggio dei 3 vicini.
#
# Valori misurati il 19/10/2026 (possono variare di ±0.01 tra versioni):
#   1° → indice 1, busta_paga, ≈0.612
#   2° → indice 24, altro (ricevuta bonifico), ≈0.582
#   3° → indice 5, busta_paga, ≈0.570
#
# Domanda (rispondi in una riga): il 2° vicino NON è una busta paga. Guardando
# i punteggi, diresti che è "sbagliato di brutto" o "un vicino onesto"?
#
# RISPOSTA:
# dal punteggio direi che è un vicino onesto

print("\nMini-esercizio 2.2\n")

q = embedda("prospetto paga di aprile", modello, True)[0]
E = carica_vettori()
S = E @ q
tk = top_k(S, 3)
tipi = pd.read_csv(PERCORSO_CSV)['tipo'].tolist()
risultati = [
    {
    "indice": i,
    "tipo": tipi[i],
    "punteggio": round(float(S[i]), 4)
    } for i in [i for i, v in tk]]
import pprint
for r in risultati:
    pprint.pprint(r)

#
# -----------------------------------------------------------------------------
# 🔁 RINFORZO MIRATO — lacuna #68 (E7 del 02b, lasciata in bianco)
# -----------------------------------------------------------------------------
# In E7 dovevi scrivere perché questo ciclo è sbagliato:
#
#   for i in range(len(corpus)):
#       riga = corpus[corpus['id'] == i]
#
# Il punto: in un DataFrame ci sono DUE numeri diversi che sembrano uguali.
#   • POSIZIONE di riga: 0, 1, 2, ... (la "sedia" nella stanza) → si usa con .iloc[i]
#   • valore della COLONNA id: 1, 2, 3, ... (il "nome sulla sedia") → si usa con
#     note[note['id'] == x] oppure .loc
# Nel nostro CSV gli id partono da 1 e le posizioni da 0: `id == 0` non esiste
# (riga vuota!) e `id == 29` NON è l'ultima riga.
#
# La TUA top_k restituisce POSIZIONI (indici dell'array dei punteggi): per
# stampare testo e tipo usi quindi note.loc[i, ...] finché l'indice del
# DataFrame coincide con la posizione (qui sì, è un RangeIndex 0..29).
#
# MINI-ESERCIZIO 2.3 (rinforzo #68)
# ----------------------------------
# TODO 1: stampa note.iloc[0]['id'] e note.iloc[0]['testo'][:40] — che id ha la
#         PRIMA riga? (non 0!)
# TODO 2: prova note[note['id'] == 0] — cosa restituisce? (un DataFrame VUOTO:
#         è questo il bug silenzioso di E7)
# TODO 3: completa la frase — "Gli indici che escono da np.argsort sono
#         ____________ (posizioni/valori id), quindi per leggere la riga uso
#         ____________"
#
# RISPOSTA TODO 3:
# Risposta todo 1 -> L'id è 1
# Risposta todo 2 -> Empty Dataframe
# Risposta todo 3 -> posizioni, .iloc

print("\nMini-esercizio 2.3\n")

# TODO 1
note = pd.read_csv(PERCORSO_CSV)
print(note.iloc[0]['id'])
print(note.iloc[0]['testo'][:40], "\n")

# TODO 2
print(note[note['id'] == 0])


# -----------------------------------------------------------------------------
# 🔁 RINFORZO MIRATO — Mini 11.1 del 02b (lasciata in bianco): il contratto
# -----------------------------------------------------------------------------
# Nel 02b hai creato `dati/contratti/contratto.pkl` con aggiorna_contratto_minilm:
# è l'ETICHETTA della mappa — chi l'ha prodotta, con quale modello, con che forma.
# La domanda chiave era: "basta confrontare le dimensioni per sapere se due mappe
# sono compatibili?" Risposta: NO. Due modelli diversi possono sputare entrambi
# 384 numeri, ma sono 384 COORDINATE DI DUE SPAZI DIVERSI: la stessa frase ha
# punti diversi, e un coseno tra spazi diversi è un numero senza senso.
# Come due altezze: 170 cm e 170 pollici — stesso numero? No: stessa GRANDEZZA
# numerica, unità diverse. La chiave `modello_minilm` nel contratto è l'unità
# di misura dello spazio.
#
# MINI-ESERCIZIO 2.4 (rinforzo Mini 11.1)
# ----------------------------------------
# TODO 1: apri PERCORSO_CONTRATTO con joblib.load (NON pickle: il file è stato
#         salvato con joblib.dump in testo_utils/embed_utils) e stampa le chiavi
#         del dizionario. Quale chiave ti dice CHI ha prodotto E?
# TODO 2: stampa il valore della forma ("shape" o simile) e confrontalo con
#         E.shape: coincidono?
# TODO 3: in una riga — perché `shape` da sola non basta a garantire che una
#         query codificata OGGI sia confrontabile con E?
#
# RISPOSTE:
# Risposta todo 1 -> modello_minilm
# Risposta todo 3 -> Da sola non basta perchè due vettori di shape identica (es. 384 dimensioni), possono cmq descrivere spazi diversi. La vera chiave è di lettura corretta è il modello, che deve essere lo stesso di quello che ha fatto l'encode dei vettori che abbiamo salvati.

print("\nMini-esercizio 2.4\n")

contratto = joblib.load(PERCORSO_CONTRATTO)
print(contratto.keys(), "\n")
forma_contratto = contratto['mappa_dim_minilm']
forma_vettori = E[0].shape[0]
assert forma_contratto == forma_vettori, "Ops le dimensioni del vettore E e della dimensione riportata nel contratto non coincidono!"
print(f"Dimensioni contratto: {forma_contratto} -> Dimensione vettori salvati: {forma_vettori}\n")

# =============================================================================
# SEZIONE 3 — La soglia: quando la risposta giusta è "non lo so"
# =============================================================================
#
# 🔁 RIPASSO PROPOSITIVO — soglia e semaforo (M2 cap. 04)
# -------------------------------------------------------
# In M2 il classificatore dava una probabilità 0–1 e TU decidevi il punto di
# taglio: sopra la soglia = "positivo", sotto = "negativo". Alzare la soglia
# riduce i falsi allarmi ma lascia fuori casi veri; abbassarla fa il contrario.
# È lo stesso identico trade-off, solo che qui il numero è un COSENO e il
# "positivo" è "questo vicino è davvero pertinente".
#
# 3.1 · I NUMERI VERI DEL NOSTRO CORPUS (misurati il 19/10/2026)
# --------------------------------------------------------------
# Per ognuna delle 30 note ho preso il vicino PIÙ simile (se stessa esclusa)
# e ho guardato se è dello stesso tipo:
#
#   vicino1 del tipo giusto:  24 su 30  →  precision@1 = 0.80
#   vicino1 sbagliati (6):    indici 2, 13, 17, 18, 20, 26
#   loro punteggi:            0.74, 0.807, 0.75, 0.475, 0.627, 0.723
#   vicino1 giusti:           min 0.404 (nota 28, "atto di notorietà"), mediana ≈ 0.80
#
# Guarda bene la tabella mentale: gli errori NON stanno tutti sotto i giusti.
#   • Nota 13 (estratto_conto): il suo vicino è una busta_paga a 0.807 — un
#     punteggio ALTO, più alto di molti vicini giusti! È un FALSO POSITIVO
#     SEMANTICO: due documenti che parlano davvero di soldi, stipendi, importi.
#     Il coseno vede la somiglianza di tema, non il tipo amministrativo.
#   • Nota 28 (atto di notorietà): il suo vicino migliore è a 0.404 — giustamente
#     lontano: nel corpus non c'è niente di simile. Il motore dovrebbe dire
#     "non lo so", e infatti il punteggio basso lo grida.
#
# 3.2 · COSA FA UNA SOGLIA A 0.70 (conto già fatto — lo riverificherai tu)
# -------------------------------------------------------------------------
#   • Errori bloccati: 2 su 6 (nota 18 a 0.475, nota 20 a 0.627)
#   • Errori che passano comunque: 4 su 6 (2 a 0.74, 13 a 0.807, 17 a 0.75, 26 a 0.723)
#   • Risposte GIUSTE buttate via: diverse — la nota 28 a 0.404 e altre sotto
#     0.70 (nota 3 a ≈0.65, nota 5 a ≈0.64, nota 14 a ≈0.69, nota 27 a ≈0.67...)
#
# Morale: la soglia non è una bacchetta magica. È una MANOPOLA che sposti tra
# due mali: rispondere male (falso positivo) o non rispondere (falso "non lo so").
# Dove metterla dipende dal COSTO dei due errori nel TUO prodotto: in una torre
# di controllo che archivia pratiche, un'archiviazione sbagliata costa più di un
# "da rivedere a mano". Nel dubbio: meglio "non lo so".
#
# 3.3 · ESEMPIO GUIDATO (una riga sola, poi tocca a te)
# -----------------------------------------------------
# Un vicino è (indice, punteggio). La decisione è un filtro:
vicino_esempio = (4, 0.81)                                  # (indice, coseno)
sopra_soglia_esempio = vicino_esempio[1] >= 0.70            # True: questo passa
print("passa?", sopra_soglia_esempio)                       # True
#
# 3.4 · ORA LA SCRIVI TU — `decidi_con_soglia(vicini, soglia)`  [REGOLA 45]
# --------------------------------------------------------------------------
# Consegna: prende la lista di coppie (indice, punteggio) che esce dalla tua
# top_k e una soglia; restituisce SOLO i vicini con punteggio >= soglia,
# nello stesso formato. Se nessuno passa, restituisce lista VUOTA (= "non lo so").
#
#   def decidi_con_soglia(vicini: list[tuple[int, float]],
#                         soglia: float) -> list[tuple[int, float]]:
#
# SCRIVILA QUI SOTTO:
#

def decidi_con_soglia(vicini: list[tuple[int, float]], soglia: float = 0.7) -> list[tuple[int, float]]:
    return [(i, v) for i, v in vicini if v > soglia]
#
#
# MINI-ESERCIZIO 3.1 — verifica la tua decidi_con_soglia
# ------------------------------------------------------

print("\nMini-esercizio 3.1\n")

# TODO 1: decidi_con_soglia([(1, 0.9), (2, 0.69), (3, 0.4)], 0.70) → [(1, 0.9)]
arr_todo_1 = [(1, 0.9), (2, 0.69), (3, 0.4)]
result_1 = decidi_con_soglia(arr_todo_1, 0.7)
controprova_1 = [(1, 0.9)]

assert result_1 == controprova_1, "Ops, qualcosa non funziona con il todo 1!!"
print(result_1, "\n")

# TODO 2: decidi_con_soglia([(1, 0.5)], 0.70) → []  (il "non lo so")
arr_todo_2 = [(1, 0.5)]
result_2 = decidi_con_soglia(arr_todo_2, 0.7)
controprova_2 = []

assert result_2 == controprova_2, "Ops, qualcosa è andato storto con il todo 2!"
print(result_2, "\n")

# TODO 3: la soglia è inclusa? 0.70 con soglia 0.70 passa? (decidi e documenta
#         la scelta in una riga: >= oppure >)
# dalla prova fatta non cambia nulla nel risultato se usiamo < o <=. La funzione permette di variarlo


# def valuta_query(benchmark: tuple[str, str], i: int, tipi: list[str], modello, E, soglia: float, k: int = 1):
#     q = embedda(benchmark[0], modello, normalizza=True)[0]
#     punteggi = E @ q
#     punteggi[i] = -np.inf
#     first = decidi_con_soglia(top_k(punteggi, k), soglia)
#     first_tipo = [tipi[j] for j, _ in first]
#     return ([v == benchmark[1] for v in first_tipo], first_tipo)

# note = pd.read_csv(PERCORSO_CSV)
# Q = note['testo'].tolist()
# T = note['tipo'].tolist()

# benchmarks = []
# for q, t in zip(Q, T):
#     benchmarks.append((q, t))

# results = []
# tipi_pred = []
# for i, t in enumerate(benchmarks):
#     a, b = valuta_query(t, i, T, modello, E, 0.7, 1)
#     results.append(a)
#     tipi_pred.append(b)    
    
# new_results = []
# for r in results:
#     ok = len(r) > 0 and r[0] is True
#     new_results.append(ok)

# giusti = [(t, b) for t, b in zip(T, new_results)]
# buste_paga = [(t, b) for t, b in giusti if t == "busta_paga"]

# tp_bp = sum(1 for _, ok in buste_paga if ok)
# fn_bp = sum(1 for _, ok in buste_paga if not ok)
# fp_bp = sum(1 for pred, vero in zip (tipi_pred, T) if len(pred) > 0 and pred[0] != vero and pred[0] == "busta_paga")

# precision_bp = tp_bp / (tp_bp + fp_bp)
# recall_bp = tp_bp / (tp_bp + fn_bp)

# print(recall_bp, "\n")
# print(precision_bp, "\n")

#
# 🌉 PONTE JS/PHP: il corpo della tua funzione è una FILTER con destrutturazione:
#   vicini.filter(([i, p]) => p >= soglia)                  // JavaScript
#   array_filter($vicini, fn($v) => $v[1] >= $soglia)       // PHP
# La list comprehension con `if` di Python è la stessa idea in una riga.
#
# MINI-ESERCIZIO 3.2 — la soglia sul corpus vero
# ----------------------------------------------
# TODO 1: per OGNI nota (indice i): q = E[i] (è già norma 1!), punteggi = E @ q,
#         ma ATTENZIONE: il vicino 1 di ogni nota è SE STESSA (coseno 1.0) —
#         escludila prendendo top_k(punteggi, 2) e tenendo il SECONDO.
# TODO 2: con la tua decidi_con_soglia a 0.70 conta:
#           a) quanti vicini1 SBAGLIATI vengono bloccati (atteso: 2 su 6)
#           b) quanti vicini1 GIUSTI vengono buttati via (atteso: 7 su 24 —
#              contali e verifica: sono i giusti con punteggio < 0.70)
# TODO 3: prova soglia 0.85: cosa succede ai due conteggi? (una riga a parole —
#          poi lo VEDI nel grafico del Mini 3.5)
#
# RISPOSTE:

print("\nMini-esercizio 3.2\n")

def f(soglia: float, magg_uguale: bool = False):
    vicini_sempre = []
    note = pd.read_csv(PERCORSO_CSV)
    testi = note['testo'].tolist()
    Q = embedda(testi, modello, normalizza=True)
    for i, q in enumerate(Q):
        punteggi = E @ q
        punteggi[i] = -np.inf
        vicino_sempre = decidi_con_soglia(top_k(punteggi, 1), 0.0)
        vicino_sempre = vicino_sempre[0]
        vicini_sempre.append((i, vicino_sempre))
    
    tipi = note['tipo'].tolist()

    matches = []
    scores = []

    for v in vicini_sempre:
        match = tipi[v[0]] == tipi[v[1][0]]
        score = v[1][1]
        matches.append(match)
        scores.append(score)
    errori = sum(1 for m in matches if (not m))
    giusti = sum(1 for m in matches if m)
    if magg_uguale:
        errori_bloccati = sum(1 for m, s in zip(matches, scores) if (not m) and s <= soglia)
        giusti_persi    = sum(1 for m, s in zip(matches, scores) if m and s <= soglia)
        return errori_bloccati, giusti_persi, errori, giusti       
    errori_bloccati = sum(1 for m, s in zip(matches, scores) if (not m) and s < soglia)
    giusti_persi    = sum(1 for m, s in zip(matches, scores) if m and s < soglia)
    return errori_bloccati, giusti_persi, errori, giusti


# for y in np.linspace(0.70, 0.85, 16):
#     a, b, c, d = f(y)
#     print(f"Soglia: {y}")
#     print(f"Errori Totali: {c}, Errori bloccati: {a}")
#     print(f"Giusti persi: {b}, Giusti Totali: {d}\n")

# -----------------------------------------------------------------------------
# 🔁 RINFORZO MIRATO — E8 del 02b (lasciata in bianco): due segnali che
# discordano
# -----------------------------------------------------------------------------
# La domanda era: "la probabilità del classificatore è bassa ma il coseno con
# un documento noto è alto (o viceversa): come mostri entrambe le informazioni
# all'operatore?"
# Il punto: i due strumenti misurano cose DIVERSE.
#   • Il classificatore dice: "questo testo assomiglia alla CATEGORIA busta_paga"
#     (decide tra scaffali fissi).
#   • Il coseno dice: "questo testo assomiglia a QUESTO documento specifico"
#     (vicinanza puntuale).
# Quando discordano non c'è un "vincitore": sono due lampadine sul cruscotto.
# La regola di prodotto onesta: MOSTRALI ENTRAMBI con il loro nome
# ("tipo stimato: busta_paga, confidenza 0.51" + "documento più simile: nota 7,
# somiglianza 0.41"), e lascia alla SOGLIA il compito di dichiarare "non lo so"
# quando NESSUNO dei due è convincente. L'operatore umano decide l'ultimo miglio:
# è lui il pilota, tu gli dai gli strumenti.
#
# MINI-ESERCIZIO 3.3 (rinforzo E8)
# ---------------------------------
# Scenario: classificatore dice "busta_paga" con confidenza 0.51 (bassa); il
# vicino più simile è a 0.41 (basso). Entrambi deboli.
# TODO: scrivi in 2-3 righe cosa mostri all'operatore e perché NON scegli un
# vincitore tra i due numeri.
#
# RISPOSTA:
# All'operatore mostro entrambi i dati, sia la confidenza del classificatore, sia il coseno con il documento più simile. Entrami danno dei segnali unici, diversi e entrambi importanti. Il primo ci da la classe predetta e la relativa confidenza, l'altro ci riporta il documento più simile e il suo coseno. In pratica sono due modi di analizzare diversi ma entrambi producono segnali utili
#
# -----------------------------------------------------------------------------
# 🔁 RINFORZO MIRATO — Mini 6.4 del 02b ("vantaggio di casa" del benchmark)
# -----------------------------------------------------------------------------
# La soglia si sceglie GUARDANDO I DATI. Ma attenzione al tranello: se scegli la
# soglia che massimizza la precision SULLE STESSE 30 note che poi userai in
# produzione, hai fatto la pagella sui compiti copiati — il solito vantaggio di
# casa. In un prodotto vero la scegli su un gruppo di documenti e la VERIFICHI
# su un gruppo diverso (è la stessa idea di train/test split di M2, solo che
# qui non c'è training: c'è una manopola da regolare).
#
# MINI-ESERCIZIO 3.4 (rinforzo benchmark onesto)
# -----------------------------------------------
# TODO: con i punteggi del Mini 3.2, scegli UNA soglia con un criterio dichiarato
# (esempio: "bloccare almeno la metà degli errori" oppure "buttare via al massimo
# il 10% dei giusti"). Scrivi: criterio → soglia scelta → risultato (quanti
# errori bloccati, quanti giusti persi). Non c'è UNA risposta giusta: conta il
# CRITERIO esplicito.
#
# RISPOSTA:
# Eliminare almeno la metà degli errori -> 0.73 -> Errori evitati = 3 e buon trade-off con giusti persi = 7. 
#
# 3.5 · IL GRAFICO: la soglia si VEDE (analogia → codice → GRAFICO → morale)
# ---------------------------------------------------------------------------
# La regola matematica del corso vale anche per la soglia: dopo l'analogia (il
# maître onesto) e il codice (decidi_con_soglia), disegnamo il trade-off. Ogni
# colonna è una fascia di punteggio del vicino1; il colore dice se era giusto
# o sbagliato; la linea tratteggiata è la soglia.

import matplotlib.pyplot as plt                                     # grafici (come nel 02b)

punteggi_v1 = []            # coseno del vicino1 di ogni nota
giusti_v1 = []              # True se il vicino1 è dello stesso tipo della nota
for i in range(len(note)):                                          # una riga per nota
    s_i = E @ E[i]                                                  # coseni verso la nota i
    ordine_i = np.argsort(-s_i)                                     # dal più simile...
    j = int(ordine_i[1])                                            # ...il SECONDO è il vicino1
    punteggi_v1.append(float(s_i[j]))                               # il suo coseno
    giusti_v1.append(note.loc[j, "tipo"] == note.loc[i, "tipo"])    # giusto o no
# (queste 4 righe sono la tua top_k(s_i, 2)[1] scritta inline: se hai già
#  finito la Sez. 2 puoi sostituirle con: j, p = top_k(s_i, 2)[1])

plt.figure(figsize=(9, 4))                                          # quadro 9x4
bins = np.linspace(0.3, 1.0, 15)                                    # fasce di punteggio
plt.hist([p for p, g in zip(punteggi_v1, giusti_v1) if g],          # i 24 giusti in verde
         bins=bins, alpha=0.7, color="green", label="vicino giusto")
plt.hist([p for p, g in zip(punteggi_v1, giusti_v1) if not g],      # i 6 sbagliati in rosso
         bins=bins, alpha=0.7, color="red", label="vicino sbagliato")
# plt.axvline(0.70, color="black", linestyle="--", label="soglia 0.70")   # la manopola
plt.xlabel("coseno del vicino più simile")                          # asse x
plt.ylabel("quante note")                                           # asse y
plt.title("La soglia sposta il confine tra 'rispondo' e 'non lo so'")
plt.legend()                                                        # legenda
                                                        # apri il grafico

# Cosa DEVI vedere: le barre rosse NON stanno tutte a sinistra della linea.
# C'è una zona di MESCOLANZA (≈0.60–0.82) dove rosso e verde si sovrappongono:
# lì dentro, QUALUNQUE posizione della linea sbaglia qualcosa. È la forma
# visiva della morale della Sez. 3: la soglia è una manopola tra due mali,
# e la mescolanza è il motivo per cui nessuna soglia sarà mai perfetta.
#
# MINI-ESERCIZIO 3.5 — muovi la linea
# ------------------------------------

print("\nMini-esercizio 3.5\n")

# TODO 1: riesegui il grafico con la linea a 0.85 (cambia solo axvline).
plt.axvline(0.85, color="black", linestyle="--", label="soglia 0.85")
# plt.show()  

# TODO 2: conta sui TUOI array (non a occhio): a 0.85 quanti errori blocchi e
#         quanti giusti perdi? (attesi verificati il 19/10/2026: 6/6 e 20/24)
a, b, c, d = f(0.85)
print(f"Verificati: {a}/{c} bloccati, {b}/{d} persi")

# TODO 3: in una riga — perché "alzo la soglia finché non passa nessun errore"
#         NON è una strategia?
#
# RISPOSTE:
#
# Non è una strategia per via dell'inevitabile trade-off che abbiamo nel cercare di bloccare gli errori. Il costo, come nel caso verificato sopra, dimostra che aver bloccato tutti gli errori ( 6 su 6) ha imposto un "sacrificio molto grande", ossia l'aver "buttato" quasi tutti i simili giusti che il modello aveva correttamente individuato. Dobbiamo non cercare di eliminare del tutto l'errore, ma trovare il compromesso più accettabile per il nostro dominio.


# =============================================================================
# SEZIONE 4 — precision@k e recall@k: la pagella della ricerca
# =============================================================================
#
# 🔁 RIPASSO PROPOSITIVO — la pagella del 02b e le metriche di M2
# ---------------------------------------------------------------
# Nel 02b (Mini 5.1) hai costruito la pagella: per ogni nota, i 3 vicini più
# simili, e hai contato quanti erano dello stesso tipo. In M2 avevi precision
# ("tra quelli che ho detto positivi, quanti lo erano") e recall ("tra i veri
# positivi, quanti ne ho presi"). Qui le due cose si incontrano.
#
# 4.1 · LE DUE METRICHE DELLA RICERCA
# -----------------------------------
# La ricerca restituisce k risultati. I denominatori cambiano tutto:
#
#   • precision@k = (vicini giusti tra i k restituiti) / k
#     "Quanto è pulita la lista che ho mostrato?"
#     Esempio: 3 risultati, 2 giusti → 2/3 ≈ 0.67
#
#   • recall@k = (vicini giusti tra i k restituiti) / (TUTTI i pertinenti esistenti)
#     "Quanta parte del tesoro ho portato in superficie?"
#     Esempio: nel corpus ci sono 9 buste paga; la query ne trova 2 nei primi 3
#     → recall@3 = 2/9 ≈ 0.22 (se contiamo tutte le 9 come pertinenti)
#
# k è una manopola: k grande → recall sale (trovi più cose) ma precision scende
# (entra più rumore). k = 1 → precision massima possibile ma recall minuscola.
#
# 4.2 · PERCHÉ L'ACCURACY QUI NON HA SENSO
# ----------------------------------------
# Accuracy = (giusti totali) / (casi totali). Funziona quando i casi sono
# bilanciati ("spam/non spam": metà e metà circa). Nella ricerca i "casi totali"
# sarebbero TUTTE le coppie (query, documento-non-pertinente): milioni di "veri
# negativi" che nessuno conta. Un motore che non restituisce MAI niente avrebbe
# accuracy ~100% e utilità zero. Per questo si usano precision@k e recall@k:
# misurano solo quello che il motore ha effettivamente mostrato.
#
# 4.3 · ESEMPIO GUIDATO (conteggio su UNA riga, poi tocca a te)
# -------------------------------------------------------------
tipi_vicini_esempio = ["busta_paga", "altro", "busta_paga"]     # i tipi dei 3 vicini
tipo_atteso_esempio = "busta_paga"                              # il tipo della query
giusti_esempio = sum(1 for t in tipi_vicini_esempio             # conta quelli uguali
                     if t == tipo_atteso_esempio)               # → 2
precision_esempio = giusti_esempio / 3                          # 2/3 ≈ 0.67
print("precision@3 esempio:", round(precision_esempio, 3))      # 0.667
#
# 4.4 · ORA LA SCRIVI TU — `precision_su_k(tipi_vicini, tipo_atteso, k)`
# ----------------------------------------------------------------------  [REGOLA 45]
# Consegna: prende la lista dei tipi dei vicini (in ordine di ranking), il tipo
# atteso e k; restituisce la precision sui primi k.
#
# DOMANDA D'INGAGGIO che decide la firma: se la soglia ne ha lasciati passare
# solo 2 su k=3, il denominatore è 2 o 3? La risposta DA MANUALE (e da
# colloquio): è SEMPRE k. Chi risponde poco viene penalizzato — altrimenti un
# motore che mostra 1 solo risultato giusto avrebbe precision@k = 1.0 perfetta
# pur non rispondendo quasi mai. Il "non lo so" si misura con una metrica
# SORELLA (in quante query ricevono risposta: la copertura), non gonfiando la
# precision. Nei prodotti esiste anche la variante "precision sulle risposte
# date" (denominatore = mostrati): legittima, ma va DICHIARATA e non si chiama
# precision@k. Al colloquio: precision@k = giusti / k, punto.
#
#   def precision_su_k(tipi_vicini: list[str], tipo_atteso: str, k: int) -> float:
#
# SCRIVILA QUI SOTTO:

def precision_su_k(tipi_vicini: list[str], tipo_atteso: str, k: int) -> float:
    return float(sum(1 for t in tipi_vicini[:k] if t == tipo_atteso) / k)
#
# MINI-ESERCIZIO 4.1 — verifica la tua precision_su_k
# ----------------------------------------------------

print("\nMini-esercizio 4.1\n")

# TODO 1: precision_su_k(["cu", "cu", "altro"], "cu", 3) → 2/3 ≈ 0.667

todo_1 = precision_su_k(["cu", "cu", "altro"], "cu", 3)
assert np.isclose(todo_1, 0.667, atol= 1e-3)
print(f"Risultato TODO 1: {round(todo_1, 3)}")

# TODO 2: precision_su_k(["cu", "altro"], "cu", 3) → ? Se hai applicato la
#         regola da manuale (denominatore SEMPRE k) viene 1/3 ≈ 0.333:
#         il risultato "mancante" pesa come un errore. Rileggi la domanda
#         d'ingaggio qui sopra e scrivi in una riga PERCHÉ non è 1/2.

todo_2 = precision_su_k(["cu", "altro"], "cu", 3)
assert np.isclose(todo_2, 0.333, atol=1e-3)
print(f"Risultato TODO 2: {round(todo_2, 3)}")

# Non è 1/2 perchè se facessimo in questo modo, premieremmo un modello che risponde poco, invece decidiamo a priori di considerare le "non risposte" come errori.
#
# MINI-ESERCIZIO 4.2 · 🔤 [GLOSSARIO IN CODICE] — i nomi giusti dentro il codice
# ------------------------------------------------------------------------------

print("\nMini-esercizio 4.2\n")

# (Rinforzo #67: nel 02b hai confuso il nome della pagella chiamando
#  "precision@k" una cosa che non c'entrava. Qui la usi DAVVERO, con il suo nome.)

# TODO 1: con la query "prospetto paga di aprile" (Mini 2.2), prendi i tipi dei
#         3 vicini con la tua top_k e calcola precision_su_k(tipi, "busta_paga", 1)
#         e precision_su_k(tipi, "busta_paga", 3).
#         Atteso (19/10/2026): precision@1 = 1.0, precision@3 = 2/3 ≈ 0.67

frase = "prospetto paga di aprile"
tipi = pd.read_csv(PERCORSO_CSV)['tipo'].tolist()
q = embedda(frase, modello, normalizza=True)[0]
S = E @ q
K = [(1, 1.0), (3, 0.667)]
print("Risultato TODO 1\n")
for k, p in K:
    vicini = top_k(S, k)
    tipi_top = [tipi[i] for i, _ in vicini]
    prec = precision_su_k(tipi_top, "busta_paga", k)
    assert np.isclose(prec, p, atol=1e-3)
    print(f"K: {k} -> Precision: {round(prec, 3)}")

# TODO 2: in una riga, scrivi cosa misura precision_at_k senza usare la parola
#         "precision" (come se la spiegassi a un collega).
#
# RISPOSTA TODO 2:
# Su k risultati restituiti, quanti di questi sono giusti?


# MINI-ESERCIZIO 4.3 — recall@k sulle buste paga
# ----------------------------------------------

print("\nMini-esercizio 4.3\n")

# TODO 1: quante note di tipo "busta_paga" ci sono nel corpus? (conta con pandas:
#         atteso 9)

tipi = pd.read_csv(PERCORSO_CSV)['tipo'].tolist()
n_bp = sum(1 for t in tipi if t == "busta_paga")
assert n_bp == 9
print(f"Risultato TODO 1: {n_bp}")

# TODO 2: query "prospetto paga di aprile": quante buste paga compaiono nei
#         primi 3 vicini? (atteso: 2) → recall@3 = 2/9 ≈ 0.22

frase = "prospetto paga di aprile"
tipi = pd.read_csv(PERCORSO_CSV)['tipo'].tolist()
q = embedda(frase, modello, normalizza=True)[0]
S = E @ q
k = 3
vicini_top3 = top_k(S, k)
n_bp_tipi_top3 = sum(1 for i, _ in vicini_top3 if tipi[i] == "busta_paga")
recall_at_k = n_bp_tipi_top3 / n_bp
assert np.isclose(recall_at_k, 0.222, atol=1e-3)
print(f"Risultato TODO 2:\n")
print(f"- Recall@3:        {round(recall_at_k, 3)}")
print(f"- Max recall@3:    {round(k / n_bp, 3)}")
print(f"- Rec@3 su base 1: {round(recall_at_k / (k / n_bp), 3)}")

# TODO 3: in una riga — perché recall@3 è così bassa anche se il motore "funziona"?
#
# RISPOSTA TODO 3:
# Perché abbiamo deciso che il modello, anche se le buste paga all'interno del corpus sono 9, lui può riportarne al massimo 3 in risposta. Dunque in questo caso la recall@k va rapportata al suo effettivo massimo raggiungibile, che è dato dalla divisione k / n_buste_nel_corpus.
#
# MINI-ESERCIZIO 4.4 — la pagella completa (vettorizzata)
# -------------------------------------------------------

print("\nMini-esercizio 4.4\n")

# TODO 1: per OGNI nota i: q = E[i]; punteggi = E @ q; vicini = top_k(punteggi, 4)
#         (k+1 perché il primo è se stessa); tipi_vicini = tipi dei vicini[1:4].
#
# TODO 2: media di precision_su_k(tipi_vicini, tipo_della_nota, 3) su tutte le
#         30 note.
#         Atteso (19/10/2026): precision@3 media ≈ 0.667; precision@1 = 24/30 = 0.80
# TODO 3: confronta con la pagella del 02b (stessa metrica, fatta col ciclo):
#         i numeri devono coincidere. Se non coincidono, chi mente?

note = pd.read_csv(PERCORSO_CSV)
tipi = note['tipo'].tolist()
K = [1, 3]
for k in K:
    precision_totale = 0.0
    for i in range(len(note)):
        tipo_q = note.iloc[i]["tipo"]
        s_i = E @ E[i]
        top = top_k(s_i, k + 1)[1:k + 1]
        tipi_top = [tipi[j] for j, _ in top]
        precision_at_k = float(sum(1 for t in tipi_top if t == tipo_q) / k)
        precision_totale += precision_at_k
    precision_media = precision_totale / len(note)
    print(f"Precisio@{k} -> {round(precision_media, 3)}")

# RISPOSTA TODO 3:
# Non coincidono ma nessuno mente. La formula è la stessa, ma è stata ottenuta da due esami diversi, quindi non confrontabili.

# =============================================================================
# SEZIONE 5 — Falsi amici: dove il coseno ti mente
# =============================================================================
#
# 🔁 RIPASSO PROPOSITIVO — i limiti che hai già visto
# ---------------------------------------------------
# Nel 02a (Sez. "quando NON usarla") e nel 02b (quiz su cifre e negazione) hai
# già incontrato i punti deboli: la rappresentazione media non vede le negazioni,
# i numeri precisi, i codici. Qui li MISURIAMO sul modello vero, con numeri veri,
# e tiriamo fuori la regola pratica per la torre di controllo.
#
# 5.1 · LA NEGAZIONE: "non" sparisce nella media
# ----------------------------------------------
# Misura vera (19/10/2026):
#   "il netto supera il lordo"  vs  "il lordo supera il netto"  → coseno ≈ 0.942
# Due frasi con significato OPPOSTO risultano quasi identiche. Perché?
#   • Nel tokenizer contano i PEZZI: "netto", "supera", "lordo" — le stesse
#     parole in entrambe le frasi, solo in ordine diverso.
#   • Il pooling fa la MEDIA: la media non vede l'ordine e quasi non vede il
#     "non" (è una parola corta, frequentissima, poco informativa per la media).
# E come se giudicassi due ricette guardando solo la lista degli ingredienti:
# "sale poi zucchero" e "zucchero poi sale" hanno la stessa lista.
#
# -----------------------------------------------------------------------------
# 🔁 RINFORZO MIRATO — Micro #6 del 02b (lasciata in bianco)
# -----------------------------------------------------------------------------
# La domanda era: "guadagno" vs "non guadagno" — perché per un embedding sono
# più simili che diverse, e quando preferisci una ricerca full-text classica?
# Ora hai il numero: 0.942. Il meccanismo è quello sopra: media dei pezzi.
# La risposta completa: preferisci la ricerca per PAROLE ESATTE (full-text,
# LIKE in SQL, `in` in Python) quando il significato dipende da POCHE PAROLE
# CRITICHE: negazioni ("non", "senza"), codici (CF, IBAN), cifre esatte
# (importi, date), nomi propri. In quei casi la parola esatta È il significato.
#
# MINI-ESERCIZIO 5.1 (rinforzo Micro #6)
# ---------------------------------------
# TODO: completa le tre righe (2-3 parole ciascuna):
#   a) "guadagno" vs "non guadagno" hanno coseno alto perché ________________
#   b) per le clausole con "non"/"senza" nel contratto della torre uso
#      ________________ perché ________________
#   c) la ricerca semantica vince invece quando ________________
#
# RISPOSTE:
#
# 5.2 · CIFRE E CODICI: il coseno non sa contare
# ----------------------------------------------
# Misure vere (19/10/2026):
#   "netto 1850 euro"  vs  "netto 1851 euro"          → coseno ≈ 0.935
#   CF "RSSMRA80A01H501X" vs CF "RSSMRA80A01H501Y"    → coseno ≈ 0.992
# Per il modello sono quasi la stessa frase. Per la torre di controllo sono
# DIFFERENZE ENORMI: un euro di differenza in un cedolino, una lettera di
# differenza in un codice fiscale = PERSONA DIVERSA.
#
# -----------------------------------------------------------------------------
# 🔁 RINFORZO MIRATO — lacuna #69 (quiz verifica 02b: CF al 99%)
# -----------------------------------------------------------------------------
# Nel quiz del 02b la domanda sul CF ti ha messo in difficoltà. La regola è:
#   **LE CIFRE E I CODICI SI CONFRONTANO CON IL MATCH ESATTO, NON CON IL COSENO.**
# Il coseno serve per il SENSO ("di cosa parla questo documento"); l'uguaglianza
# (dopo normalizzazione: spazi, maiuscole) serve per i VALORI ("è la stessa
# persona? lo stesso IBAN?"). Sono due domande diverse, due strumenti diversi.
#
# -----------------------------------------------------------------------------
# 🔁 RINFORZO MIRATO — Mini 2.2 del 02b (lasciata in bianco): sottoparole e
# parole mai viste
# -----------------------------------------------------------------------------
# La domanda era: "come fa il modello a gestire parole mai viste in training?"
# Risposta: grazie alle SOTTOPAROLE. "internazionalizzazione" si spezza in pezzi
# (internazional + izza + zione...), e il modello compone il significato dai
# pezzi — come leggi una parola lunghissima in tedesco spezzandola. Per questo
# NON esiste il problema "parola fuori vocabolario" come in TF-IDF.
# MA attenzione: gestire ≠ capire. I pezzi numerici di "1850" e "1851" sono
# quasi identici ("185"+"0" vs "185"+"1"), quindi il VETTORE finale è quasi
# identico: la sottoparola salva dalla parola sconosciuta, non dalla differenza
# numerica. È esattamente il motivo per cui sopra vale la regola del match esatto.
#
# MINI-ESERCIZIO 5.2 (rinforzo #69)
# ----------------------------------
# TODO 1: verifica tu stesso con 3 righe di codice: embedda le due coppie
#         (netto 1850/1851 e i due CF) con normalizza=True e stampa i coseni.
#         Attesi ≈ 0.93 e ≈ 0.99.
# TODO 2: completa la regola ibrida della torre: "Per decidere se due documenti
#         riguardano la stessa pratica confronto ________________ con il match
#         esatto e ________________ con il coseno."
#
# RISPOSTA TODO 2:
#
# MINI-ESERCIZIO 5.3 — le cifre nella TUA tokenizza (ponte al cap. 01)
# ---------------------------------------------------------------------
# 🔁 RIPASSO PROPOSITIVO — `tokenizza` (cap. 01, testo_utils): spezza in parole
# minuscole con RE_TOKEN = re.compile(r"[a-zàèéìòù<>]+") e toglie le stopword.
# Nota il pattern: SOLO LETTERE. I numeri non ci sono.
#
# TODO 1: tokenizza("netto 1850 euro") — cosa restituisce? (prevedi, poi esegui)
# TODO 2: quindi nella pipeline del cap. 01 (TF-IDF) le cifre ________________
#
# RISPOSTE:
#
# 5.3 · TESTI CORTI: poco contesto, poca bussola
# ----------------------------------------------
# Misura vera (19/10/2026):
#   "cedolino"  vs  "busta paga"  → coseno ≈ 0.428
# Sono SINONIMI! Eppure il coseno è basso. Perché? Il pooling fa la media dei
# token: con UN token solo, il vettore è quel token e basta, senza contesto che
# lo "tiri" verso il mondo delle paghe. "cedolino" da solo potrebbe essere anche
# il cedolino di un parcheggio. Le frasi lunghe si auto-spiegano; le parole
# singole no. Regola pratica: sotto le 3-4 parole, diffida dei punteggi.
#
# MINI-ESERCIZIO 5.4 — il corto contro il lungo
# ----------------------------------------------
# TODO 1: embedda "cedolino" e "il cedolino dello stipendio di ottobre con
#         trattenute" e confronta i coseni con "busta paga". Quale delle due
#         query si avvicina di più? (esegui e scrivi i due numeri)
# TODO 2: in una riga — perché aggiungere contesto aiuta il pooling?
#
# RISPOSTE:
#
# 5.4 · QUASI DUPLICATI: il falso positivo che la soglia non salva
# -----------------------------------------------------------------
# La nota 13 (estratto_conto) ha come vicino una busta_paga a 0.807: più alto di
# MOLTI vicini corretti. Nessuna soglia ragionevole lo blocca senza buttare via
# metà delle risposte giuste. È il limite vero del retrieval denso: documenti
# che condividono tema, lessico e struttura ma NON il tipo amministrativo.
# In produzione si affronta con il re-ranking (un secondo modello più pignolo,
# Sez. 6 e M6) o con filtri a monte (cerca solo dentro il tipo già classificato —
# lo farai in E8).
#
# MINI-ESERCIZIO 5.5 — quale strumento per quale caso?
# -----------------------------------------------------
# Per ogni caso scrivi: SEMANTICO (coseno) / ESATTO (match) / ENTRAMBI:
#   a) trovare note sullo stesso argomento                    →
#   b) verificare se due documenti hanno lo stesso CF         →
#   c) capire se una clausola contiene una negazione critica  →
#   d) raggruppare documenti della stessa persona senza CF    →
#
# RISPOSTE:
#


# =============================================================================
# SEZIONE 6 — Scalabilità: da 30 note a un milione di documenti
# =============================================================================
#
# 🔁 RIPASSO PROPOSITIVO — i costi del 02b (Sez. 8: batch e dimensioni)
# ---------------------------------------------------------------------
# Nel 02b hai visto che embeddare costa millisecondi per frase e che il batch
# ammortizza il costo fisso. Qui guardiamo l'ALTRO costo: la ricerca.
#
# 6.1 · I CONTI A SPANNE
# ----------------------
# La nostra ricerca è: 1 encoding della query + 1 matmul (30 × 384).
# Con N documenti la matmul è (N × 384): i prodotti scalari crescono con N.
#   N = 30        →  11.520 prodotti        → istantaneo
#   N = 1.000.000 →  384.000.000 prodotti   → pochi ms su CPU moderna: ANCORA OK!
# Il problema vero non è il tempo: è la RAM. Ogni vettore float32 = 384 × 4 byte
# ≈ 1,5 KB. Un milione di documenti ≈ 1,5 GB sempre in memoria. Cento milioni
# ≈ 150 GB: non ci sta. E ogni documento nuovo va embeddato e indicizzato.
#
# 6.2 · LA SOLUZIONE DEL SETTORE: INDICI APPROSSIMATI E VECTOR DB
# ---------------------------------------------------------------
# • ANN (Approximate Nearest Neighbor = "vicino più prossimo APPROSSIMATO"):
#   strutture dati furbe che trovano i vicini SENZA confrontare tutti i vettori.
#   Scambi un pizzico di precisione (trovi il 99% dei vicini veri) per una
#   velocità enorme (millisecondi su milioni di vettori). Come cercare una parola
#   in un dizionario con l'indice alfabetico invece di leggere tutto.
# • VECTOR DB (database vettoriale): un database che dentro ha un indice ANN.
#   ChromaDB (lo userai in M6), pgvector (estensione di PostgreSQL), FAISS...
#   Gli dai i vettori una volta, poi gli chiedi "i 10 più simili a questo".
#
# COSA NON CAMBIA (ed è il punto didattico): coseno, top-k, soglia, precision@k
# restano IDENTICI. Cambia solo CHI fa la matmul: da NumPy in RAM a un servizio
# con indice. Le tue tre funzioni di oggi sono la logica che ritroverai dentro
# ChromaDB.
#
# MINI-ESERCIZIO 6.1 — il conto della RAM
# ----------------------------------------
# TODO: quanta RAM occupano 10 milioni di documenti da 384 dimensioni in
#       float32 (4 byte)? Fai il conto in Python e stampa in GB.
#       (atteso: 10_000_000 × 384 × 4 byte ≈ 15,4 GB)
#
# MINI-ESERCIZIO 6.2 — cosa resta, cosa cambia
# ---------------------------------------------
# TODO: completa le due righe:
#   a) "Passando a un vector DB restano identici: ________________, ________________,
#      ________________ e ________________"
#   b) "Cambia invece: ________________ e ________________"
#
# RISPOSTE:
#
# -----------------------------------------------------------------------------
# 📚 LETTURA PARALLELA (facoltativa, 15-20 min) — [ALAMMAR, Hands-On Large
# Language Models, cap. 8, "Semantic Search"]
# -----------------------------------------------------------------------------
# Quello che hai costruito a mano in questo capitolo è il dense retrieval del
# libro: embed → coseno/dot → top-k → valutazione. Lì trovi gli stessi pezzi in
# forma industriale: il bi-encoder (il tuo MiniLM), il cross-encoder per il
# re-ranking (E9) e gli indici approssimati per scalare (Sez. 6).
# LEGGI con attenzione: come presentano il trade-off velocità/accuratezza tra
# bi-encoder e cross-encoder — è la stessa scelta "indice SQL vs JOIN costosa"
# che hai visto in E9.
# SALTA pure per ora: gli esempi con API a pagamento e i nomi dei reranker
# specifici (li riprendiamo in M6 con il RAG).
#


# =============================================================================
# QUIZ DI VERIFICA (su questo capitolo — 10 domande)
# =============================================================================
# Stessa regola: primo tentativo, risposte qui, correzione con le soluzioni in
# fondo, voto nel diario.
#
# V1 · Prevedi output:
#      E ha righe a norma 1; q ha norma 1; s = E @ q.
#      print(s.shape) e il significato di s[7]?
#
# RISPOSTA:
#
# V2 · Vero o Falso: "np.argsort(-punteggi)[:5] dà gli indici dei 5 punteggi
#      più BASSI."
#
# RISPOSTA:
#
# V3 · Trova l'errore:
#      def top_k(punteggi, k):
#          ordine = np.argsort(punteggi)          # qualcosa non va
#          return [(int(i), float(punteggi[i])) for i in ordine[:k]]
#
# RISPOSTA:
#
# V4 · Definizione: precision@k e recall@k — cosa cambia al DENOMINATORE?
#
# RISPOSTA:
#
# V5 · Completa il codice della TUA decidi_con_soglia:
#      return [v for v in vicini if ______________________]
#
# RISPOSTA:
#
# V6 · Prevedi output: vicini con tipi ["cu", "cu", "altro", "cu"], tipo "cu".
#      precision@2 = ?  precision@4 = ?
#
# RISPOSTA:
#
# V7 · Trova l'errore (è la regola del capitolo):
#      cf_a, cf_b = "RSSMRA80A01H501X", "RSSMRA80A01H501Y"
#      v_a = embedda([cf_a], modello, normalizza=True)[0]
#      v_b = embedda([cf_b], modello, normalizza=True)[0]
#      stessa_persona = coseno(v_a, v_b) > 0.95     # ← perché è sbagliato?
#
# RISPOSTA:
#
# V8 · Vero o Falso: "Alzare la soglia di accettazione aumenta i casi in cui
#      il motore risponde 'non lo so'."
#
# RISPOSTA:
#
# V9 · Trova l'errore:
#      indici = np.argsort(-punteggi)[:3]
#      for i in indici:
#          print(note[note['id'] == i]['testo'])     # corpus: id da 1 a 30
#
# RISPOSTA:
#
# V10 · 💬 FEYNMAN — Spiega con parole tue (3-5 righe, niente codice):
#      a un collega web dev: perché rispondere "non lo so" (lista vuota sotto
#      soglia) è MEGLIO che mostrare comunque il vicino meno lontano?
#
# RISPOSTA:
#


# =============================================================================
# ESERCIZI
# =============================================================================

# -----------------------------------------------------------------------------
# E1 · 🔧 [REFACTORING] — dal ciclo alla matmul
# -----------------------------------------------------------------------------
# Questo codice funziona ma è scritto male (stile pagella del 02b: un coseno
# alla volta, ciclo Python, niente vettorizzazione). Riscrivilo in MASSIMO
# 4 righe usando E @ q e la TUA top_k, con stesso output.
#
#   def cerca_lento(query, E, testi, modello, k=3):
#       q = embedda([query], modello, normalizza=True)[0]
#       risultati = []
#       for i in range(E.shape[0]):
#           riga = E[i]
#           punteggio = coseno(riga, q)
#           risultati.append((i, punteggio))
#       risultati_ordinati = sorted(risultati, key=lambda coppia: coppia[1], reverse=True)
#       return risultati_ordinati[:k]
#
# SCRIVI QUI LA TUA VERSIONE:
#
# def cerca_veloce(query, E, testi, modello, k=3):
#     ...
#
# Verifica: cerca_lento e cerca_veloce devono dare gli stessi indici su
# "cedolino di ottobre" (a meno di pareggi).

# -----------------------------------------------------------------------------
# E2 · 🔍 [DEBUG] — la ricerca impazzita (3 bug: prima il SILENZIO, poi il crash)
# -----------------------------------------------------------------------------
# ATTO 1 — il silenzio. Questo codice dovrebbe stampare le 3 note più simili
# a "prospetto paga". Eseguilo: NON va in errore. Ed è proprio questo il guaio.
#
#   q = embedda(["prospetto paga"], modello)[0]              # bug nascosto qui
#   punteggi = E @ q
#   ordine = np.argsort(punteggi)[:3]                        # ...e qui
#   for i in ordine:
#       riga = note[note["id"] == int(i)]                    # ...e qui (id da 1 a 30!)
#       print(riga["testo"].iloc[0], round(float(punteggi[i]), 3))
#
# Output reale (misurato il 19/10/2026):
#   ESTRATTO CONTO - data valuta 15/04/2026 - causale accredito emolumenti... 0.826
#   CERTIFICAZIONE UNICA 2026 redditi 2025 - dati fiscali...                 0.907
#   Visura camerale ordinaria - sezione attività e qualifiche...             0.916
# Tre note fuori tema per "prospetto paga", stampate con faccia seria.
# INDIZIO: stampa anche punteggi.max() → 2.457. Un coseno non può superare 1.
#
# ATTO 2 — il crash. Cambia solo la riga di `ordine` in:
#   ordine = np.argsort(punteggi)          # classifica completa, 30 righe
# e riesegui il ciclo: dopo una quindicina di righe stampate esplode:
#   IndexError: single positional indexer is out-of-bounds
#
# TRE bug: trovali e correggili SENZA riscrivere tutto. Intervento del mentor
# solo dopo 2 tentativi (Regola 17). Suggerimento di metodo: risolvi prima
# l'IndexError (Atto 2), poi spiega perché l'Atto 1 era sbagliato SENZA alcun
# errore — i bug peggiori sono quelli silenziosi.
#
# Bug 1 (dove e perché):
# Bug 2 (dove e perché):
# Bug 3 (dove e perché):
# Codice corretto (riscrivi il blocco):

# -----------------------------------------------------------------------------
# E3 · 🧠 [RETRIEVAL] — riscrivi `coseno(a, b)` da zero
# -----------------------------------------------------------------------------
# Senza guardare testo_utils.py: riscrivi la funzione coseno per vettori 1D,
# con la guardia sulla norma zero. Poi confrontala con l'originale.
# (Terza volta che la scrivi: è il cuore del capitolo, deve uscire a memoria.)
#
# def coseno_mio(a: NDArray[np.float64], b: NDArray[np.float64]) -> float:
#     ...

# -----------------------------------------------------------------------------
# E4 · 🔀 [INTERLEAVING] — la tua top_k su TF-IDF (cap. 01)
# -----------------------------------------------------------------------------
# 🔁 RIPASSO PROPOSITIVO — TF-IDF (cap. 01): ogni testo diventa un vettore dove
# ogni colonna è una parola e il peso dice quanto quella parola è "decisiva" per
# quel testo (frequente nel testo, rara nel corpus). Con norm='l2' le righe sono
# già a norma 1: anche lì dot product = coseno.
#
# TODO 1: costruisci la matrice TF-IDF dei 30 testi:
#           from sklearn.feature_extraction.text import TfidfVectorizer
#           vett = TfidfVectorizer()                      # default: norm='l2'
#           X = vett.fit_transform(testi)                 # matrice sparsa (30, n_parole)
# TODO 2: trasforma la query "prospetto paga di aprile" con vett.transform([query])
#         e calcola i punteggi: X @ q_tfidf.T → attenzione alla forma, serve
#         .toarray().ravel() per avere (30,).
# TODO 3: applica la TUA top_k(punteggi_tfidf, 3) e confronta i vicini con quelli
#         semantici del Mini 2.2. Cambiano? Scrivi 2 righe: cosa trova TF-IDF che
#         il semantico non trova (e viceversa)?
#
# RISPOSTE:

# -----------------------------------------------------------------------------
# E5 · 🎯 [COLLOQUIO] — "Implementami una ricerca semantica"
# -----------------------------------------------------------------------------
# Domanda da colloquio reale: "Devi aggiungere la ricerca semantica a un gestore
# documentale. Come la implementi? E quando NON la useresti?"
# Prepara la risposta a VOCE in 60-90 secondi, poi scrivi qui lo scheletro
# (4-6 righe guida, come se fossero appunti sul foglio del colloquio).
# Deve contenere: embedding + normalizzazione, matmul/top-k, soglia + "non lo so",
# metrica per valutarla, e almeno 2 casi in cui NON la usi.
# Antidoto Pattern #6 (dichiaralo!): prima di scrivere, metti come prima riga
# "PUNTI CHE VEDO: 6" (gli elementi della checklist qui sopra) e spunta ogni
# punto mentre lo copri.
#
# APPUNTI:

# -----------------------------------------------------------------------------
# E6 · ⌨️ [PIPELINE A MEMORIA] — P1 → P2 → P3 senza guardare sopra
# -----------------------------------------------------------------------------
# Scrivi da zero, in fondo al file o su un foglio poi ricopiato, la pipeline
# completa su un mini-benchmark: 4 query con tipo atteso noto
#   ("busta paga con totale competenze e trattenute del mese" → busta_paga;
#    "redditi da lavoro dipendente e ritenute nella certificazione unica" → cu;
#    "estratto conto con elenco movimenti bonifici e saldo progressivo" → estratto_conto;
#    "atto notarile" → altro).
# Per ogni query: embedda → E @ q → top_k → decidi_con_soglia(0.70).
# Stampa una tabellina con, per ogni query: i 3 vicini (tipo + punteggio),
# precision@3 sul RANKING (la tua precision_su_k sui tipi dei 3 vicini, PRIMA
# della soglia), quanti vicini passano la soglia, esito ("risposta"/"non_lo_so").
# Poi rileggi la Sez. 2-4 e segna cosa avevi dimenticato (se qualcosa).
# Nota: le query 1-3 sono volutamente "piene di contesto" (quelle corte
# funzionano peggio, Sez. 5.3); la 4 è volutamente fuori corpus.
#
# COSA AVEVI DIMENTICATO:

# -----------------------------------------------------------------------------
# E7 · 🔤 [GLOSSARIO IN CODICE] — i termini nuovi diventano codice
# -----------------------------------------------------------------------------
# Scrivi una funzione `scheda_ricerca(query, E, note, modello, k, soglia)` che
# restituisce un dizionario con CHIAVI che usano i termini del capitolo:
#   {
#     "candidati": [...],              # i k vicini come (indice, punteggio) PRIMA della soglia
#     "ranking": [...],                # gli stessi in ordine decrescente di punteggio
#     "sopra_soglia": [...],           # dopo decidi_con_soglia
#     "soglia": soglia,
#     "esito": "risposta" | "non_lo_so",
#     "falso_positivo_semantico_rischio": True/False,  # True se il top1 ha tipo diverso
#                                                      # dalla moda dei tipi sopra soglia
#   }
# Le variabili dentro si chiamano punteggi, vicini, candidati: niente x, tmp, res.
#
# SCRIVILA QUI:

# -----------------------------------------------------------------------------
# E8 · 🌐 [CROSS-CAPITOLO] — classifica PRIMA, cerca DENTRO (cap. 01 + 03)
# -----------------------------------------------------------------------------
# 🔁 RIPASSO PROPOSITIVO — pipeline TF-IDF + LogisticRegression (cap. 01, M2):
# il classificatore impara dai 30 testi a prevedere il TIPO. predict_proba dà la
# distribuzione sulle classi; predict dà la classe vincente. Qui lo riusiamo come
# FILTRO A MONTE: prima decidi il tipo, poi cerchi SOLO tra le note di quel tipo.
#
# TODO 1: addestra al volo la pipeline del cap. 01:
#           from sklearn.feature_extraction.text import TfidfVectorizer
#           from sklearn.linear_model import LogisticRegression
#           from sklearn.pipeline import Pipeline
#           pipe = Pipeline([("tfidf", TfidfVectorizer()),
#                            ("clf", LogisticRegression(max_iter=1000))])
#           pipe.fit(testi, note["tipo"])
# TODO 2: query "addebito bolletta in conto". Prevedi il tipo (atteso:
#         estratto_conto) e la sua probabilità.
# TODO 3: MASCHERA: prendi gli INDICI delle note di quel tipo
#         (es. idx_tipo = note.index[note["tipo"] == tipo_predetto].to_numpy()),
#         calcola punteggi = E @ q SOLO su E[idx_tipo], applica top_k e soglia.
# TODO 4: rifai la stessa ricerca SENZA maschera (su tutta E). Cambia il vicino1?
# TODO 5 · LA DOMANDA FINALE (rispondi in 2 righe): "tra classificatore, coseno
#          e soglia: quale pezzo ha DECISO la risposta finale in questo giro?"
#
# RISPOSTA TODO 5:

# -----------------------------------------------------------------------------
# E9 · 📚 [ALAMMAR] — bi-encoder, cross-encoder e il re-ranking (riformulato)
# -----------------------------------------------------------------------------
# (Il libro spiega il semantic search come retrieve + re-rank; qui è riformulato
#  con il TUO caso, Regola 44d — niente "vai a leggere il libro".)
#
# Il tuo MiniLM è un BI-ENCODER ("due torri"): ogni testo diventa un punto DA
# SOLO, senza vedere la query. Per questo hai potuto calcolare E UNA VOLTA e
# salvarla in note_minilm.pkl: i punti non dipendono da chi li guarda. A query
# time resta una sola codifica + una matmul. Veloce, scala.
#
# Un CROSS-ENCODER invece legge la COPPIA (query, documento) INSIEME e dà un
# punteggio alla coppia: più accurato, perché vede le interazioni tra le parole
# dei due testi (quelle negazioni che il pooling si perde!). Ma non puoi
# pre-calcolare NIENTE: 30 documenti × 1 query = 30 forward; un milione di
# documenti = un milione di forward a OGNI query. Impraticabile.
#
# Per questo il mondo RAG fa RETRIEVE THEN RE-RANK: il bi-encoder pesca 20-50
# CANDIDATI in un lampo; il cross-encoder riordina SOLO quelli, con cura.
# Come in un'agenzia immobiliare: prima filtri sul database (zona, prezzo —
# veloce, grezzo), poi visiti di persona SOLO le 5 case finaliste (lento, accurato).
#
# TODO 1: metti in ordine le fasi di una ricerca con re-ranking:
#         [re-rank dei candidati · codifica della query · top-k sul corpus ·
#          codifica di TUTTI i documenti (una volta) · soglia e risposta]
# TODO 2: perché il bi-encoder può pre-calcolare E e il cross-encoder no?
#         (2 righe)
# TODO 3: con 30 note il cross-encoder costerebbe 30 forward a query. La nota 13
#         (falso positivo a 0.807) verrebbe probabilmente "smascherata" in
#         re-ranking. Perché? (2 righe: pensa alle interazioni parola-parola)
#
# RISPOSTE:


# =============================================================================
# 🏗️ PROGETTO INCREMENTALE — Catalogo E-commerce → Torre di controllo
# =============================================================================
# Roadmap M4: il classificatore (cap. 01) assegna il TIPO; la ricerca semantica
# (02b/03) trova i documenti SIMILI. Manca il terzo mattone della torre:
# **il MATCHING CROSS-DOCUMENTO** — "questa busta paga e questa CU parlano della
# STESSA persona?" È la domanda che la torre si farà di continuo.
#
# Crea un file NUOVO `match_utils.py` (accanto a embed_utils.py) con tre
# funzioni. Le funzioni che DECIDONO (T1 logica di confronto, T3 esito) le
# scrivi tu dopo l'esempio guidato (spirito Regola 45); la versione di
# riferimento è nelle soluzioni.
#
# --- T1 · match_esatto(valore_a, valore_b) -> bool ---------------------------
# Confronta CF/IBAN: restituisce True solo se uguali DOPO normalizzazione
# (spazi via, maiuscole). È la regola #69 nel prodotto: i codici si confrontano
# con l'uguaglianza, MAI con il coseno.
#   match_esatto("RSSMRA80A01H501X", "rssmra80a01h501x ") → True
#   match_esatto("RSSMRA80A01H501X", "RSSMRA80A01H501Y")  → False
#
# --- T2 · match_semantico(testo_a, testo_b, modello) -> float -----------------
# Coseno tra due testi liberi via embedda (normalizza=True) + dot delle due
# righe. ESEMPIO GUIDATO (questa è meccanica, te la do quasi fatta):
#   v = embedda([testo_a, testo_b], modello, normalizza=True)   # (2, 384)
#   return float(v[0] @ v[1])                                    # dot = coseno (norme 1)
#
# --- T3 · verifica_coppia_documenti(doc_a, doc_b, modello, soglia=0.50) -------
# doc = dict con chiavi "cf" e "titolo" (es. "Busta paga ottobre 2025").
# ESEMPIO GUIDATO su UNA coppia, poi la funzione la scrivi tu:
#   doc1 = {"cf": "RSSMRA80A01H501X", "titolo": "Busta paga ottobre 2025"}
#   doc2 = {"cf": "RSSMRA80A01H501X", "titolo": "Certificazione Unica 2026"}
#   cf_uguali = match_esatto(doc1["cf"], doc2["cf"])             # True
#   sim = match_semantico(doc1["titolo"], doc2["titolo"], modello)  # esegui e leggi
# Restituisce un dict:
#   {"cf_uguali": bool, "coseno_titoli": float, "sopra_soglia": bool,
#    "esito": "coerenti" | "da_rivedere" | "diversi"}
# Logica di esito (la scrivi tu, criterio dichiarato nel docstring). Suggerimento:
#   - CF diversi  → MAI "coerenti", anche con coseno alto (l'esatto vince: #69)
#   - CF uguali + titoli sopra soglia → "coerenti"
#   - il resto → "da_rivedere" (un umano guarda)
#
# --- T4 · ASSERT DI REGRESSIONE ------------------------------------------------
#   assert verifica_coppia_documenti(doc1, doc2, m)["esito"] == "coerenti"
#   doc3 = {"cf": "VRDLGI90B02F205Z", "titolo": "Busta paga ottobre 2025"}
#   assert verifica_coppia_documenti(doc1, doc3, m)["esito"] != "coerenti"
#   # anche se i titoli sono IDENTICI: il CF diverso blocca tutto.
#
# Definition of Done del task: match_utils.py esiste, T1-T3 scritte da te,
# T4 verde, soglia e criterio di esito dichiarati nel docstring.
#
# SPAZIO DI LAVORO (bozze prima di copiare in match_utils.py):


# =============================================================================
# CHECK FINALE
# =============================================================================
# [ ] Le tre funzioni Regola 45 (top_k, decidi_con_soglia, precision_su_k) sono
#     scritte da me e passano i mini-esercizi di verifica
# [ ] So dire a memoria: perché dot = coseno su norme 1
# [ ] So dire a memoria: cosa cambia al denominatore tra precision@k e recall@k
# [ ] So dire a memoria: la regola "cifre e codici → match esatto"
# [ ] Quiz di verifica ≥ 70%, voto primo tentativo nel diario
# [ ] match_utils.py creato con assert verdi
# [ ] Voto difficoltà 1-10 comunicato al mentor


# =============================================================================
# SOLUZIONI
# =============================================================================
#
# ----- QUIZ D'INGRESSO -----
# Q1: (1, 384) — embedda restituisce SEMPRE una matrice, una riga per testo.
# Q2: Vero. coseno = dot/(norma·norma); con norme = 1 resta dot. È la
#     scorciatoia della Sez. 1.
# Q3: confonde POSIZIONE (0..29) con colonna id (1..30): id==0 non esiste
#     (DataFrame vuoto) e l'ultima riga (id 30) non viene mai presa. Per la
#     posizione: corpus.iloc[i].
# Q4: token = pezzo che il modello legge; sottoparola = frammento di parola
#     (un token può essere una parola intera o un pezzo con ##).
# Q5: np.linalg.norm(q)
# Q6: 2/3 ≈ 0.67
# Q7: Falso. Stessa dimensione ≠ stesso spazio: 384 coordinate di modelli
#     diversi non sono confrontabili (contratto: chiave modello_minilm).
# Q8: perché q non è normalizzata: con norme ≠ 1, E @ q NON è un coseno e può
#     superare 1. Serve normalizza=True (o q / np.linalg.norm(q)).
#
# ----- MINI-ESERCIZI (risposte brevi) -----
# 1.1: S è (30, 30); diagonale tutta 1.0 (ogni nota è identica a se stessa);
#      S simmetrica. TODO 4: np.argsort(-s0) e np.argsort(d0) risultano identici
#      ((... == ...).all() → True): su vettori a norma 1, euclidea e coseno
#      producono la STESSA classifica (distanza² = 2 − 2·coseno, verificato
#      su E[3] vs E[7]: 1.604118 da entrambe le parti).
# 1.2: (1, 384), (1, 384), (3, 384). Per la freccia singola: [0].
# 2.3: la prima riga ha id 1; id==0 → DataFrame vuoto; "posizioni / .loc o
#      .iloc con la posizione".
# 2.4: caricare con joblib.load(PERCORSO_CONTRATTO) — NON pickle (file scritto
#      con joblib.dump). Chiavi utili: forma_minilm / modello_minilm /
#      max_seq_length_minilm; chi decide la compatibilità è modello_minilm,
#      la forma da sola non basta (stessa dimensione ≠ stesso spazio).
# 3.2: errori bloccati a 0.70: 2 su 6 (nota 18 a 0.475, nota 20 a 0.627);
#      giusti persi: 7 su 24 (verificato 19/10/2026; tra cui nota 28 a 0.404,
#      nota 3 ≈0.65, nota 5 ≈0.64, nota 14 ≈0.69, nota 27 ≈0.67).
# 3.5: a 0.85 errori bloccati 6/6 ma giusti persi 20/24 (verificato 19/10/2026).
#      "Alzare la soglia finché non passa nessun errore" dà un motore che dice
#      "non lo so" a 5 query giuste su 6: corretto, ma inutile — il punto della
#      soglia è bilanciare i due mali, non azzerarne uno.
# 3.3: mostro entrambi i segnali con il loro nome e dichiaro "non lo so":
#      nessuno dei due supera la sua soglia; non esiste un vincitore tra due
#      strumenti che misurano cose diverse (categoria vs documento).
# 4.1: TODO 1 → 2/3 ≈ 0.667. TODO 2 → 1/3 ≈ 0.333: il denominatore è SEMPRE k,
#      altrimenti un motore che mostra 1 solo risultato giusto avrebbe
#      precision@k = 1.0 pur non rispondendo quasi mai. Il "non lo so" si
#      misura con la copertura (in quante query si risponde), non qui.
# 4.3: recall@3 = 2/9 ≈ 0.22: k=3 mostra solo 3 posti, le 9 buste non ci
#      stanno tutte — recall bassa è fisiologica con k piccolo.
# 4.4: precision@3 media ≈ 0.667; precision@1 = 0.80. Devono coincidere con la
#      pagella del 02b: stessa metrica, altra implementazione.
# 5.1: a) il pooling fa la media dei pezzi e il "non" pesa pochissimo
#      b) ricerca a parole esatte (full-text); lì la parola "non" È il significato
#      c) il significato emerge dal tema complessivo, non da singole parole critiche
# 5.2: coseni ≈ 0.93 e ≈ 0.99; regola ibrida: "CF/IBAN/codici con match esatto,
#      titoli/contenuti con il coseno".
# 5.3: tokenizza("netto 1850 euro") → ["netto", "euro"]: le cifre spariscono
#      (RE_TOKEN prende solo lettere); in TF-IDF le cifre non esistono come feature.
# 5.4: la frase lunga si avvicina di più: il pooling media più token e il
#      contesto "stipendio/trattenute" spinge il vettore verso il mondo paghe.
# 5.5: a) SEMANTICO  b) ESATTO  c) ESATTO (o entrambi: esatto per il "non",
#      semantico per il tema)  d) ENTRAMBI (coseno sui contenuti + esatto sui
#      codici quando ci sono)
# 6.1: 10_000_000 × 384 × 4 byte = 15,36 miliardi di byte ≈ 15,4 GB
# 6.2: a) coseno, top-k, soglia, precision@k  b) dove vivono i vettori
#      (servizio/indice invece di RAM) e chi fa la matmul (indice ANN
#      approssimato invece di NumPy esatto)
#
# ----- QUIZ DI VERIFICA -----
# V1: (30,) — s[7] è il coseno tra la query e la nota in posizione 7.
# V2: Falso: il segno meno rovescia l'ordine → i 5 punteggi più ALTI.
# V3: manca il meno: np.argsort(punteggi) ordina dal PEGGIORE. Corretto:
#     np.argsort(-punteggi).
# V4: precision@k divide per k (quanti ne ho mostrati); recall@k divide per
#     TUTTI i pertinenti esistenti nel corpus.
# V5: v[1] >= soglia
# V6: precision@2 = 2/2 = 1.0; precision@4 = 3/4 = 0.75
# V7: i CF si confrontano con il MATCH ESATTO, non con il coseno: il modello
#     dà ~0.99 a due CF di persone diverse (Sez. 5.2). Corretto:
#     stessa_persona = cf_a.strip().upper() == cf_b.strip().upper()
# V8: Vero: soglia più alta → più vicini scartati → più liste vuote → più
#     "non lo so" (e meno falsi positivi).
# V9: gli indici di argsort sono POSIZIONI (0..29), la colonna id parte da 1:
#     id==0 è vuoto e si perde l'ultima nota. Corretto: note.loc[i, "testo"]
#     (o note.iloc[i]).
# V10: (Feynman — valuta: menziona che il vicino "meno lontano" può essere
#      comunque lontano; che un "non lo so" manda il caso a un umano invece di
#      archiviare sbagliato; che in produzione l'errore costa più del silenzio.)
#
# ----- ESERCIZI (versioni di riferimento) -----
#
# E1:
#   def cerca_veloce(query, E, testi, modello, k=3):
#       q = embedda([query], modello, normalizza=True)[0]   # (384,) norma 1
#       punteggi = E @ q                                    # (30,) coseni
#       return top_k(punteggi, k)                           # la TUA funzione
#
# E2: bug 3 (il crash dell'Atto 2): note[note["id"] == i] confonde POSIZIONE e
#     colonna id (#68): con la classifica completa prima o poi arriva i=0 →
#     id 0 non esiste → DataFrame vuoto → .iloc[0] → IndexError. Nell'Atto 1
#     NON esplode mai: gli indici peggiori sono [16, 7, 19] e gli id 16/7/19
#     esistono — il bug si nasconde e STAMPA LA RIGA SBAGLIATA (quella con
#     id = i, cioè la nota in posizione i−1): coppie testo/punteggio
#     disallineate. Silenzioso e sfasato: il peggior tipo di bug.
#     bug 2: argsort senza meno → ordine CRESCENTE → i 3 punteggi più BASSI
#     (0.826, 0.907, 0.916 sono i coseni peggiori!) presentati come i migliori.
#     bug 1: embedda senza normalizza=True → q non a norma 1 → E @ q non sono
#     coseni: per questo punteggi.max() = 2.457 > 1 (l'indizio dell'Atto 1).
#     Corretto:
#       q = embedda(["prospetto paga"], modello, normalizza=True)[0]
#       punteggi = E @ q
#       ordine = np.argsort(-punteggi)[:3]
#       for i in ordine:
#           print(note.loc[i, "testo"], round(float(punteggi[i]), 3))
#     Morale: l'IndexError è stato una FORTUNA (ha smascherato il bug 3); i bug
#     1 e 2 non alzano mai la mano — li trovi solo guardando i numeri (max > 1)
#     e il contenuto (fuori tema). Prima regola del debug: fidati degli errori,
#     diffida dei silenzi.
#
# E3: come testo_utils.coseno: dot/(norme) con guardia 0.0 su norma zero.
#
# E4: i vicini TF-IDF premiano le PAROLE ESATTE ("prospetto", "paga"): trova
#     documenti che le contengono, ma manca sinonimi ("cedolino"). Il semantico
#     trova i sinonimi ma può portare "altro" a tema soldi. Due righelli diversi.
#
# E6: (pipeline a memoria — confronta con Sez. 2-4). Tabellina attesa misurata
#     il 19/10/2026 (±0.01):
#       query 1 (busta paga…): vicini 1 busta_paga 0.708 · 29 busta_paga 0.608 ·
#         3 busta_paga 0.572 → precision@3 = 1.0; sopra soglia: 1; esito: risposta
#       query 2 (redditi…): 22 cu 0.873 · 9 cu 0.868 · 6 cu 0.657
#         → precision@3 = 1.0; sopra soglia: 2; esito: risposta
#       query 3 (estratto conto…): 27 estratto_conto 0.479 · 14 estratto_conto
#         0.426 · 11 estratto_conto 0.321 → precision@3 = 1.0; sopra soglia: 0;
#         esito: non_lo_so
#       query 4 (atto notarile): 4 busta_paga 0.298 · 28 altro 0.294 · 18 altro
#         0.286 → precision@3 = 2/3 ≈ 0.667; sopra soglia: 0; esito: non_lo_so
#     precision@3 media sul ranking: ≈ 0.917.
#     Le due righe che insegnano: la 3 (ranking PERFETTO ma motore muto —
#     precision e soglia misurano cose diverse: qui la soglia 0.70 è troppo
#     severa per le query su estratto conto, vedi Mini 3.4) e la 4 (il
#     "non lo so" è la risposta GIUSTA per una query fuori corpus: meglio muto
#     che sbagliato — il maître onesto della Sez. 3).
#
# E7 (riferimento):
#   def scheda_ricerca(query, E, note, modello, k, soglia):
#       q = embedda([query], modello, normalizza=True)[0]
#       punteggi = E @ q
#       candidati = top_k(punteggi, k)                        # prima della soglia
#       ranking = sorted(candidati, key=lambda c: c[1], reverse=True)
#       sopra_soglia = decidi_con_soglia(ranking, soglia)
#       if sopra_soglia:
#           tipi = [note.loc[i, "tipo"] for i, _ in sopra_soglia]
#           moda = max(set(tipi), key=tipi.count)
#           rischio = note.loc[sopra_soglia[0][0], "tipo"] != moda
#       else:
#           rischio = False
#       return {"candidati": candidati, "ranking": ranking,
#               "sopra_soglia": sopra_soglia, "soglia": soglia,
#               "esito": "risposta" if sopra_soglia else "non_lo_so",
#               "falso_positivo_semantico_rischio": rischio}
#
# E8: il pezzo che DECIDE è il classificatore (la maschera): restringe lo
#     spazio di ricerca PRIMA del coseno; coseno e soglia scelgono solo dentro
#     quel sottoinsieme. (È il pattern "filtro a monte" della Sez. 5.4.)
#
# E9: ordine: codifica di tutti i documenti (una volta) → codifica della query
#     → top-k sul corpus → re-rank dei candidati → soglia e risposta.
#     Il bi-encoder codifica ogni testo DA SOLO → i punti non dipendono dalla
#     query → si pre-calcolano. Il cross-encoder legge la COPPIA → il punteggio
#     dipende da entrambi → niente da pre-calcolare.
#     La nota 13: il cross-encoder vede le interazioni (es. "estratto conto" vs
#     "busta paga" come unità, i movimenti vs le voci stipendio) che il pooling
#     a media aveva appiattito.
#
# ----- PROGETTO (riferimento) -----
#   def match_esatto(valore_a, valore_b):
#       return str(valore_a).strip().upper() == str(valore_b).strip().upper()
#
#   def match_semantico(testo_a, testo_b, modello):
#       v = embedda([testo_a, testo_b], modello, normalizza=True)
#       return float(v[0] @ v[1])
#
#   def verifica_coppia_documenti(doc_a, doc_b, modello, soglia=0.50):
#       cf_uguali = match_esatto(doc_a["cf"], doc_b["cf"])
#       sim = match_semantico(doc_a["titolo"], doc_b["titolo"], modello)
#       sopra = sim >= soglia
#       if not cf_uguali:
#           esito = "da_rivedere" if sopra else "diversi"   # l'esatto vince: mai "coerenti"
#       else:
#           esito = "coerenti" if sopra else "da_rivedere"
#       return {"cf_uguali": cf_uguali, "coseno_titoli": sim,
#               "sopra_soglia": sopra, "esito": esito}
# =============================================================================
# FINE DEL CAPITOLO 03
# =============================================================================
