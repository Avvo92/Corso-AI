"""
============================================================================
MODULO 3 (DL & CV) - CAPITOLO 07
"PyTorch intro": NumPy con autograd (e GPU su Colab)
============================================================================

Dopo il cap.06 hai addestrato una rete 2-layer A MANO in NumPy:
    forward → cache → backward analitico → update GD → loop epoche.

Qui cambi SOLO lo strumento: PyTorch fa il backward da solo (autograd).
Il ciclo concettuale resta IDENTICO.

⚠️ HARDWARE: AMD Vega 10 → niente CUDA in locale.
   Workflow consigliato: codice in Cursor → copia celle su Google Colab (GPU)
   → salva pesi su Drive → riporta in locale per inferenza CPU.

Chiusura anticipata cap.06 (03/08/2026): ~3000 righe, residui NON svolti
migrati qui come blocchi 🔁 RINFORZO (quiz V, confronto 01→06, scaler,
drift, clip BCE, Pattern #27).

REVISIONE 03/08/2026 (richiesta studente): capitolo riscritto con MOLTE piu'
spiegazioni sul passaggio NumPy → PyTorch. Le tue risposte precedenti sono
state conservate parola per parola.

----------------------------------------------------------------------------
COME LEGGERE QUESTO FILE
----------------------------------------------------------------------------
Ogni sezione segue sempre lo stesso schema, per non perdere la bussola:

    [1] ANALOGIA          "come nella vita reale / nel web"
    [2] COME LO FACEVI    codice NumPy del cap.01-06 (lo conosci)
    [3] COME SI FA ORA    codice PyTorch equivalente
    [4] COSA CAMBIA       le 2-3 differenze che contano davvero
    [5] TRANELLI          gli errori che fanno TUTTI la prima volta
    [6] MINI-ESERCIZIO    2-4 righe da scrivere tu
    [7] LETTURA PARALLELA (📚)  sezione PDF consigliata — opzionale, dopo il mini

Regola d'oro del capitolo: **PyTorch non introduce concetti nuovi di
matematica**. Introduce solo un modo piu' comodo (e piu' veloce) di scrivere
le stesse cose. Se ti senti confuso, torna alla domanda:
"questa riga PyTorch quale riga NumPy del cap.06 sta sostituendo?"

----------------------------------------------------------------------------
DEFINITION OF DONE (cap.07)
----------------------------------------------------------------------------
Alla fine sai rispondere "in 1 riga" e in CODICE a:

  1) Cos'e' un Tensor vs un ndarray?                          → Sez. 1
  2) Cos'e' requires_grad / autograd / .backward()?           → Sez. 2
  3) nn.Linear = Dense del Ponte; nn.Module = contenitore     → Sez. 3
  4) Dataset + DataLoader: perche' batch + shuffle            → Sez. 4
  5) Training loop: zero_grad → forward → loss → backward → step → Sez. 5
  6) state_dict: salvare/caricare pesi                        → Sez. 6

E hai riscritto (refactor) il training del cap.06 in forma PyTorch
sul CSV M2 (progetto incrementale).

----------------------------------------------------------------------------
MAPPA DEL CAPITOLO
----------------------------------------------------------------------------
   *  QUIZ D'INGRESSO (cerniera cap.06 + residui V1-V10)   Q1 - Q8
   *  🔁 RINFORZO #42 clip BCE su p (non su z)              micro
   *  🔁 RINFORZO #43 scaler: (X-mean)/std                 micro
   *  🔁 RINFORZO Pattern #27 formula→codice               micro
   *  🔁 RINFORZO #44 sanity check = analitico vs numerico  micro
   *  DIZIONARIO NumPy → PyTorch (tabella di traduzione)
   *  SEZIONE 1  Tensori vs ndarray                        1.1 - 1.5 + mini
   *  SEZIONE 2  Autograd = backward automatico            2.1 - 2.5 + mini
   *  SEZIONE 3  nn.Module / Linear / attivazioni          3.1 - 3.4 + mini
   *  SEZIONE 4  Dataset + DataLoader                      4.1 - 4.3 + mini
   *  SEZIONE 5  Training loop standard                    5.1 - 5.4 + mini
   *  SEZIONE 6  state_dict save/load                      6.1 - 6.2 + mini
   *  🔁 CONFRONTO PRIMA/DOPO (migrato da cap.06)          prosa
   *  🔁 TODO 18-ish: StandardScaler + train               commento
   *  🔁 TODO 19-ish: drift REAL-WORLD                     ipotesi
   *  ESERCIZI: COLLOQUIO, REFACTOR, DEBUG, RETRIEVAL,
                INTERLEAVING, REAL-WORLD
   *  🏗️ PROGETTO INCREMENTALE: rete 2-layer PyTorch vs NumPy
   *  QUIZ DI VERIFICA                                     V1 - V6
   *  Soluzioni quiz
============================================================================
"""

from __future__ import annotations

# ---------------------------------------------------------------------------
# Import: NumPy sempre; torch opzionale in locale (obbligatorio su Colab)
#
# NOTA (errore reale incontrato il 03/08/2026):
#   In locale l'import di torch puo' fallire con
#       OSError: [WinError 126] ... torch_python.dll
#   che NON e' un ImportError: significa "pacchetto trovato, ma Windows non
#   riesce a caricare le librerie native". Per questo qui catturiamo
#   Exception e non solo ImportError.
#   Cause tipiche: Python molto recente (3.14), Visual C++ Redistributable
#   mancante, installazione torch corrotta. Soluzione consigliata dal corso:
#   fare le sezioni 1-6 su Google Colab.
# ---------------------------------------------------------------------------
import numpy as np
from torch.nn import BCELoss

try:
    import torch
    import torch.nn as nn
    from torch.utils.data import Dataset, DataLoader, TensorDataset
    TORCH_OK = True
except Exception as errore_torch:            # ImportError, OSError (DLL), ...
    TORCH_OK = False
    print(
        "[AVVISO] torch non utilizzabile in questo ambiente:\n"
        f"         {type(errore_torch).__name__}: {errore_torch}\n"
        "         Le sezioni 1-6 vanno eseguite su Google Colab.\n"
        "         (In locale CPU-only si puo' provare:\n"
        "          pip install torch --index-url "
        "https://download.pytorch.org/whl/cpu)"
    )

# ==========================================================================
# WORKFLOW COLAB (leggi prima di partire)
# ==========================================================================
#
# 1) Apri https://colab.research.google.com → Runtime → Cambia tipo runtime
#    → GPU (T4 o simile).
# 2) Verifica:
#       import torch
#       print(torch.__version__, torch.cuda.is_available())
# 3) Copia qui le sezioni / esercizi in celle.
# 4) Dopo il training: torch.save(model.state_dict(), "rete_m2.pt")
#    → scarica il file o salvalo su Drive.
# 5) In Cursor (CPU): model.load_state_dict(torch.load("rete_m2.pt",
#       map_location="cpu"))
#
# Analogia: Colab = "macchina da cantiere in affitto"; Cursor = "ufficio
# dove progetti i pezzi". Non serve CUDA sul tuo PC.
#
# ATTENZIONE (visto il 03/08/2026): se stampi a.device e leggi "cpu", NON e'
# un bug. I tensori nascono SEMPRE su CPU. La GPU si usa solo se:
#   (a) il runtime Colab ha l'acceleratore GPU attivo, E
#   (b) tu sposti il tensore: torch.tensor(..., device="cuda") oppure .to(dev)


# ==========================================================================
# QUIZ D'INGRESSO (Q1 - Q8) — cerniera cap.06 + residui quiz verifica
# ==========================================================================
#
# Regola: rispondi SENZA aprire il file del cap.06. Poi confronta con
# le soluzioni in fondo.
#
# Q1) Training loop in 1 riga: forward + ? + ? (+ update)
# TUA RISPOSTA:
# forward + loss + backward + update

# Q2) A cosa serve la CACHE del forward nel backward manuale?
# TUA RISPOSTA:
# Serve per avere i valori per poter calcolare le derivate nella fase di backward (Z1, H, Z2, P)

# Q3) Rete d=4, h=8, output 1. Shape di grad_W1, grad_b1, grad_W2, grad_b2?
# TUA RISPOSTA:
#  grad_W1 = (d, h)
#  grad_b1 = (h, )
#  grad_W2 = (h, 1)
#  grad_b2 = (1, )

# Q4) Sanity check del backward: cos'e' e perche' farlo PRIMA di addestrare?
# TUA RISPOSTA:
# per vedere che le funzioni contenute all'interno del training non abbiamo subito modifiche che rompano il risultato finale. Una prova del nove ci evita calcoli inutili.

# Q5) [Trova errore] dZ2 = (P - y).reshape(-1, 1)  # manca qualcosa per la
#     media di batch della BCE. Cosa?
# TUA RISPOSTA:
# P - y deriva dalla semplificazione miracoloso di dL/dp * dp/dZ2. ma dato che la loss è una media sul batch, (P-y) va diviso per N righe del batch. La formula corretta è ((P-y) / N).reshape(-1, 1)

# Q6) Dataset bilanciato, rete random: loss iniziale BCE circa quanto?
#     (pista: -log(0.5))
# TUA RISPOSTA:
# circa 0,693147

