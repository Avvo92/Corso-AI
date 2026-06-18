"""
============================================================================
MODULO 3 (DL & CV) - CAPITOLO 05
"CHAIN RULE + GRADIENT DESCENT": la ricetta della correzione
============================================================================

Terzo dei 4 sotto-capitoli del vecchio "Backpropagation". Mappa:

    03_loss.py                  (loss BCE, MSE)               ← FATTO
    04_derivate_gradiente.py    (derivata, gradiente)         ← FATTO
    05_chain_rule_gd.py         ← QUESTO FILE
    06_backprop_training.py     (backward 2-layer + training loop)

Filosofia (richiesta studente): tanti esercizi pratici, pipeline complete,
richiami forti ai capitoli precedenti DI QUESTO MODULO.

----------------------------------------------------------------------------
DA DOVE ARRIVI (cap.04 DERIVATE)
----------------------------------------------------------------------------
Hai imparato:
  - derivata = pendenza
  - gradiente = vettore di derivate parziali
  - derivata sigmoid (max 0.25)
  - derivata BCE rispetto al logit z = (p - y) (semplificazione miracolosa)

Ti mancano DUE pezzi per chiudere la pipeline:

  (1) Come COMBINARE piu' derivate quando una funzione e' "composizione"
      di altre? -> CHAIN RULE (cap.05, qui)
  (2) Come USARE il gradiente per CORREGGERE i pesi? -> GRADIENT DESCENT
      (cap.05, qui)

Nel cap.06 metterai entrambe insieme sulla rete 2-layer (backprop completo).

----------------------------------------------------------------------------
DEFINITION OF DONE (cap.05)
----------------------------------------------------------------------------
Alla fine sai rispondere in 1 riga + in CODICE a:

  1) Cos'e' la CHAIN RULE? Quando si applica?
  2) Hai f(x) = sin(x^2). Quanto vale f'(x)?
  3) Cos'e' il GRADIENT DESCENT in 1 riga?
  4) Che ruolo ha il LEARNING RATE? Cosa succede se troppo grande?
                                     E se troppo piccolo?
  5) [Qualitativo] In una rete 2-layer, per calcolare il gradiente
     rispetto a W1, quante derivate si moltiplicano (e quali)?

Hai aggiunto al toolkit:

  - gradient_descent_1d      (per funzioni di 1 variabile)
  - gradient_descent_nd      (per funzioni multivariate)
  - chain_rule_2step         (helper per chain rule a 2 livelli)
  - traiettoria_gd_2d        (per visualizzare la convergenza)

----------------------------------------------------------------------------
MAPPA DEL CAPITOLO
----------------------------------------------------------------------------
   *  PRONTUARIO TRANELLI                       [C1] - [C6]
   *  QUIZ D'INGRESSO                           Q1 - Q7
   *  SEZIONE 1  Chain rule intuitiva (2 livelli)  1.1 - 1.3
                  con 4 mini-esercizi inline
   *  🔁 RINFORZO MIRATO cap.04 (p-y)             R1 - R6  retrieval backward
   *  SEZIONE 2  Chain rule multilivello          2.1 - 2.2
                  con 3 mini-esercizi inline
   *  SEZIONE 3  Chain rule QUALITATIVA su rete   3.1 - 3.2
                  (la mappa logica della backprop)
   *  SEZIONE 4  Gradient descent (1 variabile)   4.1 - 4.3
                  con 4 mini-esercizi inline
   *  SEZIONE 5  Effetto del LEARNING RATE        5.1 - 5.2
                  con 3 mini-esercizi inline
   *  SEZIONE 6  Gradient descent (multivariato)  6.1 - 6.2
                  + visualizzazione "piano dei pesi"
   *  TODO MIRATI BASE                           TODO 1 - 6
   *  RINFORZI CAP.01-04 M3                      TODO 7 - 11
   *  PIPELINE INTEGRATA                         addestramento_via_gradiente_numerico()
                  1 neurone addestrato con GD + grad. numerico su BCE
   *  TIPOLOGIE STANDARD                         TODO 12 - 17
   *  QUIZ DI VERIFICA                           V1 - V8
   *  MINI-PROGETTO FINALE                       confronto_lr_su_addestramento()
   *  CHECKPOINT FINALE                          C1 - C5
   *  SOLUZIONI                                  in fondo

Conta esercizi: ~23 mini-inline (incl. RINFORZO MIRATO R1-R6) + 17 TODO + 1 pipeline + 1 mini-progetto.
"""

import os
from typing import Callable

import numpy as np
import matplotlib.pyplot as plt
from numpy.typing import NDArray


# ==========================================================================
# FUNZIONI RIUTILIZZABILI (recall cap.03-04 + nuove di questo capitolo)
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


def bce_loss(
    p: NDArray[np.float64],
    y: NDArray[np.int64] | NDArray[np.float64],
    eps: float = 1e-12,
) -> float:
    p_safe = np.clip(p, eps, 1.0 - eps)
    return float(np.mean(- y * np.log(p_safe) - (1.0 - y) * np.log(1.0 - p_safe)))


def derivata_numerica(f: Callable[[float], float], x: float, h: float = 1e-6) -> float:
    return (f(x + h) - f(x - h)) / (2.0 * h)


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


# Nuove di questo capitolo

def gradient_descent_1d(
    f: Callable[[float], float],
    x0: float,
    lr: float,
    n_steps: int,
) -> list[float]:
    """Gradient descent per funzioni di 1 variabile. Usa derivata numerica.

    Ritorna la lista di x visitati (per visualizzare la traiettoria).
    """
    traiettoria = [x0]
    x = x0
    for _ in range(n_steps):
        grad = derivata_numerica(f, x)
        x = x - lr * grad
        traiettoria.append(x)
    return traiettoria


def gradient_descent_nd(
    f: Callable[[NDArray[np.float64]], float],
    x0: NDArray[np.float64],
    lr: float,
    n_steps: int,
) -> list[NDArray[np.float64]]:
    """Gradient descent per funzioni multivariate (gradiente numerico)."""
    traiettoria = [x0.copy()]
    x = x0.copy()
    for _ in range(n_steps):
        grad = gradiente_numerico(f, x)
        x = x - lr * grad
        traiettoria.append(x.copy())
    return traiettoria


# ==========================================================================
# PRONTUARIO TRANELLI - 5 minuti
# ==========================================================================
#
# [C1] CHAIN RULE = "moltiplica le derivate locali".
#      Se y = f(g(x)) allora dy/dx = f'(g(x)) * g'(x).
#      Catena: y -> f -> g -> x. Vai INDIETRO moltiplicando derivate.
#      In Python e' come "stack di funzioni" che decomponi 1 alla volta.
#
# [C2] GRADIENT DESCENT = "fai un passetto contro il gradiente":
#          x_nuovo = x_vecchio - lr * grad
#      lr = learning rate = "quanto e' grande il passetto".
#
# [C3] LEARNING RATE - 3 scenari:
#      - lr troppo PICCOLO: convergenza lentissima (a volte mai).
#      - lr troppo GRANDE:  oscillazione o divergenza (loss esplode).
#      - lr ben scelto:     convergenza in 50-500 step.
#      Tipici: 0.001 - 0.1. Va sperimentato (hyperparameter tuning).
#
# [C4] CONVERGENZA NON GARANTITA. Il GD trova UN minimo locale, non
#      necessariamente il GLOBALE. Per le reti neurali sopravvive perche'
#      il paesaggio della loss in alte dimensioni e' "amico" (i minimi
#      locali sono per lo piu' "buoni minimi"). Vero solo SE i pesi
#      iniziali e l'lr sono ragionevoli.
#
# [C5] CHAIN RULE su una RETE: per W1 (primo layer) devi moltiplicare
#      5 derivate locali:
#          dL/dW1 = dL/dP * dP/dZ2 * dZ2/dH * dH/dZ1 * dZ1/dW1
#      Per W2 (ultimo): solo 3:
#          dL/dW2 = dL/dP * dP/dZ2 * dZ2/dW2
#      Lo facciamo IN CODICE al cap.06. Qui solo qualitativo.
#
# [C6] FORMULA AGGIORNAMENTO PESI per il TRAINING:
#          W -= lr * dL/dW       (per ogni parametro)
#      Il "-=" perche' vogliamo SCENDERE la loss (contro il gradiente
#      che punta in salita).


# ==========================================================================
# QUIZ D'INGRESSO - cerniera cap.04 -> cap.05
# ==========================================================================

