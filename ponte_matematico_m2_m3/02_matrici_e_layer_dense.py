"""
============================================================================
PONTE MATEMATICO (bridge M2 -> M3) - CAPITOLO 02
"Matrici e layer Dense": una matrice = un batch di pratiche
============================================================================

----------------------------------------------------------------------------
DA DOVE ARRIVI (cap.01 Ponte)
----------------------------------------------------------------------------
Nel cap.01 hai imparato che:

    pratica_A = np.array([1200, 30, 250, 180, 90])   # un VETTORE 1D, shape (5,)
    z         = np.dot(pratica_A, w) + b              # un DOT PRODUCT
    norma_A   = np.linalg.norm(pratica_A)             # GRANDEZZA
    cos_AB    = coseno(pratica_A, pratica_B)          # DIREZIONE/FORMA

Tutto bello. Ma in produzione NON arriva una pratica alla volta:
arrivano 1000 pratiche al giorno. Le vuoi classificare TUTTE INSIEME, in
un colpo solo, perche':

    - se fai un loop Python -> 1000 dot product separati = SLOW
    - se le metti in una MATRICE e fai 1 prodotto matrice-vettore -> FAST
      (NumPy parallelizza sotto, GPU accelera ancora di piu' in M3)

In questo capitolo impariamo a:
    1) impacchettare N pratiche in una MATRICE X di shape (N, d)
    2) calcolare TUTTI i punteggi con UN solo "X @ w + b"
    3) capire che un layer Dense di una rete neurale (M3) = la stessa
       cosa, solo che "w" non e' fissato ma lo IMPARA il training

----------------------------------------------------------------------------
COSA PORTI VIA DA QUESTO CAPITOLO (Definition of Done)
----------------------------------------------------------------------------
Alla fine sai rispondere "in 1 riga" a queste 6 domande:

  1) Differenza fra shape (N, d), (d,), (N,)?                   -> Sezione 1
  2) Cosa calcola X @ w quando X e' (N, d) e w e' (d,)?         -> Sezione 2
  3) Perche' e' equivalente a fare N dot product separati?      -> Sezione 2
  4) Cosa fa "X @ W2 + b2" quando W2 e' (d, h)?                 -> Sezione 3
  5) Perche' un layer Dense = matrice di pesi + bias?           -> Sezione 3
  6) Quando NON si possono moltiplicare due matrici? (regola)   -> Sezione 1

Hai anche scritto 3 funzioni riutilizzabili: punteggio_batch, layer_dense,
classifica_batch.

----------------------------------------------------------------------------
MAPPA DEL CAPITOLO
----------------------------------------------------------------------------
   *  PRONTUARIO TRANELLI MATRICI       [M1] - [M8]
   *  QUIZ D'INGRESSO                   Q1 - Q8     (cerniera cap.01 Ponte)
   *  RINFORZO Pattern #23              (virgole -> tuple)
   *  RINFORZO Pattern #24              (iloc vs loc)
   *  RINFORZO Pattern #25              (np.array vs np.ndarray)
   *  RIPASSO 5 BLOCCHI cap.01          R1 - R5     (richiesto dallo studente)
   *  SEZIONE 1  Matrici come batch          1.1 - 1.2
   *  SEZIONE 2  Prodotto matrice-vettore    2.1 - 2.2
   *  SEZIONE 3  Layer Dense (preludio M3)   3.1 - 3.2
   *  QUIZ DI VERIFICA                  V1 - V8
   *  ESERCIZI FINALI                   E1 - E5     (colloquio/refactor/debug/retrieval/interleaving)
   *  MINI-PROGETTO GUIDATO             classifica_batch (batch-mode)
   *  CHECKPOINT FINALE                 C1 - C4
   *  SOLUZIONI QUIZ                    in fondo

----------------------------------------------------------------------------
COME USARE QUESTO FILE (regola del corso)
----------------------------------------------------------------------------
   1. Leggi in ORDINE. La sezione N usa la sezione N-1.
   2. Per ogni TODO scrivi nel blocco "TUO CODICE" (non cancellare lo
      scaffold, lascialo come traccia).
   3. Quando vuoi una valutazione: "valuta cap.02 ponte sezione X.Y"
   4. Se ti blocchi >10 min: "sono bloccato sezione X" -> ti do solo
      l'IDEA, mai la soluzione.
   5. Niente LaTeX (preferenza tua): le formule sono in PAROLE + codice.
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# ==========================================================================
# PRONTUARIO TRANELLI MATRICI - leggilo PRIMA di iniziare (8 minuti)
# ==========================================================================
# Sono i tranelli specifici delle MATRICI. Quelli sui vettori (T1-T10) li
# trovi nel cap.01 Ponte: ti restano validi anche qui.
#
# [M1] SHAPE DI UNA MATRICE: (righe, colonne) = (N, d).
#      Per noi: N = "quante pratiche", d = "quante feature per pratica".
#      Esempio: 1000 pratiche con 5 feature -> X.shape == (1000, 5)
#
# [M2] REGOLA DEL PRODOTTO MATRICE-MATRICE:
#      A @ B funziona SOLO se A.shape[1] == B.shape[0]
#      "Le colonne di A devono uguagliare le righe di B".
#      A: (N, d) e B: (d, h)  -> output: (N, h)  OK
#      A: (N, d) e B: (h, d)  -> ERRORE shapes not aligned
#
# [M3] PRODOTTO MATRICE-VETTORE: e' un caso particolare di [M2].
#      X: (N, d) e w: (d,)  -> output (N,)
#      Stai facendo N dot product in parallelo, uno per riga di X.
#
# [M4] BROADCASTING DEL BIAS:
#      X @ w + b  con X:(N,d), w:(d,), b: scalare -> output (N,)
#      NumPy aggiunge "b" a TUTTI gli elementi (broadcasting).
#      Se b fosse (N,), idem: b si somma riga per riga.
#
# [M5] X.T (TRASPOSTA): scambia righe e colonne.
#      X: (N, d)  ->  X.T: (d, N)
#      Serve quando il prodotto "non torna" e devi riallineare le shape.
#
# [M6] X[i] vs X[i, :] vs X[i:i+1] - cosa estrai e che shape?
#      X[i]      -> riga i, shape (d,)        (1D! attento)
#      X[i, :]   -> riga i, shape (d,)        (identico a sopra)
#      X[i:i+1]  -> sottomatrice 1 riga, shape (1, d)  (2D!)
#      Per predict_proba di sklearn ti serve la versione (1, d).
#
# [M7] PANDAS DataFrame -> NumPy: usa .to_numpy() per ottenere una matrice
#      X = df.drop(columns=["pratica_id", "y_alterato"]).to_numpy(dtype=float)
#      Senza dtype=float rischi colonne object se ci sono NaN o stringhe.
#
# [M8] NON CONFONDERE w (vettore di pesi) con W (matrice di pesi):
#      regressione/log: w shape (d,)        -> output 1 numero per riga
#      layer Dense:     W shape (d, h)      -> output h numeri per riga
#      In M3 i layer Dense usano W (matrice). Qui ne diamo solo l'anteprima.


# ==========================================================================
# QUIZ D'INGRESSO - cerniera cap.01 Ponte -> cap.02 Ponte
# ==========================================================================
# Rispondi nei commenti sotto ogni domanda. Non barare scorrendo in fondo.
# Soluzioni a fine file.

# Q1) Cosa restituisce np.linalg.norm([3, 4])?
#     Spiega anche PERCHE'.
# TUA RISPOSTA:
# restituisce la norma euclidea, ossia la radice della somma dei quadrati degli elementi di un vettore=> sqrt(9 + 16) => 5. Si usa per definire la grandezza del vettore ([3, 4]).

# Q2) Hai due vettori a = [1, 2, 3] e b = [2, 4, 6].
#     Quanto vale coseno(a, b)? Senza calcolare a mano: che intuizione hai?
# TUA RISPOSTA:
# Si può osservare che gli elementi di b sono il doppio degli elementi di a posizionati allo stesso indice. Senza fare calcoli, si può intuire che coseno(a, b) = 1, mentre la grandezza è esattamente il doppio, poiche' ||b|| = 2 * ||a||

# Q3) np.dot([1, 2, 3], [4, 5, 6]) restituisce uno SCALARE o un VETTORE?
#     Quale e' il valore?
# TUA RISPOSTA:
# Il dot product restituisce uno scalare, poichè il suo risultato è la somma tra i prodotti delle moltiplicazioni degli elementi posizionati allo stesso indice di due vettori (anche detto somma di un prodotto element-wise di due vettori). Nel nostro caso , (1*4 + 2*5 + 3*6) = 32

# Q4) Vero o Falso, e perche':
#     "Se due vettori hanno coseno = 1.0, allora sono UGUALI."
# TUA RISPOSTA:
# Falso. La risposta corretta è che hanno stessa direzione, ossia le loro direzioni li rendono paralleli. Se oltre a coseno 1 (direzione uguale) avessero anche norma uguale (stessa grandezza), allora potrebbero essere definiti uguali (salvo micro-errori di arrotondamento).

# Q5) np.array([1, 2, 3]).shape vale (3,) o (1, 3)? Perche' importa?
# TUA RISPOSTA:
# Vale (3,). E importante perchè nel nostro caso la shape descritta identifica un vettore mono-dimensionale. Se avesse shape (1, 3) staremmo descrivendo una matrice, nella fatti-specie scritta np.array([[1, 2, 3]])

# Q6) Type hint: scriveresti "def f(v: np.array) -> float" o
#     "def f(v: np.ndarray) -> float"? Spiega.
# TUA RISPOSTA:
# Nel primo caso stiamo formulando il type hint in modo errato, poichè la sintassi np.array in realtà descrive la chiamata a un metodo della libreria Numpy. La secondo invece è la sintassi corretta, perchè descrive nella fatti-specie il type hint restituito dal metodo prima citato, ossia un array numpy.

# Q7) [Trova l'errore] - Questo codice da' TypeError. Perche'?
#       df = pd.DataFrame({"a": [1, 2], "b": [3, 4]})
#       valore = df.iloc[0, "a"]
#     Come lo sistemeresti?
# TUA RISPOSTA:
# il metodo iloc accetta solo parametri numerici, mentre nel caso descritto sopra si sta usando una striga per travare la colonna con etichetta "a". Se "a" avesse indice 1, la scrittura corretta sarebbe df.iloc[0, 1] => trova l'elemento che si trova nella riga 0 , colonna 1.

# Q8) [Feynman] Spiega con parole tue, come lo diresti a un collega web dev
#     che non ha mai visto NumPy: cosa misura la NORMA di un vettore e cosa
#     misura il COSENO fra due vettori? Niente formule, solo intuizione.
# TUA RISPOSTA:
# La norma serve per descrivere la grandezza di un vettore, mentre il coseno indica la differenza di direzioni tra due vettori. Immaginando i vettori come delle freccie, la norma sarebbe la lunghezza della freccia. Il coseno invece la differenza di direzioni di due freccie confrontate tra loro, espressa tramite un valore che va da 1 (parallele) a -1 (opposte).


# ==========================================================================
# RINFORZO Pattern #23 - virgole a fine chiamata creano tuple inutili
# ==========================================================================
# Nel cap.01 Ponte (sezioni 4.2 e 5.1) hai scritto codice tipo:
#
#     ax.quiver(0, 0, vx, vy, color="red"),
#     plt.savefig("figures/demo.png"), plt.close(fig)
#
# Sembra una "scorciatoia per stare in 8 righe", ma Python lo legge come
# una TUPLA. Verifichiamolo:

def _demo_pattern_23() -> None:
    """Mostra cosa restituisce davvero la 'virgola a fine riga'."""
    risultato_a = (print("hello"),)            # tupla con 1 elemento (None,)
    risultato_b = (print("a"), print("b"))     # tupla con 2 elementi (None, None)
    print("type(risultato_a):", type(risultato_a), "->", risultato_a)
    print("type(risultato_b):", type(risultato_b), "->", risultato_b)


# Cosa fare invece:
#   - se vuoi piu' istruzioni su una riga, usa il punto-e-virgola ";"
#         plt.savefig("x.png"); plt.close(fig)
#   - oppure (preferito) UNA istruzione per riga, e basta.
#   - se servisse continuare una riga lunga, usa la backslash "\" o le
#     parentesi tonde.

# TODO Rinforzo #23 (3 minuti):
# 1) Cancella le virgole spurie da questo codice rotto e fallo girare:
#       fig, ax = plt.subplots(),
#       ax.set_title("ciao"), ax.set_xlim(-1, 1), ax.set_ylim(-1, 1),
#       plt.close(fig)
# 2) Spiega in 1 riga COMMENTATA cosa cambia:
# TUO CODICE QUI:
# prima oltre a dare le istruzioni necessarie a generare i grafico, stavamo anche creando tuple inutili.
fig, ax = plt.subplots()
ax.set_title("ciao")
ax.set_xlim(-1, 1)
ax.set_ylim(-1, 1)
plt.close(fig)


# ==========================================================================
# RINFORZO Pattern #24 - iloc vs loc: indici NUMERICI vs ETICHETTE
# ==========================================================================
# Nel mini-progetto del cap.01 hai scritto:
#
#     pratiche.iloc[i, "pratica_id"]   # TypeError!
#
# .iloc accetta SOLO indici numerici (int o slice). Le etichette stringa
# vanno con .loc. Questa e' la tabella decisionale:
#
#   COSA HAI?                  USA       ESEMPIO
#   ---------------------------------------------------------
#   indice int (riga 5)        iloc      df.iloc[5]
#   indice int + indice int    iloc      df.iloc[5, 2]
#   nome colonna (str)         loc       df.loc[5, "colonna"]
#   slice di righe per pos.    iloc      df.iloc[0:10]
#   slice di righe per nome    loc       df.loc["a":"c"]
#   maschera booleana          loc       df.loc[mask]
#
# Caso comune: vuoi accedere a "colonna_x" della riga in posizione i.
# 3 modi corretti:
#   df.iloc[i]["colonna_x"]      # prima estrai la riga, poi la colonna
#   df.loc[df.index[i], "colonna_x"]
#   df["colonna_x"].iloc[i]      # stesso risultato, prima la colonna

def _demo_pattern_24() -> None:
    df = pd.DataFrame({"pratica_id": [101, 102, 103], "importo": [1200, 800, 1500]})
    primo_id = df.iloc[0]["pratica_id"]   # 101 - corretto
    primo_importo = df.loc[0, "importo"]  # 1200 - corretto
    print("primo_id:", primo_id, "primo_importo:", primo_importo)


# TODO Rinforzo #24 (3 minuti):
# Dato il df qui sotto, scrivi 2 righe per:
#   (a) ottenere la riga in posizione 1 come Series
#   (b) ottenere il valore di "voto" per la riga in posizione 2
df_demo = pd.DataFrame({"nome": ["Anna", "Bob", "Carla"], "voto": [7, 5, 9]})
# TUO CODICE QUI:
riga_series = df_demo.iloc[1, :]
voto_riga_2 = df_demo['voto'].iloc[2]

# ==========================================================================
# RINFORZO Pattern #25 - np.array vs np.ndarray (factory vs tipo)
# ==========================================================================
# Nel cap.01 hai scritto:
#
#     def norma(v: np.array) -> float:   # tecnicamente sbagliato
#
# Il motivo: np.array NON e' un tipo, e' una FUNZIONE che CREA un ndarray.
# Il TIPO si chiama np.ndarray. Per type hint moderni hai 2 opzioni:
#
#   (basic)   def norma(v: np.ndarray) -> float
#   (strict)  from numpy.typing import NDArray
#             def norma(v: NDArray[np.float64]) -> float
#
# Verifica con isinstance:

def _demo_pattern_25() -> None:
    v = np.array([1, 2, 3])
    print("isinstance(v, np.ndarray):", isinstance(v, np.ndarray))   # True
    # print("isinstance(v, np.array):", isinstance(v, np.array))     # TypeError!
    # np.array non e' una classe, e' una funzione.
    print("type(v):", type(v))   # <class 'numpy.ndarray'>


# TODO Rinforzo #25 (2 minuti):
# Riscrivi questa firma con il type hint CORRETTO:
#   def somma_due_vettori(a: np.array, b: np.array) -> np.array:
#       return a + b
# TUO CODICE QUI:
# def somma_due_vettori(a: np.ndarray, b: np.ndarray) -> np.ndarray:
#     return a + b


# ==========================================================================
# RIPASSO 5 BLOCCHI cap.01 (richiesto da te in auto-rating)
# ==========================================================================
# Mini-esercizi rapidi (2-4 righe ciascuno) per fissare i 5 pilastri del
# cap.01 PRIMA di passare alle matrici. Sono di "retrieval practice":
# scrivi senza guardare il cap.01.

# R1) VETTORI + SHAPE
# Crea un vettore NumPy con 6 elementi qualsiasi. Stampa la sua shape e
# il suo dtype.
# TUO CODICE:
print("\nMini-esercizio R1\n")
v = np.array([1, 2, 3, 4, 5, 6], dtype=float)
print(v.shape)
print(v.dtype)


# R2) OPERAZIONI BASE
# Dati a = np.array([2, 4, 6]) e b = np.array([1, 1, 1]),
# stampa: a + b, a - b, 2 * a, a * b
# Quanti scalari produce ognuna? Quale e' element-wise?
# TUO CODICE:
# Sono tutte operazione element-wise che producono vettori con shape sempre uguale
print("\nMini-esercizio R2\n")
a = np.array([2, 4, 6])
b = np.array([1, 1, 1])
print(a + b)
print(a - b)
print(a * b)
print(2 * a)

# R3) DOT PRODUCT (senza usare np.dot)
# Dati x = np.array([1, 2, 3]) e w = np.array([10, 20, 30]),
# calcola il dot product SENZA usare np.dot ne' "@".
# Suggerimento: element-wise + .sum().
# TUO CODICE:
print("\nMini-esercizio R3\n")
x = np.array([1, 2, 3])
w = np.array([10, 20, 30])
dot = (x * w).sum()
print(dot)

# R4) NORMA EUCLIDEA (senza usare np.linalg.norm)
# Dato v = np.array([3, 4]), calcola la norma USANDO solo np.sqrt e .sum().
# Verifica che sia 5.0.
# TUO CODICE:
print("\nMini-esercizio R4\n")
v = np.array([3, 4])
norma = np.sqrt((v**2).sum())
print(norma)

# R5) COSENO (usando la tua definizione mentale)
# Dati a = np.array([1, 0]) e b = np.array([0, 1]), calcola il coseno
# (devi ottenere 0.0). Ora prova con b = np.array([1, 0]) (devi ottenere 1.0).
# TUO CODICE:
print("\nMini-esercizio R5\n")
a = np.array([1, 0])
b = np.array([0, 1])
coseno = (a @ b) / (np.linalg.norm(a) * np.linalg.norm(b))
print(coseno)
assert np.isclose(coseno, 0.0)
b = np.array([1, 0])
coseno = (a @ b) / (np.linalg.norm(a) * np.linalg.norm(b))
print(coseno)
assert np.isclose(coseno, 1.0)

# ==========================================================================
# SEZIONE 1 - MATRICI COME BATCH DI PRATICHE
# ==========================================================================

# ---------------------- ANALOGIA --------------------------------------------
# Pensa a una giornata di lavoro nel tuo studio:
#   - ogni cliente porta una pratica
#   - ogni pratica = vettore di feature [importo, giorni, tasse, irpef, contributi]
#   - ogni giorno arrivano 1000 pratiche
#
# Se le metti tutte in una TABELLA, ottieni una matrice X:
#
#   X = [[1200,  30, 250, 180,  90],   <- pratica 1, riga 0
#        [ 800,  10, 100,  90,  60],   <- pratica 2, riga 1
#        [1500,  45, 320, 220, 110],   <- pratica 3, riga 2
#        ...
#        [ 900,  20, 150, 120,  70]]   <- pratica N, riga N-1
#
#   X.shape == (N, 5)
#   N = "quante pratiche"
#   5 = "quante feature per pratica" (chiamiamolo d, "dimension")
#
# In Pandas: X = df.to_numpy()
# In SQL:    X = SELECT * FROM pratiche

# ---------------------- TEORIA + CODICE -------------------------------------
# 1.1 - CREAZIONE DI UNA MATRICE BATCH
# Una matrice in NumPy nasce da una "lista di liste":

def _esempio_matrice() -> np.ndarray:
    X = np.array([
        [1200, 30, 250, 180,  90],
        [ 800, 10, 100,  90,  60],
        [1500, 45, 320, 220, 110],
        [ 900, 20, 150, 120,  70],
    ], dtype=float)
    print("X.shape:", X.shape)         # (4, 5)
    print("X.dtype:", X.dtype)         # float64
    print("X[0]:", X[0])               # prima pratica, vettore (5,)
    print("X[:, 0]:", X[:, 0])         # tutti gli importi, vettore (4,)
    return X


# 1.2 - VETTORE-RIGA, VETTORE-COLONNA, MATRICE: chi e' chi?
#
# Hai 3 modi diversi di rappresentare gli stessi 5 numeri:
#
#   v_1d  = np.array([1200, 30, 250, 180, 90])         shape (5,)    1D
#   v_riga = np.array([[1200, 30, 250, 180, 90]])      shape (1, 5)  2D
#   v_col  = np.array([[1200], [30], [250], [180], [90]])  shape (5, 1)  2D
#
# Quale usare? DIPENDE dall'operazione:
#   - dot product con un vettore w di pesi: serve 1D (5,)
#   - predict_proba di sklearn: serve (1, 5)  -> reshape(1, -1)
#   - layer Dense matematicamente "puro": (1, 5)  o  (5, 1) a seconda della convenzione

# TODO 1.1 (5 minuti):
# Carica il CSV reale del Modulo 2 e costruisci la matrice X delle prime 5
# pratiche. Stampa: X.shape, X.dtype, X[0], X[:, 0].
# Path consigliato (Windows + bash safe):
#   csv_path = os.path.join(
#       os.path.dirname(os.path.dirname(__file__)),
#       "modulo_02_ml", "dati", "pratiche_genuinita_mock.csv",
#   )
#
# Suggerimento: drop "pratica_id" e "y_alterato" PRIMA di chiamare to_numpy.
# Lo schema corretto:
#   df = pd.read_csv(csv_path)
#   X_full = df.drop(columns=["pratica_id", "y_alterato"]).to_numpy(dtype=float)
#   X = X_full[:5]
#
# TUO CODICE QUI:
print("\nEsercizio 1.1\n")
CSV_PATH = os.path.join(
    os.path.dirname(
        os.path.dirname(__file__)
    ),
    "modulo_02_ml",
    "dati",
    "pratiche_genuinita_mock.csv"
)

pratiche = pd.read_csv(CSV_PATH)
X_full = pratiche.drop(columns=['pratica_id', 'y_alterato']).to_numpy(dtype=float)
X = X_full[:5]
print(X.shape)
print(X.dtype)
print(X[0])
print(X[:, 0])


# TODO 1.2 (5 minuti):
# Dato il vettore v = np.array([10, 20, 30, 40, 50]):
#   (a) crea un vettore-riga (1, 5) usando reshape o np.array([v])
#   (b) crea un vettore-colonna (5, 1) usando reshape o np.array([[x] for x in v])
#   (c) stampa le 3 shape per verificare
# TUO CODICE QUI:
print("\nEsercizio 1.2\n")
v = np.array([10, 20, 30, 40, 50])
vr = v.reshape(1, 5)
vc = v.reshape(5, 1)
print(v.shape)
print(vr.shape)
print(vc.shape)

# ==========================================================================
# SEZIONE 2 - PRODOTTO MATRICE-VETTORE: 1 OPERAZIONE = N DOT PRODUCT
# ==========================================================================

# ---------------------- ANALOGIA --------------------------------------------
# Hai gia' calcolato il punteggio di UNA pratica nel cap.01:
#
#     z = np.dot(pratica_A, w) + b
#
# Adesso devi calcolarlo per N=1000 pratiche. Due strade:
#
# STRADA LENTA (loop Python):
#     punteggi = []
#     for i in range(N):
#         punteggi.append(np.dot(X[i], w) + b)
#     punteggi = np.array(punteggi)            # shape (N,)
#
# STRADA VELOCE (1 sola operazione vettoriale):
#     punteggi = X @ w + b                     # shape (N,)
#
# Le due strade danno lo STESSO risultato. La seconda e' 50-1000 volte
# piu' veloce perche' NumPy chiama codice C sotto. In M3 con la GPU
# diventa ancora piu' importante.

# ---------------------- TEORIA + CODICE -------------------------------------
# 2.1 - REGOLA DELLE SHAPE PER X @ w
#
#   X.shape == (N, d)
#   w.shape == (d,)
#   ----------------------- @
#   output.shape == (N,)
#
# Riga per riga, NumPy calcola: output[i] = sum_j X[i, j] * w[j]
# Cioe' un dot product fra la riga i di X e il vettore w.

def _esempio_punteggio_batch() -> None:
    X = np.array([
        [1.0, 0.0, 2.0],
        [3.0, 1.0, 0.0],
        [0.0, 2.0, 1.0],
    ])
    w = np.array([0.5, 1.0, -1.0])
    b = 0.1
    z = X @ w + b
    print("X.shape:", X.shape, "w.shape:", w.shape, "z.shape:", z.shape)
    print("z:", z)
    # Verifica: z[0] dovrebbe essere 1.0*0.5 + 0.0*1.0 + 2.0*(-1.0) + 0.1 = -1.4
    assert np.isclose(z[0], -1.4), "qualcosa non torna nel dot product"


# TODO 2.1 (8 minuti):
# Scrivi una funzione "punteggio_batch(X, w, b)" che:
#   - prende X di shape (N, d), w di shape (d,), b scalare
#   - alza ValueError se X.shape[1] != w.shape[0]
#   - restituisce z di shape (N,) calcolato come X @ w + b
#
# Type hint corretti (Pattern #25): np.ndarray, non np.array.
# TUO CODICE QUI:
# def punteggio_batch(...):
#     ...


# 2.2 - PERCHE' E' EQUIVALENTE A N DOT PRODUCT (verifica)
#
# La via lenta e la via veloce DEVONO dare lo stesso risultato.
# Verificalo confrontando i due output con np.allclose.

# TODO 2.2 (5 minuti):
# Usa la X e w dell'esempio sopra (o la tua funzione 2.1) e:
#   (a) calcola z_lento con un for loop su X
#   (b) calcola z_veloce con X @ w + b
#   (c) verifica con assert np.allclose(z_lento, z_veloce)
#   (d) misura i tempi con time.perf_counter() per N=10_000 pratiche random
#       (X = np.random.randn(10000, 5), w = np.random.randn(5))
# TUO CODICE QUI:
# ...


# ==========================================================================
# SEZIONE 3 - ANTEPRIMA LAYER DENSE (M3)
# ==========================================================================

# ---------------------- ANALOGIA --------------------------------------------
# Una rete neurale = sequenza di "trasformazioni affini" + funzioni
# non-lineari. Una "trasformazione affine" e' esattamente quello che hai
# appena scritto:
#
#     z = X @ W + b
#
# La differenza con la sezione 2 e' che W e' una MATRICE (non un vettore):
#
#     X.shape == (N, d)        N pratiche, d feature in input
#     W.shape == (d, h)        d feature -> h "neuroni" (output dim)
#     b.shape == (h,)          un bias per neurone
#     ----------------------------- @ + broadcast
#     z.shape == (N, h)        N pratiche, h "punteggi" ognuna
#
# Pensa a "h" come "h diversi modi di guardare la stessa pratica":
#   - neurone 1: focus sull'importo -> contribuisce molto se importo grande
#   - neurone 2: focus su tasse/contributi -> contribuisce se squilibrio
#   - ...
# Sono "esperti" specializzati. La rete IMPARA W e b dai dati.

# ---------------------- TEORIA + CODICE -------------------------------------
# 3.1 - LAYER DENSE FORWARD (senza attivazione)

def _esempio_layer_dense() -> None:
    rng = np.random.default_rng(seed=42)
    X = rng.standard_normal(size=(4, 5))       # 4 pratiche, 5 feature
    W = rng.standard_normal(size=(5, 3))       # 5 feature -> 3 neuroni
    b = np.zeros(shape=(3,))                   # 1 bias per neurone
    z = X @ W + b                              # (4, 3)
    print("X:", X.shape, "W:", W.shape, "b:", b.shape, "-> z:", z.shape)
    print("z:\n", z)


# TODO 3.1 (8 minuti):
# Scrivi una funzione "layer_dense(X, W, b)" che:
#   - prende X (N, d), W (d, h), b (h,) o scalare
#   - alza ValueError se X.shape[1] != W.shape[0]
#   - restituisce z di shape (N, h)
#
# Bonus: aggiungi un parametro "attivazione" che applica una funzione
# element-wise al risultato (es. lambda x: np.maximum(0, x) per ReLU).
# Default: identita' (nessuna attivazione).
# TUO CODICE QUI:
# def layer_dense(...):
#     ...


# 3.2 - PERCHE' "DENSE"?
# "Dense" significa "ogni neurone vede TUTTE le feature in input".
# Cioe' la matrice W non ha zeri obbligati: ogni colonna di W
# (= un neurone) e' un vettore di pesi che combina TUTTE le d feature.
# Contrari: "sparse" o "convolutional" (M3 cap.05+: ogni neurone vede solo
# alcuni input, tipico per immagini).

# TODO 3.2 (5 minuti):
# Usa la tua layer_dense con:
#   X = matrice 4x5 random (seed 42)
#   W = matrice 5x2 con valori specifici: W = [[1, 0], [0, 1], [0, 0], [0, 0], [0, 0]]
#   b = [0, 0]
# Cosa stampa il risultato? Cosa "fa" questo layer? (suggerimento: estrae
# le prime 2 colonne di X). Spiega in 1 riga commentata.
# TUO CODICE QUI:
# ...


# ==========================================================================
# QUIZ DI VERIFICA (fai PRIMA di passare agli esercizi)
# ==========================================================================

# V1) X ha shape (100, 5), w ha shape (5,). Che shape ha X @ w?
# TUA RISPOSTA:
# ...

# V2) X ha shape (100, 5), W ha shape (5, 3), b ha shape (3,). Che shape
#     ha X @ W + b? E quante "operazioni di moltiplicazione" sono state
#     fatte sotto, in totale?
# TUA RISPOSTA:
# ...

# V3) [Trova l'errore] Questo codice da' ValueError. Perche'?
#       X = np.random.randn(100, 5)
#       w = np.random.randn(3)
#       z = X @ w
# TUA RISPOSTA:
# ...

# V4) [Trova l'errore] Stessa X di V3. Cosa stampa questo codice?
#       z = X @ w + (0.1,)
#     Qual e' il PROBLEMA stilistico? (suggerimento: pattern #23)
# TUA RISPOSTA:
# ...

# V5) Vero o Falso, e perche':
#     "Un layer Dense di una rete neurale e' matematicamente identico a
#      una regressione lineare con piu' output."
# TUA RISPOSTA:
# ...

# V6) Perche' X @ w (1 operazione) e' MOLTO piu' veloce di un for loop con
#     N dot product separati? Da' almeno 2 motivi.
# TUA RISPOSTA:
# ...

# V7) Hai una matrice X (10, 5) e una W (5, 3). Quale di queste righe ha
#     l'operazione INVERSA che ti riallinea per fare W @ X?
#       (a) X.T @ W
#       (b) W @ X.T
#       (c) (X @ W).T
# TUA RISPOSTA:
# ...

# V8) [Feynman] Spiega con parole tue, come a un collega web dev: cosa
#     significa "una rete neurale e' sequenza di prodotti matrice-vettore"?
#     Niente formule, niente termini tecnici - solo analogia.
# TUA RISPOSTA:
# ...


# ==========================================================================
# ESERCIZI FINALI
# ==========================================================================
#
# E1) [COLLOQUIO] - 15 minuti
#     Implementa "softmax(z)" che dato un vettore (h,) restituisce un
#     vettore (h,) di probabilita' (somma a 1, tutti positivi). E' la
#     "predict_proba" di un classificatore multi-classe nelle reti neurali.
#     Formula in parole: per ogni elemento, esponenziale, poi dividi per
#     la somma di tutte le esponenziali.
#     Tip anti-overflow: sottrai prima il max(z).
#     Verifica con z = [1, 2, 3] -> output ~ [0.09, 0.245, 0.665]
# TUO CODICE QUI:
# def softmax(z: np.ndarray) -> np.ndarray:
#     ...


# E2) [REFACTORING]
#     Questo codice funziona ma e' brutto. Riscrivilo seguendo le regole
#     del cap.02:
#       - usa np.ndarray nei type hint (Pattern #25)
#       - niente virgole spurie a fine riga (Pattern #23)
#       - nessun loop Python: usa l'algebra vettoriale
#       - una funzione pulita con docstring e ValueError dove serve
#
#     def calcola_punteggi(X, w, b):
#         out = []
#         for i in range(len(X)),:
#             tot = 0
#             for j in range(len(X[i])),:
#                 tot += X[i][j] * w[j]
#             out.append(tot + b),
#         return np.array(out),
#
# TUO CODICE QUI:
# ...


# E3) [DEBUG] - autonomo, niente scala progressiva (regola corso)
#     Questo codice da' "ValueError: shapes (100,5) and (3,) not aligned".
#     Trova IL bug PRIMA di guardare i suggerimenti.
#
#     X = np.random.randn(100, 5)
#     w = np.random.randn(3)
#     z = X @ w
#
#     Quando hai trovato il bug, scrivi qui sotto:
#       - cosa hai diagnosticato (1 riga)
#       - come l'hai sistemato (1 riga di codice corretto)
# TUA RISPOSTA / FIX:
# ...


# E4) [RETRIEVAL] - senza guardare il cap.01 Ponte
#     Riscrivi da zero la funzione "coseno(a, b) -> float" senza guardare
#     come l'avevi fatta. Deve avere:
#       - type hint corretti (np.ndarray, non np.array)
#       - controllo shape
#       - controllo norma zero
#       - cast esplicito a float
#     Verifica con a = [1, 2] e b = [2, 4] -> deve dare 1.0.
# TUO CODICE QUI:
# def coseno_v2(...) -> float:
#     ...


# E5) [INTERLEAVING] cap.06 M2 + cap.02 Ponte
#     Nel cap.06 M2 hai calcolato "motivi_top3" come x_scaled * coef per
#     UNA pratica. Adesso hai la matrice X (5 pratiche), il vettore coef
#     (5 pesi), lo scaler gia' fatto. Calcola la matrice "contribuzioni"
#     di shape (5, 5) dove contribuzioni[i, j] = X_scaled[i, j] * coef[j].
#
#     Cosa serve: il broadcasting di NumPy.
#     Quando moltiplichi X_scaled (5, 5) per coef (5,):
#       NumPy "stiracchia" coef a (5, 5) replicandolo per riga, poi fa
#       l'operazione element-wise. NIENTE LOOP.
#
#     Verifica: per ogni riga i, contribuzioni[i].sum() + intercept_
#     deve coincidere con (X_scaled @ coef + intercept_)[i].
# TUO CODICE QUI:
# ...


# ==========================================================================
# MINI-PROGETTO GUIDATO - "classifica_batch"
# ==========================================================================
#
# OBIETTIVO: data una matrice X di N pratiche, un vettore w di pesi e
# un bias b, calcola in UN solo prodotto matrice-vettore i punteggi di
# tutte le pratiche e poi ordinale dalla piu' "alterata" alla piu'
# "genuina". Niente loop di calcolo, solo loop opzionale di stampa.
#
# Firma:
#     def classifica_batch(
#         X: np.ndarray,            # (N, d)
#         w: np.ndarray,            # (d,)
#         b: float,
#         k: int = 5,
#     ) -> list[tuple[int, float]]:
#         ...
#         return top_k_pratiche  # [(indice_riga, punteggio), ...]
#
# Vincoli:
#   - alza ValueError se X.shape[1] != w.shape[0]
#   - alza ValueError se k < 1 o k > N
#   - usa X @ w + b (1 sola operazione)
#   - ordina decrescente per punteggio (le piu' "alterate" prima)
#   - restituisci esattamente k elementi
#
# Verifica: passa una X (10, 3) random, w random, b = 0.0.
# La funzione deve restituire 5 tuple ordinate decrescente.
#
# TUO CODICE QUI:
# def classifica_batch(...):
#     ...


# ==========================================================================
# CHECKPOINT FINALE (auto-verifica)
# ==========================================================================
#
# C1) Hai una X di shape (1000, 5). Quanti dot product calcola "X @ w" con
#     w di shape (5,)? Quanti scalari ha l'output?
# TUA RISPOSTA:
# ...

# C2) [Feynman] Spiega in una frase a un collega web dev: "Perche' un layer
#     Dense lo chiamiamo 'matematicamente uguale' a una regressione lineare
#     ripetuta h volte?"
# TUA RISPOSTA:
# ...

# C3) Cosa stampa "X[5]" se X.shape == (100, 3)? E "X[5:6]"? Quale e' 1D
#     e quale e' 2D? (Tranello [M6])
# TUA RISPOSTA:
# ...

# C4) Auto-rating onesto (compila in chiusura capitolo):
#       - matrici e shape (N, d):     /10
#       - prodotto matrice-vettore:    /10
#       - layer Dense (anteprima M3):  /10
#       - ripasso 5 blocchi cap.01:    /10
#       - rinforzi pattern #23/24/25:  /10
# TUE RISPOSTE:
# ...


# ==========================================================================
# SOLUZIONI QUIZ (NON BARARE - leggi solo dopo aver risposto)
# ==========================================================================
"""
QUIZ D'INGRESSO

