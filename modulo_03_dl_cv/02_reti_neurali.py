"""
============================================================================
MODULO 3 (DL & CV) - CAPITOLO 02
"Reti neurali da zero": layer impilati = sequenza di X @ W + b + attivazione
============================================================================

----------------------------------------------------------------------------
DA DOVE ARRIVI (cap.01 M3)
----------------------------------------------------------------------------
Nel cap.01 M3 hai imparato che un NEURONE artificiale e' fatto da 2 passi:

    z = X @ w + b           # logit (punteggio)        shape (N,)
    a = sigmoid(z)          # probabilita' [0, 1]      shape (N,)

E hai dimostrato (con l'esercizio E7 - RECALL CROSS-MODULO) che il neurone
e' un caso particolare del layer Dense del Ponte cap.02:

    layer_dense(X, W, b, att) = att(X @ W + b)
    con W (d, h) e h=1, att=sigmoid -> ritorna esattamente neurone_batch.

In questo capitolo si fa il PASSO successivo: invece di UN layer, ne
impiliamo DUE (o piu'). Il risultato si chiama RETE NEURALE.

L'oggetto matematico e' identico: una pila di "X @ W + b + attivazione".
Cambia solo il NUMERO di volte che lo applichi:

    H = ReLU(X @ W1 + b1)        # layer 1 (NASCOSTO)   shape (N, h)
    P = sigmoid(H @ W2 + b2)     # layer 2 (OUTPUT)     shape (N, 1)

Per chi viene dal web dev: una rete neurale e' come una PIPELINE Laravel
in cui ogni middleware (layer) trasforma il "request" (X) e lo passa al
successivo. L'ultimo middleware emette la "response" (la probabilita').

----------------------------------------------------------------------------
COSA PORTI VIA DA QUESTO CAPITOLO (Definition of Done)
----------------------------------------------------------------------------
Alla fine sai rispondere "in 1 riga" a queste 5 domande:

  1) Cos'e' un LAYER DENSE (Fully Connected) e che shape hanno W e b?  -> Sez. 1
  2) Perche' una rete senza attivazione interna NON e' una vera rete? -> Sez. 2
  3) Come si scrive il forward di una rete 2-layer in NumPy in 2 righe? -> Sez. 2
  4) Cosa succede ai pesi se li inizializzi TUTTI a zero (e perche')?  -> Sez. 2
  5) Cos'e' l'"Universal Approximation Theorem" (in linguaggio umano)? -> Sez. 3

Hai anche scritto 3 funzioni riutilizzabili:
  - layer_dense (riprende E7 cap.01 M3)
  - rete_2_layer (input -> hidden ReLU -> output sigmoid)
  - init_pesi_he   (inizializzazione "He" raccomandata per ReLU)

E hai dimostrato (mini-progetto) che una rete 2-layer NON addestrata fa
peggio della LogisticRegression M2 (e' giusto cosi': nel cap.03 M3
imparera' a fare meglio).

----------------------------------------------------------------------------
MAPPA DEL CAPITOLO
----------------------------------------------------------------------------
   *  PRONTUARIO TRANELLI RETE            [R1] - [R6]
   *  QUIZ D'INGRESSO                     Q1 - Q5     (cerniera cap.01 M3)
   *  SEZIONE 1  Dal neurone al layer (W matrice)  1.1 - 1.3
   *  SEZIONE 2  Rete a 2 layer in NumPy puro      2.1 - 2.3
   *  SEZIONE 3  Forward batch su CSV M2 + UAT      3.1 - 3.2
   *  QUIZ DI VERIFICA                    V1 - V7
   *  ESERCIZI FINALI                     E1 - E6
                                          (colloquio / refactoring / debug /
                                           retrieval / interleaving / real-world)
   *  MINI-PROGETTO                       rete_2_layer_vs_logreg
   *  CHECKPOINT FINALE                   C1 - C4
   *  SOLUZIONI QUIZ                      in fondo

----------------------------------------------------------------------------
COME USARE QUESTO FILE (regola del corso)
----------------------------------------------------------------------------
   1. Leggi in ORDINE. La sezione N usa la sezione N-1.
   2. Per ogni TODO scrivi nel blocco "TUO CODICE" (non cancellare lo
      scaffold, lascialo come traccia).
   3. Quando vuoi una valutazione: "valuta cap.02 M3 sezione X.Y"
   4. Se ti blocchi >10 min: "sono bloccato sezione X" -> ti do solo
      l'IDEA, mai la soluzione.
   5. Niente LaTeX (preferenza tua): formule in PAROLE + codice.
   6. Hardware: tutto su CPU + NumPy + Matplotlib. PyTorch arriva al cap.04.
"""

import os
from typing import Callable
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy.typing import NDArray


# ==========================================================================
# PRONTUARIO TRANELLI RETE - leggilo PRIMA di iniziare (5 minuti)
# ==========================================================================
# Sono i tranelli specifici delle RETI multi-layer. Quelli sui vettori
# (T1-T10) e sulle matrici (M1-M8) li trovi nel Ponte cap.01-02. I tranelli
# del NEURONE (N1-N6) li trovi nel cap.01 M3.
#
# [R1] UNA RETE = N LAYER, NON 1.
#      Layer 1: H = ReLU(X @ W1 + b1)        shape (N, h)
#      Layer 2: P = sigmoid(H @ W2 + b2)     shape (N, 1) o (N,)
#      Il NUMERO di layer e l'attivazione fra di mezzo definiscono la rete.
#
# [R2] SENZA ATTIVAZIONE INTERNA, NON E' UNA RETE.
#      Se metti H = X @ W1 + b1 e P = H @ W2 + b2 (senza ReLU in mezzo),
#      la rete e' EQUIVALENTE a un solo layer X @ (W1 @ W2) + b'.
#      In altre parole: 2 trasformazioni lineari = 1 trasformazione lineare.
#      L'attivazione "non lineare" e' cio' che permette di approssimare
#      funzioni complesse.
#
# [R3] SHAPE DEI PESI - vai SEMPRE a vedere W.shape se hai dubbi.
#      X (N, d) -> W1 (d, h)     -> H (N, h)
#      H (N, h) -> W2 (h, k)     -> P (N, k)
#      Regola: "le colonne di W di un layer == le righe di W del layer
#      successivo" (in altre parole: l'output di un layer e' l'input del
#      successivo).
#
# [R4] BIAS: 1 PER NEURONE DEL LAYER, NON 1 PER PRATICA.
#      b1.shape == (h,)   <- 1 bias per ognuno degli h neuroni del layer 1
#      b2.shape == (k,)   <- 1 bias per ognuno dei k neuroni di output
#      Quando fai X @ W1 + b1, b1 viene "broadcast" su tutte le N pratiche.
#
# [R5] INIZIALIZZAZIONE: random PICCOLI, mai zero, mai uguali.
#      W1 = rng.standard_normal((d, h)) * 0.01        <- ok
#      W1 = rng.standard_normal((d, h)) * np.sqrt(2/d) <- He init (per ReLU)
#      W1 = np.zeros((d, h))                          <- BUG (symmetry)
#      Tutti i neuroni con pesi identici imparano la stessa cosa: la rete
#      "collassa" a un solo neurone.
#
# [R6] L'OUTPUT FINALE E' UNA PROBABILITA' SOLO SE METTI SIGMOID/SOFTMAX
#      ALL'ULTIMO LAYER.
#      - classificazione binaria -> ultimo layer ha sigmoid e shape (N, 1)
#      - classificazione multi-classe -> ultimo layer ha softmax e shape (N, k)
#      Nei layer NASCOSTI usa ReLU (M3 cap.01 N4): non sigmoid, ne' tanh
#      (saturano e ammazzano il gradiente in M3 cap.03).