# Q7) Dopo 500 epoche loss = 0.692. Cosa pensi? (a/b/c/d come V7 cap.06)
# TUA RISPOSTA:
# Penso che qualcosa non funziona, perchè la rete dopo 500 epoche non dovrebbe produrre risultati simili a dataset bilanciate e rete random.

# Q8) 💬 Feynman: in 4-6 frasi, differenza tra backpropagation e
#     gradient descent. (Punto debole TODO 14 cap.06 — non mischiarli.)
# TUA RISPOSTA:
# Backpropagation: è la "retropropagazione dell'errore". Usando la chian rule (moltiplicazione di derivate locali), si "distribuisce l'errore" su ogni parametro della rete.
# Gradient descent: usando poi le derivate parziali prodotte dalla chian rule, si aggiornano i parametri (fase update), tramite la formula w = w - grad * lr.

# ==========================================================================
# 🔁 RINFORZO MIRATO #42 — Clip BCE su p, NON su z
# ==========================================================================
#
# Cap.06 TODO 17: per stabilizzare log(p) hai messo np.clip su z (logit).
# z e' un numero reale qualunque (−∞…+∞). Il clip bilaterale serve su p
# (probabilita' in (0,1)) PRIMA del log.
#
# Analogia: non "tagli" la temperatura del forno se il problema e' il
# termometro fuori scala: tagli la LETTURA del termometro (p), non il fuoco (z).
#
# Micro 42.A — completa (una riga ciascuna):
#   p_safe = np.clip(p, eps, 1 - eps)
#   loss = -np.mean(y * np.log(p_safe) + (1 - y) * np.log(1 - p_safe))
#
# Micro 42.B — V/F: "clippare z in [eps, 1-eps] e' equivalente a clippare p".
# TUA RISPOSTA:
# Falso. nell formula della BCE usiamo p, e lo clippiamo per evitare di avere -log(0) e - log(1), i quali produrrebbero inf e nan.
#
# ⭐ ANTICIPO UTILE (vedi Sez.3): in PyTorch questo problema si risolve
#    strutturalmente usando `nn.BCEWithLogitsLoss()`, che prende in input i
#    LOGIT (z) e applica la sigmoid *dentro* la loss in modo numericamente
#    stabile. In pratica: il "clip" non lo scrivi piu' tu, ma il motivo per
#    cui serve resta esattamente quello che hai scritto sopra.

# ==========================================================================
# 🔁 RINFORZO MIRATO #43 — Scaler: (X - mean) / std  (parentesi!)
# ==========================================================================
#
# Cap.06 TODO 16/18: hai scritto X - mean / std.
# In Python: / ha precedenza su − → diventa X - (mean/std), NON standardizzato.
#
# Micro 43.A — correggi a mente, poi verifica con codice:
mean_demo = np.array([10.0, 20.0])
std_demo = np.array([2.0, 5.0])
X_demo = np.array([[12.0, 25.0], [8.0, 15.0]])
# SBAGLIATO (precedenza):
X_wrong = X_demo - mean_demo / std_demo
# CORRETTO:
X_right = (X_demo - mean_demo) / std_demo
print("43.A wrong[0]=", X_wrong[0], "right[0]=", X_right[0])
# Commenta in 1 riga: perche' i due risultati sono diversi?
# TUA RISPOSTA:
# Per via della precedenza sulle operazioni. I risultati della sottrazioni devo poi dopo essere divisi, ma dato che non avevamo messo le parentesi la precedenza veniva sballata.

# Micro 43.B — std==0: cosa metti al posto dello 0 per non dividere per zero?
# TUA RISPOSTA:
# Mettiamo 1.0


# ==========================================================================
# 🔁 RINFORZO MIRATO Pattern #27 — formula → codice (simbolo per simbolo)
# ==========================================================================
#
# Errori tipici: * vs @, * vs /, parentesi al denominatore, == vs =.
#
# Micro 27.A — riscrivi in NumPy (senza moltiplicazione implicita tipo p(1-p)):
#   dL/dp = (p - y) / (p * (1 - p))
# TUA CODICE (1 riga, p e y array):

print("\nRINFORZO MIRATO Pattern 27\n")

p = np.array([.68, .23], dtype=float)
y = np.array([1, 0], dtype=float)

dL_dp = (p - y) / (p * (1 - p))

print(dL_dp)

# Micro 27.B — quale e' corretto per hidden @ pesi output?
#   (a) H * W2   (b) H @ W2   (c) W2 @ H
# TUA RISPOSTA:
# (b)
#
# PROMEMORIA ANTI-#27 (vale per tutto il capitolo):
#   1. leggi la formula UN SIMBOLO ALLA VOLTA;
#   2. denominatore sempre tra parentesi;
#   3. dopo aver scritto la riga, rileggi solo i NOMI delle variabili
#      (l'errore di ieri era `(1 - y)` al posto di `(1 - p)`: formula giusta,
#      variabile sbagliata);
#   4. quando puoi, chiudi con un assert.


# ==========================================================================
# 🔁 RINFORZO MIRATO #44 — Cos'e' ESATTAMENTE un sanity check
# ==========================================================================
#
# Nel quiz Q4 hai detto "prova del nove per non fare calcoli inutili":
# giusto come SPIRITO, ma manca il MECCANISMO. Fissiamolo con un esempio
# minuscolo (nessuna rete, solo una funzione).
#
# Sanity check del gradiente = confrontare DUE modi di calcolare la stessa
# derivata:
#   (a) ANALITICO  → la formula che hai derivato a mano (veloce, ma sbagliabile)
#   (b) NUMERICO   → differenza centrata (lento, ma quasi impossibile sbagliare)
# Se coincidono → il backward e' corretto. Se no → c'e' un bug, e addestrare
# sarebbe tempo buttato.


def f_demo(x: float) -> float:
    """Funzione di prova: f(x) = 3x^2 + 2x."""
    return 3.0 * x ** 2 + 2.0 * x


def derivata_analitica_demo(x: float) -> float:
    """Derivata a mano: f'(x) = 6x + 2."""
    return 6.0 * x + 2.0


def derivata_numerica_demo(f, x: float, h: float = 1e-6) -> float:
    """Differenza centrata: (f(x+h) - f(x-h)) / (2h). Attenzione: 2*h, non 2/h."""
    return (f(x + h) - f(x - h)) / (2.0 * h)


_x0 = 2.0
_an = derivata_analitica_demo(_x0)
_nu = derivata_numerica_demo(f_demo, _x0)
print(f"\n44 sanity check: analitico={_an:.6f} numerico={_nu:.6f}")
assert np.isclose(_an, _nu, atol=1e-5), "backward/derivata da correggere!"
print("44 sanity check: OK (i due metodi coincidono)")

# Micro 44.A — riscrivi in 1 frase la definizione operativa di sanity check
#              usando le parole "analitico" e "numerico".
# TUA RISPOSTA:
# il sanity check tra analitico e numerico serve perchè la formula della derivata analitica è rigorosa ma sbagliabile, invece la numerica è lenta ma praticamente sempre esatta. Se i valori coincidono, allora la derivata analitica è corretta, e si può procedere con l'addestramento.
#
# Micro 44.B — in PyTorch il sanity check "manuale" quasi non serve piu'.
#              Perche'? (1 frase; pista: chi calcola i gradienti?)
# TUA RISPOSTA:
# Perchè i gradienti sono gestiti direttamente da pytorch, quindi molto improbabile che si sbagli
#
# (Per curiosita': PyTorch ha comunque `torch.autograd.gradcheck`, usato
#  quando ti scrivi un layer custom. Stesso principio, automatizzato.)


# ==========================================================================
# DIZIONARIO NumPy → PyTorch  (la "Rosetta Stone" del capitolo)
# ==========================================================================
def dizionario():
    return
# Tieni questa tabella a portata di mano: il 90% della confusione iniziale
# e' solo vocabolario.
#
#   CONCETTO                 NumPy (cap.01-06)          PyTorch (cap.07)
#   -----------------------  -------------------------  ------------------------
#   contenitore di numeri    np.ndarray                 torch.Tensor
#   creare zeri              np.zeros((4,3))            torch.zeros(4, 3)
#   creare random normale    rng.standard_normal(...)   torch.randn(...)
#   tipo dei numeri          dtype=np.float32           dtype=torch.float32
#   forma                    a.shape                    t.shape  (uguale!)
#   prodotto matriciale      A @ B                      A @ B    (uguale!)
#   element-wise             A * B                      A * B    (uguale!)
#   trasposta                A.T                        A.T / A.t()
#   somma su asse            a.sum(axis=0)              t.sum(dim=0)   ← axis→dim
#   media                    a.mean()                   t.mean()
#   reshape                  a.reshape(-1, 1)           t.reshape(-1, 1) / view
#   da (N,1) a (N,)          a.ravel() / a[:,0]         t.squeeze(-1)
#   copia in numpy           —                          t.detach().cpu().numpy()
#   scalare Python           float(a)                   t.item()
#   dove vive il dato        (sempre RAM/CPU)           t.device  ("cpu"/"cuda:0")
#   -----------------------  -------------------------  ------------------------
#   LOSS BCE                 tua bce_loss(p, y)         nn.BCELoss()(p, y)
#                                                       nn.BCEWithLogitsLoss()(z,y)
#   layer Dense              X @ W + b                  nn.Linear(d, h)
#   ReLU                     np.maximum(0, z)           torch.relu(z)
#   sigmoid                  1/(1+np.exp(-z))           torch.sigmoid(z)
#   -----------------------  -------------------------  ------------------------
#   BACKWARD                 lo scrivi TU (5 step)      loss.backward()
#   gradiente di un peso     grad_W1 (array che crei)   W1.grad (lo riempie torch)
#   UPDATE                   W -= lr * grad_W           optimizer.step()
#   azzerare i gradienti     (non serve: li ricrei)     optimizer.zero_grad()  ⚠️
#
# LE UNICHE 3 COSE VERAMENTE NUOVE:
#   1) device        → il dato puo' stare su CPU o GPU
#   2) autograd      → i gradienti li calcola il framework
#   3) zero_grad     → i gradienti si ACCUMULANO, quindi vanno svuotati
#
# Tutto il resto e' NumPy con un altro nome.


