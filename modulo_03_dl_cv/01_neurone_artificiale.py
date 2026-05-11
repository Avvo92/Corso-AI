"""
============================================================================
MODULO 3 (DL & CV) - CAPITOLO 01
"Neurone artificiale da zero": un neurone = un layer Dense con h=1 + attivazione
============================================================================

----------------------------------------------------------------------------
DA DOVE ARRIVI (cap.02 Ponte Matematico)
----------------------------------------------------------------------------
Nel cap.02 Ponte hai imparato che, dato un batch X di pratiche:

    X.shape == (N, d)            # N pratiche, d feature
    w.shape == (d,)              # 1 vettore di pesi (1 "regressore")
    z = X @ w + b                # shape (N,)  -> 1 punteggio per pratica

E che generalizzando con W matrice:

    W.shape == (d, h)            # h "neuroni" in parallelo
    Z = X @ W + b                # shape (N, h) -> h punteggi per pratica

In questo capitolo "smontiamo" lo stesso oggetto da un'altra angolazione: il
NEURONE come unita' atomica di una rete. Un neurone artificiale e':

    1) un dot product fra input e pesi          -> X @ w + b
    2) seguito da una FUNZIONE DI ATTIVAZIONE   -> sigma(X @ w + b)

Per chi viene dal web dev: un neurone e' una "funzione" che accetta un
vettore (le feature di una pratica), somma in modo pesato i suoi input
(come una media pesata) e poi decide con una "soglia morbida" (0..1).

Concettualmente:
    - PUNTEGGIO (logit) = X @ w + b           <- numero da -inf a +inf
    - PROBABILITA'      = sigmoid(punteggio)  <- numero da 0 a 1

Logit != probabilita'. La probabilita' la fa l'ATTIVAZIONE (sigmoid o
softmax). Questa distinzione era una delle Lacune Quiz aperte (#28).

----------------------------------------------------------------------------
COSA PORTI VIA DA QUESTO CAPITOLO (Definition of Done)
----------------------------------------------------------------------------
Alla fine sai rispondere "in 1 riga" a queste 5 domande:

  1) Cosa fanno (esattamente, in ordine) i 2 passi di un neurone?     -> Sez. 1
  2) Differenza fra logit e probabilita'?                              -> Sez. 1
  3) Quando uso sigmoid, ReLU, tanh? E perche'?                        -> Sez. 2
  4) Come faccio il forward di UN neurone su 1000 pratiche
     SENZA loop Python?                                                -> Sez. 3
  5) Il neurone artificiale e' un caso particolare del layer Dense
     del Ponte cap.02? Spiega.                                         -> E7

Hai anche scritto 3 funzioni riutilizzabili: sigmoid, neurone, neurone_batch.
E hai dimostrato (mini-progetto) che un neurone scritto a mano riproduce
la LogisticRegression del Modulo 2 cap.04.

----------------------------------------------------------------------------
MAPPA DEL CAPITOLO
----------------------------------------------------------------------------
   *  PRONTUARIO TRANELLI NEURONE        [N1] - [N6]
   *  QUIZ D'INGRESSO                    Q1 - Q6     (cerniera cap.02 Ponte)
   *  RINFORZO Lacuna #23                (shape (N,) vs (N, 1)) + mini-esercizio
   *  RINFORZO Lacuna #24                (tupla (0.1,) vs scalare 0.1) + mini-esercizio
   *  RINFORZO Lacuna #26                (perche' BLAS batte il loop) + mini-esercizio
   *  RINFORZO Lacuna #28                (logit vs probabilita') + mini-esercizio
   *  RINFORZO Lacuna #29 (re-check)     (X[i] vs X[i:i+1]) + mini-esercizio
   *  RIPASSO 5 PUNTI cap.02 Ponte       R1 - R5     (mini 2-4 righe)
   *  SEZIONE 1  Il neurone come "if morbido"     1.1 - 1.3
   *  SEZIONE 2  Funzioni di attivazione          2.1 - 2.2
   *  SEZIONE 3  Forward su batch reale (CSV M2)  3.1 - 3.2
   *  QUIZ DI VERIFICA                    V1 - V8
   *  ESERCIZI FINALI                     E1 - E7
                                          (colloquio / refactor stilistico
                                           / refactor logica / debug
                                           / retrieval / interleaving
                                           / RECALL CROSS-MODULO)
   *  MINI-PROGETTO                       neurone_vs_logreg
   *  CHECKPOINT FINALE                   C1 - C4
   *  SOLUZIONI QUIZ                      in fondo

----------------------------------------------------------------------------
COME USARE QUESTO FILE (regola del corso)
----------------------------------------------------------------------------
   1. Leggi in ORDINE. La sezione N usa la sezione N-1.
   2. Per ogni TODO scrivi nel blocco "TUO CODICE" (non cancellare lo
      scaffold, lascialo come traccia).
   3. Quando vuoi una valutazione: "valuta cap.01 M3 sezione X.Y"
   4. Se ti blocchi >10 min: "sono bloccato sezione X" -> ti do solo
      l'IDEA, mai la soluzione.
   5. Niente LaTeX (preferenza tua): le formule sono in PAROLE + codice.
   6. Hardware: tutto su CPU + NumPy + Matplotlib. PyTorch arriva al cap.04.
"""

import os
from typing import Callable
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy.typing import NDArray


# ==========================================================================
# PRONTUARIO TRANELLI NEURONE - leggilo PRIMA di iniziare (5 minuti)
# ==========================================================================
# Sono i tranelli specifici dei NEURONI. Quelli sui vettori (T1-T10) e sulle
# matrici (M1-M8) li trovi nel Ponte cap.01-02: ti restano validi anche qui.
#
# [N1] UN NEURONE = 2 PASSI, NON 1.
#      Passo 1: z = x @ w + b           (combinazione lineare = logit)
#      Passo 2: a = sigma(z)            (attivazione = decisione/probabilita')
#      Se salti il passo 2, non hai un neurone: hai una regressione lineare.
#
# [N2] LOGIT vs PROBABILITA' - non sono la stessa cosa!
#      logit = z          -> numero da -inf a +inf
#      prob  = sigmoid(z) -> numero fra 0 e 1
#      In sklearn: model.decision_function(X) -> logit
#                  model.predict_proba(X)     -> prob
#      Questa era la Lacuna Quiz #28 (cap.02 Ponte). Ora la chiudiamo.
#
# [N3] SIGMOID per binario, SOFTMAX per multi-classe.
#      sigmoid(z) = 1 / (1 + exp(-z))     <- 1 numero in input, 1 in output
#      softmax(z) (vettore) -> vettore di probabilita' che sommano a 1
#      Per neurone "1 classe positiva vs 1 negativa" -> sigmoid.
#
# [N4] RELU per i layer NASCOSTI delle reti neurali (M3 cap.02+).
#      relu(z) = max(0, z)   <- "filtro che lascia passare solo i positivi"
#      In output finale di un classificatore quasi mai. La sigmoid/softmax
#      stanno solo all'ULTIMO layer.
#
# [N5] INIZIALIZZAZIONE PESI: piccoli random, NON zero, NON troppo grandi.
#      np.zeros(d) -> tutti i neuroni imparano la stessa cosa (rotto).
#      np.random.standard_normal(d) * 0.01 -> ok per ora.
#      In M3 cap.04+ vedremo "Xavier" e "He" init: per ora basta sapere
#      che "tutti zero" e' bug, "casuali piccoli" e' ok.
#
# [N6] FORWARD BATCH = stesso del Ponte cap.02:
#      Z = X @ w + b              shape (N,)
#      A = sigmoid(Z)             shape (N,)   element-wise
#      Le attivazioni si applicano element-wise al vettore di logit.
#      NIENTE LOOP. Una sola operazione per (potenzialmente) milioni di righe.


# ==========================================================================
# QUIZ D'INGRESSO - cerniera cap.02 Ponte -> cap.01 M3
# ==========================================================================
# Rispondi nei commenti sotto ogni domanda. Non barare scorrendo in fondo.
# Soluzioni a fine file.
#
# Nota: questo quiz ricontrolla "a freddo" le 5 lacune ancora aperte dal
# cap.02 Ponte (#23, #24, #26, #27, #28) + #29 in re-check.

# Q1) [Lacuna #23 - re-check] Hai X di shape (200, 7) e w di shape (7,).
#     Che shape ha "X @ w"? E "X @ w.reshape(-1, 1)"?
#     Una delle due e' 1D, l'altra 2D: spiega quale e perche'.
# TUA RISPOSTA: la prima => (200, ); la seconda => (200, 1);
# Il perchè è che il Dot product di una matrice (N, d) per un vettore (d, ) restituisce un vettore di shape (N, ), mentre se lo stesso vettore
# lo trasformiamo tramite reshape in una matrice  (d, 1) usando .reshape(-1, 1) a qual punto avremo un dot product tra due matrici, che
# restituirà una matrice di shape (N, 1).

