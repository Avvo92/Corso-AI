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
   *  SEZIONE 1  Tensori vs NumPy                          mini inline
   *  SEZIONE 2  Autograd = backward automatico            mini + 🔁 cache
   *  SEZIONE 3  nn.Module / Linear / ReLU / Sigmoid       mini
   *  SEZIONE 4  Dataset + DataLoader                      mini
   *  SEZIONE 5  Training loop standard                    mini + 🔁 loop
   *  SEZIONE 6  state_dict save/load                      mini
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
# ---------------------------------------------------------------------------
import numpy as np

try:
    import torch
    import torch.nn as nn
    from torch.utils.data import Dataset, DataLoader, TensorDataset
    TORCH_OK = True
except ImportError:
    TORCH_OK = False
    print(
        "[AVVISO] torch non installato in questo ambiente. "
        "Su Colab: gia' presente. In locale CPU-only: "
        "pip install torch --index-url https://download.pytorch.org/whl/cpu"
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
# ...

# Q5) [Trova errore] dZ2 = (P - y).reshape(-1, 1)  # manca qualcosa per la
#     media di batch della BCE. Cosa?
# TUA RISPOSTA:
# ...

# Q6) Dataset bilanciato, rete random: loss iniziale BCE circa quanto?
#     (pista: -log(0.5))
# TUA RISPOSTA:
# ...

# Q7) Dopo 500 epoche loss = 0.692. Cosa pensi? (a/b/c/d come V7 cap.06)
# TUA RISPOSTA:
# ...

# Q8) 💬 Feynman: in 4-6 frasi, differenza tra backpropagation e
#     gradient descent. (Punto debole TODO 14 cap.06 — non mischiarli.)
# TUA RISPOSTA:
# ...


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
#   p_safe = np.clip(___, eps, 1 - eps)
#   loss = -np.mean(y * np.log(p_safe) + (1 - y) * np.log(1 - p_safe))
#
# Micro 42.B — V/F: "clippare z in [eps, 1-eps] e' equivalente a clippare p".
# TUA RISPOSTA:
# ...


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
# ...

# Micro 43.B — std==0: cosa metti al posto dello 0 per non dividere per zero?
# TUA RISPOSTA:
# ...


# ==========================================================================
# 🔁 RINFORZO MIRATO Pattern #27 — formula → codice (simbolo per simbolo)
# ==========================================================================
#
# Errori tipici: * vs @, * vs /, parentesi al denominatore, == vs =.
#
# Micro 27.A — riscrivi in NumPy (senza moltiplicazione implicita tipo p(1-p)):
#   dL/dp = (p - y) / (p * (1 - p))
# TUA CODICE (1 riga, p e y array):
# ...

# Micro 27.B — quale e' corretto per hidden @ pesi output?
#   (a) H * W2   (b) H @ W2   (c) W2 @ H
# TUA RISPOSTA:
# ...


# ==========================================================================
# SEZIONE 1 — Tensori PyTorch vs ndarray NumPy
# ==========================================================================
#
# Analogia: ndarray = foglio Excel di numeri; Tensor = stesso foglio MA
# puo' stare su GPU e puo' "ricordare" le operazioni (se requires_grad=True).
#
# JS: un Array di numeri. PHP: un array numerico. Qui in piu': device + tape.
#
# if TORCH_OK:
#     a = torch.tensor([[1.0, 2.0], [3.0, 4.0]])
#     b = torch.from_numpy(np.array([1.0, 2.0], dtype=np.float32))
#     print(a.shape, a.dtype, a.device)
#     # .numpy() solo se tensor e' su CPU e non richiede grad (o .detach())
#
# Mini 1.1 — Crea un tensor float32 shape (4, 3) di zeri su CPU.
# TUO CODICE:
# ...

# Mini 1.2 — Converti un ndarray (5,) in tensor e stampa .shape.
# TUO CODICE:
# ...


# ==========================================================================
# SEZIONE 2 — Autograd: il "nastro" che sostituisce il backward manuale
# ==========================================================================
#
# Cap.06: scrivevi a mano dZ2, dH, dZ1, grad_W...
# Qui: PyTorch registra le operazioni (come uno scontrino / tape recorder)
# e .backward() calcola i gradienti.
#
# 🔁 Ponte con CACHE cap.06: la cache manuale = pezzi dello scontrino.
#    Autograd conserva lo scontrino intero per te.
#
# Esempio (se TORCH_OK):
#   w = torch.tensor(2.0, requires_grad=True)
#   x = torch.tensor(3.0)
#   y = (w * x) ** 2          # y = 36
#   y.backward()
#   print(w.grad)             # dy/dw = 2*(w*x)*x = 36
#
# Mini 2.1 — Calcola a mano dy/dw per y = (w+1)^2 in w=1, poi verifica
#            con autograd (requires_grad=True).
# TUO CODICE:
# ...

# Mini 2.2 — 💬 In 2 frasi: cosa sostituisce autograd rispetto al cap.06?
# TUA RISPOSTA:
# ...


# ==========================================================================
# SEZIONE 3 — nn.Module, nn.Linear, attivazioni
# ==========================================================================
#
# Ponte Matematico / cap.02: Dense = X @ W + b.
# PyTorch: nn.Linear(in_features, out_features) FA ESATTAMENTE quello.
#
# class Rete2Layer(nn.Module):
#     def __init__(self, d, h):
#         super().__init__()
#         self.fc1 = nn.Linear(d, h)
#         self.fc2 = nn.Linear(h, 1)
#     def forward(self, x):
#         h = torch.relu(self.fc1(x))
#         return torch.sigmoid(self.fc2(h)).squeeze(-1)
#
# Mini 3.1 — Istanzia Rete2Layer(d=7, h=8) e stampa i parametri
#            (nome + shape) con model.named_parameters().
# TUO CODICE:
# ...


# ==========================================================================
# SEZIONE 4 — Dataset e DataLoader
# ==========================================================================
#
# Analogia: Dataset = scaffale di pratiche; DataLoader = carrello che prende
# N pratiche a caso (batch) e le mescola (shuffle) ogni epoca.
#
# Perche' non passare tutto X ogni volta?
#   - memoria GPU limitata
#   - SGD stocastico: rumore del batch aiuta a non bloccarsi
#
# Mini 4.1 — Da X_np (N,d) e y_np (N,) crea TensorDataset + DataLoader
#            batch_size=32, shuffle=True. Stampa la shape del primo batch.
# TUO CODICE:
# ...


# ==========================================================================
# SEZIONE 5 — Training loop standard PyTorch
# ==========================================================================
#
# Cap.06 (NumPy):
#   P, cache = forward(...)
#   loss = bce(P, y)
#   grads = backward(...)
#   W -= lr * grad_W
#
# PyTorch:
#   optimizer.zero_grad()     # svuota gradienti accumulati
#   p = model(xb)
#   loss = criterion(p, yb)
#   loss.backward()           # riempie .grad
#   optimizer.step()          # update tipo GD/Adam
#
# 🔁 RINFORZO training loop (da V1 cap.06): completa a parole
#   zero_grad → forward → ? → backward → ?
# TUA RISPOSTA:
# ...

# Mini 5.1 — Scrivi un loop di 5 epoche su TensorDataset finto (N=64, d=4)
#            con BCELoss + SGD. Stampa loss ogni epoca.
# TUO CODICE:
# ...


# ==========================================================================
# SEZIONE 6 — Salvare e caricare i pesi (state_dict)
# ==========================================================================
#
# Analogia: state_dict = "export delle manopole" (W e b), non tutto il codice.
#
# torch.save(model.state_dict(), "pesi.pt")
# model2.load_state_dict(torch.load("pesi.pt", map_location="cpu"))
#
# Mini 6.1 — Salva e ricarica i pesi di un nn.Linear(3,1) su file temporaneo.
#            Verifica allclose sui weight.
# TUO CODICE:
# ...


# ==========================================================================
# 🔁 CONFRONTO PRIMA/DOPO (migrato da cap.06 — NON svolto li')
# ==========================================================================
#
# Scrivi in commento 8-10 righe:
#   - cosa NON capivi al cap.01 M3 (neurone)
#   - cosa sembrava magia al cap.02-03
#   - cosa spaventava a derivate / chain / backprop
#   - cosa hai "afferrato" ORA
#   - cosa ti aspetti da PyTorch: API pulita, sotto il cofano = cap.06
#
# BONUS: accuracy di un neurone manuale a pesi inventati vs rete addestrata
#         (anche solo a parole se non hai i pesi del cap.06 sotto mano).
#
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
# Poi, se TORCH_OK: train 2 modelli uguali (raw vs scaled) 20 epoche e
# confronta loss finale.
#
# TUO COMMENTO + CODICE:
# ...


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
# ...


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
# ...

# --------------------------------------------------------------------------
# TODO 2 — 🔧 [REFACTORING] (20 min)
# --------------------------------------------------------------------------
# Riscrivi in PyTorch (nn.Module) la rete 2-layer del cap.06:
#   hidden ReLU, output sigmoid, BCE, SGD.
# Confronta mentalmente con train_rete_2_layer NumPy.
# TUO CODICE:
# ...

# --------------------------------------------------------------------------
# TODO 3 — 🔍 [DEBUG] (15 min)
# --------------------------------------------------------------------------
# Bug tipici (scegline 2 e spiega la fix):
#   A) loss.backward() senza zero_grad → gradienti sommati
#   B) tensor su CUDA e modello su CPU (device mismatch)
#   C) BCELoss con target float vs Long per CrossEntropy (famiglie diverse)
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
# --- Verifica ---
# V1) Dire a PyTorch di tracciare operazioni su quel tensore per .backward()
# V2) Vero nella pratica PyTorch: weight shape (out, in); y = x @ W.T + b
# V3) b → d → a → c  (zero_grad, forward+loss, backward, step)
# V4) Autograd calcola i GRADIENTI; GD/Adam fanno l'UPDATE. Non sono la stessa cosa
# V5) Caricare pesi salvati da GPU su macchina solo-CPU (il tuo PC)
# V6) Tipo un paginatore/carrello: prende pacchetti di esempi dallo scaffale,
#     li mescola, te li porta batch per batch
