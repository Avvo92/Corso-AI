"""
============================================================================
MODULO 3 (DL & CV) - CAPITOLO 08
"CNN e Computer Vision": filtri che scorrono sulle immagini
============================================================================

Nel cap.07 hai imparato PyTorch su dati TABELLARI (righe × colonne):
    Tensor → autograd → nn.Module → DataLoader → training loop → state_dict

Qui cambi il TIPO di input: IMMAGINI.
La matematica del training resta la stessa. Cambia l'architettura:
invece di solo Linear su vettori, usi CONVOLUZIONI (CNN).

Analogia (web):
  - Rete fully-connected su pixel flatten = leggere un PDF carattere per
    carattere in un unico array lunghissimo, senza layout.
  - CNN = selettore CSS / filtro Photoshop che cerca un pattern LOCALE
    (bordo, texture) e lo cerca in tutta l'immagine riutilizzando gli
    stessi pesi (come una classe CSS riusata su tanti elementi).

⚠️ HARDWARE: AMD Vega 10 → niente CUDA in locale.
   Workflow: Cursor (studio) → Google Colab GPU (training Fashion-MNIST)
   → salva .pt → locale con map_location="cpu".

⚠️ PRIVACY: in questo capitolo NIENTE buste paga.
   Dataset: Fashion-MNIST (abbigliamento 28×28, pubblico, low-stakes).
   Il ramo visivo sul prodotto (buste) parte dal cap.09.

Chiusura anticipata cap.07 (13/08/2026): residui migrati come 🔁
(#27 Micro 27.A, #45 5-step, #46 map_location/DataLoader, TODO 5–6, 🏗️).

----------------------------------------------------------------------------
COME LEGGERE QUESTO FILE
----------------------------------------------------------------------------
Stesso schema del cap.07 dove serve:

    [1] ANALOGIA → [2] idea → [3] codice PyTorch → [4] tranelli → [5] mini
    [6] 📚 LETTURA PARALLELA (opzionale, dopo il mini)

----------------------------------------------------------------------------
DEFINITION OF DONE (cap.08)
----------------------------------------------------------------------------
  1) Shape immagine PyTorch: (N, C, H, W)                         → Sez. 1
  2) Cos'è una convoluzione 2D / nn.Conv2d                        → Sez. 2
  3) Pooling e perché riduce H×W                                  → Sez. 3
  4) Alleni una CNN piccola su Fashion-MNIST (Colab)              → Sez. 4
  5) Visualizzi feature maps del primo Conv                       → Sez. 5
  6) Spieghi (Feynman) perché CNN ≫ dense su immagini             → Quiz V

----------------------------------------------------------------------------
MAPPA DEL CAPITOLO
----------------------------------------------------------------------------
   *  QUIZ D'INGRESSO (cerniera cap.07 + residui)              Q1 - Q8
   *  🔁 RINFORZO #27 Micro 27.A  (1-p vs 1-y)                 micro
   *  🔁 RINFORZO #45  5-step + loss.backward()                micro
   *  🔁 RINFORZO #46  map_location + DataLoader               micro
   *  SEZIONE 1  Immagini come tensori (N,C,H,W) + Fashion-MNIST
   *  SEZIONE 2  Convoluzione 2D / nn.Conv2d
   *  SEZIONE 3  Pooling + feature maps (idea)
   *  SEZIONE 4  CNN piccola + training loop (stesso del 07)
   *  SEZIONE 5  Visualizzare feature maps
   *  QUIZ DI VERIFICA                                         V1 - V7
   *  ESERCIZI: COLLOQUIO, REFACTOR, DEBUG, RETRIEVAL,
                INTERLEAVING (Dataset CSV), REAL-WORLD
   *  🏗️ PROGETTO: chiudi M3-07 tabellare + nota prodotto CV
   *  Soluzioni quiz
============================================================================
"""

from __future__ import annotations

import numpy as np
from pathlib import Path

try:
    import torch
    import torch.nn as nn
    import torch.nn.functional as F
    from torch.utils.data import Dataset, DataLoader, TensorDataset
    TORCH_OK = True
except Exception as errore_torch:
    TORCH_OK = False
    print(
        "[AVVISO] torch non utilizzabile in questo ambiente:\n"
        f"         {type(errore_torch).__name__}: {errore_torch}\n"
        "         Esegui Sez. 1–5 e il training su Google Colab (GPU).\n"
    )

# torchvision: serve per Fashion-MNIST (su Colab è già tipicamente ok)
try:
    from torchvision import datasets, transforms
    VISION_OK = True
except Exception as errore_vision:
    VISION_OK = False
    if TORCH_OK:
        print(
            "[AVVISO] torchvision non disponibile:\n"
            f"         {type(errore_vision).__name__}: {errore_vision}\n"
            "         Su Colab: !pip install torchvision  (se manca)\n"
        )

try:
    import matplotlib.pyplot as plt
    PLOT_OK = True
except Exception:
    PLOT_OK = False


# ==========================================================================
# WORKFLOW COLAB (obbligatorio per training)
# ==========================================================================
#
# 1) https://colab.research.google.com → Runtime → GPU
# 2) Verifica:
#       import torch
#       print(torch.__version__, torch.cuda.is_available())
# 3) Copia le sezioni in celle; scarica Fashion-MNIST (automatico).
#    Nota: in cella Colab non c'è __file__ — il file usa Path.cwd()
#    come fallback (cartella /content/dati/fashion_mnist).
# 4) Dopo il train: torch.save(model.state_dict(), "cnn_fashion.pt")
# 5) In locale: load con map_location="cpu"
#
# Analogia: Colab = cantiere GPU in affitto; Cursor = ufficio progetto.
# ==========================================================================
# QUIZ D'INGRESSO (Q1 - Q8) — cerniera cap.07
# ==========================================================================
#
# Rispondi SENZA aprire 07_pytorch_intro.py. Soluzioni in fondo.
#
# Q1) Completa l'ordine del training step PyTorch:
#     ____ → forward+loss → ____ → optimizer.step()
# TUA RISPOSTA:
# optimizer.zero_grad() → forward+loss → loss.backward() → optimizer.step()

# Q2) 🔁 #45 — Elenca in 5 bullet (a parole) il backward 2-layer del cap.06
#     (dZ2 → … → grad_W1). Poi completa: "In PyTorch li fa loss.backward()."
# TUA RISPOSTA:

# troviamo la dL/dZ2 nel caso della bce tramite semplificazione miracolosa p - y.