Q1) np.linalg.norm([3, 4]) restituisce 5.0.
    Perche' applica la formula della norma euclidea L2:
        sqrt(3*3 + 4*4) = sqrt(9 + 16) = sqrt(25) = 5
    E' "il teorema di Pitagora" applicato a un vettore 2D.

Q2) coseno(a, b) = 1.0 perche' b = 2*a (stessa direzione, lunghezza diversa).
    Il coseno misura SOLO direzione: la moltiplicazione per uno scalare
    positivo non cambia il coseno (la grandezza viene "normalizzata via").

Q3) np.dot([1,2,3],[4,5,6]) restituisce uno SCALARE.
    Valore: 1*4 + 2*5 + 3*6 = 4 + 10 + 18 = 32.

Q4) FALSO. Coseno = 1 significa "stessa direzione", NON "stesso valore".
    Esempio: a = [1,2,3] e b = [10,20,30] hanno coseno = 1 ma sono
    diversissimi come grandezza. Per uguaglianza serve anche stessa norma.

Q5) np.array([1, 2, 3]).shape vale (3,) - e' 1D.
    Per ottenere (1, 3) servirebbe np.array([[1, 2, 3]]) (doppia parentesi).
    Importa perche' molte funzioni (predict_proba, layer Dense) si aspettano
    una shape 2D, non 1D.