# 📚 LETTURA PARALLELA — [PYTORCH] cap. 3–4 + [GERON] cap. 12 (intro tensori)
# Dopo aver letto il dizionario sopra, apri i PDF e confronta le tabelle
# NumPy↔torch con quelle del libro. Il libro PyTorch spiega anche `device`
# e la differenza float32/float64 con piu' esempi.
# Domanda guida: quali 2 voci del dizionario trovi anche nel libro con un
# nome leggermente diverso? (es. axis → dim)
# TUA RISPOSTA (opzionale, 1-3 righe):
#


# --------------------------------------------------------------------------
# Da qui in poi serve torch: se non e' disponibile in locale, fermiamoci
# con un messaggio chiaro invece di far esplodere il file.
# --------------------------------------------------------------------------
if not TORCH_OK:
    print(
        "\n[STOP LOCALE] I rinforzi NumPy sopra sono stati eseguiti.\n"
        "              Le SEZIONI 1-6 richiedono torch: aprile su Colab.\n"
    )
    raise SystemExit(0)


# ==========================================================================
# SEZIONE 1 — Tensori PyTorch vs ndarray NumPy
# ==========================================================================
#
# ---------- [1] ANALOGIA --------------------------------------------------
# ndarray  = un foglio Excel di numeri, in un cassetto del tuo ufficio (RAM).
# Tensor   = lo STESSO foglio, ma con due superpoteri:
#            (a) puoi spostarlo in un altro ufficio piu' potente (la GPU);
#            (b) se glielo chiedi, tiene il registro di cio' che gli fai
#                (serve per le derivate — Sezione 2).
#
# Nel mondo web: come passare da un array PHP in memoria a un record che
# vive su un server dedicato e tiene un log delle modifiche.
#
# ---------- [2] COME LO FACEVI (cap.01-06) --------------------------------
#   X = np.zeros((4, 3), dtype=np.float32)
#   H = np.maximum(0, X @ W1 + b1)
#
# ---------- [3] COME SI FA ORA --------------------------------------------
#   X = torch.zeros(4, 3)                  # float32 di default
#   H = torch.relu(X @ W1 + b1)
#
# Nota che `@`, `+`, broadcasting, `.shape`: IDENTICI a NumPy.

print("\n=== SEZIONE 1 — tensori ===")

# 1.1 — creare tensori (i 4 modi che userai davvero)
t_zeri = torch.zeros(4, 3)                     # zeri, float32
t_uni = torch.ones(2, 2)                       # uni
t_rand = torch.randn(3, 2)                     # normale standard (media 0, std 1)
t_lista = torch.tensor([[1.0, 2.0], [3.0, 4.0]])   # da lista Python
print("1.1 shape/dtype/device:", t_zeri.shape, t_zeri.dtype, t_zeri.device)

# 1.2 — dtype: il tranello numero 1 del passaggio da NumPy
#
# NumPy crea float64 per default. PyTorch lavora in float32 per default
# (meta' memoria, doppia velocita' su GPU). Se mischi i due, ottieni errori
# tipo: "expected scalar type Float but found Double".
arr64 = np.array([1.0, 2.0])                   # float64!
t_da64 = torch.tensor(arr64)                   # → torch.float64
t_ok32 = torch.tensor(arr64, dtype=torch.float32)
print("1.2 dtype da numpy:", t_da64.dtype, "| forzato:", t_ok32.dtype)
#
# REGOLA PRATICA: quando porti dati da NumPy/Pandas verso PyTorch, converti
# SEMPRE in float32:
#     X_np.astype(np.float32)      oppure     torch.tensor(X_np, dtype=torch.float32)

# 1.3 — from_numpy vs tensor: copia o memoria condivisa?
arr_shared = np.array([1.0, 2.0, 3.0], dtype=np.float32)
t_shared = torch.from_numpy(arr_shared)        # CONDIVIDE la memoria
t_copy = torch.tensor(arr_shared)              # COPIA
arr_shared[0] = 99.0
print("1.3 from_numpy (condivisa):", t_shared, "| tensor (copia):", t_copy)
#
# Quando usare cosa:
#   from_numpy → dataset grossi, vuoi evitare di duplicare la RAM
#   tensor     → vuoi essere sicuro che nessuno ti cambi i dati sotto i piedi

# 1.4 — tornare a NumPy (per Matplotlib, sklearn, Pandas...)
t_qualunque = torch.randn(3)
arr_di_ritorno = t_qualunque.detach().cpu().numpy()
print("1.4 tensor → numpy:", type(arr_di_ritorno).__name__, arr_di_ritorno.shape)
#
# Perche' quella catena di 3 metodi?
#   .detach()  stacca il tensore dal registro delle derivate (altrimenti errore)
#   .cpu()     lo riporta dalla GPU alla RAM (se era su GPU)
#   .numpy()   converte
# In locale su CPU senza gradienti bastano `.numpy()`, ma la catena completa
# funziona SEMPRE: imparala cosi' e non ci pensi piu'.

# 1.5 — device: dove vive il tensore
device = "cuda" if torch.cuda.is_available() else "cpu"
t_sul_device = torch.zeros(2, 2, device=device)
print(f"1.5 device scelto: {device} | tensor su: {t_sul_device.device}")
#
# ⚠️ TRANELLO: puoi fare operazioni SOLO tra tensori sullo STESSO device.
#    Se il modello e' su GPU e i dati su CPU → RuntimeError "expected all
#    tensors to be on the same device". La fix e' sempre `.to(device)`.

# ---------- [5] TRANELLI DELLA SEZIONE 1 ----------------------------------
#   T1) float64 di NumPy vs float32 di PyTorch     → converti con astype
#   T2) `axis=` non esiste, si chiama `dim=`
#   T3) .numpy() su tensore con gradienti          → serve .detach()
#   T4) tensori su device diversi                  → .to(device)
#   T5) shape (N,1) vs (N,)                        → .squeeze(-1), come in cap.06

# Mini 1.1 — Crea un tensor float32 shape (4, 3) di zeri su CPU.
# TUO CODICE:
a = torch.tensor(np.zeros((4, 3), dtype=np.float32))
# [valutato 8.5/10 — corretto; versione idiomatica: torch.zeros(4, 3)]

# Mini 1.2 — Converti un ndarray (5,) in tensor e stampa .shape.
# TUO CODICE:
arr_numpy = np.array([1, 2, 3, 4, 5], dtype=np.float32)
print(type(arr_numpy))
arr_torch = torch.tensor(arr_numpy)
print(type(arr_torch))
# [valutato 6.5/10 — la consegna chiedeva .shape, non type(): aggiungi la riga]

# Mini 1.3 — (nuovo) Prendi X_demo (float64, definito nel rinforzo #43),
#            convertilo in tensor float32 e stampa shape + dtype.
# TUO CODICE:
X_demo = np.array([[12.0, 25.0], [8.0, 15.0]])
X_tensor = torch.tensor(X_demo, dtype=torch.float32)

print(X_tensor.shape)
print(X_tensor.dtype)

# Mini 1.4 — (nuovo) Crea due tensori (2,3) e (3,2) e moltiplicali con @.
#            Che shape ti aspetti PRIMA di stampare?
# TUO CODICE:

tensor_1 = torch.rand(2, 3)
tensor_2 = torch.rand(3, 2)

product = tensor_1 @ tensor_2

# shape attesa == (2, 2)

print(product.shape)

# ==========================================================================
# SEZIONE 2 — Autograd: il "nastro" che sostituisce il backward manuale
# ==========================================================================
#
# ---------- [1] ANALOGIA --------------------------------------------------
# Nel cap.06 tenevi la CACHE: ti segnavi a mano Z1, H, Z2, P perche' ti
# servivano dopo, nel backward. Era come conservare gli scontrini dei pezzi
# per poter fare il reso.
#
# Autograd fa la stessa cosa, ma automaticamente e COMPLETAMENTE: registra
# ogni operazione che fai su un tensore "sorvegliato" (requires_grad=True),
# costruendo un grafo. Quando chiami .backward(), ripercorre quel grafo
# all'indietro applicando la chain rule al posto tuo.
#
# In una frase da colloquio: "autograd e' la backpropagation automatica".
#
# ---------- [2] COME LO FACEVI (cap.06) -----------------------------------
#   P, cache = forward_2layer(X, W1, b1, W2, b2)
#   dZ2 = (P - y).reshape(-1, 1) / N
#   grad_W2 = cache["H"].T @ dZ2
#   dH = dZ2 @ W2.T
#   dZ1 = dH * (cache["Z1"] > 0)
#   grad_W1 = X.T @ dZ1
#   ... 5 step scritti a mano, ogni volta ricontrollati col sanity check
#
# ---------- [3] COME SI FA ORA --------------------------------------------
#   loss.backward()      # ...e basta. I gradienti finiscono in W1.grad, ecc.
#
# ---------- [4] COSA CAMBIA DAVVERO ---------------------------------------
#   (a) non scrivi piu' le derivate → meno bug (Pattern #27 respira);
#   (b) i gradienti NON stanno in variabili tue, stanno in `.grad` dei tensori;
#   (c) `.grad` si ACCUMULA (si somma) tra chiamate → va azzerato.

