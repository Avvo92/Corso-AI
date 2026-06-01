"""
============================================================================
MODULO 3 (DL & CV) - CAPITOLO 03
"LOSS": come misuriamo l'errore della rete (BCE vs MSE)
============================================================================

Primo dei 4 sotto-capitoli del vecchio "Backpropagation" (split 27/05/2026).
Mappa nuova del modulo:

    03_loss.py                  ← QUESTO FILE (loss, BCE, MSE)
    04_derivate_gradiente.py    (derivata, gradiente)
    05_chain_rule_gd.py         (chain rule + gradient descent)
    06_backprop_training.py     (backward 2-layer + training loop)

Filosofia di questo capitolo (richiesta studente 27/05/2026):
    "Tanti esercizi pratici, pipeline complete, richiami ai capitoli
    precedenti del modulo. Alla fine devo essere maestro della backprop."

Qui ti FOCALIZZI sulla LOSS, ma ogni esercizio ti obbliga a riscrivere
forward / sigmoid / ReLU / metriche del cap.01-02 M3 (richiami forti
intra-modulo, non monopolio dei moduli precedenti).

----------------------------------------------------------------------------
DA DOVE ARRIVI (cap.02 M3)
----------------------------------------------------------------------------
Nel cap.02 M3 hai costruito la rete 2-layer in NumPy puro:

    H = ReLU(X @ W1 + b1)        # hidden     shape (N, h)
    P = sigmoid(H @ W2 + b2)     # output     shape (N, 1) -> (N,)

Con pesi RANDOM accuracy ~ 0.5. Per addestrarla servono 4 pezzi:
    (1) MISURA dell'errore                  -> QUESTO CAPITOLO
    (2) DIREZIONE di correzione             -> cap.04 (derivate, gradiente)
    (3) ALGORITMO di correzione             -> cap.05 (chain rule + GD)
    (4) TUTTO insieme sulla rete            -> cap.06 (backprop + training)

----------------------------------------------------------------------------
DEFINITION OF DONE (cap.03 LOSS)
----------------------------------------------------------------------------
Alla fine sai rispondere "in 1 riga" e in CODICE a queste 5 domande:

  1) Cos'e' una LOSS e perche' e' diversa dall'ACCURACY?       -> Sez. 1
  2) Cos'e' la BCE come FORMULA?                                -> Sez. 1
  3) Perche' BCE invece di MSE per classificazione binaria?     -> Sez. 2
  4) Cosa fa il `clip` BILATERALE nella BCE?                    -> Sez. 1
  5) Come si calcola accuracy con soglia 0.5 in NumPy?           -> Sez. 3

Hai anche scritto/usato 4 funzioni riutilizzabili (le piazzo in alto, dopo
gli import, per averle disponibili a tutto il file):

  - bce_loss            (binary cross-entropy media su batch)
  - mse_loss            (mean squared error, per confronto)
  - accuracy_score      (accuracy con soglia)
  - sigmoid             (recall cap.01/02, in versione stabile)

E hai consolidato 3 anti-pattern emersi nel cap.02-03 monolitico:
  - segno meno della BCE
  - clip BILATERALE (eps, 1-eps), non solo (eps, 1)
  - soglia di accuracy 0.5, non > 0

----------------------------------------------------------------------------
MAPPA DEL CAPITOLO
----------------------------------------------------------------------------
   *  PRONTUARIO TRANELLI                       [L1] - [L5]
   *  QUIZ D'INGRESSO                           Q1 - Q5
   *  RINFORZO UAT (lacuna #31)                 1 micro-esercizio
   *  SEZIONE 1  BCE: la loss standard          1.1 - 1.4
                  con 4 mini-esercizi inline
   *  SEZIONE 2  BCE vs MSE: perche' BCE        2.1 - 2.2
                  con 3 mini-esercizi inline
   *  SEZIONE 3  ACCURACY + soglia 0.5          3.1 - 3.2
                  con 3 mini-esercizi inline
   *  ESERCIZI MIRATI (TODO 1.1 - 1.3)          (gia' fatti, migrati)
   *  RINFORZI CAP.01-02 M3 (TODO 4.x)          forward + sigmoid + relu
   *  RINFORZI LACUNE EMERSE (TODO 5.x)         segno BCE, clip, soglia
   *  PIPELINE INTEGRATA                        valuta_rete_random()
                  Forward (cap.02) + LOSS (cap.03) + metriche (M2)
   *  TIPOLOGIE STANDARD                        TODO 6-11
                  COLLOQUIO, REFACTORING, DEBUG, RETRIEVAL,
                  INTERLEAVING, REAL-WORLD
   *  QUIZ DI VERIFICA                          V1 - V7
   *  MINI-PROGETTO FINALE                      valuta_modello_completo()
                  P + y -> dict con bce, mse, acc, recall, prec, f1, auc
   *  CHECKPOINT FINALE                         C1 - C5
   *  SOLUZIONI                                 in fondo

Conta esercizi: ~12 mini-inline + 17 TODO numerati + 1 pipeline grande +
1 mini-progetto finale = ~30 occasioni di scrivere codice.

----------------------------------------------------------------------------
COME USARE QUESTO FILE
----------------------------------------------------------------------------
   1. Leggi in ORDINE. NON saltare i mini-esercizi inline (sono il sale).
   2. Per ogni TODO scrivi nel blocco "TUO CODICE" (non cancellare scaffold).
   3. Se ti blocchi >15 min: "sono bloccato sezione X" -> ti do un'IDEA.
   4. Quando vuoi una valutazione: "valuta cap.03 M3 sezione X.Y".
   5. Niente LaTeX (preferenza tua): formule in PAROLE + codice + grafico.
   6. Hardware: CPU + NumPy + Matplotlib.
   7. Quando hai chiuso TUTTO: "ho finito il cap.03 M3" -> correzione + voto.

----------------------------------------------------------------------------
PRIMA DI APRIRE QUESTO FILE - BRIDGE RIPASSO (~10 min)
----------------------------------------------------------------------------
Fai i 10 mini-esercizi di ripasso in:

    modulo_03_dl_cv/quiz_ripasso_tra_capitoli/
        M03_R02_after_C02_before_C03_reti_to_loss.md
"""

from math import nan
import os
from typing import Callable
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from numpy.typing import NDArray
from pprint import pprint
from sklearn.metrics import roc_auc_score


# ==========================================================================
# FUNZIONI RIUTILIZZABILI (le definisco qui in alto, le riusi in tutti i TODO)
# ==========================================================================

def sigmoid(z: NDArray[np.float64] | float) -> NDArray[np.float64] | float:
    """Sigmoid stabile (recall cap.01/02 M3). Input qualsiasi shape.

    Stabilita': clip a +-500 per evitare overflow di exp.
    """
    z_arr = np.asarray(z, dtype=float)
    z_safe = np.clip(z_arr, -500.0, 500.0)
    out = 1.0 / (1.0 + np.exp(-z_safe))
    if np.isscalar(z):
        return float(out)
    return out


def relu(z: NDArray[np.float64]) -> NDArray[np.float64]:
    """ReLU (recall cap.02 M3): max(0, z). Vettorizzato."""
    return np.maximum(0.0, z)


def bce_loss(
    p: NDArray[np.float64],
    y: NDArray[np.int64] | NDArray[np.float64],
    eps: float = 1e-12,
) -> float:
    """Binary cross-entropy media su un batch.

    Args:
        p:   probabilita' predette in (0, 1), shape (N,).
        y:   etichette 0/1, shape (N,).
        eps: per evitare log(0) (clip BILATERALE eps, 1-eps).

    Returns:
        loss media (scalare float >= 0). 0 = predizioni perfette.
    """
    p_safe = np.clip(p, eps, 1.0 - eps)
    loss = - y * np.log(p_safe) - (1.0 - y) * np.log(1.0 - p_safe)
    return float(np.mean(loss))


def mse_loss(
    p: NDArray[np.float64],
    y: NDArray[np.int64] | NDArray[np.float64],
) -> float:
    """Mean squared error medio su batch. Definito per confronto con BCE."""
    return float(np.mean((p - y) ** 2))


def accuracy_score(
    p: NDArray[np.float64],
    y: NDArray[np.int64] | NDArray[np.float64],
    soglia: float = 0.5,
) -> float:
    """Accuracy con soglia (default 0.5)."""
    y_pred = (p >= soglia).astype(int)
    return float(np.mean(y_pred == y))


# ==========================================================================
# PRONTUARIO TRANELLI LOSS - leggilo PRIMA di iniziare (5 minuti)
# ==========================================================================
#
# [L1] LOSS != ACCURACY.
#      Accuracy = "quante predizioni giuste in %". Discreta (0 o 1 per
#                  pratica, soglia di solito 0.5).
#      Loss    = "quanto sbagliamo, su scala continua, DERIVABILE".
#      Si addestra MINIMIZZANDO la loss. L'accuracy NON e' derivabile
#      (cap.06 - backprop), quindi inutile per training.
#
# [L2] BCE per classificazione binaria, NON l'MSE.
#      L'MSE punisce "poco" gli errori clamorosi (es. p=0.51 e y=1:
#      errore quadratico 0.24, "piccolo"). La BCE punisce in modo
#      INFINITO quando p -> 0 e y = 1 (sicurissima sbagliata).
#
# [L3] CLIP BILATERALE eps, 1-eps.
#      log(0) = -inf, log(1) = 0, ma 0 * log(0) = NaN in NumPy.
#      Devi tagliare p lontano da ENTRAMBE le estremita':
#          p_safe = np.clip(p, eps, 1 - eps)      eps = 1e-12
#      Se proteggi solo eps, 1 (lato basso) ti esplode quando y=0 e p=1:
#      log(1 - p) = log(0) = -inf.
#
# [L4] SOGLIA 0.5 per accuracy (NON 0).
#      P arriva da sigmoid -> P in (0, 1) -> P > 0 e' sempre True!
#      La predizione binaria si fa con P >= 0.5 (soglia neutra).
#      Altre soglie (es. 0.7) per privilegiare recall vs precision.
#
# [L5] DERIVABILE vs DERIVATA.
#      "Derivabile" significa che la funzione e' liscia, niente scalini.
#      Ti permette di chiedere "se sposto un peso di poco, cosa cambia?"
#      Vedremo cosa significa CONCRETAMENTE nel cap.04 e 05.