# Q2) [Lacuna #28 - re-check] Hai un neurone con w (7,), b scalare e
#     applichi sigmoid in fondo. Su un batch X (200, 7) ottieni:
#         z = X @ w + b
#         a = sigmoid(z)
#     Quale dei due (z o a) e' "probabilita' di alterato"?
#     L'altro come si chiama?
# TUA RISPOSTA:
# a è la probabilità, il secondo è un logit grezzo

# Q3) [Trova l'errore - Lacuna #24 re-check]
#     Questo codice "gira" ma e' sbagliato come stile. Perche'?
#         z = X @ w + (0.1,)
#     Qual e' la versione corretta? E cosa stampa "type((0.1,))"?
# TUA RISPOSTA:
# la versione corretta è => z = X @ w + 0.1. Nonostante tutto numpy farebbe cmq bradcasting e matematicamente l'operazione non cambierebbe, ma
# stiamo dando una tupla come valore di b senza alcun motivo. Infatti, type((0.1,)) darebbe "tuple". 

# Q4) [Lacuna #26 - re-check] Da' DUE motivi DIVERSI per cui:
#         z = X @ w + b
#     e' molto piu' veloce di:
#         z = np.array([np.dot(X[i], w) + b for i in range(len(X))])
#     (uno tecnico-NumPy, uno legato all'interprete Python).
# TUA RISPOSTA:
# 1) z = X@ w + b è un operazione vettorizzata eseguita in C, mentre il secondo è loop python (dalle 50 alle 1000 volte più lento);
# 2) Esssendo un linguaggio interpretato, il codice python deve essere preprocessato prima di essere eseguito, e questo fa diminuire l'efficienza.

# Q5) [Lacuna #29 - re-check] Hai X.shape == (100, 7).
#     Che shape ha X[5]? E X[5:6]? Quale dei due passi a:
#         clf.predict_proba(?)
#     di sklearn senza ottenere errore?
# TUA RISPOSTA: Il primo restituisce un vettore di shape (7, ), secondo ottenuto tramite slicing restituisce una matrice di shape (1, 7). Predict proba accetta in input matrici di shape (1, n), quindi il secondo è quello giusto.
print("Prova 1")
X = np.random.randn(100, 7)
print(X[5])
print(X[5:6])

# Q6) [Feynman - Lacuna #27 re-check] Spiega cos'e' un NEURONE artificiale
#     a un collega web dev che non ha mai sentito parlare di reti neurali.
#     VINCOLO STRETTO: niente "feature", niente "logit", niente "regressione",
#     niente "matrice", niente "sigmoid", niente "vettore". SOLO analogia
#     dal mondo reale (cucina, sport, ufficio...). Massimo 5 righe.
# TUA RISPOSTA:
# un neurone è uno specialista che si occupa di tirare fuori un punteggio da un insieme di valori assegnati a diversi aspetti di qualcosa. 
# Ad esempio, un neurone e un cuoco che, da un insieme di ingredienti, tira fuori un punteggio riguardo a "Primo piatto". Se gli ingredienti sono adatti a fare un primo piatto, il punteggio sarà alto, altrimenti sarà basso. 


# ==========================================================================
# RINFORZO Lacuna #23 - shape (N,) vs (N, 1) in NumPy
# ==========================================================================
# Nel Quiz V1 cap.02 Ponte hai risposto "(100, 1)" mentre la risposta era
# "(100,)". E' un punto chirurgico: se sbagli qui in M3, sklearn/PyTorch ti
# urlano "shape mismatch" e perdi 30 minuti a debuggare. Verifichiamolo:

def _demo_lacuna_23() -> None:
    """Mostra concretamente la differenza fra (N,) e (N, 1)."""
    X = np.array([[1.0, 2.0, 3.0],
                  [4.0, 5.0, 6.0]])     # (2, 3)
    w = np.array([0.5, 1.0, -1.0])      # (3,)

    z_1d = X @ w                         # (2,)   <- caso "vettore"
    z_2d = X @ w.reshape(-1, 1)          # (2, 1) <- caso "matrice colonna"

    print("z_1d.shape:", z_1d.shape, "ndim:", z_1d.ndim)
    print("z_2d.shape:", z_2d.shape, "ndim:", z_2d.ndim)
    print("Stessi numeri? ", np.allclose(z_1d, z_2d.ravel()))
    # Contengono gli STESSI valori, ma uno e' 1D e l'altro e' 2D.
    # Per sklearn classifier: di solito (N,). Per layer Dense con W (d, h)
    # con h>=1: (N, h). Quando h=1 alcune librerie restituiscono (N,) altre
    # (N, 1) - controllare sempre con .shape PRIMA di usare l'output.


# Regola pratica:
#   - X (N, d) @ w (d,)        -> (N,)   = vettore 1D di logit
#   - X (N, d) @ W (d, 1)      -> (N, 1) = matrice colonna 2D di logit
#   - X (N, d) @ W (d, h)      -> (N, h) = matrice 2D, una colonna per neurone

# --- Mini-esercizio [RINFORZO #23] (2-4 righe) ---
# Con X di shape (6, 3) e w di shape (3,), calcola z1 = X @ w e z2 = X @ w.reshape(-1, 1).
# Stampa z1.shape, z2.shape e verifica con np.allclose(z1, z2.ravel()) che i numeri coincidano.
# TUO CODICE:


# ==========================================================================
# RINFORZO Lacuna #24 - tupla accidentale "(0.1,)" vs scalare 0.1
# ==========================================================================
# Nel Quiz V4 cap.02 Ponte hai detto che "X @ w + (0.1,)" da' TypeError.
# In realta' NumPy lo accetta (broadcast): la tupla "(0.1,)" diventa un
# array (1,) e si somma element-wise. Il problema NON e' la sintassi, e' la
# *intenzione*: chi legge il codice si chiede "perche' una tupla?".
#
# Mini-test dimostrativo:

def _demo_lacuna_24() -> None:
    """Confronta scalare vs tupla accidentale come bias."""
    X = np.array([[1.0, 2.0], [3.0, 4.0]])
    w = np.array([0.5, -0.5])

    z_scalar = X @ w + 0.1               # bias scalare: ok, leggibile
    z_tuple = X @ w + (0.1,)             # bias "tupla": stesso risultato, illeggibile
    z_array = X @ w + np.array([0.1])    # versione "esplicita" della tupla

    print("z_scalar:", z_scalar, type((0.1,)))   # <class 'tuple'>
    print("z_tuple :", z_tuple)
    print("z_array :", z_array)
    print("Tutti uguali?", np.allclose(z_scalar, z_tuple) and
          np.allclose(z_scalar, z_array))


# Regola pratica:
#   - bias scalare: scrivi "+ b" (o "+ 0.1").
#   - bias vettoriale (un valore per neurone): scrivi "+ b_vec" con
#     b_vec = np.array([...])  esplicito.
#   - mai virgole "decorative" a fine espressione: creano tuple involontarie.

# --- Mini-esercizio [RINFORZO #24] (2-4 righe) ---
# (a) In una riga: cosa stampa print(type((0.05,))) ?
# (b) Scrivi z_ok = X @ w + 0.05 con X = np.ones((2, 3)), w = np.ones(3) (NO tuple come bias).
# TUO CODICE:
#(a) => tuple
print("\nMini-esercizio Rinforzo 24\n")

X = np.ones((2, 3))
w = np.ones(3)
b = 0.05
z_ok = X @ w + b

# ==========================================================================
# RINFORZO Lacuna #26 - perche' BLAS batte il loop Python (DUE motivi)
# ==========================================================================
# Nel Quiz V6 cap.02 Ponte hai dato 1 motivo (esecuzione in C). Ce ne sono
# almeno 3, e capirli serve quando si parla di GPU in M3 cap.04.
#
# Motivo 1 - "Compiled vs Interpreted":
#   - "X @ w" chiama una funzione gia' compilata in C (BLAS/MKL/OpenBLAS).
#   - Il loop Python "for i in range(N): np.dot(X[i], w)" passa dal
#     bytecode dell'interprete a ogni iterazione: overhead enorme.
#
# Motivo 2 - "Vettorizzazione SIMD / multi-thread":
#   - BLAS usa istruzioni SIMD (AVX/AVX2/AVX-512) che eseguono 4-16
#     operazioni float per ciclo di clock. Il loop Python e' single-thread,
#     1 op per iterazione + tutto l'overhead del dispatch.
#
# Motivo 3 - "Cache / memoria contigua":
#   - X (N, d) e' un blocco contiguo in memoria. BLAS legge a colpi di
#     cache line (64 byte = 8 float64). Il loop Python tocca oggetti
#     Python che vivono SPARSI nello heap -> cache miss continui.