print("\n=== SEZIONE 2 — autograd ===")

# 2.1 — il caso minimo: una moltiplicazione
w = torch.tensor(2.0, requires_grad=True)   # "sorveglia questo numero"
x = torch.tensor(3.0)                       # dato: non serve gradiente
y_out = (w * x) ** 2                        # y = (2*3)^2 = 36
y_out.backward()                            # calcola dy/dw
print("2.1 y =", y_out.item(), "| dy/dw =", w.grad.item())
#
# Verifica a mano (chain rule del cap.05):
#   y = u^2  con u = w*x  →  dy/du = 2u = 2*6 = 12 ;  du/dw = x = 3
#   dy/dw = 12 * 3 = 36  ✓  (coincide con w.grad)

w_1 = np.array([2.0], dtype=float)
x_1 = np.array([3.0], dtype=float)
eps = 1e-6

f_1 = lambda x: x**2
f_2 = lambda w: w*x_1

derivata_numerica = (f_1(f_2(w_1 + eps)) - f_1(f_2(w_1 - eps))) / (2.0 * eps)

assert np.isclose(w.grad.item(), derivata_numerica), "Ops, qualcosa è andato storto!"

# 2.2 — requires_grad: chi e' "sorvegliato"
peso = torch.tensor([1.0, 2.0], requires_grad=True)   # PARAMETRO → sorvegliato
dato = torch.tensor([5.0, 7.0])                       # DATO     → no
print("2.2 requires_grad:", peso.requires_grad, dato.requires_grad)
#
# Regola: requires_grad=True va sui PARAMETRI da imparare (W, b), non sui dati.
# Con nn.Module (Sezione 3) non lo scrivi nemmeno: i parametri lo hanno di serie.

# 2.3 — l'accumulo dei gradienti (il tranello piu' frequente in assoluto)
q = torch.tensor(1.0, requires_grad=True)
for passo in range(3):
    perdita = q ** 2            # dL/dq = 2q = 2
    perdita.backward()          # NON azzeriamo: guarda cosa succede
    print(f"2.3 dopo backward #{passo + 1}: q.grad = {q.grad.item()}")
# Output: 2, 4, 6 → i gradienti si SOMMANO.
# Ecco perche' nel training loop esiste optimizer.zero_grad() (Sezione 5).
q.grad = None                    # azzerare "a mano" (equivalente a zero_grad)

# 2.4 — no_grad: quando NON vuoi il registro
with torch.no_grad():
    # dentro questo blocco autograd non registra nulla:
    # meno memoria, piu' velocita'. Si usa in VALUTAZIONE/inferenza.
    prova = peso * 2
print("2.4 dentro no_grad, requires_grad del risultato:", prova.requires_grad)

# 2.5 — 🔁 ponte esplicito con la CACHE del cap.06
#
#   cap.06: cache = {"Z1": Z1, "H": H, "Z2": Z2, "P": P}   ← la scrivevi tu
#   cap.07: il grafo di autograd                            ← lo scrive torch
#
# Stessa idea (conservare l'informazione del forward per il backward),
# due livelli di automazione. Non e' magia: e' contabilita'.

# Mini 2.1 — Calcola a mano dy/dw per y = (w+1)^2 in w=1, poi verifica
#            con autograd (requires_grad=True).
# TUO CODICE:

w_np = 1.0
y_np = (w_np+1)**2
der_ana = float(2*(w_np+1))

w_tch = torch.tensor(1.0, requires_grad=True)
y_tch = (w_tch+1)**2
y_tch.backward()

assert np.isclose(der_ana, w_tch.grad.item()), "Ops, qualcosa è andato"

print(der_ana)
print(w_tch.grad.item())

# Mini 2.2 — 💬 In 2 frasi: cosa sostituisce autograd rispetto al cap.06?
# TUA RISPOSTA:
# sostituisce la cache e le derivate parziali calcolate a mano usando la chian rule. Non sostituisce il gradiente descent.

# Mini 2.3 — (nuovo) Perche' `q.grad` valeva 2, poi 4, poi 6 in 2.3?
#            Rispondi in 1 riga usando la parola "accumulo".
# TUA RISPOSTA:
# Perchè .grad accumula (somma) i gradienti effettuati in ogni ciclo.

# 📚 LETTURA PARALLELA — [PYTORCH] 1ª ed. cap. 5 "The mechanics of learning"
# Scheda: docs/libri_corso/schede/M03_C07_sez2_5_puntatori.md
# Dopo i mini: sfoglia il cap.5 e collega "autograd" a "non derivare a mano".
# Domanda guida: in 1 frase, cosa sostituisce autograd rispetto al backward
# del tuo cap.06? (pista: cache + derivate locali)
# TUA RISPOSTA (opzionale):
#

# ==========================================================================
# SEZIONE 3 — nn.Module, nn.Linear, attivazioni
# ==========================================================================
#
# ---------- [1] ANALOGIA --------------------------------------------------
# nn.Linear = il layer Dense che hai costruito a mano nel Ponte Matematico.
# nn.Module = la "scatola" (classe) che tiene insieme i layer e sa dirti
#             quali sono i suoi parametri. Come un Controller Laravel che
#             raccoglie le sue dipendenze invece di lasciarle sparse.
#
# ---------- [2] COME LO FACEVI (cap.02/06) --------------------------------
#   W1 = he_init(d, h); b1 = np.zeros(h)
#   W2 = he_init(h, 1); b2 = np.zeros(1)
#   H = np.maximum(0, X @ W1 + b1)
#   P = sigmoid(H @ W2 + b2).ravel()
#   → 4 variabili sciolte da passare a mano a ogni funzione
#
# ---------- [3] COME SI FA ORA --------------------------------------------
#   model = Rete2Layer(d, h)
#   P = model(X)
#   → i 4 parametri vivono DENTRO il modello, e li vedi con .parameters()

print("\n=== SEZIONE 3 — nn.Module ===")


class Rete2Layer(nn.Module):
    """Stessa architettura del cap.06: input → hidden ReLU → output sigmoid."""

    def __init__(self, d: int, h: int) -> None:
        super().__init__()                  # obbligatorio: registra i layer
        self.fc1 = nn.Linear(d, h)          # = X @ W1 + b1
        self.fc2 = nn.Linear(h, 1)          # = H @ W2 + b2

    def forward(self, x: "torch.Tensor") -> "torch.Tensor":
        h = torch.relu(self.fc1(x))         # hidden con ReLU
        z = self.fc2(h)                     # logit, shape (N, 1)
        return torch.sigmoid(z).squeeze(-1)  # probabilita', shape (N,)


modello_demo = Rete2Layer(d=7, h=8)

# 3.1 — dove sono finiti W e b?
print("3.1 parametri del modello:")
for nome, parametro in modello_demo.named_parameters():
    print(f"    {nome:<12} shape={tuple(parametro.shape)} "
          f"requires_grad={parametro.requires_grad}")
#
# Cosa vedi (e perche' e' importante):
#   fc1.weight  (8, 7)   ← ATTENZIONE: (out, in), NON (in, out) come il tuo W1!
#   fc1.bias    (8,)     ← come il tuo b1
#   fc2.weight  (1, 8)
#   fc2.bias    (1,)

# 3.2 — la convenzione (out, in): il tranello di shape del capitolo
#
# Nel cap.06 scrivevi:      H = X @ W1        con W1 di shape (d, h)
# PyTorch memorizza invece: weight di shape (h, d)  e calcola  x @ weight.T + bias
#
# Cioe': stessa matematica, matrice memorizzata trasposta.
# Non e' un capriccio: rende piu' efficienti alcune operazioni interne.
lin = nn.Linear(4, 3)                       # in=4, out=3
print("3.2 weight.shape =", tuple(lin.weight.shape), "(out, in)")
xb_demo = torch.randn(5, 4)                 # 5 campioni, 4 feature
out_pytorch = lin(xb_demo)
out_manuale = xb_demo @ lin.weight.T + lin.bias
print("3.2 uguali?", torch.allclose(out_pytorch, out_manuale))
# ↑ questo assert e' il "sanity check" versione PyTorch: dimostri a te stesso
#   che nn.Linear NON fa niente di magico.

# 3.3 — inizializzazione: la He del cap.02 esiste anche qui
#
# Di default nn.Linear usa una Kaiming-uniform (parente della He), quindi
# NON parti da zeri e non hai il "collasso" che avevi visto nel cap.02.
# Se vuoi esattamente He normale come nel corso:
nn.init.kaiming_normal_(lin.weight, nonlinearity="relu")
nn.init.zeros_(lin.bias)
print("3.3 He applicata a mano: std ≈", round(lin.weight.std().item(), 3))