# il prodotto matriciale della derivata dZ2 e H trasposto ci restituisce il gradiente del W2, e la somma della derivata dZ2 sull'asse 0 il gradiente del b2.

# dH la otteniamo da dZ2 prodotto matriciale con W2 trasposto

# otteniamo poi dZ1 moltiplicando dH per la derivata_relu di Z1

# infine ottiniamo il gradiente di W1 facendo un prodotto matriciale tra X.T e dZ1, e ottieniamo il gradiente del b1 facendo dZ1.sum(axis=0)


# Q3) 🔁 Pattern #27 — Nella derivata della sigmoid usiamo p*(1-?).
#     Il ? è p oppure y? Perché l'altro è un bug tipico?
# TUA RISPOSTA:
#
# la risposta corretta è "p", l'altro è un bug tipico che restituirebbe come risultato dell'espressione p * 1 0 p * 0. Il simbolo è sbagliato, perchè la derivata di sigmoid dipende dalla probibilità, e non dall'etichetta y.

# Q4) Vero/Falso: basta zero_grad() una sola volta prima del for epoch.
#     Se Falso, quando va chiamato?
# TUA RISPOSTA:
# Falso. Va chiamato all'inizio di ogni epoch perchè altrimenti di ciclo in ciclo i grad si sommerebbero, e sballerebbero il lavoro dell'optimizer.step()

# Q5) 🔁 #46 — Hai salvato pesi su Colab (GPU). Sul PC AMD carichi con
#     torch.load(..., map_location=???). Cosa metti e perché?
# TUA RISPOSTA:
#torch.load("percorso_pesi.pt", map_location="cpu"). Uso la cpu perchè cuda non è disponibile con gpu amd

# Q6) 💬 Feynman (max 4 frasi): cos'è un DataLoader rispetto a un Dataset?
# TUA RISPOSTA:
# Dataset: scaffale, su cui c'è tutta la collezione della merce.
# DataLoader: magazziniere, che prende quello che gli chiedo come glielo chiedo


# Q7) `.item()` sulla loss: prima o dopo `backward` se ti serve il grafo?
# TUA RISPOSTA:
# Dopo

# Q8) `requires_grad=True` su un tensore serve a… (1-2 frasi, non solo
#     "chiedere il gradiente")
# TUA RISPOSTA:
# Accende il diario delle operazioni per quel tensore, permettendo ad autograd di calcolare il gradiente.


# ==========================================================================
# 🔁 RINFORZO MIRATO #27 — Micro 27.A: (1-p) non (1-y)
# ==========================================================================
#
# Cap.07: in p*(1-p) hai scritto (1-y). y è l'etichetta 0/1; p è la
# probabilità. La derivata di sigmoid dipende da p.
#
# Analogia: il "quanto è sicuro il modello" (p) non è la "risposta corretta" (y).
#
# Micro 27.A — completa:
#   ds_dp_ok = p * (1 - p)     # <- p
#   # bug tipico: p * (1 - y)
#
# Micro 27.B — una riga: perché y=1 e p=0.9 darebbe un fattore diverso
#   se usassi (1-y) invece di (1-p)?
# TUA RISPOSTA 27.A/B:
# Perchè (1 - 1) != (1 - 0.9)


# ==========================================================================
# 🔁 RINFORZO MIRATO #45 — 5 step + loss.backward()
# ==========================================================================
#
# Non comprimere tutto in una sola formula. Elenca:
#   (1) dZ2   (2) dW2/db2   (3) dH   (4) dZ1 via ReLU'   (5) dW1/db1
# Fill-in: in PyTorch → loss.backward()  (motore: autograd)
# NON esiste auto_grad() come API del corso.
#
# Micro 45.A — riscrivi i 5 bullet + fill-in qui sotto.
# TUA RISPOSTA:
#
# Nel caso di bce, dZ2 tramite semplificazione miracolosa p-y.

# grad_W2 tramite prodotto matriciale di H.T @ dZ2 e grad_b2 facendo dZ2.sum(axis=0)

# dH tramite prodotto matriciale di dZ2 @ W2.T

# dZ1 tramite prodotto di dH * derivata_relu(Z1)

# grad_W1 tramite prodotto matriciale di X.T @ dZ1 e grad_b1 facendo dZ1.sum(axis=0)


# ==========================================================================
# 🔁 RINFORZO MIRATO #46 — map_location + DataLoader=batch
# ==========================================================================
#
# map_location="cpu": i tensori nel file .pt "ricordano" di essere su cuda;
# sul PC senza CUDA serve rimappare il device al load.
#
# DataLoader = magazziniere: prende N esempi dallo scaffale (Dataset),
# li mette sul carrello (batch), eventualmente mescola, te li porta a pacchetti.
#
# Micro 46.A — completa:
#   ckpt = torch.load("modello.pt", map_location="cpu")
# Micro 46.B — in 2 frasi: Dataset vs DataLoader (operativo, non poetico).
# TUA RISPOSTA:
# Dataset è la collezione di dati a nostra disposizione.
# DataLoader è il "carrello" che li prende, li suddivide in batch composti da N esempi, li mescola, e li rende di fatto disponibili per l'addestramento.

# ==========================================================================
# SEZIONE 1 — Immagini come tensori (N, C, H, W)
# ==========================================================================
#
# [1] ANALOGIA
# Una foto è una griglia di pixel. In web/CSS pensi width×height; in ML
# aggiungi i CANALI: grayscale=1, RGB=3. Un batch è una pila di foto.
#
# [2] CONVENZIONE PyTorch (obbligatoria)
#   singolo sample:  (C, H, W)
#   batch:           (N, C, H, W)
# Matplotlib/PIL spesso usano (H, W) o (H, W, C) → serve permute/squeeze
# per plottare.
#
# [3] Fashion-MNIST
# 60k train + 10k test, 28×28, 10 classi (T-shirt, sneaker, …).
# Ideale per la prima CNN: leggero, 1 canale, scaricabile da torchvision.
#
# 📚 LETTURA PARALLELA — [PYTORCH] Cap. 7 "Telling birds from airplanes"
# (dataset torchvision, tensore C×H×W). Noi usiamo Fashion-MNIST al posto
# di CIFAR-10 (più semplice: 1 canale, 28×28). Vedi scheda M03_C08_cnn.md
#
# Tranelli:
#   - print(img.shape) su PIL ≠ tensore: ToTensor() fa il lavoro
#   - ToTensor() porta i pixel in [0, 1] float
#   - label è int (Long) per CrossEntropyLoss

