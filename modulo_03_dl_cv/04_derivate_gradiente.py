"""
============================================================================
MODULO 3 (DL & CV) - CAPITOLO 04
"DERIVATE e GRADIENTE": il linguaggio della correzione
============================================================================

Secondo dei 4 sotto-capitoli del vecchio "Backpropagation". Mappa:

    03_loss.py                  (loss BCE, MSE)               ← FATTO
    04_derivate_gradiente.py    ← QUESTO FILE
    05_chain_rule_gd.py         (chain rule + gradient descent)
    06_backprop_training.py     (backward 2-layer + training loop)

Filosofia (richiesta studente): tanti esercizi pratici, pipeline complete,
richiami forti ai capitoli precedenti DI QUESTO MODULO (cap.01, 02, 03 M3).

----------------------------------------------------------------------------
DA DOVE ARRIVI (cap.03 LOSS)
----------------------------------------------------------------------------
Hai una rete 2-layer (cap.02) che produce P (probabilita') e sai
misurare quanto sbaglia con la BCE (cap.03):

       loss = bce_loss(P, y)     # numero >= 0

Domanda chiave: COME usiamo questo numero per CORREGGERE i pesi?
Risposta breve: serve sapere "se sposto un peso di poco, la loss
scende o sale, e di quanto?". Quello e' una DERIVATA.

Questo capitolo introduce:
  1) Derivata come pendenza (in 1 variabile) -> Sez. 1
  2) Derivata della sigmoid e della ReLU      -> Sez. 2-3
  3) Gradiente = vettore di derivate parziali -> Sez. 4
  4) Derivata della BCE rispetto a p e rispetto al logit z (semplifica!)
                                              -> Sez. 5

NON facciamo ancora chain rule "vera" (cap.05) ne' backprop su rete (cap.06).

----------------------------------------------------------------------------
DEFINITION OF DONE (cap.04)
----------------------------------------------------------------------------
Alla fine sai rispondere in 1 riga + in CODICE a:

  1) Cos'e' una DERIVATA (parla di pendenza, NIENTE limiti)?
  2) Cos'e' la DERIVATA PARZIALE (e perche' "parziale")?
  3) Cos'e' il GRADIENTE come "vettore di derivate parziali"?
  4) Quanto vale la derivata della SIGMOID in z=0 (e perche' max 0.25)?
  5) Quanto vale la derivata della BCE rispetto a p? E rispetto a z?
  6) Perche' nella combinazione "BCE + sigmoid" la derivata si semplifica
     in (p - y)?

Hai aggiunto al "toolkit" 4 funzioni riutilizzabili:

  - derivata_numerica   (sanity check per derivate analitiche)
  - gradiente_numerico  (una derivata parziale per coordinata)
  - derivata_sigmoid    (analitica: s(z) * (1 - s(z)))
  - derivata_relu       (analitica: 1 se z > 0, 0 se z <= 0)

----------------------------------------------------------------------------
MAPPA DEL CAPITOLO
----------------------------------------------------------------------------
   *  PRONTUARIO TRANELLI                       [D1] - [D5]
   *  QUIZ D'INGRESSO                           Q1 - Q6
   *  SEZIONE 1  Derivata come pendenza         1.1 - 1.3
                  con 4 mini-esercizi inline
   *  SEZIONE 2  Derivata della SIGMOID         2.1 - 2.2
                  con 3 mini-esercizi inline
   *  SEZIONE 3  Derivata della ReLU            3.1 - 3.2
                  con 2 mini-esercizi inline
   *  SEZIONE 4  Gradiente (multivariato)       4.1 - 4.3
                  con 4 mini-esercizi inline
   *  SEZIONE 5  Derivata della BCE             5.1 - 5.3
                  (rispetto a p, rispetto a z, semplificazione)
                  con 3 mini-esercizi inline
   *  TODO MIRATI BASE                          TODO 1 - 6
   *  PIPELINE INTEGRATA                        derivate_check_completo()
                  Verifica numerica vs analitica su sigmoid/relu/bce
   *  RINFORZI CAP.01-03 M3                     TODO 7 - 10
   *  TIPOLOGIE STANDARD                        TODO 11 - 16
                  COLLOQUIO, REFACTORING, DEBUG, RETRIEVAL,
                  INTERLEAVING, REAL-WORLD
   *  QUIZ DI VERIFICA                          V1 - V8
   *  MINI-PROGETTO FINALE                      analizza_funzione_attivazione()
   *  CHECKPOINT FINALE                         C1 - C5
   *  SOLUZIONI                                 in fondo

Conta esercizi: ~16 mini-inline + 16 TODO numerati + 1 pipeline + 1 mini-progetto.

----------------------------------------------------------------------------
COME USARE QUESTO FILE
----------------------------------------------------------------------------
Identico a tutti i capitoli M3:
  1. Leggi in ordine. Mini-esercizi inline = sale.
  2. TODO numerati = piatti principali.
  3. Pipeline / mini-progetto = consolidamento.
  4. "valuta cap.04 M3 sezione X" quando vuoi correzione.
  5. "ho finito cap.04 M3" -> chiusura + voto.
"""

import os
from typing import Callable

import numpy as np
import matplotlib.pyplot as plt
from numpy.typing import NDArray


# ==========================================================================
# FUNZIONI RIUTILIZZABILI (riprese dal cap.03 + nuove di questo capitolo)
# ==========================================================================

# Funzioni dal cap.03 (le ridefinisco qui per autosufficienza del file)

def sigmoid(z: NDArray[np.float64] | float) -> NDArray[np.float64] | float:
    """Sigmoid stabile. Recall cap.01/02 M3."""
    z_arr = np.asarray(z, dtype=float)
    z_safe = np.clip(z_arr, -500.0, 500.0)
    out = 1.0 / (1.0 + np.exp(-z_safe))
    if np.isscalar(z):
        return float(out)
    return out


def relu(z: NDArray[np.float64]) -> NDArray[np.float64]:
    """ReLU: max(0, z). Recall cap.02 M3."""
    return np.maximum(0.0, z)


def bce_loss(
    p: NDArray[np.float64],
    y: NDArray[np.int64] | NDArray[np.float64],
    eps: float = 1e-12,
) -> float:
    """BCE media. Recall cap.03 LOSS."""
    p_safe = np.clip(p, eps, 1.0 - eps)
    loss = - y * np.log(p_safe) - (1.0 - y) * np.log(1.0 - p_safe)
    return float(np.mean(loss))


# Nuove di questo capitolo

def derivata_numerica(
    f: Callable[[float], float],
    x: float,
    h: float = 1e-6,
) -> float:
    """Derivata numerica via differenza centrata: (f(x+h) - f(x-h)) / (2h).

    Sanity check per derivate analitiche. Per h piccolo (1e-6) coincide
    con la derivata analitica fino a ~6 cifre decimali per funzioni
    "normali" (no salti, no esplosioni).
    """
    return (f(x + h) - f(x - h)) / (2.0 * h)


def derivata_sigmoid(z: NDArray[np.float64] | float) -> NDArray[np.float64] | float:
    """Derivata della sigmoid: s(z) * (1 - s(z)). Massima in z=0 (=0.25)."""
    s = sigmoid(z)
    return s * (1.0 - s)


def derivata_relu(z: NDArray[np.float64] | float) -> NDArray[np.float64] | float:
    """Derivata di ReLU: 1 se z > 0, 0 se z <= 0. Step function.

    NOTA: in z=0 la derivata e' tecnicamente indefinita; per convenzione
    si prende 0 (alcune librerie usano 0.5; PyTorch usa 0).
    """
    z_arr = np.asarray(z, dtype=float)
    out = (z_arr > 0).astype(float)
    if np.isscalar(z):
        return float(out)
    return out