Q6) Corretto e' "v: np.ndarray". np.array e' una FUNZIONE che CREA un
    ndarray, non un tipo. Type hint stricter: numpy.typing.NDArray.

Q7) Errore: .iloc accetta solo indici NUMERICI, non etichette stringa.
    Fix: df.loc[0, "a"]  oppure  df.iloc[0]["a"]  oppure  df["a"].iloc[0]

Q8) (Feynman) Risposta tipo:
    "La norma di un vettore e' la sua lunghezza, come la diagonale di un
    rettangolo se i numeri fossero le sue coordinate. Il coseno fra due
    vettori dice quanto due 'frecce' puntano nella stessa direzione,
    indipendentemente da quanto sono lunghe. Coseno alto = stesso 'gusto',
    norma alta = grande intensita'."


QUIZ DI VERIFICA

V1) (100,) - un punteggio per ognuna delle 100 pratiche.

V2) (100, 3) - 100 pratiche, ognuna con 3 punteggi (uno per neurone).
    Moltiplicazioni totali: 100 * 5 * 3 = 1500 (ogni elemento di output
    e' un dot product di lunghezza 5).

V3) X.shape[1] = 5 ma w.shape[0] = 3. La regola [M2] dice che le colonne
    di X (5) DEVONO uguagliare le righe di w (3). 5 != 3 -> errore.