if TORCH_OK and VISION_OK:
    # Su .py locale: cartella del capitolo. Su Colab (cella notebook):
    # __file__ non esiste → usa la cwd (di solito /content).
    try:
        _base_dir = Path(__file__).resolve().parent
    except NameError:
        _base_dir = Path.cwd()
    DATA_DIR = _base_dir / "dati" / "fashion_mnist"
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    transform_base = transforms.Compose([
        transforms.ToTensor(),  # PIL → float tensor (C,H,W) in [0,1]
    ])

    # download=True la prima volta; poi riusa la cartella
    # (su Colab: ok; in locale senza rete fallisce — usa Colab)
    try:
        ds_demo = datasets.FashionMNIST(
            root=str(DATA_DIR),
            train=True,
            download=True,
            transform=transform_base,
        )
        img0, y0 = ds_demo[0]
        print("[Sez.1] sample shape (C,H,W):", tuple(img0.shape), "label:", int(y0))
        # batch finto
        batch = torch.stack([ds_demo[i][0] for i in range(4)], dim=0)
        print("[Sez.1] batch shape (N,C,H,W):", tuple(batch.shape))
    except Exception as e_dl:
        print("[Sez.1] download/load Fashion-MNIST fallito:", e_dl)
        print("         Esegui questa sezione su Colab con rete.")
        ds_demo = None
else:
    ds_demo = None
    print("[Sez.1] salta demo: serve torch + torchvision (Colab).")

# --- MINI-ESERCIZIO 1.1 ---
# Se hai caricato ds_demo: prendi l'immagine 10, stampa shape e label.
# Poi (se PLOT_OK) mostra l'immagine in grayscale:
#   plt.imshow(img.squeeze(), cmap="gray"); plt.title(str(label)); plt.show()
# TUA SOLUZIONE:

immagine_10 = ds_demo[10][0]
etichetta_10 = ds_demo[10][1]

print(immagine_10.shape)
print(etichetta_10)

plt.imshow(immagine_10.squeeze(),
           cmap="gray")
plt.title(str(etichetta_10))
plt.show()


# --- MINI-ESERCIZIO 1.2 ---
# Completa a parole: perché Matplotlib vuole spesso squeeze/permute
# rispetto a un tensore (1, 28, 28)?
# TUA RISPOSTA:
#
# tensore 1×28×28 = un canale grigio; squeeze lo rende 28×28 per imshow.


# ==========================================================================
# SEZIONE 2 — Convoluzione 2D (il cuore della CNN)
# ==========================================================================
#
# [1] ANALOGIA
# Un kernel (filtro) 3×3 è un "timbre" di pesi. Lo appoggi su ogni zona
# dell'immagine, fai prodotto-somma locale, ottieni un nuovo valore.
# Stesso timbre su tutta la foto = pesi CONDIVISI (parameter sharing).
#
# [2] PERCHÉ NON flatten + Linear su tutti i pixel? (teoria per 📚 e colloquio)
#
# Immagine 28×28 → flatten = vettore di 784 numeri. Un nn.Linear(784 → …)
# tratta ogni pixel come "colonna di CSV" indipendente.
#
# Problemi di una rete SOLO dense (fully-connected) sulle immagini:
#
#   (A) TROPPI PARAMETRI
#       Già Linear(784, 256) ≈ 200k pesi; su foto più grandi esplode.
#       Overfitting facile: "impara a memoria" invece di regole utili.
#
#   (B) IGNORA LA GEOMETRIA
#       Pixel vicini (un bordo, una manica) sono correlati. Il dense non
#       "sa" che l'indice 10 e l'indice 11 sono vicini sulla griglia: per
#       lui sono solo due feature diverse, come prezzo e CAP.
#
#   (C) POCA INVARIANZA ALLA TRASLAZIONE
#       Lo stesso pattern "bordo verticale" in alto a sinistra o spostato
#       di 3 pixel diventa un insieme di pesi diverso da reimparare.
#       La CNN riusa LO STESSO filtro ovunque (parameter sharing).
#
#   (D) COSA FA MEGLIO CONV + POOL
#       Conv = cerca pattern LOCALI con pochi pesi riusati.
#       Pool = rimpicciolisce e tollera piccoli spostamenti.
#       Poi un Linear piccolo classifica le feature (non i pixel grezzi).
#       Stessa "voglia di imparare" (training), ma rappresentazione migliore.
#
# Analogia web: dense = un form gigante con 784 campi scollegati;
# CNN = componenti CSS riusati su ogni zona della pagina.
# Riferimento: [PYTORCH] Cap. 8 §8.1; scheda M03_C08_cnn.md
#
# [3] CODICE
#   nn.Conv2d(in_channels, out_channels, kernel_size=3, padding=1)
#   - in_channels: 1 per Fashion-MNIST, 3 per RGB
#   - out_channels: quanti filtri diversi impari (= canali in uscita)
#   - padding=1 con kernel 3 → H,W restano uguali (comodo)
#
# Formula shape (stride=1 tipico):
#   H_out = floor((H + 2*pad - k) / stride) + 1
# (stessa idea del Ponte: conta indici / "finestre" che entrano)
#
# Tranelli:
#   - Conv2d vuole 4D: (N,C,H,W) anche per 1 immagine → unsqueeze(0)
#   - out_channels ≠ "classi": sono feature maps intermedie

if TORCH_OK:
    # Demo: un Conv2d random su un batch finto 4×1×28×28
    conv_demo = nn.Conv2d(in_channels=1, out_channels=8, kernel_size=3, padding=1)
    x_fake = torch.randn(4, 1, 28, 28)
    with torch.no_grad():
        y_fake = conv_demo(x_fake)
    print("[Sez.2] Conv2d out shape:", tuple(y_fake.shape))  # (4, 8, 28, 28)

# 📚 LETTURA PARALLELA — [PYTORCH] Cap. 8 §8.1–8.2 "The case for convolutions"
# + [GERON] Cap. 14 (Convolutional Layers): filtri e feature maps.
# Scheda: docs/libri_corso/schede/M03_C08_cnn.md

# --- MINI-ESERCIZIO 2.1 ---
# Calcola a mano H_out, W_out per:
#   H=W=28, kernel=3, padding=0, stride=1
# TUA RISPOSTA (numeri):

# H_out = ((28 + 2*0 - 3) / 1) + 1 = 26
# W_out = ((28 + 2*0 - 3) / 1) + 1 = 26