# ==========================================================================
# QUIZ D'INGRESSO - cerniera cap.02 M3 -> cap.03 M3 LOSS
# ==========================================================================

# Q1) Hai una rete 2-layer e la addestri. Cos'e' la LOSS (1 riga)?
#     E cos'e' l'ACCURACY (1 riga)? Qual e' la differenza importante per
#     la backpropagation?
# TUA RISPOSTA:
# La loss misura la distanza tra previsione e realtà. Avendo noi la risposta (si o no) a un quesito, e la percentuale di sicurezza fornita da un modello rispetto la sua previsione (sigmoide, percentuale di sicurezza rispetto la classe alterato), possiamo capire sia quando il modello risponde correttamente, sia quando sbaglia, la "gravità", ossia la convinzione della sua risposta, proprio grazie alla percentuale che descrive la sua sicurezza nel fornirla.
# l'accuracy descrive l'accuratezza in termini generali del modello (tp + tn / (tp + tn + fp + fn)).
# Per noi è importante avere informazioni qualitative degli errori, così da poter definire in maniera coerente una correzione tramite la backpropagation.

# Q2) Hai f(x) = x^2. La PENDENZA della curva in x = 3 e' positiva o
#     negativa? E in x = -3? Spiega "geometricamente" senza derivate.
#     Grafico didattico: py -3 modulo_03_dl_cv/plot_pendenza_parabola_q2.py
#     -> figures/03_02_pendenza_parabola_q2.png
# TUA RISPOSTA:
# in x = 3 ci troviamo in pendenza positiva, inteso che se ci spostiamo a destra (f(4))sull'asse delle x, la curva ha una andamente positivo (sale). Per x = -3 esattamente in contrario, ossia la curva tende a scendere spostandoci di valore verso destra (f(-2)).

# Q3) Una rete sbaglia molto su una pratica: previsione p = 0.05, verita'
#     y = 1. Qual e' l'errore "intuitivo" della rete? E in che direzione
#     dovresti spostare i pesi? (su o giu', cioe' aumentarli o diminuirli?)
# TUA RISPOSTA:
# La rete ha detto che la pratica era quasi sicuramente genuina. Evidentemente i suoi pesi sono troppo "leggeri", ossia vanno aumentati. Così, il prodotto matriciale produrra valori più grandi, e di conseguenza la sigmoide produrra alla fine del processo dei valori più vicini a 1.

# Q4) [Recall cap.02 M3] Hai una rete con W1 (4, 8) e W2 (8, 1). Quanti
#     PARAMETRI totali ha la rete? (W1, b1, W2, b2)
# TUA RISPOSTA:
# (4 * 8) + 8 + (8 * 1) + 1 => 49 pesi

# Q5) [Feynman - no jargon] Spiega in 4 righe a un collega web dev cos'e'
#     un "loop di training". Vietato: gradiente, derivata, loss, layer,
#     pesi, neurone.
# TUA RISPOSTA:
#  Si parte dalla fase in cui i dati vengono processati attraverso vari livelli di parametri che, trasformando questi dati, alla fine produce una probabilita'. In un contesto in cui le risposte possono essere solo 2 (binario), confrontiamo quella probabilità con la risposta reale (0 o 1), e capiamo quanto il modello ha prodotto una risposta lontana dalla risposta corretta. A quel punto, questo margine di errore viene proiettato all'indietro, andando a riflettersi su tutti i parametri del modello, e sulla base di quanto il singolo parametro ha contribuito a produrre quel margine di errore, viene aggiustato in una direzione particolare. Poi si ricomincia e si ripete questo processo, fino a minimizzare il margine d'errore.


# ==========================================================================
# 🔁 RINFORZO MIRATO - "UAT: esistenza VS come la trovi" (lacuna #31)
# ==========================================================================
#
# Nel cap.02 M3 hai imparato il teorema UAT: una rete 2-layer abbastanza
# grande PUO' approssimare quasi qualsiasi funzione. ESISTE. Ok. Ma con
# pesi RANDOM accuracy ~ 0.5 -> la rete giusta esiste, ma noi siamo finiti
# in un punto a caso dello spazio dei pesi.
#
# Analogia: UAT dice "c'e' una cima panoramica in questa montagna". Bene.
# Ma noi siamo in un bosco, di notte, senza mappa. Sapere che la cima
# esiste NON ci aiuta.
#
# I prossimi 4 capitoli sono la MAPPA + LA BUSSOLA:
#   - LOSS               = "quanto sei distante dalla cima" (cap.03, QUI)
#   - DERIVATA/GRADIENTE = "in che direzione devi camminare" (cap.04)
#   - GRADIENT DESCENT   = "fai un passetto in quella direzione" (cap.05)
#   - BACKPROPAGATION    = chain rule applicata su TUTTI i pesi (cap.06)
#
# Micro-esercizio (1 minuto, mentale):
# Una rete random pesca sigmoid(0) ~ 0.5 in media: accuracy ~ 0.5 su un
# dataset bilanciato. Dopo training, accuracy 0.92. Cos'e' cambiato:
# (a) l'architettura della rete, (b) i pesi, (c) gli input, (d) la sigmoid?
# RISPOSTA:
# (b)


# ==========================================================================
# SEZIONE 1 - BCE: la loss standard per classificazione binaria
# ==========================================================================

# ---------------------- ANALOGIA --------------------------------------------
# Un broker che valuta pratiche sbaglia. Domanda: come misuri quanto
# sbaglia?
#
#   (1) ACCURACY (= % di pratiche correttamente classificate)
#       Pro: facile. "9 su 10 giuste".
#       Contro: discreta. Se p=0.51 vs y=1 e p=0.99 vs y=1, sono entrambi
#               "giusto" -> non distinguo "tiepido" da "sicuro".
#
#   (2) LOSS BCE (Binary Cross-Entropy)
#       Numero CONTINUO. Piu' la rete e' sicura della verita', loss bassa.
#       Piu' e' sicura sbagliando, loss esplode (verso +infinito).
#       Pro: derivabile -> si puo' chiedere "se sposto un peso di poco,
#            cosa cambia alla loss?". Lo facciamo dal cap.04.
#       Contro: meno intuitiva di "9 su 10".
#
# Per il web dev: accuracy = "test passa/fallisce", loss = "test con
# punteggio 0-100, lascia spazio a 'quasi passato'".


# ---------------------- TEORIA + CODICE --------------------------------------
# 1.1 - LA FORMULA BCE
#
# Per UNA pratica con verita' y in {0, 1} e probabilita' predetta p in (0, 1):
#
#       loss = - y * log(p) - (1 - y) * log(1 - p)
#
# Funziona come "interruttore" automatico:
#   - se y = 1: (1 - y) = 0 -> sparisce il secondo termine
#               loss = - log(p)
#               -> p ~ 1 (rete giusta):  -log(1) = 0      OK
#               -> p ~ 0 (rete sbagliata): -log(0) = +inf  PUNIZIONE
#   - se y = 0: y = 0 -> sparisce il primo termine
#               loss = - log(1 - p)
#               -> p ~ 0 (rete giusta):  -log(1) = 0      OK
#               -> p ~ 1 (rete sbagliata): -log(0) = +inf  PUNIZIONE
#
# Sul batch: media della loss su tutte le N pratiche.

# 🔵 MINI-ESERCIZIO INLINE 1.1.A (~3 minuti) — calcolo manuale
# Calcola la BCE A MANO (con calcolatrice o `import math`) per:
#   - y = 1, p = 0.8 -> loss = ?
#   - y = 1, p = 0.2 -> loss = ?
#   - y = 0, p = 0.8 -> loss = ?
#   - y = 0, p = 0.2 -> loss = ?
# Quale dei 4 casi e' "rete che sbaglia di piu'"?
# TUO CALCOLO/COMMENTO QUI:


# 🔵 MINI-ESERCIZIO INLINE 1.1.B (~3 minuti) — formula come interruttore
# Verifica che la formula completa "y*log(p) + (1-y)*log(1-p)" si riduce a:
#   - log(p)        quando y = 1   (sostituisci y=1 e semplifica)
#   - log(1 - p)    quando y = 0   (sostituisci y=0 e semplifica)
# Scrivi sotto i 2 passaggi in commento.
# TUA SCRITTURA:


# Ora la funzione bce_loss e' DEFINITA IN ALTO (la riusi). Verifichiamola.

# 🔵 MINI-ESERCIZIO INLINE 1.1.C (~3 minuti) — usa la funzione
# Verifica con bce_loss():
#   - bce_loss(np.array([0.8]), np.array([1])) ~ 0.22
#   - bce_loss(np.array([0.5]), np.array([1])) ~ 0.69
#   - bce_loss(np.array([0.5]), np.array([0])) ~ 0.69
# Cosa noti su p=0.5? La BCE e' "tiepida" indipendentemente da y!
# TUO CODICE QUI:


# 1.2 - PERCHE' SERVE IL CLIP BILATERALE
#
# log(0) = -inf, e in NumPy:    0 * log(0) = NaN (non 0!)
# Quindi se y=1 e p=0:          loss = -1 * log(0) - 0 * log(1) = +inf
# E se y=0 e p=1:                loss = -0 * log(1) - 1 * log(0) = +inf
# Ma anche se "moltiplichi 0 per inf" NumPy fa NaN, non 0.
#
# Soluzione: clip BILATERALE
#     p_safe = np.clip(p, eps, 1 - eps)       eps = 1e-12 (piccolissimo)
# Se proteggi solo (eps, 1) ti esplode quando y=0 e p=1.
# Vedi il codice di bce_loss in alto.

# 🔵 MINI-ESERCIZIO INLINE 1.2.A (~2 minuti) — verifica clip bilaterale
# Senza il clip, cosa succederebbe con:
#   p = np.array([0.0, 1.0]), y = np.array([1, 0])
# Prevedi PRIMA in commento, POI verifica chiamando bce_loss
# (che ha il clip) e poi anche la formula manuale (senza clip).
# TUO CODICE QUI:


# 1.3 - LOSS CURVE: visualizza la BCE in funzione di p


def _grafico_bce(
    out_path: str | None = None,
    show: bool = False,
) -> None:
    """Plot BCE(p) per y=0 e y=1 - mostra che la loss esplode in modo asimmetrico."""
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


# 🔵 MINI-ESERCIZIO INLINE 1.3.A (~3 minuti) — prevedi dal grafico
# Dopo aver chiamato _grafico_bce (TODO 1.3 sotto), guarda il grafico
# `figures/03_01_bce_loss.png` e PREVEDI a occhio:
#   - se y=1 e p=0.6, la BCE e' circa: (a) 0.1  (b) 0.5  (c) 1.0  (d) 2.0
#   - se y=0 e p=0.9, la BCE e' circa: (a) 0.1  (b) 0.5  (c) 1.0  (d) 2.5
# Poi verifica con bce_loss().
# TUO COMMENTO + CODICE QUI:


# 1.4 - BCE BATCH: come si calcola sulla media di N pratiche
# La formula su batch e' semplicemente la MEDIA delle BCE singole:
#       loss_batch = mean( bce_loss_singola[i] for i in range(N) )
# In NumPy si fa vettorizzato (vedi bce_loss in alto).

# 🔵 MINI-ESERCIZIO INLINE 1.4.A (~5 minuti) — batch + argmax
# Dato:
#   y = np.array([1, 0, 1, 0, 1])
#   p = np.array([0.9, 0.1, 0.8, 0.7, 0.05])
# Calcola:
#   1) loss singola per ogni pratica (5 valori)
#   2) loss media (1 valore)
#   3) argmax(loss_singole) -> indice della pratica peggiore
# La pratica peggiore qual e'? Perche'? (rispondi in commento)
# TUO CODICE QUI:


# ==========================================================================
# SEZIONE 2 - BCE vs MSE: perche' BCE per classificazione binaria
# ==========================================================================
#
# 2.1 - MSE (Mean Squared Error) per riferimento
#       loss = mean((p - y)^2)
# (vedi funzione `mse_loss` in alto)
#
# Confronto con p molto distante dalla verita':
#   y=1, p=0.01:   BCE = -log(0.01) = 4.6  (punizione enorme)
#                  MSE = (0.01 - 1)^2 = 0.98 (limitata a 1)
#   y=1, p=0.5:    BCE = -log(0.5) = 0.69
#                  MSE = (0.5 - 1)^2 = 0.25
#   y=1, p=0.99:   BCE = -log(0.99) = 0.01
#                  MSE = (0.99 - 1)^2 = 0.0001


def _confronto_bce_mse() -> None:
    """Stampa BCE vs MSE per varie p con y=1 fissato."""
    y = np.array([1.0])
    print(f"{'p':>10} {'BCE':>10} {'MSE':>10}")
    for p_val in [0.01, 0.1, 0.5, 0.9, 0.99]:
        p = np.array([p_val])
        bce = bce_loss(p, y)
        mse = mse_loss(p, y)
        print(f"{p_val:>10.2f} {bce:>10.4f} {mse:>10.4f}")
    print("BCE esplode quando p si discosta dalla verita'. MSE rimane modesto.")


# 🔵 MINI-ESERCIZIO INLINE 2.1.A (~3 minuti) — replicare tabella
# Replica la tabella di sopra ma con y=0 (e p variabile da 0.01 a 0.99).
# Cosa cambia? Quale colonna ti "punisce di piu'" gli errori clamorosi?
# TUO CODICE QUI:


# 2.2 - PERCHE' la BCE punisce di piu' i casi "sicuro sbagliato"
#
# Intuizione: la BCE e' costruita con `log`, che esplode a -inf vicino
# a zero. L'MSE e' un quadrato, limitato a 1 (su valori in [0, 1]).
#
# Implicazione per il TRAINING (cap.06): il gradiente della BCE quando
# p e' molto distante dalla verita' e' MOLTO PIU' GRANDE del gradiente
# dell'MSE. Tradotto: la BCE "tira via" la rete dagli errori clamorosi
# in modo molto piu' netto.
#
# Bonus storico: la derivata di "BCE + sigmoid" si semplifica
# miracolosamente in (p - y). Niente derivata della sigmoid da
# moltiplicare. E' uno dei motivi per cui in DL si combinano
# "sigmoid + BCE" e "softmax + cross-entropy". Lo dimostreremo nel
# cap.04 e useremo nel cap.06.

# 🔵 MINI-ESERCIZIO INLINE 2.2.A (~5 minuti) — soglia di "esplosione"
# A che valore di p la BCE supera 1.0 (con y=1)?  E supera 5.0?
# Suggerimento: BCE = -log(p), quindi cerchi p tale che -log(p) = 1
# (cioe' p = 1/e ~ 0.37). Verifica anche numericamente.
# TUO CODICE QUI:


# ==========================================================================
# SEZIONE 3 - ACCURACY + soglia 0.5
# ==========================================================================
#
# 3.1 - ACCURACY in NumPy
#
# Da P (probabilita' in (0, 1)) a y_pred (binario 0/1):
#       y_pred = (P >= 0.5).astype(int)     soglia 0.5 e' NEUTRA
#
# Poi accuracy:
#       acc = float(np.mean(y_pred == y))
#
# (vedi funzione `accuracy_score` in alto)
#
# ATTENZIONE: P > 0 e' SEMPRE True quando P arriva da sigmoid!
# (perche' sigmoid(z) in (0, 1) sempre). Quindi (P > 0) restituisce
# tutti 1 -> accuracy ~ frequenza di y=1 nel dataset. Sbaglio classico.

# 🔵 MINI-ESERCIZIO INLINE 3.1.A (~3 minuti) — accuracy sbagliata
# Dato P = np.array([0.1, 0.4, 0.6, 0.9]) e y = np.array([0, 0, 1, 1]):
#   1) calcola accuracy con soglia 0.5 (giusta)
#   2) calcola accuracy con "soglia" P > 0 (sbagliata: prevede SEMPRE 1)
# Quale differenza vedi?
# TUO CODICE QUI:


# 🔵 MINI-ESERCIZIO INLINE 3.1.B (~3 minuti) — soglia personalizzata
# Stessa P e y di sopra. Calcola accuracy con soglie 0.3, 0.5, 0.7.
# Quale ti da' accuracy piu' alta? Perche'? (la "soglia ottima" puo'
# variare a seconda dei costi di falsi positivi vs falsi negativi - lo
# vedrai nei capitoli sul deploy.)
# TUO CODICE QUI:


# 3.2 - LOSS vs METRICA: regola operativa
#
# - LOSS (BCE):       DURANTE il training, su PROBABILITA' continue.
# - METRICA (acc/AUC/recall/precision): DOPO il training, per giudicare.
#   - accuracy/recall/precision/F1: su PREDIZIONI binarie (P >= soglia)
#   - AUC (ROC):                    su PROBABILITA' continue, NON binari
#
# Errore tipico (lacuna cap.02 mini-progetto):
#       y_pred = (P >= 0.5).astype(int)
#       auc = roc_auc_score(y, y_pred)        # SBAGLIATO: AUC vuole P
#       roc_auc_score(y, P)                   # GIUSTO

# 🔵 MINI-ESERCIZIO INLINE 3.2.A (~5 minuti) — AUC su P vs su binari
# Dato:
#   P = np.array([0.10, 0.45, 0.55, 0.95])
#   y = np.array([0, 1, 0, 1])
# Calcola:
#   1) accuracy con soglia 0.5
#   2) AUC su P (continuo)         -> roc_auc_score(y, P)
#   3) AUC su (P>=0.5).astype(int) -> roc_auc_score(y, y_pred)
# Perche' (2) e (3) danno valori diversi?
# Suggerimento: AUC su (2) usa il RANKING delle 4 probabilita',
# AUC su (3) collassa tutto a binario e perde l'informazione di ordine.
# TUO CODICE QUI:


# ==========================================================================
# ESERCIZI MIRATI BASE (TODO 1.1 - 1.3)
# Sono i 3 TODO storici migrati dal vecchio file con il codice studente.
# ==========================================================================

# TODO 1.1 (5 minuti):
# Crea y = np.array([1, 0, 1, 0, 1]) e p = np.array([0.9, 0.1, 0.8, 0.2, 0.05])
# Calcola e stampa:
#   - la BCE media
#   - quale pratica contribuisce DI PIU' alla loss (argmax delle 5 loss singole)
# Spiega in 1 commento PERCHE' quella e' la pratica "peggiore".
# TUO CODICE QUI:
y = np.array([1, 0 , 1, 0, 1])
p = np.array([0.9, 0.1, 0.8, 0.2, 0.05])

