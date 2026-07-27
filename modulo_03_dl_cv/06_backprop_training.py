"""
============================================================================
MODULO 3 (DL & CV) - CAPITOLO 06
"BACKPROP + TRAINING": tutto insieme, finalmente
============================================================================

Quarto e ULTIMO dei sotto-capitoli del vecchio "Backpropagation". Mappa:

    03_loss.py                  (loss BCE, MSE)               ← FATTO
    04_derivate_gradiente.py    (derivata, gradiente)         ← FATTO
    05_chain_rule_gd.py         (chain rule + GD)             ← FATTO
    06_backprop_training.py     ← QUESTO FILE (chiude il blocco)

Questo capitolo CHIUDE il primo blocco del modulo (cap.01-06):
- partiti dal neurone manuale (cap.01)
- alla rete 2-layer in NumPy (cap.02)
- imparato a misurare l'errore (cap.03)
- a calcolare il gradiente (cap.04)
- a comporre derivate e a "scendere" (cap.05)
- QUI mettiamo tutto in UN training loop -> rete che impara dai dati.

Dopo questo cap. tutto sara' "PyTorch" (cap.07-10): l'API e' diversa,
ma sotto il cofano fa esattamente quello che IMPLEMENTI qui.

----------------------------------------------------------------------------
DA DOVE ARRIVI (cap.03-05 M3)
----------------------------------------------------------------------------
Hai:
  - bce_loss, sigmoid, relu (cap.03)
  - derivata_sigmoid, derivata_relu, gradiente_numerico (cap.04)
  - intuizione "dL/dz = p - y" (cap.04)
  - gradient_descent_nd con grad numerico (cap.05)
  - chain rule a 5 livelli per la rete 2-layer (cap.05, qualitativa)

----------------------------------------------------------------------------
DEFINITION OF DONE (cap.06)
----------------------------------------------------------------------------
Alla fine sai:

  1) [Forward con cache] perche' serve memorizzare Z1, H, Z2, P durante
     il forward (e non solo P)?
  2) [Backward] implementare il backward STEP-BY-STEP per i 4 parametri
     (W1, b1, W2, b2) di una rete 2-layer.
  3) [Shape rules] tracciare ogni shape e capire perche' "X.T @ qualcosa"
     produce gradiente di W1.
  4) [Sanity check] confrontare il backward analitico con il gradiente
     numerico - se NON coincidono c'e' un bug.
  5) [Training loop] mettere forward + backward + update in un loop
     che addestra una rete e misurare loss/accuracy in tempo reale.
  6) [Mini-progetto reale] addestrare una rete sul CSV del M2 e
     verificare che batta (o sia comparabile a) LogReg.

Toolkit chiuso:
  - forward_2layer (ritorna P + cache)
  - backward_2layer (ritorna grad di W1, b1, W2, b2)
  - sanity_check_grad (confronto numerico vs analitico)
  - train_rete_2_layer (loop completo)
  - he_init (inizializzazione pesi standard del cap.02)

----------------------------------------------------------------------------
MAPPA DEL CAPITOLO
----------------------------------------------------------------------------
   *  PRONTUARIO TRANELLI                       [B1] - [B8]
   *  QUIZ D'INGRESSO                           Q1 - Q8
   *  RINFORZO SHAPE (carry-over)               1 micro-esercizio
   *  🔁 RINFORZO MIRATO cap.05                 dL/dp vs dL/dz (#38)
                  + la catena verso W1: W2 non e' un anello (#39)
   *  SEZIONE 1  Forward con CACHE              1.1 - 1.2
                  con 3 mini-esercizi inline
   *  SEZIONE 2  Backward step-by-step          2.1 - 2.6 (6 step)
                  con un mini-esercizio per step
                  + 🔁 RINFORZO derivata_relu in z=0 (#37) allo step 2.4
   *  SEZIONE 3  Sanity check numerico          3.1 - 3.2
                  + 🔁 RINFORZO formula -> codice (Pattern #27)
                  con 2 mini-esercizi inline
   *  SEZIONE 4  Training loop                  4.1 - 4.3
                  + 🔁 RINFORZO "spiegare il training come ciclo" (#40)
                  con 3 mini-esercizi inline
   *  SEZIONE 5  Visualizzazione                5.1 - 5.2
                  loss curve + decision boundary
   *  SEZIONE 6  Mini-batch SGD (cenno)         6.1
   *  TODO MIRATI BASE                          TODO 1 - 8
   *  RINFORZI CAP.01-05 M3 (mega-integrati)    TODO 9 - 13
   *  PIPELINE INTEGRATA                        train_rete_2_layer_completo()
                  Addestra rete + sanity check + history
   *  MINI-PROGETTO FINALE                      train_rete_su_csv_m2()
                  Rete sul dataset M2 + confronto con LogReg
   *  TIPOLOGIE STANDARD                        TODO 14 - 19
   *  CONFRONTO PRIMA/DOPO cap.01-06            (chiusura primo blocco M3)
   *  QUIZ DI VERIFICA                          V1 - V10
   *  CHECKPOINT FINALE                         C1 - C8
   *  SOLUZIONI                                 in fondo

Conta esercizi: ~14 mini-inline + 19 TODO + 1 pipeline + 1 mini-progetto reale.

----------------------------------------------------------------------------
COME USARE QUESTO FILE
----------------------------------------------------------------------------
   0. PRIMA di aprire questo file: fai il bridge di ripasso
      quiz_ripasso_tra_capitoli/M03_R05_after_C05_before_C06_chain_to_backprop.md
      (11 esercizi, 15-20 min). Questo capitolo e' il piu' tosto del modulo:
      conviene arrivarci con i fondamentali freschi.
   1. Sezioni 1-4 in ORDINE. Il backward e' "step-by-step" per imparare,
      poi al TODO 7 lo unifichi in una funzione `backward_2layer`.
   2. Il sanity check (sez. 3) e' OBBLIGATORIO: e' come ti accorgi dei
      bug del backward in qualsiasi rete (anche in produzione, non solo qui).
   3. Il mini-progetto finale e' il "voto di laurea" del primo blocco.
   4. Quando hai finito: "ho finito cap.06 M3" -> chiusura primo blocco
      del modulo + voto di difficolta'.
"""

import csv
import os
from typing import Callable

import numpy as np
import matplotlib.pyplot as plt
from numpy.typing import NDArray


# ==========================================================================
# FUNZIONI RIUTILIZZABILI (recall cap.03-05 - per autosufficienza del file)
# ==========================================================================

def sigmoid(z: NDArray[np.float64] | float) -> NDArray[np.float64] | float:
    z_arr = np.asarray(z, dtype=float)
    z_safe = np.clip(z_arr, -500.0, 500.0)
    out = 1.0 / (1.0 + np.exp(-z_safe))
    if np.isscalar(z):
        return float(out)
    return out


def relu(z: NDArray[np.float64]) -> NDArray[np.float64]:
    return np.maximum(0.0, z)


def derivata_relu(z: NDArray[np.float64]) -> NDArray[np.float64]:
    return (z > 0).astype(float)


def bce_loss(
    p: NDArray[np.float64],
    y: NDArray[np.int64] | NDArray[np.float64],
    eps: float = 1e-12,
) -> float:
    p_safe = np.clip(p, eps, 1.0 - eps)
    return float(np.mean(- y * np.log(p_safe) - (1.0 - y) * np.log(1.0 - p_safe)))


def accuracy_score(
    p: NDArray[np.float64],
    y: NDArray[np.int64] | NDArray[np.float64],
    soglia: float = 0.5,
) -> float:
    return float(np.mean((p >= soglia).astype(int) == y))


def gradiente_numerico(
    f: Callable[[NDArray[np.float64]], float],
    x: NDArray[np.float64],
    h: float = 1e-6,
) -> NDArray[np.float64]:
    grad = np.zeros_like(x, dtype=float)
    for i in range(x.size):
        xp = x.copy(); xp.flat[i] += h
        xm = x.copy(); xm.flat[i] -= h
        grad.flat[i] = (f(xp) - f(xm)) / (2.0 * h)
    return grad


def he_init(
    n_in: int,
    n_out: int,
    seed: int | None = None,
) -> NDArray[np.float64]:
    """Inizializzazione He (cap.02 M3): adatta per layer con ReLU."""
    rng = np.random.default_rng(seed)
    return rng.standard_normal((n_in, n_out)) * np.sqrt(2.0 / n_in)


# ==========================================================================
# PRONTUARIO TRANELLI - 5 minuti
# ==========================================================================
#
# [B1] FORWARD CON CACHE. Durante il forward devi MEMORIZZARE Z1, H, Z2, P
#      (non solo P). Servono per il backward, perche' la chain rule
#      richiede di "valutare le derivate locali in z" e tu queste z le
#      vedi UNA SOLA VOLTA, durante il forward.
#
# [B2] BACKWARD VA INDIETRO. Si parte dall'OUTPUT (P) e si va verso
#      l'INPUT (X), moltiplicando le derivate locali. Lo facciamo a mano
#      qui; PyTorch lo fa automaticamente (cap.08).
#
# [B3] SHAPE RULES. Ogni gradiente DEVE avere la stessa shape del
#      parametro corrispondente:
#         W1.shape == grad_W1.shape == (d, h)
#         b1.shape == grad_b1.shape == (h,)
#         W2.shape == grad_W2.shape == (h, 1)
#         b2.shape == grad_b2.shape == (1,)
#      Se non quadra, hai un bug nei prodotti matriciali.
#
# [B4] MEDIA SUL BATCH. Tutti i gradienti vanno DIVISI PER N (numero di
#      pratiche). Se no l'lr "effettivo" dipende dalla taglia del batch.
#
# [B5] SANITY CHECK. PRIMA di lanciare il training, verifica che il
#      tuo backward coincida con il gradiente NUMERICO (max diff < 1e-5).
#      Se non coincide -> bug. Quasi sempre: shape sbagliata, segno
#      sbagliato, o transpose dimenticato.
#
# [B6] CONNESSIONE CON CAP.05 -> GD. Una volta che hai grad_W1, grad_b1,
#      grad_W2, grad_b2, l'update e' identico al cap.05:
#         W1 -= lr * grad_W1   (e cosi' via per gli altri)
#
# [B7] LR + INIT. Tipici per ReLU + sigmoid + BCE: He init, lr 0.01-0.1,
#      batch FULL (tutto il dataset) per 100-500 epoche. Per dataset
#      grandi -> mini-batch SGD (cenno sez. 6).
#
# [B8] LA RETE PUO' NON IMPARARE. Cause comuni:
#      1) lr sbagliato (troppo piccolo o grande)
#      2) feature non scalate (StandardScaler!)
#      3) inizializzazione cattiva (no He, pesi tutti 0)
#      4) dataset banale (tutti y=0 -> loss minima ~ 0.69 sempre)