# --- MINI-ESERCIZIO 2.2 ---
# Scrivi UNA riga: crea nn.Conv2d(1 → 16 filtri, kernel 5, padding 2)
# e applica a torch.randn(2, 1, 28, 28); stampa shape uscita.
# TUA SOLUZIONE:

my_conv_demo = nn.Conv2d(in_channels=1, out_channels=16, kernel_size=5, padding=2)

x_demo = torch.randn(2, 1, 28, 28)

with torch.no_grad():
    out_my_conv_demo = my_conv_demo(x_demo)

print(out_my_conv_demo.shape)

# ==========================================================================
# SEZIONE 3 — Pooling + feature maps
# ==========================================================================
#
# [1] ANALOGIA
# Max-pool 2×2: in ogni finestrella 2×2 tieni solo il valore più alto.
# Come fare uno thumbnail che conserva il "contrasto più forte".
# Riduci H e W (tipicamente /2) → meno calcolo nei layer dopo,
# e il campo ricettivo "vede" una zona più ampia dell'immagine originale.
#
# [2] CODICE
#   nn.MaxPool2d(kernel_size=2)  # stride default = kernel → dimezza
#
# Feature map = l'uscita di un Conv (o Conv+ReLU): una "mappa" per ogni
# filtro che dice DOVE quel pattern si è attivato.
#
# Tranelli:
#   - dopo 2 pool su 28×28 → 7×7 (28/2/2); se sbagli, il Linear esplode
#   - AvgPool vs MaxPool: qui usiamo Max (classico per classificazione)

if TORCH_OK:
    pool = nn.MaxPool2d(2)
    with torch.no_grad():
        z = pool(torch.randn(1, 8, 28, 28))
    print("[Sez.3] dopo MaxPool2d(2):", tuple(z.shape))  # (1, 8, 14, 14)

# --- MINI-ESERCIZIO 3.1 ---
# Parti dalla shape: (N, 16, 28, 28)
#   (pensa: batch N, 16 feature map, griglia 28×28)
#
# Applica IN ORDINE:
#   A) MaxPool2d(2)              → dimezza H e W; i canali restano 16
#   B) Conv2d con out_channels=32 e padding che mantiene H e W
#                                → C diventa 32; H e W uguali a dopo A
#   C) MaxPool2d(2)              → dimezza di nuovo H e W; C resta 32
#
# Qual è la shape finale?  (N, ?, ?, ?)
# Trucco: aggiorna a mente solo C, H, W a ogni step A → B → C.
# TUA RISPOSTA:
# (5, 32, 7, 7)

my_maxpool_demo = nn.MaxPool2d(2)
my_conv2d_demo = nn.Conv2d(in_channels=16, out_channels=32, kernel_size=3, padding=1)

start_batch = torch.randn(5, 16, 28, 28)
out_maxpool = my_maxpool_demo(start_batch)
out_conv = my_conv2d_demo(out_maxpool)
out_maxpool2 = my_maxpool_demo(out_conv)

print(f"Shape finale: {out_maxpool2.shape}")


# --- MINI-ESERCIZIO 3.2 ---
# Vero/Falso: il pooling impara pesi come Conv2d.
# TUA RISPOSTA:
# Falso. Il pooling prende il massimo valore all'interno di un timbro di dimensione kernel_size = int, scorrendo sopra tutta la feature map passata dal Conv2d, e restituisce una sorta di thumbnail della stessa.

# ==========================================================================
# SEZIONE 4 — CNN piccola + training (Fashion-MNIST)
# ==========================================================================
#
# Architettura didattica (non ResNet — quello è cap.09):
#
#   Conv(1→16, 3, pad1) → ReLU → MaxPool(2)     # 28→14
#   Conv(16→32, 3, pad1) → ReLU → MaxPool(2)    # 14→7
#   Flatten → Linear(32*7*7 → 10)               # 10 classi
#
# Loss: CrossEntropyLoss (multiclasse) = softmax+NLL internamente.
#   logits: (N, 10)   target: (N,) long
#
# Training loop = IDENTICO al cap.07:
#   zero_grad → forward → loss → backward → step
# Cambia solo il modulo e la loss (BCE → CrossEntropy).
#
# 📚 LETTURA PARALLELA — [PYTORCH] Cap. 8 (CNN in azione su immagini)
# Noi: Fashion-MNIST invece di birds/airplanes CIFAR.

FASHION_CLASSES = [
    "T-shirt/top", "Trouser", "Pullover", "Dress", "Coat",
    "Sandal", "Shirt", "Sneaker", "Bag", "Ankle boot",
]