# Q1) [Recall cap.04] La derivata di sigmoid(z) e' s(z)*(1-s(z)). Quanto
#     vale in z = 0? E in z = 10? Cosa significa per il vanishing gradient?
# TUA RISPOSTA:
# in 0 vale 0.25. in 10 vale circa 4.539574272044433e-05. E' molto facile, soprattutto per diversi layer di sigmoidi uno dopo l'altro, avere un gradiente che diventa troppo piccolo (circa 0.25^n_layer_sigmoidi). 


# Q2) [Recall cap.04] Hai p = sigmoid(z), L(p, y) = BCE. La derivata di
#     L rispetto a z e' (p - y). Da dove arriva questa semplificazione?
# GUIDA (se bloccato — completa i 4 passi, NON copiare la loss intera):
#   Passo 1: chain rule -> dL/dz = (dL/dp) * (dp/dz)
#   Passo 2: dL/dp = (p - y) / (p * (1 - p))
#   Passo 3: dp/dz = p * (1 - p)
#   Passo 4: moltiplica -> i p(1-p) si cancellano -> p - y
# TUA RISPOSTA:
# Questa è la semplificazione miracolosa, che si applica però solo per BCE + sigmoid. Dato che il rapporto tra derivata della BCE e derivata del logit di partenza (dL / dz) è sostanzialmente dL/dp * dp/dz si ha -> (p-y)/p(1-p)*p(1-p) = p - y.

# Q3) [Recall cap.03 LOSS] Spiega in 1 riga perche' la BCE va calcolata
#     su PROBABILITA' continue e non su predizioni binarie (P>=0.5).
# TUA RISPOSTA:
# Perchè la BCE loss in pratica giudica la sicurezza del modello, e per farlo ha bisogno di avere una percentuale, ossia un valore continuo. E' la differenza tra BCE e accuracy_score.

# Q4) [Recall cap.02 M3] In una rete 2-layer hai input X shape (N, d),
#     W1 shape (d, h), W2 shape (h, 1). Quante operazioni elementari
#     fa il forward (per ogni pratica)?
#     Suggerimento: pensa a un dot product W1 -> Z1, attivazione,
#     dot product W2 -> Z2, attivazione.
# TUA RISPOSTA:
# *d*h + *h*1

# Q5) [Intuizione] Hai f(x) = (x - 3)^2. Sei in x = 0. In che direzione
#     devi muoverti per FAR SCENDERE f? (+x o -x?) Spiega in 1 riga.
# TUA RISPOSTA:
# +x. Devo movermi nella direzione che porta il risultato delle operazioni svolte nella parentesi verso 0, che è il valore di x per cui la funzione produce valore minimo.

# Q6) [💬 Feynman] Spiega in 4 righe il GRADIENT DESCENT a un collega
#     web dev. VIETATO: gradiente, derivata, funzione, pesi.
# TUA RISPOSTA:

# Immagina di voler abbassare un numero che misura quanto sbagli -> alto = male  -> basso = bene.
# Parti da un punto qualsiasi.
# Provi una piccola modifica e guardi se il punteggio scende o sale.
# Se è sceso → fai un altro passetto nella stessa direzione (magari più piccolo).
# Se è salito → vai dall’altra parte.
# Ripeti finché il punteggio non smette di migliorare.

# Q7) [Prevedi output] Cosa stampa?
#       x = 10.0
#       for _ in range(3):
#           x = x - 0.1 * (2 * x)     # derivata di x^2 e' 2x; lr = 0.1
#           print(round(x, 4))
# Suggerimento: ogni step moltiplica x per (1 - 0.2) = 0.8.
# TUA RISPOSTA:
# 8
# 6.4
# 5.12

# ==========================================================================
# SEZIONE 1 - CHAIN RULE intuitiva (2 livelli)
# ==========================================================================
#
# ANALOGIA: una catena di trasformatori in serie. Ogni "scatola" prende
# l'output del precedente e lo trasforma. Se chiedi "se cambio l'input
# di poco, di quanto cambia l'output finale?", la risposta e':
# moltiplica le SENSIBILITA' (= derivate) di OGNI scatola.
#
# Formula (a 2 livelli):
#     se h(x) = f(g(x)), allora h'(x) = f'(g(x)) * g'(x)
#
# In codice (per visualizzarla):
#     x_punto = x0
#     interno = g(x_punto)         # output intermedio
#     d_interno = g'(x_punto)      # derivata locale di g
#     d_finale = f'(interno)        # derivata locale di f, valutata in interno
#     deriv_totale = d_finale * d_interno


# 1.1 - ESEMPIO MINIMALE


def chain_rule_2step(
    f_prime: Callable[[float], float],
    g: Callable[[float], float],
    g_prime: Callable[[float], float],
    x: float,
) -> float:
    """Calcola la derivata di h(x) = f(g(x)) usando la chain rule.

    Args:
        f_prime: derivata di f
        g:       funzione interna
        g_prime: derivata di g
        x:       punto in cui calcolare

    Returns:
        h'(x) = f'(g(x)) * g'(x)
    """
    return f_prime(g(x)) * g_prime(x)


# Esempio: h(x) = (3x + 1)^2
#   g(x) = 3x + 1,   g'(x) = 3
#   f(u) = u^2,      f'(u) = 2u
#   h'(x) = f'(g(x)) * g'(x) = 2*(3x+1) * 3 = 6*(3x+1)


def _esempio_chain_rule() -> None:
    """h(x) = (3x + 1)^2. Confronto chain rule vs derivata numerica."""
    g = lambda x: 3.0 * x + 1.0
    g_prime = lambda x: 3.0
    f_prime = lambda u: 2.0 * u
    h = lambda x: (3.0 * x + 1.0) ** 2

    for x in [0.0, 1.0, 2.0, -1.0]:
        ana = chain_rule_2step(f_prime, g, g_prime, x)
        num = derivata_numerica(h, x)
        print(f"x = {x:>5.1f}  chain rule = {ana:>10.4f}  numerica = {num:>10.4f}")


# 🔵 MINI-ESERCIZIO INLINE 1.1.A (~5 minuti) — chain rule su 3 composizioni
# Per ognuna, calcola h'(x) prima a mano e poi verifica con derivata_numerica:
#   1) h(x) = (x^2 + 1)^3
#      decomponi: g(x) = x^2 + 1 (g'(x) = 2x),  f(u) = u^3 (f'(u) = 3u^2)
#      h'(x) = 3*(x^2 + 1)^2 * 2x = 6x * (x^2 + 1)^2
#   2) h(x) = sin(x^2)
#      decomponi: g(x) = x^2,  f(u) = sin(u)
#      h'(x) = cos(x^2) * 2x
#   3) h(x) = e^(2x + 1)
#      decomponi: g(x) = 2x + 1,  f(u) = e^u
#      h'(x) = e^(2x + 1) * 2
# Verifica in x = 1 per ognuna.
# TUO CODICE QUI:

# 1)  h(x) = (x^2 + 1)^3
g = lambda x: x**2 + 1
f = lambda x: x**3
h = lambda x: f(g(x))
g_prime = lambda x: 2*x
f_prime = lambda x: 3*x**2

h_prime = lambda x: 3*(x**2+1)**2 * 2*x
h_prima_chain = lambda x: f_prime(g(x)) * g_prime(x)

# 1.2 - CHAIN RULE come "moltiplicazione di sensibilita'"

# 🔵 MINI-ESERCIZIO INLINE 1.2.A (~5 minuti) — spiegazione operativa
# Scrivi in 3 righe (commento) cosa significa la chain rule INTUITIVAMENTE:
# "se l'input di x cambia di poco, di quanto cambia l'output finale?
#  Devo moltiplicare le sensibilita' (= derivate locali) di ogni
#  trasformazione intermedia."
# Esempio: se g raddoppia l'input (g' = 2) e f triplica (f' = 3),
# allora h = f(g(...)) moltiplica per 6.
# TUO COMMENTO QUI:


# 1.3 - CONNESSIONE con la sigmoid + BCE (recall cap.04)

# 🔵 MINI-ESERCIZIO INLINE 1.3.A (~5 minuti) — chain rule per "sigmoid composta"
# Sia h(x) = sigmoid(2 * x + 1). Calcola h'(x):
#   g(x) = 2 * x + 1,  g'(x) = 2
#   f(u) = sigmoid(u), f'(u) = sigmoid(u) * (1 - sigmoid(u))
#   h'(x) = sigmoid(g(x)) * (1 - sigmoid(g(x))) * 2
# Verifica in x = 0, 1, -1 con derivata_numerica.
# TUO CODICE QUI:


# ==========================================================================
# 🔁 RINFORZO MIRATO cap.04 — BCE + sigmoid → dL/dz = p - y
# ==========================================================================
#
# Al cap.04 hai visto la "semplificazione miracolosa". Qui la ripassiamo con
# RETRIEVAL progressivo, collegandola alla chain rule (questo capitolo) e al
# backward del cap.06.
#
# CATENA (un campione, prima della loss media sul batch):
#
#   z  ----sigmoid---->  p  ----BCE---->  L
#   ^                    ^               ^
#  logit            probabilita'        loss
#
# BACKWARD (idea): parti da L e torni INDIETRO verso z moltiplicando le
# derivate locali. La formula "magica" e' il primo anello dopo la loss:
#
#   dL/dz = (dL/dp) * (dp/dz)
#         = (p-y)/(p(1-p)) * p(1-p)
#         = p - y
#
# Nel codice del cap.06 vedrai:  dZ2 = P - y   (un solo passaggio sul batch)


# 🔵 RINFORZO R1 (~3 minuti) — schema a parole (senza formule lunghe)
# Completa in 4 righe (commento):
#   1) Cosa e' z? Cosa e' p? Come sono legati?
#   2) Cosa chiede dL/dz (rispetto a quale variabile)?
#   3) Perche' non calcoli dL/dz "diretto" ma passi da dL/dp e dp/dz?
#   4) Perche' nel backward userai spesso P - y invece di ricalcolare tutto?
# TUO COMMENTO QUI:


# 🔵 RINFORZO R2 (~5 minuti) — retrieval formule (senza guardare cap.04)
# Per UN campione (y fissato 0 o 1):
#   Scrivi a mano (commento) le due derivate locali:
#     dL/dp = ?
#     dp/dz = ?     (con p = sigmoid(z))
# Poi moltiplica e mostra la cancellazione di p(1-p).
# TUO COMMENTO QUI:


# 🔵 RINFORZO R3 (~8 minuti) — numerico vs analitico su z
# Per z = np.array([-2.0, 0.0, 2.0]) e y = np.array([1, 0, 1]):
#   p = sigmoid(z)
#   ana = (p - y) / len(z)          # media BCE sul batch (come cap.04 TODO 6)
#   num = gradiente_numerico(
#       lambda z_vec: bce_loss(sigmoid(z_vec), y),
#       z.astype(float),
#   )
#   assert np.allclose(ana, num)
#   stampa ana e num
# TUO CODICE QUI:


# 🔵 RINFORZO R4 (~8 minuti) — retrieval dL/dp (cap.04 TODO 5)
# Per p = np.array([0.9, 0.1, 0.7]), y = np.array([1, 0, 1]):
#   ana = ((p - y) / (p * (1 - p))) / len(p)
#   num = gradiente_numerico(lambda p_vec: bce_loss(p_vec, y), p.astype(float))
#   assert np.allclose(ana, num)
# Perche' qui NON basta p - y? (Risposta: stai derivando rispetto a p, non a z.)
# TUO CODICE + 1 RIGA COMMENTO:


# 🔵 RINFORZO R5 (~10 minuti) — chain rule su 1 neurone (collegamento cap.04 TODO 7)
# Neurone: y = sigmoid(w*x + b). Loss: L = BCE(y_pred, y_vera) con y_vera=1.
# Per x=2, w=0.5, b=0.1:
#   1) Calcola dL/dz con la semplificazione (z = w*x+b, p = sigmoid(z)):
#        dL/dz = p - y_vera
#   2) Chain rule fino a w: dL/dw = (dL/dz) * (dz/dw) = (p - y) * x
#   3) Verifica dL/dw con gradiente_numerico su w
#   4) Stampa ana e num
# TUO CODICE QUI:


# 🔵 RINFORZO R6 (~5 minuti) — trappola + Feynman
# A) Perche' dL/dz = p - y vale SOLO con sigmoid + BCE?
#    (1 riga: cosa si cancella e perche' con ReLU non succede.)
# B) In 3 righe spiega il backward a un collega:
#    "Parto dalla loss, torno indietro fino al logit, e li trovo P - y."
# TUO COMMENTO QUI:


# ==========================================================================
# SEZIONE 2 - CHAIN RULE multilivello
# ==========================================================================
#
# La chain rule si estende a tutti i livelli che vuoi:
#   se y = f(g(h(x))), allora y' = f'(g(h(x))) * g'(h(x)) * h'(x)
#
# In pratica: vai INDIETRO dall'output all'input, moltiplicando le
# derivate locali.


# 2.1 - 3 livelli

# 🔵 MINI-ESERCIZIO INLINE 2.1.A (~8 minuti) — chain rule a 3 livelli
# Sia y(x) = sin((2x + 1)^2). Decomponi e calcola y'(x):
#   livello 1: h(x) = 2x + 1,     h'(x) = 2
#   livello 2: g(u) = u^2,         g'(u) = 2u
#   livello 3: f(v) = sin(v),      f'(v) = cos(v)
# Quindi y'(x) = f'(g(h(x))) * g'(h(x)) * h'(x)
#              = cos((2x+1)^2) * 2*(2x+1) * 2
#              = 4*(2x+1) * cos((2x+1)^2)
# Verifica in x = 0 e x = 1 con derivata_numerica.
# TUO CODICE QUI:


# 🔵 MINI-ESERCIZIO INLINE 2.1.B (~5 minuti) — chain rule a 4 livelli
# Sia y(x) = exp(sin(cos(x^2))). Conta i 4 livelli:
#   1) h1(x) = x^2,         h1'(x) = 2x
#   2) h2(u) = cos(u),       h2'(u) = -sin(u)
#   3) h3(v) = sin(v),       h3'(v) = cos(v)
#   4) h4(w) = exp(w),       h4'(w) = exp(w)
# Scrivi y'(x) come prodotto di 4 derivate locali. NON serve calcolare,
# basta SCRIVERE la formula. Poi verifica numericamente in x = 0.5.
# TUO COMMENTO + CODICE:


# 2.2 - INTUIZIONE per le reti neurali

# 🔵 MINI-ESERCIZIO INLINE 2.2.A (~3 minuti) — quanti livelli ha una rete
# Una rete 2-layer come quella del cap.02 e' fatta cosi':
#   Z1 = X @ W1 + b1       (livello 1: combinazione lineare)
#   H  = ReLU(Z1)          (livello 2: attivazione)
#   Z2 = H @ W2 + b2       (livello 3: combinazione lineare)
#   P  = sigmoid(Z2)       (livello 4: attivazione)
#   L  = BCE(P, y)         (livello 5: loss)
#
# Per derivare L rispetto a W1, dovrai applicare la chain rule
# attraverso QUANTI livelli? Conta.
# TUA RISPOSTA (in commento):


# ==========================================================================
# SEZIONE 3 - CHAIN RULE QUALITATIVA SU RETE (la mappa)
# ==========================================================================
#
# Non scriveremo codice qui - questa sezione e' la "MAPPA logica" che
# implementeremo al cap.06. Riassume cosa la chain rule deve calcolare
# per la rete 2-layer.
#
# Notazione:
#   X (N, d),  W1 (d, h),  b1 (h,),  W2 (h, 1),  b2 (1,)
#   Z1 = X @ W1 + b1                        (N, h)
#   H  = ReLU(Z1)                           (N, h)
#   Z2 = H @ W2 + b2                        (N, 1)
#   P  = sigmoid(Z2).ravel()                (N,)
#   L  = BCE(P, y)                          scalare
#
# 3.1 - GRADIENTE DI L RISPETTO A W2 (3 livelli)
#
#     dL/dW2 = dL/dZ2 * dZ2/dW2
#
# La parte dL/dZ2 viene dalla semplificazione miracolosa cap.04:
#     dL/dZ2 = P - y          (broadcasting: shape (N,) -> (N, 1))
# Mediato sul batch:
#     dL/dZ2 = (P - y) / N
# Poi:
#     dZ2/dW2 = H (perche' Z2 = H @ W2 + b2 -> derivata di Z2 rispetto a W2 e' H)
# Quindi:
#     dL/dW2 = H^T @ (P - y) / N        shape (h, 1)
#
# 3.2 - GRADIENTE DI L RISPETTO A W1 (5 livelli!)
#
#     dL/dW1 = dL/dZ1 * dZ1/dW1
#     dL/dZ1 = dL/dH * dH/dZ1
#     dL/dH  = dL/dZ2 * dZ2/dH
#
# Tradotto:
#     dL/dZ2 = (P - y) / N                      shape (N, 1)
#     dL/dH  = dL/dZ2 @ W2^T                    shape (N, h)
#     dL/dZ1 = dL/dH * derivata_relu(Z1)        shape (N, h), * elementwise
#     dL/dW1 = X^T @ dL/dZ1                     shape (d, h)
#
# Lo IMPLEMENTI nel cap.06 (e' il backward).
#
# TODO 3 (10 minuti) — Identifica le 5 derivate per dL/dW1
# In un commento, nomina ciascuna delle 5 derivate locali con il loro
# nome "logico" (es. "derivata della BCE rispetto a P", ecc.). NON
# scrivere codice. E' un esercizio di mappatura mentale.
# TUO COMMENTO QUI:


# ==========================================================================
# SEZIONE 4 - GRADIENT DESCENT (1 variabile)
# ==========================================================================
#
# Idea: hai una funzione f(x). Vuoi trovare il MINIMO.
# Sai calcolare la pendenza in ogni x (derivata).
# Ricetta:
#   1) Parti da x_0 (anche a caso)
#   2) Calcola pendenza in x_0: m_0 = f'(x_0)
#   3) Sposta x_0 nella direzione OPPOSTA a m_0 (= scendi):
#         x_1 = x_0 - lr * m_0      lr = learning rate (passetto)
#   4) Ripeti finche' m_i si avvicina a 0 (sei in un minimo)
#
# Funzione: vedi `gradient_descent_1d` in alto.


# 4.1 - GD su una parabola


def _demo_gd_1d() -> None:
    """GD su f(x) = (x - 3)^2. Minimo in x = 3."""
    f = lambda x: (x - 3.0) ** 2
    traiettoria = gradient_descent_1d(f, x0=10.0, lr=0.2, n_steps=20)
    print(f"x0 = 10.0")
    print(f"Step 1 -> x = {traiettoria[1]:.4f}")
    print(f"Step 5 -> x = {traiettoria[5]:.4f}")
    print(f"Step 20 -> x = {traiettoria[20]:.4f}  (minimo atteso: 3.0)")


# 🔵 MINI-ESERCIZIO INLINE 4.1.A (~5 minuti) — applica GD a 3 funzioni
# Per ognuna trova il minimo con gradient_descent_1d (x0=10, n_steps=50):
#   1) f(x) = (x - 5)^2          minimo in x = 5,   prova lr = 0.2
#   2) f(x) = x^2 + 4*x + 4      minimo in x = -2,  prova lr = 0.1
#   3) f(x) = (x - 1)^4          minimo in x = 1,   prova lr = 0.05
# Stampa l'ultimo x della traiettoria per ognuno.
# TUO CODICE QUI:


# 🔵 MINI-ESERCIZIO INLINE 4.1.B (~5 minuti) — quando GD fallisce
# Prova GD con lr troppo grande:
#   f(x) = (x - 3)^2
#   gradient_descent_1d(f, x0=10.0, lr=1.5, n_steps=20)
# Stampa la traiettoria. Cosa noti? (diverge, oscilla, NaN?)
# Spiega in 2 righe perche'.
# TUO CODICE QUI:


# 4.2 - VISUALIZZARE LA TRAIETTORIA


def _grafico_gd_1d_traiettoria(
    out_path: str | None = None,
    show: bool = False,
) -> None:
    """Plot della funzione + traiettoria del GD su parabola.
    Mostra come ogni step "scende" verso il minimo."""
    f = lambda x: (x - 3.0) ** 2
    x = np.linspace(-2, 11, 200)
    y = f(x)
    traiettoria = gradient_descent_1d(f, x0=10.0, lr=0.2, n_steps=30)
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(x, y, color="#1f77b4", label="f(x) = (x - 3)²")
    tx = np.array(traiettoria)
    ty = (tx - 3) ** 2
    ax.plot(tx, ty, "ro-", markersize=4, label="traiettoria GD (lr=0.2)")
    ax.set_xlabel("x")
    ax.set_ylabel("f(x)")
    ax.set_title("Gradient descent: passetto contro il gradiente, ogni volta")
    ax.legend()
    ax.grid(True, alpha=0.3)
    if out_path:
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        fig.savefig(out_path, dpi=120, bbox_inches="tight")
    if show:
        plt.show()
    plt.close(fig)


# 🔵 MINI-ESERCIZIO INLINE 4.2.A (~3 minuti) — genera grafico GD
# Chiama _grafico_gd_1d_traiettoria(out_path="figures/05_01_gd_1d.png")
# e verifica esistenza file.
# TUO CODICE QUI:


# 4.3 - CONDIZIONE DI USCITA (convergenza)

# 🔵 MINI-ESERCIZIO INLINE 4.3.A (~5 minuti) — variant GD con early stop
# Modifica gradient_descent_1d (in una funzione NUOVA, non sovrascrivere):
#   def gradient_descent_1d_early_stop(f, x0, lr, n_steps, tol=1e-6):
#       """Ferma se |grad| < tol oppure se la differenza fra due x consecutivi
#       e' < tol. Ritorna la traiettoria E quante iterazioni ha fatto."""
#       ...
# Test su f(x) = (x - 3)^2, x0=10, lr=0.2. Quante iterazioni servono per
# arrivare a |grad| < 1e-6? (Suggerimento: ~50-100.)
# TUO CODICE QUI:


# ==========================================================================
# SEZIONE 5 - LEARNING RATE: l'ingrediente piu' importante
# ==========================================================================
#
# Lo stesso GD su f(x) = (x-3)^2 si comporta in 3 modi diversi a seconda
# di lr:
#   lr = 0.01:  converge MOLTO lentamente (~500 step)
#   lr = 0.2:   converge BENE (~30 step)
#   lr = 0.9:   oscilla, ma converge (instabile)
#   lr = 1.5:   diverge (loss esplode)
#
# Trovare l'lr giusto e' un'arte. Tipici per reti neurali: 0.001 - 0.1.


def _demo_lr() -> None:
    """Mostra l'effetto di 4 lr diversi su f(x) = (x - 3)^2."""
    f = lambda x: (x - 3.0) ** 2
    print(f"{'lr':>6} {'x dopo 20 step':>18} {'distanza dal minimo':>22}")
    for lr in [0.01, 0.2, 0.9, 1.5]:
        traiettoria = gradient_descent_1d(f, x0=10.0, lr=lr, n_steps=20)
        x_finale = traiettoria[-1]
        print(f"{lr:>6.2f} {x_finale:>18.4f} {abs(x_finale - 3):>22.4f}")


def _grafico_lr_a_confronto(
    out_path: str | None = None,
    show: bool = False,
) -> None:
    """Plot della loss vs step per 4 lr diversi (in scala log y se serve)."""
    f = lambda x: (x - 3.0) ** 2
    fig, ax = plt.subplots(figsize=(10, 5))
    for lr in [0.01, 0.2, 0.9, 1.5]:
        traiettoria = gradient_descent_1d(f, x0=10.0, lr=lr, n_steps=30)
        losses = [f(x) for x in traiettoria]
        ax.plot(range(len(losses)), losses, marker="o", markersize=3,
                label=f"lr = {lr}")
    ax.set_yscale("symlog")
    ax.set_xlabel("Step")
    ax.set_ylabel("Loss (symlog)")
    ax.set_title("Effetto del LEARNING RATE sulla convergenza")
    ax.legend()
    ax.grid(True, alpha=0.3)
    if out_path:
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        fig.savefig(out_path, dpi=120, bbox_inches="tight")
    if show:
        plt.show()
    plt.close(fig)


# 🔵 MINI-ESERCIZIO INLINE 5.1.A (~5 minuti) — replica e interpreta
# Chiama _demo_lr(). Spiega in 3 righe perche':
#   - lr=0.01: lento (passetti piccoli)
#   - lr=0.9:  oscilla (passetti troppo grandi, supera il minimo)
#   - lr=1.5:  diverge (ogni passo ti porta piu' lontano)
# TUO COMMENTO QUI:


# 🔵 MINI-ESERCIZIO INLINE 5.1.B (~3 minuti) — genera grafico lr
# Chiama _grafico_lr_a_confronto(out_path="figures/05_02_lr_confronto.png")
# Verifica esistenza file. Guarda il grafico: con lr=1.5 la loss diverge
# in modo plateau o esponenziale?
# TUO CODICE QUI:


# 5.2 - "LEARNING RATE SWEEP" (mini-hyperparameter tuning)