V4) Stampa una tupla "(z, 0.1)" o un errore di shape (dipende). Il problema
    stilistico e' il pattern #23: "(0.1,)" e' una TUPLA, non uno scalare.
    NumPy potrebbe accettarla ma e' fragile. Scrivi "+ 0.1" senza virgole.

V5) VERO. Un layer Dense di output dim h e' h regressioni lineari in
    parallelo che condividono l'input X. La differenza con sklearn:
    nelle reti neurali si applica poi una funzione non-lineare ("attivazione")
    e si concatenano piu' layer.

V6) (a) NumPy esegue il calcolo in C compilato, non in Python interpretato
    (il loop Python e' ~50x piu' lento per overhead).
    (b) NumPy puo' parallelizzare (BLAS, AVX/SIMD) e in M3 spostare tutto
    sulla GPU. Un loop Python e' single-thread su CPU.
    (c) Memoria: NumPy lavora su array contigui in cache, il loop Python
    fa "object dispatch" su ogni elemento.

V7) (b) W @ X.T  perche' W ha shape (5, 3) e X.T ha shape (5, 10) ->
    funziona se invertiamo l'ordine? No: per W @ X.T servono colonne_W
    (= 3) uguali a righe_X.T (= 5). Quindi NON funziona neanche cosi'.
    L'unica che ha shape "valide" e' (c) (X @ W).T = (3, 10).
    -> Risposta corretta: (c).