if TORCH_OK:

    class PiccolaCNN(nn.Module):
        """CNN didattica per Fashion-MNIST (1×28×28 → 10 classi)."""

        def __init__(self) -> None:
            super().__init__()  # collega questa classe al sistema nn.Module di PyTorch

            # Blocco "visione": estrae feature map dall'immagine.
            # Shape tipica lungo il percorso (N = batch):
            #   (N, 1, 28, 28)  →  (N, 16, 28, 28)  →  (N, 16, 14, 14)
            #                →  (N, 32, 14, 14)  →  (N, 32, 7, 7)
            self.features = nn.Sequential(
                # 16 filtri 3×3; pad=1 → H,W restano 28. C: 1 → 16
                nn.Conv2d(1, 16, kernel_size=3, padding=1),
                # spegne i negativi; shape invariata
                nn.ReLU(),
                # thumbnail: H,W / 2 → 14×14; C resta 16
                nn.MaxPool2d(2),
                # altri 32 filtri; pad=1 → H,W restano 14. C: 16 → 32
                nn.Conv2d(16, 32, kernel_size=3, padding=1),
                nn.ReLU(),
                # di nuovo /2 → 7×7; C resta 32
                nn.MaxPool2d(2),
            )
            # Testa di classificazione: vettore 32*7*7=1568 → 10 logits (una per classe)
            self.classifier = nn.Linear(32 * 7 * 7, 10)

        def forward(self, x: torch.Tensor) -> torch.Tensor:
            # x in ingresso: (N, 1, 28, 28)
            x = self.features(x)          # → (N, 32, 7, 7) feature map finali
            x = torch.flatten(x, 1)       # → (N, 1568); dim 0 = batch, non si schiaccia
            return self.classifier(x)     # → (N, 10) logits grezzi (non probabilità)

    def accuracy_logits(logits: torch.Tensor, y: torch.Tensor) -> float:
        # logits: (N, 10) punteggi; y: (N,) indici classe veri (0..9)
        pred = logits.argmax(dim=1)  # per ogni riga, indice del logit più alto
        # media di True/False → accuracy in [0, 1]; .item() → float Python
        return (pred == y).float().mean().item()

    def train_cnn_epochs(
        model: nn.Module,
        loader_train: DataLoader,
        loader_val: DataLoader,
        device: torch.device,
        epochs: int = 3,
        lr: float = 1e-3,
    ) -> list[dict[str, float]]:
        """Loop standard cap.07 — multiclasse (mini-batch SGD/Adam)."""
        # Adam aggiorna tutti i pesi del modello; lr = ampiezza dei passi
        opt = torch.optim.Adam(model.parameters(), lr=lr)
        # CrossEntropy: softmax+NLL interni; vuole logits (N,10) e target Long (N,)
        crit = nn.CrossEntropyLoss()
        history: list[dict[str, float]] = []  # metriche per epoch
        model.to(device)  # pesi su CPU o CUDA (stesso device dei batch)

        for ep in range(1, epochs + 1):
            model.train()  # attiva dropout/batchnorm in train (qui quasi no-op, ma idioma)
            loss_sum, n_seen = 0.0, 0
            for xb, yb in loader_train:  # xb: (B,1,28,28), yb: (B,)
                xb, yb = xb.to(device), yb.to(device)  # dati sullo stesso device del modello
                opt.zero_grad()  # azzera .grad accumulati (ogni BATCH)
                logits = model(xb)  # forward → (B, 10)
                loss = crit(logits, yb)  # scalare: quanto sbagliamo sul batch
                loss.backward()  # riempie .grad sui pesi (autograd)
                opt.step()  # aggiorna i pesi con Adam
                # log: .item() DOPO backward (float Python); * B per media pesata
                loss_sum += loss.item() * xb.size(0)
                n_seen += xb.size(0)

            # --- valutazione (niente update pesi) ---
            model.eval()  # modo inferenza
            correct, n_val = 0, 0
            with torch.no_grad():  # non costruire grafo → risparmio RAM
                for xb, yb in loader_val:
                    xb, yb = xb.to(device), yb.to(device)
                    logits = model(xb)
                    correct += (logits.argmax(1) == yb).sum().item()
                    n_val += yb.size(0)

            row = {
                "epoch": float(ep),
                "loss_train": loss_sum / max(n_seen, 1),  # loss media sull'epoch
                "acc_val": correct / max(n_val, 1),  # accuracy sul validation set
            }
            history.append(row)
            print(
                f"[Sez.4] epoch {ep}: loss_train={row['loss_train']:.4f} "
                f"acc_val={row['acc_val']:.3f}"
            )
        return history

    def feature_maps_primo_conv(
        model: PiccolaCNN, img_chw: torch.Tensor
    ) -> torch.Tensor:
        """img (1,H,W) o (1,1,H,W) → (16, H, W) dopo primo Conv+ReLU."""
        # assicura batch dim: Conv2d vuole 4D (N,C,H,W)
        if img_chw.dim() == 3:
            img_chw = img_chw.unsqueeze(0)  # (1,H,W) → (1,1,H,W) se C già c'è: (C,H,W)→(1,C,H,W)
        # Sequential: [0]=primo Conv, [1]=prima ReLU (vedi __init__)
        conv0 = model.features[0]
        relu0 = model.features[1]
        with torch.no_grad():  # solo visualizzazione, niente gradienti
            maps = relu0(conv0(img_chw))  # (1, 16, 28, 28) tipicamente
        return maps.squeeze(0)  # togli N → (16, 28, 28) una mappa per filtro


# Demo training: SOLO se torch+vision ok. Su Colab usa subset o full.
# Di default usiamo un SUBSET per non bloccare la macchina (CPU).
if TORCH_OK and VISION_OK and ds_demo is not None:
    # GPU se c'è CUDA (Colab), altrimenti CPU (PC AMD)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print("[Sez.4] device:", device)

    # Subset piccolo = smoke test rapido (non tutto Fashion-MNIST)
    n_train_smoke, n_val_smoke = 2000, 500
    ds_train_full = datasets.FashionMNIST(
        root=str(DATA_DIR), train=True, download=False, transform=transform_base
    )
    ds_test_full = datasets.FashionMNIST(
        root=str(DATA_DIR), train=False, download=False, transform=transform_base
    )
    # prime n immagini come train/val di prova
    ds_train = torch.utils.data.Subset(ds_train_full, range(n_train_smoke))
    ds_val = torch.utils.data.Subset(ds_test_full, range(n_val_smoke))

    # carrelli: shuffle in train, batch fissi in val
    loader_tr = DataLoader(ds_train, batch_size=64, shuffle=True)
    loader_va = DataLoader(ds_val, batch_size=128, shuffle=False)

    torch.manual_seed(42)  # riproducibilità (pesi iniziali / shuffle controllato)
    cnn = PiccolaCNN()
    # Decommenta su Colab per allenare (2–3 epoche sul subset bastano come smoke):
    # hist = train_cnn_epochs(cnn, loader_tr, loader_va, device, epochs=2)
    print(
        "[Sez.4] PiccolaCNN creata. Per trainare: decommenta "
        "train_cnn_epochs(...) sopra (meglio su Colab GPU)."
    )
    # Sanity: un forward finto deve dare (2, 10)
    with torch.no_grad():
        logits0 = cnn(torch.randn(2, 1, 28, 28))
    print("[Sez.4] logits shape attesa (2,10):", tuple(logits0.shape))
else:
    print("[Sez.4] salta demo CNN (serve torch+vision+dataset).")

# 📚 [LIBRO] — Ispirato a [PYTORCH] Cap.7→8 (adattato Fashion-MNIST)
#
# PRIMA leggi (o rileggi) in Sez. 2 il blocco
#   "[2] PERCHÉ NON flatten + Linear su tutti i pixel?"
# lì trovi parametri, geometria, traslazione, ruolo di Conv+Pool.
#
# Poi, CON PAROLE TUE (5–8 frasi, niente copia dal PDF / dalla Sez.2):
# perché una rete solo Linear su flatten(28*28) generalizza peggio di
# Conv+Pool, anche a parità di "voglia di imparare" (stesso training).
#
# TUA RISPOSTA (qui sotto o in TODO 1 negli esercizi finali):
#
# Una rete di soli layer dense, già solo al primo livello arriva facilmente ad avere decine di migliaia di pesi. Per immagini grandi esplode facilmente. Ignora la geometria perchè non è in grado di riconoscere la correlazione di pixel vicini tra loro, ma tratta ogni singolo pixel come una feature a se stante. Non sopporta la traslazione, se nel immagine lo stesso schema è spostato anche sono di un pixel, la rete lo tratta come un nuovo insieme di pesi da imparare. Conv+pool servono a riconoscere schemi simili, e a trasformare ridimensionando i risultati di ogni livello. 