# ==========================================================================
# QUIZ D'INGRESSO - cerniera cap.01 M3 -> cap.02 M3
# ==========================================================================
# Rispondi nei commenti sotto ogni domanda. Soluzioni a fine file.

# Q1) Hai X (200, 7) e una rete con W1 (7, 16). Che shape ha
#     H = X @ W1 + b1?  E b1 che shape DEVE avere?
# TUA RISPOSTA:
# H ha shape = (200, 16), b1 ha shape = (16,)

# Q2) Spiega in 1 riga PERCHE' fra due layer Dense si mette una funzione
#     di attivazione NON LINEARE (es. ReLU). Cosa succederebbe senza?
# TUA RISPOSTA:
# Si mette una funzione di attivazione per non avere una semplice sequenza di layer che fanno 
# operazione lineari, dove di fatto si avrebbe alla fine solo un unico grande layer. Le attivazioni
# non lineari come ReLU permettono di seguire la complessita di funzioni non lineari.

# Q3) sigmoid e ReLU - quale va all'ULTIMO layer di un classificatore
#     binario? Quale nei layer NASCOSTI? E perche'?
# TUA RISPOSTA:
# nei layer nascosti va il ReLU, metre nel layer di output va la sigmoid. Questo perchè ReLU restituisce i valori cosi come sono, eccetto per i valori inferiori di 0 per i quali restituisce proprio 0. In questo modo, possiamo seguire un andamento non lineare nel passaggio tra i vai layer. Alla fine del percorso invece sigmoid (o softmax) ci da delle probabilità che sono utili per determinare che tipo di output è più corretto ai nostri scopi

# Q4) [Trova l'errore]
#       W1 = np.zeros((7, 16))
#       b1 = np.zeros(16)
#       H = X @ W1 + b1
#       P = sigmoid(H @ W2 + b2)
#     Che valore avranno tutte le probabilita' P, indipendentemente da
#     X? Perche'?
# TUA RISPOSTA:
# Il valore è 0.5. questo perchè se i pesi di w e il bias sono tutti 0, inevitabilmente il dot product + b produrra sempre valori = 0. le sigmoidi di 0 saranno 0.5, ossia massima incertezza (questo perchè se sigmoid schiaccia tutti i valori da -inf a +inf tra 0 e 1, a meta strada, ossia a 0.5, c'è proprio lo 0)

# Q5) [Feynman - no jargon tecnico] Spiega in 3 righe cos'e' una rete
#     neurale a un collega web dev che non sa nulla di AI. VIETATO usare
#     "tensore", "gradiente", "neurone", "layer", "sigmoid", "ReLU".
# TUA RISPOSTA:
# immagine una fabbrica di oggetti. Ogni livello della rete neurale è come uno pezzo di una catena di montaggio di una fabbrica. Ad ogni step della catena, il prodotto che si sta fabricando viene trasformato, e alla fine ne esce il prodotto finito


# ==========================================================================
# SEZIONE 1 - DAL NEURONE AL LAYER: la matrice W
# ==========================================================================

# ---------------------- ANALOGIA --------------------------------------------
# Pensa a una commissione bancaria che valuta una pratica di mutuo. Nel
# cap.01 M3 c'era UN solo commissario (UN neurone) che dava un giudizio.
#
# Adesso immagina che il direttore voglia un PARERE COLLEGIALE: invece di
# UN commissario, ne mette H = 16 in parallelo. Ognuno guarda la stessa
# pratica con i propri "occhi" (vettore di pesi) e da' il proprio
# punteggio.
#
# Risultato: per ogni pratica hai 16 punteggi diversi (un "ritratto
# multi-prospettiva" della pratica). Questi 16 punteggi diventeranno
# l'input del COMMISSARIO FINALE (l'output layer) che dovra' decidere.
#
# In codice:
#     H = ReLU(X @ W1 + b1)    <- pareri dei 16 commissari
#     P = sigmoid(H @ W2 + b2) <- giudizio finale del direttore
#
# Per il web dev: e' come avere 16 "validator" sullo stesso request, e
# poi un "aggregator" che decide il responso finale in base ai 16
# validator. Ogni validator vede la stessa cosa ma "pesa" diversamente.

# ---------------------- TEORIA + CODICE -------------------------------------
# 1.1 - IL LAYER DENSE (Fully Connected): definizione
#
# Un layer Dense con h neuroni prende un input X (N, d) e produce un
# output H (N, h). Sotto il cofano e' UN dot product di matrici:
#
#       H = att(X @ W + b)
#       W.shape == (d, h)     <- "una colonna per neurone"
#       b.shape == (h,)       <- "un bias per neurone"
#
# E' lo STESSO oggetto che hai gia' scritto in E7 cap.01 M3 (con
# h=1). Qui generalizziamo a qualsiasi h.


def layer_dense(
    X: NDArray[np.float64],
    W: NDArray[np.float64],
    b: NDArray[np.float64] | float,
    att: Callable[[NDArray[np.float64]], NDArray[np.float64]] | None = None,
) -> NDArray[np.float64]:
    """Forward di un layer Dense.

    Args:
        X:   batch di pratiche, shape (N, d)
        W:   matrice pesi,      shape (d, h)
        b:   bias,              shape (h,) o scalare (broadcast su h)
        att: funzione di attivazione element-wise (es. sigmoid, relu, tanh)
             se None, layer "lineare" (nessuna attivazione).

    Returns:
        H, shape (N, h)
    """
    if X.ndim != 2 or W.ndim != 2:
        raise ValueError(
            f"X deve essere 2D e W 2D, invece X{X.shape} W{W.shape}"
        )
    if X.shape[1] != W.shape[0]:
        raise ValueError(
            f"shape incompatibili: X{X.shape} colonne vs W{W.shape} righe"
        )
    z = X @ W + b              # logit, shape (N, h)
    if att is None:
        return np.asarray(z, dtype=float)
    return np.asarray(att(z), dtype=float)


# 1.2 - LE 3 ATTIVAZIONI (recap cap.01 M3, le servono qui)

def sigmoid(z: NDArray[np.float64] | float) -> NDArray[np.float64] | float:
    """Sigmoid stabile numericamente (clip ±500 per evitare overflow)."""
    z_arr = np.asarray(z, dtype=float)
    z_safe = np.clip(z_arr, -500.0, 500.0)
    out = 1.0 / (1.0 + np.exp(-z_safe))
    if np.isscalar(z) or out.ndim == 0:
        return float(out)
    return out


def relu(z: NDArray[np.float64]) -> NDArray[np.float64]:
    """ReLU element-wise: max(0, z)."""
    return np.maximum(0.0, z)


def tanh(z: NDArray[np.float64]) -> NDArray[np.float64]:
    """Tanh element-wise."""
    return np.tanh(z)


# 1.3 - INIZIALIZZAZIONE DEI PESI: "He" per ReLU
#
# Nel cap.01 M3 hai visto che inizializzare a zero NON funziona (R5).
# La domanda e': quanto "grandi" devono essere i pesi random?
#
# Regola moderna (2026): si usa un'inizializzazione che dipende dal
# numero di input del layer (fan_in = d).
#
#   - per LAYER con ReLU      -> He init:     W ~ N(0, sqrt(2/d))
#   - per LAYER con tanh      -> Xavier init: W ~ N(0, sqrt(1/d))
#
# Spiegazione intuitiva: vogliamo che il logit z = X @ W + b abbia una
# "scala stabile" (ne' troppo piccolo, ne' troppo grande) all'inizio.
# Se W e' troppo grande, sigmoid satura (R6) e l'apprendimento muore.
# Se W e' troppo piccolo, z ~ 0 e tutto e' "indistinto".