V8) (Feynman) Risposta tipo:
    "E' come un foglio Excel di trasformazioni: in input hai una tabella
    di clienti (X), in mezzo hai una tabella di pesi (W), e ad ogni
    passaggio ottieni una nuova tabella derivata. Sequenza di tabelle
    moltiplicate fra loro = una rete neurale. La 'magia' della rete e'
    che impara automaticamente i pesi giusti dai dati."


CHECKPOINT FINALE

C1) X @ w con X (1000, 5) e w (5,) calcola 1000 dot product (uno per
    riga di X). L'output ha 1000 scalari, shape (1000,).

C2) (Feynman) Risposta tipo:
    "Una regressione lineare standard ha 1 output per pratica (z = x @ w + b
    con w un vettore e b uno scalare). Un layer Dense di output dim h ha
    h output per pratica (z = X @ W + b con W una matrice (d, h) e b un
    vettore (h,)). E' come avere h regressioni lineari in parallelo che
    condividono lo stesso input."

C3) X[5] e' la riga 5: shape (3,), 1D.
    X[5:6] e' la sottomatrice con SOLO la riga 5: shape (1, 3), 2D.
    Sembrano uguali ma per .predict_proba e per layer Dense conta la
    differenza (1D vs 2D).
"""


# ==========================================================================
# ENTRY POINT (esegui solo le demo che esistono nel file, niente di tuo)
# ==========================================================================
if __name__ == "__main__":
    print("=" * 70)
    print("Cap.02 Ponte - demo di riferimento (rinforzi #23, #24, #25)")
    print("=" * 70)

    print("\n[Demo Pattern #23 - virgole -> tuple]")
    _demo_pattern_23()

    print("\n[Demo Pattern #24 - iloc vs loc]")
    _demo_pattern_24()

    print("\n[Demo Pattern #25 - np.array vs np.ndarray]")
    _demo_pattern_25()

    print("\n[Demo matrice batch (Sez. 1)]")
    X_demo = _esempio_matrice()

    print("\n[Demo punteggio batch (Sez. 2)]")
    _esempio_punteggio_batch()

    print("\n[Demo layer Dense (Sez. 3)]")
    _esempio_layer_dense()

    print("\n" + "=" * 70)
    print("Demo finite. Adesso tocca a te: completa i TODO in ordine.")
    print("=" * 70)