# ==========================================================================
# QUIZ D'INGRESSO - cerniera cap.05 -> cap.06
# ==========================================================================

# Q1) [Recall cap.05] Cos'e' la chain rule in 1 riga? E qual e'
#     l'aggiornamento dei pesi con gradient descent?
# TUA RISPOSTA:
# ...

# Q2) [Recall cap.05] Hai una rete 2-layer. Per calcolare dL/dW1 devi
#     comporre QUANTE derivate locali (con la chain rule)? Quali?
# TUA RISPOSTA:
# ...

# Q3) [Recall cap.04] Qual e' la semplificazione miracolosa per BCE +
#     sigmoid? Quanto vale dL/dZ2 in una rete con output sigmoid?
# TUA RISPOSTA:
# ...

# Q4) [Recall cap.04] La derivata di ReLU(z) vale: 1 se z > 0, 0 se z <= 0.
#     In una rete dove l'hidden ha Z1 con la meta' dei valori negativi,
#     cosa succede al gradiente di W1 in quei "neuroni" inattivi?
# TUA RISPOSTA:
# ...

# Q5) [Recall cap.02 M3] Quali sono le SHAPE di X, W1, b1, Z1, H, W2, b2,
#     Z2, P per una rete con (N=10, d=5, h=8, output=1)?
# TUA RISPOSTA:
# ...

# Q6) [Intuizione - sanity check] Hai implementato un backward "a mano".
#     Come verifichi che NON ci siano bug PRIMA di lanciare il training?
# TUA RISPOSTA:
# ...

# Q7) [💬 Feynman] Spiega in 4 righe il backpropagation a un collega
#     web dev. VIETATO: gradiente, derivata, layer, chain, backward.
#     Suggerimento: analogia "passare la colpa indietro nella catena".
# TUA RISPOSTA:
# ...

# Q8) [Prevedi output] Una rete 2-layer (d=3, h=4) con pesi RANDOM, su
#     un dataset di 100 pratiche bilanciate (50% y=1, 50% y=0):
#     - loss iniziale (epoch 0): circa quanto?         (a) ~0   (b) ~0.69   (c) ~5
#     - accuracy iniziale: circa quanto?               (a) ~0   (b) ~0.5    (c) ~1
# TUA RISPOSTA:
# ...


# ==========================================================================
# 🔁 RINFORZO MIRATO (carry-over): SHAPE
# ==========================================================================
#
# Lo SHAPE-tracking e' la causa #1 di bug nei backward. Vediamoli tutti
# in una tabella, una sola volta.
#
#   Tensor       Shape       Note
#   ------       -----       ----
#   X            (N, d)      input batch
#   y            (N,)        labels (0 o 1)
#   W1           (d, h)      pesi primo layer
#   b1           (h,)        bias primo layer
#   Z1 = X @ W1 + b1   (N, h)
#   H  = ReLU(Z1)      (N, h)
#   W2           (h, 1)      pesi secondo layer
#   b2           (1,)        bias secondo layer
#   Z2 = H @ W2 + b2   (N, 1)
#   P  = sigmoid(Z2).ravel()  (N,)
#
# Ogni operazione di backward DEVE produrre gradiente con stessa shape
# del parametro:
#   grad_W1.shape == (d, h)
#   grad_b1.shape == (h,)
#   grad_W2.shape == (h, 1)
#   grad_b2.shape == (1,)
#
# Micro-esercizio: per N=10, d=5, h=8, quanto vale ogni shape sopra?


# ==========================================================================
# 🔁 RINFORZO MIRATO — `dL/dp` vs `dL/dz` (lacuna #38)
# ==========================================================================
#
# Al bridge R04 (Q6) hai risposto che `dL/dp = p - y`. Non e' cosi':
# `p - y` e' `dL/dZ2`, cioe' la derivata rispetto al LOGIT, non rispetto
# alla probabilita'.
#
# Rivediamolo con un esempio diverso da quello del quiz — un TERMOSTATO:
#
#   z = "quanto giri la manopola"      (logit, puo' essere qualsiasi numero)
#   p = "temperatura che ne esce"      (probabilita', schiacciata fra 0 e 1)
#   L = "quanto sei scontento"         (loss)
#
#   dL/dp = "se la temperatura sale di un filo, quanto cala lo scontento?"
#   dp/dz = "se giro la manopola di un filo, quanto sale la temperatura?"
#   dL/dz = "se giro la manopola di un filo, quanto cala lo scontento?"
#
# Solo l'ULTIMA e' `p - y`, e solo perche' le altre due si moltiplicano e
# il fattore `p(1-p)` si cancella:
#
#   dL/dp = (p - y) / (p * (1 - p))        <- ha il denominatore
#   dp/dz = p * (1 - p)                    <- derivata della sigmoid
#   dL/dz = (p - y)                        <- il denominatore sparisce
#
# Nel backward di questo capitolo parti SEMPRE da `dL/dZ2 = (P - y)/N`:
# non incontrerai mai `dL/dp` da solo. Ma devi sapere perche'.
#
# Prova subito:
# 1) Con p = 0.8 e y = 1, calcola a mano i tre valori (dL/dp, dp/dz, dL/dz)
#    e verifica che il prodotto dei primi due dia il terzo.
# 2) Verifica in codice con gradiente_numerico:
#      p = np.array([0.8]); y = np.array([1.0]); z = np.log(p/(1-p))
#      num_p = gradiente_numerico(lambda pv: bce_loss(pv, y), p)
#      num_z = gradiente_numerico(lambda zv: bce_loss(sigmoid(zv), y), z)
#      # num_p deve valere circa dL/dp, num_z circa (p - y)
# TUO CODICE / COMMENTO QUI:


# ==========================================================================
# 🔁 RINFORZO MIRATO — la catena verso W1: W2 NON e' un anello (lacuna #39)
# ==========================================================================
#
# Al quiz V7 del cap.05 hai scritto la catena verso W1 passando da W2
# (`... dZ2/dW2 · dW2/dH ...`). W2 e' un PARAMETRO, non una tappa.
#
# Analogia (diversa da quella del cap.05) — due rami di un fiume:
#
#            X ──▶ Z1 ──▶ H ──▶ Z2 ──▶ P ──▶ L
#                  ▲             ▲
#                  │             │
#                 W1            W2
#
# W1 e W2 sono due AFFLUENTI che entrano nel fiume in punti diversi.
# Per risalire il fiume dalla foce (L) fino all'affluente W1, passi per
# Z2 e per H — ma non "entri" nell'affluente W2: quello e' un altro ramo,
# e lo risali solo quando cerchi `dL/dW2`.
#
# W2 compare nel percorso verso W1 solo come VALORE (un numero che
# moltiplica), dentro `dZ2/dH = W2`. Non come tappa della catena.
#
# Catena corretta (5 anelli):
#     dL/dW1 = dL/dP · dP/dZ2 · dZ2/dH · dH/dZ1 · dZ1/dW1
# Catena corretta per W2 (3 anelli):
#     dL/dW2 = dL/dP · dP/dZ2 · dZ2/dW2
#
# Regola pratica: gli anelli sono sempre "variabile precedente → variabile
# successiva" lungo il forward. Se in un anello compare un PARAMETRO al
# denominatore (dW2), quella catena si sta fermando li'.
#
# Prova subito:
# 1) Scrivi (commento) la catena per `dL/db1`. Quanti anelli ha?
#    Suggerimento: b1 entra nello stesso punto di W1.
# 2) Vero o falso: "per calcolare dL/dW2 devo prima calcolare dL/dW1".
#    Motiva in una riga.
# TUO COMMENTO QUI:


# ==========================================================================
# SEZIONE 1 - FORWARD con CACHE
# ==========================================================================
#
# La modifica rispetto al cap.02 e' MINIMA: salvi le matrici intermedie
# (Z1, H, Z2) in un dict per averle disponibili al backward.


def forward_2layer(
    X: NDArray[np.float64],
    W1: NDArray[np.float64],
    b1: NDArray[np.float64],
    W2: NDArray[np.float64],
    b2: NDArray[np.float64],
) -> tuple[NDArray[np.float64], dict[str, NDArray[np.float64]]]:
    """Forward con cache delle matrici intermedie (per il backward).

    Args:
        X:  input batch, shape (N, d)
        W1: pesi primo layer, shape (d, h)
        b1: bias primo layer, shape (h,)
        W2: pesi secondo layer, shape (h, 1)
        b2: bias secondo layer, shape (1,)

    Returns:
        P:     probabilita' predette, shape (N,)
        cache: dict con X, Z1, H, Z2, P (necessarie per backward)
    """
    Z1 = X @ W1 + b1
    H = relu(Z1)
    Z2 = H @ W2 + b2
    P = sigmoid(Z2).ravel()
    cache = {"X": X, "Z1": Z1, "H": H, "Z2": Z2, "P": P}
    return P, cache


# 1.1 - VERIFICA delle shape della cache