# y * np.log(p_safe) - (1.0 - y) * np.log(1.0 - p_safe)
bce = - y * np.log(p) - (1 - y) * np.log(1.0 - p)
bce_mean = bce.mean()
bce_max = np.argmax(bce)
print(bce_mean)
print(bce_max)

# la pratica in indice 4 è la peggiore perchè è quella che si discosta di più per valore predetto rispetto al valore reale.


# TODO 1.2 (5 minuti):
# Verifica empiricamente che BCE perfetta = 0:
#   - y = np.array([1, 0, 1, 0])
#   - p = np.array([0.99999, 0.00001, 0.99999, 0.00001])    (quasi perfette)
#   - p = y  -> ATTENZIONE: log(0) = -inf e 0*log(0) = NaN. Usa eps=1e-12.
# Cosa stampa bce_loss in entrambi i casi? Perche' NON puoi mettere p = y
# senza il clip?
# TUO CODICE QUI:
y = np.array([1, 0, 1, 0])
p = np.array([0.99999, 0.00001, 0.99999, 0.00001])
eps = 1e-12

p_safe = np.clip(p, eps, 1 - eps)

bce_safe = - y * np.log(p_safe) - (1.0 - y) * np.log(1.0 - p_safe)
print(bce_safe)

p = y

bce = - y * np.log(p) - (1.0 - y) * np.log(1.0 - p)

print(bce)

p_safe = np.clip(p, eps, 1 - eps)

bce_safe = - y * np.log(p_safe) - (1.0 - y) * np.log(1.0 - p_safe)
print(bce_safe)

# Per tutti i casi, la bce_loss è un numero infinitesima. Se non usassimo il clip, nel caso in cui in input fornissimo array di 0 e 1, avremo nella formula dei log(0), i quali restituirebbero a loro volta una array di nan.


# TODO 1.3 (3 minuti):
# Chiama _grafico_bce passando out_path = "figures/03_01_bce_loss.png"
# e verifica con os.path.exists() che il file sia stato creato.
# TUO CODICE QUI:
print("\nTODO 1.3\n")

_grafico_bce(out_path="figures/03_01_bce_loss.png")
file_created = os.path.exists(os.path.join(os.path.dirname(__file__), "figures/03_01_bce_loss.png"))
assert file_created, "Il file non è stato creato!!"
if file_created:
    print("File creato con successo!!")


# ==========================================================================
# 🔁 RINFORZO MIRATO - "LOSS (per training) VS METRICA (per giudicare)"
# Pattern ⚠️ emerso nel mini-progetto cap.02 (AUC su 0/1 invece che su P).
# ==========================================================================
#
# Regola pratica:
#   - LOSS:           con PROBABILITA' continue P (cap.03 BCE).
#   - METRICA finale: dipende:
#       * accuracy/recall/precision/F1 -> binari (P >= soglia)
#       * AUC ROC                       -> probabilita' continue
#
# Vedi anche le funzioni `accuracy_score` (con soglia) in alto.


# ==========================================================================
# RINFORZI CAP.01-02 M3 (TODO 4.1 - 4.4) — Ricostruisci la rete del cap.02
# ==========================================================================

# TODO 4.1 (5 minuti) [🔄 RECALL cap.01 M3 — neurone manuale]:
# RIVEDI in mente il cap.01 M3: un neurone artificiale e' fondamentalmente
#       z = w . x + b      (dot product + bias)
#       y_pred = sigmoid(z)
#
# Dato:
#   x = np.array([1.0, -2.0, 3.0])      # 3 feature
#   w = np.array([0.5, -0.3, 0.2])      # 3 pesi
#   b = 0.1
# Calcola z (scalare) e y_pred = sigmoid(z) usando la funzione `sigmoid`
# definita in alto. Stampa entrambi.
# Suggerimento: usa np.dot(w, x) per il prodotto scalare.
# TUO CODICE QUI:
print("\nTODO 4.1\n")
x = np.array([1.0, -2.0, 3.0])
w = np.array([0.5, -0.3, 0.2])
b = 0.0

z = x @ w + b # np.dot(x, w) +b
y_pred = sigmoid(z) # 1 / (1 + np.exp(-z)) -> sigmoide
print (p)

# TODO 4.2 (8 minuti) [🔄 RECALL cap.02 M3 — forward 2-layer]:
# Estendi a una RETE 2-layer con h=4 neuroni hidden:
#   X = np.array([[1.0, -2.0, 3.0],
#                 [0.5,  0.5, 0.5],
#                 [-1.0, 2.0, -3.0]])    # 3 pratiche, 3 feature
#   rng = np.random.default_rng(0)
#   W1 = rng.standard_normal((3, 4)) * 0.1
#   b1 = np.zeros(4)
#   W2 = rng.standard_normal((4, 1)) * 0.1
#   b2 = np.zeros(1)
# Calcola passo per passo (e stampa le shape!):
#   Z1 = X @ W1 + b1
#   H  = relu(Z1)
#   Z2 = H @ W2 + b2
#   P  = sigmoid(Z2).ravel()      # shape (3,)
# Verifica: P deve essere (3,), valori in (0, 1).
# TUO CODICE QUI:
print("\nTODO 4.2\n")
X = np.array(
    [[1.0, -2.0, 3.0],
    [0.5,  0.5, 0.5],
    [-1.0, 2.0, -3.0]]
)
d, h, k = 3, 4, 1
rng = np.random.default_rng(0)
W1 = rng.standard_normal(size=(d, h)) * np.sqrt(2.0 / d)
b1 = np.zeros(h)
W2 = rng.standard_normal(size=(h, k)) * np.sqrt(2.0 / h)
b2 = np.zeros(k)

Z1 = X @ W1 + b1
print(Z1.shape)
H = np.maximum(0.0, Z1)
Z2 = H @ W2 + b2
print(Z2.shape)
P = 1 / (1 + np.exp(- np.clip(Z2, -500, +500))).ravel()

assert P.shape[0] == X.shape[0] and P.ndim == 1, "Ops qualcosa è andato storto!"

print(P.ravel())


# TODO 4.3 (5 minuti) [🔀 INTERLEAVING cap.02 + cap.03] — Forward + BCE:
# Riprendi il TODO 4.2: hai P (shape (3,)) dalla rete random.
# Aggiungi y = np.array([1, 0, 1]).
# Calcola:
#   1) la BCE media usando bce_loss(P, y)
#   2) l'accuracy con accuracy_score(P, y)
# Cosa ti aspetti? BCE ~ 0.69 (= log(2)) perche' pesi random producono
# P ~ 0.5. Accuracy puo' essere ovunque tra 0 e 1 a causa del campione
# piccolo (N=3).
# TUO CODICE QUI:
print("\nTODO 4.3\n")

y = np.array([1, 0, 1])

BCE_tool = bce_loss(P, y)
eps = 1e-12
P_safe = np.clip(P, eps, 1 - eps )
BCE_manual = (- y * np.log(P_safe) - (1.0 - y) * np.log(1.0 - P_safe)).mean()
assert np.isclose(BCE_tool, BCE_manual), "Le due BCE non combaciano!"
acc_score = accuracy_score((P_safe >= 0.5).astype(int), y)

print(f"BCE TOOL: {BCE_tool} BCE MANUAL: {BCE_manual}")
print(f"ACCURACY_SCORE: {acc_score}")


# TODO 4.4 (10 minuti) [🧠 RETRIEVAL cap.02 M3] — Riscrivi `layer_dense`:
# Senza aprire `02_reti_neurali.py`, riscrivi da zero la funzione
# `layer_dense` come l'hai imparata nel cap.02 M3.
#
# Firma attesa:
#   def layer_dense(
#       X: NDArray[np.float64],
#       W: NDArray[np.float64],
#       b: NDArray[np.float64],
#       activation: Callable[[NDArray[np.float64]], NDArray[np.float64]] | None = None,
#   ) -> NDArray[np.float64]:
#       """Restituisce activation(X @ W + b). Se activation=None, restituisce
#       solo l'output lineare X @ W + b."""
#       ...
#
# Verifica con:
#   X = np.random.default_rng(0).standard_normal((5, 4))
#   W = np.random.default_rng(0).standard_normal((4, 8)) * 0.1
#   b = np.zeros(8)
#   out_lineare = layer_dense(X, W, b)              # shape (5, 8)
#   out_relu    = layer_dense(X, W, b, relu)        # shape (5, 8), valori >= 0
#   out_sigmoid = layer_dense(X, W, b, sigmoid)     # shape (5, 8), valori in (0,1)
# Stampa le 3 shape.
# TUO CODICE QUI:
print("\nTODO 4.4\n")
def layer_dense(
    X: NDArray[np.float64],
    W: NDArray[np.float64],
    b: NDArray[np.float64] | float,
    att: Callable[[NDArray[np.float64] | float], NDArray[np.float64] | float] | None = None
) -> NDArray[np.float64]:
    if X.ndim != 2:
        raise ValueError("X deve essere una matrice 2D!")
    if W.ndim > 2:
        raise ValueError("W può essere un vettore o una matrice!")
    if X.shape[1] != W.shape[0]:
        raise ValueError("X.shape[1] e W.shape[0] devono coincidere")
    Z = X @ W + b
    if att is not None:
        return att(Z)
    return Z

def my_relu(
    z: NDArray[np.float64] | float
) -> NDArray[np.float64] | float:
    out = np.maximum(0.0, z)
    if np.isscalar(z):
        return float(out)
    return out

def my_sigmoid(
    z: NDArray[np.float64] | float
) -> NDArray[np.float64] | float:
    z_safe = np.clip(z, -500, +500, dtype=float)
    out = 1 / (1 + np.exp(-z_safe))
    if np.isscalar(z):
        return float(out)
    return out