# --- Mini-esercizio [RINFORZO #26] (solo parole, poi confronti col benchmark) ---
# Scrivi in DUE bullet (frasi brevi) due motivi DIVERSI tra loro per cui
# `X @ w + b` batte `for i in range(N): np.dot(X[i], w) + b`.
#   - Motivo A (tecnico sulla libreria NumPy/C): Invece di chiara una funzione scritta in C, Python essendo un liguaggio interpretato passa per l'interprete ad ogni iterazione: overhead molto grande, perdita di efficenza.
#   - Motivo B (tecnico sul loop Python / memoria): le operazioni vettorizzaate effeettuate su blocchi contigui di memeoria sfruttano la vicinanza della info in memoria: con Python questo non avviene, perchè gli oggetti python vivono sparsi nell'heap.
# Dopo aver eseguito _benchmark_loop_vs_blas() nel __main__, annota lo speedup stampato.

# Verifichiamo con un benchmark mini (deve girare in <1 secondo):

def _benchmark_loop_vs_blas(n: int = 100_000, d: int = 50) -> None:
    """Confronto rapido: loop Python vs BLAS."""
    import time
    rng = np.random.default_rng(42)
    X = rng.standard_normal((n, d))
    w = rng.standard_normal(d)
    b = 0.1

    # versione lenta
    t0 = time.perf_counter()
    z_slow = np.array([np.dot(X[i], w) + b for i in range(n)])
    t1 = time.perf_counter()

    # versione veloce
    t2 = time.perf_counter()
    z_fast = X @ w + b
    t3 = time.perf_counter()

    speedup = (t1 - t0) / max(t3 - t2, 1e-9)
    print(f"loop Python: {(t1 - t0)*1000:7.2f} ms   shape: {z_slow.shape}")
    print(f"BLAS @     : {(t3 - t2)*1000:7.2f} ms   shape: {z_fast.shape}")
    print(f"speedup    : ~{speedup:.0f}x")
    assert np.allclose(z_slow, z_fast), "i due risultati DEVONO coincidere"


# ==========================================================================
# RINFORZO Lacuna #28 - logit vs probabilita'
# ==========================================================================
# Nel Checkpoint C2 cap.02 Ponte hai descritto l'output di un layer Dense
# come "probabilita'". E' un errore concettuale rischioso: l'output e' un
# PUNTEGGIO (logit), non una probabilita'. La probabilita' arriva DOPO,
# applicando un'attivazione (sigmoid per binario, softmax per multi-classe).
#
# Tabella decisionale:
#
#   COSA HAI?                     CHE COS'E'?           COME LO RICONOSCI?
#   -------------------------------------------------------------------------
#   z = X @ w + b                 LOGIT (punteggio)     puo' valere -1000, +1000
#   a = 1 / (1 + exp(-z))         PROBABILITA' [0, 1]   sempre fra 0 e 1
#   a = softmax(z) (vettore)      VETTORE PROB. [0, 1]  somma a 1.0
#
# Esempio mini:

def _demo_lacuna_28() -> None:
    """Logit vs probabilita' fianco a fianco."""
    z = np.array([-2.0, -0.5, 0.0, 0.7, 3.0])
    p = 1 / (1 + np.exp(-z))
    print("logit z:", z)
    print("prob  a:", np.round(p, 3))
    print("note   : z>0 <-> p>0.5; z=0 <-> p=0.5; z e' senza limiti, p in [0,1]")
    
print(_demo_lacuna_28())


# Regola pratica:
#   - "il modello pensa al 73% che sia alterato" -> stai parlando di p, non z.
#   - per "ordinare" pratiche da piu' a meno alterate: usare z basta
#     (sigmoid e' monotona, non cambia l'ordine).
#   - per "soglia umana" (es. >= 0.7) -> usare p, non z.

# --- Mini-esercizio [RINFORZO #28] (2-4 righe + commento) ---
# Dato z_test = np.array([-100.0, 0.0, 100.0]), calcola p_test = 1 / (1 + np.exp(-z_test))
# (usa np.clip(z_test, -500, 500) prima dell'exp se vuoi evitare warning).
# Stampa z_test e np.round(p_test, 6). In commento: qual e' il logit e qual e' la probabilita'?
# TUO CODICE:
print("\nMini-esercizio Rinforzo 28\n")
z_test = np.clip(np.array([-100.0, 0.0, 100.0]), -500, 500)
p_test = 1 / (1 + np.exp(-z_test))
print(z_test)
print(np.round(p_test, 6))
# z_test è l'array dei logit, mentre p_test sono le probabilità


# ==========================================================================
# RINFORZO Lacuna #29 (re-check) - X[i] (1D) vs X[i:i+1] (2D)
# ==========================================================================
# Nel Checkpoint C3 cap.02 Ponte hai detto che X[5:6] ha shape (1, 1) -
# in realta' e' (1, d) (la colonna "righe" si conserva). Ricontrolliamo
# in piedi prima di farla diventare un bug in M3.

def _demo_lacuna_29() -> None:
    rng = np.random.default_rng(0)
    X = rng.standard_normal((100, 7))
    print("X.shape       :", X.shape)
    print("X[5].shape    :", X[5].shape)        # (7,)   1D
    print("X[5:6].shape  :", X[5:6].shape)      # (1, 7) 2D
    print("X[[5]].shape  :", X[[5]].shape)      # (1, 7) 2D (fancy indexing)
    print("X[5, :].shape :", X[5, :].shape)     # (7,)   1D


# Quando serve 2D? Per sklearn:
#   clf.predict_proba(X[5])      <- ERRORE: serve 2D
#   clf.predict_proba(X[5:6])    <- OK
#   clf.predict_proba(X[[5]])    <- OK
#   clf.predict_proba(X[5].reshape(1, -1))  <- OK

# --- Mini-esercizio [RINFORZO #29] (2-4 righe) ---
# Crea X = np.arange(40.0).reshape(8, 5). Stampa shape di X[3], X[3:4], X[[3]].
# Scrivi una variabile riga_2d = ... che seleziona solo la riga indice 3 con shape (1, 5).
# TUO CODICE:
print("\nMini-esercizio Rinforzo 29\n")
X = np.arange(40.0).reshape(8, 5)
print(f"X[3]   => {X[3].shape}")
print(f"X[3:4] => {X[3:4].shape}")
print(f"X[[3]] => {X[[3]].shape}")
riga_2d = X[[3]]
print(riga_2d)

# ==========================================================================
# RIPASSO 5 PUNTI cap.02 Ponte (mini-esercizi 2-4 righe ciascuno)
# ==========================================================================
# Prima di passare al neurone, fissa i 5 pilastri del cap.02 Ponte con 5
# micro-esercizi di "retrieval practice" (Regola 8 + Regola 15). Sono
# 2-4 righe ciascuno: scrivi senza guardare il cap.02.

# R1) MATRICE = BATCH DI PRATICHE
# Crea una matrice X di shape (3, 4) di interi qualsiasi. Stampa: shape,
# dtype, X[0] (la prima pratica) e X[:, 0] (la prima feature di tutte
# le pratiche).
# TUO CODICE:
print("\nMini-esercizio R1\n")
X = np.random.randint(1, 40, size=(3, 4), dtype=np.int64)
print(f"Shape: {X.shape}")
print(f"Dtype: {X.dtype}")
print(f"Prima pratica: {X[0]}")
print(f"Prima feature: {X[:, 0]}")
print(X)


# R2) PRODOTTO MATRICE-VETTORE = N DOT PRODUCT IN PARALLELO
# Dato X (3, 4) random e w (4,) random, calcola z = X @ w. Verifica con
# un assert che z[i] == np.dot(X[i], w) per ogni i (usa np.allclose
# sull'array intero, NIENTE for-loop di assert).
# TUO CODICE:
print("\nMini-esercizio R2\n")
X = np.random.randn(3, 4)
w = np.random.randn(4)
z = X @ w
assert np.allclose(z, np.dot(X, w)), "i valori devono coincidere"


# R3) BROADCASTING DEL BIAS
# Dato z di shape (3,) e b scalare = 0.5, calcola "z_pre = z + b". Cosa
# succede a b durante la somma? Stampa la shape di z_pre e di un nuovo
# z2_pre = z + np.array([0.1, 0.2, 0.3]) (bias vettoriale).
# TUO CODICE:
z = np.arange(3)
b = 0.5
z_pre = z + b
# durante l'operazione di somma di z e b, dove z ha shape (3, ), e b è uno scalare, viene fatto il broadcasting di b in un vettore di shape (3, ), dove ogni elemento è uguale al valore scalare di b. In questo modo si ottiene una somma element-wise (operazione vettorizzata) di agni elemento del vettore z con l'elemento corrispondente (posizionato allo stesso indice) del vettore b.
z2_pre = z + np.array([0.1, 0.2, 0.3])