# --- MINI-ESERCIZIO 4.1 ---
# Conta a mano i parametri SOLO del primo Conv2d(1,16,k=3,pad=1):
#   pesi = out_ch * in_ch * k * k ; bias = out_ch
# TUA RISPOSTA (numero totale):
#
# Per i pesi il numero di parametri della Conv2d è = canali_immagine * n_kernel * base_kernel * altezza_kernel -> 1 * 16 * 3 * 3 -> 144; Il N_bias è = N_kernel -> 16; Totale = 160

# --------------------------------------------------------------------------
# CrossEntropyLoss: target = INDICE di classe (Long), non one-hot
# --------------------------------------------------------------------------
#
# [1] ANALOGIA
# Hai 10 cassetti (classi 0..9). Per ogni esempio non consegni 10 adesivi
# "è / non è" (one-hot): consegni il NUMERO del cassetto giusto, es. 7 = Sneaker.
#
# [2] COSA VUOLE PyTorch
#   logits:  (N, C)   float   — punteggi grezzi (C=10 per Fashion-MNIST)
#   target:  (N,)     long    — un intero per riga: la classe vera (0..C-1)
#
# Esempio batch N=3:
#   y = tensor([3, 0, 7])           # Dress, T-shirt, Sneaker
#   NON serve: [[0,0,0,1,0,...], ...]  # one-hot float (N, 10)
#
# [3] PERCHÉ
#   - CrossEntropyLoss fa (dentro): softmax sui logits + NLL rispetto alla
#     classe indicata dall'indice. L'API è pensata così: più compatta e
#     standard in classificazione multiclasse.
#   - One-hot float è tipico di altre loss (es. soft-label / BCE multi-label).
#     Qui le classi sono MUTUALMENTE ESCLUSIVE: un solo indice basta.
#   - dtype Long = interi 64-bit usati come indici (come un indice di array).
#
# [4] CONFRONTO COL CAP.07
#   BCEWithLogitsLoss (binario): target float 0.0/1.0 shape (N,1) o (N,)
#   CrossEntropy (multiclasse): target Long shape (N,) con valori 0..C-1
#
# --- MINI-ESERCIZIO 4.2 ---
# Perché CrossEntropyLoss vuole target Long (N,) e non float one-hot?
# (Rispondi con parole tue, dopo aver letto il blocco sopra.)
# TUA RISPOSTA:
#
# perchè le classi sono esclusive, quindi mi basta solo prendere in considerazione una sola classe per immagine. Gli interi nel Long(N, ) sono usati come indici per sapere quale risultato del vettore output del softmax prendere per la CE. Usare un float one-hot sarebbe ridondante, la CE non ne ha bisogno.


# ==========================================================================
# SEZIONE 5 — Visualizzare le feature maps
# ==========================================================================
#
# Idea: prendi un'immagine, passa solo il PRIMO Conv+ReLU, ottieni
# 16 mappe 28×28 (con pad=1). Plottale in una griglia: vedi "cosa eccita"
# ogni filtro (anche a pesi random all'inizio — dopo il train cambiano).
#
# Analogia: 16 "evidenziatori" diversi sulla stessa pagina.

# --- MINI-ESERCIZIO 5.1 ---
#
# Obiettivo: "vedere" cosa fa il primo strato convoluzionale su UNA immagine
# reale di Fashion-MNIST — non i 10 logits finali, ma le attivazioni intermedie
# (feature maps): una mappa per ciascuno dei 16 filtri del primo Conv (+ ReLU).
#
# Prerequisiti (già visti in Sez.4 / demo):
#   - un modello `PiccolaCNN` (anche appena creato, anche non addestrato);
#   - un tensore immagine nel formato che la rete si aspetta (canale + H + W).
# Nel capitolo c'è già un helper che estrae solo il primo Conv+ReLU: usalo
# se ti è comodo, oppure ottieni lo stesso risultato a mano dal modulo.
#
# Cosa verificare:
#   1) Quante mappe ottieni? Che shape ha il tensore risultante, e perché
#      H e W restano 28×28 con il padding usato in PiccolaCNN?
# Ottengo un tensore di shape (16, 28, 28). Restano uguali perchè ((h (o w) + 2p - k) / stride) + 1 = ((28 + 2 - 3) / 1) + 1 = 28
#   2) Se puoi plottare (PLOT_OK / ambiente con Matplotlib): mostra tutte le
#      mappe in una griglia di figure, in scala di grigi, così confronti
#      a colpo d'occhio i diversi "evidenziatori" sullo stesso capo.
#
# Nota: a pesi iniziali (random) le mappe possono sembrare rumore; dopo un
# po' di training spesso emergono bordi/texture. Qui conta il pipeline di
# estrazione + shape + visualizzazione, non la bellezza artistica.
#
# TUA SOLUZIONE:
#
img = ds_train[1][0]
maps = feature_maps_primo_conv(model=PiccolaCNN(), img_chw=img)
print(maps.shape)

fig, axes = plt.subplots(4, 4, figsize=(14, 10))
fig.suptitle("Visualizzazione Features Maps + ReLU", fontsize=18, fontweight="bold")
for i, m in enumerate(maps):
    m = m.detach().cpu().numpy()
    ax = axes.flatten()[i]
    ax.imshow(m, cmap="gray")

plt.show()

# --- MINI-ESERCIZIO 5.2 ---
# Vero/Falso: le feature maps del primo layer sono già le probabilità delle 10 classi.
# TUA RISPOSTA:
# falso, sono la risposta di n_kernel, ognuna delle quali e la mappa delle risposte che ha fornito il kernel specifico ad ogni punto in cui è stato appoggiato sull immagine.


# ==========================================================================
# QUIZ DI VERIFICA (V1 - V7)
# ==========================================================================
#
# V1) Shape di un batch Fashion-MNIST tipico con batch_size=32?
# TUA RISPOSTA: (32, 1, 28, 28)
#

