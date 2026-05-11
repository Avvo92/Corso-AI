"""
============================================================================
MODULO 3 (DL & CV) - CAPITOLO 03
"Backpropagation": come fa una rete a IMPARARE i propri pesi
============================================================================

⚠️  CAPITOLO PIU' TOSTO DEL MODULO (difficolta' attesa: 9/10).
    Vai LENTO. Ogni concetto viene tradotto in codice eseguibile e in
    un grafico PRIMA di vedere la formula in parole. NIENTE LaTeX.

----------------------------------------------------------------------------
DA DOVE ARRIVI (cap.02 M3)
----------------------------------------------------------------------------
Nel cap.02 M3 hai costruito una RETE 2-layer:

    H = ReLU(X @ W1 + b1)        # hidden     shape (N, h)
    P = sigmoid(H @ W2 + b2)     # output     shape (N, 1) -> (N,)

E hai notato che la rete con PESI RANDOM fa accuracy ~ 0.5: e' una
moneta truccata, non un classificatore.

Domanda chiave: COME le insegniamo a fare meglio?

Risposta: BACKPROPAGATION. E' l'algoritmo che, dato un errore di
predizione, calcola "di quanto" ogni peso della rete e' responsabile di
quell'errore e lo aggiorna nella direzione giusta.

Tre concetti collegati, tutti tradotti qui in codice prima che in formule:

  1) LOSS (errore di previsione)        -> "quanto sbagliamo, in numeri"
  2) GRADIENT (vettore di derivate)     -> "in che direzione cambiare i pesi"
  3) GRADIENT DESCENT (discesa)         -> "fai un passetto in quella direzione"

E poi:
  4) CHAIN RULE                         -> "come si propaga il gradiente
                                            da output a input"
  5) BACKPROPAGATION                    -> "chain rule applicata a una rete"
  6) LEARNING RATE                      -> "quanto e' grande il passetto"

Per chi viene dal web dev: la backprop e' come il "git bisect" della rete.
La rete sbaglia? Bene, andiamo a ritroso da output a input e troviamo
"quale layer/peso e' responsabile e di quanto". Solo che invece di
binary search, usiamo derivate.

----------------------------------------------------------------------------
COSA PORTI VIA DA QUESTO CAPITOLO (Definition of Done)
----------------------------------------------------------------------------
Alla fine sai rispondere "in 1 riga" a queste 6 domande:

  1) Cos'e' una LOSS e perche' la binary cross-entropy e non l'MSE per
     classificazione binaria?                                      -> Sez. 1
  2) Cos'e' la DERIVATA (parla di pendenza, non di limiti)?         -> Sez. 2
  3) Cos'e' il GRADIENTE in 2D? (NO formule, solo geometria)         -> Sez. 3
  4) Cos'e' la CHAIN RULE? Spiegala con una pipeline web.            -> Sez. 4
  5) Come fai 1 STEP di gradient descent su w?                       -> Sez. 5
  6) Cosa succede se il LEARNING RATE e' troppo grande / troppo piccolo? -> Sez. 5

Hai anche scritto 6 funzioni riutilizzabili:
  - bce_loss            (binary cross-entropy)
  - derivata_numerica   (sanity check delle derivate analitiche)
  - gradient_descent    (loop di ottimizzazione su funzione semplice)
  - forward_2layer      (riprende cap.02 M3 ma "ricorda" le attivazioni intermedie)
  - backward_2layer     (calcola gradienti dW1, db1, dW2, db2)
  - train_rete_2_layer  (loop forward -> loss -> backward -> update)

E hai dimostrato (mini-progetto) che la rete 2-layer del cap.02 M3
ADESSO addestrata sul CSV M2 BATTE la LogisticRegression del cap.04 M2
(o almeno la pareggia, perche' il dataset e' semplice).

----------------------------------------------------------------------------
MAPPA DEL CAPITOLO
----------------------------------------------------------------------------
   *  PRONTUARIO TRANELLI BACKPROP        [B1] - [B8]
   *  QUIZ D'INGRESSO                     Q1 - Q5     (cerniera cap.02 M3)
   *  SEZIONE 1  LOSS: come misuriamo l'errore           1.1 - 1.3
   *  SEZIONE 2  DERIVATA come pendenza                  2.1 - 2.3
   *  SEZIONE 3  GRADIENTE come vettore di pendenze      3.1 - 3.3
   *  SEZIONE 4  CHAIN RULE: derivate concatenate        4.1 - 4.2
   *  SEZIONE 5  GRADIENT DESCENT e learning rate         5.1 - 5.3
   *  SEZIONE 6  BACKPROP + TRAINING su rete 2-layer     6.1 - 6.3
   *  QUIZ DI VERIFICA                    V1 - V8
   *  ESERCIZI FINALI                     E1 - E7
                                          (colloquio / refactor / debug /
                                           retrieval / interleaving / real-world)
   *  MINI-PROGETTO                       train_rete_su_csv_m2
   *  CHECKPOINT FINALE                   C1 - C5
   *  SOLUZIONI QUIZ                      in fondo

----------------------------------------------------------------------------
COME USARE QUESTO FILE (regola del corso)
----------------------------------------------------------------------------
   1. Leggi in ORDINE. Le sezioni 4-5-6 dipendono dalle 1-2-3.
   2. Per ogni TODO scrivi nel blocco "TUO CODICE" (non cancellare lo
      scaffold).
   3. Quando vuoi una valutazione: "valuta cap.03 M3 sezione X.Y"
   4. Se ti blocchi >15 min (capitolo difficile, si concede tempo extra):
      "sono bloccato sezione X" -> ti do un'IDEA, mai la soluzione.
   5. Niente LaTeX (preferenza tua): tutte le derivate sono in PAROLE +
      codice + grafico.
   6. Hardware: tutto su CPU + NumPy + Matplotlib. PyTorch arriva al cap.04.
   7. Se a meta' capitolo sei perso -> ferma, recap, NON proseguire. Meglio
      una sessione in piu' che incrociare le derivate.
"""

import os
from typing import Callable
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy.typing import NDArray


# ==========================================================================
# PRONTUARIO TRANELLI BACKPROP - leggilo PRIMA di iniziare (8 minuti)
# ==========================================================================
#
# [B1] LOSS != ACCURACY.
#      Accuracy = "quante predizioni giuste in %". Discreta (0 o 1).
#      Loss    = "quanto sbagliamo, su scala continua, derivabile".
#      Si addestra MINIMIZZANDO la loss, non massimizzando l'accuracy
#      (l'accuracy non e' derivabile -> backprop non funziona).
#
# [B2] BCE (Binary Cross-Entropy) per classificazione binaria, NON l'MSE.
#      L'MSE punisce "poco" gli errori di classificazione (es. previsione
#      0.51 quando la verita' e' 1: errore quadratico 0.24, "piccolo").
#      La BCE punisce in modo INFINITO quando p -> 0 e y = 1 (cioe' la
#      rete dice "sicurissima sbagliata"). Il gradiente e' molto piu' netto.
#
# [B3] DERIVATA = PENDENZA della funzione, NON "limite di rapporto
#      incrementale" (quella e' la definizione, ma non la useremo).
#      In codice: derivata = (f(x + h) - f(x - h)) / (2 * h)  con h piccolo.
#      Visivamente: e' la pendenza della retta tangente alla curva.
#
# [B4] GRADIENTE = vettore di derivate parziali, una per ogni variabile
#      della funzione. In 2D: grad = [df/dx, df/dy]. Geometricamente:
#      punta nella DIREZIONE di maggior CRESCITA della funzione.
#      Per MINIMIZZARE, si va nella direzione OPPOSTA: w_new = w - lr * grad.
#
# [B5] CHAIN RULE in parole: "la derivata di una composizione e' il
#      prodotto delle derivate". Se h = f(g(x)), allora:
#           dh/dx = df/dg * dg/dx
#      In una rete: per sapere "di quanto" un peso del primo layer
#      influenza la loss, devi moltiplicare le derivate "strato per strato"
#      dall'output al peso.
#
# [B6] LEARNING RATE (lr) e' un IPER-PARAMETRO, non un parametro.
#      lr troppo grande -> rimbalzi sopra il minimo (loss oscilla)
#      lr troppo piccolo -> impari lentissimo (servono milioni di step)
#      Tipici valori iniziali: 1e-3 (0.001), 1e-2 (0.01).
#
# [B7] OGNI BACKWARD HA SHAPE = shape del peso corrispondente.
#      dW1 ha la STESSA shape di W1.
#      db1 ha la STESSA shape di b1.
#      Se shape non coincidono -> bug. Stampa SEMPRE le shape in debug.
#
# [B8] FORWARD CACHE le attivazioni intermedie, BACKWARD le rilegge.
#      Per calcolare i gradienti del layer 1 ti serve H (output del
#      layer 1) che hai gia' calcolato nel forward. NON ricalcolarlo
#      nel backward: passalo come argomento (o salvalo in un dict
#      "cache" - pattern moderno).