print(z_pre.shape)
print(z2_pre.shape)


# R4) LAYER DENSE = h REGRESSIONI IN PARALLELO  [Lacuna #28 ricontrollo]
# Dato X (3, 4) e W (4, 2) random, calcola Z = X @ W. Che shape ha Z?
# Cosa rappresenta ogni colonna di Z? E ogni riga? (commentalo in 1 riga)
# TUO CODICE:
print("\nMini-esercizio R4\n")
rng = np.random.default_rng(42)
X = rng.random(12).reshape(3, 4)
W = rng.random(8).reshape(4, 2)
Z = X @ W
# Nel nostro dominio, ogni colonna di Z rappresenta una feature differente di una pratica (es. delta netto-lordo), mentre ogni riga rappresenta una pratica differente (la quale è di fatto costituita da un vettore di feature).
# nel dot product vettorizzato tra X di shape (N, d) e di W di shape (d, h), come risultato di otterrà una matrice di risultadi di shape (N, h).
print(Z.shape)

# R5) SHAPE 1D vs 2D  [Lacuna #29 ricontrollo]
# Data X (10, 3) random, stampa la shape di:
#   X[2]      <- riga 2
#   X[2:3]    <- "riga 2" come matrice 1xN
#   X[2, :]   <- equivalente a X[2]?
# Quale dei tre passi a "clf.predict_proba(...)" di sklearn senza errore?
# TUO CODICE:
print("\nMini-esercizio R5\n")
X = np.random.randn(10, 3)
print(X[2].shape)
print(X[2:3].shape)
print(X[2, :].shape)

# predict_proba necessita in una matrice con shape (1, N), quindi bisogna passare valore tramite slicing tipo X[r:r+1]


# ==========================================================================
# SEZIONE 1 - IL NEURONE COME "IF MORBIDO"
# ==========================================================================

# ---------------------- ANALOGIA --------------------------------------------
# Immagina di dover decidere se un cliente e' "buono" o "rischioso" per
# concedergli un mutuo. NON usi una sola variabile (es. "stipendio") ma
# ne pesi varie:
#
#   - stipendio:           peso = +0.6   (piu' alto -> piu' buono)
#   - eta':                peso = +0.1   (piu' alto -> un po' piu' buono)
#   - rate gia' arretrate: peso = -1.5   (piu' alte -> molto peggio)
#   - puntualita' storico: peso = +0.9
#
# Per ogni cliente:
#   1) calcoli un PUNTEGGIO = somma pesata(features) + costante (bias)
#   2) passi il punteggio attraverso una "soglia morbida" che lo
#      schiaccia fra 0 e 1 (probabilita' di essere buono)
#
# Ecco. Hai appena descritto un NEURONE ARTIFICIALE.
# In codice:
#
#     z = w_stipendio * stipendio + w_eta * eta + ... + b   <- punteggio
#     prob_buono = sigmoid(z)                               <- "soglia morbida"
#
# La differenza con un "if" tradizionale (Java/PHP)?
#   - if classico: rigido, decide 0 oppure 1, taglio netto.
#   - neurone:     morbido, restituisce un numero fra 0 e 1
#                  (= "quanto sono sicuro?").
#
# Per il web dev: pensa a una "rule engine" dove ogni regola contribuisce
# con un peso, e alla fine c'e' un "soft threshold" invece di un boolean.

# ---------------------- TEORIA + CODICE -------------------------------------
# 1.1 - SIGMOID: la "soglia morbida"
#
#   sigmoid(z) = 1 / (1 + exp(-z))
#
# In parole:
#   - se z e' MOLTO negativo (-10) -> sigmoid(z) ~ 0.000045 (quasi 0)
#   - se z e' 0                    -> sigmoid(z) = 0.5      (incertezza max)
#   - se z e' MOLTO positivo (+10) -> sigmoid(z) ~ 0.99995  (quasi 1)
#
# Tre proprieta' che la rendono perfetta per "convertire un punteggio
# in una probabilita'":
#   (a) range [0, 1]
#   (b) monotona crescente (z piu' grande -> p piu' grande)
#   (c) liscia/derivabile (utile per backpropagation, M3 cap.03)


def sigmoid(z: NDArray[np.float64] | float) -> NDArray[np.float64] | float:
    """Sigmoid stabile numericamente (zero RuntimeWarning per |z| grandi).

    Formula: sigmoid(z) = 1 / (1 + exp(-z))
    Trick anti-overflow: clip dell'argomento di exp in [-500, +500].
    Per z fuori da quel range il valore di sigmoid e' gia' "saturato"
    a 0 o 1 con precisione float64, quindi clip-pare non cambia il
    risultato pratico ma evita warning di overflow.
    """
    z_arr = np.asarray(z, dtype=float)
    z_safe = np.clip(z_arr, -500.0, 500.0)
    out = 1.0 / (1.0 + np.exp(-z_safe))
    if np.isscalar(z) or out.ndim == 0:
        return float(out)
    return out


# 1.2 - IL NEURONE: forward su UNA pratica
# Un neurone e' una funzione "vettore -> scalare". Prende le feature di una
# pratica e restituisce 1 numero (probabilita').

def neurone(
    x: NDArray[np.float64],
    w: NDArray[np.float64],
    b: float,
) -> float:
    """Forward di UN neurone su UNA pratica (vettore di feature).

    Args:
        x: feature di una pratica, shape (d,)
        w: pesi del neurone,        shape (d,)
        b: bias scalare

    Returns:
        probabilita' (in [0, 1]) che la pratica sia di classe positiva.
    """
    if x.ndim != 1 or w.ndim != 1:
        raise ValueError("x e w devono essere vettori 1D")
    if x.shape[0] != w.shape[0]:
        raise ValueError(f"shape incompatibili: x{x.shape} vs w{w.shape}")
    z = float(x @ w + b)        # logit (punteggio)
    return float(sigmoid(z))    # probabilita'


def _esempio_neurone_singolo() -> None:
    """Forward di 1 pratica + 1 neurone."""
    x = np.array([1200.0, 30.0, 250.0, 180.0, 90.0])    # 5 feature
    w = np.array([+0.001, -0.05, +0.02, -0.03, +0.01])  # pesi finti
    b = -3.0
    p = neurone(x, w, b)
    print("pratica x:", x)
    print(f"prob_alterato (1 neurone): {p:.4f}")


# 1.3 - IL NEURONE IN BATCH: una sola operazione su 1000 pratiche
# Il neurone su un batch e' lo STESSO oggetto del Ponte cap.02:
#       Z = X @ w + b              <- vettore di N logit
#       A = sigmoid(Z)             <- vettore di N probabilita'

def neurone_batch(
    X: NDArray[np.float64],
    w: NDArray[np.float64],
    b: float,
) -> NDArray[np.float64]:
    """Forward di UN neurone su un BATCH di pratiche (matrice X (N, d)).

    Returns:
        probabilita', shape (N,) - una probabilita' per pratica.
    """
    if X.ndim != 2 or w.ndim != 1:
        raise ValueError("X deve essere 2D, w deve essere 1D")
    if X.shape[1] != w.shape[0]:
        raise ValueError(
            f"shape incompatibili: X{X.shape} colonne vs w{w.shape} elementi"
        )
    z = X @ w + b               # logit, shape (N,)
    a = sigmoid(z)              # probabilita', shape (N,)
    return np.asarray(a, dtype=float)


def _esempio_neurone_batch() -> None:
    """Forward su un mini-batch di 4 pratiche."""
    X = np.array([
        [1200, 30, 250, 180,  90],
        [ 800, 10, 100,  90,  60],
        [1500, 45, 320, 220, 110],
        [ 900, 20, 150, 120,  70],
    ], dtype=float)
    w = np.array([+0.001, -0.05, +0.02, -0.03, +0.01])
    b = -3.0
    A = neurone_batch(X, w, b)
    print("X.shape:", X.shape, " A.shape:", A.shape)
    for i in range(len(X)):
        print(f"  pratica {i}: prob={A[i]:.4f}")