rng = np.random.default_rng(0)
X = rng.standard_normal(size=(5, 4))
W = rng.standard_normal(size=(4, 8)) * 0.1 # sostitutivo di scala np.sqrt(2 / 4)
b = np.zeros(8)

out_lineare = layer_dense(X, W, b, att=None)
out_relu = layer_dense(X, W, b, att=my_relu)
out_sigmoid = layer_dense(X, W, b, att=my_sigmoid)

print(out_lineare.shape)
print(out_relu.shape)
print(out_sigmoid.shape)


# ==========================================================================
# RINFORZI LACUNE EMERSE (TODO 5.1 - 5.3) — Sigilla i 3 anti-pattern
# ==========================================================================

# TODO 5.1 (5 minuti) [🔴 PATTERN segno BCE]:
# Hai sotto 4 formule "candidate" della BCE. UNA SOLA e' corretta.
# Per ognuna, calcolala su y = np.array([1, 0]) e p = np.array([0.9, 0.1])
# e stampa il risultato. Indica:
#   - quale e' la formula corretta
#   - perche' le altre 3 danno valori "negativi" o "incoerenti"
#
# Candidate:
#   (a) loss_a =   y * np.log(p) + (1-y) * np.log(1-p)
#   (b) loss_b = - y * np.log(p) - (1-y) * np.log(1-p)
#   (c) loss_c = - y * np.log(p) + (1-y) * np.log(1-p)
#   (d) loss_d =   y * np.log(p) - (1-y) * np.log(1-p)
# TUO CODICE QUI:
print("\nTODO 5.1\n")

# la risposta corretta è la (b)

y = np.array([1, 0])
p = np.array([0.9, 0.1])

loss_a =   y * np.log(p) + (1-y) * np.log(1-p)
loss_b = - y * np.log(p) - (1-y) * np.log(1-p)
loss_c = - y * np.log(p) + (1-y) * np.log(1-p)
loss_d =   y * np.log(p) - (1-y) * np.log(1-p)

print(loss_b, f" -> risposta corretta!")
print(loss_a)
print(loss_c)
print(loss_d)

# a e d non traformano in negativa la y dando quindi un segno finale errato (-),e la d inoltre, come anche la c, non utilizzano correttamente lo switch matematico - (1 - y), e quindi da un valore sbagliato.

# TODO 5.2 (5 minuti) [⚠️ PATTERN clip bilaterale]:
# Testa 3 versioni di clip su:
#     y = np.array([1, 0])
#     p = np.array([0.0, 1.0])      # casi estremi
#
#   v1:  p_safe = p                              (niente clip)
#   v2:  p_safe = np.clip(p, 1e-12, 1)           (solo lato basso)
#   v3:  p_safe = np.clip(p, 1e-12, 1 - 1e-12)   (BILATERALE - corretto)
#
# Per ognuna calcola la BCE manualmente (- y*log(p_safe) - (1-y)*log(1-p_safe))
# e stampa il risultato. Segnala se vedi NaN, +inf, oppure un numero
# "ragionevole".
# Domanda finale (in commento): perche' v2 NON BASTA quando y=0 e p=1?
# TUO CODICE QUI:

print("\nTODO 5.2\n")

y = np.array([1, 0])
p = np.array([0.0, 1.0])
eps = 1e-12
p_semi_safe = np.clip(p, eps, 1)
p_safe = np.clip(p , eps, 1 - eps)

BCE_p = - y * np.log(p) - (1 - y) * np.log(1 - p)
BCE_semi = - y * np.log(p_semi_safe) - (1 - y) * np.log(1 - p_semi_safe)
BCE_safe = - y * np.log(p_safe) - (1 - y) * np.log(1 - p_safe)
print("v1 (no clip):", BCE_p)
print("v2 (solo basso):", BCE_semi)
print("v3 (bilaterale):", BCE_safe)
# non basta porre un taglio sicuro solo in basso (0), perchè comunque ci sarebbe il rischio di avere inf con un 1. 

# TODO 5.3 (5 minuti) [⚠️ PATTERN soglia 0.5]:
# P = np.array([0.10, 0.45, 0.55, 0.95])
# y = np.array([0, 1, 0, 1])
# Calcola accuracy con DUE soglie:
#   - soglia_sbagliata: y_pred1 = (P > 0).astype(int)
#   - soglia_giusta:    y_pred2 = (P >= 0.5).astype(int)
# Per ognuna stampa y_pred e accuracy.
# Domanda in commento: perche' "P > 0" e' SEMPRE True quando P viene da sigmoid?
# perchè la funzione sigmoide trasforma tutti in numeri in una scala che ha limiti 0 e 1 (quindi il risultato non sarà mai inferiore a 0)
# TUO CODICE QUI:

print("\nTODO 5.3\n")

P = np.array([0.10, 0.45, 0.55, 0.95])
y = np.array([0, 1, 0, 1])

y_pred1 = (P > 0).astype(int)
y_pred2 = (P > 0.5).astype(int)

acc_score_1 = accuracy_score(P, y, soglia=0.0)
acc_score_2 = accuracy_score(P, y, soglia=0.5)

print(y_pred1, f"-> Accuracy Score: {acc_score_1}")
print(y_pred2, f"-> Accuracy Score: {acc_score_2}")


# ==========================================================================
# PIPELINE INTEGRATA — `valuta_rete_random()`
# ==========================================================================
#
# OBIETTIVO: combinare TUTTO il cap.01-03 in una sola pipeline.
#
# Step (da implementare nel TODO sotto):
#   1) Genera dati sintetici:
#         rng = np.random.default_rng(0)
#         N, d, h = 200, 5, 16
#         X = rng.standard_normal((N, d))
#         y = (X[:, 0] + X[:, 1] > 0).astype(int)    # label "complessa"
#   2) Inizializza una rete 2-layer con He init (recall cap.02 M3):
#         W1 = rng.standard_normal((d, h)) * np.sqrt(2.0 / d)
#         b1 = np.zeros(h)
#         W2 = rng.standard_normal((h, 1)) * np.sqrt(2.0 / h)
#         b2 = np.zeros(1)
#   3) Forward (recall cap.02 M3):
#         Z1 = X @ W1 + b1
#         H  = relu(Z1)
#         Z2 = H @ W2 + b2
#         P  = sigmoid(Z2).ravel()
#   4) Loss + metriche (cap.03 LOSS):
#         loss = bce_loss(P, y)
#         acc  = accuracy_score(P, y)
#   5) Stampa loss, accuracy. Ti aspetti loss ~ 0.69 (log 2),
#      accuracy ~ 0.5 (rete random).

# TODO PIPE.1 (15 minuti) — implementa la pipeline sopra in una funzione:
#
#   def valuta_rete_random(
#       N: int = 200,
#       d: int = 5,
#       h: int = 16,
#       seed: int = 0,
#   ) -> dict[str, float]:
#       """Ritorna {'loss': ..., 'accuracy': ..., 'n': ...}."""
# Verifica chiamandola con 3 seed diversi (0, 1, 42): la loss DEVE
# essere intorno a 0.69, l'accuracy intorno a 0.5 (con qualche
# variazione perche' il dataset e' piccolo).
# TUO CODICE QUI:

print("\nTODO PIPE .1\n")

def my_He_init(
    d: int,
    h: int,
    seed: int = 42
) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    rng = np.random.default_rng(seed)
    scale = np.sqrt(2 / d)    
    return rng.standard_normal(size=(d, h)) * scale, np.zeros(h)

def valuta_rete_random(
    N: int = 200,
    d: int = 5,
    h: int = 16,
    seed: int = 0
) -> dict[str, float]:
    
    # inizializzazione dei valori sintentici
    
    rng = np.random.default_rng(seed)
    X = rng.standard_normal(size=(N, d))
    W1, b1 = my_He_init(d, h, seed)
    W2, b2 = my_He_init(h, 1, seed)
    y = (X[:, 0] + X[:, 1] > 0).astype(int) # versione alternativa (X[:, d//2]).sum(axis=1).astype(int)
    
    # fase forward

    Z1 = X @ W1 + b1
    H = my_relu(Z1)
    Z2 = H @ W2 + b2
    Z2_safe = np.clip(Z2, -500, +500)
    P = my_sigmoid(Z2_safe).ravel()
    
    # calcolo loss e BCE
    
    P_safe = np.clip(P, 1e-12, 1 - 1e-12)
    BCE = (- y * np.log(P_safe) - (1 - y) * np.log(1 - P_safe)).mean()
    BCE_tool = bce_loss(P, y)
    
    assert np.isclose(BCE, BCE_tool, atol=1e-12), "Problemi con la BCE, il calcolo manuale e tramite tool non combaciano!"
    
    acc_score = accuracy_score(P, y, soglia=0.5)
    
    return {
        "loss": float(BCE),
        "accuracy" : acc_score,
        "n": N
    }    
    
if __name__ == "__main__":
    pprint(valuta_rete_random(seed=0))
    pprint(valuta_rete_random(seed=1))
    pprint(valuta_rete_random(seed=42))

# ==========================================================================
# TIPOLOGIE STANDARD (TODO 6 - 11)
# ==========================================================================