# V2) nn.Conv2d(1, 8, 3, padding=1) su (4,1,28,28) → shape uscita?
# TUA RISPOSTA:
#(4, 8, ((28 + 2 - 3) / 1) + 1, ((28 + 2 - 3) / 1) + 1) -> (4, 8, 28, 28)

# V3) Trova l'errore concettuale:
#     "MaxPool2d impara 4 pesi per ogni finestra 2×2."
# TUA RISPOSTA:
# Falso. MaxPool2d con finestra 2*2 semplicemente prende la feature map del layer Conv e in pratica prende in esame di quella mappa 4 punti per volta, restituendo per ognuno solo il valore più alto della specifica finestra, iscrivendo il risultato in un nuovo tensore. Questo tensore, supponendo che in input il MaxPool abbia preso un tensore di shape (4, 8, 28, 28), avrà shape (4, 8, 14, 14), ossia avrà ridotto ogni feature map di 4 volte la sua dimensione originale.

# V4) Completa: dopo due MaxPool2d(2) su 28×28, H=W= ___
# TUA RISPOSTA:
# 14 -> 7

# V5) Ordine corretto nel loop: (a) step (b) zero_grad (c) backward (d) loss
# TUA RISPOSTA (lettere in ordine):
# b, d, c, a

# V6) map_location serve quando… (1 frase operativa)
# TUA RISPOSTA:
# la map_location serve nel load di uno state_dict di un modello, nel caso ad esempio in cui i pesi della rete siano caricati da Colab (che usa gpu / cuda nvidia per addestrare), ed ora noi li stiamo portando in locale nel nostro pc che invece fa girare il modello in cpu

# V7) 💬 Feynman: perché una CNN ha senso per immagini mentre una rete
#     solo fully-connected su pixel flatten fa più fatica? (5–8 frasi,
#     analogia web/Photoshop ok; puoi citare località + pesi condivisi)
# TUA RISPOSTA:
# per 4 motivi principali. La rete layer dense non è indicata per shape che riporterebbero numero di pesi enormi, poichè tratta ogni pixel come colonna di un csv(già un Linear(784, 256), crea centinaia di migliaia di pesi).
# Un layer dense non capisce la geometria. Ogni pixel è per lui una feature a se stante, quindi non vede le correlazioni tra pixel vicini. Una CNN risolve questo problema perchè analizza e filtra pezzi dell'immagine insieme, riconoscendo pattern specifici, e riutilizzando gli stessi pesi di ogni kernel su tutta l'immagine, piuttosto che crearne uno specifico per ogni pixel visto da ogni neurone.
# Un LayerDense a poca invarianza alla traslazione. Se lo schema che ricerchiamo nell'immagine è spostato anche solo di un pixel, la rete deve addestrare nuovi pesi specifici per poter riconoscerlo. La CNN riconosce i pattern ovunque si trovino proprio grazie alla convoluzione dei kernel.
# Conv+pool sono più efficiente sulle immagine. Conv riconosce gli schemi, mentre maxpool sintetizza. Usiamo un linear solo in uscita prima di soft max per i logit delle classi.

# ==========================================================================
# ESERCIZI PRATICI
# ==========================================================================

# --------------------------------------------------------------------------
# TODO 1 — 🎯 [COLLOQUIO]
# --------------------------------------------------------------------------
# Spiega a un collega web (senza formule) in max 10 frasi:
#   convoluzione, pooling, feature map, e perché non flatten+MLP.
# TUA RISPOSTA:
# la convoluzione in una CNN consiste nel passare vari filtri su tutta la grandezza dell immagine, alla ricerca di schemi ricorrenti. Ogni filtro, per ogni punto dell'immagine su cui passa da un punteggio riguardo lo schema di cui è alla ricerca e li inserisce una mappa (feature map). Il pooling fa una sintesi di questi punteggi, tenendo solo i punteggi più alti e rilevanti all'interno di piccole finestre(che come nella convoluzione viene passata questa volta su tutta la feature map). flatten+MLP non è una scelta efficente, perchè una rete layer dense ha bisogno di pesi per ogni pixel, e non riesce a riconoscere schemi geometrici perchè vede i pixel singolarmente e non in correllazioni con i loro vicini (a differenza della CNN che usa e riusa gli stessi filtri di pesi su tutta l'immagine). Inolte, se anche lo schema che cerchiamo si sposta di un solo pixel, la rete fully connected deve addestrare un neurone specifico e tutti i suoi pesi solo per poter vedere questo piccolissimo spostamento.


# --------------------------------------------------------------------------
# TODO 2 — 🔧 [REFACTORING]
# --------------------------------------------------------------------------
# Questa CNN "brutta ma funzionante" ripete codice. Riscrivila pulita
# (Sequential o metodi chiari), stessa shape di PiccolaCNN.
#
# class CnnBrutta(nn.Module):
#     def __init__(self):
#         super().__init__()
#         self.c1 = nn.Conv2d(1, 16, 3, 1, 1)
#         self.c2 = nn.Conv2d(16, 32, 3, 1, 1)
#         self.fc = nn.Linear(1568, 10)  # magico: 32*7*7
#     def forward(self, x):
#         x = torch.relu(self.c1(x))
#         x = torch.max_pool2d(x, 2)
#         x = torch.relu(self.c2(x))
#         x = torch.max_pool2d(x, 2)
#         x = x.view(x.size(0), -1)
#         return self.fc(x)
#
# TUA SOLUZIONE (classe rifattorizzata):