# TODO 1.1 (8 minuti) - "perche' una pratica e' alterata?":
# Quando il neurone classifica una pratica come alterata (prob > 0.5), un
# auditor umano vorra' sapere "QUALI feature hanno contribuito di piu'
# alla decisione?". Implementa una funzione:
#
#       def top3_contributi(
#           x: NDArray[np.float64],
#           w: NDArray[np.float64],
#           feature_names: list[str],
#       ) -> list[tuple[str, float]]:
#           ...
#
# che, data UNA pratica x (1D), il vettore pesi w (1D) e i nomi delle
# feature, restituisce le 3 feature con CONTRIBUTO PIU' GRANDE (in valore
# assoluto), ordinate decrescente. Il "contributo" della feature j e':
#       contrib_j = x[j] * w[j]
#
# Vincoli:
#   - type hint corretti (ndarray, non array - Pattern #25)
#   - ValueError se shape incompatibili (x.ndim != 1, mismatch lunghezze)
#   - niente loop Python: usa np.argsort sul valore assoluto dei contributi
#
# Verifica con feature_names = ["delta_netto_lordo", "ratio_trattenute",
# "match_cf", "coerenza_date", "accrediti", "confidence_ocr", "incoerenze"]
# (le 7 feature reali del CSV M2). Stampa il risultato per le prime 2
# pratiche del CSV.
#
# Suggerimento operativo: hai gia' fatto qualcosa di simile nel
# E5 (interleaving) cap.02 Ponte con "contribuzioni = X_scaled * coef".
# Qui pero' lavori su 1 sola pratica, quindi e' un dot product element-wise
# fra 2 vettori 1D.
# TUO CODICE QUI:
pratiche = pd.read_csv(os.path.join(os.path.dirname(os.path.dirname(__file__)), "modulo_02_ml/", "dati", "pratiche_genuinita_mock.csv"))
X = pratiche.drop(columns=['pratica_id', 'y_alterato']).to_numpy()[:2]
rng = np.random.default_rng(42)
w = rng.standard_normal(X[0].size)
feature_names = pratiche.drop(columns=["pratica_id", "y_alterato"]).columns
def top3_contributi(
    x: NDArray[np.float64],
    w: NDArray[np.float64],
    feature_names: list[str],
) -> list[tuple[str, float]]:
    if x.ndim != 1 or w.ndim !=  1:
        raise ValueError("Il numero di dimensioni di x e w devono coincidere, e entrambi devono essere vettori 1D")
    if x.shape != w.shape:
        raise ValueError("Entrambi i vettori devono avere shape uguale")
    if x.shape[0] != len(feature_names):
        raise ValueError("Il numero delle features non combacia con la lista dei nomi")
    contrib_values = x * w
    contrib = np.argsort(np.abs(contrib_values))[::-1]
    out = [(feature_names[i], float((contrib_values)[i])) for i in contrib[0:3]]
    return out    
    
print(top3_contributi(X[0], w, feature_names))
print(top3_contributi(X[1], w, feature_names))


# TODO 1.2 (5 minuti):
# Crea un mini-batch X (3, 4) e un vettore w (4,) inventati. Stampa:
#   - lo stato shape di X e w (verifica che siano coerenti)
#   - i 3 logit (X @ w + b)
#   - le 3 probabilita' (sigmoid dei logit)
#   - SUGGERIMENTO #29: stampa anche X[0] (1D) e X[0:1] (2D) per fissare
#     la differenza che hai sbagliato nel Checkpoint C3 cap.02 Ponte.
# TUO CODICE QUI:


# TODO 1.3 (3 minuti) - "if morbido" vs "if rigido":
# Dato un batch X (10, 3) random e w (3,) random, calcola:
#   (a) y_morbido = neurone_batch(X, w, 0.0)             <- in [0, 1]
#   (b) y_rigido  = (y_morbido >= 0.5).astype(int)        <- 0 o 1
# Stampa la coppia (y_morbido[i], y_rigido[i]) per ogni pratica.
# Cosa noti? In che situazione "y_rigido" perde informazione?
# TUO CODICE QUI:


# ==========================================================================
# SEZIONE 2 - FUNZIONI DI ATTIVAZIONE: sigmoid, ReLU, tanh
# ==========================================================================

# ---------------------- ANALOGIA --------------------------------------------
# La sigmoid serve all'output (probabilita'). Ma DENTRO una rete neurale
# (M3 cap.02+) si usa di solito un'altra attivazione: la ReLU.
#
# Pensa a una rete neurale come a una catena di MONTAGGIO:
#   - ogni "stazione" prende un punteggio in input
#   - decide cosa "passare avanti" alla stazione successiva
#
# ReLU = "sportello chiuso ai negativi":
#   - se il punteggio e' negativo  -> passa 0
#   - se il punteggio e' positivo  -> passa il punteggio cosi' com'e'
#   - "max(0, z)"
#
# tanh = "sigmoid simmetrica":
#   - schiaccia in [-1, +1] invece di [0, 1]
#   - quando ti serve un output "centrato sullo zero"
#
# Sigmoid in fondo, ReLU in mezzo: e' la combinazione standard nelle reti.

# ---------------------- TEORIA + CODICE -------------------------------------
# 2.1 - LE 3 ATTIVAZIONI BASE
#
#   sigmoid(z) = 1 / (1 + exp(-z))     range (0, 1)
#   tanh(z)    = (e^z - e^-z) / (e^z + e^-z)   range (-1, +1)
#   relu(z)    = max(0, z)             range [0, +inf)


def relu(z: NDArray[np.float64]) -> NDArray[np.float64]:
    """ReLU element-wise: max(0, z)."""
    return np.maximum(0.0, z)


def tanh(z: NDArray[np.float64]) -> NDArray[np.float64]:
    """Tanh element-wise (delega a NumPy)."""
    return np.tanh(z)


def _grafico_attivazioni(
    out_path: str | None = None,
    show: bool = False,
) -> None:
    """Plot di sigmoid/ReLU/tanh per visualizzarne la forma."""
    z = np.linspace(-6, 6, 400)
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(z, sigmoid(z), label="sigmoid")
    ax.plot(z, tanh(z),    label="tanh")
    ax.plot(z, relu(z),    label="ReLU")
    ax.axhline(0, color="gray", lw=0.5)
    ax.axvline(0, color="gray", lw=0.5)
    ax.set_title("Funzioni di attivazione")
    ax.set_xlabel("z (logit)")
    ax.set_ylabel("attivazione")
    ax.legend()
    ax.grid(True, alpha=0.3)
    if out_path:
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        fig.savefig(out_path, dpi=120, bbox_inches="tight")
    if show:
        plt.show()
    plt.close(fig)


def _infografica_forward_neurone(
    out_path: str | None = None,
    show: bool = False,
) -> None:
    """Infografica didattica: pipeline x -> z -> sigmoid -> p.

    Spiega VISIVAMENTE i 2 passi di un neurone: dot product (= logit z),
    poi sigmoid (= probabilita' p in [0, 1]). Usa una pratica fittizia
    dello scenario "controllo documentale".
    """
    x = np.array([1200.0, 30.0, 250.0, 180.0, 90.0])
    nomi = ["delta_netto", "ratio_tratt", "match_cf", "coerenza_date",
            "confidence_ocr"]
    w = np.array([+0.001, -0.05, +0.02, -0.03, +0.01])
    b = -3.0
    contribuzioni = x * w
    z = float(contribuzioni.sum() + b)
    p = float(sigmoid(z))

    fig, axes = plt.subplots(1, 3, figsize=(15, 4.5),
                             gridspec_kw={"width_ratios": [3, 2, 3]})

    # Pannello 1: feature x pesi = contribuzioni (passo 1 del neurone)
    ax = axes[0]
    ax.barh(nomi, contribuzioni, color=["#2ca02c" if c > 0 else "#d62728"
                                          for c in contribuzioni])
    ax.axvline(0, color="black", lw=0.7)
    ax.set_title("Passo 1: x * w (contribuzioni)")
    ax.set_xlabel("contributo al logit")
    ax.invert_yaxis()
    ax.grid(True, axis="x", alpha=0.3)

    # Pannello 2: somma + bias = logit z (numero singolo)
    ax = axes[1]
    ax.bar(["sum(x*w)", "bias b", "z (logit)"],
           [contribuzioni.sum(), b, z],
           color=["#1f77b4", "#ff7f0e", "#9467bd"])
    ax.axhline(0, color="black", lw=0.7)
    ax.set_title("Passo 1bis: + bias = z")
    ax.set_ylabel("valore")
    for i, v in enumerate([contribuzioni.sum(), b, z]):
        ax.text(i, v, f"{v:+.2f}", ha="center",
                va="bottom" if v >= 0 else "top", fontsize=9)
    ax.grid(True, axis="y", alpha=0.3)

    # Pannello 3: sigmoid che trasforma z in probabilita' (passo 2)
    ax = axes[2]
    z_grid = np.linspace(-6, 6, 400)
    ax.plot(z_grid, sigmoid(z_grid), color="#2ca02c", lw=2, label="sigmoid")
    ax.axhline(0.5, color="gray", lw=0.5, ls="--")
    ax.scatter([z], [p], s=120, color="#d62728", zorder=5,
               label=f"z = {z:.2f}\np = {p:.3f}")
    ax.set_title("Passo 2: sigmoid(z) = probabilita'")
    ax.set_xlabel("z (logit)")
    ax.set_ylabel("p (probabilita')")
    ax.set_ylim(-0.05, 1.05)
    ax.legend(loc="lower right")
    ax.grid(True, alpha=0.3)

    fig.suptitle(
        f"Forward di UN neurone su 1 pratica  ->  prob_alterato = {p:.3f}",
        fontsize=13, y=1.02,
    )
    fig.tight_layout()

    if out_path:
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        fig.savefig(out_path, dpi=120, bbox_inches="tight")
    if show:
        plt.show()
    plt.close(fig)