def gradiente_numerico(
    f: Callable[[NDArray[np.float64]], float],
    x: NDArray[np.float64],
    h: float = 1e-6,
) -> NDArray[np.float64]:
    """Gradiente numerico via differenza centrata, una coordinata alla volta.

    Per ogni i: muove SOLO x[i] di +h e di -h, calcola f, e fa la
    derivata parziale. Ripete per tutte le coordinate.

    ATTENZIONE: scala O(N) chiamate di f -> lentissimo per reti vere
    (milioni di parametri). Lo usiamo solo come SANITY CHECK; in
    produzione si usa il backprop (cap.06).
    """
    grad = np.zeros_like(x, dtype=float)
    for i in range(x.size):
        xp = x.copy(); xp.flat[i] += h
        xm = x.copy(); xm.flat[i] -= h
        grad.flat[i] = (f(xp) - f(xm)) / (2.0 * h)
    return grad


# ==========================================================================
# PRONTUARIO TRANELLI - 5 minuti
# ==========================================================================
#
# [D1] DERIVATA = PENDENZA. Non e' un limite, e' il numero che ti dice
#      "se aumento x di un filo, di quanto cambia f(x)".
#      In codice (sanity check): (f(x+h) - f(x-h)) / (2h) con h piccolo.
#
# [D2] DERIVATA PARZIALE: stessa cosa, ma in una funzione di piu' variabili.
#      Df/Dx_i = "se muovo SOLO x_i, lasciando le altre ferme, di quanto
#      cambia f?". "Parziale" perche' guardi una variabile alla volta.
#
# [D3] GRADIENTE = vettore di derivate parziali, una per ogni variabile.
#      grad f = [Df/Dx_1, Df/Dx_2, ..., Df/Dx_n].
#      Geometricamente: punta nella direzione di MAGGIORE CRESCITA.
#      Per minimizzare -> direzione opposta (-grad). Lo vediamo al cap.05.
#
# [D4] DERIVATA SIGMOID = s(z) * (1 - s(z)). Massima in z=0 (=0.25).
#      Implicazione: se hai TANTI layer con sigmoid, il gradiente
#      "evapora" (vanishing gradient). E' uno dei motivi per cui in DL
#      moderno si usa ReLU nei layer interni e sigmoid solo all'output.
#
# [D5] SEMPLIFICAZIONE MIRACOLOSA "BCE + sigmoid":
#      Se p = sigmoid(z), la derivata della BCE(p, y) rispetto a z e':
#               dL/dz = p - y
#      Niente derivata della sigmoid da moltiplicare. PuLito e stabile.
#      E' uno dei motivi per cui la coppia "sigmoid + BCE" e' lo
#      standard per classificazione binaria.


# ==========================================================================
# QUIZ D'INGRESSO - cerniera cap.03 LOSS -> cap.04 DERIVATE
# ==========================================================================

# Q1) [Recall cap.03] Cos'e' la BCE in 1 riga? E perche' minimizziamo
#     la loss invece dell'accuracy?
# TUA RISPOSTA:
# la BCE è un tipo di loss che viene utilizzato in classificazione binaria, e la sua formula tende a far esplodere gli errori di grande entità. Rispetto all'accuracy che ci indica solo quanto sbaglia la rete in termini generali, ci dice anche quanto gravemente sbaglia, perchè punisce in maniera esponenziale gli errori man mano che diventano più gravi.

# Q2) [Recall cap.03] Perche' la BCE usa un CLIP BILATERALE (eps, 1-eps)?
#     Cosa succederebbe senza il lato destro?
# TUA RISPOSTA:
# Usa la clip laterale per proteggere gli estremi. Senza il lato destro, potremmo passare p = 1 e ricevere come risultato nan.

# Q3) [Recall cap.02 M3] In 1 riga: cos'e' un "layer dense"? E come
#     calcolerai il forward di una rete 2-layer in NumPy?
# TUA RISPOSTA:
# layer dense significa "densamente connessa", ossia ogni neaurone legge tutti gli input del layer precedente. il forward di una rete a due livelli prevede un livello con operazione matriciale + bias tra feature e pesi, poi funzione di attivazione (relu), e un secondo livello di output con prodotto matriciale del output del relu con altri pesi e bias, e infine funzione sigmoide per avere delle probabilità.

# Z1 = X @ W1 + b1 -> H = relu(Z1) -> Z2 = H @ W2 + b2 -> P = sigmoid(Z2)


# Q4) [Intuizione - prossima sezione] Hai f(x) = x^2 e ti sposti da x=2
#     a x=2.001 (un passo piccolissimo a destra). f(x) sale o scende?
#     Di QUANTO circa? Stima ad occhio.
# TUA RISPOSTA: Sale, di circa 0,004
# 

# Q5) [💬 Feynman] Spiega in 3 righe cos'e' una "pendenza" a un collega
#     web dev. Senza usare derivate / limiti / matematica simbolica.
#     Suggerimento: analogie con grafici di sviluppo (CPU usage che sale,
#     load time che scende, ecc.).
# TUA RISPOSTA:
# La pendenza è il guadagno o la perdita di altezza sulla asse y rispetto a un piccolo spostamento del valore di partenza sull'asse x. In pratica, se mi sposto un po più avanti o indietro lungo questa traiettoria, quanto mi muovo verso l'alto o verso il basso?

# Q6) [Prevedi output] Cosa stampa questo codice?
#       def f(x):
#           return x ** 3
#       h = 1e-6
#       deriv_approx = (f(2 + h) - f(2 - h)) / (2 * h)
#       print(round(deriv_approx, 1))
# TUA RISPOSTA:
# (Suggerimento: la derivata di x^3 e' 3*x^2; in x=2 vale 3*4 = 12.)

# restituisce round((8,012006001 - 7,98800599) / 0,002, 1) = 12.0


# ==========================================================================
# SEZIONE 1 - DERIVATA come pendenza
# ==========================================================================
#
# ANALOGIA: sei in macchina su una strada. Il TACHIMETRO ti dice quanti
# km/h fai. La pendenza della strada (= "quanti metri sali per ogni metro
# avanzato") e' la DERIVATA della funzione "altezza vs distanza".
#
# Definizione operativa (niente limiti):
#       derivata di f in x = "se aumento x di un filo h, di quanto
#                             cambia f? (la differenza diviso h)"
#
# In codice (differenza CENTRATA - piu' precisa di quella avanti):
#       derivata_numerica(f, x, h) = (f(x+h) - f(x-h)) / (2*h)
#
# Per h piccolo (1e-6) coincide con la derivata analitica fino a ~6 cifre.


# 1.1 - DERIVATA NUMERICA in azione

# 🔵 MINI-ESERCIZIO INLINE 1.1.A (~3 minuti) — applica derivata_numerica
# Usa la funzione `derivata_numerica` definita in alto per calcolare la
# derivata di f(x) = x^2 in:
#   - x = 3   (atteso ~6.0)
#   - x = -3  (atteso ~-6.0)
#   - x = 0   (atteso ~0.0)
# TUO CODICE QUI:

print("\nMini-esercizio in-line 1.1.A")
def f(x):
    return x ** 2

x = 3
print(f"f'(x) di x = 3  -> {derivata_numerica(f, x)}")
x = -3
print(f"f'(x) di x = -3 -> {derivata_numerica(f, x)}")
x = 0
print(f"f'(x) di x = 0  -> {derivata_numerica(f, x)}")

# 🔵 MINI-ESERCIZIO INLINE 1.1.B (~3 minuti) — pendenza di una retta
# Una retta y = 3x + 1 ha pendenza costante = 3.
# Verifica con derivata_numerica in 3 punti diversi (x=0, x=5, x=-10).
# Tutti devono dare 3.0.
# TUO CODICE QUI:

print("\nMini-esercizio in-line 1.1.B\n")

def f_y(x):
    return 3 * x + 1

x = 0
der_1 = derivata_numerica(f_y, x)
print(f"{round(derivata_numerica(f_y, x), 1)}")
x = 5
der_2 = derivata_numerica(f_y, x)
print(f"{round(derivata_numerica(f_y, x), 1)}")
x = -10
der_3 = derivata_numerica(f_y, x)
print(f"{round(derivata_numerica(f_y, x), 1)}")

arr = np.array([der_1, der_2, der_3])
target = 3.0

assert np.all(np.isclose(arr, target)), "Ops qualcosa è andato storto!"


# 1.2 - DERIVATA NUMERICA vs DERIVATA ANALITICA
#
# Quando hai una formula chiusa per la derivata (es. f(x) = x^2 -> f'(x) = 2x),
# puoi confrontare con la derivata numerica per "verificare". E' il sanity
# check che useremo nel cap.06 per smascherare bug nel backward.