def init_pesi_he(
    d: int,
    h: int,
    seed: int | None = 42,
) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """Init He: W ~ Normal(0, sqrt(2/d)), b = 0.

    Args:
        d: numero di input del layer (fan_in)
        h: numero di neuroni del layer
        seed: per riproducibilita'. None = casuale ogni volta.

    Returns:
        (W, b) con W.shape == (d, h), b.shape == (h,)
    """
    rng = np.random.default_rng(seed)
    scala = np.sqrt(2.0 / d)
    W = rng.standard_normal((d, h)) * scala
    b = np.zeros(h, dtype=float)
    return W, b


def _esempio_layer_dense() -> None:
    """Forward di UN layer Dense su 4 pratiche, 5 feature, 3 neuroni."""
    rng = np.random.default_rng(0)
    X = rng.standard_normal((4, 5))
    W, b = init_pesi_he(d=5, h=3, seed=0)
    H = layer_dense(X, W, b, att=relu)
    print(f"X.shape = {X.shape}, W.shape = {W.shape}, b.shape = {b.shape}")
    print(f"H.shape = {H.shape}  (4 pratiche x 3 neuroni)")
    print("H[0] =", np.round(H[0], 3))


# TODO 1.1 (5 minuti):
# Obiettivo: vedere ReLU "tagliare" i logit negativi → molti zeri in H.
#
# Traccia (usa funzioni GIÀ definite sopra: layer_dense, relu, init_pesi_he):
#   1) rng = np.random.default_rng(1)
#   2) X con shape (5, 3) — es. numeri gaussiani o uniformi, come preferisci.
#   3) Layer con d=3 input e h=4 neuroni → W deve essere (3, 4), b (4,).
#      Puoi costruire W,b con init_pesi_he(d=3, h=4, seed=...) oppure a mano,
#      ma resta coerente con le shape del dot X @ W.
#   4) H = layer_dense(X, W, b, att=relu)  → ti aspetti H.shape == (5, 4).
#   5) Stampa X.shape, W.shape, b.shape e H.shape.
#   6) Conta le celle esattamente 0: (H == 0) è una maschera booleana;
#      .sum() su quella maschera conta i True (equivalente a np.count_nonzero(H == 0)).
#   7) Sotto, UNA riga di commento: perche' ReLU azzera quelle celle?
# TUO CODICE QUI:
print("\nTODO 1.1\n")
rng = np.random.default_rng(1)
X = rng.uniform(-5, 5, size=(5, 3))
W, b = init_pesi_he(X.shape[1], 4)
# z = X @ W + b
# H = relu(z)
H = layer_dense(X, W, b, att=relu)
print(X.shape) # controllo visuale della shape coerente con la richiesta della traccia
print(W.shape)
print(b.shape)
print(H.shape)
celle_0 = (H == 0).sum()
print(H)
print(celle_0)
# relu azzera quelle celle perchè la sua funzione è quella di riportare 0 al posto dei logit z negativi.

# TODO 1.2 (5 minuti):
# Obiettivo: stessi pesi e bias, ma cambia SOLO l'attivazione → cambia la "scala"
# dei numeri in uscita (lineare illimitato vs probabilita'-like in (0, 1)).
#
# Traccia:
#   1) rng = np.random.default_rng(...) e crea X (10, 2), W (2, 3), b (3,) tutti random.
#   2) Due forward sullo STESSO triplo (X, W, b):
#        H_lineare = layer_dense(X, W, b, att=None)
#        H_sigmoid = layer_dense(X, W, b, att=sigmoid)
#      (Se vuoi restare sintetico: una riga per assegnazione va bene.)
#   3) print min/max di H_lineare e di H_sigmoid — confronta ordini di grandezza e limiti.
#   4) Rispondi in 2-3 parole tue (anche solo commento): cosa cambia nella scala?
#      Suggerimento: ricorda R6 nel prontuario (saturazione sigmoid) vs output lineare.
# TUO CODICE QUI:
print("\nTODO 1.2\n")
# rng = np.random.default_rng(1)
# X = rng.uniform(-5, + 5, (10, 2))
# d = X.shape[1]
# h = 3
# W = rng.standard_normal((d, h)) * np.sqrt(2 / d)
# b = rng.standard_normal(h)

# def layer_dense(
#     X: NDArray[np.float64],
#     W: NDArray[np.float64],
#     b: NDArray[np.float64] | float,
#     att: Callable[[NDArray[np.float64] | float], NDArray[np.float64] | float] | None = None,
# ) -> NDArray[np.float64]:
    
#     if X.ndim != 2 or W.ndim != 2:
#         raise ValueError(
#             f"X deve essere 2D e W 2D, invece X{X.shape} W{W.shape}"
#         )
#     if X.shape[1] != W.shape[0]:
#         raise ValueError(
#             f"shape incompatibili: X{X.shape} colonne vs W{W.shape} righe"
#         )
#     z = X @ W + b
#     if att is None:
#         return np.asarray(z, dtype=float)
#     return np.asarray(att(z), dtype=float)

# def relu(
#     z: NDArray[np.float64] | float
# ) -> NDArray[np.float64] | float:
#     z_arr = np.asarray(z, dtype=float)
#     out = np.maximum(0, z_arr)
#     if np.isscalar(out) or out.ndim == 0:
#         return float(out)
#     return out

# def sigmoid(
#     z: NDArray[np.float64] | float
# ) -> NDArray[np.float64] | float:
#     z_arr = np.asarray(z, dtype=float)
#     z_clip = np.clip(z_arr, -500, +500)
#     out = 1 / (1 + np.exp(-z_clip))
#     if np.isscalar(out) or out.ndim == 0:
#         return float(out)
#     return out

# H_lineare = layer_dense(X, W, b)
# H_sigmoid = layer_dense(X, W, b, att=sigmoid)
# print(f"{H_lineare}\n")
# np.set_printoptions(precision=4, suppress=True)
# print(f"{H_sigmoid}\n")
# print(H_lineare.min(), H_lineare.max())
# print(H_sigmoid.min(), H_sigmoid.max())

# la scala, se lasciamo i logit così come sono, può essere piccola come enorme, dipende dal risultato delle operazione.
# se schiacciamo i valori tramite sigmoid, avremo valori gestibili tra 0 e 1.


# TODO 1.3 (3 minuti):
# Obiettivo: He init produce W con campioni ~ N(0, scala^2) dove scala = sqrt(2/d).
#
# Traccia:
#   1) W, b = init_pesi_he(d=10, h=20, seed=42)   # o altro seed, ma tienilo fisso
#      Verifica con uno sguardino: W.shape == (10, 20), b.shape == (20,) e b e' tutto zero.
#   2) Stampa float(W.mean()) e float(W.std()) — oppure np.mean/np.std su W.ravel().
#   3) Confronto teorico: dev_std atteso circa sqrt(2/d) con d=10 → ~0.447;
#      la media teorica del processo e' 0.
#   4) Una frase (commento): perche' la media campionaria non e' ESATTAMENTE 0?
# perchè i valori sono estratti da una gaussiana a media 0 e dev std 1.Si avrà dunque che la media sarà circa 0, mentra dato che tutti valori sono poi moltiplicati per la scala (np.sqrt(2/d)) la dev std (sigma) che di base e' 1 verrà moltiplicato * sqrt(2 / 10), diventando circa 0.447.
#      (Indizio: stai osservando un numero FINITO di campioni da una Gaussiana.)
# TUO CODICE QUI:
print("\nTODO 1.2\n")

W, b = init_pesi_he(10, 20, seed=42)
assert W.shape == (10, 20), "Errore con la shape di W"
print(W.shape)
assert b.shape == (20, ), "Errore con la shape di b"
print(b.shape)
W_1d = W.ravel()
print(np.mean(W_1d))
print(np.std(W_1d))