# 2.2 - QUANDO USO CHE COSA?
#
#   COMPITO                                    ATTIVAZIONE FINALE     ATTIVAZIONI INTERNE
#   -------------------------------------------------------------------------------------
#   classificazione binaria (alterato si/no)   sigmoid                ReLU
#   classificazione multi-classe (cane/gatto)  softmax                ReLU
#   regressione (prezzo casa)                  nessuna (lineare)      ReLU
#
# Regola pratica per M3:
#   - hidden layer  -> ReLU (default moderno, veloce, evita "vanishing gradient")
#   - output binario -> sigmoid
#   - output multi-classe -> softmax (Ponte cap.02 esercizio E1!)


# TODO 2.1 (5 minuti) - mini-esercizio inline:
# Dato z = np.array([-3.0, -1.0, 0.0, 1.0, 3.0]), stampa:
#   - sigmoid(z)
#   - relu(z)
#   - tanh(z)
# E rispondi (commenti):
#   (a) quale attivazione fa la cosa MENO interessante su z=-1?
#   (b) quale e' l'unica che restituisce 0 esatto per z negativi?
# TUO CODICE QUI:


# TODO 2.2 (5 minuti):
# Genera il grafico delle 3 attivazioni e salvalo in
#       modulo_03_dl_cv/figures/02_01_attivazioni.png
# Suggerimento: usa la funzione _grafico_attivazioni() gia' pronta.
# Verifica che il file esista.
# TUO CODICE QUI:


# ==========================================================================
# SEZIONE 3 - FORWARD DI UN NEURONE SUL CSV REALE DEL MODULO 2
# ==========================================================================
#
# Adesso usiamo i veri dati del Modulo 2 (pratiche_genuinita_mock.csv).
# Vogliamo vedere "in vivo" che un neurone manuale, con i pesi giusti,
# riproduce le predizioni della LogisticRegression del Modulo 2 cap.04.
#
# Idea: la LogisticRegression di sklearn E' un neurone (con sigmoid in
# output). I suoi attributi:
#       clf.coef_      shape (1, d)   <- "il vettore w del neurone"
#       clf.intercept_ shape (1,)     <- "il bias b del neurone"
# Quindi:
#       prob_sklearn  = clf.predict_proba(X)[:, 1]        # via sklearn
#       prob_manuale  = sigmoid(X @ clf.coef_.ravel() + clf.intercept_[0])
# Devono coincidere fino alle ultime cifre decimali.

# ---------------------- TEORIA + CODICE -------------------------------------
# 3.1 - CARICAMENTO DATI (riusa il pattern del Ponte cap.02)
#
# Il CSV ha 7 feature numeriche + 'pratica_id' + 'y_alterato'.

CSV_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "modulo_02_ml",
    "dati",
    "pratiche_genuinita_mock.csv",
)


def carica_pratiche() -> tuple[NDArray[np.float64], NDArray[np.int64]]:
    """Carica X (N, d) e y (N,) dal CSV M2."""
    df = pd.read_csv(CSV_PATH)
    X = df.drop(columns=["pratica_id", "y_alterato"]).to_numpy(dtype=float)
    y = df["y_alterato"].to_numpy(dtype=int)
    return X, y


# 3.2 - FORWARD DI UN NEURONE "PRE-COTTO"
# Per ora i pesi non li impariamo (M3 cap.03 backpropagation): li prendiamo
# in prestito da un modello sklearn gia' addestrato e mostriamo che il
# forward manuale produce gli stessi numeri.

def _esempio_neurone_su_csv() -> None:
    """Mostra che forward manuale = LogisticRegression(predict_proba)."""
    from sklearn.linear_model import LogisticRegression
    from sklearn.preprocessing import StandardScaler

    X, y = carica_pratiche()
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    clf = LogisticRegression(max_iter=1000, random_state=42)
    clf.fit(X_scaled, y)

    w = clf.coef_.ravel()           # shape (d,)
    b = float(clf.intercept_[0])    # scalare

    prob_sklearn = clf.predict_proba(X_scaled)[:, 1]   # shape (N,)
    prob_manuale = sigmoid(X_scaled @ w + b)            # shape (N,)

    diff_max = float(np.max(np.abs(prob_sklearn - prob_manuale)))
    print(f"X_scaled.shape = {X_scaled.shape}, w.shape = {w.shape}")
    print(f"diff_max sklearn vs neurone manuale: {diff_max:.2e}")
    assert diff_max < 1e-10, "le due probabilita' DEVONO coincidere"
    print("OK: il neurone manuale riproduce LogisticRegression al 1e-10.")


# TODO 3.1 (10 minuti):
# Riproduci il setup di "_esempio_neurone_su_csv" senza guardare il codice
# sopra, MA stampando in piu':
#   (a) le PRIME 5 probabilita' (manuali) arrotondate a 3 decimali
#   (b) il numero di pratiche con prob >= 0.5  (predizione "alterato")
#   (c) la media delle probabilita' sulle pratiche dove y == 1 (deve essere
#       ALTA, > 0.6) e la media sulle pratiche dove y == 0 (deve essere
#       BASSA, < 0.4). Se non torna -> qualcosa non va nel forward.
# TUO CODICE QUI:


# TODO 3.2 (5 minuti):
# Sulle stesse pratiche del CSV, prova a mettere SCALARE = 0.0 (cioe'
# usa X NON scalato) con gli stessi w e b di sklearn. Cosa succede?
# I numeri esplodono? Restano sensati?
# Spiega in 1 commento PERCHE' la LogisticRegression viene allenata su
# X scalato e non sui valori grezzi (ricorda M2 cap.04).
# TUO CODICE QUI:


# ==========================================================================
# QUIZ DI VERIFICA (fai PRIMA di passare agli esercizi)
# ==========================================================================

# V1) [Lacuna #28] In una rete neurale binaria, l'output dell'ULTIMO layer
#     prima della sigmoid si chiama:
#       (a) probabilita'
#       (b) logit
#       (c) score F1
#     Spiega in 1 riga la differenza.
# TUA RISPOSTA:
# ...

# V2) sigmoid(0) vale:
#       (a) 0      (b) 0.5     (c) 1     (d) e
# E sigmoid(z) tende a quanto per z -> +inf? E per z -> -inf?
# TUA RISPOSTA:
# ...

# V3) [Trova l'errore] - Questo codice da' shape strana. Perche'?
#       X = rng.standard_normal((100, 4))
#       w = rng.standard_normal((4, 1))
#       z = X @ w + b
#       p = sigmoid(z)
#     Che shape ha p? Come la "appiattisci" a (100,) per usarla con sklearn
#     (es. metrics.roc_auc_score)?
# TUA RISPOSTA:
# ...

# V4) Per quale motivo le ATTIVAZIONI nei layer NASCOSTI di una rete sono
#     ReLU/tanh e NON sigmoid? Da' 1 motivo concettuale (anche solo
#     intuitivo: pensa a "cosa schiaccia troppo").
# TUA RISPOSTA:
# ...

# V5) [Trova l'errore] - Inizializzazione pesi:
#       w = np.zeros(4)
#       b = 0.0
#       z = X @ w + b
#       p = sigmoid(z)
#     Cosa stampa "p.mean()"? E perche' mettere tutti zero non funziona
#     quando poi vuoi imparare i pesi (M3 cap.03)?
# TUA RISPOSTA:
# ...

# V6) Hai z (logit) = +1.5. Quanto vale sigmoid(z), circa? E z = -1.5?
#     Un cliente con z = +1.5 ha probabilita' ALTA o BASSA di essere
#     classificato "positivo"?
# TUA RISPOSTA:
# ...

# V7) [Recap shape - cerniera #23] Hai X (N, d), w (d,), b scalare.
#     Quale di queste righe e' la PIU' Pythonic e idiomatica per fare il
#     forward di UN neurone in batch?
#       (a) np.dot(X, w) + b
#       (b) X @ w + b
#       (c) X.dot(w) + b
#     E che shape hanno tutte e tre?
# TUA RISPOSTA:
# ...