# 3.4 — sigmoid dentro il modello o dentro la loss? (collegamento a #42)
#
# Due strade equivalenti in matematica, diverse in stabilita' numerica:
#
#   (A) modello restituisce PROBABILITA' p  → loss = nn.BCELoss()(p, y)
#       ↳ e' la traduzione letterale del cap.06 (tua bce_loss su p)
#       ↳ ma serve il clip di p, altrimenti log(0) → inf/nan
#
#   (B) modello restituisce LOGIT z         → loss = nn.BCEWithLogitsLoss()(z, y)
#       ↳ sigmoid + log calcolati insieme in modo stabile (clip incorporato)
#       ↳ e' quello che si usa in produzione
#
# In questo capitolo useremo (A) perche' e' il ponte diretto col cap.06,
# ma sappi che (B) e' la scelta professionale: e' letteralmente la lacuna
# #42 risolta a livello di libreria.

# Mini 3.1 — Istanzia Rete2Layer(d=7, h=8) e stampa i parametri
#            (nome + shape) con model.named_parameters().
# TUO CODICE:

class My_Rete_2_layer(nn.Module):
    
    def __init__(self, d: int, h: int) -> None:
        super().__init__()
        self.fc1 = nn.Linear(d, h)
        self.fc2 = nn.Linear(h, 1)
        
    def forward(self, x: "torch.Tensor") -> "torch.Tensor":
        h = torch.relu(self.fc1(x))
        z = self.fc2(h)
        return torch.sigmoid(z).squeeze(-1)
    
d = 7
h = 8
    
modello_prova = My_Rete_2_layer(d=d, h=h)

for name, parameter in modello_prova.named_parameters():
    print(name, parameter.shape)        

# Mini 3.2 — (nuovo) Conta i parametri totali del modello con
#            sum(p.numel() for p in model.parameters()).
#            Verifica a mano: d*h + h + h*1 + 1. Torna?
# TUO CODICE:

total_parameters = sum(p.numel() for p in modello_prova.parameters())
total_manual = d * h + h + h * 1 + 1

assert np.isclose(total_manual, total_parameters),"Ops, qualcosa è andato storto!!"

# Mini 3.3 — (nuovo) Passa un batch torch.randn(10, 7) al modello e stampa
#            la shape dell'output. Perche' NON e' (10, 1)?
# TUO CODICE:

N = 10

rand_batch = torch.randn(N, d)

print(rand_batch.shape)

out_modello_prova = modello_prova(rand_batch)

print(out_modello_prova.shape)

# la shape è (10, ) e non (10, 1) perchè abbiamo usato il metodo sqeeze(-1) che funzione come .ravel() per numpy.

# 📚 LETTURA PARALLELA — [PYTORCH] 1ª ed. cap. 6 "Using a neural network to fit the data"
# Confronta nn.Linear / nn.Module con il tuo layer Dense del Ponte.
# Domanda guida: perche' `named_parameters()` stampa chiavi tipo `fc1.weight`?
# TUA RISPOSTA (opzionale):
#

# ==========================================================================
# SEZIONE 4 — Dataset e DataLoader
# ==========================================================================
#
# ---------- [1] ANALOGIA --------------------------------------------------
# Dataset    = lo SCAFFALE con tutte le pratiche, numerate. Sai dire
#              "dammi la pratica numero 37" e quante pratiche ci sono.
# DataLoader = il CARRELLO che gira per lo scaffale, prende 32 pratiche alla
#              volta (batch), le mescola a ogni giro (shuffle) e te le porta.
#
# Nel web: Dataset = la tabella + il metodo find($id);
#          DataLoader = la paginazione con ordinamento casuale.
#
# ---------- [2] COME LO FACEVI (cap.06) -----------------------------------
#   for epoca in range(n_epoche):
#       P, cache = forward(X, ...)      # TUTTO il dataset in un colpo
#       ...
#   (era "full batch": va bene con 200 righe, non con 200.000 immagini)
#
# ---------- [3] COME SI FA ORA --------------------------------------------
#   for epoca in range(n_epoche):
#       for xb, yb in loader:           # ← un pezzo alla volta
#           ...
#
# ---------- [4] PERCHE' A PEZZI (3 motivi concreti) -----------------------
#   1) MEMORIA: le immagini del cap.08-10 non entrano tutte in GPU;
#   2) VELOCITA': aggiorni i pesi molte volte per epoca invece di una sola;
#   3) RUMORE UTILE: il gradiente stimato su un batch e' "sporco", e questo
#      rumore aiuta a non incastrarsi (SGD = Stochastic Gradient Descent).
#
# ---------- VOCABOLARIO da fissare bene ----------------------------------
#   campione (sample) = 1 riga / 1 immagine
#   batch             = un gruppo di campioni (es. 32)
#   step (iterazione) = un update dei pesi = un batch processato
#   epoca (epoch)     = un giro completo su TUTTO il dataset
#   → con N=200 e batch_size=32 → 7 step per epoca (6 pieni + 1 da 8)

print("\n=== SEZIONE 4 — Dataset e DataLoader ===")

# 4.1 — la via rapida: TensorDataset (quando i dati sono gia' tensori)
N_demo, d_demo = 200, 7
rng_demo = np.random.default_rng(42)
X_np_demo = rng_demo.standard_normal((N_demo, d_demo)).astype(np.float32)
y_np_demo = (X_np_demo[:, 0] + X_np_demo[:, 1] > 0).astype(np.float32)

X_t = torch.from_numpy(X_np_demo)
y_t = torch.from_numpy(y_np_demo)

dataset_demo = TensorDataset(X_t, y_t)
loader_demo = DataLoader(dataset_demo, batch_size=32, shuffle=True)
print(f"4.1 campioni={len(dataset_demo)} | batch per epoca={len(loader_demo)}")

primo_xb, primo_yb = next(iter(loader_demo))
print("4.1 shape primo batch:", tuple(primo_xb.shape), tuple(primo_yb.shape))

# 4.2 — la via manuale: Dataset custom (ti servira' per le immagini nel cap.08)
#
# Devi implementare solo 3 metodi. E' un'interfaccia, come un Repository:


class PraticheDataset(Dataset):
    """Dataset custom: legge da array NumPy e restituisce tensori float32."""

    def __init__(self, X: np.ndarray, y: np.ndarray) -> None:
        self.X = X.astype(np.float32)
        self.y = y.astype(np.float32)

    def __len__(self) -> int:
        """Quante pratiche ci sono sullo scaffale."""
        return len(self.X)

    def __getitem__(self, idx: int):
        """Dammi la pratica numero idx (come find($id))."""
        return torch.from_numpy(self.X[idx]), torch.tensor(self.y[idx])


ds_custom = PraticheDataset(X_np_demo, y_np_demo)
print("4.2 dataset custom: len =", len(ds_custom),
      "| item 0 shape =", tuple(ds_custom[0][0].shape))

# 4.3 — parametri del DataLoader che userai davvero
#   batch_size   quante righe per volta (32 / 64 tipici)
#   shuffle=True SOLO sul train (sul test non serve e confonde i confronti)
#   drop_last    scarta l'ultimo batch se incompleto (utile con BatchNorm)
#   num_workers  processi paralleli per caricare i dati (0 = tutto nel main)

# Mini 4.1 — Da X_np (N,d) e y_np (N,) crea TensorDataset + DataLoader
#            batch_size=32, shuffle=True. Stampa la shape del primo batch.
# TUO CODICE:

N = 200
d = 7
h = 8

rng = np.random.default_rng(0)
X_np = rng.standard_normal(size=(N, d), dtype=np.float32)
y_np = (X_np[:, 0] - X_np[:, 1] > 0).astype(np.float32)

X_trc = torch.tensor(X_np)
y_trc = torch.tensor(y_np)

trc_dataset = TensorDataset(X_trc, y_trc)
trc_loader = DataLoader(trc_dataset, batch_size=32, shuffle=True)

primo_x_trc, primo_y_trc = next(iter(trc_loader))

print(f"Primo Batch X.shape: {primo_x_trc.shape}")
print(f"Primo Batch y.shape: {primo_y_trc.shape}")

# Mini 4.2 — (nuovo) Con N=200 e batch_size=64, quanti step per epoca?
#            Rispondi PRIMA a mente, poi verifica con len(loader).
# TUA RISPOSTA:
# 200 / 64 = 3.125 -> 4

trc_loader = DataLoader(trc_dataset, batch_size=64, shuffle=True)

print(len(trc_loader))

# 📚 LETTURA PARALLELA — [PYTORCH] 1ª ed. overview cap. 1 + uso DataLoader nei cap. 7–8
# Idea chiave: batch + shuffle = carrello di pratiche (la nostra analogia).
# Domanda guida: se shuffle=False, cosa rischi nel training? (1 frase)
# TUA RISPOSTA (opzionale):
#