# ==========================================================================
# SEZIONE 2 - UNA RETE A 2 LAYER IN NUMPY PURO
# ==========================================================================

# ---------------------- ANALOGIA --------------------------------------------
# Una rete a 2 layer e' come una CATENA DI MONTAGGIO con 2 stazioni:
#
#   stazione 1 (hidden):  prende le 7 feature della pratica e le trasforma
#                         in 16 "feature derivate". Ad esempio una di
#                         queste 16 potrebbe essere "stipendio - rate
#                         arretrate" (combinazione delle feature originali
#                         che il modello scopre da solo).
#
#   stazione 2 (output):  prende le 16 feature derivate e decide: questa
#                         pratica e' alterata? (probabilita' fra 0 e 1)
#
# La magia: lo studente NON dice alla rete "calcolami stipendio - rate
# arretrate". La rete IMPARA da sola che combinazione delle feature
# originali e' utile. Questo si chiama RAPPRESENTAZIONE LEARNATA.
#
# Per il web dev: e' come avere un sistema in cui il primo middleware
# riformatta i dati di input in modo "intelligente" prima di passarli al
# secondo. Solo che NON e' il developer a programmare quel riformat: e'
# l'allenamento (M3 cap.03) a sceglierlo.

# ---------------------- TEORIA + CODICE -------------------------------------
# 2.1 - LA RETE 2-LAYER: forward
#
# Architettura standard per classificazione binaria:
#
#   layer 1 (hidden):  H = ReLU(X @ W1 + b1)        shape (N, h)
#   layer 2 (output):  Z = H @ W2 + b2              shape (N, 1)
#                      P = sigmoid(Z).ravel()       shape (N,)
#
# Dimensioni "consigliate" per il nostro CSV M2 (d=7, classificazione
# binaria):
#       d = 7    (feature di input)
#       h = 16   (neuroni nello strato nascosto - puoi sperimentare)
#       k = 1    (output binario: 1 probabilita' per pratica)


def rete_2_layer(
    X: NDArray[np.float64],
    W1: NDArray[np.float64],
    b1: NDArray[np.float64],
    W2: NDArray[np.float64],
    b2: NDArray[np.float64] | float,
) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """Forward di una rete 2-layer (input -> hidden ReLU -> output sigmoid).

    Args:
        X:  batch, shape (N, d)
        W1: pesi hidden,  shape (d, h)
        b1: bias hidden,  shape (h,)
        W2: pesi output,  shape (h, 1)
        b2: bias output,  shape (1,) o scalare

    Returns:
        (H, P) dove:
          - H: attivazioni hidden, shape (N, h)
          - P: probabilita' output, shape (N,) - "ravel" applicato gia'
    """
    if X.ndim != 2:
        raise ValueError(f"X deve essere 2D, e' {X.shape}")
    H = layer_dense(X, W1, b1, att=relu)       # (N, h)
    Z = layer_dense(H, W2, b2, att=None)       # (N, 1)
    P = sigmoid(Z).ravel()                      # (N,)
    return H, np.asarray(P, dtype=float)


def _esempio_rete_2_layer_random() -> None:
    """Forward di una rete con pesi random su un mini-batch fittizio."""
    rng = np.random.default_rng(0)
    N, d, h = 8, 7, 16
    X = rng.standard_normal((N, d))
    W1, b1 = init_pesi_he(d, h, seed=1)
    W2, b2 = init_pesi_he(h, 1, seed=2)
    H, P = rete_2_layer(X, W1, b1, W2, b2)
    print(f"X.shape = {X.shape}")
    print(f"H.shape = {H.shape}, P.shape = {P.shape}")
    print(f"P (prime 4): {np.round(P[:4], 3)}")
    print(f"P.mean() = {P.mean():.3f}  "
          f"(pesi random -> circa 0.5: rete NON addestrata)")


# 2.2 - PERCHE' SERVE L'ATTIVAZIONE FRA I LAYER (R2 - dimostrazione)
#
# Senza attivazione interna, una rete 2-layer collassa a 1 solo layer.
# Si vede algebricamente:
#
#       H = X @ W1 + b1
#       Z = H @ W2 + b2 = (X @ W1 + b1) @ W2 + b2
#                       = X @ (W1 @ W2) + (b1 @ W2 + b2)
#                       = X @ W_combinato + b_combinato
#
# 2 layer lineari == 1 layer lineare. NON aggiungi capacita' espressiva.
# L'attivazione (ReLU) "rompe" questa equivalenza: max(0, x) NON e'
# lineare, quindi 2 layer con ReLU in mezzo NON si possono fondere in 1.


def _demo_collasso_lineare() -> None:
    """Mostra che 2 layer lineari sono equivalenti a 1 layer lineare."""
    rng = np.random.default_rng(0)
    X = rng.standard_normal((50, 4))
    W1, b1 = init_pesi_he(4, 8, seed=1)
    W2, b2 = init_pesi_he(8, 1, seed=2)

    # Rete 2-layer LINEARE (NIENTE ReLU)
    H = layer_dense(X, W1, b1, att=None)
    Z_due_layer = layer_dense(H, W2, b2, att=None).ravel()

    # Rete EQUIVALENTE a 1 layer
    W_eq = W1 @ W2                  # (4, 1)
    b_eq = b1 @ W2 + b2             # (1,)
    Z_un_layer = (X @ W_eq + b_eq).ravel()

    diff = float(np.max(np.abs(Z_due_layer - Z_un_layer)))
    print(f"diff_max (2 layer lineari vs 1 layer): {diff:.2e}")
    assert diff < 1e-10, "qualcosa non torna nella dimostrazione"
    print("OK: due layer SENZA attivazione = 1 solo layer (R2).")


# 2.3 - BUG SCUOLA: inizializzazione ZERO (R5 - dimostrazione)


def _demo_init_zero() -> None:
    """Mostra che con pesi tutti zero la rete e' "rotta": P = 0.5 sempre."""
    rng = np.random.default_rng(0)
    X = rng.standard_normal((20, 4))
    W1 = np.zeros((4, 8))
    b1 = np.zeros(8)
    W2 = np.zeros((8, 1))
    b2 = np.zeros(1)
    _, P = rete_2_layer(X, W1, b1, W2, b2)
    print(f"P.mean() = {P.mean():.4f}, P.min() = {P.min():.4f}, "
          f"P.max() = {P.max():.4f}")
    print("Tutti 0.5 perche' z = 0 ovunque e sigmoid(0) = 0.5.")
    print("Anche peggio: durante il training (M3 cap.03) tutti i neuroni")
    print("dello strato hidden imparerebbero la STESSA cosa "
          "('symmetry breaking' rotto).")


# TODO 2.1 (8 minuti):
# Replica _esempio_rete_2_layer_random() ma:
#   - N = 12, d = 5, h = 8
#   - usa default_rng(7) per X
#   - usa init_pesi_he con seed diversi (10, 11) per (W1, b1) e (W2, b2)
#   - stampa H.shape, P.shape, P.min(), P.max(), P.mean()
# Domanda finale (commento): la P.mean() e' vicina a 0.5? Perche'?
# TUO CODICE QUI:
print("\nTODO 2.1\n")

def my_esempio_rete_2_layer_random():
    rng = np.random.default_rng(7)
    N, d, h = 12, 5, 8
    X = rng.uniform(-5, +5, size=(N, d))
    W1, b1 = init_pesi_he(d, h, seed=10)
    W2, b2 = init_pesi_he(h, 1, seed=11)
    return rete_2_layer(X, W1, b1, W2, b2)