# V8) [Feynman - vincolo #27] Spiega cos'e' una "funzione di attivazione"
#     a un collega web dev. VINCOLI STRETTI: niente "non lineare", niente
#     "logit", niente "sigmoid", niente "rete". Solo analogia.
# TUA RISPOSTA:
# ...


# ==========================================================================
# ESERCIZI FINALI
# ==========================================================================
#
# E1) [COLLOQUIO] - 15 minuti
#     Scenario: ti chiedono in colloquio "spiega cos'e' un neurone
#     artificiale". Scrivi una RISPOSTA STRUTTURATA in 4 punti:
#       (1) cos'e' (definizione operativa, NON wikipedia)
#       (2) come si calcola (formula in parole, NO LaTeX)
#       (3) differenza fra logit e probabilita'
#       (4) perche' serve l'attivazione (cosa succederebbe senza)
#     Massimo 8-10 righe in totale, niente codice.
# TUA RISPOSTA:
# ...


# E2) [REFACTORING - parte 1: pattern stilistici] - 5 minuti
#     Questo codice ha 3 problemi STILISTICI che hai gia' visto. NON
#     toccare la logica: sistema solo lo "stile":
#       - Pattern #25: type hint corretti (np.ndarray, NON np.array)
#       - Pattern #23: niente virgole spurie a fine riga (creano tuple)
#       - Pattern #19: "is None" / "is not None" sui parametri opzionali
#                       (NON "if b:" su un numero, perche' confonde 0.0 con None)
#
#     def neuro_v1(X: np.array, w: np.array, b=None) -> np.array:
#         if b: bias = b,
#         else: bias = 0.0,
#         z = X @ w + bias
#         return z,
#
#     Devi RESTITUIRE z (non una tupla con z dentro!).
#     NON modificare la logica: rimane "if b is None"-stile, solo pulito.
# TUO CODICE QUI:


# E3) [REFACTORING - parte 2: logica vettoriale + naming] - 10 minuti
#     Adesso lavora sulla LOGICA. Questo codice gira ma e' brutto e lento.
#     Riscrivilo con:
#       - vettorizzazione: niente loop Python (1 sola operazione "@")
#       - controllo shape: ValueError se X.shape[1] != w.shape[0]
#       - lacuna #28: dai un nome esplicito a "logit" e "probabilita'",
#         restituendo entrambi (es. tuple (logit, prob)).
#       - lacuna #21: usa "round(x, 4)" senza virgola finale.
#
#     def neuro_v2(X, w, b):
#         out = []
#         for i in range(len(X)):
#             tot = 0
#             for j in range(len(X[i])):
#                 tot += X[i][j] * w[j]
#             prob = 1 / (1 + np.exp(-(tot + b)))
#             out.append(round(prob, 4),)
#         return np.array(out)
#
#     Verifica: con X (3, 4) random, w (4,) random, b = 0.0, la tua
#     funzione DEVE produrre gli stessi numeri (a meno della tolleranza
#     numerica) della "neuro_v2" originale.
# TUO CODICE QUI:


# E4) [DEBUG] - autonomo, niente scala progressiva (regola corso)
#     Questo codice gira ma da' risultati STRANI: tutte le probabilita'
#     sono ~0.5 indipendentemente dai dati. Trova il bug PRIMA di chiedere
#     aiuto.
#
#         rng = np.random.default_rng(0)
#         X = rng.standard_normal((50, 4))
#         w = np.zeros(4)
#         b = 0.0
#         z = X @ w + b
#         p = sigmoid(z)
#         print(p.mean(), p.min(), p.max())   # tutto ~0.5
#
#     Quando hai trovato il bug, scrivi qui sotto:
#       - cosa hai diagnosticato (1 riga)
#       - come l'hai sistemato (1 riga di codice corretto)
# TUA RISPOSTA / FIX:
# ...


# E5) [RETRIEVAL] - regola 15: riscrivi da zero una funzione di un capitolo
#                    PRECEDENTE, senza guardare il file vecchio.
#     Senza riaprire `ponte_matematico_m2_m3/01_vettori_da_zero.py`,
#     riscrivi da zero la funzione "coseno(a, b) -> float" che hai gia'
#     scritto al cap.01 Ponte (e ricontrollata in E4 cap.02 Ponte).
#
#     Deve avere TUTTI questi controlli (regole pulite cap.02 Ponte):
#       - type hint corretti (np.ndarray, non np.array - Pattern #25)
#       - controllo shape uguale + ndim == 1 sia per a sia per b
#       - controllo "norma zero" robusto: usa np.isclose con tolleranza
#       - cast esplicito a float in output
#       - assert sul range [-1.0 - eps, 1.0 + eps]
#
#     Verifica:
#       coseno([1, 2], [2, 4])      ->  1.0   (paralleli, stesso verso)
#       coseno([1, 0], [0, 1])      ->  0.0   (perpendicolari)
#       coseno([1, 0], [-1, 0])     -> -1.0   (paralleli, opposti)
#
# TUO CODICE QUI:


# E6) [INTERLEAVING] cap.01 Ponte (norma) + cap.01 M3 (neurone su CSV M2)
#     Una pratica con norma "molto alta" rispetto alle altre puo' "dominare"
#     il dot product e far esplodere il logit (z grande -> sigmoid satura
#     a 0 o 1). Per questo si SCALA prima.
#
#     Compito:
#       (a) carica X dal CSV M2 (usa "carica_pratiche()" gia' fornita)
#       (b) calcola la norma di OGNI riga di X (broadcasting + np.linalg.norm
#           con axis=1) -> vettore di N norme
#       (c) stampa min/max/media delle norme
#       (d) ora applica StandardScaler e ricalcola le norme delle righe
#       (e) confronta: nelle X scalate, le norme sono piu' "uniformi"?
#
#     Usa SOLO operazioni vettoriali (NIENTE loop). Suggerimento per (b):
#         np.linalg.norm(X, axis=1)
# TUO CODICE QUI:


# E7) [RECALL CROSS-MODULO] - OBBLIGATORIO (Regola 26 - cap.01 di nuovo modulo)
#
#     Questo esercizio dimostra che il NEURONE artificiale di M3 e' un
#     CASO PARTICOLARE del layer Dense del Ponte cap.02.
#
#     (a) Riscrivi da zero (senza guardare il Ponte) la funzione:
#             layer_dense(X, W, b, att)
#         con firma:
#             X: ndarray (N, d)
#             W: ndarray (d, h)
#             b: ndarray (h,) | float
#             att: callable o None
#         che restituisce att(X @ W + b) di shape (N, h).
#
#     (b) Mostra che il NEURONE di questa lezione si ottiene da layer_dense
#         con:
#             - W = w.reshape(-1, 1)     # da (d,) a (d, 1)
#             - b come scalare
#             - att = sigmoid
#         e che il risultato (.ravel()) coincide con neurone_batch(X, w, b).
#
#     (c) Fai girare l'asserzione su un mini-batch random (assert
#         np.allclose(...)). Se il test passa, hai dimostrato che neurone
#         = layer Dense con h=1 + sigmoid.
#
#     OBIETTIVO MENTALE: nel cap.02 M3 metteremo h>1 (vera rete), il
#     codice del layer_dense sara' lo stesso, cambia solo W.
# TUO CODICE QUI:


# ==========================================================================
# MINI-PROGETTO - "neurone_vs_logreg"
# ==========================================================================
#
# OBIETTIVO: confrontare le predizioni di un neurone scritto a mano con
# quelle di LogisticRegression (Modulo 2 cap.04) sulle stesse pratiche.
# Risultato atteso: i due classificatori producono probabilita' identiche
# fino a 1e-10. Se non torna, hai sbagliato il forward.
#
# Firma:
#     def neurone_vs_logreg() -> dict[str, float]:
#         """
#         Ritorna un dict con:
#             'diff_max'       : massima differenza |p_sklearn - p_manuale|
#             'accuracy_match' : frazione di pratiche dove le predizioni
#                                 (>= 0.5) coincidono (deve essere 1.0)
#             'recall_alterato': recall del neurone manuale sulla classe 1
#         """
#
# Vincoli OBBLIGATORI:
#   - usa StandardScaler.fit_transform per scalare X
#   - allena LogisticRegression(max_iter=1000, random_state=42) su (X_scaled, y)
#   - estrai w = clf.coef_.ravel() e b = clf.intercept_[0]
#   - calcola p_manuale = sigmoid(X_scaled @ w + b)  (NIENTE LOOP)
#   - usa la TUA sigmoid, non scipy
#   - assert np.allclose(p_sklearn, p_manuale, atol=1e-10)
#
# Verifica: stampa il dict alla fine. Ti aspetti diff_max < 1e-10,
# accuracy_match == 1.0, recall_alterato > 0.7 (il dataset e' bilanciato
# e separabile).
#
# TUO CODICE QUI:


# ==========================================================================
# CHECKPOINT FINALE (auto-verifica)
# ==========================================================================
#
# C1) [Lacuna #28 finale] In 1 frase: differenza fra "z" (logit) e "a"
#     (output di sigmoid)?
# TUA RISPOSTA:
# ...

# C2) [Feynman - vincolo #27] Spiega in 2 righe (no termini tecnici!) la
#     differenza fra un "if" classico e un "neurone".
# TUA RISPOSTA:
# ...

# C3) Hai un neurone con w = [+0.5, -1.0, +2.0] e b = -1.0. Su una pratica
#     x = [1, 1, 1] quanto vale z? E sigmoid(z), circa?
#     Mostra il calcolo a mano (no codice).
# TUA RISPOSTA:
# ...

# C4) Auto-rating onesto (compila in chiusura capitolo):
#       - neurone come "if morbido":           /10
#       - logit vs probabilita' (#28):         /10
#       - sigmoid/ReLU/tanh quando usarle:     /10
#       - forward batch su CSV M2:             /10
#       - recall cross-modulo (E7):            /10
# TUE RISPOSTE:
# ...


# ==========================================================================
# SOLUZIONI QUIZ (NON BARARE - leggi solo dopo aver risposto)
# ==========================================================================
"""
QUIZ D'INGRESSO

Q1) X @ w ha shape (200,)  - 1D, vettore di 200 logit.
    X @ w.reshape(-1, 1) ha shape (200, 1) - 2D, matrice colonna.
    Contengono gli STESSI numeri, ma uno e' un vettore e l'altro una matrice
    con 1 colonna. La distinzione conta per sklearn (predict_proba si
    aspetta 2D in input, ma per metriche tipo roc_auc_score di solito 1D).

Q2) "a" e' la probabilita' di alterato. "z" si chiama logit (o "score",
    "punteggio"). z e' senza limiti, a sta in [0, 1]. Confonderli era la
    Lacuna #28 chiusa nel Checkpoint C2 cap.02 Ponte: ora dovresti
    risponderlo "a freddo".

Q3) "(0.1,)" e' una TUPLA con un elemento, non lo scalare 0.1. NumPy lo
    accetta (broadcast), ma il codice e' illeggibile e fragile (Pattern
    #23). Versione corretta: "z = X @ w + 0.1".
    type((0.1,)) -> <class 'tuple'>.

Q4) Due motivi (almeno):
    1) BLAS / SIMD: l'operazione "@" delega a codice C ottimizzato (BLAS)
       che usa istruzioni SIMD (AVX) e a volte multi-thread. Il loop
       Python e' single-thread interpretato.
    2) Overhead dell'interprete: ogni iterazione del for-loop passa
       attraverso la VM di Python (bytecode dispatch) - costoso.
    Bonus 3) Cache locality: gli array NumPy sono contigui, BLAS legge a
       blocchi che entrano in cache. Il loop Python tocca oggetti sparsi.

Q5) X[5].shape == (7,)    -> 1D, NON va bene per predict_proba.
    X[5:6].shape == (1, 7) -> 2D, va bene per predict_proba.
    Per sklearn devi sempre passare 2D: usa X[5:6] o X[5].reshape(1, -1)
    o X[[5]] (fancy indexing).

Q6) (Feynman - risposta tipo, no termini tecnici):
    "Immagina un cuoco che prepara una pietanza. Hai 7 ingredienti
    (sale, zucchero, aceto, ...). Per ogni ingrediente sai 'quanto pesa'
    nel risultato finale (i 'gusti'). Il cuoco somma tutti i contributi
    pesati e poi DECIDE: questa pietanza e' 'piaciuta' o no? La sua
    decisione non e' un secco si/no, e' un giudizio fra 0 e 1: '0.85'
    significa 'mi piace molto'. Un neurone e' esattamente quel cuoco."


QUIZ DI VERIFICA

V1) (b) logit. Differenza in 1 riga: il logit e' un numero senza limiti
    (puoi avere -100, +100), la probabilita' sta sempre in [0, 1].

V2) sigmoid(0) = 0.5 (b). Per z -> +inf, sigmoid -> 1. Per z -> -inf,
    sigmoid -> 0. La curva e' a "S" e satura agli estremi.

V3) z e p hanno shape (100, 1) - 2D, perche' w e' (4, 1) e non (4,).
    Per ottenere (100,) usa "p.ravel()" o "p.flatten()" o "p[:, 0]".

V4) Sigmoid satura: per |z| >= 5 schiaccia tutto a 0 o 1, e il segnale
    "muore". ReLU non satura per i positivi -> permette gradienti grossi
    e quindi l'apprendimento (che vedrai in M3 cap.03 backpropagation).
    Inoltre la ReLU e' computazionalmente piu' economica.

V5) p.mean() == 0.5 esatto. Se w = 0 allora z = X@0 + 0 = 0 sempre, e
    sigmoid(0) = 0.5. Se i pesi sono tutti zero, durante il training tutti
    i neuroni di un layer ricevono gradienti identici e imparano la stessa
    cosa: "symmetry breaking" rotto. Per questo si inizializza random.

V6) sigmoid(+1.5) ~ 0.818, sigmoid(-1.5) ~ 0.182.
    z = +1.5 -> probabilita' alta (>0.5) di classe positiva.

V7) Tutte e tre fanno lo stesso lavoro e ritornano shape (N,).
    La PIU' Pythonic e moderna e' (b) X @ w + b. (a) e (c) sono legacy.

V8) (Feynman - risposta tipo):
    "E' come un volume controller a manopola: prima sommi gli effetti
    dei vari segnali in ingresso (e arrivi a un valore qualsiasi), poi
    una manopola lo schiaccia in un range utile - tipo 'da 0 a 100' -
    in modo dolce. Senza la manopola, i segnali si sommano per sempre
    e si perde il significato."


CHECKPOINT FINALE

C1) z e' il punteggio grezzo (-inf, +inf), a e' la probabilita' [0, 1].
    a = sigmoid(z).

C2) (Feynman - tipo):
    "L'if classico e' un interruttore on/off: se passi la soglia, sei
    dentro; altrimenti, fuori. Il neurone e' un cursore continuo: in base
    a quanto sei sopra/sotto la soglia, ti da' un grado di confidenza fra
    0 e 1. Cosi' puoi distinguere 'sicuramente si', 'forse si', 'forse no'."

C3) z = 0.5*1 + (-1.0)*1 + 2.0*1 - 1.0 = 0.5 - 1 + 2 - 1 = 0.5
    sigmoid(0.5) ~ 0.622
    Quindi probabilita' moderata-alta di classe positiva.
"""


# ==========================================================================
# ENTRY POINT (esegui solo le demo che esistono nel file, niente di tuo)
# ==========================================================================
if __name__ == "__main__":
    print("=" * 70)
    print("Cap.01 M3 - demo di riferimento")
    print("=" * 70)

    print("\n[Demo Lacuna #23 - shape (N,) vs (N, 1)]")
    _demo_lacuna_23()

    print("\n[Demo Lacuna #24 - tupla (0.1,) vs scalare 0.1]")
    _demo_lacuna_24()

    print("\n[Demo Lacuna #26 - benchmark BLAS vs loop]")
    _benchmark_loop_vs_blas(n=50_000, d=20)

    print("\n[Demo Lacuna #28 - logit vs probabilita']")
    _demo_lacuna_28()

    print("\n[Demo Lacuna #29 - X[5] (1D) vs X[5:6] (2D)]")
    _demo_lacuna_29()

    print("\n[Demo neurone singolo (Sez. 1)]")
    _esempio_neurone_singolo()

    print("\n[Demo neurone batch (Sez. 1)]")
    _esempio_neurone_batch()

    print("\n[Demo neurone su CSV reale (Sez. 3)]")
    try:
        _esempio_neurone_su_csv()
    except FileNotFoundError as exc:
        print("Skip: CSV M2 non trovato.", exc)
    except ImportError as exc:
        print("Skip: scikit-learn non disponibile in questo interprete.", exc)

    print("\n[Genero infografiche PNG nella cartella figures/]")
    figures_dir = os.path.join(os.path.dirname(__file__), "figures")
    _grafico_attivazioni(
        out_path=os.path.join(figures_dir, "01_attivazioni.png"),
    )
    _infografica_forward_neurone(
        out_path=os.path.join(figures_dir, "01_forward_neurone.png"),
    )
    print(f"  -> {figures_dir}/01_attivazioni.png")
    print(f"  -> {figures_dir}/01_forward_neurone.png")

    print("\n" + "=" * 70)
    print("Demo finite. Adesso tocca a te: completa i TODO in ordine.")
    print("Quando vuoi una valutazione: 'valuta cap.01 M3 sezione X.Y'.")
    print("=" * 70)