# 🔵 MINI-ESERCIZIO INLINE 5.2.A (~8 minuti) — trova l'lr ottimo
# Per f(x) = (x - 4)^2 (minimo in x = 4), x0 = 0, n_steps = 30:
#   - Prova lr in [0.001, 0.01, 0.1, 0.3, 0.5, 0.9, 1.0, 1.5]
#   - Per ognuno: distanza finale dal minimo |x_finale - 4|
#   - Stampa una tabella ordinata per "qualita'"
#   - Qual e' l'lr "ottimo" per questo problema?
# TUO CODICE QUI:


# ==========================================================================
# SEZIONE 6 - GRADIENT DESCENT multivariato + piano dei pesi
# ==========================================================================
#
# Stessa ricetta, ma il gradiente e' un VETTORE. Aggiorni tutte le
# componenti contemporaneamente:
#       x_nuovo = x_vecchio - lr * grad_f(x_vecchio)
#
# Vedi `gradient_descent_nd` in alto.


# 6.1 - GD su un paraboloide 2D


def _demo_gd_2d() -> None:
    """GD su f(x, y) = (x - 3)^2 + (y + 2)^2. Minimo in (3, -2)."""
    f = lambda v: float((v[0] - 3.0) ** 2 + (v[1] + 2.0) ** 2)
    x0 = np.array([10.0, 10.0])
    traiettoria = gradient_descent_nd(f, x0, lr=0.2, n_steps=20)
    print(f"x0 = {x0}")
    print(f"Step  5 -> {traiettoria[5]}")
    print(f"Step 20 -> {traiettoria[20]}  (atteso ~ [3, -2])")


def _grafico_gd_2d_traiettoria(
    out_path: str | None = None,
    show: bool = False,
) -> None:
    """Contour della loss + traiettoria del GD (piano dei pesi)."""
    f = lambda v: (v[..., 0] - 3.0) ** 2 + (v[..., 1] + 2.0) ** 2
    x = np.linspace(-2, 12, 100)
    y = np.linspace(-10, 12, 100)
    X, Y = np.meshgrid(x, y)
    F = (X - 3) ** 2 + (Y + 2) ** 2

    f_scalar = lambda v: float((v[0] - 3.0) ** 2 + (v[1] + 2.0) ** 2)
    traiettoria = gradient_descent_nd(f_scalar, np.array([10.0, 10.0]), lr=0.2, n_steps=30)
    tx = np.array([t[0] for t in traiettoria])
    ty = np.array([t[1] for t in traiettoria])

    fig, ax = plt.subplots(figsize=(8, 8))
    ax.contour(X, Y, F, levels=20, colors="gray", alpha=0.5)
    ax.contourf(X, Y, F, levels=20, alpha=0.3, cmap="viridis")
    ax.plot(tx, ty, "ro-", markersize=4, label="traiettoria GD")
    ax.plot(3, -2, "g*", markersize=15, label="minimo (3, -2)")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title("Gradient descent su f(x, y) = (x-3)² + (y+2)²  ('piano dei pesi')")
    ax.legend()
    ax.set_aspect("equal")
    ax.grid(True, alpha=0.3)
    if out_path:
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        fig.savefig(out_path, dpi=120, bbox_inches="tight")
    if show:
        plt.show()
    plt.close(fig)


# 🔵 MINI-ESERCIZIO INLINE 6.1.A (~5 minuti) — GD multivariato a mano
# Per f(x, y) = x^2 + 4*y^2 (minimo in (0, 0)):
#   - x0 = np.array([2.0, 2.0]), lr = 0.1, n_steps = 30
#   - chiama gradient_descent_nd
#   - stampa la traiettoria ogni 5 step
# Qualcosa di strano: la y converge MOLTO piu' velocemente di x. Perche'?
# Suggerimento: la derivata rispetto a y e' 8y (vs 2x per x): gradiente
# piu' grande -> passo piu' lungo. Anisotropia.
# TUO CODICE QUI:


# 🔵 MINI-ESERCIZIO INLINE 6.1.B (~3 minuti) — genera grafico 2D
# Chiama _grafico_gd_2d_traiettoria(out_path="figures/05_03_gd_2d.png")
# Guarda il grafico: la traiettoria scende dritta o "a zig-zag"?
# TUO CODICE QUI:


# 6.2 - CONNESSIONE CON L'ADDESTRAMENTO DELLA RETE
#
# In una rete:
#   - le VARIABILI di GD sono i pesi (W1, b1, W2, b2)
#   - la FUNZIONE da minimizzare e' la loss (BCE su tutto il dataset)
#   - lo SPAZIO ha tante dimensioni quante sono i parametri (es. 49 per
#     una rete con d=4, h=8, 1 output)
#   - non possiamo visualizzarlo, ma vale la stessa logica:
#         "muovi i pesi un po' contro il gradiente, ripeti".
#
# La SOLA DIFFERENZA con cap.05 -> cap.06: il gradiente NON sara' piu'
# numerico (lento), ma analitico (backprop). Stessa formula:
#       W_nuovo = W_vecchio - lr * grad_loss


# ==========================================================================
# TODO MIRATI BASE (1 - 6)
# ==========================================================================

# TODO 1 (10 minuti) — chain rule per la SIGMOID composta
# Sia h(x) = sigmoid(a * x + b) con a = 2, b = -1. Calcola h'(x) usando
# la chain rule e verificalo numericamente in x = 0, 1, 2.
#   - g(x) = a*x + b, g'(x) = a
#   - f(u) = sigmoid(u), f'(u) = sigmoid(u) * (1 - sigmoid(u))
#   - h'(x) = sigmoid(a*x+b) * (1 - sigmoid(a*x+b)) * a
# TUO CODICE QUI:


# TODO 2 (8 minuti) — gradient_descent_1d su 3 funzioni
# Per ognuna delle 3 funzioni qui sotto, trova il minimo con GD
# (x0=10, lr e n_steps a tua scelta):
#   1) f(x) = (x - 7)^2
#   2) f(x) = x^4 - 4*x^2 + 1   (ATTENZIONE: 2 minimi locali!)
#   3) f(x) = abs(x - 5)        (non derivabile in x=5, ma quasi ovunque OK)
# Per ognuna: stampa l'x finale + commento se hai trovato il minimo
# atteso, un minimo locale, o non sei convergente.
# TUO CODICE QUI:


# TODO 3 (15 minuti) — gradient_descent_nd su f(w1, w2) = (w1 - 3)^2 + (w2 + 2)^2
# Setup: x0 = np.array([0.0, 0.0]), lr = 0.3, n_steps = 30.
# Calcola la traiettoria. Stampa:
#   - x0
#   - x dopo 1, 5, 15, 30 step
#   - distanza euclidea dal minimo (3, -2)
# Verifica che converga al minimo.
# TUO CODICE QUI:


# TODO 4 (15 minuti) — confronto GD con 3 lr (sullo stesso problema)
# Per f(x, y) = x^2 + y^2 (minimo in (0, 0)), x0 = np.array([5.0, 5.0]):
#   - prova lr = 0.05, 0.3, 0.99
#   - per ognuno: 30 step
#   - stampa per ognuno la loss finale
#   - costruisci un grafico con 3 traiettorie sovrapposte sul contour plot
#     (vedi _grafico_gd_2d_traiettoria come template)
# Salva in figures/05_04_lr_2d.png.
# TUO CODICE QUI:


# TODO 5 (10 minuti) — GD con gradiente numerico applicato alla BCE
# Per un mini-modello a 1 peso:
#   y = sigmoid(w * x)         con x = 2, y_vera = 1
# Vogliamo trovare il w che MINIMIZZA bce_loss(sigmoid(w*x), y_vera).
#
# Costruisci la funzione:
#   def loss_w(w_vec):
#       p = sigmoid(w_vec[0] * 2.0)
#       return bce_loss(np.array([p]), np.array([1.0]))
#
# Esegui gradient_descent_nd con x0 = np.array([-3.0]), lr = 1.0,
# n_steps = 30. A che valore di w converge? La loss finale?
# TUO CODICE QUI:


# TODO 6 (10 minuti) — derivata della loss rispetto al peso (chain rule + miracolosa)
# Conferma analitica: per il TODO 5, la derivata di loss(w) rispetto a w e':
#   dL/dw = (sigmoid(w*x) - y) * x        (semplificazione miracolosa cap.04!)
# Per (x=2, y=1, w=-3):
#   p = sigmoid(-6) ~ 0.0025
#   dL/dw = (0.0025 - 1) * 2 = -1.995
# Verifica numericamente con gradiente_numerico.
# Cosa significa il segno negativo? (Stiamo aumentando w -> p si avvicina a 1.)
# TUO CODICE QUI:


# ==========================================================================
# RINFORZI CAP.01-04 M3 (TODO 7 - 11)
# ==========================================================================
#
# Nota: i retrieval mirati su dL/dz = p - y sono nella sezione
# 🔁 RINFORZO MIRATO cap.04 (R1-R6) sopra — falli PRIMA di questi TODO
# se il cap.04 ti e' costato fatica.

# TODO 7 (12 minuti) [🧠 RETRIEVAL cap.04 — chiusura p-y]:
# Senza aprire 04_derivate_gradiente.py, in un commento scrivi l'intera
# catena del backward sul logit (4 righe max):
#   z -> p -> L ; dL/dz = dL/dp * dp/dz ; formule ; risultato p - y.
# Poi in codice: verifica su z=[0.0], y=[1] che
#   derivata_numerica(lambda zv: bce_loss(sigmoid(zv), np.array([1.0])), 0.0)
# coincide con sigmoid(0)-1.
# TUO COMMENTO + CODICE QUI:


# TODO 8 (8 minuti) [🔄 RECALL cap.03 LOSS]:
# Riscrivi bce_loss da zero (senza guardare la versione in alto).
# Firma:
#   def my_bce(p, y, eps=1e-12) -> float:
#       """media di -y*log(p) - (1-y)*log(1-p), con clip bilaterale."""
# Verifica con p = np.array([0.9, 0.1, 0.5]), y = np.array([1, 0, 1]).
# TUO CODICE QUI:


# TODO 9 (8 minuti) [🔄 RECALL cap.04 — derivata sigmoid e ReLU]:
# Riscrivi le 2 funzioni:
#   def my_derivata_sigmoid(z): ...
#   def my_derivata_relu(z): ...
# Vettorizzate (no for su elementi). Verifica con z = np.array([-2, 0, 2]).
# TUO CODICE QUI:


# TODO 10 (8 minuti) [🔄 RECALL cap.04 — gradiente_numerico]:
# Riscrivi gradiente_numerico da zero (senza copiare la versione in alto).
# Verifica con f(v) = v[0]^2 + v[1]^2 in (1, -2): atteso [2, -4].
# TUO CODICE QUI:


# TODO 11 (15 minuti) [🔀 INTERLEAVING cap.02 + cap.03 + cap.05]:
# Mini-pipeline "training di 1 step" su una rete 2-layer:
#   1) Setup: X (5, 3), y (5,), W1 (3, 4), W2 (4, 1) random come al solito
#   2) Forward: P = sigmoid(relu(X@W1+b1)@W2+b2).ravel()
#   3) loss_iniziale = bce_loss(P, y)
#   4) Calcola gradiente numerico della loss rispetto a W2 (8 valori):
#        - "flatten" W2 in un vettore di 8 elementi
#        - definisci una funzione f(W2_flat) -> loss
#        - applica gradiente_numerico
#   5) Aggiorna W2 con un passo di GD: W2_nuovo = W2 - lr * grad_W2 (con lr=0.1)
#   6) Ricalcola forward + loss_finale.
#   7) Verifica: loss_finale < loss_iniziale? (Dovrebbe SI, ma di poco.)
# TUO CODICE QUI:


# ==========================================================================
# PIPELINE INTEGRATA — addestramento_via_gradiente_numerico
# ==========================================================================
#
# OBIETTIVO: addestrare un MINI-MODELLO (1 neurone, 1 input scalare, 1 peso w
# e 1 bias b) su un dataset binario usando GD + gradiente_numerico.
#
# Dataset:
#   x = np.array([0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0])   # 8 pratiche
#   y = (x > 2.0).astype(int)                                  # label binarie
#
# Modello:
#   p_i = sigmoid(w * x_i + b)
#
# Loss:
#   L(w, b) = bce_loss(p, y)
#
# Algoritmo:
#   - inizializza w = 0.0, b = 0.0
#   - per n_steps = 200 iterazioni:
#       1) calcola P
#       2) calcola loss
#       3) calcola gradiente numerico di L rispetto a [w, b] (vettore di 2)
#       4) aggiorna [w, b] -= lr * grad      (lr = 0.5)
#       5) ogni 20 step, stampa step / loss / w / b / accuracy
#   - stampa risultato finale

# TODO PIPE.1 (25 minuti) — implementa addestramento_via_gradiente_numerico
#
# Firma:
#   def addestramento_via_gradiente_numerico(
#       n_steps: int = 200,
#       lr: float = 0.5,
#       verbose: bool = True,
#   ) -> dict[str, list[float] | float]:
#       """Ritorna:
#         {
#           'loss_history':  lista di n_steps+1 loss
#           'w_history':     lista di n_steps+1 w
#           'b_history':     lista di n_steps+1 b
#           'w_finale':      w dopo n_steps
#           'b_finale':      b dopo n_steps
#           'acc_finale':    accuracy finale
#         }
#       """
#
# Verifica:
#   - alla fine la rete deve raggiungere accuracy = 1.0
#   - w finale dovrebbe essere positivo (perche' "x grande -> y=1")
#   - b finale dovrebbe essere negativo (perche' la soglia e' x=2,
#     quindi sigmoid(w*x + b) = 0.5 quando w*x + b = 0, cioe' x = -b/w ~ 2)
#
# Bonus: dopo la pipeline, plottala come grafico (loss vs step) in
# figures/05_05_addestramento_neurone.png.
# TUO CODICE QUI:


# ==========================================================================
# TIPOLOGIE STANDARD (TODO 12 - 17)
# ==========================================================================

# TODO 12 (15 minuti) [🎯 COLLOQUIO]:
# "Sei in un colloquio. L'intervistatore chiede:
#   (1) Cos'e' la chain rule? 1 frase.
#   (2) Cos'e' il gradient descent? 1 frase.
#   (3) Hai una rete 2-layer; per aggiornare W1 devi moltiplicare
#       quante derivate locali? Quali?
#   (4) Cosa succede se l'lr e' troppo grande? Troppo piccolo?
#   (5) (bonus) Cos'e' la 'semplificazione miracolosa' per BCE + sigmoid?"
# Risposta in 8-10 righe TOTALI.
# TUA RISPOSTA:
# ...


# TODO 13 (15 minuti) [🔧 REFACTORING]:
# Questo GD funziona ma e' brutto. Riscrivilo.
#
#   def gd_brutto(f, x, lr, n):
#       lista = []
#       lista.append(x)
#       for i in range(0, n):
#           h = 1e-6
#           g = (f(x + h) - f(x)) / h        # bug 1: differenza avanti, non centrata
#           x = x - lr * g
#           lista.append(x)
#       return lista, x, lr,                  # bug 2: return tupla a 3 senza motivo
#
# Riscrivila:
#   - differenza CENTRATA
#   - return solo la lista (la x finale e' lista[-1])
#   - type hint
#   - docstring di 2 righe
# Confronta i risultati con gradient_descent_1d su f(x) = (x-3)^2, x0=10, lr=0.2.
# TUO CODICE QUI:


# TODO 14 (15 minuti) [🔍 DEBUG]:
# Questo codice "addestra" un mini-modello, ma la loss SALE invece di scendere.
# Trova il bug.
#
#   def addestra_buggato():
#       x_dati = np.array([1.0, 2.0, 3.0])
#       y_dati = np.array([0, 1, 1])
#       w = 0.0
#       lr = 0.1
#       for _ in range(20):
#           p = sigmoid(w * x_dati)
#           loss = bce_loss(p, y_dati)
#           # bug: il segno!
#           w = w + lr * np.mean((p - y_dati) * x_dati)
#           print(loss)
#       return w, loss
#
# Spiega il bug e dai la versione corretta.
# TUO COMMENTO + FIX:
# ...


# TODO 15 (15 minuti) [🧠 RETRIEVAL cap.04]:
# Senza guardare il cap.04, riscrivi da zero:
#   - derivata_sigmoid(z)        (formula: s(z) * (1 - s(z)))
#   - derivata_relu(z)           (formula: 1 se z > 0, 0 altrimenti)
#   - gradiente_numerico(f, x)   (differenza centrata, una coord alla volta)
# Verifica che le tue versioni coincidano con quelle in alto su 5 punti.
# TUO CODICE QUI:


# TODO 16 (20 minuti) [🔀 INTERLEAVING cap.02 + cap.04 + cap.05]:
# Vuoi addestrare la RETE 2-LAYER su un mini-dataset usando GD + grad numerico:
#   1) Setup random come al solito (N=20, d=3, h=4)
#   2) Etichette: y = (X[:, 0] + X[:, 1] > 0).astype(int)
#   3) Forward + loss
#   4) Definisci una "loss function" che riceve un VETTORE flat di TUTTI i
#      parametri (W1 + b1 + W2 + b2 = 3*4 + 4 + 4*1 + 1 = 21 parametri)
#      e ritorna la loss BCE.
#   5) Inizializza parametri random (He init: W * sqrt(2/d_input))
#   6) Esegui gradient_descent_nd per 50 step (lr = 0.5)
#   7) Stampa loss + accuracy ogni 10 step.
# ATTENZIONE: gradiente_numerico fa 2 chiamate per parametro per step ->
# 21 * 2 * 50 = 2100 forward. Sara' LENTO (~secondi). E' il punto: al
# cap.06 sostituiremo questo con backprop analitico (1 sola forward + 1
# backward per step).
# TUO CODICE QUI:


# TODO 17 (15 minuti) [🌊 REAL-WORLD]:
# "Un collega ti dice: 'ho addestrato la rete, l'lr e' 0.001, dopo 1000
# epoche la loss e' ancora 0.69. Cosa faccio?'"
# Suggerisci 3-4 cose da provare (e perche'). Esempi (in commento):
#   1) provare lr piu' grande (es. 0.01 o 0.1) - convergenza lenta
#   2) verificare che i dati siano standardizzati - feature con scale
#      molto diverse rallentano GD
#   3) controllare l'inizializzazione - He init aiuta con ReLU
#   4) verificare che il dataset NON sia banale (es. tutti y=0 -> rete
#      che prevede 0.5 e' ottima -> BCE = 0.69 e' il minimo possibile!)
# TUA RISPOSTA + (bonus) verifica numerica del caso (4):
# ...


# ==========================================================================
# QUIZ DI VERIFICA (V1 - V8)
# ==========================================================================

# V1) Cos'e' la chain rule in 1 riga? E in 1 formula su 2 livelli?
# TUA RISPOSTA:
# ...

# V2) Hai h(x) = sin(x^2). Quanto vale h'(x)?
# TUA RISPOSTA:
# ...

# V3) Cos'e' il gradient descent in 1 riga? Qual e' l'aggiornamento dei
#     pesi (formula a parole)?
# TUA RISPOSTA:
# ...

# V4) Cosa succede al GD se lr e' troppo grande? Troppo piccolo?
#     Cita 1 sintomo per ognuno.
# TUA RISPOSTA:
# ...

# V5) [Trova l'errore] Questo codice "addestra" ma sbaglia:
#       w = 0
#       for _ in range(100):
#           grad = derivata_numerica(loss, w)
#           w = w + 0.1 * grad        # bug
# Quale e' il bug? E perche'?
# TUA RISPOSTA:
# ...

# V6) [Prevedi output] Per f(x) = x^2, x0 = 5, lr = 0.1:
#       step 1: x = 5 - 0.1 * 10 = 4
#       step 2: x = 4 - 0.1 *  8 = 3.2
#       step 3: x = 3.2 - 0.1 * ? = ?
# Calcola.
# TUA RISPOSTA:
# ...

# V7) Per una rete 2-layer, scrivi (a parole) le 5 derivate locali che
#     devi moltiplicare per ottenere dL/dW1.
# TUA RISPOSTA:
# ...

# V8) [💬 Feynman] Spiega in 4 righe cosa fa il GRADIENT DESCENT a un
#     collega web dev. VIETATO: gradiente, derivata, pendenza, loss,
#     learning rate. Suggerimento: usa l'analogia della discesa al buio.
# TUA RISPOSTA:
# ...


# ==========================================================================
# MINI-PROGETTO FINALE — `confronto_lr_su_addestramento`
# ==========================================================================
#
# OBIETTIVO: confronta 4 learning rate sull'addestramento del mini-neurone
# del PIPE.1, e produci una visualizzazione finale del piano dei pesi
# (w, b) con la traiettoria di ogni lr.

# TODO MINI-PROGETTO (30 minuti):
#
# Firma:
#   def confronto_lr_su_addestramento(
#       lr_da_provare: list[float] = [0.01, 0.1, 0.5, 2.0],
#       n_steps: int = 100,
#   ) -> dict[float, dict[str, list[float] | float]]:
#       """Per ogni lr, addestra il mini-neurone (dataset del PIPE.1)
#       e ritorna un dict con:
#         {
#           lr: {
#             'loss_history': [...],
#             'w_history':    [...],
#             'b_history':    [...],
#             'acc_finale':   float
#           }
#         }
#       """
#
# Poi disegna 1 figura con 4 subplot:
#   1) loss vs step per ogni lr
#   2) traiettoria (w, b) sul piano dei pesi per ogni lr
#   3) sovrapposizione delle accuracy finali (bar chart)
#   4) effetto lr sul tempo di convergenza (n step per loss < 0.1)
# Salva in figures/05_06_confronto_lr.png.
#
# Commenta:
#   - quale lr funziona meglio?
#   - quali divergono?
#   - lr "fortunato" che converge a w/b plausibili?
# TUO CODICE QUI:


# ==========================================================================
# CHECKPOINT FINALE
# ==========================================================================

# C1) In 1 frase: cos'e' la chain rule? E come la useresti per derivare
#     L(p, y) = BCE(sigmoid(z), y) rispetto a z?
# TUA RISPOSTA:
# ...

# C2) Il gradient descent in 2 righe: cosa fa, e quale rischio ha?
# TUA RISPOSTA:
# ...

# C3) [Prevedi] Per f(x) = (x - 3)^2, x0 = 5, lr = 0.3. Dopo 1 step quanto vale x?
#     Suggerimento: derivata in x=5 e' 2*(5-3) = 4. x_nuovo = 5 - 0.3 * 4 = 3.8.
# TUA RISPOSTA:
# ...

# C4) [Recap a parole] Una rete 2-layer ha 49 parametri (con d=4, h=8).
#     Quante derivate parziali devi calcolare per fare 1 step di GD?
#     E con la chain rule "fatta a mano", quante MOLTIPLICAZIONI per W1
#     (assumendo di gia' avere dL/dZ2)?
# TUA RISPOSTA:
# ...

# C5) Auto-rating onesto:
#       - Chain rule a 2 livelli:                 /10
#       - Chain rule multilivello (3+):            /10
#       - Chain rule QUALITATIVA su rete (5 deriv):/10
#       - Gradient descent (formula + intuizione): /10
#       - Effetto del learning rate (3 scenari):   /10
#       - Pipeline addestramento mini-neurone:     /10
# TUE RISPOSTE:
# ...