# ==========================================================================
# SEZIONE 5 — Training loop standard PyTorch
# ==========================================================================
#
# ---------- LA TABELLA CHE VALE TUTTA LA SEZIONE -------------------------
#
#   COSA FA                cap.06 (NumPy, a mano)      cap.07 (PyTorch)
#   ---------------------  --------------------------  ----------------------
#   azzera i gradienti     (implicito: li ricreavi)    optimizer.zero_grad()
#   forward                P, cache = forward(X, ...)  p = model(xb)
#   loss                   loss = bce_loss(P, y)       loss = criterion(p, yb)
#   backward               dZ2, dH, dZ1, grad_W...     loss.backward()
#   update                 W1 -= lr * grad_W1 (x4)     optimizer.step()
#
# Cinque righe di PyTorch = tutto il lavoro del cap.06.
# Se sai spiegare questa tabella, sai spiegare il capitolo.
#
# ---------- PERCHE' zero_grad() E' LA PRIMA RIGA -------------------------
# L'hai visto in 2.3: `.grad` si ACCUMULA. Se non lo svuoti, al secondo step
# useresti la somma dei gradienti di due batch → passi troppo grandi, loss
# che impazzisce. Non e' un dettaglio stilistico: e' il bug numero 1 dei
# principianti in PyTorch.
#
# ---------- CHI E' L'OPTIMIZER -------------------------------------------
# `torch.optim.SGD(model.parameters(), lr=0.1)` e' letteralmente il tuo
# `W -= lr * grad` del cap.05/06, scritto una volta per tutti i parametri.
# `Adam` e' un parente piu' furbo (passo adattivo per parametro): lo userai
# dal cap.08, ma il concetto e' lo stesso — backprop calcola, l'optimizer
# cammina.

print("\n=== SEZIONE 5 — training loop ===")

# 5.1 — training loop completo e commentato (il modello che riuserai)
modello_train = Rete2Layer(d=d_demo, h=8)
criterio = nn.BCELoss()                                   # loss su PROBABILITA'
ottimizzatore = torch.optim.SGD(modello_train.parameters(), lr=0.1)

storia_loss: list[float] = []
for epoca in range(5):
    modello_train.train()                                 # modalita' training
    somma_loss, n_batch = 0.0, 0

    for xb, yb in loader_demo:
        ottimizzatore.zero_grad()                         # 1. svuota i .grad
        p_pred = modello_train(xb)                        # 2. forward
        perdita_batch = criterio(p_pred, yb)              # 3. loss
        perdita_batch.backward()                          # 4. backward (autograd)
        ottimizzatore.step()                              # 5. update dei pesi

        somma_loss += perdita_batch.item()                # .item() → float Python
        n_batch += 1

    media = somma_loss / n_batch
    storia_loss.append(media)
    print(f"5.1 epoca {epoca + 1}: loss media = {media:.4f}")

# 5.2 — la valutazione va SEMPRE dentro no_grad + eval
modello_train.eval()                                      # spegne dropout/BN
with torch.no_grad():                                     # niente grafo: piu' veloce
    p_finale = modello_train(X_t)
    acc = ((p_finale >= 0.5).float() == y_t).float().mean().item()
print(f"5.2 accuracy sul train: {acc:.3f}")
#
# NOTA: la soglia 0.5 e' esattamente quella del cap.03 (lacuna storica sulla
# soglia). Non cambia niente: cambia solo la sintassi.

# 5.3 — cosa NON devi fare (raccolta dei classici)
#   ✗ dimenticare zero_grad()          → gradienti sommati
#   ✗ chiamare backward() su un vettore → serve uno SCALARE (la loss media)
#   ✗ tenere `loss` invece di `loss.item()` in una lista → memory leak del grafo
#   ✗ valutare senza no_grad()         → lento e memoria sprecata
#   ✗ dati e modello su device diversi → RuntimeError

# 5.4 — 🔁 RINFORZO training loop (da V1 cap.06): completa a parole
#   zero_grad → forward → ? → backward → ?
# TUA RISPOSTA:
# loss

# Mini 5.1 — Scrivi un loop di 5 epoche su TensorDataset finto (N=64, d=4)
#            con BCELoss + SGD. Stampa loss ogni epoca.
# TUO CODICE:

def aaa():
    return

N, d, h = 64, 4, 8

X_trc = torch.randn(N, d, dtype=torch.float32)
y_trc = torch.tensor(X_trc[:, 0] - X_trc[:, 1] > 0, dtype=torch.float32)

data = TensorDataset(X_trc, y_trc)
loader = DataLoader(data, batch_size=32, shuffle=True)

modello = Rete2Layer(d=d, h=h)
criterio = nn.BCELoss()
ottimizzatore = torch.optim.SGD(modello.parameters(), lr=0.1)

media_epoche = []

for epoca in range(5):
    modello.train()
    somma_loss, n_batch = 0.0, 0
    
    for xb, yb in loader:
        ottimizzatore.zero_grad()
        p_pred = modello(xb)
        loss_batch = criterio(p_pred, yb)
        loss_batch.backward()
        ottimizzatore.step()
        somma_loss += loss_batch.item()
        n_batch += 1
    media_batch = somma_loss / n_batch
    media_epoche.append((epoca, float(media_batch)))
    
for a in media_epoche:
    print(f"Epoca n°{a[0]} -> Loss: {a[1]:4f}")
    

# Mini 5.2 — (nuovo) Commenta la riga `ottimizzatore.step()` (mettila come
#            commento) e rilancia: cosa fa la loss? Perche'?
# TUA RISPOSTA:
# La loss non scende perche l'ottimizzatore non effettua il gradient descent sulla base del backward.

# 📚 LETTURA PARALLELA — [PYTORCH] 1ª ed. cap. 5–6 + inizio §8.4 (training loop)
# Confronta la tabella NumPy↔PyTorch di questa sezione con il loop del libro.
# Domanda guida: perche' il libro (e noi) usiamo loss.item() e non loss grezzo
# nella somma delle epoche?
# TUA RISPOSTA (opzionale):
#

# ==========================================================================
# SEZIONE 6 — Salvare e caricare i pesi (state_dict)
# ==========================================================================
#
# ---------- [1] ANALOGIA --------------------------------------------------
# state_dict = l'export delle MANOPOLE (i valori di W e b), non della macchina.
# Come esportare solo il .env / la configurazione: per ricostruire il sistema
# ti serve comunque il codice della classe.
#
# Concretamente: e' un dizionario {nome_parametro: tensore}.
#
# Contrasti utili dai libri (scheda M03_C07_sez6_state_dict.md):
#   [PYTORCH] §8.4.2 — salvi SOLO i pesi; la classe Net/Rete2Layer la tieni tu.
#   [GERON] cap. 10  — Keras model.save() salva anche architettura+optimizer;
#                      in PyTorch di solito NO → ricostruisci tu le "mura".
#
# ---------- [2] PERCHE' TI SERVE ORA -------------------------------------
# Perche' addestri su Colab (che si spegne) e usi il modello in locale.
# Senza salvataggio, chiudere la scheda = buttare il training.
# [PYTORCH] §8.4.3: se i pesi nascono su GPU, in locale usa map_location="cpu"
# (il tuo caso: AMD senza CUDA).

print("\n=== SEZIONE 6 — state_dict ===")

# 6.1 — cosa c'e' dentro
print("6.1 chiavi dello state_dict:", list(modello_train.state_dict().keys()))

# 6.2 — salva e ricarica (il ciclo completo Colab → locale)
percorso_pesi = "rete_demo_cap07.pt"
torch.save(modello_train.state_dict(), percorso_pesi)

modello_ricaricato = Rete2Layer(d=d_demo, h=8)             # stessa ARCHITETTURA
modello_ricaricato.load_state_dict(
    torch.load(percorso_pesi, map_location="cpu")          # GPU → CPU
)
modello_ricaricato.eval()

with torch.no_grad():
    uguali = torch.allclose(modello_train(X_t), modello_ricaricato(X_t))
print("6.2 il modello ricaricato dà le stesse predizioni?", uguali)
#
# ⚠️ La classe Rete2Layer deve essere definita PRIMA di load_state_dict:
#    i pesi senza l'architettura sono numeri senza contesto.
#    (`map_location="cpu"` serve quando i pesi sono stati salvati da GPU.)
# ⚠️ Preferisci state_dict (non pickle del modello intero): piu' flessibile
#    ([PYTORCH] §13.6.6).

# 📚 LETTURA PARALLELA — [PYTORCH] 1ª ed. §8.4.2 + fine §8.4.3 (map_location)
# Scheda: docs/libri_corso/schede/M03_C07_sez6_state_dict.md
# Opzionale contrasto: [GERON] cap. 10 "Saving and Restoring a Model" (Keras).
# Domanda guida: in 2 frasi — (a) cosa c'e' nel file .pt? (b) perche' map_location
# e' critico sul TUO PC dopo un training su Colab?
# TUA RISPOSTA (opzionale):
#

# Mini 6.1 — Salva e ricarica i pesi di un nn.Linear(3,1) su file temporaneo.
#            Verifica allclose sui weight.
# TUO CODICE:

print("\nMini-esercizio 6.1\n")

torch.manual_seed(0)
modello = nn.Linear(3, 1)
g = torch.Generator().manual_seed(0)
x_demo = torch.randn(5, 3, generator=g)
out = modello(x_demo)

print(out)

path_weigths = "pesi_mini_esercizio_1.pt"

torch.save(modello.state_dict(), path_weigths)