# TODO 6 (15 minuti) [🎯 COLLOQUIO]:
# "Sei in un colloquio AI Engineer. L'intervistatore ti chiede:
#  'Cos'e' la Binary Cross-Entropy? Quando la useresti? Quali sono i
#  bug tipici di chi la implementa la prima volta?'
# Rispondi in 6-8 righe MASSIMO, struttura:
#   (1) Cosa misura (1 riga)
#   (2) Formula a parole (1-2 righe, NIENTE LaTeX)
#   (3) Quando si usa (1 riga)
#   (4) 3 bug tipici (2-3 righe)
#   (5) (bonus) perche' BCE invece di MSE per classificazione (1 riga)"
# TUA RISPOSTA:
# la BCE è la loss utilizzata per addestrare una rete neurale, la quale deve produrre un output di tipo binario. Misura quando la rete è sicura delle sue risposte. la formula è per y == 1 -> -log(P) e per y == 0 -log(1 - p). Un bug tipico è quello di non prevedere un clipping per i valori in uscita dall'ultimo layer (sigmoide), che non devono coincidere con 0 e 1, così da evitare che vengano prodotti valori nan o inf. Rispetto all' MSE, la BCE punisce in modo maggiore (tendente a inf) per gli errori di sconstamento più grandi.


# TODO 7 (15 minuti) [🔧 REFACTORING]:
# Questa implementazione di bce_loss "funziona" ma e' lentissima e brutta.
# Riscrivila in modo VETTORIZZATO (no for) e pulito.
#
#   def bce_loss_brutta(p, y):
#       totale = 0.0
#       eps = 1e-12
#       for i in range(len(p)):
#           p_i = max(eps, min(1 - eps, p[i]))
#           if y[i] == 1:
#               totale += - np.log(p_i)
#           else:
#               totale += - np.log(1 - p_i)
#       loss = totale / len(p)
#       return round(loss, 6),        # bug stile (regola #21 tuple/round)
#
# Riscrivila con:
#   - clip vettorizzato (np.clip)
#   - formula in una sola riga
#   - return float, non tupla
#   - type hint corretti (NDArray[np.float64])
# Confronta poi i risultati con la `bce_loss` definita in alto su
# array random (devono coincidere a meno di 1e-12).
# TUO CODICE QUI:

print("\nTODO 7\n")

def bce_loss_bella(
    p: NDArray[np.float64],
    y: NDArray[np.float64] | NDArray[np.int64],
    eps: float = 1e-12) -> float:
    p_safe = np.clip(p, eps, 1 - eps)
    return float((- y * np.log(p_safe) - (1 - y) * np.log(1 - p_safe)).mean())
rng = np.random.default_rng(0)
P = rng.uniform(0, 1, size=(10))
y = rng.uniform(0.5, 1.5, size=(10)).astype(int)

assert np.isclose(bce_loss_bella(P, y), bce_loss(P, y), atol=1e-12), "Le BCE non coincidono!!"

print(bce_loss_bella(P, y))
print(bce_loss(P, y))


# TODO 8 (15 minuti) [🔍 DEBUG]:
# Il codice sotto gira ma ogni tanto restituisce NaN. Trova il bug,
# spiegalo in commento, e dai la versione corretta.
#
#   def bce_buggata(p, y):
#       loss = - y * np.log(p) - (1 - y) * np.log(1 - p)
#       return float(np.mean(loss))
#
# Indizio: NON e' il segno meno (quello c'e'). Pensa ai casi in cui p
# vale ESATTAMENTE 0 o ESATTAMENTE 1.
# Verifica con:
#   p = np.array([0.0, 0.5, 1.0])
#   y = np.array([1, 1, 0])
# TUO CODICE QUI:
print("\nTODO 8 DEBUG\n")
def bce_riparata(
    p: NDArray[np.float64] = np.array([0.0, 0.5, 1.0]),
    y: NDArray[np.float64] = np.array([1, 1, 0])
) -> float:     
    eps = 1e-12
    p_safe = np.clip(p, eps, 1 - eps)
    loss = (- y * np.log(p_safe) - (1 - y) * np.log(1 - p_safe)).mean()
    return float(loss)

print(bce_riparata())

# Il problema è che non prevedendo un clipping per i valori di p, automaticamente vengono prodotti
# dei nan e inf. L'ho riparato inserendo un controllo sui valori di p.

# TODO 9 (15 minuti) [🧠 RETRIEVAL cap.02 M3 — full]:
# SENZA APRIRE 02_reti_neurali.py, riscrivi da zero la funzione
# `rete_2_layer` come la ricordi dal cap.02:
#
#   def rete_2_layer(X, W1, b1, W2, b2) -> NDArray[np.float64]:
#       """Forward completo: H = ReLU(X@W1+b1), P = sigmoid(H@W2+b2).ravel().
#       Ritorna P, shape (N,)."""
#       ...
#
# Verifica che la tua versione produca lo stesso P della pipeline TODO PIPE.1.
# TUO CODICE QUI:

def my_rete_2_layer(
    X: NDArray[np.float64],
    W1: NDArray[np.float64],
    b1: NDArray[np.float64] | float,
    W2: NDArray[np.float64],
    b2: NDArray[np.float64] | float
)-> NDArray[np.float64]:
    Z1 = X @ W1 + b1
    H = relu(Z1)
    Z2 = H @ W2 + b2
    P = sigmoid(np.clip(Z2, -500, +500)).ravel()
    return P

# TODO 10 (20 minuti) [🔀 INTERLEAVING cap.01 + cap.02 + cap.03 M3]:
# Mini pipeline a "due reti casuali" (test di varianza):
#   1) Genera dataset come in PIPE.1 (N=200, d=5)
#   2) Inizializza DUE reti random (seed 0 e seed 1, stessa architettura h=16)
#   3) Per ciascuna rete: forward + BCE + accuracy + numero di P > 0.5
#   4) Stampa una tabella con 2 righe (1 per rete) e 4 colonne
#   5) Commenta in 2 righe: quanto variano loss e accuracy fra 2 reti
#      random? Quale conclusione trai sull'importanza dei pesi iniziali?
# TUO CODICE QUI:

print("\nTODO 10\n")

N, d, h, k = 200, 5, 16, 1
seeds = [0, 1]
X = rng.standard_normal(size=(N, d))
y = ((X[:, 0] + X[:, 1]) > 0).astype(int)
report = []
for seed in seeds:
    W1, b1 = my_He_init(d, h, seed=seed)
    W2, b2 = my_He_init(h, k, seed=seed)

    P = my_rete_2_layer(X, W1, b1, W2, b2)

    bce = bce_loss(P, y)
    acc = accuracy_score(P, y)
    n_prev_sup_soglia = (P[P > 0.5]).size
    result = {
        "SEED": seed,
        "BCE": bce,
        "accuracy": acc,
        "N P > 0.5": n_prev_sup_soglia,
    }
    report.append(result)
print(pd.DataFrame(report).to_string(index=False))

# possono variare molto, perchè tutto dipende dal prodotto di features e pesi , che possono produrre risultati molto diversi. In generale si osserva che in reti random l'accuracy oscilla intorno a 0.5 e bce intorno a 0.69.

# TODO 11 (15 minuti) [🌊 REAL-WORLD]:
# Il broker dice: "Ho un dataset di 1000 pratiche, ma alcune etichette
# sono UNKNOWN (codificate come -1, non 0 e non 1). Vorrei calcolare la
# BCE solo sulle pratiche con etichetta valida (0 o 1). Aiutami."
#
# Implementa:
#   def bce_robusta(p, y) -> float:
#       """Calcola la BCE solo sulle pratiche con y in {0, 1}.
#       Ignora le pratiche con y = -1 (o qualsiasi altro valore).
#       Se non ci sono pratiche valide, ritorna NaN.
#       """
#       ...
#
# Verifica con:
#   p = np.array([0.9, 0.1, 0.8, 0.7, 0.3])
#   y = np.array([1,   0,  -1,   1,  -1])     # 2 unknown
# La BCE robusta deve essere calcolata solo sulle pratiche y in {0, 1}.
# Stampa anche quante pratiche sono state ignorate.
# TUO CODICE QUI:

print("\nTODO 11\n")

def bce_robusta(p, y) -> tuple[float, float]:
    mask = np.isin(y, [0, 1])
    y_ver = y[mask]
    p_ver = p[mask]
    if p_ver.size == 0:
        return float(np.nan), float(np.nan)
    return bce_loss(p_ver, y_ver), p.size - p_ver.size
p = np.array([0.9, 0.1, 0.8, 0.7, 0.3])
y = np.array([1,   0,  -1,   1,  -1])
result = bce_robusta(p, y)
print(f"BCE pratiche verificate: {result[0]}")
print(f"Pratiche ignorate: {result[1]}")

# ==========================================================================
# QUIZ DI VERIFICA (fai PRIMA del mini-progetto finale)
# ==========================================================================

# V1) Cos'e' una LOSS in 1 riga? E perche' minimizziamo lei e non l'accuracy?
# TUA RISPOSTA:
# La loss è risposta alla domanda "ad ogni pratica, quanto sono distante dalla previsione corretta?". Si cerca di minimizzare lei e non l'accuracy perchè questa, essendo una metrica "discreta" e non continua, si limita solo a dirci quanto la rete sbaglia in senso generale, mentre la loss a un gradiente che ci permette di retropopagare l'errore e spostare ogni peso in una direzione sulla base della sua responsabilità dell'errore.

# V2) Perche' BCE invece dell'MSE per classificazione binaria (2 motivi)?
# TUA RISPOSTA:
# Perchè tramite la formula della bce che sfrutta il logaritmo naturale, è possibile amplificare in modo "esplosivo" gli errori man mano che diventano più gravi, mettendoli su una scala che tende a infinito. L’MSE punisce poco gli errori clamorosi (quadratico e limitato), quindi in training il gradiente resta più debole quando la rete sbaglia di grosso.