# ==========================================================================
# SOLUZIONI QUIZ
# ==========================================================================
"""
QUIZ D'INGRESSO

Q1) derivata_sigmoid(0) = 0.5 * 0.5 = 0.25 (massima). In z=10:
    sigmoid(10) ~ 0.9999 -> derivata ~ 9.99e-5. Vanishing: se hai N
    layer di sigmoid e tutti i z sono "grandi", il gradiente dei primi
    layer diventa zero per la chain rule (moltiplicazioni di derivate
    quasi nulle).

Q2) dL/dz = dL/dp * dp/dz = ((p-y)/(p(1-p))) * (p(1-p)) = p - y.
    I p(1-p) si elidono fra derivata BCE rispetto a p (al denominatore)
    e derivata sigmoid rispetto a z (al numeratore).

Q3) BCE = -y*log(p) - (1-y)*log(1-p) e' DERIVABILE in p (continuamente).
    Su predizioni binarie (P>=0.5).astype(int) la BCE darebbe -log(0)=+inf
    per ogni errore -> formula esplode + non e' derivabile -> training
    impossibile.

Q4) Per pratica: dot W1 (h prodotti scalari di lunghezza d), attivazione,
    dot W2 (1 prodotto scalare di lunghezza h), attivazione.
    Operazioni elementari ~ d*h + h*1 = h*(d+1).

Q5) +x. In x=0 la pendenza di (x-3)^2 e' 2*(0-3) = -6 (verso sinistra).
    Devi muoverti in direzione OPPOSTA al gradiente -> +x.

Q6) Esempio: "Vuoi minimizzare il tempo di caricamento di una pagina.
    Provi una piccola modifica e misuri se il tempo migliora o peggiora.
    Sai quanto e' migliorato, fai un passetto piu' deciso in quella
    direzione. Ripeti. Funziona finche' non sei in un minimo."

Q7) Step 1: x = 10 - 0.1 * 20 = 8.
    Step 2: x = 8 - 0.1 * 16 = 6.4.
    Step 3: x = 6.4 - 0.1 * 12.8 = 5.12.


MINI-ESERCIZI INLINE

1.1.A) (1) h'(1) = 6*1 * (1^2 + 1)^2 = 24. (2) h'(1) = cos(1) * 2 ~ 1.08.
       (3) h'(1) = e^3 * 2 ~ 40.17. Tutti coincidono con numerico.

1.2.A) "Se la prima trasformazione raddoppia (g'=2) e la seconda triplica
       (f'=3), allora un cambio di 1 nell'input dell'intera catena
       produce 6 di cambio nell'output (2*3)."

1.3.A) h'(0) = sigmoid(1) * (1 - sigmoid(1)) * 2 ~ 0.731 * 0.269 * 2 ~ 0.393.
       Confermato numericamente.

2.1.A) Per x=0: y = sin(1) ~ 0.841. y'(0) = cos(1) * 2*1 * 2 = 4*cos(1) ~ 2.16.
       Verifica numerica coincide.

2.1.B) y'(x) = cos(cos(x^2)) * (-sin(x^2)) * cos(x^2) ... in realta':
       y'(x) = exp(sin(cos(x^2))) * cos(cos(x^2)) * (-sin(x^2)) * 2x.
       In x=0.5: derivata = exp(sin(cos(0.25))) * cos(cos(0.25)) *
       (-sin(0.25)) * 1 ~ ... un numero piccolo (~-1.0).

2.2.A) 5 livelli. (Da L a P, P a Z2, Z2 a H, H a Z1, Z1 a W1.)

4.1.A) Tutti convergono al minimo (entro ~30 step). x finale ~5, -2, 1.

4.1.B) Con lr=1.5: traiettoria diverge (10, -4, 18, -50, ...). Ogni passo
       e' "troppo lungo" - supera il minimo e finisce piu' lontano di
       prima.

4.2.A) File creato in figures/05_01_gd_1d.png.

4.3.A) Per f(x)=(x-3)^2 con tol 1e-6: ~40 iterazioni.

5.1.A) lr=0.01: dopo 20 step x ~5.8 (lontano dal minimo 3). Lento.
       lr=0.9:  dopo 20 step x ~ 3.0 ma traiettoria oscillante.
       lr=1.5:  dopo 20 step x e' un numero enorme (diverge).

5.1.B) File creato. lr=1.5: divergenza ESPONENZIALE (loss raddoppia
       circa ad ogni step).

5.2.A) Per f(x)=(x-4)^2: lr ottimo ~ 0.5 (converge subito).
       lr=0.001 lentissimo. lr=1.5 diverge.

6.1.A) x converge piu' lentamente di y (derivata 2x vs 8y). Anisotropia.

6.1.B) File creato. Traiettoria a "zig-zag" che si attenua.


QUIZ DI VERIFICA

V1) Chain rule = "moltiplica le derivate locali" / "se y = f(g(x)),
    allora dy/dx = f'(g(x)) * g'(x)".

V2) h'(x) = cos(x^2) * 2x.

V3) Gradient descent = "fai un passetto contro il gradiente, ripeti
    finche' arrivi a un minimo". Aggiornamento: x_nuovo = x_vecchio -
    lr * gradiente_in_x_vecchio.

V4) lr troppo grande: la loss OSCILLA o diverge (esplode).
    lr troppo piccolo: la loss scende lentissimamente (mai converge in
    tempo utile).

V5) Bug: "w = w + 0.1 * grad" -> dovrebbe essere "w = w - 0.1 * grad".
    Il GD MINIMIZZA la loss -> va contro il gradiente. Con il "+" sali
    invece di scendere -> la loss esplode.

V6) Step 3: derivata in x=3.2 e' 2*3.2 = 6.4. x = 3.2 - 0.1*6.4 = 2.56.

V7) 1) dL/dP (derivata BCE rispetto a P)
    2) dP/dZ2 (derivata sigmoid)
    3) dZ2/dH (=W2^T)
    4) dH/dZ1 (derivata ReLU)
    5) dZ1/dW1 (=X^T)
    Le 5 moltiplichi (con shape giusti).

V8) Esempio: "Sei in cima a una collina al buio. Vuoi scendere fino in
    fondo. Tocchi il terreno con il piede in cerchio: senti dove e'
    piu' giu'. Fai un passetto in quella direzione. Senti di nuovo.
    Continui cosi'. Se i passetti sono troppo lunghi rischi di
    inciampare; se troppo corti ci metti una vita."


CHECKPOINT

C1) Chain rule = "moltiplica le derivate locali" lungo la catena di
    funzioni. Per L(p, y) = BCE(sigmoid(z), y) rispetto a z:
    dL/dz = dL/dp * dp/dz = ((p-y)/(p(1-p))) * (p(1-p)) = (p - y).

C2) GD: parti da x0, calcoli gradiente, sposti x contro il gradiente,
    ripeti. Rischio: convergenza solo a un MINIMO LOCALE (e in alte
    dimensioni anche divergenza con lr sbagliato).

C3) x_nuovo = 5 - 0.3 * 4 = 5 - 1.2 = 3.8.

C4) 49 derivate parziali (una per ogni parametro). Per W1 (32 pesi),
    assumendo di gia' avere dL/dZ2: ~3 moltiplicazioni "logiche"
    (W2^T, deriv ReLU, X^T) ma vettorizzate -> 3 operazioni matriciali.
"""


# ==========================================================================
# NOTE PER IL CAPITOLO SUCCESSIVO (cap.06 backprop + training)
# ==========================================================================
#
# Cosa porti via:
#   - chain rule a 2, 3, n livelli (numericamente + a mano)
#   - GD su 1 e n variabili
#   - addestramento del mini-neurone con grad numerico (lento!)
#   - intuizione "lr troppo grande -> oscilla; troppo piccolo -> lento"
#
# Cosa farai nel cap.06:
#   - sostituire gradiente_numerico con BACKWARD ANALITICO (5x piu' veloce)
#   - calcolare backward step-by-step su rete 2-layer
#   - sanity check numerico vs analitico
#   - training loop completo
#   - addestrare la rete sul CSV M2 + battere LogReg
#
# Prima di aprire il cap.06, fai il bridge ripasso:
#   modulo_03_dl_cv/quiz_ripasso_tra_capitoli/
#       M03_R05_after_C05_before_C06_chain_to_backprop.md


# ==========================================================================
# ENTRY POINT
# ==========================================================================
if __name__ == "__main__":
    print("=" * 70)
    print("Cap.05 M3 - CHAIN RULE + GRADIENT DESCENT - demo")
    print("=" * 70)

    print("\n[Demo 1.1 - chain rule su h(x) = (3x+1)^2]")
    _esempio_chain_rule()

    print("\n[Demo 4.1 - GD su f(x) = (x-3)^2, x0 = 10]")
    _demo_gd_1d()

    print("\n[Demo 5 - effetto del learning rate]")
    _demo_lr()

    print("\n[Demo 6.1 - GD 2D su f(x,y) = (x-3)^2 + (y+2)^2]")
    _demo_gd_2d()

    print("\n[Demo - genero grafici nelle figures/]")
    figures_dir = os.path.join(os.path.dirname(__file__), "figures")
    _grafico_gd_1d_traiettoria(out_path=os.path.join(figures_dir, "05_01_gd_1d.png"))
    _grafico_lr_a_confronto(out_path=os.path.join(figures_dir, "05_02_lr_confronto.png"))
    _grafico_gd_2d_traiettoria(out_path=os.path.join(figures_dir, "05_03_gd_2d.png"))
    print(f"  -> {figures_dir}/05_01_gd_1d.png")
    print(f"  -> {figures_dir}/05_02_lr_confronto.png")
    print(f"  -> {figures_dir}/05_03_gd_2d.png")

    print("\n" + "=" * 70)
    print("Demo finite. Adesso tocca a te:")
    print("  - 17 mini-esercizi inline (sez 1-6)")
    print("  - 6 TODO base (1-6)")
    print("  - 4 TODO recall cap.01-04 M3 (7-10)")
    print("  - 1 pipeline integrata (addestramento_via_gradiente_numerico)")
    print("  - 6 TODO tipologie (colloquio/refactor/debug/retrieval/INT/RW)")
    print("  - 8 quiz verifica + mini-progetto confronto_lr + checkpoint")
    print("Quando vuoi una valutazione: 'valuta cap.05 M3 sezione X'.")
    print("=" * 70)