# 🔵 MINI-ESERCIZIO INLINE 1.1.A (~3 minuti) — chiama forward + ispeziona shape
# Setup:
#   rng = np.random.default_rng(0)
#   X = rng.standard_normal((10, 5))
#   W1 = he_init(5, 8, seed=0); b1 = np.zeros(8)
#   W2 = he_init(8, 1, seed=1); b2 = np.zeros(1)
# Chiama forward_2layer(X, W1, b1, W2, b2). Stampa le shape di P,
# cache["Z1"], cache["H"], cache["Z2"]. Atteso: (10,), (10,8), (10,8), (10,1).
# TUO CODICE QUI:


# 🔵 MINI-ESERCIZIO INLINE 1.1.B (~3 minuti) — perche' "ravel"?
# In commento (2 righe): perche' alla fine di forward facciamo
# sigmoid(Z2).ravel() invece di lasciare Z2 con shape (N, 1)?
# Suggerimento: pensa a come usiamo P per BCE e accuracy - serve shape (N,).
# TUO COMMENTO QUI:


# 1.2 - PERCHE' SERVE LA CACHE (intuizione)

# 🔵 MINI-ESERCIZIO INLINE 1.2.A (~3 minuti) — backward "alla cieca"?
# Domanda: se nel backward ho SOLO P (e non Z1, H, Z2), posso ricostruire
# da P le matrici intermedie? Spiega in 2 righe:
#   - per ricostruire H dovrei "invertire" sigmoid e dovrei avere Z2 +
#     "invertire" il dot product H @ W2 (non e' univocamente reversibile)
#   - meglio MEMORIZZARE durante forward (1 sola volta) che ricalcolare.
# TUO COMMENTO QUI:


# ==========================================================================
# SEZIONE 2 - BACKWARD step-by-step
# ==========================================================================
#
# OBIETTIVO: calcolare 4 gradienti (grad_W1, grad_b1, grad_W2, grad_b2)
# che servono al GD per aggiornare i pesi.
#
# Strategia: andiamo INDIETRO dall'output (P) all'input (X), calcolando
# UNA derivata locale alla volta. Notazione: dL/dX = "derivata della
# loss media rispetto a X" (anche se "L" e' uno scalare e X e' una
# matrice, il gradiente ha la stessa shape di X).


# 2.1 - STEP 1: dL/dZ2 (semplificazione miracolosa BCE + sigmoid)
#
# Recall cap.04 + 05: dL/dz_i = (p_i - y_i) per la singola pratica i.
# Per il BATCH (media), aggiungiamo /N:
#
#       dL/dZ2 = (P - y).reshape(-1, 1) / N         shape (N, 1)
#
# (Reshape perche' Z2 ha shape (N, 1), mentre P ha shape (N,)).

# 🔵 MINI-ESERCIZIO INLINE 2.1.A (~5 minuti) — calcola dL/dZ2 a mano
# Per N=3, P = np.array([0.9, 0.4, 0.7]), y = np.array([1, 0, 1]):
#   - calcola dL/dZ2 con la formula sopra
#   - stampa shape e valori
# Atteso shape (3, 1). Valori: P - y = [-0.1, 0.4, -0.3], diviso 3
# = [-0.033, 0.133, -0.1]. Reshape -> (3, 1).
# TUO CODICE QUI:


# 2.2 - STEP 2: dL/dW2 e dL/db2 (dal dL/dZ2)
#
# Da Z2 = H @ W2 + b2:
#   dL/dW2 = H^T @ dL/dZ2                shape (h, 1)
#   dL/db2 = sum(dL/dZ2, axis=0)         shape (1,)  (b2 e' broadcast su N)
#
# Intuizione: il bias b2 e' "uguale per tutte le pratiche", quindi il
# suo gradiente e' la SOMMA dei contributi di ogni pratica.

# 🔵 MINI-ESERCIZIO INLINE 2.2.A (~5 minuti) — calcola dL/dW2 e dL/db2
# Riprendi i dati del MINI 2.1.A e aggiungi:
#   H = np.array([[1.0, 0.0], [2.0, 1.0], [0.0, 3.0]])    # shape (3, 2)
#   N = 3
#   dL_dZ2 = ... (come MINI 2.1.A)
# Calcola:
#   dL_dW2 = H.T @ dL_dZ2                # shape attesa (2, 1)
#   dL_db2 = dL_dZ2.sum(axis=0)          # shape attesa (1,)
# Stampa shape e valori.
# TUO CODICE QUI:


# 2.3 - STEP 3: dL/dH (dal dL/dZ2)
#
# Da Z2 = H @ W2 + b2:
#   dL/dH = dL/dZ2 @ W2.T                shape (N, h)
#
# Ovvero: il gradiente "ritorna indietro" verso H moltiplicando per la
# trasposta dei pesi.

# 🔵 MINI-ESERCIZIO INLINE 2.3.A (~3 minuti) — calcola dL/dH
# Con il setup precedente, W2 = np.array([[0.5], [1.0]]):
#   dL_dH = dL_dZ2 @ W2.T               # shape attesa (3, 2)
# Stampa shape e valori.
# TUO CODICE QUI:


# 2.4 - STEP 4: dL/dZ1 (dal dL/dH, attraverso la ReLU)
#
# Da H = ReLU(Z1):
#   dL/dZ1 = dL/dH * derivata_relu(Z1)       elementwise   shape (N, h)
#
# La derivata di ReLU "spegne" i neuroni con Z1 <= 0 (dying ReLU).


# --------------------------------------------------------------------------
# 🔁 RINFORZO MIRATO — `derivata_relu` in z = 0 (lacuna #37)
# --------------------------------------------------------------------------
# Al bridge R04 (Q4) hai risposto `derivata_relu([-2, 0, 3]) = [0, 0.5, 1]`.
# Il valore in z = 0 e' **0**, non 0.5. Lo 0.5 e' `sigmoid(0)`: due funzioni
# diverse, non mescolarle.
#
# Perche' 0? Nel punto z = 0 la ReLU fa un "gomito": a sinistra e' piatta
# (pendenza 0), a destra sale a 45 gradi (pendenza 1). In quel punto esatto
# la derivata matematicamente NON esiste, quindi ogni libreria sceglie una
# convenzione. PyTorch, TensorFlow e questo corso scelgono **0**.
#
# Esempio diverso — un rubinetto con valvola di non ritorno:
#   pressione negativa o nulla -> non passa niente, e muovere ancora la
#   manopola non cambia nulla (sensibilita' 0)
#   pressione positiva        -> passa tutto, 1 a 1 (sensibilita' 1)
#
# Nel codice del capitolo la regola e' scritta cosi':
#     (z > 0).astype(float)          # STRETTAMENTE maggiore
# Se scrivessi `>=` otterresti 1 in z = 0: e' l'altra convenzione, e ti
# farebbe fallire i confronti con PyTorch al cap.07.
#
# Prova subito:
# 1) Stampa `derivata_relu(np.array([-2.0, -0.0, 0.0, 1e-9, 3.0]))`.
#    Quanti 1 ti aspetti PRIMA di eseguire? Scrivi la previsione, poi esegui.
# 2) In una riga: cosa succede al gradiente di un neurone che ha Z1 = 0
#    per TUTTE le pratiche del batch? (collegalo a "dying ReLU")
# TUO CODICE / COMMENTO QUI:


# 🔵 MINI-ESERCIZIO INLINE 2.4.A (~5 minuti) — calcola dL/dZ1
# Aggiungi:
#   Z1 = np.array([[ 1.0, -1.0], [2.0, 1.0], [-3.0, 3.0]])   # shape (3, 2)
# Calcola:
#   dL_dZ1 = dL_dH * derivata_relu(Z1)
# Stampa shape e valori. Cosa noti per gli elementi con Z1 < 0? (azzerati)
# TUO CODICE QUI:


# 2.5 - STEP 5: dL/dW1 e dL/db1 (dal dL/dZ1)
#
# Da Z1 = X @ W1 + b1:
#   dL/dW1 = X^T @ dL/dZ1                shape (d, h)
#   dL/db1 = sum(dL/dZ1, axis=0)         shape (h,)

# 🔵 MINI-ESERCIZIO INLINE 2.5.A (~5 minuti) — calcola dL/dW1 e dL/db1
# Aggiungi:
#   X = np.array([[1.0, 2.0, 3.0], [0.0, 1.0, 0.0], [1.0, -1.0, 1.0]])
# Calcola:
#   dL_dW1 = X.T @ dL_dZ1               # shape attesa (3, 2)
#   dL_db1 = dL_dZ1.sum(axis=0)         # shape attesa (2,)
# Stampa shape.
# TUO CODICE QUI:


# 2.6 - METTI INSIEME: funzione `backward_2layer`

def backward_2layer(
    cache: dict[str, NDArray[np.float64]],
    y: NDArray[np.int64] | NDArray[np.float64],
    W2: NDArray[np.float64],
) -> dict[str, NDArray[np.float64]]:
    """Backward analitico per rete 2-layer (BCE + sigmoid + ReLU).

    Args:
        cache: dict ottenuto da forward_2layer (X, Z1, H, Z2, P)
        y:     labels, shape (N,)
        W2:    pesi secondo layer (necessari per propagare dL/dH)

    Returns:
        dict con grad_W1, grad_b1, grad_W2, grad_b2 (shape identiche
        ai parametri originali).
    """
    X = cache["X"]
    Z1 = cache["Z1"]
    H = cache["H"]
    P = cache["P"]
    N = X.shape[0]

    # Step 1: dL/dZ2 (semplificazione miracolosa)
    dZ2 = (P - y).reshape(-1, 1) / N                # (N, 1)
    # Step 2: dL/dW2, dL/db2
    grad_W2 = H.T @ dZ2                              # (h, 1)
    grad_b2 = dZ2.sum(axis=0)                        # (1,)
    # Step 3: dL/dH
    dH = dZ2 @ W2.T                                  # (N, h)
    # Step 4: dL/dZ1 (attraverso ReLU)
    dZ1 = dH * derivata_relu(Z1)                     # (N, h)
    # Step 5: dL/dW1, dL/db1
    grad_W1 = X.T @ dZ1                              # (d, h)
    grad_b1 = dZ1.sum(axis=0)                        # (h,)

    return {
        "grad_W1": grad_W1,
        "grad_b1": grad_b1,
        "grad_W2": grad_W2,
        "grad_b2": grad_b2,
    }