# 🔵 MINI-ESERCIZIO INLINE 1.2.A (~5 minuti) — confronto su 3 funzioni
# Per ognuna di queste funzioni, calcola in 3 punti la derivata numerica
# e quella analitica. Devono coincidere a meno di 1e-4.
#   1) f(x) = x^3                 ->  f'(x) = 3 * x^2
#   2) f(x) = sin(x)              ->  f'(x) = cos(x)
#   3) f(x) = np.exp(x)           ->  f'(x) = np.exp(x)
# Usa np.isclose(num, ana, atol=1e-4) per confermare ogni confronto.
# TUO CODICE QUI:

print("\nMini-esercizio in-line 1.2.A\n")

def f_cubo(x) -> tuple[float, float]:
    der_num = derivata_numerica(lambda x: x ** 3, x)
    der_ana = 3 * (x ** 2)
    if not np.isclose(der_num, der_ana, atol=1e-4):
        raise ValueError("Derivata numerica e analitica non combaciano")
    return (float(der_num), float(der_ana))
    

def f_seno(x):
    der_num = derivata_numerica(lambda x: np.sin(x), x)
    der_ana = np.cos(x)
    if not np.isclose(der_num, der_ana, atol=1e-4):
        raise ValueError("Derivata numerica e analitica non combaciano")
    return (float(der_num), float(der_ana))

def f_exp(x):
    der_num = derivata_numerica(lambda x: np.exp(x), x)
    der_ana = np.exp(x)
    if not np.isclose(der_num, der_ana, atol=1e-4):
        raise ValueError("Derivata numerica e analitica non combaciano")
    return (float(der_num), float(der_ana))

arr = np.array([-3, 0, 3])

for a in arr:
    print(f"\nDerivate per x = {a}")
    print(f_cubo(a))
    print(f_seno(a))
    print(f"{f_exp(a)}\n")
    

# 1.3 - VISUALIZZAZIONE: funzione + tangente


def _grafico_funzione_e_tangenti(
    out_path: str | None = None,
    show: bool = False,
) -> None:
    """f(x) = x^2 con tangenti (derivata) in 5 punti. Mostra che la derivata
    e' la PENDENZA della tangente."""
    x = np.linspace(-3, 3, 200)
    y = x ** 2
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.plot(x, y, label="f(x) = x²", color="#1f77b4")
    # 5 punti con tangenti
    punti = [-2, -1, 0, 1, 2]
    for x0 in punti:
        y0 = x0 ** 2
        m = 2 * x0  # derivata analitica
        # retta tangente: y = m * (x - x0) + y0
        x_tan = np.linspace(x0 - 1, x0 + 1, 30)
        y_tan = m * (x_tan - x0) + y0
        ax.plot(x_tan, y_tan, "--", alpha=0.7,
                label=f"tang. in x={x0}, pend.={m}")
        ax.plot(x0, y0, "o", markersize=8)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title("f(x) = x² e tangenti (derivata = pendenza della tangente)")
    ax.legend(loc="upper center", fontsize=8)
    ax.grid(True, alpha=0.3)
    ax.set_ylim(-1, 12)
    if out_path:
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        fig.savefig(out_path, dpi=120, bbox_inches="tight")
    if show:
        plt.show()
    plt.close(fig)



# 🔵 MINI-ESERCIZIO INLINE 1.3.A (~3 minuti) — genera grafico tangenti
# Chiama _grafico_funzione_e_tangenti(out_path="figures/04_01_tangenti.png")
# e verifica che il file esista (assert os.path.exists).
# TUO CODICE QUI:

# _grafico_funzione_e_tangenti(out_path="figures/04_01_tangenti.png")
# assert os.path.exists(os.path.join(os.path.dirname(__file__), "figures/04_01_tangenti.png")), "Ops, il grafico non è stato creato!"

# 🔵 MINI-ESERCIZIO INLINE 1.3.B (~2 minuti) — interpreta dal grafico
# Guardando il grafico generato, rispondi (commento):
#   1) In quale punto la pendenza e' nulla (= "fondo della valle")? -> 
#   2) Da quel punto, in che direzione devi muoverti per FAR SCENDERE -> 
#      f(x)? (suggerimento: una trick question - sei gia' al minimo)
# TUO COMMENTO QUI:
# La pendenza è nulla in x = 0 e non è possibile far scendere ulteriormente il valore di f(x), perchè se anche ci spostassimo verso sinistra entrando nei valori negativi, la funzione di x ricomincerebbe a salire.

def _grafico_funzione_e_tangenti(
    out_path: str | None = None,
    show: bool = False,
) -> None:
    """f(x) = x^2 con tangenti (derivata) in 5 punti. Mostra che la derivata
    e' la PENDENZA della tangente."""
    x = np.linspace(-3, 3, 200)
    y = x ** 2
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.plot(x, y, label="f(x) = x²", color="#1f77b4")
    # 5 punti con tangenti
    punti = [-2, -1, 0, 1, 2]
    for x0 in punti:
        y0 = x0 ** 2
        m = 2 * x0  # derivata analitica
        # retta tangente: y = m * (x - x0) + y0
        x_tan = np.linspace(x0 - 1, x0 + 1, 30)
        y_tan = m * (x_tan - x0) + y0
        ax.plot(x_tan, y_tan, "--", alpha=0.7,
                label=f"tang. in x={x0}, pend.={m}")
        ax.plot(x0, y0, "o", markersize=8)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title("f(x) = x² e tangenti (derivata = pendenza della tangente)")
    ax.legend(loc="upper center", fontsize=8)
    ax.grid(True, alpha=0.3)
    ax.set_ylim(-1, 12)
    if out_path:
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        fig.savefig(out_path, dpi=120, bbox_inches="tight")
    if show:
        plt.show()
    plt.close(fig)

# ==========================================================================
# SEZIONE 2 - Derivata della SIGMOID
# ==========================================================================
#
# 🔁 RINFORZO MIRATO — Vanishing gradient (lacuna checkpoint C3 cap.03 LOSS)
# Al checkpoint C3 hai spiegato bene l'output probabilistico, ma mancava il
# motivo "tecnico" per NON usare sigmoid nei layer nascosti:
#   s'(z) = s(z) * (1 - s(z))  →  MASSIMO 0.25 in z=0
# Con 4 layer sigmoid impilati, il gradiente può essere moltiplicato per
# ~0.25^4 ≈ 0.004 → training lentissimo. Per questo nel cap.02 usi ReLU
# al centro e sigmoid solo in uscita.
#
# Prova subito (commento, 2 righe):
# 1) Se s'(z) max = 0.25, quanto vale dopo 3 layer sigmoid (stima 0.25^3)?
# 2) Perché ReLU in hidden non ha questo tetto 0.25?
# TUO COMMENTO QUI:
#ReLU non ha questo effetto perchè non trasforma i valori, ma spegne solo i neuroni che riportano valori inferiori di 0. Le informazioni (valori) maggiori di 0 non vengono alterati e passano direttamente al layer successivo. Se utilizzassimo sigmoid nei layer, perderemmo per ogni layer molte info per via della saturazione agli estremi.
#
# La sigmoid e' la funzione di output del cap.02 M3:
#       s(z) = 1 / (1 + e^-z)         z in R, output in (0, 1)
#
# Formula chiusa della derivata (DA SAPERE A MEMORIA, e' una delle 3
# formule "must" di tutto il DL classico):
#
#       s'(z) = s(z) * (1 - s(z))
#
# Proprieta' importanti:
#   - massima in z=0 (=0.25) -> implicazione "vanishing gradient"
#   - tende a 0 per |z| grande -> sigmoid "satura"
#
# (vedi `derivata_sigmoid` in alto)


# 2.1 - Verifica numerica della formula

# 🔵 MINI-ESERCIZIO INLINE 2.1.A (~5 minuti) — sigmoid vs sua derivata
# Per ogni z in [-3, -1, 0, 1, 3]:
#   1) num = derivata_numerica(sigmoid, z, h=1e-6)
#   2) ana = derivata_sigmoid(z)
#   3) assert np.isclose(num, ana, atol=1e-6)
#   4) stampa z, num, ana
# Quale z dà la derivata MASSIMA? (Suggerimento: z=0)
# TUO CODICE QUI:

print("Mini-esercizio in-line 2.1.A\n")

logits = np.array([-3, -1, 0, 1, 3])
report = {}
for z in logits:
    num = derivata_numerica(sigmoid, z, h=1e-6)
    ana = derivata_sigmoid(z)
    assert np.isclose(num, ana, atol=1e-6), "Derivata analitiva e numerica non coincidono!"
    report.update({str(z): ana})
    print(f"\nDerivata Sigmoide per z = {z}\n")
    print(f"Numerica: {round(num, 6)}")
    print(f"Analitica: {round(ana, 6)}")
print("\nValore massimo della derivata:")  
print(max(report.items(), key=lambda item: item[1]))


# 🔵 MINI-ESERCIZIO INLINE 2.1.B (~3 minuti) — massimo di s'(z)
# Dimostra (numericamente, con un grafico o con `argmax`):
# il massimo di derivata_sigmoid(z) e' 0.25 ed e' raggiunto in z=0.
#   1) Crea zz = np.linspace(-5, 5, 1000)
#   2) Calcola der = derivata_sigmoid(zz)
#   3) Stampa der.max() (~ 0.25) e zz[np.argmax(der)] (~ 0)
# TUO CODICE QUI:


# 2.2 - Implicazione del massimo 0.25 (vanishing gradient teaser)

# 🔵 MINI-ESERCIZIO INLINE 2.2.A (~3 minuti) — gradient "evapora"
# Se hai una rete con 5 layer di sigmoid impilati, il gradiente di un
# parametro del PRIMO layer (per la chain rule che vedremo al cap.05)
# viene MOLTIPLICATO per la derivata sigmoid di OGNI layer.
# Stima il massimo possibile dopo 5 moltiplicazioni:
#   gradiente_massimo = 0.25 ** 5
# Stampa il valore. Cosa noti? Per questo si usa ReLU nei layer interni.
# TUO CODICE QUI:


# ==========================================================================
# SEZIONE 3 - Derivata della ReLU
# ==========================================================================
#
# ReLU(z) = max(0, z)
# Derivata: 1 se z > 0, 0 se z < 0. In z=0 e' "indefinita" -> convenzione 0.
# (vedi `derivata_relu` in alto)
#
# Quindi la derivata di ReLU e' una STEP FUNCTION. Implicazioni:
#   - se z > 0: gradiente passa "intero" (moltiplicato per 1)
#   - se z <= 0: gradiente "muore" (moltiplicato per 0) -> "dying ReLU"
#
# Vantaggio rispetto a sigmoid: NIENTE vanishing gradient per z > 0
# (la derivata e' sempre 1, non 0.25). Da qui l'uso di ReLU nei layer
# interni in tutto il DL moderno.


# 3.1 - Verifica numerica della step function

# 🔵 MINI-ESERCIZIO INLINE 3.1.A (~3 minuti) — derivata_relu in 5 punti
# Per ogni z in [-2, -1, 0, 1, 2]:
#   1) num = derivata_numerica(relu, z, h=1e-6) ma ATTENZIONE: in z=0 la
#      derivata numerica puo' restituire 0.5 (perche' (relu(h) - relu(-h)) / 2h
#      = (h - 0) / 2h = 0.5). E' un problema della non-derivabilita' in 0.
#   2) ana = derivata_relu(z)
#   3) stampa z, num, ana. Commenta dove num e ana coincidono e dove no.
# TUO CODICE QUI:


# 3.2 - DYING ReLU teaser

# 🔵 MINI-ESERCIZIO INLINE 3.2.A (~3 minuti) — neurone "morto"
# Se in un layer ReLU TUTTI i z sono negativi (Z = X@W + b, supponi b
# molto negativo), allora H = ReLU(Z) e' tutto 0, e derivata_relu(Z) e'
# tutto 0. Il gradiente non passa -> il neurone non impara mai.
# Costruisci un esempio numerico:
#   X = np.array([[1.0, 2.0], [3.0, 4.0]])
#   W = np.array([[0.1], [0.2]])     # (2, 1)
#   b = np.array([-10.0])             # bias molto negativo
# Calcola Z = X @ W + b. Quanti elementi di Z sono > 0?
# Calcola anche derivata_relu(Z). Quanti sono 1.0?
# TUO CODICE QUI:


# ==========================================================================
# SEZIONE 4 - GRADIENTE (multivariato)
# ==========================================================================
#
# ANALOGIA: non sei piu' su una strada (1D), sei su un PRATO IN COLLINA
# (2D). In ogni punto hai DUE pendenze:
#   - pendenza verso EST (asse x)
#   - pendenza verso NORD (asse y)
# Il GRADIENTE in un punto e' un VETTORE [pendenza_x, pendenza_y].
# Punta nella direzione di MAGGIOR salita.
#
# In 3D, 4D, ... 1.000.000-D (= num parametri di una rete): stessa cosa,
# vettore con UNA componente per variabile.
#
# DERIVATA PARZIALE: muovi SOLO una variabile, le altre fisse.
#       df/dx_i = "se sposto SOLO x_i, di quanto cambia f?"
#
# Codice: gradiente_numerico(f, x) muove ogni componente di x una alla
# volta e fa la differenza centrata (vedi funzione in alto).


# 4.1 - GRADIENTE su un paraboloide

def _esempio_gradiente_2d() -> None:
    """f(x, y) = x^2 + y^2. In (3, 4) il gradiente analitico e' [2*3, 2*4] = [6, 8]."""
    f = lambda v: float(v[0] ** 2 + v[1] ** 2)
    x0 = np.array([3.0, 4.0])
    grad_num = gradiente_numerico(f, x0)
    grad_ana = np.array([2 * x0[0], 2 * x0[1]])
    print(f"x0 = {x0}")
    print(f"grad numerico:   {grad_num}")
    print(f"grad analitico:  {grad_ana}")
    print(f"differenza max:  {np.abs(grad_num - grad_ana).max():.2e}")


# 🔵 MINI-ESERCIZIO INLINE 4.1.A (~5 minuti) — applica gradiente_numerico
# Per ognuna di queste funzioni, calcola il gradiente in un punto e
# confronta con l'analitico (se lo sai):
#   1) f(x, y) = x^2 + y^2      in (1, -2)   -> atteso [2, -4]
#   2) f(x, y) = x * y          in (3, 5)    -> atteso [5, 3]
#   3) f(x, y, z) = x^2 + 2*y^2 + 3*z^2  in (1, 1, 1)  -> atteso [2, 4, 6]
# Stampa numerico e analitico per ognuno.
# TUO CODICE QUI:


# 4.2 - GRADIENTE punta in salita (visualizzazione)


def _grafico_campo_gradiente(
    out_path: str | None = None,
    show: bool = False,
) -> None:
    """Campo di gradienti per f(x, y) = x^2 + y^2 (paraboloide).
    Le frecce mostrano che il gradiente punta dal centro verso fuori."""
    # Contour della funzione
    x = np.linspace(-3, 3, 100)
    y = np.linspace(-3, 3, 100)
    X, Y = np.meshgrid(x, y)
    F = X ** 2 + Y ** 2
    # Gradienti su una griglia rada
    xs, ys = np.meshgrid(np.linspace(-2, 2, 8), np.linspace(-2, 2, 8))
    gx = 2 * xs
    gy = 2 * ys
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.contour(X, Y, F, levels=10, colors="gray", alpha=0.5)
    ax.quiver(xs, ys, gx, gy, color="#d62728", angles="xy",
              scale_units="xy", scale=8)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title("f(x, y) = x² + y²: gradiente punta verso fuori (salita)")
    ax.set_aspect("equal")
    ax.grid(True, alpha=0.3)
    if out_path:
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        fig.savefig(out_path, dpi=120, bbox_inches="tight")
    if show:
        plt.show()
    plt.close(fig)


# 🔵 MINI-ESERCIZIO INLINE 4.2.A (~3 minuti) — genera campo gradienti
# Chiama _grafico_campo_gradiente(out_path="figures/04_02_gradiente_2d.png")
# e verifica esistenza file.
# TUO CODICE QUI:


# 4.3 - DERIVATA PARZIALE = "muovi una variabile alla volta"

# 🔵 MINI-ESERCIZIO INLINE 4.3.A (~5 minuti) — derivate parziali a mano
# Per f(x, y) = x^2 * y + 3 * y + 2:
#   df/dx = ?     (tratti y come una costante)
#   df/dy = ?     (tratti x come una costante)
# Calcola "a mano" in commento. Poi verifica numericamente con
# gradiente_numerico in (x=1, y=2). Atteso: [2*1*2, 1^2 + 3] = [4, 4].
# TUO COMMENTO + CODICE QUI:


# 🔵 MINI-ESERCIZIO INLINE 4.3.B (~3 minuti) — gradiente come "lista coordinate"
# Spiega in 2 righe (commento) perche' il gradiente di una funzione di
# 3 variabili "vive" in R^3 (cioe' e' un vettore di 3 numeri).
# Suggerimento: una derivata parziale per ogni variabile.
# TUO COMMENTO QUI:


# ==========================================================================
# SEZIONE 5 - DERIVATA DELLA BCE (preparazione cap.05+06)
# ==========================================================================
#
# 🔁 RINFORZO MIRATO — Clip bilaterale + ordine bce_loss(p, y) (cap.03 LOSS)
# Pattern emersi nel cap.03: (1) clip `(eps, 1-eps)` prima dei log; (2) firma
# `bce_loss(p, y)` — prima probabilità, poi etichette.
#
# Prova subito (~3 min):
#   p = np.array([0.0, 1.0])
#   y = np.array([1, 0])
#   eps = 1e-12
#   1) Calcola BCE con clip solo (eps, 1) — cosa ottieni?
#   2) Calcola BCE con clip (eps, 1-eps) — valore finito?
#   3) Verifica che bce_loss(p, y) == bce_loss(y, p) → False (ordine conta!)
# TUO CODICE QUI:
#
# La BCE su una singola pratica:
#       L(p, y) = - y * log(p) - (1 - y) * log(1 - p)
#
# 5.1 - Derivata di L rispetto a p (per y fissato)
#
# Calcolo "a mano":
#       dL/dp = - y / p - (1 - y) * (-1) / (1 - p)
#             = - y / p + (1 - y) / (1 - p)
#             = (p - y) / (p * (1 - p))           [con qualche manipolazione]
#
# Verifichiamo numericamente.

# 🔵 MINI-ESERCIZIO INLINE 5.1.A (~5 minuti) — derivata BCE rispetto a p
# Per (p=0.8, y=1) calcola:
#   1) num: derivata_numerica(lambda p_var: -y * np.log(p_var) - (1-y) * np.log(1-p_var), p=0.8)
#      con y=1
#   2) ana: (p - y) / (p * (1 - p)) con p=0.8, y=1
#   3) confronta con np.isclose, atol=1e-4
# TUO CODICE QUI:


# 5.2 - SEMPLIFICAZIONE MIRACOLOSA: BCE + sigmoid -> derivata e' (p - y)
#
# Adesso il pezzo "geniale" del deep learning classico.
#
# Nel cap.02 hai visto:
#       z = X @ W + b           (logit)
#       p = sigmoid(z)          (probabilita')
#
# La loss alla fine e' L(p, y) = BCE.
# Vogliamo la derivata di L rispetto a z (NON a p).
# Applichiamo la chain rule (che vedremo formalmente al cap.05):
#       dL/dz = dL/dp * dp/dz
#
# Sostituiamo:
#   dL/dp = (p - y) / (p * (1 - p))            (sez. 5.1)
#   dp/dz = derivata_sigmoid(z) = p * (1 - p)  (sez. 2)
#
# Moltiplicando:
#   dL/dz = (p - y) / (p * (1 - p)) * p * (1 - p)
#         = (p - y)
#
# SEMPLIFICAZIONE MIRACOLOSA: i due "p*(1-p)" si elidono. Risultato pulito
# e numericamente stabile. Senza questa, dovresti calcolare separatamente
# derivata sigmoid e derivata BCE in ogni step -> overhead + instabilita'.
#
# Tradotto in codice (lo vedrai nel backward del cap.06):
#       dZ2 = P - y      # un solo passaggio, una sola riga di codice

# 🔵 MINI-ESERCIZIO INLINE 5.2.A (~8 minuti) — verifica numerica di "p - y"
# Per 5 valori di z:
#   z_vals = np.array([-3.0, -1.0, 0.0, 1.0, 3.0])
# Per ogni z (con y=1 fissato):
#   1) calcola p = sigmoid(z)
#   2) calcola num = derivata_numerica(lambda z_var: bce_loss(np.array([sigmoid(z_var)]), np.array([y])), z)
#   3) ana = p - y
#   4) verifica np.isclose(num, ana, atol=1e-3) per OGNI z
# Stampa una tabella z | p | num | ana | diff.
# Bonus: ripeti con y=0.
# TUO CODICE QUI:


# 5.3 - QUANDO la semplificazione NON vale

# 🔵 MINI-ESERCIZIO INLINE 5.3.A (~3 minuti) — funzione di attivazione diversa
# Cosa succede se invece di sigmoid usi un'altra funzione? La
# semplificazione "(p - y)" NON funziona piu'. Spiega in 2 righe perche':
# nel calcolo di dL/dz dovresti moltiplicare dL/dp per dp/dz, e dp/dz
# dipende dalla funzione di attivazione usata. Solo sigmoid + BCE
# producono la cancellazione magica.
# TUO COMMENTO QUI:


# ==========================================================================
# TODO MIRATI BASE (1 - 6)
# ==========================================================================

# TODO 1 (8 minuti) — derivata numerica vs analitica su 4 funzioni:
# Per ognuna, in 3 punti diversi, confronta derivata_numerica con la
# tua formula analitica. Devono coincidere a meno di 1e-4.
#   1) f(x) = x^4              ->  f'(x) = 4 * x^3
#   2) f(x) = 2 / x            ->  f'(x) = -2 / x^2
#   3) f(x) = np.log(x)        ->  f'(x) = 1 / x      (x > 0)
#   4) f(x) = sigmoid(x)       ->  f'(x) = sigmoid(x) * (1 - sigmoid(x))
# Stampa una tabella con i risultati.
# TUO CODICE QUI:


# TODO 2 (10 minuti) — grafico sigmoid + sua derivata sovrapposti
# Crea una funzione _grafico_sigmoid_e_derivata che:
#   - plot sigmoid(z) per z in [-6, 6]
#   - plot derivata_sigmoid(z) per z in [-6, 6]
#   - 2 curve nello stesso assi, label corretti, griglia
#   - salva in modulo_03_dl_cv/figures/04_03_sigmoid_derivata.png
# Chiamala. Verifica esistenza file.
# TUO CODICE QUI:


# TODO 3 (8 minuti) — grafico ReLU + sua derivata sovrapposti
# Stesso schema di TODO 2 ma per:
#   - plot relu(z)
#   - plot derivata_relu(z)
# Salva in figures/04_04_relu_derivata.png.
# Verifica esistenza file. Cosa noti graficamente sulla derivata? (step)
# TUO CODICE QUI:


# TODO 4 (10 minuti) — gradiente_numerico su una rete random
# Riprende il setup del cap.02 M3:
#   rng = np.random.default_rng(0)
#   X = rng.standard_normal((5, 3))
#   y = rng.integers(0, 2, size=5)
#   W1 = rng.standard_normal((3, 4)) * 0.1
#   b1 = np.zeros(4)
#   W2 = rng.standard_normal((4, 1)) * 0.1
#   b2 = np.zeros(1)
#
# Definisci una funzione f(W1_flat) che:
#   1) reshape W1_flat -> W1 di shape (3, 4)
#   2) forward 2-layer
#   3) ritorna bce_loss(P, y)
#
# Poi calcola il gradiente_numerico di f rispetto a W1_flat.
# Stampa la shape del gradiente e i primi 4 valori.
# TUO CODICE QUI:


# TODO 5 (5 minuti) — derivata della BCE su batch
# Per p = np.array([0.9, 0.1, 0.7]), y = np.array([1, 0, 1]):
#   - calcola dL/dp_i per ogni i (formula (p - y) / (p * (1 - p)))
#   - verifica con gradiente_numerico applicato a p (devi rendere p il
#     "vettore di variabili" rispetto a cui derivi)
# Stampa entrambi i vettori.
# TUO CODICE QUI:


# TODO 6 (5 minuti) — derivata della BCE rispetto al logit (semplificazione)
# Per z = np.array([-2.0, 0.0, 2.0]) e y = np.array([1, 0, 1]):
#   - calcola p = sigmoid(z)
#   - calcola dL/dz USANDO la semplificazione miracolosa: dL/dz = p - y
#   - verifica numericamente con gradiente_numerico applicato a z
# Stampa entrambi i vettori. Coincidono?
# TUO CODICE QUI:


# ==========================================================================
# PIPELINE INTEGRATA — `derivate_check_completo()`
# ==========================================================================
#
# OBIETTIVO: una sola funzione che verifica TUTTE le derivate analitiche
# (sigmoid, relu, BCE rispetto a p, BCE rispetto a z) confrontandole
# con quelle numeriche, e stampa una tabella riassuntiva. Sara' il
# "sanity check" che useremo al cap.06 per smascherare bug nel backward.

# TODO PIPE.1 (20 minuti) — implementa derivate_check_completo
#
# Firma:
#   def derivate_check_completo(
#       n_punti: int = 10,
#       seed: int = 0,
#   ) -> dict[str, float]:
#       """Verifica le derivate analitiche vs numeriche su `n_punti`
#       casuali in [-3, 3]. Ritorna un dict con i max errori per ciascuna.
#       """
#       ...
#
# Step:
#   1) Genera n_punti z casuali in [-3, 3]:
#         rng = np.random.default_rng(seed)
#         z_punti = rng.uniform(-3, 3, size=n_punti)
#   2) Per ognuno, verifica:
#         (a) derivata_sigmoid(z) vs derivata_numerica(sigmoid, z)
#         (b) derivata_relu(z) vs derivata_numerica(relu, z)
#             ATTENZIONE: ReLU non e' derivabile in 0; per i punti
#             casuali in [-3, 3] difficilmente cadrai esattamente in 0,
#             ma se la differenza in 1 punto supera 1e-3, accettalo.
#         (c) per BCE: per y=1 e y=0:
#               - num: derivata_numerica(lambda zv: bce_loss(sigmoid(zv), y), z)
#               - ana: sigmoid(z) - y      (la semplificazione miracolosa!)
#               - verifica np.isclose(num, ana, atol=1e-3)
#   3) Calcola max errore per ognuno e mettilo in un dict:
#         {
#           "sigmoid_max_err": ...,
#           "relu_max_err":    ...,
#           "bce_y1_max_err":  ...,
#           "bce_y0_max_err":  ...,
#         }
#   4) Stampa una tabella leggibile.
#   5) Tutti gli errori devono essere < 1e-3 (sigmoid e BCE) e
#      < 0.5 (ReLU, per via di z vicini a 0).
#
# Verifica chiamando con n_punti=20.
# TUO CODICE QUI:


# ==========================================================================
# RINFORZI CAP.01-03 M3 (TODO 7 - 10)
# ==========================================================================

# TODO 7 (8 minuti) [🔄 RECALL cap.01 M3 — derivata "intuitiva" del neurone]:
# Un neurone:  z = w . x + b,  p = sigmoid(z).
# Domanda: se aumento w di un filo, di quanto cambia p?
# Risposta intuitiva: dp/dw = derivata_sigmoid(z) * x (chain rule semplice).
# Verifica numericamente per:
#   x = 2.0 (singola feature)
#   w = 0.5, b = 0.1
# Calcola:
#   - num: gradiente_numerico applicato a una funzione che (w_var) -> sigmoid(w_var * x + b)
#   - ana: derivata_sigmoid(w * x + b) * x
# Devono coincidere.
# TUO CODICE QUI:


# TODO 8 (10 minuti) [🔄 RECALL cap.02 M3 — sigmoid e relu su batch]:
# Riscrivi (senza guardare il cap.02) le funzioni sigmoid e relu in modo
# vettorizzato. Poi applica entrambe a:
#   Z = np.array([-2.0, -1.0, 0.0, 1.0, 2.0])
# Stampa sigmoid(Z) e relu(Z). Calcola anche le rispettive derivate.
# TUO CODICE QUI:


# TODO 9 (10 minuti) [🔄 RECALL cap.03 LOSS — bce_loss vettorizzata da zero]:
# Riscrivi bce_loss da zero (senza guardare la versione in alto):
#   def my_bce(p, y, eps=1e-12) -> float: ...
# Verifica con:
#   p = np.array([0.9, 0.1, 0.8, 0.2])
#   y = np.array([1, 0, 1, 0])
# Confronta my_bce(p, y) con bce_loss(p, y) - devono coincidere.
# TUO CODICE QUI:


# TODO 10 (15 minuti) [🔀 INTERLEAVING cap.02 + cap.03 + cap.04 — derivata sul forward]:
# Mini-pipeline:
#   1) Setup come TODO 4 (X, y, W1, W2, b1, b2 random)
#   2) Forward: P = sigmoid(relu(X @ W1 + b1) @ W2 + b2).ravel()
#   3) loss = bce_loss(P, y)
#   4) Calcola il GRADIENTE NUMERICO della loss RISPETTO A b2 (1 sola
#      variabile = uno scalare!). Quanto vale? Stampa.
#   5) Bonus: questo numero ti dice "se sposto b2 di +epsilon, la loss
#      cambia di gradiente*epsilon". Confermalo numericamente:
#      cambia b2 -> 0.01, ricalcola loss, vedi se loss_nuova - loss_iniziale
#      e' ~ gradiente * 0.01.
# TUO CODICE QUI:


# ==========================================================================
# TIPOLOGIE STANDARD (TODO 11 - 16)
# ==========================================================================

# TODO 11 (15 minuti) [🎯 COLLOQUIO]:
# "Spiega in 6-8 righe a un intervistatore tech:
#   (1) Cos'e' una derivata in 1 riga (NIENTE limiti)
#   (2) Cos'e' un gradiente in 1 riga
#   (3) Quanto vale la derivata di sigmoid in z=0? Perche' e' importante?
#   (4) Cos'e' il vanishing gradient e come si mitiga?
#   (5) Perche' la coppia 'sigmoid + BCE' produce dL/dz = p - y? In una riga."
# TUA RISPOSTA:
# ...


# TODO 12 (15 minuti) [🔧 REFACTORING]:
# Questa derivata_numerica funziona ma ha bug e brutture:
#
#   def derivata_brutta(f, x, h):
#       result = (f(x+h) - f(x)) / h         # bug 1: differenza avanti (meno precisa)
#       return round(result, 5),             # bug 2: round + tuple
#
# Riscrivila:
#   - usa differenza CENTRATA (f(x+h) - f(x-h)) / (2h)
#   - rimuovi il round (perdi precisione) e la virgola finale
#   - dai un valore di default a h (1e-6)
#   - aggiungi type hint
# Confronta poi le due versioni su f(x) = x^3 in x=2.
# TUO CODICE QUI:


# TODO 13 (15 minuti) [🔍 DEBUG]:
# Questo codice DA' un risultato sbagliato. Trova il bug, spiegalo, fixa.
#
#   def derivata_sigmoid_buggata(z):
#       s = sigmoid(z)
#       return s * (1 + s)        # bug: dovrebbe essere s * (1 - s)
#
#   z = np.linspace(-3, 3, 5)
#   for zi in z:
#       num = derivata_numerica(sigmoid, zi)
#       ana = derivata_sigmoid_buggata(zi)
#       print(zi, num, ana)
#
# Confronta con la funzione `derivata_sigmoid` corretta.
# TUA SPIEGAZIONE + FIX:
# ...