# ==========================================================================
# QUIZ D'INGRESSO - cerniera cap.02 M3 -> cap.03 M3
# ==========================================================================

# Q1) Hai una rete 2-layer e la addestri. Cos'e' la LOSS (1 riga)?
#     E cos'e' l'ACCURACY (1 riga)? Qual e' la differenza importante per
#     la backpropagation?
# TUA RISPOSTA:
# ...

# Q2) Hai f(x) = x^2. La PENDENZA della curva in x = 3 e' positiva o
#     negativa? E in x = -3? Spiega "geometricamente" senza derivate.
# TUA RISPOSTA:
# ...

# Q3) Una rete sbaglia molto su una pratica: previsione p = 0.05, verita'
#     y = 1. Qual e' l'errore "intuitivo" della rete? E in che direzione
#     dovresti spostare i pesi? (su o giu', cioe' aumentarli o diminuirli?)
# TUA RISPOSTA:
# ...

# Q4) [Recall cap.02 M3] Hai una rete con W1 (4, 8) e W2 (8, 1). Quanti
#     PARAMETRI totali ha la rete? (W1, b1, W2, b2)
# TUA RISPOSTA:
# ...

# Q5) [Feynman - no jargon] Spiega in 4 righe a un collega web dev cos'e'
#     un "loop di training". Vietato: gradiente, derivata, loss, layer,
#     pesi, neurone.
# TUA RISPOSTA:
# ...


# ==========================================================================
# SEZIONE 1 - LOSS: COME MISURIAMO L'ERRORE
# ==========================================================================

# ---------------------- ANALOGIA --------------------------------------------
# Un broker che valuta pratiche sbaglia. Domanda: come misuri quanto
# sbaglia? Due opzioni:
#
#   (1) ACCURACY (= % di pratiche correttamente classificate)
#       Pro: facile da capire ("ho azzeccato 9 su 10").
#       Contro: discreta. Se ho previsto 0.51 vs verita' 1, e' "giusto" al
#               51%. Se ho previsto 0.99 vs verita' 1, e' "giusto" al 99%.
#               L'accuracy NON DISTINGUE: entrambi i casi sono "1 corretto".
#               Non posso usare l'accuracy per dire alla rete "sei stato
#               poco sicuro, sii piu' sicuro".
#
#   (2) LOSS (Binary Cross-Entropy)
#       Una formula che da' un numero CONTINUO. Piu' la rete e' sicura
#       della risposta giusta, piu' la loss e' bassa. Piu' la rete e'
#       sicura della risposta SBAGLIATA, piu' la loss esplode (tende a
#       +infinito).
#       Pro: derivabile. La rete puo' chiedersi "se sposto questo peso di
#            poco, la loss scende o sale?".
#       Contro: meno intuitiva di "9 su 10".
#
# Per il web dev: l'accuracy e' come "test passa/fallisce", la loss e'
# come "test con score 0-100, lascia spazio a 'quasi passato'".

# ---------------------- TEORIA + CODICE -------------------------------------
# 1.1 - BINARY CROSS-ENTROPY (BCE): la loss standard per classificazione
#       binaria.
#
# Per UNA pratica con verita' y in {0, 1} e probabilita' predetta p in (0, 1):
#
#       loss = - y * log(p) - (1 - y) * log(1 - p)
#
# In parole umane:
#   - se y = 1 (alterato): loss = -log(p)
#                          -> se p ~ 1 (previsto bene): -log(1) = 0      OK
#                          -> se p ~ 0 (previsto male): -log(0) = +inf   PUNIZIONE
#   - se y = 0 (genuino):  loss = -log(1 - p)
#                          -> se p ~ 0 (previsto bene): -log(1) = 0      OK
#                          -> se p ~ 1 (previsto male): -log(0) = +inf   PUNIZIONE
#
# Sul batch: si prende la MEDIA della loss su tutte le N pratiche.


def bce_loss(
    p: NDArray[np.float64],
    y: NDArray[np.int64] | NDArray[np.float64],
    eps: float = 1e-12,
) -> float:
    """Binary cross-entropy media su un batch.

    Args:
        p:   probabilita' predette in (0, 1), shape (N,)
        y:   verita' in {0, 1}, shape (N,)
        eps: clip per evitare log(0) numerico.

    Returns:
        loss media (scalare float >= 0). 0 = predizioni perfette.
    """
    if p.shape != y.shape:
        raise ValueError(f"shape diverse: p{p.shape} vs y{y.shape}")
    p_safe = np.clip(p, eps, 1.0 - eps)
    loss = - y * np.log(p_safe) - (1.0 - y) * np.log(1.0 - p_safe)
    return float(np.mean(loss))


# 1.2 - PERCHE' NON USIAMO L'MSE? (Mean Squared Error)
#
# MSE per classificazione binaria:    loss = mean((p - y)^2)
#
# Tecnicamente "funziona" come segnale di errore, ma:
#  - quando p ~ 0 e y = 1, MSE = (0 - 1)^2 = 1 (un numero limitato)
#  - quando p ~ 0 e y = 1, BCE = -log(0) = +inf (punizione enorme)
#
# La BCE costringe la rete a NON essere "sicurissima sbagliata".
# Inoltre, la derivata della BCE rispetto al logit z (PRIMA della
# sigmoid) si semplifica miracolosamente:
#
#       d(BCE)/dz = p - y           <- una sottrazione, niente piu'!
#
# E' uno dei motivi per cui in DL si combinano "sigmoid + BCE" e
# "softmax + cross-entropy": le derivate si semplificano.


def _confronto_bce_mse() -> None:
    """Stampa BCE vs MSE per varie predizioni con y = 1 (verita' alterato)."""
    y = np.array([1.0])
    print(f"{'p':>10} {'BCE':>10} {'MSE':>10}")
    for p_val in [0.01, 0.1, 0.5, 0.9, 0.99]:
        p = np.array([p_val])
        bce = bce_loss(p, y)
        mse = float(np.mean((p - y) ** 2))
        print(f"{p_val:>10.2f} {bce:>10.4f} {mse:>10.4f}")
    print("Quando p e' molto distante dalla verita' (p=0.01, y=1):")
    print(" - BCE = 4.6 (punizione grande)")
    print(" - MSE = 0.98 (punizione 'mite')")


# 1.3 - LOSS CURVE: come visualizzare la BCE in funzione di p


def _grafico_bce(
    out_path: str | None = None,
    show: bool = False,
) -> None:
    """Plot BCE(p) per y=0 e y=1 - mostra che la loss esplode in modo
    asimmetrico."""
    p = np.linspace(0.001, 0.999, 400)
    bce_y1 = - np.log(p)
    bce_y0 = - np.log(1.0 - p)
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(p, bce_y1, label="loss se y=1 (alterato)", color="#d62728")
    ax.plot(p, bce_y0, label="loss se y=0 (genuino)", color="#1f77b4")
    ax.set_xlabel("p (probabilita' predetta)")
    ax.set_ylabel("BCE loss (per pratica)")
    ax.set_title("Binary cross-entropy: la loss 'esplode' verso l'errore")
    ax.set_ylim(0, 5)
    ax.legend()
    ax.grid(True, alpha=0.3)
    if out_path:
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        fig.savefig(out_path, dpi=120, bbox_inches="tight")
    if show:
        plt.show()
    plt.close(fig)


# TODO 1.1 (5 minuti):
# Crea y = np.array([1, 0, 1, 0, 1]) e p = np.array([0.9, 0.1, 0.8, 0.2, 0.05])
# Calcola e stampa:
#   - la BCE media
#   - quale pratica contribuisce DI PIU' alla loss (suggerimento:
#     calcola le 5 loss singole e trova l'argmax)
# Spiega in 1 commento PERCHE' quella e' la pratica "peggiore".
# TUO CODICE QUI:


# TODO 1.2 (5 minuti):
# Verifica empiricamente che BCE perfetta = 0:
#   - y = np.array([1, 0, 1, 0])
#   - p = np.array([0.99999, 0.00001, 0.99999, 0.00001])    (quasi perfette)
#   - p = y  -> ATTENZIONE: log(0) = -inf. Usa eps=1e-12.
# Cosa stampa bce_loss in entrambi i casi? Perche' NON puoi mettere p = y
# senza il clip?
# TUO CODICE QUI:


# TODO 1.3 (3 minuti):
# Genera il grafico della BCE (gia' fornita la funzione) e salvalo in
#       modulo_03_dl_cv/figures/03_01_bce_loss.png
# Verifica che il file esista (os.path.exists).
# TUO CODICE QUI:


# ==========================================================================
# SEZIONE 2 - DERIVATA COME PENDENZA
# ==========================================================================

# ---------------------- ANALOGIA --------------------------------------------
# Sei in macchina su una strada di montagna. A ogni punto della strada
# hai una PENDENZA: positiva (in salita), negativa (in discesa), zero
# (pianeggiante).
#
# La derivata di una funzione f(x) in un punto x0 e' esattamente questo:
# "qual e' la pendenza della curva f nel punto x0?".
#
#   - pendenza > 0   -> se aumenti x, la funzione SALE
#   - pendenza < 0   -> se aumenti x, la funzione SCENDE
#   - pendenza = 0   -> sei in un punto piatto (massimo, minimo o sella)
#
# Per il web dev: la derivata e' come "il delta della response time se
# aumento di 1 il numero di utenti". Positivo = peggiora, negativo =
# migliora. E' una "sensibilita' al cambio".

# ---------------------- TEORIA + CODICE -------------------------------------
# 2.1 - DERIVATA NUMERICA: l'approccio "stupido ma sempre giusto"
#
# Definizione operativa: derivata di f in x e':
#
#       f'(x) = (f(x + h) - f(x - h)) / (2 * h)     con h piccolo (es. 1e-6)
#
# Questa formula si chiama "differenza centrata" ed e' piu' precisa
# della "differenza in avanti" (f(x+h) - f(x))/h.
#
# Quando serve la derivata numerica?
#   - in ottica didattica (qui): vedere "fisicamente" cosa fa la derivata
#   - in produzione: per VERIFICARE che le derivate analitiche scritte a
#     mano siano corrette (sanity check di backprop fatto bene).


def derivata_numerica(
    f: Callable[[float], float],
    x: float,
    h: float = 1e-6,
) -> float:
    """Derivata numerica di f in x via differenza centrata."""
    return (f(x + h) - f(x - h)) / (2.0 * h)


def _esempio_derivata() -> None:
    """Mostra derivata di f(x) = x^2 in vari punti (analitica = 2x)."""
    f = lambda x: x ** 2
    for x in [-3.0, -1.0, 0.0, 1.0, 3.0]:
        num = derivata_numerica(f, x)
        ana = 2.0 * x
        print(f"f(x)=x^2  x={x:+.1f}  derivata_num={num:+.4f}  analitica={ana:+.4f}")


# 2.2 - DERIVATE NOTE (te ne servono solo 3 per il M3)
#
#   f(x) = x^2          -> f'(x) = 2x
#   f(x) = e^x          -> f'(x) = e^x      (la sola che e' uguale a se stessa!)
#   f(x) = sigmoid(x)   -> f'(x) = sigmoid(x) * (1 - sigmoid(x))
#                          (compatta: si esprime tutta in funzione di
#                           sigmoid(x) stessa)
#   f(x) = ReLU(x)      -> f'(x) = 1 se x > 0, 0 se x < 0 (non definita in 0)
#   f(x) = log(x)       -> f'(x) = 1/x
#
# Ti aiuta a credere "a occhio" che il backprop di sigmoid sia stabile:
# la derivata massima e' 0.25 (in x=0) e tende a 0 ai bordi.


def _grafico_funzione_e_derivata(
    out_path: str | None = None,
    show: bool = False,
) -> None:
    """Plot f(x)=x^2 con la sua derivata sovrapposta."""
    x = np.linspace(-4, 4, 300)
    f = x ** 2
    df = 2 * x
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(x, f, label="f(x) = x^2", color="#1f77b4", lw=2)
    ax.plot(x, df, label="derivata f'(x) = 2x", color="#d62728", lw=2)
    ax.axhline(0, color="gray", lw=0.5)
    ax.axvline(0, color="gray", lw=0.5)
    ax.set_title("Funzione e sua derivata (pendenza)")
    ax.set_xlabel("x")
    ax.set_ylabel("valore")
    ax.legend()
    ax.grid(True, alpha=0.3)
    if out_path:
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        fig.savefig(out_path, dpi=120, bbox_inches="tight")
    if show:
        plt.show()
    plt.close(fig)


# 2.3 - DERIVATA DELLA SIGMOID (utile in backprop)


def sigmoid(z: NDArray[np.float64] | float) -> NDArray[np.float64] | float:
    """Sigmoid stabile (clip ±500)."""
    z_arr = np.asarray(z, dtype=float)
    z_safe = np.clip(z_arr, -500.0, 500.0)
    out = 1.0 / (1.0 + np.exp(-z_safe))
    if np.isscalar(z) or out.ndim == 0:
        return float(out)
    return out


def derivata_sigmoid(z: NDArray[np.float64]) -> NDArray[np.float64]:
    """Derivata della sigmoid: s(z) * (1 - s(z))."""
    s = sigmoid(z)
    return s * (1.0 - s)


def relu(z: NDArray[np.float64]) -> NDArray[np.float64]:
    """ReLU element-wise: max(0, z)."""
    return np.maximum(0.0, z)


def derivata_relu(z: NDArray[np.float64]) -> NDArray[np.float64]:
    """Derivata della ReLU: 1 se z > 0, 0 altrimenti (in 0 si sceglie 0)."""
    return (z > 0).astype(float)


# TODO 2.1 (5 minuti):
# Verifica numerica della derivata di sigmoid:
# Per z in [-3, -1, 0, 1, 3], confronta derivata_numerica(sigmoid, z) con
# la formula analitica derivata_sigmoid(z). Stampa entrambi i valori.
# Devono coincidere fino alla 4-5 cifra decimale.
# TUO CODICE QUI:


# TODO 2.2 (3 minuti):
# La derivata di sigmoid in z=0 vale 0.25. Quale e' il valore MASSIMO
# della derivata di sigmoid? (suggerimento: prova vari z e cerca il
# massimo, oppure ragionalo). Perche' questo numero piccolo crea problemi
# se hai TANTI layer (vanishing gradient)?
# TUO CODICE QUI:


# TODO 2.3 (5 minuti):
# Genera il grafico f(x)=x^2 + derivata e salvalo in
#       modulo_03_dl_cv/figures/03_02_derivata.png
# Verifica esistenza file.
# TUO CODICE QUI:


# ==========================================================================
# SEZIONE 3 - GRADIENTE COME VETTORE DI PENDENZE
# ==========================================================================

# ---------------------- ANALOGIA --------------------------------------------
# Adesso non sei su una strada (1D), sei su un PRATO IN COLLINA (2D).
# In ogni punto del prato hai DUE pendenze:
#   - pendenza verso EST (asse x)
#   - pendenza verso NORD (asse y)
#
# Il GRADIENTE in un punto e' un VETTORE [pendenza_x, pendenza_y].
# Geometricamente: punta nella direzione di MAGGIOR salita.
#
# Domanda chiave: SE VUOI SCENDERE (minimizzare), in che direzione vai?
# Risposta: nella direzione OPPOSTA al gradiente. Cioe' "-grad".
#
# La regola di aggiornamento del gradient descent:
#
#       w_new = w - lr * grad        (lr = learning rate, "lunghezza del passo")
#
# Per il web dev: e' come la dashboard "performance hotspots". Il
# gradiente indica QUALI variabili (response time, memoria...) stanno
# spingendo PEGGIORARE il sistema. Per migliorare, agisci nella
# direzione opposta a quel "vettore di problemi".

# ---------------------- TEORIA + CODICE -------------------------------------
# 3.1 - GRADIENTE NUMERICO (sanity check per backprop)
#
# In multivariato, il gradiente e' un vettore con UNA derivata parziale
# per ogni variabile della funzione. La derivata parziale rispetto a x_i
# si calcola muovendo SOLO x_i e tenendo le altre fisse.