class CnnBella(nn.Module):
    def __init__(self) -> None:
        super().__init__()
        self.features = nn.Sequential(
            nn.Conv2d(1, 16, kernel_size=3, stride=1, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Conv2d(16, 32, kernel_size=3, stride=1, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),
        )
        self.classifier = nn.Linear(32 * 7 * 7, 10)
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = self.features(x)
        x = torch.flatten(x, 1)
        return self.classifier(x)



# --------------------------------------------------------------------------
# TODO 3 — 🔍 [DEBUG]
# --------------------------------------------------------------------------
# Stack trace / sintomo (simulato):
#
#   RuntimeError: mat1 and mat2 shapes cannot be multiplied (64x3200 and 1568x10)
#
# Contesto: batch 64, qualcuno ha messo Linear(32*10*10, 10) oppure ha
# dimenticato un MaxPool. Diagnosi in 3 bullet + fix.
# TUA RISPOSTA:
#
# il problema può essere un disallineamento dei maxpool oppure shape sbagliata per l'ingresso nel linear finale. Il fix consiste nel verificare se i maxpool siano stati entrambi inseriti e siano corretti, oppure agire sulla shape attesa nell'ingresso del linear

# --------------------------------------------------------------------------
# TODO 4 — 🧠 [RETRIEVAL]
# --------------------------------------------------------------------------
# Senza guardare Sez. 4: riscrivi da zero (10–20 righe) il corpo di UN
# epoch di training per una CNN già creata: zero_grad → … → step,
# e calcola loss media con .item() nel posto giusto.
# TUA SOLUZIONE:


# --------------------------------------------------------------------------
# TODO 5 — 🔀 [INTERLEAVING]  (migrato da cap.07 TODO 5)
# --------------------------------------------------------------------------
# Dataset CUSTOM su dati TABELLARI (ponte M2 → PyTorch), non immagini.
# Usa modulo_02_ml/dati/case.csv (o path che conosci):
#   - leggi con pandas
#   - X = feature numeriche; y = target binario (come nel M2)
#   - class TabularDataset(Dataset): __len__ / __getitem__ → tensor float / long
#   - DataLoader batch_size=32
#   - nn.Sequential(Linear, ReLU, Linear(1)) + BCEWithLogitsLoss
#   - 1 epoca di train (basta per dimostrare il filo)
#
# Collega: stesso Dataset/DataLoader del cap.07, feature del M2, idea CNN dopo.
# TUA SOLUZIONE:


# --------------------------------------------------------------------------
# TODO 6 — 🌊 [REAL-WORLD]  (migrato da cap.07 TODO 6)
# --------------------------------------------------------------------------
# Scenario: un collega ti manda "foto prodotti" 28×28 ma metà dei file è
# corrotta, le label arrivano in un CSV disallineato (nomi file ≠ indici),
# e ti chiede "allenami una CNN per domani".
# Non c'è una sola soluzione. Scrivi:
#   (a) 5 controlli che faresti PRIMA di trainare
#   (b) cosa rifiuteresti di fare "in fretta" e perché
#   (c) metrica che guarderesti oltre all'accuracy se le classi sono sbilanciate
# TUA RISPOSTA:
#


# --------------------------------------------------------------------------
# TODO 7 — Shape gymnastics (Ponte + CNN)
# --------------------------------------------------------------------------
# Input (8, 1, 64, 64). Dopo:
#   Conv2d(1, 16, 3, padding=1) → ReLU → MaxPool2d(2)
#   Conv2d(16, 32, 3, padding=1) → ReLU → MaxPool2d(2)
#   Flatten
# Qual è la shape prima del Linear? Quante feature in ingresso al Linear?
# TUA RISPOSTA:
#


# ==========================================================================
# 🏗️ PROGETTO INCREMENTALE — M3 cap.08
# ==========================================================================
#
# A) PRODOTTO (Validator / buste paga): NON si tocca.
#    Qui solo Fashion-MNIST pubblico. Documenta in 3 bullet nel diario
#    (o qui sotto) cosa servirà dal cap.09 (transfer + anonimizzazione).
#
# B) CHIUSURA DEBITO M3-07 (tabellare PyTorch):
#    Completa TODO 5 (Dataset CSV + train 1 epoca) OPPURE, se già fatto,
#    salva state_dict del modello tabellare in
#      modulo_03_dl_cv/dati/pesi/pesi_m3_07_tabellare.pt
#    con map_location in mente per il load.
#
# C) CNN portfolio (opzionale ma consigliato su Colab):
#    Allena PiccolaCNN su SUBSET o full Fashion-MNIST (3–5 epoche),
#    stampa acc_val, salva cnn_fashion.pt, plotta 1 griglia feature maps.
#
# TUA NOTA / CHECKLIST:


# ==========================================================================
# CHECKPOINT AUTO-VALUTAZIONE (C1 - C5) — opzionale
# ==========================================================================
# C1) So spiegare (N,C,H,W) senza guardare gli appunti?     [ ]
# C2) So calcolare H_out di una Conv a mano?                 [ ]
# C3) So perché MaxPool non ha pesi?                         [ ]
# D4) Ho eseguito almeno 1 epoca CNN su Colab?               [ ]
# C5) Ho chiuso TODO 5 (debito tabellare) o schedulato?      [ ]


# ==========================================================================
# SOLUZIONI QUIZ (guarda solo DOPO il tentativo)
# ==========================================================================
#
# --- INGRESSO ---
# Q1) zero_grad → forward+loss → backward → step
# Q2) (1) dZ2 (2) dW2/db2 (3) dH (4) dZ1=dH⊙ReLU' (5) dW1/db1 ;
#     fill-in: loss.backward() / autograd
# Q3) ? = p  (non y). y è etichetta; derivata sigmoid = p(1-p)
# Q4) Falso — zero_grad ogni batch/step
# Q5) "cpu" — pesi salvati su CUDA non caricabili su device assente
# Q6) Dataset = scaffale campioni; DataLoader = carrello batch (+shuffle)
# Q7) .item() per log DOPO aver fatto backward (o su loss già usata
#     per backward); non "staccare" prima se ti serve il grafo
# Q8) Dice ad autograd di tracciare le operazioni su quel tensore per
#     costruire il grafo e riempire .grad al backward
#
# --- RINFORZI ---
# 27.A) 1 - p
# 27.B) (1-y)=0 se y=1 → azzeri il fattore; (1-p)=0.1 resta informativo
# 45) vedi Q2
# 46.A) "cpu"   46.B) come Q6
#
# --- VERIFICA ---
# V1) (32, 1, 28, 28)
# V2) (4, 8, 28, 28)
# V3) Pooling NON impara pesi: è un downsampling fisso (max/avg)
# V4) 7
# V5) b → d → c → a   (zero_grad, loss, backward, step)
# V6) caricare checkpoint da un device a un altro (es. GPU→CPU)
# V7) Criteri: località, parameter sharing, invarianza/equivarianza
#     traslazione, parametri ≪ dense su flatten; analogia filtro/CSS ok
#
# --- MINI UTILI ---
# 2.1) H_out = 28 - 3 + 1 = 26 (padding 0)
# 3.1) (N, 32, 7, 7)
# 3.2) Falso
# 4.1) 16*1*3*3 + 16 = 144+16 = 160
# 5.2) Falso — sono attivazioni intermedie, non probabilità classi
# TODO 7) dopo pool2: (8, 32, 16, 16) → flatten 32*16*16 = 8192
#
# Fine capitolo 08.