# TODO 14 (15 minuti) [🧠 RETRIEVAL cap.02 M3]:
# Riscrivi da zero la funzione `rete_2_layer` SENZA guardare il file
# del cap.02 ne' altre tue versioni precedenti.
# Firma:
#   def rete_2_layer(
#       X: NDArray[np.float64],
#       W1: NDArray[np.float64], b1: NDArray[np.float64],
#       W2: NDArray[np.float64], b2: NDArray[np.float64],
#   ) -> NDArray[np.float64]:
#       """Forward: H = ReLU(X@W1+b1), P = sigmoid(H@W2+b2).ravel()."""
#       ...
# Verifica con shape: X (5, 3), W1 (3, 4), b1 (4,), W2 (4, 1), b2 (1,)
# -> P shape (5,).
# TUO CODICE QUI:


# TODO 15 (15 minuti) [🔀 INTERLEAVING cap.01 + cap.04 — gradiente del neurone]:
# Riscrivi un neurone manuale (cap.01 M3):
#   def neurone(w, x, b):
#       return sigmoid(w * x + b)
# Per (w=0.5, b=0.1, x=2.0):
#   - calcola y_pred = neurone(w, x, b)
#   - calcola dy/dw, dy/db, dy/dx CHIAMANDO gradiente_numerico su 3
#     funzioni "wrapper" diverse (una per ognuna delle 3 variabili)
#   - stampa i 3 gradienti
# Cosa noti? Il gradiente di y rispetto a w "dipende" da x; il gradiente
# rispetto a b non dipende da x. (Pensa al perche'.)
# TUO CODICE QUI:


# TODO 16 (15 minuti) [🌊 REAL-WORLD]:
# Scenario: hai una rete con 10 layer di sigmoid (architettura sbagliata).
# Un collega ti dice: "la loss non scende mai, sembra che la rete non
# impari". Tu sospetti vanishing gradient. Come lo dimostri?
# Implementa un mini-test:
#   1) Calcola derivata_sigmoid in z=0 (=0.25)
#   2) Simula la chain rule per 10 layer: gradiente totale = 0.25 ** 10
#   3) Stampa il valore. Quale ordine di grandezza?
#   4) Commenta in 3 righe perche' la ReLU risolve questo problema
#      (la sua derivata e' 1 per z > 0).
# TUO CODICE QUI:


# ==========================================================================
# QUIZ DI VERIFICA (V1 - V8)
# ==========================================================================

# V1) Cos'e' una derivata in 1 riga (NIENTE limiti, NIENTE formule)?
# TUA RISPOSTA:
# ...

# V2) Cos'e' un gradiente in 1 riga?
# TUA RISPOSTA:
# ...

# V3) La derivata di f(x) = x^2 in x = -5 vale:
#     (a) 25  (b) -10  (c) +10  (d) 0
# TUA RISPOSTA:
# ...

# V4) Il gradiente di f(x, y) = x^2 + y^2 in (1, -2) vale:
#     (a) [2, -4]   (b) [-2, 4]   (c) [2, 4]   (d) [1, 2]
# TUA RISPOSTA:
# ...

# V5) [Trova l'errore] Questo codice ha 1 bug:
#       def derivata_sigmoid_buggata(z):
#           s = sigmoid(z)
#           return s + (1 - s)
#     Quale? E qual e' la formula corretta?
# TUA RISPOSTA:
# ...

# V6) [Prevedi output] Cosa stampa?
#       z = np.array([-10.0, 0.0, 10.0])
#       print(derivata_sigmoid(z))
# (Suggerimento: ai bordi sigmoid satura, derivata ~ 0; in 0 max ~ 0.25.)
# TUA RISPOSTA:
# ...

# V7) Perche' nella coppia "BCE + sigmoid" la derivata rispetto al logit
#     z si semplifica in (p - y)?
# TUA RISPOSTA:
# ...

# V8) [💬 Feynman] Spiega in 4 righe il "vanishing gradient" a un collega
#     web dev. Senza usare derivata, gradiente, layer, vanishing, chain.
# TUA RISPOSTA:
# ...


# ==========================================================================
# MINI-PROGETTO FINALE — `analizza_funzione_attivazione`
# ==========================================================================
#
# OBIETTIVO: una funzione che, data una funzione di attivazione f e la
# sua derivata f', restituisce uno scorecard "analitico" che ti dice
# quanto e' adatta per il deep learning.

# TODO MINI-PROGETTO (25 minuti):
#
# Firma:
#   def analizza_funzione_attivazione(
#       f: Callable[[float], float],
#       f_prime: Callable[[float], float],
#       nome: str,
#       z_range: tuple[float, float] = (-6.0, 6.0),
#   ) -> dict[str, float]:
#       """Ritorna un dict con:
#         'nome'              : nome della funzione
#         'f_in_z=0'          : f(0)
#         'f_prime_max'       : massimo di f' nel range
#         'f_prime_max_z'     : argmax (z dove la derivata e' max)
#         'f_prime_mean'      : media di f' nel range (= "passa quanto gradiente")
#         'satura_a_sinistra' : True se f'(-5) < 0.01
#         'satura_a_destra'   : True se f'(+5) < 0.01
#         'sanity_check_ok'   : True se derivata_numerica(f, z) ~ f_prime(z)
#                                in 5 punti random (atol 1e-3)
#       """
#
# Implementala. Poi chiamala 3 volte:
#   1) sigmoid + derivata_sigmoid
#   2) relu + derivata_relu
#   3) tanh: f = lambda z: np.tanh(z), f' = lambda z: 1 - np.tanh(z)**2
#
# Stampa la tabella dei 3 scorecard (1 riga per attivazione). Commenta:
#   - quale ha derivata massima piu' alta? (-> meno vanishing)
#   - quale satura ai bordi? (-> piu' vanishing)
#   - quale e' "migliore" per DL classico? Perche'?
# TUO CODICE QUI:


# ==========================================================================
# CHECKPOINT FINALE (auto-verifica)
# ==========================================================================

# C1) In 1 frase: cos'e' una derivata in 1D? E un gradiente in nD?
# TUA RISPOSTA:
# ...

# C2) La derivata di sigmoid in z=0 vale 0.25. Spiega in 2 righe perche'
#     questo causa problemi se hai TANTI layer di sigmoid impilati.
# TUA RISPOSTA:
# ...

# C3) [Prevedi] Hai p = sigmoid(z) e L(p, y) = BCE. Per (z=0, y=1):
#     - dL/dz = ?
#     - dL/dp = ?
# Suggerimento: per dL/dz usa la semplificazione miracolosa.
# TUA RISPOSTA:
# ...

# C4) [Recap calcolo] Per f(x, y, z) = x^2 * y + sin(z), in (x=1, y=2, z=0):
#     - df/dx = ?
#     - df/dy = ?
#     - df/dz = ?
#     Gradiente complessivo = ?
# TUA RISPOSTA:
# ...

# C5) Auto-rating onesto:
#       - Derivata come pendenza:                       /10
#       - Derivata sigmoid (max 0.25 + implicazione):    /10
#       - Derivata ReLU (step, dying ReLU):              /10
#       - Gradiente come vettore di derivate parziali:   /10
#       - Semplificazione miracolosa BCE+sigmoid:        /10
#       - Pipeline integrata derivate_check:             /10
# TUE RISPOSTE:
# ...