H, P = my_esempio_rete_2_layer_random()
print(H.shape)
print(P.shape)
print(P.min())
print(P.max())
print(P.mean())

# Perchè usando valori random, la rete non è allenata, e i logit sono circa 0. Sigmoide di valori circa 0 da circa 0.5.

# TODO 2.2 (10 minuti):
# Verifica empirica del crollo lineare di R2 ma su una rete A 3 LAYER
# senza attivazioni in mezzo. Mostra che e' equivalente a UN solo layer.
# Usa shape X (30, 4), W1 (4, 8), W2 (8, 6), W3 (6, 1). Stampa il
# diff_max fra le due implementazioni e fai un assert < 1e-10.
# TUO CODICE QUI:

print("\nTODO 2.2\n")
rng = np.random.default_rng(42)
N, d, h, k = 30, 4, 8, 6
X = rng.standard_normal((N, d))
W1 = rng.standard_normal((d, h)) * np.sqrt(2 / d)
b1 = np.zeros(h)
W2 = rng.standard_normal((h, k)) * np.sqrt(2 / h)
b2 = np.zeros(k)
W3 = rng.standard_normal((k, 1)) * np.sqrt(2 / k)
b3 = 0.0

Z = layer_dense(X, W1, b1, att=None)
H = layer_dense(Z, W2, b2, att=None)
K = layer_dense(H, W3, b3)

W_eq = W1 @ W2 @ W3
b_eq = ((b1 @ W2 + b2) @ W3 + b3)

K_eq = layer_dense(
    X,
    W_eq,
    b_eq
    )
diff_max = np.max(np.abs(K - K_eq))
assert np.allclose(K, K_eq, atol=1e-10), "Qualcosa è andato storto!, gli Array K e K_eq non combaciano"
print(f"Max differenza: {diff_max}")


# TODO 2.3 (5 minuti):
# Replica _demo_init_zero ma usa init_pesi_he per i pesi (zero solo per
# i bias). Cosa cambia in P.mean() / P.min() / P.max() ? Spiega in 1
# riga perche' (suggerimento: ora i neuroni "vedono cose diverse").
# TUO CODICE QUI:

# ora non avendo restituiti dei dot product = 0, in neuroni effettuano delle operazione che producono risultati diversi in base alle feature di partenza e i pesi dei vari layer
print("\nTODO 2.3\n")
    
def my_demo_init_zero() -> None:
    rng = np.random.default_rng(42)
    N, d, h = 20, 4, 8, 
    X = rng.standard_normal((N, d))
    W1, b1 = init_pesi_he(d, h)
    W2, b2 = init_pesi_he(h, 1)
    _, P = rete_2_layer(X, W1, b1, W2, b2)
    print(f"P.mean() = {P.mean():.4f}, P.min() = {P.min():.4f}, P.max() = {P.max():.4f}")
my_demo_init_zero()


# ==========================================================================
# SEZIONE 3 - FORWARD SU CSV REALE + UNIVERSAL APPROXIMATION
# ==========================================================================
#
# Adesso usiamo i veri dati del Modulo 2 (pratiche_genuinita_mock.csv) e
# mostriamo:
#   (a) il forward di una rete 2-layer (NON addestrata) su tutto il batch
#   (b) che la rete NON addestrata fa malissimo (accuracy ~ 0.5)
#   (c) che la LogisticRegression M2 (allenata) la batte facilmente
#
# E' giusto cosi'. Nel cap.03 M3 (backpropagation) imparerai ad ALLENARE
# la rete, e li' iniziera' a battere la LogisticRegression.

# ---------------------- TEORIA + CODICE -------------------------------------
# 3.1 - CARICAMENTO DATI (riusa il pattern del cap.01 M3)

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


# 3.2 - FORWARD DELLA RETE 2-LAYER SU TUTTE LE PRATICHE


def _esempio_rete_2_layer_su_csv() -> None:
    """Forward di una rete random + confronto con LogisticRegression M2."""
    from sklearn.linear_model import LogisticRegression
    from sklearn.preprocessing import StandardScaler
    from sklearn.metrics import accuracy_score

    X, y = carica_pratiche()
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    d = X_scaled.shape[1]
    h = 16

    # Rete 2-layer NON addestrata (pesi random)
    W1, b1 = init_pesi_he(d, h, seed=42)
    W2, b2 = init_pesi_he(h, 1, seed=43)
    _, P_rete = rete_2_layer(X_scaled, W1, b1, W2, b2)
    pred_rete = (P_rete >= 0.5).astype(int)
    acc_rete = accuracy_score(y, pred_rete)

    # LogisticRegression M2 (allenata)
    clf = LogisticRegression(max_iter=1000, random_state=42)
    clf.fit(X_scaled, y)
    pred_lr = clf.predict(X_scaled)
    acc_lr = accuracy_score(y, pred_lr)

    print(f"X_scaled.shape = {X_scaled.shape}")
    print(f"Rete 2-layer (RANDOM, non addestrata):   accuracy = {acc_rete:.3f}")
    print(f"LogisticRegression M2 (ALLENATA):        accuracy = {acc_lr:.3f}")
    print("La rete random fa peggio: e' giusto cosi'.")
    print("Nel cap.03 M3 la addestriamo con la backpropagation.")
print ("\nsezione 3\n")
_esempio_rete_2_layer_su_csv()

# 3.3 - INTUIZIONE: UNIVERSAL APPROXIMATION THEOREM (no formule)
#
# UAT (Universal Approximation Theorem - 1989): una rete neurale a 2
# layer con un numero "sufficiente" di neuroni nascosti puo' approssimare
# QUALSIASI funzione continua a piacere, con la precisione che vuoi.
#
# In parole umane: con abbastanza neuroni, la rete puo' "imparare" a
# riprodurre qualsiasi pattern matematico. La LogisticRegression e' una
# linea retta nello spazio delle feature: separa due classi solo se sono
# linearmente separabili. La rete neurale puo' tracciare confini di
# qualunque forma (curvi, a S, a spirale).
#
# Limite: il teorema dice CHE ESISTE una rete che funziona, NON come
# trovarla. E' come dire "esiste una strada per Milano" senza dare il
# GPS. Il "GPS" e' la BACKPROPAGATION (cap.03 M3).
#
# Per il web dev: l'UAT e' come dire "qualunque API tu voglia esporre,
# esiste un modo di scriverla in Laravel". Vero ma poco utile finche'
# non sai come scrivere il codice.


# TODO 3.1 (10 minuti):
# Riproduci _esempio_rete_2_layer_su_csv() senza guardarlo. Pero':
#   (a) prova SEI valori diversi di h: 4, 8, 16, 32, 64, 128
#   (b) per ogni h stampa l'accuracy della rete RANDOM
#   (c) le accuracy sono tutte vicino a 0.5? Spiega in 1 riga perche' (sugg.:
#       cosa fa una rete random sui dati?)
# TUO CODICE QUI:

print("\nTODO 3.1\n")

def my_rete_2_layer_su_csv(h: int):
    # from sklearn.linear_model import LogisticRegression
    from sklearn.preprocessing import StandardScaler
    from sklearn.metrics import accuracy_score
    
    X, y = carica_pratiche()
    
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # clf = LogisticRegression(max_iter=1_000, random_state=42)
    # clf.fit(X_scaled, y)
    # pred_clf = (clf.predict_proba(X_scaled)[:, 1] >= 0.5).astype(int)
    # acc_clf = accuracy_score(y, pred_clf)
    
    d = X_scaled.shape[1]
    
    W1, b1 = init_pesi_he(d, h)
    W2, b2 = init_pesi_he(h, 1)
    
    _, P = rete_2_layer(X_scaled, W1, b1, W2, b2)
    pred_rete = (P >= 0.5).astype(int)
    acc_rete = accuracy_score(y, pred_rete)
    print(f"h: {h} => {acc_rete}")
    