def gradiente_numerico(
    f: Callable[[NDArray[np.float64]], float],
    x: NDArray[np.float64],
    h: float = 1e-6,
) -> NDArray[np.float64]:
    """Gradiente numerico via differenza centrata, una dimensione alla volta."""
    grad = np.zeros_like(x, dtype=float)
    for i in range(x.size):
        xp = x.copy(); xp.flat[i] += h
        xm = x.copy(); xm.flat[i] -= h
        grad.flat[i] = (f(xp) - f(xm)) / (2.0 * h)
    return grad


def _esempio_gradiente() -> None:
    """Gradiente di f(x, y) = x^2 + y^2 nel punto (3, 4) (atteso [6, 8])."""
    f = lambda v: float(v[0] ** 2 + v[1] ** 2)
    x0 = np.array([3.0, 4.0])
    g_num = gradiente_numerico(f, x0)
    g_ana = np.array([2 * 3.0, 2 * 4.0])
    print(f"f(x,y) = x^2 + y^2 in (3, 4)")
    print(f"gradiente numerico:  {g_num}")
    print(f"gradiente analitico: {g_ana}")


# 3.2 - GRADIENTE DI UNA FUNZIONE 2D: visualizzazione


def _grafico_gradiente(
    out_path: str | None = None,
    show: bool = False,
) -> None:
    """Plot 2D di f(x, y) = x^2 + y^2 con frecce del gradiente."""
    x = np.linspace(-3, 3, 12)
    y = np.linspace(-3, 3, 12)
    X, Y = np.meshgrid(x, y)
    F = X ** 2 + Y ** 2
    GX = 2 * X
    GY = 2 * Y

    fig, ax = plt.subplots(figsize=(7, 7))
    cs = ax.contour(X, Y, F, levels=10, colors="gray", linewidths=0.5)
    ax.clabel(cs, inline=True, fontsize=8)
    ax.quiver(X, Y, GX, GY, color="#d62728", alpha=0.6, scale=80)
    ax.plot(0, 0, "o", color="#2ca02c", markersize=12,
            label="minimo (0, 0)")
    ax.set_title("f(x, y) = x^2 + y^2: gradiente punta verso fuori\n"
                 "(per minimizzare bisogna andare CONTRO le frecce)")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.legend()
    ax.set_aspect("equal")
    ax.grid(True, alpha=0.3)
    if out_path:
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        fig.savefig(out_path, dpi=120, bbox_inches="tight")
    if show:
        plt.show()
    plt.close(fig)


# 3.3 - PERCHE' CI INTERESSA?
#
# Una rete neurale ha potenzialmente MIGLIAIA o MILIONI di pesi. La
# "loss" in funzione dei pesi e' una superficie ad altissima dimensione.
# Il gradiente ci dice: "per ognuno di questi milioni di pesi, di quanto
# spostarlo per far scendere la loss". E' la BUSSOLA della rete.


# TODO 3.1 (5 minuti):
# Calcola il gradiente numerico di f(x, y, z) = x^2 + 2*y^2 + 3*z^2 nel
# punto (1, 1, 1). Atteso: [2, 4, 6]. Verifica con assert.
# TUO CODICE QUI:


# TODO 3.2 (5 minuti):
# Per la funzione f(x, y) = x^2 + y^2 (paraboloide), prendi il punto
# iniziale x0 = np.array([3.0, 4.0]) e fai 1 STEP di gradient descent
# con lr = 0.1:
#       x1 = x0 - lr * gradiente(x0)
# Stampa x0, x1, f(x0), f(x1). f(x1) e' minore di f(x0)?
# TUO CODICE QUI:


# TODO 3.3 (3 minuti):
# Genera il grafico del gradiente 2D (gia' fornito) e salvalo in
#       modulo_03_dl_cv/figures/03_03_gradiente.png
# Verifica esistenza.
# TUO CODICE QUI:


# ==========================================================================
# SEZIONE 4 - CHAIN RULE: DERIVATE CONCATENATE
# ==========================================================================

# ---------------------- ANALOGIA --------------------------------------------
# Sei un controllore di qualita' in fabbrica. La pratica passa per 3
# stazioni di lavorazione (S1 -> S2 -> S3 -> output). Alla fine c'e' un
# difetto: la pratica e' venuta male. Vuoi sapere "di quanto" e'
# responsabile ogni stazione.
#
# Idea: per quantificare "quanto influisce S1 sul difetto finale", devi
# moltiplicare:
#   - "di quanto influisce S2 sull'output finale"
#   - "di quanto influisce S1 sull'output di S2"
#
# In matematica si chiama CHAIN RULE (regola di derivazione delle funzioni
# composte). Formula in parole:
#
#       output = S3( S2( S1( input ) ) )
#
#       d(output) / d(input) = d(S3)/d(out_S2) * d(S2)/d(out_S1) * d(S1)/d(input)
#
# E' una catena di prodotti. In una rete: andando dall'OUTPUT all'INPUT
# moltiplichi le derivate di ogni layer.
#
# Per il web dev: e' come un "trace ID" che propaga un'informazione
# attraverso una pipeline di micro-servizi. Ogni servizio "annota" il
# suo contributo all'errore finale.

# ---------------------- TEORIA + CODICE -------------------------------------
# 4.1 - ESEMPIO NUMERICO MINIMALE
#
# h(x) = (3x + 1)^2
#
# Si puo' vedere h come composizione:
#       g(x) = 3x + 1       -> g'(x) = 3
#       f(u) = u^2          -> f'(u) = 2u
#       h(x) = f(g(x))      -> h'(x) = f'(g(x)) * g'(x) = 2 * (3x + 1) * 3
#
# Verifichiamolo numericamente.


def _esempio_chain_rule() -> None:
    """Verifica chain rule su h(x) = (3x + 1)^2 in x = 2."""
    g = lambda x: 3 * x + 1
    f = lambda u: u ** 2
    h = lambda x: f(g(x))
    x = 2.0
    h_num = derivata_numerica(h, x)
    h_chain = 2.0 * (3 * x + 1) * 3.0   # f'(g(x)) * g'(x)
    print(f"h(x) = (3x + 1)^2 in x = {x}")
    print(f"derivata numerica:    {h_num:.4f}")
    print(f"chain rule analitica: {h_chain:.4f}")


# 4.2 - LA CHAIN RULE IN UNA RETE 2-LAYER (qualitativa, senza derivare a mano)
#
# Forward:
#       Z1 = X @ W1 + b1
#       H  = ReLU(Z1)
#       Z2 = H @ W2 + b2
#       P  = sigmoid(Z2)
#       L  = BCE(P, y)
#
# Per sapere "quanto W1 influisce sulla loss" applichiamo la chain rule
# dall'output all'input:
#
#       dL/dW1 = dL/dP * dP/dZ2 * dZ2/dH * dH/dZ1 * dZ1/dW1
#
# Questa moltiplicazione lunga e' la BACKPROPAGATION. Ogni "fattore" e'
# un pezzo della rete, e si calcolano in ordine INVERSO (da output a
# input). Nella Sez. 6 implementiamo esattamente questi 5 fattori.


# TODO 4.1 (8 minuti):
# Implementa h(x) = sin(x^2) e verifica numericamente che la sua
# derivata in x = 1.0 vale: cos(1^2) * 2*1 = 2 * cos(1) ~ 1.0806.
# Usa derivata_numerica(...) sulla funzione composta direttamente.
# Stampa il risultato e fai assert |num - analitica| < 1e-4.
# TUO CODICE QUI:


# TODO 4.2 (5 minuti):
# Spiega in 3-4 righe con tue parole (no copia-incolla del file): perche'
# la chain rule e' "il cuore" del backprop? Cosa succederebbe se non
# avessimo questa regola?
# TUA RISPOSTA:
# ...


# ==========================================================================
# SEZIONE 5 - GRADIENT DESCENT E LEARNING RATE
# ==========================================================================

# ---------------------- ANALOGIA --------------------------------------------
# Sei in cima a una collina con la nebbia. Vuoi raggiungere il fondovalle.
# Non vedi nulla, ma sotto i piedi senti la pendenza. Allora:
#   - fai un passo nella direzione di MAGGIOR DISCESA
#   - controlli di nuovo la pendenza
#   - ripeti
#
# Questa procedura iterativa si chiama GRADIENT DESCENT (discesa del
# gradiente). La direzione di maggior discesa = -grad. La "lunghezza
# del passo" e' il LEARNING RATE (lr).
#
# Tre scenari:
#   - lr troppo PICCOLO: passetti minuscoli, ci metti l'eta'
#   - lr troppo GRANDE:  passi tanto che salti dall'altra parte della
#                        valle, oscilli, non arrivi mai
#   - lr "giusto":       discendi in tempo ragionevole
#
# Per il web dev: e' come la "step size" in una migrazione di database.
# Troppo piccolo -> migrazione lentissima. Troppo grande -> failure su
# tabelle troppo grandi. Si trova per tentativi.