# ==========================================================================
# SOLUZIONI QUIZ
# ==========================================================================
"""
QUIZ D'INGRESSO

Q1) BCE = misura continua e DERIVABILE di quanto la rete sbaglia. La
    minimizziamo perche' e' derivabile -> possiamo calcolarne il
    gradiente sui pesi. L'accuracy e' a scalini -> derivata zero
    quasi ovunque -> backprop non funziona.

Q2) Il clip e' bilaterale perche' la BCE usa SIA log(p) (esplode in 0)
    SIA log(1-p) (esplode in 1). Senza il lato destro: y=0, p=1 ->
    log(1-1) = log(0) = -inf.

Q3) Layer dense = "out = activation(X @ W + b)". W matrice di pesi,
    b vettore di bias. Forward 2-layer: H = ReLU(X@W1+b1),
    P = sigmoid(H@W2+b2).

Q4) f(2) = 4. f(2.001) = 4.004001. Differenza ~ 0.004. Pendenza ~ 4
    (= derivata di x^2 in x=2 = 2*2 = 4).

Q5) Esempio: "Hai un grafico di CPU usage nel tempo. La pendenza in un
    punto ti dice 'in questo istante la CPU sta salendo o scendendo, e
    di quanto al secondo'. Una pendenza forte verso l'alto = problema."

Q6) 12.0 (= 3 * 2^2 = 12).


MINI-ESERCIZI INLINE

1.1.A) ~6.0, ~-6.0, ~0.0  (la derivata di x^2 e' 2x; in x=3, x=-3, x=0).
1.1.B) Sempre 3.0 (pendenza costante della retta).
1.2.A) Tutte coincidono a meno di ~1e-10 per funzioni "lisce" come
       x^3, sin, exp.
1.3.A) File creato in figures/04_01_tangenti.png.
1.3.B) (1) In x=0 la pendenza e' 0. (2) Trick: sei al MINIMO, non puoi
       scendere oltre. (Se vuoi proprio "scendere di piu'", devi
       cambiare funzione, non punto!)

2.1.A) z=-3 -> ~0.045, z=-1 -> ~0.197, z=0 -> 0.25,
       z=1 -> ~0.197, z=3 -> ~0.045. Massimo in z=0.
2.1.B) der.max() ~ 0.25, zz[argmax] ~ 0.

2.2.A) 0.25^5 ~ 0.00098. Dopo 5 layer di sigmoid il gradiente massimo
       e' ~0.1% di quello iniziale. Per 10 layer: 0.25^10 ~ 9.5e-7.
       Praticamente zero -> i primi layer non imparano.

3.1.A) z=-2 -> ana=0, num=0 (ok). z=-1 -> ana=0, num=0 (ok). z=0 -> ana=0,
       num=0.5 (la derivata in 0 non e' definita). z=1 -> ana=1, num=1 (ok).
       z=2 -> ana=1, num=1 (ok).
3.2.A) Z = X @ W + b = X @ [[0.1],[0.2]] + (-10) -> circa -9.5 e -8.9.
       Nessun Z > 0. derivata_relu(Z) tutto 0. Neurone "morto" -> non impara.

4.1.A) f(x,y)=x^2+y^2 in (1,-2) -> [2, -4]. f(x,y)=xy in (3,5) -> [5, 3].
       f(x,y,z)=x^2+2y^2+3z^2 in (1,1,1) -> [2, 4, 6].
4.2.A) File creato in figures/04_02_gradiente_2d.png.
4.3.A) df/dx = 2*x*y, df/dy = x^2 + 3. In (1,2): [4, 4].
4.3.B) Una variabile -> una derivata parziale. 3 variabili -> 3 derivate
       parziali -> vettore in R^3.

5.1.A) Per p=0.8, y=1: num ~ -1.25. ana = (0.8 - 1) / (0.8 * 0.2) = -1.25.
5.2.A) Per z=-3 y=1: p~0.0474, dL/dz = p-y ~ -0.953.
       Per z=0 y=1: p=0.5, dL/dz = -0.5. Per z=3 y=1: p~0.953, dL/dz ~ -0.047.
5.3.A) La cancellazione p*(1-p)/p*(1-p) avviene SOLO perche' la
       derivata sigmoid e' p*(1-p) e la derivata BCE rispetto a p ha
       p*(1-p) al denominatore. Cambia attivazione -> cambia dp/dz
       -> niente cancellazione.


QUIZ DI VERIFICA

V1) Derivata = "pendenza della curva in un punto" / "se aumento x di un
    filo, di quanto cambia f?"

V2) Gradiente = "lista di tutte le derivate parziali" / "vettore di
    pendenze, una per ogni variabile della funzione".

V3) (b) -10. Derivata di x^2 e' 2x; in x=-5 vale -10.

V4) (a) [2, -4]. Gradiente di x^2+y^2 e' [2x, 2y]; in (1, -2) -> [2, -4].

V5) Bug: "s + (1-s)" sempre uguale a 1, costante. La formula corretta:
    derivata_sigmoid(z) = s(z) * (1 - s(z)).

V6) [~4.5e-5, 0.25, ~4.5e-5]. Sigmoid satura ai bordi -> derivata ~ 0;
    in 0 e' massima.

V7) Per chain rule (cap.05): dL/dz = dL/dp * dp/dz = ((p-y)/(p(1-p))) *
    (p(1-p)) = p-y. I p(1-p) si elidono.

V8) Esempio: "Immagina di passare un messaggio in un gruppo di amici:
    ognuno lo ripete sussurrando. Dopo 10 amici, il messaggio e'
    talmente debole che l'ultimo non lo sente piu'. Cosi' un'informazione
    di 'correzione' che viene passata indietro attraverso tanti layer
    si attenua a ogni passo. Se ogni amico parlasse a voce piena
    (= ReLU per z > 0), il messaggio arriverebbe intero."


CHECKPOINT FINALE

C1) Derivata 1D = "pendenza della funzione in un punto" / "se aumento
    x di un filo, di quanto cambia f". Gradiente nD = "vettore di
    pendenze, una per ogni variabile" / "lista di derivate parziali".

C2) La derivata di sigmoid e' max 0.25. Per chain rule (cap.05+06),
    il gradiente di un parametro del PRIMO layer viene moltiplicato
    per la derivata sigmoid di ogni layer. Con N layer di sigmoid il
    fattore massimo e' 0.25^N -> diventa ~0 molto in fretta -> i
    primi layer NON ricevono segnale di apprendimento.

C3) z=0 y=1: p = sigmoid(0) = 0.5.
    dL/dz = p - y = 0.5 - 1 = -0.5.
    dL/dp = (p - y) / (p * (1-p)) = -0.5 / 0.25 = -2.0.

C4) df/dx = 2x*y. df/dy = x^2. df/dz = cos(z).
    In (1, 2, 0): df/dx = 4, df/dy = 1, df/dz = cos(0) = 1.
    Gradiente = [4, 1, 1].
"""


# ==========================================================================
# NOTE PER IL CAPITOLO SUCCESSIVO (cap.05 chain_rule + gradient descent)
# ==========================================================================
#
# Cosa porti via:
#   - derivata_numerica, gradiente_numerico (sanity check)
#   - derivata_sigmoid, derivata_relu (analitiche)
#   - intuizione "dL/dz = p - y" per BCE+sigmoid
#
# Cosa NON sai ancora:
#   - come comporre piu' derivate (chain rule formale)         -> cap.05
#   - come usare il gradiente per AGGIORNARE i pesi (GD)       -> cap.05
#   - tutto questo applicato a una rete reale (backprop)       -> cap.06
#
# Prima di aprire il cap.05, fai il bridge ripasso:
#   modulo_03_dl_cv/quiz_ripasso_tra_capitoli/
#       M03_R04_after_C04_before_C05_derivate_to_chain.md


# ==========================================================================
# ENTRY POINT
# ==========================================================================
if __name__ == "__main__":
    print("=" * 70)
    print("Cap.04 M3 - DERIVATE e GRADIENTE - demo di riferimento")
    print("=" * 70)

    print("\n[Demo 4.1 - gradiente di x^2 + y^2 in (3, 4)]")
    _esempio_gradiente_2d()

    print("\n[Demo - genero grafici nelle figures/]")
    figures_dir = os.path.join(os.path.dirname(__file__), "figures")
    _grafico_funzione_e_tangenti(out_path=os.path.join(figures_dir, "04_01_tangenti.png"))
    _grafico_campo_gradiente(out_path=os.path.join(figures_dir, "04_02_gradiente_2d.png"))
    print(f"  -> {figures_dir}/04_01_tangenti.png")
    print(f"  -> {figures_dir}/04_02_gradiente_2d.png")

    print("\n" + "=" * 70)
    print("Demo finite. Adesso tocca a te:")
    print("  - 16 mini-esercizi inline (sez 1-5)")
    print("  - 6 TODO base (1-6)")
    print("  - 1 pipeline integrata (derivate_check_completo)")
    print("  - 4 TODO recall cap.01-03 M3 (7-10)")
    print("  - 6 TODO tipologie (colloquio/refactor/debug/retrieval/INT/RW)")
    print("  - 8 quiz verifica + mini-progetto + checkpoint")
    print("Quando vuoi una valutazione: 'valuta cap.04 M3 sezione X'.")
    print("=" * 70)