h_values = np.array([4, 8, 16, 32, 64, 128])

for h in h_values:
    my_rete_2_layer_su_csv(h)
    
# in realtà i valori sono del tutto randomici, e non sembrano avere nessuna correlazione con il valore di h.
# molte volte si avvicinano allo 0.5, ma per ogni riga del csv equivale a lanciare una moneta.

# TODO 3.2 (8 minuti) — Visualizzare ReLU su più neuroni nascosti
#
# Obiettivo:
#   Capire a occhio cosa fa ReLU (Rectified Linear Unit: max(0, z)) quando
#   applichi UN layer nascosto a molti valori di input sulla stessa feature.
#   Non stai addestrando la rete: pesi e bias sono random, solo per vedere le forme.
#
# Cosa devi produrre:
#   Un PNG con 5 curve sovrapposte → salvato in:
#   modulo_03_dl_cv/figures/02_relu_attivazioni.png
#
# Traccia (shape esplicite — controllale con .shape prima del plot):
#   1) rng = np.random.default_rng(42)   # seed fisso = grafico ripetibile
#   2) Griglia input (una sola feature, molti punti):
#        x_grid = np.linspace(-5, 5, 200).reshape(-1, 1)   # (200, 1)
#   3) Layer nascosto con h=5 neuroni (pesi random, NON serve He init qui):
#        W1 = rng.standard_normal((1, 5))    # (1, 5)
#        b1 = rng.standard_normal(5)         # (5,)
#   4) Logit poi attivazione (usa la funzione relu() già definita sopra):
#        z = x_grid @ W1 + b1               # (200, 5) — broadcasting su b1
#        H = relu(z)                         # (200, 5) — stessa shape di z
#   5) Grafico:
#        - asse x: i 200 valori di x_grid (es. x_grid.ravel() o [:, 0])
#        - asse y: per ogni colonna j in {0..4}, plotta H[:, j]
#        - legenda opzionale: "neurone 0" … "neurone 4"
#        - titolo tipo: "ReLU su 5 neuroni nascosti (pesi random)"
#   6) plt.savefig(...); plt.close()  — crea la cartella figures/ se manca
#
# Cosa dovresti vedere (1 riga in commento dopo il plot):
#   5 "rampe" che restano a 0 fino a un certo x, poi salgono con pendenza diversa:
#   ogni neurone taglia e inclina in modo diverso → pezzi semplici che la rete
#   può combinare (intuizione del teorema di approssimazione universale — UAT:
#   "con abbastanza neuroni puoi approssimare funzioni complicate").
#
# Errori da evitare:
#   - Non limitare ReLU al solo vettore 1D: qui z e H sono (200, 5).
#   - Non usare sigmoid nel layer nascosto: in questo TODO è solo ReLU.
#
# TUO CODICE QUI:

print("TODO 3.2")
x_grid = np.linspace(-5, 5, 200).reshape(-1, 1)
rng = np.random.default_rng(42)
W1 = np.sort(rng.standard_normal(size=(1, 5), dtype=float).ravel()).reshape(1, 5)
b1 = rng.standard_normal(size=(5, ), dtype=float)

z = x_grid @ W1 + b1
H = relu(z)

x_ax = x_grid.ravel()

y_arr = [H[:, j] for j in range(0, H.shape[1])]

fig_dir_path = os.path.join(os.path.dirname(__file__),"reti_neurali_plot")
os.makedirs(fig_dir_path, exist_ok=True)

plt.title("Grafico ReLU su 5 neuroni nascosti")
plt.xlabel("Valori di X da -5 a +5")
plt.ylabel("Valori dell'attivazione del Neurone per i valori di X")
for i, y_ax in enumerate(y_arr):
    plt.plot(x_ax, y_ax)    
out = os.path.join(fig_dir_path, "02_relu_attivazioni.png")
plt.savefig(out, dpi=300)
plt.close()

fig, axes = plt.subplots(1, 5, figsize=(8, 8), sharex=True, sharey=True)
fig.suptitle("Grafici Singoli ReLU su 5 neuroni nascosti")
fig.supxlabel("Valori delle 'Features'", fontsize=8)
fig.supylabel("Valore ritornato da RELU", fontsize=8)
fig.tight_layout(rect=[0, 0, 1, 0.92])
for i, (w, ax) in enumerate(zip(W1.ravel(), axes)):
    ax.plot(x_ax, H[:, i])
    ax.set_title(f"Relu per w = {round(w, 3)}", fontsize=8) # Titolo
    ax.grid(True, alpha=0.3) # Griglia (semi-trasparente)                                       # Mostra la legenda
out = os.path.join(fig_dir_path, "03_relu_attivazioni_grafici_singoli.png")
plt.savefig(out, dpi=300)
plt.close()

# si nota che in base al valore del dot del peso del singolo neurone, si produce o meno un attivazione

# ==========================================================================
# QUIZ DI VERIFICA (fai PRIMA di passare agli esercizi)
# ==========================================================================

# V1) X (N, d), W1 (d, h1), W2 (h1, h2), W3 (h2, k). Che shape ha
#     l'output finale Z = (((X @ W1) @ W2) @ W3) ? Spiega.
# TUA RISPOSTA:
# (N, k).

# V2) Una rete 2-layer con ReLU nello strato nascosto. Se imposti tutti
#     i pesi a zero, P.mean() vale circa: (a) 0  (b) 0.5  (c) 1  (d) random
#     Perche'?
# TUA RISPOSTA:
# La risposta corretta è (b). Questo perchè se i pesi sono impostati tutti 0 (e assumendo che anche i bias siano 0), per ogni riga il dot product, indipendentemente dal numero di pesi, produrrà 0 per ogni riga. All'attivazione tramite sigmoide nel ultimo layer, la funzione ricevendo per ogni riga valore 0, produrrà per ogni riga 0.5.

# V3) Cosa dice (in parole umane) l'Universal Approximation Theorem?
#     E qual e' il suo limite pratico?
# TUA RISPOSTA:
# Se si hanno abbastanza neuroni in un hydden layer, in teoria sarebbe possibile approssimare il risultato di qualunque funzione continua. I limiti sono sostanzialmente 3: 
# Il teorema dice che esiste la strada, ma non indica ne dove ne come raggiungerla (non è un gps).
# Abbastanza neuroni può potenzialmente essere un numero enorme, che non è possibile avere.
# L'approssimazione fatta sul training rimane sostanzialmente diversa dal mondo reale.


# V4) [Trova l'errore]
#       W1 = rng.standard_normal((4, 8)) * 100.0
#       b1 = np.zeros(8)
#       H = sigmoid(X @ W1 + b1)
#     Cosa succede a H se i pesi sono "troppo grandi"? Perche' usare He
#     init invece?
# TUA RISPOSTA:
# avendo moltiplicato tutti i valori dei pesi * 100, questo può generare dei dot product molto grandi, rischiando di bloccare il calcolo della sigmoide per via di risultati troppo grandi o troppo piccoli (clipping, di solito si cerca di bloccare tutto nel range -500 +500). con He init, invece noi ancoriamo la scala al numero delle righe di W tramite la formula [W con shape(d, h) * np.sqrt(2 / d)]. in questo modo più è lungo W, minori saranno i risultati dei singoli prodotti di X * W, riuscendo così a gestire il valore finale del dot product e controllarlo in fase di test.