# ---------------------- TEORIA + CODICE -------------------------------------
# 5.1 - GRADIENT DESCENT SU UNA FUNZIONE SEMPLICE


def gradient_descent(
    grad_f: Callable[[NDArray[np.float64]], NDArray[np.float64]],
    x0: NDArray[np.float64],
    lr: float = 0.1,
    n_iter: int = 100,
) -> tuple[NDArray[np.float64], list[NDArray[np.float64]]]:
    """Gradient descent generico.

    Args:
        grad_f: funzione che data x ritorna il gradiente di f in x.
        x0:     punto iniziale.
        lr:     learning rate (lunghezza del passo).
        n_iter: numero di iterazioni.

    Returns:
        (x_finale, lista_punti)
    """
    x = x0.astype(float).copy()
    traiettoria = [x.copy()]
    for _ in range(n_iter):
        g = grad_f(x)
        x = x - lr * g
        traiettoria.append(x.copy())
    return x, traiettoria


def _esempio_gd_paraboloide() -> None:
    """Discesa su f(x, y) = x^2 + y^2 (minimo in (0, 0))."""
    grad_f = lambda v: 2 * v
    x0 = np.array([3.0, 4.0])
    x_finale, traiet = gradient_descent(grad_f, x0, lr=0.1, n_iter=50)
    print(f"x0 = {x0}, f(x0) = {float(np.sum(x0 ** 2)):.4f}")
    print(f"x_finale = {x_finale}, f(x_finale) = {float(np.sum(x_finale ** 2)):.6f}")
    print(f"Convergenza verso (0, 0): SI'.")


# 5.2 - EFFETTO DEL LEARNING RATE


def _grafico_gd_lr(
    out_path: str | None = None,
    show: bool = False,
) -> None:
    """Plot del gradient descent su paraboloide con 3 lr diversi."""
    grad_f = lambda v: 2 * v
    x0 = np.array([3.0, 4.0])
    lrs = [0.01, 0.3, 0.99]
    colori = ["#1f77b4", "#2ca02c", "#d62728"]

    fig, ax = plt.subplots(figsize=(8, 8))
    # Contour della funzione
    x = np.linspace(-5, 5, 100)
    y = np.linspace(-5, 5, 100)
    X, Y = np.meshgrid(x, y)
    F = X ** 2 + Y ** 2
    ax.contour(X, Y, F, levels=10, colors="gray", linewidths=0.5, alpha=0.5)

    for lr, col in zip(lrs, colori):
        _, traiet = gradient_descent(grad_f, x0, lr=lr, n_iter=50)
        T = np.array(traiet)
        ax.plot(T[:, 0], T[:, 1], "-o", color=col, markersize=4,
                label=f"lr = {lr}")
    ax.plot(0, 0, "*", color="#9467bd", markersize=18, label="minimo")
    ax.set_title("Gradient descent: effetto del learning rate")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.legend()
    ax.set_aspect("equal")
    ax.grid(True, alpha=0.3)
    if out_path:
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        fig.savefig(out_path, dpi=120, bbox_inches="tight")
    if show:
        plt.show()
    plt.close(fig)


# 5.3 - CURVA DI LOSS NEL TEMPO
#
# Quando addestri una rete, plotti SEMPRE la loss in funzione delle
# iterazioni. Quello che vedi ti dice se l'apprendimento sta funzionando:
#   - loss che cala monotona       -> training sano
#   - loss che oscilla forte       -> lr troppo grande
#   - loss che cala lentissimo     -> lr troppo piccolo
#   - loss che cala e poi sale     -> overfitting (M3 cap.04+)


# TODO 5.1 (10 minuti):
# Applica gradient_descent alla funzione f(x) = (x - 4)^2 (minimo in x=4):
#   - grad_f = lambda x: 2 * (x - 4)
#   - x0 = np.array([0.0])
#   - prova 3 lr: 0.01, 0.5, 1.1
# Per ogni lr, stampa x_finale dopo 50 iterazioni. Cosa succede a lr=1.1?
# (suggerimento: aspettati esplosione)
# TUO CODICE QUI:


# TODO 5.2 (5 minuti):
# Genera il grafico del gradient descent con 3 lr (gia' fornito) e
# salvalo in modulo_03_dl_cv/figures/03_04_gd_lr.png. Verifica esistenza.
# TUO CODICE QUI:


# TODO 5.3 (8 minuti):
# Riproduci il gradient descent su f(x, y) = x^2 + y^2 ma stampando
# anche la traiettoria della LOSS in funzione delle iterazioni:
#   - lr = 0.1, n_iter = 30
#   - per ogni step, calcola loss = float(np.sum(x_corrente ** 2))
#   - alla fine plotta loss vs iter e salva in
#       modulo_03_dl_cv/figures/03_05_loss_curve.png
# Cosa noti? La loss cala monotona, oscilla, o si stabilizza prima della
# fine?
# TUO CODICE QUI:


# ==========================================================================
# SEZIONE 6 - BACKPROP E TRAINING SU RETE 2-LAYER
# ==========================================================================
#
# Adesso tutti i pezzi: chain rule (Sez.4) + gradient descent (Sez.5)
# applicati alla rete 2-layer di cap.02 M3.

# ---------------------- TEORIA + CODICE -------------------------------------
# 6.1 - FORWARD CON CACHE
#
# Per il backward ci servono le attivazioni intermedie (Z1, H, Z2, P)
# che abbiamo calcolato nel forward. Le salviamo in un dict "cache".


def forward_2layer(
    X: NDArray[np.float64],
    W1: NDArray[np.float64],
    b1: NDArray[np.float64],
    W2: NDArray[np.float64],
    b2: NDArray[np.float64],
) -> tuple[NDArray[np.float64], dict[str, NDArray[np.float64]]]:
    """Forward 2-layer con cache delle attivazioni intermedie.

    Returns:
        (P, cache) dove P shape (N,) e cache contiene Z1, H, Z2, P.
    """
    Z1 = X @ W1 + b1                       # (N, h)
    H = relu(Z1)                            # (N, h)
    Z2 = H @ W2 + b2                        # (N, 1)
    P = sigmoid(Z2).ravel()                 # (N,)
    cache = {"X": X, "Z1": Z1, "H": H, "Z2": Z2, "P": P}
    return np.asarray(P, dtype=float), cache


# 6.2 - BACKWARD: chain rule applicata
#
# Forward (rinominato per chiarezza, gli operatori sono gli stessi):
#       Z1 = X @ W1 + b1
#       H  = ReLU(Z1)
#       Z2 = H @ W2 + b2
#       P  = sigmoid(Z2)
#       L  = BCE(P, y)
#
# Backward (chain rule, calcolata "a ritroso"):
#
#   dL/dZ2  =  P - y                                                  shape (N, 1)
#       (semplificazione miracolosa BCE+sigmoid: d(BCE+sigmoid)/dZ2 = P - y)
#
#   dL/dW2  =  H.T @ dL/dZ2 / N                                       shape (h, 1)
#   dL/db2  =  somma su N di dL/dZ2 / N                                shape (1,)
#
#   dL/dH   =  dL/dZ2 @ W2.T                                           shape (N, h)
#   dL/dZ1  =  dL/dH * derivata_relu(Z1)                              shape (N, h)
#       (la derivata di ReLU "spegne" i contributi dove Z1 <= 0)
#
#   dL/dW1  =  X.T @ dL/dZ1 / N                                        shape (d, h)
#   dL/db1  =  somma su N di dL/dZ1 / N                                shape (h,)