# 🔵 MINI-ESERCIZIO INLINE 2.6.A (~5 minuti) — usa backward_2layer
# Setup:
#   rng = np.random.default_rng(0)
#   X = rng.standard_normal((10, 5))
#   y = rng.integers(0, 2, size=10).astype(float)
#   W1 = he_init(5, 8, seed=0); b1 = np.zeros(8)
#   W2 = he_init(8, 1, seed=1); b2 = np.zeros(1)
# Chiama:
#   P, cache = forward_2layer(X, W1, b1, W2, b2)
#   grads = backward_2layer(cache, y, W2)
# Verifica che le shape siano:
#   grad_W1.shape == (5, 8)
#   grad_b1.shape == (8,)
#   grad_W2.shape == (8, 1)
#   grad_b2.shape == (1,)
# TUO CODICE QUI:


# ==========================================================================
# SEZIONE 3 - SANITY CHECK numerico vs analitico
# ==========================================================================
#
# Il backward analitico fa ~10 righe di NumPy, ma puoi sbagliare:
#   - axis sbagliato in sum
#   - transpose dimenticata
#   - segno invertito
#   - shape (N,1) vs (N,) (broadcasting silenzioso)
#
# Sanity check: prendi UN parametro (es. W1[0, 0]) e calcola la sua
# derivata sia ANALITICAMENTE (con backward_2layer) sia NUMERICAMENTE
# (gradiente_numerico). Devono coincidere a meno di ~1e-5.
#
# Se non coincidono: c'e' un bug.


# --------------------------------------------------------------------------
# 🔁 RINFORZO MIRATO — dalla formula al codice senza sbagliare operatore
#    (Pattern #27, emerso nel cap.05)
# --------------------------------------------------------------------------
# Nel cap.05 il concetto era sempre giusto, ma la trascrizione no:
#     sigmoid(z) / (1 - sigmoid(z))   invece di   sigmoid(z) * (1 - sigmoid(z))
#     H * W2                          invece di   H @ W2
#     (2.0 / h)                       invece di   (2.0 * h)
#     grad.flat[i] == ...             invece di   grad.flat[i] = ...
#
# Il backward di questo capitolo e' 6 righe di NumPy piene di `@`, `.T` e
# `sum(axis=...)`: la probabilita' di un errore di trascrizione e' alta.
# La buona notizia: il sanity check numerico li trova TUTTI. E' letteralmente
# il motivo per cui esiste.
#
# Tre regole di lettura, prima di eseguire:
#   1) `*` = elemento per elemento (stessa shape o broadcasting).
#      `@` = prodotto matriciale (le dimensioni interne devono combaciare).
#      Se stai combinando due matrici "grandi" per ottenerne una piu' piccola,
#      quasi sempre e' `@`.
#   2) Controlla la SHAPE attesa prima di scrivere: se `grad_W1` deve essere
#      (d, h) e hai X (N, d) e dZ1 (N, h), l'unico modo e' `X.T @ dZ1`.
#   3) Dentro un ciclo, `=` assegna e `==` confronta. Se una riga "non fa
#      niente", cerca prima i doppi uguale.
#
# Prova subito:
# 1) Senza eseguire, di' quale di queste e' corretta per grad_W2 (shape (h,1)),
#    con H (N, h) e dZ2 (N, 1):
#       (a) H * dZ2     (b) H.T @ dZ2     (c) dZ2 @ H.T     (d) H @ dZ2
#    Motiva con le shape.
# 2) Scrivi la shape del risultato di `dZ2 @ W2.T` con dZ2 (N,1) e W2 (h,1).
# TUO COMMENTO QUI:


def sanity_check_grad(
    X: NDArray[np.float64],
    y: NDArray[np.int64] | NDArray[np.float64],
    W1: NDArray[np.float64],
    b1: NDArray[np.float64],
    W2: NDArray[np.float64],
    b2: NDArray[np.float64],
    h: float = 1e-6,
    rtol: float = 1e-4,
) -> dict[str, float]:
    """Confronta backward analitico con gradiente numerico.

    Verifica TUTTI i 4 parametri (W1, b1, W2, b2) e ritorna max diff
    per ognuno. Tutti devono essere < rtol (di default 1e-4).
    """

    def loss_di_params(W1v, b1v, W2v, b2v) -> float:
        P, _ = forward_2layer(X, W1v, b1v, W2v, b2v)
        return bce_loss(P, y)

    P, cache = forward_2layer(X, W1, b1, W2, b2)
    grads = backward_2layer(cache, y, W2)

    risultati: dict[str, float] = {}

    # Per ogni parametro: applichiamo gradiente_numerico con una
    # funzione "wrapper" che, dato un vettore flat, ricostruisce il
    # parametro e calcola la loss.

    # W1
    grad_W1_num = gradiente_numerico(
        lambda Wf: loss_di_params(Wf.reshape(W1.shape), b1, W2, b2),
        W1.flatten(),
    ).reshape(W1.shape)
    risultati["W1_max_diff"] = float(np.abs(grad_W1_num - grads["grad_W1"]).max())

    # b1
    grad_b1_num = gradiente_numerico(
        lambda bf: loss_di_params(W1, bf, W2, b2),
        b1.copy(),
    )
    risultati["b1_max_diff"] = float(np.abs(grad_b1_num - grads["grad_b1"]).max())

    # W2
    grad_W2_num = gradiente_numerico(
        lambda Wf: loss_di_params(W1, b1, Wf.reshape(W2.shape), b2),
        W2.flatten(),
    ).reshape(W2.shape)
    risultati["W2_max_diff"] = float(np.abs(grad_W2_num - grads["grad_W2"]).max())

    # b2
    grad_b2_num = gradiente_numerico(
        lambda bf: loss_di_params(W1, b1, W2, bf),
        b2.copy(),
    )
    risultati["b2_max_diff"] = float(np.abs(grad_b2_num - grads["grad_b2"]).max())

    risultati["ok"] = all(v < rtol for k, v in risultati.items() if k.endswith("_max_diff"))
    return risultati


# 🔵 MINI-ESERCIZIO INLINE 3.1.A (~5 minuti) — esegui sanity_check
# Setup come MINI 2.6.A. Chiama sanity_check_grad e stampa i risultati.
# Tutti i max_diff devono essere < 1e-4 (idealmente < 1e-6).
# Se UNO solo e' grande -> c'e' un bug nel backward (rispetto a quel
# parametro). Per ora la nostra implementazione e' corretta -> tutto ok.
# TUO CODICE QUI:


# 🔵 MINI-ESERCIZIO INLINE 3.1.B (~3 minuti) — sanity check fallito
# Simula un bug: modifica TEMPORANEAMENTE backward_2layer per "dimenticare"
# /N nel passo 1 (commenta il "/N"). Esegui sanity_check_grad: cosa cambia
# nei max_diff? Rimetti a posto il /N dopo l'esperimento.
# (Per non sporcare il file, commenta + spiega: con N=10 i grad sono
# 10 volte piu' grandi -> max_diff > 0.01.)
# TUO COMMENTO QUI:


# ==========================================================================
# SEZIONE 4 - TRAINING LOOP completo
# ==========================================================================
#
# Mettiamo tutto insieme:
#   1) inizializza pesi (He init)
#   2) per ogni epoch:
#      a) forward -> P + cache
#      b) calcola loss
#      c) backward -> grad_W1, ...
#      d) update: W1 -= lr * grad_W1, ...
#      e) (ogni K epoch) stampa loss + accuracy
#   3) ritorna pesi finali + history


# --------------------------------------------------------------------------
# 🔁 RINFORZO MIRATO — spiegare il training come CICLO (lacuna #40)
# --------------------------------------------------------------------------
# Al quiz V8 del cap.05 hai spiegato il gradient descent con l'analogia della
# collina: giusta, ma ti sei fermato a "capisco dove e' piu' giu'". Mancavano
# i due pezzi che fanno di quella immagine un ALGORITMO:
#
#   (1) il CICLO: senti → fai un passo → risenti da dove sei → ripeti,
#       finche' non smetti di migliorare;
#   (2) la DIMENSIONE del passo (il learning rate): passi lunghi ti fanno
#       scavalcare il fondo, passi corti ti fanno arrivare a notte fonda.
#
# Il training loop qui sotto e' esattamente quel ciclo scritto in Python:
# ogni `epoch` e' un "senti → passo". Guardando il codice puoi finalmente
# indicare col dito dove sta ognuna delle due cose.
#
# Prova subito:
# 1) Dopo aver letto `train_rete_2_layer`, scrivi in 4 righe la spiegazione
#    dell'addestramento a un collega web dev, includendo esplicitamente
#    "ripeti" e "quanto e' grande il passo".
#    VIETATO: gradiente, derivata, loss, peso, learning rate.
# 2) Indica con il numero di riga (o copiando la riga) dove nel loop sta:
#    (a) il "senti", (b) il "fai un passo", (c) il "ripeti".
# TUO COMMENTO QUI:


def train_rete_2_layer(
    X: NDArray[np.float64],
    y: NDArray[np.float64],
    h: int = 16,
    lr: float = 0.1,
    n_epochs: int = 200,
    seed: int = 0,
    verbose: bool = True,
    log_every: int = 20,
) -> dict[str, list[float] | NDArray[np.float64]]:
    """Training loop per rete 2-layer.

    Returns:
        dict con W1, b1, W2, b2 finali + history di loss e accuracy.
    """
    N, d = X.shape
    rng = np.random.default_rng(seed)
    W1 = rng.standard_normal((d, h)) * np.sqrt(2.0 / d)
    b1 = np.zeros(h)
    W2 = rng.standard_normal((h, 1)) * np.sqrt(2.0 / h)
    b2 = np.zeros(1)

    loss_history: list[float] = []
    acc_history: list[float] = []

    for epoch in range(n_epochs):
        P, cache = forward_2layer(X, W1, b1, W2, b2)
        loss = bce_loss(P, y)
        acc = accuracy_score(P, y)
        loss_history.append(loss)
        acc_history.append(acc)

        grads = backward_2layer(cache, y, W2)
        W1 -= lr * grads["grad_W1"]
        b1 -= lr * grads["grad_b1"]
        W2 -= lr * grads["grad_W2"]
        b2 -= lr * grads["grad_b2"]

        if verbose and (epoch % log_every == 0 or epoch == n_epochs - 1):
            print(f"epoch {epoch:>4d}  loss = {loss:>7.4f}  acc = {acc:>5.3f}")

    return {
        "W1": W1, "b1": b1, "W2": W2, "b2": b2,
        "loss_history": loss_history,
        "acc_history": acc_history,
    }


# 🔵 MINI-ESERCIZIO INLINE 4.1.A (~10 minuti) — addestra su dataset "facile"
# Setup:
#   rng = np.random.default_rng(0)
#   N, d = 200, 5
#   X = rng.standard_normal((N, d))
#   y = (X[:, 0] + X[:, 1] > 0).astype(float)    # label "lineare facile"
# Esegui train_rete_2_layer(X, y, h=16, lr=0.1, n_epochs=300).
# Verifica:
#   - loss finale < 0.3 (eventualmente < 0.1 se converge bene)
#   - accuracy finale > 0.9
# TUO CODICE QUI:


# 🔵 MINI-ESERCIZIO INLINE 4.2.A (~10 minuti) — addestra su XOR (non lineare)
# Setup:
#   X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]], dtype=float)
#   y = np.array([0, 1, 1, 0], dtype=float)
# Esegui train_rete_2_layer(X, y, h=8, lr=0.5, n_epochs=2000, log_every=200).
# XOR e' il classico problema NON lineare che dimostra perche' la rete
# 2-layer batte la regressione logistica (che NON impara mai XOR).
# Verifica: accuracy finale = 1.0 (su 4 pratiche).
# TUO CODICE QUI:


# 🔵 MINI-ESERCIZIO INLINE 4.3.A (~5 minuti) — confronta lr sull'addestramento
# Sul dataset di 4.1.A, prova lr in [0.001, 0.01, 0.1, 1.0]:
#   - per ognuno: 200 epoch
#   - stampa loss finale + accuracy finale
# Quale lr converge meglio? Commenta in 1 riga.
# TUO CODICE QUI:


# ==========================================================================
# SEZIONE 5 - VISUALIZZAZIONE
# ==========================================================================
#
# Due grafici "must" del training:
#   1) Loss curve (loss vs epoch) - mostra che la loss scende
#   2) Decision boundary - per dataset 2D, mostra come la rete separa
#      i positivi dai negativi


def grafico_loss_curve(
    history: dict[str, list[float] | NDArray[np.float64]],
    out_path: str | None = None,
    show: bool = False,
) -> None:
    """Plot della loss e dell'accuracy vs epoch."""
    loss_history = history["loss_history"]
    acc_history = history["acc_history"]
    fig, ax1 = plt.subplots(figsize=(10, 5))
    ax1.plot(loss_history, color="#d62728", label="loss (BCE)")
    ax1.set_xlabel("epoch")
    ax1.set_ylabel("BCE loss", color="#d62728")
    ax1.tick_params(axis="y", labelcolor="#d62728")
    ax2 = ax1.twinx()
    ax2.plot(acc_history, color="#1f77b4", label="accuracy")
    ax2.set_ylabel("accuracy", color="#1f77b4")
    ax2.tick_params(axis="y", labelcolor="#1f77b4")
    ax1.set_title("Training history: loss scende, accuracy sale")
    ax1.grid(True, alpha=0.3)
    if out_path:
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        fig.savefig(out_path, dpi=120, bbox_inches="tight")
    if show:
        plt.show()
    plt.close(fig)


def grafico_decision_boundary(
    X: NDArray[np.float64],
    y: NDArray[np.float64],
    W1: NDArray[np.float64],
    b1: NDArray[np.float64],
    W2: NDArray[np.float64],
    b2: NDArray[np.float64],
    out_path: str | None = None,
    show: bool = False,
) -> None:
    """Plot decision boundary per dataset 2D."""
    assert X.shape[1] == 2, "decision boundary serve un dataset 2D"
    x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
    y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
    xx, yy = np.meshgrid(np.linspace(x_min, x_max, 200),
                         np.linspace(y_min, y_max, 200))
    grid = np.c_[xx.ravel(), yy.ravel()]
    P_grid, _ = forward_2layer(grid, W1, b1, W2, b2)
    Z = P_grid.reshape(xx.shape)
    fig, ax = plt.subplots(figsize=(8, 7))
    ax.contourf(xx, yy, Z, levels=20, cmap="RdBu_r", alpha=0.6)
    ax.contour(xx, yy, Z, levels=[0.5], colors="black", linewidths=2)
    ax.scatter(X[y == 0, 0], X[y == 0, 1], c="blue", edgecolors="white",
               label="y = 0", s=60)
    ax.scatter(X[y == 1, 0], X[y == 1, 1], c="red", edgecolors="white",
               label="y = 1", s=60)
    ax.set_xlabel("x1")
    ax.set_ylabel("x2")
    ax.set_title("Decision boundary della rete 2-layer addestrata")
    ax.legend()
    ax.grid(True, alpha=0.3)
    if out_path:
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        fig.savefig(out_path, dpi=120, bbox_inches="tight")
    if show:
        plt.show()
    plt.close(fig)


# 🔵 MINI-ESERCIZIO INLINE 5.1.A (~5 minuti) — visualizza training su XOR
# Addestra la rete su XOR (come 4.2.A) e genera:
#   - loss curve in figures/06_01_loss_xor.png
#   - decision boundary in figures/06_02_boundary_xor.png
# Verifica entrambi i file.
# TUO CODICE QUI:


# ==========================================================================
# SEZIONE 6 - MINI-BATCH SGD (cenno per il futuro)
# ==========================================================================
#
# Finora abbiamo fatto BATCH GD: ogni epoch usa TUTTO il dataset per
# calcolare un gradiente, poi update. Per dataset con N >> 1000 questo
# diventa lento e occupa memoria.
#
# MINI-BATCH SGD: a ogni step usa solo M pratiche (M < N), randomizzate.
# Ad esempio M=32, 64, 128. Vantaggi:
#   - 1 epoch = N/M update (piu' update per "passata sul dataset")
#   - meno memoria
#   - "rumore" del mini-batch aiuta a uscire da minimi locali
#
# In PyTorch (cap.08): DataLoader gestisce automaticamente il mini-batch.
# Qui sotto vediamo l'idea in 6 righe.
#
# (Solo concettuale - non e' un mini-esercizio obbligatorio.)
#
#   rng = np.random.default_rng(0)
#   indici = rng.permutation(N)
#   for start in range(0, N, batch_size):
#       idx = indici[start:start + batch_size]
#       Xb, yb = X[idx], y[idx]
#       # forward + backward + update SOLO su Xb, yb


# ==========================================================================
# TODO MIRATI BASE (1 - 8)
# ==========================================================================

# TODO 1 (10 minuti) — forward_2layer e ispezione cache
# Setup:
#   rng = np.random.default_rng(0)
#   X = rng.standard_normal((20, 4))
#   W1 = he_init(4, 6, seed=0); b1 = np.zeros(6)
#   W2 = he_init(6, 1, seed=1); b2 = np.zeros(1)
# Chiama forward_2layer e:
#   - stampa le shape della cache
#   - verifica che H >= 0 ovunque (ReLU)
#   - verifica che P in (0, 1) ovunque (sigmoid)
# TUO CODICE QUI:


# TODO 2 (15 minuti) — backward_2layer + verifica shape
# Continuando dal TODO 1, aggiungi y = rng.integers(0, 2, size=20).astype(float).
# Chiama backward_2layer. Stampa per ogni gradiente: shape + somma assoluta.
# Verifica che le shape siano (4, 6), (6,), (6, 1), (1,).
# TUO CODICE QUI:


# TODO 3 (20 minuti) — sanity_check_grad in azione
# Continuando dai TODO 1-2: chiama sanity_check_grad. Tutti i max_diff
# devono essere < 1e-4.
# Bonus: prova a INTRODURRE un bug nel backward (es. ometti il /N) e
# verifica che sanity_check_grad PROTESTA correttamente. Poi rimetti a posto.
# TUO CODICE QUI:


# TODO 4 (15 minuti) — train_rete_2_layer su dataset semplice
# Setup:
#   rng = np.random.default_rng(0)
#   X = rng.standard_normal((300, 4))
#   y = (X[:, 0] - X[:, 1] > 0).astype(float)    # label lineare
# Esegui train_rete_2_layer con h=16, lr=0.1, n_epochs=200.
# Verifica:
#   - loss iniziale ~ 0.69
#   - loss finale < 0.2
#   - accuracy finale > 0.95
# Salva loss curve in figures/06_03_loss_lineare.png.
# TUO CODICE QUI:


# TODO 5 (15 minuti) — train su CERCHIO (dataset non lineare)
# Setup:
#   rng = np.random.default_rng(0)
#   X = rng.uniform(-3, 3, size=(400, 2))
#   y = ((X[:, 0]**2 + X[:, 1]**2) < 4.0).astype(float)    # cerchio di raggio 2
# Esegui train_rete_2_layer con h=32, lr=0.1, n_epochs=500.
# Verifica accuracy finale > 0.95.
# Salva decision boundary in figures/06_04_boundary_cerchio.png.
# TUO CODICE QUI:


# TODO 6 (15 minuti) — effetto della larghezza h
# Stesso dataset cerchio del TODO 5. Prova h in [2, 4, 8, 16, 32]:
#   - per ognuno: addestra 500 epoche
#   - stampa loss finale + accuracy finale
# Quale h serve come MINIMO per imparare il cerchio?
# Commenta in 2 righe: "la UAT (cap.02 M3) dice che basta h grande;
# in pratica per cerchio bastano h = ?".
# TUO CODICE QUI:


# TODO 7 (15 minuti) — refactoring del backward in stile "step rule"
# Riscrivi backward_2layer scomposto in 5 funzioni che fanno UNO step
# ciascuna. Esempio:
#   def step1_dZ2(P, y) -> dZ2: ...
#   def step2_grad_W2_b2(H, dZ2) -> (grad_W2, grad_b2): ...
#   def step3_dH(dZ2, W2) -> dH: ...
#   def step4_dZ1(dH, Z1) -> dZ1: ...
#   def step5_grad_W1_b1(X, dZ1) -> (grad_W1, grad_b1): ...
# Poi backward_2layer_v2(cache, y, W2) le chiama in sequenza.
# Verifica che dia gli STESSI risultati del backward originale.
# (Refactoring che ti aiuta a "vedere" la chain rule in codice.)
# TUO CODICE QUI:


# TODO 8 (15 minuti) — confronto BCE finale tra reti con seed diversi
# Sul dataset del TODO 4 (lineare), addestra 5 reti con seed = 0..4
# (stesso lr, stesso h, stesso n_epochs). Stampa una tabella con:
#   - seed | loss finale | accuracy finale
# Cosa noti? La rete e' "deterministica" data la stessa init? Oppure
# converge a SOLUZIONI DIVERSE? Commenta in 2 righe.
# TUO CODICE QUI:


# ==========================================================================
# RINFORZI CAP.01-05 M3 mega-integrati (TODO 9 - 13)
# ==========================================================================

# TODO 9 (10 minuti) [🔄 RECALL cap.03 LOSS]:
# Riscrivi bce_loss da zero (senza guardare la versione in alto).
# Verifica con p=np.array([0.9, 0.1, 0.5]), y=np.array([1, 0, 1]).
# TUO CODICE QUI:


# TODO 10 (10 minuti) [🔄 RECALL cap.04 — derivata sigmoid]:
# Riscrivi derivata_sigmoid (formula: s(z) * (1 - s(z))).
# Verifica numericamente con derivata_numerica per z in [-3, 0, 3].
# TUO CODICE QUI:


# TODO 11 (15 minuti) [🔄 RECALL cap.05 — gradient descent]:
# Riscrivi gradient_descent_1d (con differenza centrata) e usala per
# trovare il minimo di f(x) = (x - 4)^2 partendo da x0 = -2, lr = 0.3.
# Stampa la traiettoria. Atteso: converge a 4 in ~ 20 step.
# TUO CODICE QUI:


# TODO 12 (15 minuti) [🧠 RETRIEVAL cap.02 M3 — rete_2_layer da zero]:
# Senza guardare il cap.02 ne' i precedenti TODO, riscrivi forward_2layer
# (con cache) da zero. Verifica con il setup del TODO 1.
# TUO CODICE QUI:


# TODO 13 (20 minuti) [🔀 INTERLEAVING MEGA cap.01-05 + cap.06]:
# Mini-pipeline completa "carico CSV M2 + addestro + valuto":
#   1) Carica i dati dal CSV del cap.M2_C04 (mini-progetto LogReg):
#         path_csv = os.path.join(
#             os.path.dirname(__file__), "..", "modulo_02_ml",
#             "dati", "pratiche.csv",
#         )
#      Se il CSV NON esiste, usa il dataset sintetico:
#         rng = np.random.default_rng(0)
#         X = rng.standard_normal((300, 4))
#         y = (X[:, 0] + X[:, 1] - X[:, 2] > 0).astype(float)
#   2) Carica con csv.DictReader e converti in NumPy (X, y).
#   3) Standardizza X con (X - mean) / std (calcolando mean e std solo
#      sui dati di train... per ora usiamo tutto, e' didattico).
#   4) Addestra una rete con h=16, lr=0.1, n_epochs=300.
#   5) Stampa loss finale + accuracy finale.
#   6) Per ora confronta solo con accuracy di una "baseline costante":
#         accuracy_baseline = max(y.mean(), 1 - y.mean())
#      La rete deve battere la baseline (di almeno 5 punti percentuali).
# TUO CODICE QUI:


# ==========================================================================
# PIPELINE INTEGRATA — train_rete_2_layer_completo
# ==========================================================================
#
# OBIETTIVO: una funzione "tutto in uno" che addestra + valida + traccia
# loss/accuracy + esegue sanity check al passo 0.

# TODO PIPE.1 (30 minuti):
#
# Firma:
#   def train_rete_2_layer_completo(
#       X: NDArray[np.float64],
#       y: NDArray[np.float64],
#       h: int = 16,
#       lr: float = 0.1,
#       n_epochs: int = 200,
#       seed: int = 0,
#       fai_sanity_check: bool = True,
#   ) -> dict:
#       """
#       1) Inizializza pesi (He init).
#       2) Se fai_sanity_check, chiama sanity_check_grad PRIMA del
#          training (al passo 0) e ALERTA se max_diff > 1e-4.
#       3) Esegue il training loop (forward + backward + update).
#       4) Salva loss_history, acc_history.
#       5) Ritorna: pesi finali, history, dict con loss/acc iniziali e finali,
#          e (se applicabile) i risultati del sanity check.
#       """
#
# Verifica chiamandola sul dataset del TODO 5 (cerchio). Verifica che il
# sanity check passi e che la rete converga ad accuracy > 0.95.
# TUO CODICE QUI:


# ==========================================================================
# MINI-PROGETTO FINALE — `train_rete_su_csv_m2`
# ==========================================================================
#
# OBIETTIVO ULTIMO: addestrare la rete 2-layer su un CSV reale (dataset
# del M2) e battere LogReg. Replica del confronto del cap.02 M3, ma
# stavolta con la rete ADDESTRATA (non random).
#
# Note:
#   - se il CSV del M2 non e' presente, fallback a un dataset sintetico
#   - normalizza le feature (StandardScaler "a mano")
#   - target: loss < 0.3, accuracy > 0.85
#   - confronto: stampa accuracy LogReg (se sklearn disponibile) vs rete

# TODO MINI-PROGETTO (45 minuti):
#
# Firma:
#   def train_rete_su_csv_m2(
#       path_csv: str | None = None,
#       h: int = 16,
#       lr: float = 0.1,
#       n_epochs: int = 500,
#       seed: int = 0,
#   ) -> dict[str, float]:
#       """
#       Carica CSV (o fallback sintetico), normalizza, addestra,
#       valuta. Confronta con LogReg di sklearn (se disponibile).
#       Ritorna:
#         {
#           'rete_loss_finale':     float
#           'rete_accuracy':        float
#           'logreg_accuracy':      float    (NaN se sklearn non installato)
#           'differenza_accuracy':  float    (rete - logreg)
#           'rete_meglio_di_logreg': bool
#         }
#       """
#
# Step:
#   1) Carica CSV (header = feature names + target).
#   2) Convertilo a NumPy. Standardizza X.
#   3) Train/test split 80/20 (uso np.random.permutation e slicing).
#   4) train_rete_2_layer_completo su (X_train, y_train).
#   5) Valuta su X_test: P_test, loss_test, accuracy_test.
#   6) (Se sklearn ok) LogisticRegression su (X_train, y_train),
#      accuracy_logreg = score su X_test.
#   7) Stampa una tabella di confronto.
#   8) Salva loss curve + decision boundary (se X 2D) nelle figures/.
#
# Target di successo:
#   - rete_accuracy >= 0.85
#   - differenza_accuracy >= -0.05 (la rete e' almeno comparabile a LogReg)
#
# Bonus: se il CSV del M2 ha piu' di 2 feature, fai un train solo su 2
# feature per poter visualizzare il decision boundary.
# TUO CODICE QUI:


# ==========================================================================
# TIPOLOGIE STANDARD (TODO 14 - 19)
# ==========================================================================

# TODO 14 (20 minuti) [🎯 COLLOQUIO]:
# "L'intervistatore ti dice: 'Spiega la BACKPROPAGATION in 5 minuti. Voglio:
#   (1) cos'e' il problema che risolve (1-2 frasi)
#   (2) intuizione qualitativa (analogia, 2-3 frasi)
#   (3) la RICETTA (forward + backward + update, 3-4 frasi)
#   (4) connessione con gradient descent (1 frase)
#   (5) 2-3 problemi tipici in produzione (vanishing gradient, dataset
#       sbilanciato, lr troppo grande, etc.)
#  '"
# Scrivi la risposta sotto, in 15-20 righe MASSIMO. Usa pseudo-italiano,
# NIENTE formule LaTeX, parole tipo "derivata" sono ok.
# TUA RISPOSTA:
# ...


# TODO 15 (20 minuti) [🔧 REFACTORING]:
# Questo training loop "funziona" ma ha 4 bug/brutture. Trovali e fixali.
#
#   def train_brutto(X, y, h=16, lr=0.1, n_epochs=200, seed=0):
#       N, d = X.shape
#       np.random.seed(seed)                  # bug 1: stile vecchio
#       W1 = np.random.randn(d, h)            # bug 2: no He init -> brutta convergenza
#       b1 = np.zeros((h, 1))                 # bug 3: shape sbagliata (deve essere (h,))
#       W2 = np.random.randn(h, 1)
#       b2 = np.zeros(1)
#       for ep in range(n_epochs):
#           Z1 = X @ W1 + b1                  # bug 4: con b1 (h,1) il broadcast e' sbagliato
#           H = relu(Z1)
#           Z2 = H @ W2 + b2
#           P = sigmoid(Z2).ravel()
#           loss = bce_loss(P, y)
#           # ... backward (uguale all'analitico) ...
#           dZ2 = (P - y).reshape(-1, 1) / N
#           grad_W2 = H.T @ dZ2
#           grad_b2 = dZ2.sum(axis=0)
#           dH = dZ2 @ W2.T
#           dZ1 = dH * derivata_relu(Z1)
#           grad_W1 = X.T @ dZ1
#           grad_b1 = dZ1.sum(axis=0)
#           W1 -= lr * grad_W1
#           b1 -= lr * grad_b1                # bug 3 -> qui propaga errore
#           W2 -= lr * grad_W2
#           b2 -= lr * grad_b2
#       return W1, b1, W2, b2, loss
#
# Spiega in commento ogni bug e dai la versione corretta.
# TUO CODICE QUI:


# TODO 16 (15 minuti) [🔍 DEBUG]:
# La rete del TODO 4 (lineare) NON impara: loss resta a 0.69, accuracy
# fluttua intorno a 0.5. Possibili cause:
#   (1) lr = 0 (mai update)
#   (2) backward "spento" (ritorna 0 per tutti i grad)
#   (3) feature non normalizzate e con varianza enorme
#   (4) labels invertite (y = 1 - y per errore)
# Costruisci un test che simuli (3): genera X con varianza 100 (X *= 100)
# e prova ad addestrare con i settaggi del TODO 4. Cosa succede?
# Come risolvi?
# TUO CODICE QUI:


# TODO 17 (15 minuti) [🧠 RETRIEVAL cap.03 LOSS + cap.04 derivate]:
# Senza guardare cap.03 e cap.04, riscrivi DA ZERO:
#   - bce_loss (clip bilaterale!)
#   - derivata_sigmoid (formula chiusa)
#   - derivata_relu (step function)
# Verifica le 3 funzioni in 1 script con asserzioni.
# TUO CODICE QUI:


# TODO 18 (20 minuti) [🔀 INTERLEAVING cap.02 + cap.06 + scaler]:
# Mini-pipeline che integra "regola scaler" del cap.M2:
#   1) Genera dataset con scale molto diverse:
#        X1 ~ N(0, 1)        (feature "normale")
#        X2 ~ N(0, 100)      (feature con varianza ENORME)
#   2) Stack -> X di shape (200, 2)
#   3) y = (X1 + X2 > 0).astype(float)
#   4) Addestra train_rete_2_layer su X "crudo" - osserva loss/acc.
#   5) Standardizza: X_std = (X - X.mean(0)) / X.std(0). Riaddestra.
#   6) Confronta: senza standardizzazione la rete arranca; con
#      standardizzazione converge molto piu' veloce.
# TUO CODICE QUI:


# TODO 19 (20 minuti) [🌊 REAL-WORLD]:
# "Una rete che hai deployato 6 mesi fa stava al 92% di accuracy. Oggi
# misuri 78%. Il modello e' lo stesso, i pesi non sono cambiati. Cosa
# pensi? Da dove cominci a investigare?"
# Suggerisci 4-5 ipotesi (in commento). Esempi:
#   1) DATA DRIFT: la distribuzione dei nuovi dati e' diversa da quella
#      di training. Verifica calcolando mean/std delle nuove feature.
#   2) LABEL SHIFT: la prevalenza delle classi e' cambiata (es. piu' pratiche
#      alterate negli ultimi mesi).
#   3) CONCEPT DRIFT: la relazione X -> y e' cambiata (i broker hanno
#      cambiato strategia di frode).
#   4) BUG IN PRE-PROCESSING: lo scaler che usavi in training non e'
#      esattamente quello usato in inferenza (mean/std diversi).
#   5) BUG IN POSTPROCESSING: cambio della soglia (era 0.5, e' diventata 0.7).
# Bonus: simula data drift moltiplicando X_test per 1.5 e misurando il
# degrado dell'accuracy.
# TUA RISPOSTA + (bonus) verifica:
# ...


# ==========================================================================
# 🔄 CONFRONTO PRIMA/DOPO cap.01-06 (chiusura primo blocco del modulo)
# ==========================================================================
#
# OBIETTIVO: lo studente CONFRONTA il codice di partenza (neurone manuale
# del cap.01 M3) con quello attuale (rete 2-layer ADDESTRATA, cap.06 M3).
# Mostra il salto qualitativo.

# TODO CONFRONTO (25 minuti):
#
# (1) Riprendi mentalmente cosa facevi al cap.01 M3:
#       z = w . x + b
#       p = sigmoid(z)
#       # pesi inventati a mano, accuracy ~ 0.5 sul dataset M2
#
# (2) Cosa fai ora (cap.06 M3):
#       - rete 2-layer (input + hidden + output)
#       - inizializzazione He
#       - forward + cache + backward analitico
#       - GD su 21+ parametri contemporaneamente
#       - accuracy >> 0.5 (su un dataset non banale)
#
# (3) Scrivi nel file (in commento) la tua "evoluzione" in 8-10 righe:
#       - cosa NON capivi al cap.01
#       - cosa ti sembrava magia al cap.02
#       - cosa ti spaventava al cap.03 (BCE) e cap.04 (derivate)
#       - cosa ti sembra di aver "afferrato" ORA
#       - cosa ti aspetti di trovare in PyTorch (cap.07-10): API piu'
#         pulita ma SOTTO IL COFANO fa esattamente questo
#
# (4) BONUS pratico: ricrea il "neurone manuale del cap.01 M3":
#       neurone_manuale(x, w, b) = sigmoid(w . x + b)
#     con w, b inventati a mano sul dataset del TODO 13.
#     Confronta la sua accuracy con quella della rete addestrata. Quanti
#     "punti" di accuracy hai guadagnato grazie all'addestramento?
# TUO COMMENTO + CODICE:
# ...


# ==========================================================================
# QUIZ DI VERIFICA (V1 - V10)
# ==========================================================================

# V1) Cos'e' un "training loop" in 1 riga (forward + ?  + ?)?
# TUA RISPOSTA:
# ...

# V2) Perche' serve la CACHE durante il forward?
# TUA RISPOSTA:
# ...

# V3) Hai una rete 2-layer (d=4, h=8). Scrivi le shape di grad_W1, grad_b1,
#     grad_W2, grad_b2.
# TUA RISPOSTA:
# ...

# V4) Cos'e' il sanity check del backward e perche' farlo PRIMA di
#     addestrare?
# TUA RISPOSTA:
# ...

# V5) [Trova l'errore] Questo backward "dimentica" una cosa:
#       dZ2 = (P - y).reshape(-1, 1)    # bug
#       grad_W2 = H.T @ dZ2
#     Quale?
# TUA RISPOSTA:
# ...

# V6) [Prevedi output] Dataset bilanciato (50% y=1). Rete random h=8.
#     Loss iniziale (epoch 0): circa quanto? (suggerimento: -log(0.5))
# TUA RISPOSTA:
# ...

# V7) Hai addestrato 500 epoche e la loss e' 0.692. Cosa pensi?
#     (a) ottimo, hai imparato       (b) qualcosa non funziona
#     (c) ti aspetti loss negativa   (d) e' la loss minima possibile
# TUA RISPOSTA:
# ...

# V8) [💬 Feynman] Spiega in 4-5 righe il "training loop" a un collega
#     web dev. VIETATO: gradient, derivata, loss, layer.
# TUA RISPOSTA:
# ...

# V9) Hai una rete che impara XOR. ReLU + sigmoid. Loss finale 0.05,
#     accuracy 1.0. Se sostituisci ReLU con sigmoid nei layer interni,
#     cosa ti aspetti? Spiega in 1 riga.
# TUA RISPOSTA:
# ...

# V10) [SYSTEM DESIGN mini] Vuoi addestrare una rete su 1M di pratiche.
#      Quali 3 modifiche al training loop sono indispensabili?
#      (Suggerimento: mini-batch, normalizzazione, train/val/test split.)
# TUA RISPOSTA:
# ...


# ==========================================================================
# CHECKPOINT FINALE
# ==========================================================================

# C1) In 1 frase: cos'e' la BACKPROPAGATION?
# TUA RISPOSTA:
# ...

# C2) In 1 frase: cos'e' il TRAINING LOOP?
# TUA RISPOSTA:
# ...

# C3) Hai due reti con stessa architettura. Una addestrata, una random.
#     Su un dataset bilanciato: che accuracy ti aspetti per ognuna?
# TUA RISPOSTA:
# ...

# C4) [Recall] Quali sono i 5 step del backward per la rete 2-layer?
#     Scrivili in pseudocodice (5 righe).
# TUA RISPOSTA:
# ...

# C5) [Recall cap.03-04] La derivata di L = BCE(sigmoid(z), y) rispetto
#     a z e' = ?
# TUA RISPOSTA:
# ...

# C6) [Recall cap.05] Cos'e' la chain rule? E come applichi per dL/dW1?
# TUA RISPOSTA:
# ...

# C7) [Recall cap.02 M3] Cos'e' la He init? Perche' "He" e non "uniform"?
# TUA RISPOSTA:
# ...

# C8) Auto-rating onesto:
#       - Forward con cache:                          /10
#       - Backward step-by-step (i 5 passi):          /10
#       - Sanity check numerico vs analitico:         /10
#       - Training loop completo:                     /10
#       - Connessione con cap.01-05 M3:                /10
#       - Addestramento su CSV M2 (mini-progetto):    /10
#       - Confronto prima/dopo cap.01-06:             /10
# TUE RISPOSTE:
# ...