# V3) [Trova l'errore] Questo codice ha DUE bug. Trovali entrambi:
#       def bce_buggata(p, y, eps=1e-12):
#           p_safe = np.clip(p, eps, 1)         # bug qui
#           return float(np.mean(y * np.log(p_safe) +
#                                (1-y) * np.log(1-p_safe)))   # e qui
# TUA RISPOSTA:
# clip sbagliato -> corretto = np.clip(p, eps, 1 -eps)
# formula bce sbagliata -> corretta = float(np.mean(- y * np.log(p_safe) - (1 - y) * np.log(1 - p_safe)))

# V4) Cosa fa il `clip` nella BCE e perche' DEVE essere su entrambi i lati
#     (eps, 1-eps) e non solo (eps, 1)?
# TUA RISPOSTA:
# Perchè per P = 0 la bce restituirebbe inf e per P = 1 restituirebbe NaN, quindi dobbiamo contenere P entro valori leggerermente più grandi di 0 o leggermente più piccoli di 1.


# V5) Hai P = np.array([0.20, 0.49, 0.51, 0.80]) e y = np.array([0, 1, 0, 1]).
#     Calcola accuracy con soglia 0.5. Spiega in 1 riga perche' usiamo
#     0.5 e non 0.
# TUA RISPOSTA:
# ...

# V6) [💬 Feynman] Spiega in 4 righe a un collega web dev cos'e' la BCE.
#     VIETATO: log, probabilita', binario, entropia, gradiente, derivata.
# TUA RISPOSTA:
# ...

# V7) [Prevedi output] Dato:
#       y = np.array([1, 0, 1])
#       p = np.array([0.99, 0.01, 0.99])
#     - Che valore ha bce_loss(p, y)? (~ 0.01? 0.69? 5.0?)
#     - Che valore ha accuracy_score(p, y)? (0.0? 0.5? 1.0?)
# TUA RISPOSTA:
# ...


# ==========================================================================
# MINI-PROGETTO FINALE — `valuta_modello_completo`
# ==========================================================================
#
# OBIETTIVO: una sola funzione che riceve P (probabilita') e y (labels)
# e restituisce un dict COMPLETO con BCE, MSE, accuracy, recall,
# precision, F1, AUC. E' lo "scorecard" che useremo dal cap.06 in poi
# per giudicare reti addestrate.
#
# Firma:
#   def valuta_modello_completo(
#       P: NDArray[np.float64],
#       y: NDArray[np.int64],
#       soglia: float = 0.5,
#   ) -> dict[str, float]:
#       """
#       Ritorna un dict con (tutte chiavi minuscole):
#         'bce'        : BCE media (usa bce_loss)
#         'mse'        : MSE media (usa mse_loss)
#         'accuracy'   : accuracy con soglia (usa accuracy_score)
#         'recall'     : TP / (TP + FN)
#         'precision'  : TP / (TP + FP)
#         'f1'         : media armonica di recall e precision
#         'auc_roc'    : roc_auc_score(y, P) - USA P CONTINUA, non binari!
#         'n_pratiche' : numero pratiche (int)
#         'soglia'     : soglia usata (float)
#       """
#
# Vincoli OBBLIGATORI:
#   - P e y devono avere stesso len. Se no -> raise ValueError.
#   - soglia in (0, 1). Se no -> raise ValueError.
#   - usa bce_loss, mse_loss, accuracy_score (le funzioni gia' definite).
#   - per recall/precision/F1, scrivile tu (NON usare sklearn).
#   - per auc_roc, USA `from sklearn.metrics import roc_auc_score`.
#   - se TP+FN == 0 (nessun positivo nel dataset), recall = 0.0 (non NaN).
#   - se TP+FP == 0 (nessuna predizione positiva), precision = 0.0.
#   - se recall+precision == 0, f1 = 0.0.
#
# Verifica con 3 scenari:
#   rng = np.random.default_rng(0)
#   y = rng.integers(0, 2, size=200)
#   P_random   = rng.uniform(0, 1, size=200)
#   P_perfetta = y.astype(float) * 0.99 + 0.005
#   P_pessima  = 1.0 - P_perfetta
#
# Aspettative:
#   - P_random:    bce ~ 0.7-1.0, acc ~ 0.5, auc ~ 0.5
#   - P_perfetta:  bce ~ 0.005,   acc = 1.0, auc = 1.0
#   - P_pessima:   bce > 5,       acc = 0.0, auc = 0.0
#
# Stampa la tabella dei 3 scenari (1 riga per scenario, 1 colonna per
# metrica). Commenta in 3 righe:
#   - quale metrica e' la piu' "punitiva" sugli errori clamorosi? => la BCE
#   - accuracy e' simmetrica per random e pessima? => si è simmetrica perchè nn esplode per gli errori molto grandi, e il random si pone a metà strada.
#   - AUC sa distinguere fra random e pessima? => Si, su una rete random auc è circa 0.5, mentre in pessima è 0.
# TUO CODICE QUI:

print("\nMINI-PROGETTO FINALE\n")

def valuta_modello_completo(
    P: NDArray[np.float64],
    y: NDArray[np.int64],
    soglia: float = 0.5
) -> dict[str, float]:

    if len(P) != len(y):
        raise ValueError("P e y devono essere array di pari lunghezza")
    if soglia > 1 or soglia < 0: 
        raise ValueError("il valore della soglia deve essere un numero compreso tra 0 e 1")
    bce = bce_loss(P, y)
    mse = mse_loss(P, y)
    acc = accuracy_score(P, y, soglia=soglia)
    y_pred = (P >= soglia).astype(int)
    mask_recall = (y_pred == 1) & (y == 1)
    mask_precision = (y_pred == 1) & (y == 0)
    recall = np.sum(y_pred[mask_recall]) / (np.sum(y == 1)) if  np.sum(y == 1) > 0 else 0.0
    precision =  np.sum(y_pred[mask_recall]) / (np.sum(y_pred[mask_recall]) + np.sum(y_pred[mask_precision])) if (np.sum(y_pred[mask_recall]) + np.sum(y_pred[mask_precision])) > 0 else 0.0
    f1_score = 2 * (recall * precision) / (recall + precision) if recall + precision > 0 else 0.0
    roc_auc = roc_auc_score(y, P)
    
    return {
        'bce'        : float(bce),
        'mse'        : float(mse),
        'accuracy'   : float(acc),
        'recall'     : float(recall),
        'precision'  : float(precision),
        'f1'         : float(f1_score),
        'auc_roc'    : float(roc_auc),
        'n_pratiche' : int(P.size),
        'soglia'     : float(soglia)
    }


rng = np.random.default_rng(0)
y = rng.integers(0, 2, size=(200, ))
p_random = rng.uniform(0, 1, size=(200, ))
P_perfetta = y.astype(float) * 0.99 + 0.005
P_pessima  = 1.0 - P_perfetta

arr = [p_random, P_perfetta, P_pessima]
labels = ["random", "perfetta", "pessima"]
report= []
for l, p in zip(labels, arr):
    modello = valuta_modello_completo(p, y)
    modello['label'] = l
    report.append(modello)

data_report = pd.DataFrame(report)
print(data_report)   

# ==========================================================================
# CHECKPOINT FINALE (auto-verifica)
# ==========================================================================

# C1) In 1 frase: cos'e' la LOSS e perche' minimizziamo lei e non l'accuracy?
# TUA RISPOSTA:
# ...clear


# C2) Hai p=0.99 e y=1: BCE quanto vale circa? E con p=0.01 e y=1?
#     (puoi rispondere a occhio guardando `figures/03_01_bce_loss.png`)
# TUA RISPOSTA:
# ...

# C3) [Recall cap.02 M3] In 1 riga: cos'e' la sigmoid? E perche' la usiamo
#     SOLO nell'ultimo layer (e non in tutti i layer)?
# TUA RISPOSTA:
# ...

# C4) [Prevedi output] Dato un dataset con 100 pratiche, di cui 30 positive
#     (y=1) e 70 negative (y=0), e una rete che predice SEMPRE P = 0.3
#     (cioe' prevede sempre "30% probabilita' alterato"):
#     - accuracy con soglia 0.5 = ?
#     - bce_loss ~ ?
#     Spiega entrambi in 2 righe.
# TUA RISPOSTA:
# ...

# C5) Auto-rating onesto (compila in chiusura capitolo):
#       - LOSS vs ACCURACY (derivabile vs discreta):     /10
#       - BCE formula + interpretazione:                  /10
#       - BCE vs MSE - 2 ragioni:                         /10
#       - clip bilaterale (perche' eps e 1-eps):          /10
#       - soglia 0.5 (perche' non > 0):                   /10
#       - pipeline integrata (forward + loss + metriche): /10
# TUE RISPOSTE:
# ...