modello_reloaded = nn.Linear(3, 1)

modello_reloaded.load_state_dict(
    torch.load(path_weigths, map_location = "cpu")
)

out_2 = modello_reloaded(x_demo)

print(out_2)
print(modello.state_dict)

assert torch.allclose(modello.weight.T, modello_reloaded.weight.T), "Ops, qualcosa non funziona, i pesi dei due modelli non coincidono!!"

# Mini 6.2 — (nuovo) Cosa succede se ricarichi lo state_dict in un modello
#            con h diverso (es. h=16)? Prova e leggi il messaggio d'errore.
# TUA RISPOSTA: 
# RuntimeError: Error(s) in loading state_dict for Linear:
# size mismatch for weight: copying a param with shape torch.Size([1, 3]) from checkpoint, the shape in current model is torch.Size([1, 4]).

print("\nMini-esercizio 6.2\n")

modello_errato = nn.Linear(4, 1)
modello_errato.load_state_dict(
    torch.load(path_weigths, map_location="cpu")
)

# 📚 [LIBRO] — Ispirato a [PYTORCH] §13.6.6 (checkpoint dict), adattato al cap.07
# Obiettivo: invece di salvare solo lo state_dict "nudo", salva un DIZIONARIO:
#   {
#     "model_state": modello_train.state_dict(),
#     "nota": "demo cap.07 — rete 2-layer",
#     "d": d_demo,
#     "h": 8,
#   }
# poi ricarica con torch.load(..., map_location="cpu")["model_state"] in un
# nuovo Rete2Layer(d=..., h=...) e verifica allclose sulle predizioni.
# (NON serve ancora optimizer_state: quello e' per riprendere il training.)
# TUO CODICE:

print("\nMini-esercizio 13.6.6\n")

N, d, h = 10, 5, 8

torch.manual_seed(0)

modello = Rete2Layer(d, h)
x_prova = torch.randn(N, d)
out = modello(x_prova)
out_dict = {
    "model_state": modello.state_dict(),
    "nota": "demo cap.07 — rete 2-layer",
    "d": d,
    "h": h,
}

import pprint as p
p.pprint(out_dict)

percorso = "pesi_es_13.6.6.pt"
torch.save(out_dict, percorso)

modello_reloaded = Rete2Layer(d, h)
modello_reloaded.load_state_dict(
    torch.load(percorso, map_location="cpu")['model_state']
)

out_reload = modello_reloaded(x_prova)

assert torch.allclose(out, out_reload), "Ops, qualcosa è andato storto, gli out dei due modelli non coincidono!"

print(out[:5])
print(out_reload[:5])

# ==========================================================================
# 🔁 CONFRONTO PRIMA/DOPO (migrato da cap.06 — NON svolto li')
# ==========================================================================
#
# Scrivi in commento 8-10 righe:
#   - cosa NON capivi al cap.01 M3 (neurone)
# Non capivo bene il discorso delle shape.
#   - cosa sembrava magia al cap.02-03
# arrivare a una metrica di errore come la BCE solo attraverso dei passaggi numerici
#   - cosa spaventava a derivate / chain / backprop
# il concetto stesso di derivata per definire la responsabilità dell'errore per ogni paramentro.
#   - cosa hai "afferrato" ORA
# il ciclo completo di addestamento di una rete tramite backprop, chain rule e gradient descent.
#   - cosa ti aspetti da PyTorch: API pulita, sotto il cofano = cap.06
# da pytorch mi attendo lo stesso funzionamento, ma una sintassi pulita e tutto realizzato senza scrivere i pezzetti che girano sotto il cofano.

#
# BONUS: accuracy di un neurone manuale a pesi inventati vs rete addestrata
#         (anche solo a parole se non hai i pesi del cap.06 sotto mano).
# accuracy di circa 0.5 in una rete a pesi random, mentre circa 1 con una rete addestrata.
# TUO COMMENTO:
# ...


# ==========================================================================
# 🔁 SCALER + TRAIN (spirito TODO 18 cap.06)
# ==========================================================================
#
# Obiettivo: 5-8 righe di COMMENTO (non solo plot):
#   - raw vs scaled: cosa cambia su loss iniziale / convergenza?
#   - fit dello scaler SOLO sul train (mai sul test intero prima dello split)
#
# La loss iniziale è molto più alta e il modello converge meno rispetto ad uno scalato
# Ovviamente lo scaling va fatto usando solo i dati del training per evitare leakage.
#
# Promemoria dal cap.06 (e da M2): lo scaler si "impara" (mean, std) sul TRAIN
# e si APPLICA al test. Se calcoli mean/std su tutto, il test "sbircia" il
# train → data leakage, e la metrica ti mente.
#
# Poi, se TORCH_OK: train 2 modelli uguali (raw vs scaled) 20 epoche e
# confronta loss finale.
#
# TUO COMMENTO + CODICE:
# ...

import os
import pandas as pd

path_file = os.path.join(os.path.dirname(__file__), "dati", "pratiche.csv")
df = pd.read_csv(path_file)
X = torch.tensor(df.drop(columns=['pratica_id', 'y_alterato']).to_numpy(dtype="float32"))
y = torch.tensor(df['y_alterato'].to_numpy(dtype="float32"))

cut = int((len(X) * 80) / 100)

X_train = X[:cut]
X_test = X[cut:]
y_train = y[:cut]
y_test = y[cut:]

mean = X_train.mean(axis=0)
std = X_train.std(axis=0)

X_train_scaled = (X_train - mean) / std
X_test_scaled = (X_test - mean) / std

data = TensorDataset(X_train, y_train)
load = DataLoader(data, shuffle=True, batch_size = int(len(X_train) / 6))

data_scaled = TensorDataset(X_train_scaled, y_train)
load_scaled = DataLoader(data_scaled, shuffle=True, batch_size = int(len(X_train) / 6))


class My_Rete_2Layer(nn.Module):

    def __init__(self, d: int, h: int) -> None:
        super().__init__()
        self.fc1 = nn.Linear(d, h)
        self.fc2 = nn.Linear(h, 1)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        h = torch.relu(self.fc1(x))
        z = self.fc2(h)
        return torch.sigmoid(z).squeeze(-1)

d = X_train.shape[1]
h = 8

torch.manual_seed(0)

modello = My_Rete_2Layer(d = d, h = h)
criterio = nn.BCELoss()
ottimizzatore = torch.optim.SGD(modello.parameters(), lr=0.1)

loss_media_per_epoca = []

for epoca in range(20):
    modello.train()
    somma_losses, n_in_batch = 0.0, 0
    for xb, yb in load:
        ottimizzatore.zero_grad()
        y_pred = modello(xb)
        loss = criterio(y_pred, yb)
        loss.backward()
        ottimizzatore.step()
        somma_losses += loss.item()
        n_in_batch += 1
    loss_media_per_epoca.append((epoca, float(somma_losses / n_in_batch)))

torch.manual_seed(0)

modello_scaled = My_Rete_2Layer(d = d, h = h)
criterio_scaled = nn.BCELoss()
ottimizzatore_scaled = torch.optim.SGD(modello_scaled.parameters(), lr=0.1)

loss_media_per_epoca_scaled = []

for epoca in range(20):
    modello_scaled.train()
    somma_losses, n_in_batch = 0.0, 0
    for xb, yb in load_scaled:
        ottimizzatore_scaled.zero_grad()
        y_pred = modello_scaled(xb)
        loss = criterio_scaled(y_pred, yb)
        loss.backward()
        ottimizzatore_scaled.step()
        somma_losses += loss.item()
        n_in_batch += 1
    loss_media_per_epoca_scaled.append((epoca, float(somma_losses / n_in_batch)))

percorso = "pesi_todo_18_modello_scaled.pt"
torch.save(modello_scaled.state_dict(), percorso)


print(f"Loss Iniziale Dataset Normale: {loss_media_per_epoca[0][1]:.5f}")    
print(f"Loss Iniziale Dataset Scalato: {loss_media_per_epoca_scaled[0][1]:.5f}")

print(f"Loss Finale DataSet Normale: {loss_media_per_epoca[-1][1]:.5f}")
print(f"Loss Finale DataSet Scalato: {loss_media_per_epoca_scaled[-1][1]:.5f}")

# ==========================================================================
# 🔁 DRIFT REAL-WORLD (spirito TODO 19 cap.06)
# ==========================================================================
#
# Scrivi 3 ipotesi in italiano su perche' un modello buono in lab puo'
# crollare in produzione (es. cambio scanner, nuova popolazione clienti,
# feature shift). Poi: simula X_test * 1.5 e confronta accuracy; se resta
# alta, spiega PERCHE' su quel toy set puo' non bastare (*1.5 non e'
# sempre un drift "duro").
#
# TUE IPOTESI + CODICE:
# Ipotesi 1: Cambiando il modello dello scanner, la qualità delle scansioni puà cambiare e di conseguenza influenzare l'estrazione dei dati.
# Ipotesi 2: Nel tempo, la popolazione dei clienti può variare, andando a influenzare i dati prodotti e di consueguenza il modello può non essere attrezzato a predire i loro nuovi comportamenti.
# Ipotesi 3: Nel tempo, anche se  i clieni possono rimanere gli stessi, le loro abitudini possono cambiare, provocando un drift di abitudini rispetto ai soliti dati, andando così a rendere il modello meno efficace.