def backward_2layer(
    y: NDArray[np.int64] | NDArray[np.float64],
    W2: NDArray[np.float64],
    cache: dict[str, NDArray[np.float64]],
) -> dict[str, NDArray[np.float64]]:
    """Backward 2-layer. Restituisce {dW1, db1, dW2, db2}.

    Tutto vettorizzato, niente loop su pratiche. Le derivate sono
    derivate da chain rule (vedi commenti sopra).
    """
    X = cache["X"]
    Z1 = cache["Z1"]
    H = cache["H"]
    P = cache["P"]
    N = X.shape[0]

    # dL/dZ2: shape (N, 1)
    dZ2 = (P - y).reshape(-1, 1)

    # dL/dW2, dL/db2
    dW2 = (H.T @ dZ2) / N                       # (h, 1)
    db2 = dZ2.sum(axis=0) / N                    # (1,)

    # propaga indietro: dL/dH e poi dL/dZ1
    dH = dZ2 @ W2.T                              # (N, h)
    dZ1 = dH * derivata_relu(Z1)                 # (N, h)

    # dL/dW1, dL/db1
    dW1 = (X.T @ dZ1) / N                        # (d, h)
    db1 = dZ1.sum(axis=0) / N                    # (h,)

    return {"dW1": dW1, "db1": db1, "dW2": dW2, "db2": db2}


# 6.3 - TRAINING LOOP COMPLETO