# ==========================================================================
# SOLUZIONI QUIZ (NON BARARE - leggi solo dopo aver risposto)
# ==========================================================================
"""
QUIZ D'INGRESSO

Q1) LOSS: numero che misura quanto la rete sbaglia, su scala continua e
    DERIVABILE. ACCURACY: percentuale di predizioni corrette, discreta.
    Importante per backprop: la loss e' derivabile (puoi calcolarne il
    gradiente rispetto ai pesi), l'accuracy no -> con accuracy il
    backprop non potrebbe nemmeno partire.

Q2) In x = 3 la curva x^2 e' in salita (pendenza positiva). In x = -3
    e' in discesa (pendenza negativa). La parabola "scende fino allo
    zero e poi risale" -> a sinistra di 0 pendenza negativa, a destra
    positiva. (Vedremo nel cap.04 che la derivata di x^2 e' 2x.)

Q3) Errore intuitivo: la rete ha previsto "quasi sicuro genuino" (0.05)
    quando era alterato. Errore grande, BCE alta. Direzione pesi:
    spingere in modo da FAR ALZARE p su questa pratica. (Attenzione:
    alcuni pesi salgono e altri scendono a seconda del segno delle
    feature - lo vedrai nel cap.05/06 con la chain rule.)

Q4) W1: 4*8 = 32. b1: 8. W2: 8*1 = 8. b2: 1. Totale 32+8+8+1 = 49 parametri.

Q5) Esempio: "Provi il modello su N esempi. Confronti la sua risposta
    con quella vera. Misuri quanto sbaglia. Aggiusti le manopole interne
    per sbagliare meno. Ripeti finche' migliora."


MINI-ESERCIZI INLINE

1.1.A) y=1 p=0.8 -> -log(0.8) = 0.223
       y=1 p=0.2 -> -log(0.2) = 1.609
       y=0 p=0.8 -> -log(0.2) = 1.609
       y=0 p=0.2 -> -log(0.8) = 0.223
       I 2 casi sbagliati danno 1.609; i 2 giusti danno 0.223.

1.1.B) Sostituendo: y=1 -> 1*log(p) + 0*log(1-p) = log(p) -> -log(p).
       y=0 -> 0*log(p) + 1*log(1-p) = log(1-p) -> -log(1-p).

1.1.C) bce_loss([0.8], [1]) ~ 0.223. bce_loss([0.5], [1]) ~ 0.693.
       bce_loss([0.5], [0]) ~ 0.693. p=0.5 -> BCE = log(2) sempre,
       sia che y=0 sia che y=1 -> "tiepido".

1.2.A) Senza clip: y=1 p=0 -> -log(0) = +inf; y=0 p=1 -> -log(0) = +inf.
       Con bce_loss (clip eps, 1-eps): valori grandi ma finiti (~ 27.6).

1.3.A) y=1 p=0.6 -> -log(0.6) = 0.51 -> circa (b) 0.5.
       y=0 p=0.9 -> -log(0.1) = 2.30 -> circa (d) 2.5.

1.4.A) loss singole: ~[0.105, 0.105, 0.223, 1.204, 2.996].
       loss media ~ 0.927. Argmax = 4 (pratica con p=0.05 y=1).

2.1.A) Con y=0: BCE = -log(1-p). Esplode quando p -> 1.
       MSE = p^2 limitato a 1 anche per p=0.99.

2.2.A) BCE(y=1, p) = -log(p) = 1.0 quando p = 1/e ~ 0.368.
       BCE = 5.0 quando p = e^-5 ~ 0.0067.

3.1.A) y_pred1 = [1,1,1,1] -> acc = 0.5 (50% dataset bilanciato).
       y_pred2 = [0,0,1,1] -> acc = 1.0 (corretto).

3.1.B) soglia 0.3 -> y_pred = [0,1,1,1] -> acc = 0.75.
       soglia 0.5 -> y_pred = [0,0,1,1] -> acc = 1.0.
       soglia 0.7 -> y_pred = [0,0,0,1] -> acc = 0.75.
       (soglia 0.5 ottimale per QUESTO dataset; cambia se i costi
       di FP/FN sono asimmetrici.)

3.2.A) accuracy 0.5: in 2 casi P >= 0.5 ma y=0 e in 2 casi P < 0.5 ma y=1
       (caso peggiore - ranking sbagliato). In realta':
       y_pred = [0,0,1,1] vs y=[0,1,0,1] -> 2/4 = 0.5.
       AUC su P (continuo): 3/4 coppie positivi sopra negativi = 0.75.
       AUC su binari [0,0,1,1]: degenera a 0.5 (collassa info di ranking).


QUIZ DI VERIFICA

V1) Loss = numero continuo che misura quanto le predizioni si discostano
    dalla verita'. Minimizziamo lei e non l'accuracy perche' e' DERIVABILE:
    il backprop puo' calcolare gradienti su ogni peso. L'accuracy e' a
    scalini (0 o 1 per pratica) -> derivata zero quasi ovunque.

V2) BCE invece dell'MSE perche':
    (1) la BCE punisce in modo "infinito" gli errori clamorosi
        (sicurezza sbagliata) -> spinge la rete a NON essere "sicurissima
        ma errata".
    (2) la derivata di BCE + sigmoid si semplifica in (p - y), facile e
        stabile da calcolare (lo vedrai nel cap.06).

V3) DUE bug:
    (a) clip NON BILATERALE: np.clip(p, eps, 1) protegge solo lato basso.
        Quando y=0 e p=1: log(1-p) = log(0) = -inf. Servirebbe (eps, 1-eps).
    (b) SEGNO sbagliato: BCE ha "- y*log(p) - (1-y)*log(1-p)". Senza il "-"
        davanti la "loss" sarebbe NEGATIVA (log(p) e log(1-p) sono <= 0).

V4) Il clip taglia p lontano da 0 e 1 per evitare log(0) = -inf
    (e 0*log(0) = NaN in NumPy). DEVE essere bilaterale perche' la BCE
    usa SIA log(p) (esplode se p=0) SIA log(1-p) (esplode se p=1).

V5) y_pred con soglia 0.5: [0, 0, 1, 1]. Confronto con y=[0,1,0,1]:
    corretti in posizione 0 e 3, sbagliati in 1 e 2 -> accuracy = 0.5.
    Usiamo 0.5 perche' la sigmoid produce P in (0, 1) (P>0 sempre True):
    0.5 e' la soglia NEUTRA, equidistante dai due estremi.

V6) Esempio: "Hai un controllo qualita' che dice 'questo prodotto e'
    buono al X%'. Se dichiari 99% buono e in realta' era ottimo, hai
    sbagliato poco. Se dichiari 1% buono e in realta' era ottimo, hai
    sbagliato malissimo. La BCE da' un voto basso al primo caso e
    altissimo al secondo - cosi' il tuo controllo impara a 'sparare
    numeri' coerenti con la verita'."

V7) bce_loss(p, y) ~ 0.01 (3 predizioni quasi perfette).
    accuracy_score(p, y) = 1.0 (tutte e 3 corrette con soglia 0.5).


CHECKPOINT FINALE

C1) Loss = misura continua e derivabile di quanto la rete sbaglia.
    La minimizziamo perche' e' derivabile -> calcoliamo il gradiente
    rispetto ai pesi e li aggiorniamo. L'accuracy non e' derivabile.

C2) p=0.99 y=1 -> BCE ~ 0.01 (quasi giusta).
    p=0.01 y=1 -> BCE ~ 4.6 (sicurissima sbagliata).
    Asimmetria: l'errore "sicurissimo sbagliato" pesa molto di piu'
    della predizione "tiepida" (p=0.5 -> BCE ~ 0.69).

C3) Sigmoid: 1 / (1 + e^-z). Mappa qualsiasi numero in (0, 1) -> e' una
    probabilita'. La usiamo SOLO nell'ultimo layer perche' a) ci serve
    una probabilita' come output, b) nei layer intermedi causerebbe
    "vanishing gradient" (lo vediamo al cap.04: derivata sigmoid <= 0.25).

C4) accuracy con soglia 0.5: rete prevede sempre 0.3 -> y_pred = sempre 0.
    Ha y_pred=0 ed e' corretta per le 70 negative -> accuracy = 0.70.
    bce_loss: media di -log(0.3) sui positivi (30/100 * 1.20) e
    -log(0.7) sui negativi (70/100 * 0.36). Totale ~ 0.61.
    Lezione: accuracy puo' SEMBRARE alta solo perche' il dataset e'
    sbilanciato, ma la BCE ti dice che la rete e' tutt'altro che brava.
"""


# ==========================================================================
# NOTE PER IL CAPITOLO SUCCESSIVO (cap.04 derivate_gradiente)
# ==========================================================================
#
# Cosa porti via da qui:
#   - bce_loss, mse_loss, accuracy_score (funzioni in alto)
#   - sigmoid, relu stabili (le riuserai)
#   - 3 anti-pattern chiusi: segno BCE, clip bilaterale, soglia 0.5
#   - una pipeline di valutazione modello completa
#
# Cosa NON sai ancora (e va bene cosi'):
#   - non sai derivare la BCE - cap.04 (e la cosa miracolosa al cap.05)
#   - non sai cosa sia un "gradiente" - cap.04
#   - non sai come "correggere" i pesi - cap.05
#
# Prima di aprire il cap.04, fai il bridge ripasso:
#   modulo_03_dl_cv/quiz_ripasso_tra_capitoli/
#       M03_R03_after_C03_before_C04_loss_to_derivate.md


# ==========================================================================
# ENTRY POINT
# ==========================================================================
if __name__ == "__main__":
    print("=" * 70)
    print("Cap.03 M3 - LOSS - demo di riferimento")
    print("=" * 70)

    print("\n[Demo 2.1 - BCE vs MSE su predizioni con y=1]")
    _confronto_bce_mse()

    print("\n[Demo 1.3 - Genero il grafico BCE in figures/03_01_bce_loss.png]")
    figures_dir = os.path.join(os.path.dirname(__file__), "figures")
    _grafico_bce(out_path=os.path.join(figures_dir, "03_01_bce_loss.png"))
    print(f"  -> {figures_dir}/03_01_bce_loss.png")

    print("\n" + "=" * 70)
    print("Demo finite. Adesso tocca a te:")
    print("  - 12 mini-esercizi inline (sezioni 1, 2, 3)")
    print("  - 3 TODO base (gia' migrati)")
    print("  - 4 TODO recall cap.01-02 M3 (4.1-4.4)")
    print("  - 3 TODO lacune emerse (5.1-5.3)")
    print("  - 1 pipeline integrata (PIPE.1)")
    print("  - 6 TODO tipologie (colloquio/refactor/debug/retrieval/...)")
    print("  - 7 quiz di verifica + mini-progetto + checkpoint")
    print("Quando vuoi una valutazione: 'valuta cap.03 M3 sezione X.Y'.")
    print("=" * 70)