X_test = X_test_scaled * 1.5

modello_reloaded = My_Rete_2Layer(d, h)
modello_reloaded.load_state_dict(
    torch.load(percorso, map_location="cpu")
)

criterio = nn.BCELoss()
y_pred_scaled = modello_scaled(X_test_scaled)
y_pred_reload = modello_reloaded(X_test)

loss = criterio(y_pred_scaled, y_test).item()
y_hat = (y_pred_scaled >= .5).float()
acc = (y_hat == y_test).float().mean()

loss_dopo_drift = criterio(y_pred_reload, y_test).item()
y_hat_reload = (y_pred_reload >= .5).float()
acc_dopo_drift = (y_hat_reload == y_test).float().mean().item()

assert loss_dopo_drift > loss, "La Loss deve essere più alta dopo il Drift!"
assert acc_dopo_drift < acc, "L'accuracy deve essere più alta dopo il Drift!!"

print(f"Loss Modello Scalato: {loss:.5f}")
print(f"Accuracy Modello Scalato: {acc}")
print(f"Loss dopo Drift: {loss_dopo_drift:.5f}")
print(f"Accuracy dopo Drift: {acc_dopo_drift}")

# ==========================================================================
# ESERCIZI
# ==========================================================================

# --------------------------------------------------------------------------
# TODO 1 — 🎯 [COLLOQUIO] (10 min)
# --------------------------------------------------------------------------
# (1) Cos'e' autograd in 2 frasi da colloquio.
# (2) Differenza Dataset vs DataLoader.
# (3) Perche' zero_grad() a ogni step?
# TUA RISPOSTA:

# 1) Il gradiente trovato automaticamente da torch. 
# 2) DataSet sarebbe l'insieme di tutti i dati, mentre il loader è l'organizzazione interna di quei dati.
# 3) Perchè altrimenti i gradienti si sommerebbero ad ogni epoca e dopo poche epoche avremmo divergenza invece che convergenza dell metriche.

# --------------------------------------------------------------------------
# TODO 2 — 🔧 [REFACTORING] (20 min)
# --------------------------------------------------------------------------
# Riscrivi in PyTorch (nn.Module) la rete 2-layer del cap.06:
#   hidden ReLU, output sigmoid, BCE, SGD.
# Confronta mentalmente con train_rete_2_layer NumPy.
# Bonus: fallo con BCEWithLogitsLoss (modello che restituisce logit) e
#        spiega in 1 riga perche' e' piu' stabile (collegamento #42).
# TUO CODICE:

class Rete_todo_2(nn.Module):

    def __init__(self, d: int, h:int) -> None:
        super().__init__()
        self.fc1 = nn.Linear(d, h)
        self.fc2 = nn.Linear(h, 1)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        h = torch.relu(self.fc1(x))
        z = self.fc2(h)
        return z.squeeze(-1)

X = torch.randn(20, 5)
y = (X[:, 0] - X[:, 1] > 0).float()

modello = Rete_todo_2(5, 8)
criterio = nn.BCEWithLogitsLoss()
ottimizzatore = torch.optim.SGD(modello.parameters(), lr=0.1)

loss_per_epoca = []

for e in range(10):
    ottimizzatore.zero_grad()
    z_pred = modello(X)
    loss = criterio(z_pred, y)
    loss.backward()
    loss_per_epoca.append((e, loss.item()))
    ottimizzatore.step()

# Con BCELoss + sigmoid a mano, se p va a 0 o 1 rischi log(0) → serviva il clip.
# BCEWithLogitsLoss calcola tutto in forma numericamente più sicura sui logit, senza passare da probabilità estreme esplicite.




# --------------------------------------------------------------------------
# TODO 3 — 🔍 [DEBUG] (15 min)
# --------------------------------------------------------------------------
# Bug tipici (scegline 2 e spiega la fix):
#   A) loss.backward() senza zero_grad → gradienti sommati
#   B) tensor su CUDA e modello su CPU (device mismatch)
#   C) BCELoss con target float vs Long per CrossEntropy (famiglie diverse)
#   D) X in float64 da NumPy dentro nn.Linear float32
# TUA RISPOSTA:
# ...

# --------------------------------------------------------------------------
# TODO 4 — 🧠 [RETRIEVAL] (10 min)
# --------------------------------------------------------------------------
# Senza guardare il cap.06: riscrivi a parole i 5 step del backward 2-layer
# (dZ2 → … → grad_W1). Poi: "in PyTorch questi step li fa ______".
# TUA RISPOSTA:
# ...

# --------------------------------------------------------------------------
# TODO 5 — 🔀 [INTERLEAVING] (20 min)
# --------------------------------------------------------------------------
# Carica (o simula) un CSV stile M2: X (N,d), y (N,).
# Custom Dataset __getitem__ → DataLoader → 1 epoca di training.
# Riusa PraticheDataset della sez. 4.2 come modello di partenza.
# TUO CODICE:
# ...

# --------------------------------------------------------------------------
# TODO 6 — 🌊 [REAL-WORLD] (15 min)
# --------------------------------------------------------------------------
# Scenario Validator: feature tabellari + futura feature visiva CNN.
# In 8-10 righe: dove metteresti StandardScaler? Dove andrebbe il
# ramo PyTorch/CNN? Cosa non mischieresti nel medesimo tensore grezzo?
# TUA RISPOSTA:
# ...


# ==========================================================================
# 🏗️ PROGETTO INCREMENTALE — M3-07
# ==========================================================================
#
# Task (15-25 min):
#   Addestra su Colab (o CPU) la STESSA architettura 2-layer del cap.06
#   con PyTorch sul dataset pratiche M2 (o mock equivalente).
#   Confronta:
#     - accuracy / BCE di test vs ricordo del mini-progetto NumPy
#     - tempo wall-clock (anche solo ordine di grandezza)
#   Salva state_dict.
#
# Output atteso: dict con chiavi
#   acc_test, bce_test, n_epochs, device, path_pesi
#
# Suggerimento di metodo (non la soluzione):
#   1) carica il CSV con Pandas, X/y come nel M2;
#   2) split train/test PRIMA di tutto;
#   3) scaler fit sul train (rinforzo #43), astype(np.float32) (tranello 1.2);
#   4) TensorDataset + DataLoader;
#   5) loop delle 5 righe della Sezione 5;
#   6) valutazione in no_grad + torch.save.
#
# TUO CODICE:
# ...


# ==========================================================================
# QUIZ DI VERIFICA (V1 - V6)
# ==========================================================================
#
# V1) requires_grad=True serve a …?
# TUA RISPOSTA:
# ...

# V2) V/F: "nn.Linear fa X @ W.T + b (convenzione PyTorch sui weight)."
#     (Se non sei sicuro, verifica con .weight.shape)
# TUA RISPOSTA:
# ...

# V3) Ordine corretto: (a) backward (b) zero_grad (c) step (d) forward+loss
# TUA RISPOSTA:
# ...

# V4) Trova l'errore concettuale: "Autograd sostituisce il gradient descent".
# TUA RISPOSTA:
# ...

# V5) A cosa serve map_location="cpu" in torch.load?
# TUA RISPOSTA:
# ...

# V6) 💬 Feynman: spiega DataLoader a un collega web (senza jargon inutile).
# TUA RISPOSTA:
# ...


# ==========================================================================
# SOLUZIONI QUIZ (solo dopo il tentativo)
# ==========================================================================
#
# --- Ingresso ---
# Q1) forward + loss + backward (+ update / GD)
# Q2) Riutilizzare attivazioni/Z del forward nelle derivate (H, Z1, …)
# Q3) grad_W1 (4,8), grad_b1 (8,), grad_W2 (8,1), grad_b2 (1,)
#     [o W2 (8,) se flatten — coerente col tuo codice cap.06]
# Q4) Confronta grad analitico vs numerico (h~1e-6) prima di fidarti del train
# Q5) Manca spesso /N (media batch) → dZ2 = (P-y).reshape(-1,1) / N
# Q6) ≈ 0.693 (= -log(0.5))
# Q7) (b) qualcosa non funziona (sei ancora al livello random)
# Q8) Backprop = calcolare i gradienti lungo la catena;
#     GD = usare quei gradienti per aggiornare w -= lr * grad
#
# --- Rinforzi ---
# 44.A) Confronto tra gradiente analitico (formula a mano) e numerico
#       (differenza centrata, h≈1e-6): se coincidono, il backward è corretto.
# 44.B) Perché i gradienti li calcola autograd: non c'è una tua formula da
#       verificare (resta utile per layer custom → torch.autograd.gradcheck).
#
# --- Verifica ---
# V1) Dire a PyTorch di tracciare operazioni su quel tensore per .backward()
# V2) Vero nella pratica PyTorch: weight shape (out, in); y = x @ W.T + b
# V3) b → d → a → c  (zero_grad, forward+loss, backward, step)
# V4) Autograd calcola i GRADIENTI; GD/Adam fanno l'UPDATE. Non sono la stessa cosa
# V5) Caricare pesi salvati da GPU su macchina solo-CPU (il tuo PC)
# V6) Tipo un paginatore/carrello: prende pacchetti di esempi dallo scaffale,
#     li mescola, te li porta batch per batch