def train_rete_2_layer(
    X: NDArray[np.float64],
    y: NDArray[np.int64],
    h: int = 16,
    lr: float = 0.1,
    n_iter: int = 1000,
    seed: int = 42,
    verbose: bool = True,
) -> tuple[dict[str, NDArray[np.float64]], list[float]]:
    """Allena una rete 2-layer con full-batch gradient descent.

    Returns:
        (parametri, loss_history) dove
          parametri = {"W1", "b1", "W2", "b2"}
          loss_history = lista di N_iter valori BCE
    """
    rng = np.random.default_rng(seed)
    d = X.shape[1]
    # init He (Sez.2 cap.02 M3)
    W1 = rng.standard_normal((d, h)) * np.sqrt(2.0 / d)
    b1 = np.zeros(h)
    W2 = rng.standard_normal((h, 1)) * np.sqrt(2.0 / h)
    b2 = np.zeros(1)

    losses: list[float] = []
    for i in range(n_iter):
        # FORWARD
        P, cache = forward_2layer(X, W1, b1, W2, b2)
        # LOSS
        loss = bce_loss(P, y.astype(float))
        losses.append(loss)
        # BACKWARD
        grads = backward_2layer(y.astype(float), W2, cache)
        # UPDATE
        W1 = W1 - lr * grads["dW1"]
        b1 = b1 - lr * grads["db1"]
        W2 = W2 - lr * grads["dW2"]
        b2 = b2 - lr * grads["db2"]

        if verbose and (i % max(1, n_iter // 10) == 0 or i == n_iter - 1):
            acc = float(np.mean((P >= 0.5).astype(int) == y))
            print(f"iter {i:4d}  loss={loss:.4f}  acc={acc:.3f}")

    return {"W1": W1, "b1": b1, "W2": W2, "b2": b2}, losses


def _esempio_training_2layer() -> None:
    """Demo: training su dataset sintetico XOR (non risolvibile da LR)."""
    rng = np.random.default_rng(0)
    # 2 feature, 200 pratiche, label XOR
    X = rng.uniform(-1, 1, size=(200, 2))
    y = ((X[:, 0] > 0) ^ (X[:, 1] > 0)).astype(int)   # XOR
    params, losses = train_rete_2_layer(X, y, h=16, lr=0.5, n_iter=2000,
                                         seed=0, verbose=False)
    P, _ = forward_2layer(X, params["W1"], params["b1"],
                          params["W2"], params["b2"])
    acc = float(np.mean((P >= 0.5).astype(int) == y))
    print(f"Training XOR (problema NON linearmente separabile)")
    print(f"loss iniziale = {losses[0]:.4f}, finale = {losses[-1]:.4f}")
    print(f"accuracy finale = {acc:.3f}  (LogisticRegression farebbe ~0.5)")


def _grafico_loss_training(
    losses: list[float],
    out_path: str | None = None,
    show: bool = False,
) -> None:
    """Plot della loss in funzione delle iterazioni."""
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(range(len(losses)), losses, color="#1f77b4")
    ax.set_xlabel("iterazione")
    ax.set_ylabel("BCE loss (media batch)")
    ax.set_title("Training loop: la loss cala col tempo")
    ax.grid(True, alpha=0.3)
    if out_path:
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        fig.savefig(out_path, dpi=120, bbox_inches="tight")
    if show:
        plt.show()
    plt.close(fig)


# TODO 6.1 (10 minuti):
# Verifica empirica della backward: il gradiente analitico calcolato a
# mano deve coincidere con quello numerico (controllo cardine).
#   - X (5, 3) random, y (5,) random 0/1
#   - W1 (3, 4) random, b1 (4,) zero, W2 (4, 1) random, b2 (1,) zero
#   - FORWARD: P, cache
#   - BACKWARD: grads
#   - GRADIENTE NUMERICO di dW1[0, 0]: pre-h, post-h, differenza centrata
#     (suggerimento: definisci una funzione f(W1) che ritorna la BCE,
#     poi chiama gradiente_numerico solo sulla cella W1[0, 0])
#   - confronta i due valori: |analitico - numerico| < 1e-4
# TUO CODICE QUI:


# TODO 6.2 (15 minuti):
# Riproduci _esempio_training_2layer() su XOR ma:
#   - varia lr in [0.05, 0.5, 5.0]
#   - per ogni lr, stampa loss finale e accuracy finale
#   - quale lr funziona meglio? Quale "esplode"?
#   - salva il grafico delle 3 loss curve sovrapposte in
#       modulo_03_dl_cv/figures/03_06_lr_compare.png
# TUO CODICE QUI:


# TODO 6.3 (8 minuti):
# La rete addestrata su XOR raggiunge accuracy ~ 1.0. La
# LogisticRegression su XOR non puo' superare ~ 0.5 (XOR e' il classico
# esempio NON linearmente separabile). Verifica empiricamente:
#   - allena LogisticRegression(max_iter=1000) su (X, y) di XOR
#   - stampa accuracy_score(y, clf.predict(X))
# In commento, spiega perche' XOR e' "il muro" che la LogisticRegression
# non puo' superare e perche' la rete con ReLU si'.
# TUO CODICE QUI:


# ==========================================================================
# QUIZ DI VERIFICA (fai PRIMA di passare agli esercizi)
# ==========================================================================

# V1) Cos'e' una LOSS in 1 riga? Perche' la BCE invece dell'MSE per
#     classificazione binaria (2 motivi, anche solo intuitivi)?
# TUA RISPOSTA:
# ...

# V2) La derivata di f(x) = x^2 in x = -5 e': (a) 25  (b) -10  (c) +10  (d) 0
#     Spiega geometricamente (parla di pendenza, non di formule).
# TUA RISPOSTA:
# ...

# V3) Il gradiente di f(x, y) = x^2 + y^2 nel punto (1, -2) e':
#     (a) [2, -4]   (b) [-2, 4]   (c) [2, 4]   (d) [1, 2]
#     E in che direzione vai per MINIMIZZARE f?
# TUA RISPOSTA:
# ...

# V4) [Chain rule] h(x) = e^(2x). La derivata in x = 0 vale: (a) 1  (b) 2  (c) e^0=1
#     Suggerimento: scriverla come composizione f(g(x)) e applicare chain rule.
# TUA RISPOSTA:
# ...

# V5) [Trova l'errore]
#       lr = 100.0
#       params, losses = train_rete_2_layer(X, y, lr=lr, n_iter=1000)
#     Cosa vedi nelle losses? (a) calo monotono  (b) NaN/Inf  (c) oscillazione
#     selvaggia  (d) costante. Perche'?
# TUA RISPOSTA:
# ...

# V6) Nel backward 2-layer, dW1 ha la stessa shape di:
#     (a) X    (b) H    (c) W1   (d) Z1
#     Perche'? (regola B7)
# TUA RISPOSTA:
# ...

# V7) [Recap shapes - bug killer] X (N=50, d=4), W1 (4, 8), W2 (8, 1).
#     Che shape ha dZ1? E dW1?
# TUA RISPOSTA:
# ...

# V8) [Feynman - vincoli stretti] Spiega in 5 righe a un collega web dev
#     cos'e' la BACKPROPAGATION. VIETATO: derivata, gradiente, chain rule,
#     loss, layer, neurone, peso.
# TUA RISPOSTA:
# ...


# ==========================================================================
# ESERCIZI FINALI
# ==========================================================================

# E1) [COLLOQUIO] - 20 minuti (capitolo difficile)
#     "Spiega in modo strutturato cos'e' la BACKPROPAGATION. Struttura:
#       (1) PROBLEMA che risolve (perche' la inventarono)
#       (2) INTUIZIONE (chain rule applicata a una rete)
#       (3) RICETTA OPERATIVA in 4 step (forward, loss, backward, update)
#       (4) CONNESSIONE con gradient descent
#       (5) POTENZIALI PROBLEMI in produzione (vanishing gradient,
#           exploding gradient, learning rate sbagliato)"
#     Massimo 15 righe in totale, niente codice. Si valuta CHIAREZZA, non
#     formule.
# TUA RISPOSTA:
# ...


# E2) [REFACTORING] - 15 minuti
#     Questo codice gira ma e' brutto:
#       - pattern #25: "np.array" come type hint
#       - pattern #23: virgola spuria su return
#       - pattern #21: round con virgola finale
#       - bug logico: divide per "len(losses)" invece di "len(X)" nel
#         calcolo della loss media (perche' usa una loss BCE per pratica
#         accumulata in una lista e poi divide per la lunghezza della
#         lista di losses, non per N)
#
#     def addestra_brutto(X: np.array, y, lr=0.01, n=1000):
#         losses = []
#         W1 = np.random.randn(X.shape[1], 8)
#         b1 = np.zeros(8)
#         W2 = np.random.randn(8, 1)
#         b2 = np.zeros(1)
#         for i in range(n):
#             P, cache = forward_2layer(X, W1, b1, W2, b2)
#             tot = 0
#             for j in range(len(P)):
#                 if y[j] == 1:
#                     tot += - np.log(P[j] + 1e-12)
#                 else:
#                     tot += - np.log(1 - P[j] + 1e-12)
#             loss = tot / len(losses)  # bug
#             losses.append(round(loss, 4),)
#             g = backward_2layer(y.astype(float), W2, cache)
#             W1 -= lr * g["dW1"]; b1 -= lr * g["db1"]
#             W2 -= lr * g["dW2"]; b2 -= lr * g["db2"]
#         return (W1, b1, W2, b2), losses,
#
#     Riscrivilo:
#       - type hint corretti (NDArray[np.float64])
#       - vettorizzato (bce_loss invece del loop)
#       - bug della divisione corretto
#       - niente virgole spurie
# TUO CODICE QUI:


# E3) [DEBUG] - autonomo, niente scala progressiva
#     Questo codice gira ma la loss NON cala mai: resta costante. Trova
#     il bug PRIMA di chiedere aiuto.
#
#       params, losses = train_rete_2_layer(X, y, lr=0.0, n_iter=100,
#                                            seed=0, verbose=False)
#       print(losses[0], losses[-1])    # uguali
#
#     Quando hai trovato il bug, scrivi qui sotto:
#       - cosa hai diagnosticato (1 riga)
#       - come l'hai sistemato (1 riga di codice corretto)
# TUA RISPOSTA / FIX:
# ...


# E4) [RETRIEVAL] - regola 15: riscrivi da zero una funzione di un capitolo
#                    PRECEDENTE, senza guardare il file vecchio.
#     Senza riaprire `modulo_03_dl_cv/02_reti_neurali.py`, riscrivi da
#     zero la funzione "rete_2_layer(X, W1, b1, W2, b2)" del cap.02 M3.
#     Deve:
#       - shape check (X 2D, W1 W2 2D, dimensioni coerenti)
#       - usare la TUA sigmoid e la TUA relu (gia' importate)
#       - NON usare cache (qui non serve, e' per il forward "production")
#       - type hint con NDArray[np.float64]
#       - ritornare (H, P) con P 1D
#
#     Verifica:
#       rete_2_layer(X(3,4), W1(4,8), b1(8,), W2(8,1), b2(1,)) -> H(3,8), P(3,)
# TUO CODICE QUI:


# E5) [INTERLEAVING] cap.01 M3 (sigmoid stabile) + cap.03 M3 (training)
#     Addestra una rete 2-layer su un dataset sintetico con FEATURE
#     SU SCALE DIVERSE:
#       - feature 1 in [-1, +1]
#       - feature 2 in [-1000, +1000]
#       - y = XOR delle 2 feature (semplificato: y = (f1 > 0) ^ (f2 > 0))
#     Allena PRIMA senza scalare, POI con StandardScaler.
#     Mostra accuracy + loss finale nei due casi.
#     Spiega in 2 righe perche' senza scaling il training "soffre"
#     (sugg.: i logit della feature 2 saturano la sigmoid -> derivata ~0
#     -> niente apprendimento).
# TUO CODICE QUI:


# E6) [REAL-WORLD] - regola M5 ma utile gia' qui (scenario vago)
#     Scenario: il broker dice "ho addestrato la rete su un dataset di
#     2024. Adesso siamo nel 2026 e le predizioni in produzione sono
#     peggiorate. Cosa e' successo e cosa proponi?"
#     Rispondi in 3 punti:
#       (a) il NOME del problema (suggerimento: inizia con "drift...")
#       (b) come lo verificheresti senza addestrare nulla di nuovo
#       (c) 2 alternative concrete per affrontarlo (re-training, monitoring,
#           drift detection, A/B test, ecc.)
#     Massimo 8 righe.
# TUA RISPOSTA:
# ...


# E7) [REGOLA 16 - CONFRONTO PRIMA/DOPO] - 15 minuti
#     Questa NON e' l'ultimo capitolo del modulo (la regola si applica
#     all'ULTIMO capitolo, cap.07 M3), pero' qui chiudiamo il "primo
#     blocco" (cap.01-02-03 = full-NumPy). Esercizio:
#       (a) ricarica mentalmente il cap.01 M3 (1 neurone scritto a mano)
#       (b) ora rileggi il train_rete_2_layer di questo capitolo
#       (c) scrivi in 5 righe la differenza CONCETTUALE fra "neurone manuale
#           col forward" (cap.01) e "rete che impara da sola" (cap.03).
#       (d) elenca i 3 CONCETTI NUOVI di questo capitolo che 3 capitoli fa
#           non sapevi.
# TUA RISPOSTA:
# ...


# ==========================================================================
# MINI-PROGETTO - "train_rete_su_csv_m2"
# ==========================================================================
#
# OBIETTIVO: addestrare la rete 2-layer del cap.02 M3 sul CSV M2 e
# confrontarla con LogisticRegression (M2 cap.04). Sul nostro dataset
# (semplice, separabile) la rete dovrebbe pareggiare o battere LR di poco.
# Su dataset piu' complessi la differenza sarebbe netta.
#
# Firma:
#     def train_rete_su_csv_m2(
#         h: int = 16,
#         lr: float = 0.1,
#         n_iter: int = 2000,
#         seed: int = 42,
#     ) -> dict[str, float]:
#         """
#         Ritorna un dict con:
#             'loss_iniziale'   : BCE al primo step (rete random)
#             'loss_finale'     : BCE all'ultimo step
#             'acc_rete'        : accuracy della rete addestrata
#             'acc_logreg'      : accuracy di LogisticRegression baseline
#             'auc_rete'        : roc_auc della rete addestrata
#             'auc_logreg'      : roc_auc di LogisticRegression baseline
#         """
#
# Vincoli OBBLIGATORI:
#   - usa StandardScaler.fit_transform per scalare X
#   - usa train_rete_2_layer per addestrare la rete sui dati scalati
#   - allena LogisticRegression(max_iter=1000, random_state=42) come baseline
#   - salva il grafico della loss in
#         modulo_03_dl_cv/figures/03_07_train_csv_m2.png
#   - alla fine, stampa il dict in modo leggibile
#
# Verifica attesa:
#   - loss_iniziale > 0.6   (rete random)
#   - loss_finale < 0.3     (rete addestrata)
#   - acc_rete > 0.85
#   - acc_logreg > 0.85     (paragonabile, dataset semplice)
#   - auc_rete > 0.9
#   - auc_logreg > 0.9
#
# TUO CODICE QUI:


# ==========================================================================
# CHECKPOINT FINALE (auto-verifica)
# ==========================================================================

# C1) In 1 frase: cos'e' la LOSS e perche' minimizziamo lei e non
#     l'accuracy?
# TUA RISPOSTA:
# ...

# C2) Hai f(x) = 3x + 1. La sua derivata vale ovunque: (a) 0  (b) 3  (c) x  (d) 3x
#     E intuitivamente: cosa significa "pendenza costante = 3"?
# TUA RISPOSTA:
# ...

# C3) [Feynman - vincoli stretti] Spiega in 3 righe il GRADIENT DESCENT
#     a un collega web dev. VIETATO: derivata, gradiente, loss, peso,
#     ottimizzazione, minimo.
# TUA RISPOSTA:
# ...

# C4) [Recap shapes] Rete 2-layer con X (100, 5), W1 (5, 10), W2 (10, 1).
#     Che shape hanno dZ2, dW2, db2, dZ1, dW1, db1 ?
# TUA RISPOSTA:
# ...

# C5) Auto-rating onesto (compila in chiusura capitolo):
#       - BCE vs MSE e perche':                   /10
#       - derivata come pendenza:                 /10
#       - gradiente come vettore di derivate:     /10
#       - chain rule:                              /10
#       - backprop su rete 2-layer:                /10
#       - effetto del learning rate:               /10
# TUE RISPOSTE:
# ...


# ==========================================================================
# SOLUZIONI QUIZ (NON BARARE - leggi solo dopo aver risposto)
# ==========================================================================
"""
QUIZ D'INGRESSO

Q1) LOSS: numero che misura quanto la rete sbaglia, su scala continua e
    DERIVABILE. ACCURACY: percentuale di predizioni corrette, discreta.
    La differenza importante per il backprop e' che la loss e' derivabile
    (puoi calcolarne il gradiente rispetto ai pesi), l'accuracy no.

Q2) In x = 3 la curva x^2 e' in salita (pendenza positiva). In x = -3
    e' in discesa (pendenza negativa). Geometricamente: la parabola
    "scende fino allo zero e poi risale", quindi a sinistra dello zero
    la pendenza e' negativa, a destra positiva. La derivata di x^2 e' 2x.

Q3) Errore intuitivo: la rete ha previsto "quasi sicuro genuino" (0.05)
    quando in realta' era alterato. Errore grande. Per migliorare devi
    spingere i pesi in modo da FAR ALZARE p sulla pratica simile a
    questa. Cioe' i pesi delle feature "in salita" verso alterato vanno
    aumentati, quelli in discesa vanno diminuiti.

Q4) W1: 4 * 8 = 32. b1: 8. W2: 8 * 1 = 8. b2: 1. Totale 32+8+8+1 = 49.

Q5) (Feynman, tipo):
    "Hai un modello di previsione meteo. Lo provi su 1000 giorni del
    passato e vedi quante volte ha azzeccato. Ogni volta che sbaglia,
    aggiusti un po' le manopole interne del modello in modo da ridurre
    gli errori. Poi rifai il giro su tutti i 1000 giorni. Dopo molti
    giri, il modello sbaglia sempre meno: ha 'imparato'."


QUIZ DI VERIFICA

V1) Loss: numero continuo che misura quanto le predizioni si discostano
    dalla verita'. BCE invece dell'MSE perche':
    (1) la BCE punisce in modo "infinito" gli errori clamorosi (sicurezza
        sbagliata) -> spinge la rete a NON essere "sicurissima ma errata".
    (2) la derivata di BCE + sigmoid si semplifica in (p - y), facile e
        stabile da calcolare.

V2) (b) -10. La derivata di x^2 e' 2x; in x = -5 vale -10. Geometricamente:
    a sinistra dello zero la parabola scende, pendenza negativa.

V3) (a) [2, -4]. Il gradiente di x^2 + y^2 e' [2x, 2y], quindi in (1, -2)
    vale [2, -4]. Per minimizzare vai nella direzione opposta: [-2, +4]
    (cioe' x diminuisce, y aumenta).

V4) (b) 2. h(x) = e^(2x) = f(g(x)) con f(u) = e^u (f'(u)=e^u) e g(x) = 2x
    (g'(x) = 2). Chain rule: h'(x) = e^(2x) * 2. In x = 0: e^0 * 2 = 2.

V5) (b) o (c). Con lr enorme, la rete "salta" oltre il minimo a ogni step
    e i pesi esplodono. Nei casi peggiori si arriva a NaN/Inf perche'
    i logit diventano enormi e sigmoid/log producono valori non finiti.

V6) (c) W1. Regola B7: ogni gradiente ha la STESSA shape del parametro
    rispetto a cui e' calcolato. dW1 e' "di quanto cambiare ogni cella
    di W1", quindi shape identica.

V7) dZ1: (50, 8) - una derivata per ogni Z1[i, j].
    dW1: (4, 8) - stessa shape di W1.

V8) (Feynman, tipo):
    "Immagina di costruire una pizza in catena di montaggio. 4 cuochi
    in fila preparano un pezzo ciascuno (impasto, salsa, formaggio,
    cottura). Esce dal forno e il cliente dice 'troppo salata'. Tu
    devi capire CHI deve aggiustare cosa: forse il salsa-cuoco ne ha
    messa troppa, o forse era il formaggio-cuoco. Cammini all'indietro
    nella catena chiedendo 'quanto ha contribuito ognuno a questo
    eccesso di sale?' e gli dai indicazioni per la prossima pizza."


CHECKPOINT FINALE

C1) Loss = misura continua e derivabile di quanto la rete sbaglia. La
    minimizziamo perche' e' derivabile -> possiamo calcolarne il
    gradiente rispetto ai pesi e usarlo per aggiornare. L'accuracy non
    e' derivabile (e' a scalini), quindi inutilizzabile per backprop.

C2) (b) 3. Pendenza costante = 3 vuol dire che la funzione SALE di 3
    unita' verticali per ogni unita' di x. E' una retta inclinata in su.
    La derivata di "ax + b" e' SEMPRE "a" (la b non conta perche'
    sposta la retta in su/giu', non ne cambia la pendenza).

C3) (Feynman tipo): "Immagina di essere bendato su una collina nella
    nebbia. Vuoi andare al fondovalle ma non vedi nulla. Senti la
    pendenza sotto i piedi: dove e' piu' ripido all'ingiu', li' fai un
    passo. Poi controlli di nuovo. Continui finche' senti che siamo
    in pianura: sei al fondovalle."

C4) dZ2: (100, 1). dW2: (10, 1). db2: (1,). dZ1: (100, 10).
    dW1: (5, 10). db1: (10,). Tutte coerenti con la regola B7
    (gradiente = stessa shape del parametro/output).
"""


# ==========================================================================
# ENTRY POINT (esegui solo le demo che esistono nel file, niente di tuo)
# ==========================================================================
if __name__ == "__main__":
    print("=" * 70)
    print("Cap.03 M3 - demo di riferimento")
    print("=" * 70)

    print("\n[Demo Sez.1 - BCE vs MSE su predizioni con y=1]")
    _confronto_bce_mse()

    print("\n[Demo Sez.2 - derivata di x^2]")
    _esempio_derivata()

    print("\n[Demo Sez.3 - gradiente di x^2 + y^2 in (3, 4)]")
    _esempio_gradiente()

    print("\n[Demo Sez.4 - chain rule su (3x+1)^2 in x=2]")
    _esempio_chain_rule()

    print("\n[Demo Sez.5 - gradient descent su paraboloide]")
    _esempio_gd_paraboloide()

    print("\n[Demo Sez.6 - training su XOR (problema NON lineare)]")
    _esempio_training_2layer()

    print("\n[Genero infografiche PNG nella cartella figures/]")
    figures_dir = os.path.join(os.path.dirname(__file__), "figures")
    _grafico_bce(out_path=os.path.join(figures_dir, "03_01_bce_loss.png"))
    _grafico_funzione_e_derivata(
        out_path=os.path.join(figures_dir, "03_02_derivata.png"))
    _grafico_gradiente(out_path=os.path.join(figures_dir, "03_03_gradiente.png"))
    _grafico_gd_lr(out_path=os.path.join(figures_dir, "03_04_gd_lr.png"))
    print(f"  -> {figures_dir}/03_01_bce_loss.png")
    print(f"  -> {figures_dir}/03_02_derivata.png")
    print(f"  -> {figures_dir}/03_03_gradiente.png")
    print(f"  -> {figures_dir}/03_04_gd_lr.png")

    print("\n" + "=" * 70)
    print("Demo finite. Adesso tocca a te: completa i TODO in ordine.")
    print("Capitolo difficile - vai LENTO. Quando vuoi una valutazione:")
    print("  'valuta cap.03 M3 sezione X.Y'.")
    print("=" * 70)