# ==========================================================================
# SOLUZIONI QUIZ
# ==========================================================================
"""
QUIZ D'INGRESSO

Q1) Chain rule = "moltiplica le derivate locali" (dh/dx = f'(g(x)) * g'(x)).
    GD: x_nuovo = x_vecchio - lr * grad_in_x_vecchio.

Q2) 5 derivate locali: dL/dP, dP/dZ2, dZ2/dH, dH/dZ1, dZ1/dW1.
    O equivalentemente: dL/dZ2 (=P-y), dL/dH (=dZ2 @ W2.T), dL/dZ1
    (=dH * derivata_relu(Z1)), dL/dW1 (=X.T @ dZ1).

Q3) Semplificazione: dL/dz = p - y (i p(1-p) si elidono).
    Per la rete: dL/dZ2 = (P - y).reshape(-1, 1) / N.

Q4) I neuroni con Z1 <= 0 hanno derivata_relu = 0 -> dL/dZ1 = 0 ->
    grad_W1 = 0 per i pesi che alimentano quel neurone -> non
    aggiornano -> "dying ReLU".

Q5) X (10,5), W1 (5,8), b1 (8,), Z1 (10,8), H (10,8),
    W2 (8,1), b2 (1,), Z2 (10,1), P (10,).

Q6) Sanity check: confronto backward analitico vs gradiente_numerico.
    Se max_diff > 1e-4 c'e' un bug.

Q7) Esempio: "Hai una catena di traduttori. Tu chiedi 'volevi un
    cappuccino' in italiano, lui lo traduce in inglese, l'altro in
    francese. La risposta finale arriva in francese. Se la risposta
    e' sbagliata, ognuno della catena ha contribuito 'un po' '. Tu
    risali la catena dicendo a ogni traduttore: hai sbagliato di
    questo tanto, correggi. Lo fai TANTE volte, finche' tutti
    traducono bene."

Q8) loss ~ 0.69 (= -log(0.5)). Accuracy ~ 0.5.


MINI-ESERCIZI INLINE

1.1.A) shapes: P (10,), Z1 (10,8), H (10,8), Z2 (10,1). H >= 0 ovunque,
       P in (0,1).

1.1.B) Per bce_loss(P, y) serve P shape (N,) e y shape (N,). Se P
       restasse (N,1) avresti broadcasting "fittizio" e formula corretta
       ma rischio di bug (np.mean su shape diverse).

1.2.A) sigmoid e' invertibile in (0,1) ma serve Z2; e ricostruire H da
       Z2 richiede invertire H @ W2 + b2 (non univoco se h > 1). Quindi
       e' molto piu' semplice memorizzare durante forward.

2.1.A) dL/dZ2 = [-0.0333, 0.1333, -0.1].reshape(-1, 1)
       shape (3, 1).

2.2.A) dL/dW2 = H.T @ dL_dZ2 shape (2, 1).
       dL/db2 = dL_dZ2.sum(axis=0) shape (1,).

2.3.A) dL/dH shape (3, 2).

2.4.A) Elementi con Z1 < 0 (es. (0,1), (2,0)) hanno dL/dZ1 = 0 -> "spenti".

2.5.A) dL/dW1 shape (3, 2). dL/db1 shape (2,).

2.6.A) shape grads: W1 (5,8), b1 (8,), W2 (8,1), b2 (1,) ok.

3.1.A) Tutti i max_diff < 1e-6 (di solito).
3.1.B) Con /N rimosso, max_diff per W1 e b1 cresce di ~10 (= N) volte.

4.1.A) loss < 0.2, accuracy > 0.95.
4.2.A) accuracy 1.0 su XOR (4 pratiche).
4.3.A) lr=0.001 lentissimo (loss ancora ~0.6). lr=0.01 buono ma lento.
       lr=0.1 ottimo. lr=1.0 oscilla.

5.1.A) File creati nelle figures/.


QUIZ DI VERIFICA

V1) Training loop = "ripeti: forward + backward + update".

V2) Per il backward serve Z1, H, Z2 (non solo P) per applicare la chain
    rule "step-by-step". Memorizzi in forward per non ricalcolare.

V3) grad_W1 (4, 8), grad_b1 (8,), grad_W2 (8, 1), grad_b2 (1,).

V4) Sanity check = confronto backward analitico vs gradiente numerico.
    Fallo PRIMA di addestrare: se hai bug nei gradienti, la loss
    "scendera' a caso" e penserai che lr/architettura sono sbagliate.

V5) Dimentica il /N (media sul batch). Senza /N i gradienti sono N volte
    piu' grandi -> lr effettivo "esplode" -> divergenza.

V6) ~0.693 (= log(2)). Predizioni P ~ 0.5 (pesi random) -> BCE = -log(0.5)
    sia per y=0 sia per y=1.

V7) (d) e' la loss minima possibile su un dataset di label CASUALI o
    quando la rete prevede sempre 0.5. Se hai 500 epoche e ancora 0.69,
    qualcosa non funziona (lr=0, backward spento, dataset banale).

V8) Esempio: "Hai un ricettario con un piatto da imparare. Provi a
    cucinarlo, assaggi, capisci cosa non va. Aggiusti gli ingredienti.
    Riprovi. Ogni ripetizione (= epoch) la ricetta si avvicina alla
    versione ottima. Quando il piatto e' quasi perfetto, smetti."

V9) Vanishing gradient: la sigmoid satura -> derivata ~ 0 per |z| > 3.
    Con piu' layer di sigmoid il gradiente per i primi layer e' ~0 ->
    non imparano -> XOR non si risolve (la rete resta a ~50%).

V10) (1) mini-batch SGD per ridurre memoria, (2) StandardScaler per
     stabilizzare GD, (3) train/val/test split (no overfitting).


CHECKPOINT

C1) Backprop = algoritmo per calcolare i gradienti di una rete usando
    la chain rule (5 derivate locali per W1, 3 per W2 in una rete 2-layer).
    "Propaga indietro" l'errore dall'output ai pesi.

C2) Training loop = forward (calcoli P + loss), backward (calcoli gradienti),
    update (sposti i pesi contro il gradiente). Ripeti per N epoche.

C3) Random: ~0.5 (chance). Addestrata: >> 0.5 (dipende dal dataset, ma
    sui dataset M2/M3 tipicamente 0.85-0.95).

C4) (1) dZ2 = (P - y).reshape(-1, 1) / N
    (2) grad_W2 = H.T @ dZ2;  grad_b2 = dZ2.sum(0)
    (3) dH = dZ2 @ W2.T
    (4) dZ1 = dH * derivata_relu(Z1)
    (5) grad_W1 = X.T @ dZ1;  grad_b1 = dZ1.sum(0)

C5) dL/dz = p - y (semplificazione miracolosa, cap.04).

C6) Chain rule = "moltiplica le derivate locali lungo la catena". Per
    dL/dW1: dL/dZ2 -> dL/dH (* W2.T) -> dL/dZ1 (* d_relu(Z1)) -> dL/dW1
    (= X.T @ dL/dZ1).

C7) He init: W = N(0, 1) * sqrt(2 / n_in). E' "He" dal nome
    dell'autore (Kaiming He). Adatta per layer con ReLU (compensa il
    fatto che ReLU "spegne" la meta' degli input).
"""


# ==========================================================================
# NOTE PER IL CAPITOLO SUCCESSIVO (cap.07 - PyTorch)
# ==========================================================================
#
# Hai chiuso il PRIMO BLOCCO del modulo (cap.01-06):
#   neurone manuale -> rete 2-layer -> rete ADDESTRATA in NumPy puro.
#
# Cosa ti aspetta nel cap.07 (PyTorch):
#   - tutto quello che hai scritto a mano (forward + backward + update)
#     diventa 5 righe di PyTorch
#   - `model.forward()` invece di forward_2layer
#   - `loss.backward()` invece di backward_2layer (autograd lo calcola
#     automaticamente con la chain rule)
#   - `optimizer.step()` invece di W1 -= lr * grad_W1
#
# La COMPRENSIONE che hai costruito qui ti permette di CAPIRE PyTorch,
# non solo di usarlo. Quando qualcosa va storto in PyTorch, saprai
# guardare "sotto il cofano".
#
# Prima di aprire il cap.07, fai il bridge ripasso:
#   modulo_03_dl_cv/quiz_ripasso_tra_capitoli/
#       M03_R06_after_C06_before_C07_backprop_to_pytorch.md


# ==========================================================================
# ENTRY POINT
# ==========================================================================
if __name__ == "__main__":
    print("=" * 70)
    print("Cap.06 M3 - BACKPROP + TRAINING - demo")
    print("=" * 70)

    # Dati sintetici "facili"
    rng = np.random.default_rng(0)
    N, d = 200, 5
    X = rng.standard_normal((N, d))
    y = (X[:, 0] + X[:, 1] > 0).astype(float)

    # Sanity check al passo 0
    print("\n[Sanity check al passo 0 - pesi random]")
    W1 = he_init(d, 8, seed=0)
    b1 = np.zeros(8)
    W2 = he_init(8, 1, seed=1)
    b2 = np.zeros(1)
    sc = sanity_check_grad(X, y, W1, b1, W2, b2)
    for k, v in sc.items():
        print(f"  {k}: {v}")

    # Training su dataset facile
    print("\n[Training rete 2-layer su dataset lineare]")
    history = train_rete_2_layer(X, y, h=16, lr=0.1, n_epochs=200,
                                  verbose=True, log_every=40)
    print(f"\nLoss finale: {history['loss_history'][-1]:.4f}")
    print(f"Acc finale:  {history['acc_history'][-1]:.4f}")

    # Grafici
    figures_dir = os.path.join(os.path.dirname(__file__), "figures")
    grafico_loss_curve(history, out_path=os.path.join(figures_dir, "06_demo_loss_curve.png"))
    print(f"\n  -> {figures_dir}/06_demo_loss_curve.png")

    print("\n" + "=" * 70)
    print("Demo finite. Adesso tocca a te:")
    print("  - 14 mini-esercizi inline (sez 1-5)")
    print("  - 8 TODO base (1-8)")
    print("  - 5 TODO recall cap.01-05 M3 (9-13)")
    print("  - 1 pipeline integrata (train_rete_2_layer_completo)")
    print("  - 1 mini-progetto FINALE (train_rete_su_csv_m2)")
    print("  - 6 TODO tipologie (colloquio/refactor/debug/retrieval/INT/RW)")
    print("  - 1 CONFRONTO PRIMA/DOPO cap.01-06 (chiusura primo blocco)")
    print("  - 10 quiz verifica + checkpoint")
    print("Quando hai finito: 'ho finito cap.06 M3' -> chiusura + voto.")
    print("=" * 70)