# V5) Quale di queste reti e' EQUIVALENTE a una LogisticRegression?
#     (a) 1 layer Dense con sigmoid
#     (b) 2 layer Dense con ReLU+sigmoid
#     (c) 2 layer Dense senza attivazione interna + sigmoid finale
#     Spiega anche le altre (perche' non sono LR).
# TUA RISPOSTA:
# La risposta corretta è (a). la seconda è una rete neurale, e non un LogisticRegressor. L'ultimo invece è equivalente al primo, perchè senza attivazioni intermedie il modello collassa in un unico layer.

# V6) [Recap shape] In una rete X (N=100, d=7) -> hidden (h=32) -> output
#     binario, quanti PARAMETRI ALLENABILI ha la rete in totale?
#     (suggerimento: W1, b1, W2, b2)
# TUA RISPOSTA:
# La risposta è ((7 * 32) + 32) + ((32 * 1) + 1) => 289. 7 pesi per 32 neuroni nel layer hidden più il bias di ogni neurone, più altri 32 pesi per 1 neurone più bias nel layer di output.

# V7) [Feynman - vincoli stretti] Spiega in 4 righe a tua madre (zero
#     informatica) cos'e' una rete neurale. VIETATO: matematica, codice,
#     "intelligenza artificiale", "computer".
# TUA RISPOSTA:
# ...


# ==========================================================================
# ESERCIZI FINALI
# ==========================================================================

# E1) [COLLOQUIO] - 15 minuti
#     "Disegna a mano (o descrivi a parole) una rete neurale 2-layer per
#     classificare le pratiche del nostro CSV M2 (7 feature, classe
#     binaria 'alterata'). Indica:
#       - shape di X, W1, b1, H, W2, b2, Z, P
#       - attivazione su ogni layer (e perche')
#       - quanti parametri ha la rete (numeri concreti)
#       - come si confronta con la LogisticRegression del Modulo 2"
#     Massimo 12 righe in totale, niente codice (puoi descrivere
#     le shape con "(N, d)" ecc.).
# TUA RISPOSTA:
# ...


# E2) [REFACTORING] - 10 minuti
#     Questo codice gira ma e' brutto su 3 dimensioni:
#       - pattern #25: type hint usa "np.array" (e' una funzione, non un tipo)
#       - pattern #23: virgole spurie a fine return
#       - logica: 2 loop annidati invece di X @ W
#       - leggibilita': variabili "tmp" senza significato
#
#     def forward_brutto(X: np.array, W: np.array, b) -> np.array:
#         tmp = []
#         for i in range(len(X)):
#             riga = []
#             for j in range(W.shape[1]):
#                 t = 0
#                 for k in range(W.shape[0]):
#                     t += X[i][k] * W[k][j]
#                 riga.append(t + b[j])
#             tmp.append(riga)
#         return np.array(tmp),
#
#     Riscrivilo con type hint corretti, vettorizzato (1 sola "@") e
#     ValueError se le shape non sono coerenti.
# TUO CODICE QUI:


# E3) [DEBUG] - autonomo, niente scala progressiva (regola corso)
#     Questo codice gira ma la P.mean() viene SEMPRE 0.5 esatto. Eppure
#     i pesi NON sono zero. Trova il bug.
#
#         rng = np.random.default_rng(0)
#         X = rng.standard_normal((50, 7))
#         W1, b1 = init_pesi_he(7, 16, seed=1)
#         W2, b2 = init_pesi_he(16, 1, seed=2)
#         # FORWARD
#         H = layer_dense(X, W1, b1, att=None)   # <-- guarda qui
#         Z = layer_dense(H, W2, b2, att=None)
#         P = sigmoid(Z).ravel()
#         print(P.mean())
#
#     Quando hai trovato il bug, scrivi qui sotto:
#       - cosa hai diagnosticato (1 riga)
#       - come l'hai sistemato (1 riga di codice corretto)
# TUA RISPOSTA / FIX:
# ...


# E4) [RETRIEVAL] - regola 15: riscrivi da zero una funzione di un capitolo
#                    PRECEDENTE, senza guardare il file vecchio.
#     Senza riaprire `modulo_03_dl_cv/01_neurone_artificiale.py`, riscrivi
#     da zero la funzione "neurone_batch(X, w, b) -> NDArray" del cap.01 M3.
#     Deve:
#       - shape check: X 2D, w 1D, X.shape[1] == w.shape[0]
#       - usare la TUA sigmoid (gia' importata in questo file)
#       - NON usare loop Python
#       - type hint con NDArray[np.float64] (Pattern #25)
#
#     Verifica:
#       neurone_batch(X(3,4), w(4,), 0.0) -> shape (3,) con tutti valori in (0, 1).
# TUO CODICE QUI:


# E5) [INTERLEAVING] cap.01 M3 (sigmoid stabile) + cap.02 M3 (rete 2-layer)
#     Hai una rete 2-layer con W1, W2 init He su 7 feature, h=16. Se
#     "scaliamo" i pesi W1, W2 di un fattore 100 (cioe' W1 *= 100,
#     W2 *= 100):
#       (a) cosa succede ai logit Z dell'ultimo layer? (suggerimento:
#           prova in codice e stampa Z.min(), Z.max())
#       (b) cosa succede alle probabilita' P? (suggerimento: sigmoid
#           satura, R6)
#       (c) la sigmoid stabile di cap.01 M3 (con clip ±500) ha
#           comportamento "graceful" o esplode in NaN/Inf?
#
#     Usa X dal CSV M2 scalato. Mostra le statistiche min/max/mean prima
#     e dopo la scalatura dei pesi.
# TUO CODICE QUI:


# E6) [REAL-WORLD] - REGOLA NEL CORSO DAL M5, MA UTILE GIA' QUI
#     Scenario vago: "il tuo capo broker dice 'voglio una rete neurale
#     che decide se la pratica e' alterata, ma piu' precisa di quella
#     vecchia (LogisticRegression)'. Ha sentito che 'le reti neurali
#     sono migliori'." Tu, prima di lanciarti a scrivere codice:
#       (a) quali 3 DOMANDE fai al capo prima di scegliere l'architettura?
#       (b) quale POTENZIALE PROBLEMA c'e' nel dire "rete neurale meglio
#           di LR" su questo dataset specifico? (suggerimento: dimensione
#           dataset, interpretabilita', deploy)
#       (c) se accettassi l'incarico, partiresti con una rete 2-layer
#           h=16, h=128, o ancora piu' grande? Perche'?
#
#     Massimo 8 righe per ogni punto, ragionamento di sistema.
# TUA RISPOSTA:
# ...


# ==========================================================================
# MINI-PROGETTO - "rete_2_layer_vs_logreg"
# ==========================================================================
#
# OBIETTIVO: misurare le predizioni di una rete 2-layer NON addestrata
# (pesi random He) e confrontarle con LogisticRegression M2 (allenata).
# Risultato atteso: la rete NON addestrata va peggio (accuracy ~ 0.5,
# AUC ~ 0.5). E' una baseline su cui il cap.03 M3 dovra' migliorare.
#
# Firma:
#     def rete_2_layer_vs_logreg(h: int = 16, seed: int = 42) -> dict[str, float]:
#         """
#         Ritorna un dict con:
#             'acc_rete'     : accuracy della rete random
#             'acc_logreg'   : accuracy di LogisticRegression
#             'auc_rete'     : roc_auc della rete random
#             'auc_logreg'   : roc_auc di LogisticRegression
#             'n_param_rete' : numero di parametri allenabili della rete
#         """
#
# Vincoli OBBLIGATORI:
#   - usa StandardScaler per scalare X (come M2 e cap.01 M3)
#   - init_pesi_he per (W1, b1) e (W2, b2)
#   - usa la TUA rete_2_layer, non scikit-learn MLPClassifier
#   - calcola anche roc_auc_score (sklearn.metrics)
#   - n_param_rete = W1.size + b1.size + W2.size + b2.size
#
# Verifica: stampa il dict alla fine. Ti aspetti:
#   - acc_rete ~ 0.5      (random)
#   - acc_logreg > 0.85   (allenata + dataset separabile)
#   - auc_rete ~ 0.5      (la rete non distingue)
#   - auc_logreg > 0.85   (la LR distingue molto)
#   - n_param_rete = 7*16 + 16 + 16*1 + 1 = 145
# TUO CODICE QUI:


# ==========================================================================
# CHECKPOINT FINALE (auto-verifica)
# ==========================================================================

# C1) In 1 frase: cos'e' un LAYER DENSE e quale operazione esegue?
# TUA RISPOSTA:
# ...

# C2) Hai una rete con W1 (5, 8) e W2 (8, 3). Che shape ha l'output finale
#     su X (50, 5)? (NO codice, ragionamento a mano)
# TUA RISPOSTA:
# ...

# C3) Perche' una rete con SOLO attivazioni lineari non e' "potente"
#     come una rete con ReLU? Risposta in 2 righe, no formule.
# TUA RISPOSTA:
# ...

# C4) Auto-rating onesto (compila in chiusura capitolo):
#       - layer Dense = X @ W + b:           /10
#       - importanza dell'attivazione (R2):   /10
#       - inizializzazione He vs zero (R5):   /10
#       - forward rete 2-layer su CSV M2:     /10
#       - Universal Approximation (intuiz.):  /10
# TUE RISPOSTE:
# ...


# ==========================================================================
# SOLUZIONI QUIZ (NON BARARE - leggi solo dopo aver risposto)
# ==========================================================================
"""
QUIZ D'INGRESSO

Q1) X @ W1 ha shape (200, 16). b1 DEVE avere shape (16,) - un bias per
    ogni neurone del layer 1. Il bias viene "broadcast" sulle 200 righe.

Q2) Senza attivazione non lineare in mezzo, due layer Dense collassano a
    UNO solo: X @ W1 @ W2 = X @ (W1 @ W2). Non aggiungi capacita'
    espressiva. L'attivazione (ReLU/tanh/sigmoid) "rompe" la linearita'
    e permette alla rete di approssimare funzioni complesse.

Q3) sigmoid -> ULTIMO layer di classificatore binario (vuoi output [0, 1]).
    ReLU    -> layer NASCOSTI (non satura, gradiente sano, M3 cap.03).
    Sigmoid nei layer nascosti satura e fa "vanishing gradient" (un
    classico problema del DL anni '90 risolto proprio sostituendola con
    ReLU).

Q4) P.mean() = 0.5 esatto. Pesi zero -> H = ReLU(0) = 0 -> Z = 0 + b2 = b2.
    Se anche b2 = 0, Z = 0 e sigmoid(0) = 0.5. La rete e' "rotta": tutti
    i neuroni dello strato hidden imparerebbero la stessa cosa, e nemmeno
    li addestrandola con backprop si separerebbero ("symmetry breaking"
    rotto).

Q5) (Feynman, esempio):
    "Pensa a una macchina che prende dei numeri in input e li mescola
    con dei 'pesi' che decide lei. Lo fa due volte di fila, fra una
    mescolata e l'altra c'e' un 'filtro' che butta via i numeri negativi.
    Alla fine ti dice un voto fra 'nessun mutuo' e 'mutuo sicuro'. E'
    bravo a mescolare i numeri in modi che noi non sapremmo programmare
    a mano."


QUIZ DI VERIFICA

V1) Output shape: (N, k). Le moltiplicazioni matrici si compongono:
    (N, d) @ (d, h1) @ (h1, h2) @ (h2, k) = (N, k). Le dimensioni
    "intermedie" si cancellano: ogni layer "trasforma" lo spazio.

V2) (b) 0.5. ReLU(0) = 0, sigmoid(0) = 0.5. Inoltre tutti i neuroni
    dello strato hidden sono identici (symmetry breaking rotto -> bug R5).

V3) UAT: una rete 2-layer con abbastanza neuroni nascosti puo'
    approssimare QUALSIASI funzione continua. Limite: il teorema dice
    CHE ESISTE una rete che funziona, non COME trovarla (il "come" e' la
    backpropagation - cap.03 M3). E nella pratica "abbastanza neuroni"
    puo' significare milioni, quindi conta anche l'efficienza.

V4) Con W1 * 100 i logit Z1 = X @ W1 saranno enormi -> sigmoid satura a
    0 o 1 -> derivata di sigmoid in saturazione ~ 0 -> impari poco o
    nulla (M3 cap.03). He init scala W con sqrt(2/d) proprio per evitare
    questo: tiene |Z1| in un range "sano" all'inizio.

V5) (a). 1 layer Dense + sigmoid = LogisticRegression letteralmente
    (e' il caso h=1, att=sigmoid: lo hai dimostrato in E7 cap.01 M3).
    (b) e' una vera rete 2-layer (piu' potente).
    (c) collassa a 1 layer lineare ma con sigmoid finale = LR... sui
    coefficienti combinati (W1 @ W2). E' "moralmente" una LR, ma
    riparametrizzata in modo strano.

V6) W1: 7 * 32 = 224 parametri. b1: 32. W2: 32 * 1 = 32. b2: 1.
    Totale: 224 + 32 + 32 + 1 = 289 parametri allenabili.

V7) (Feynman tipo):
    "E' come una squadra di assaggiatori in cucina. Ogni assaggiatore
    sente un sapore (dolce, salato, amaro...) e gli da' un voto. Poi
    i loro voti li sente un capo-cuoco che, mescolandoli, decide se la
    minestra e' 'buona' o 'da rifare'. Gli assaggiatori e il capo
    imparano col tempo a dare i voti giusti, guardando i risultati."


CHECKPOINT FINALE

C1) Un layer Dense (Fully Connected) e' la trasformazione
    H = att(X @ W + b), dove W ha shape (d_input, h) e b shape (h,).
    Mappa N pratiche da d feature in h "feature derivate".

C2) Output: (50, 3). Step:
    X (50, 5) @ W1 (5, 8) = (50, 8)
    (50, 8) @ W2 (8, 3) = (50, 3).

C3) Una rete tutta lineare equivale a UN solo layer lineare (puoi
    collassare W1 @ W2 in un'unica matrice). Con ReLU la composizione
    non e' piu' "appiattibile": la rete puo' approssimare funzioni con
    curvature (UAT).
"""


# ==========================================================================
# ENTRY POINT (esegui solo le demo che esistono nel file, niente di tuo)
# ==========================================================================
if __name__ == "__main__":
    print("=" * 70)
    print("Cap.02 M3 - demo di riferimento")
    print("=" * 70)

    print("\n[Demo Sez.1 - 1 layer Dense]")
    _esempio_layer_dense()

    print("\n[Demo Sez.2 - rete 2-layer random]")
    _esempio_rete_2_layer_random()

    print("\n[Demo R2 - collasso lineare di 2 layer senza attivazione]")
    _demo_collasso_lineare()

    print("\n[Demo R5 - bug dell'init a zero]")
    _demo_init_zero()

    print("\n[Demo Sez.3 - rete 2-layer random vs LogisticRegression sul CSV M2]")
    try:
        _esempio_rete_2_layer_su_csv()
    except FileNotFoundError as exc:
        print("Skip: CSV M2 non trovato.", exc)
    except ImportError as exc:
        print("Skip: scikit-learn non disponibile in questo interprete.", exc)

    print("\n" + "=" * 70)
    print("Demo finite. Adesso tocca a te: completa i TODO in ordine.")
    print("Quando vuoi una valutazione: 'valuta cap.02 M3 sezione X.Y'.")
    print("=" * 70)
