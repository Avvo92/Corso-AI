"""
============================================================================
 MODULO 1 — ESERCIZIO 08: I Tensori Spiegati
 Cos'è un Tensor, Perché Ti Serve, e Perché Dovresti Amarlo
============================================================================

 TEORIA: Cos'è un Tensor?

 Un Tensor NON è niente di spaventoso. È semplicemente un "contenitore
 di numeri" con una forma (shape) definita. L'hai già usato senza saperlo!

 Pensa così:
   - Un NUMERO singolo (es. 42)        → Tensor 0D (scalare)
   - Una LISTA di numeri (es. [1,2,3]) → Tensor 1D (vettore)
   - Una TABELLA di numeri             → Tensor 2D (matrice)
   - Un CUBO di numeri                 → Tensor 3D
   - E si può andare avanti...         → Tensor 4D, 5D, ecc.

 ANALOGIA DAL MONDO WEB:
 ┌─────────────────────────────────────────────────────────────────┐
 │  Pensa a un sito e-commerce:                                   │
 │                                                                 │
 │  • Un PREZZO (42.99)           = Scalare (0D) — un solo valore │
 │  • Una RIGA dell'ordine        = Vettore (1D) — lista di valori│
 │    [prodotto, prezzo, qty]                                      │
 │  • Una TABELLA di ordini       = Matrice (2D) — righe x colonne│
 │  • Ordini di MOLTI clienti     = Tensor 3D — clienti x ordini  │
 │    (un "cubo" di dati)           x dettagli                    │
 │  • Un'IMMAGINE a colori        = Tensor 3D — altezza x         │
 │                                   larghezza x canali (R,G,B)   │
 │  • Un VIDEO                    = Tensor 4D — tempo x altezza   │
 │                                   x larghezza x canali         │
 └─────────────────────────────────────────────────────────────────┘

 PERCHÉ UN WEB DEVELOPER DOVREBBE AMARE I TENSOR?

 1. SONO OVUNQUE: Ogni dato che l'AI processa è un tensor.
    Foto del profilo? Tensor. Testo di una chat? Tensor.
    Cronologia acquisti? Tensor.

 2. SONO PREVEDIBILI: Hanno una "shape" (forma) fissa, come lo
    schema di un database. Se sai la shape, sai esattamente
    cosa contiene.

 3. SONO VELOCI: Le GPU (schede video) sono progettate per
    elaborare tensor velocissimamente. È il motivo per cui
    l'AI usa le GPU.

 4. SONO IL LINGUAGGIO DELL'AI: Quando dai un'immagine a un
    modello AI, stai passando un tensor. Quando il modello ti
    risponde, restituisce un tensor. Capire i tensor = capire l'AI.

============================================================================
"""

import numpy as np

# ╔═════════════════════════════════════════════════════════════════════════╗
# ║  QUIZ D'INGRESSO — Ripasso dal capitolo 07 (NumPy)                    ║
# ╚═════════════════════════════════════════════════════════════════════════╝
#
# Obiettivo: consolidare le lacune emerse nel capitolo precedente.
#
# DOMANDA 1 — Prevedi l'output:
#   import numpy as np
#   a = np.array([[10, 20, 30], [40, 50, 60]])
#   print(a.mean(axis=0))
# La tua risposta:[25 35 45]
#
# DOMANDA 2 — Vero o Falso?
# "Se un CSV ha 3 valori per riga, la struttura naturale in NumPy è 2D (n, 3),
#  non 3D."
# La tua risposta (V/F): V
#
# DOMANDA 3 — Trova l'errore:
#   import random
#   n = random.randint(1, 20)   # voglio 1..19
# Qual è il problema e come lo correggi?
# La tua risposta: random.randint(1, 19) randint include sia il primo che l'ultimo valore che introduco come parametro
#
# DOMANDA 4 — Definizione pratica:
# Differenza tra list.append(x) e list.extend(iterabile) in 1-2 righe.
# La tua risposta: .append aggiunge alla fine in valore che ho scelto come parametro, mentra .extend attacca alla fine della lista un ulterio lista di elementi
#
# DOMANDA 5 — Completa il codice:
#   import csv
#   import numpy as np
#   with open("matrice.csv", "r", encoding="utf-8") as f:
#       rows = list(csv.reader(f))
#       X = np.array(rows[1:], dtype=___)
# Perché usiamo rows[1:]? => per estromettere dall' array la prima rige del file csv che di solito è costituita dall'header
# La tua risposta: float oppure int per convertire i valori che nativamente vengono riportati come stringhe
#
# DOMANDA 6 — Vero o Falso?
# "Dopo standardizzazione z-score, media e deviazione standard per colonna
#  sono circa 0 e 1."
# La tua risposta (V/F):V
#
# Checklist:
# [x] Ho verificato axis=0/axis=1 senza andare a memoria.
# [x] So distinguere append vs extend.
# [x] So convertire da CSV (stringhe) a array numerico.
#
# 🔁 RINFORZO MIRATO — Dal CSV al Tensor senza errori di tipo
# Nel capitolo 07 la pipeline corretta è questa:
#   CSV (stringhe) -> salto header -> conversione numerica -> calcolo NumPy
# Se dimentichi la conversione, NumPy lavora con testo e la statistica si rompe.
#
# Esempio rapido:
#
#   righe = [["altezza", "peso", "eta"], ["180", "75", "30"], ["170", "68", "28"]]
#   # righe[1:] elimina l'header testuale
#   X = np.array(righe[1:], dtype=float)
#   print(X.shape)         # (2, 3)
#   print(X.mean(axis=0))  # statistiche reali su numeri
#
# Micro-check:
# 1) Se il CSV ha 100 righe dati e 3 colonne, shape = 2D
# 2) Se usi dtype=int ma nel CSV trovi "49.99", cosa succede? il valore viene arrotondato all'intero, in questo caso per eccesso e quindi 50
#
# ==========================================================================
# PARTE 1: Le Dimensioni dei Tensor — Dal Semplice al Complesso
# ==========================================================================

print("=" * 60)
print("  LE DIMENSIONI DEI TENSOR")
print("=" * 60)

# --- SCALARE (0D) — Un singolo numero ---
# Come: il prezzo di un prodotto, la temperatura, un voto
scalare = np.array(42)
print(f"\nSCALARE (0D):")
print(f"  Valore: {scalare}")
print(f"  Shape: {scalare.shape}")   # () — nessuna dimensione
print(f"  Ndim: {scalare.ndim}")     # 0

# --- VETTORE (1D) — Una lista di numeri ---
# Come: una riga di un CSV, i pixel di una riga di un'immagine
vettore = np.array([10, 20, 30, 40, 50])
print(f"\nVETTORE (1D):")
print(f"  Valore: {vettore}")
print(f"  Shape: {vettore.shape}")   # (5,) — 5 elementi in 1 dimensione
print(f"  Ndim: {vettore.ndim}")     # 1

# --- MATRICE (2D) — Una tabella di numeri ---
# Come: un foglio Excel, una tabella HTML, un'immagine in bianco e nero
matrice = np.array([
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
])
print(f"\nMATRICE (2D):")
print(f"  Valore:\n{matrice}")
print(f"  Shape: {matrice.shape}")   # (3, 3) — 3 righe, 3 colonne
print(f"  Ndim: {matrice.ndim}")     # 2

# --- TENSOR 3D — Un "cubo" di numeri ---
# Come: un'immagine a colori (altezza x larghezza x 3 canali RGB)
tensor_3d = np.array([
    [[1, 2], [3, 4], [5, 6]],
    [[7, 8], [9, 10], [11, 12]]
])
print(f"\nTENSOR 3D:")
print(f"  Valore:\n{tensor_3d}")
print(f"  Shape: {tensor_3d.shape}")   # (2, 3, 2)
print(f"  Ndim: {tensor_3d.ndim}")     # 3

# --- MINI-ESERCIZIO 1 — Prova subito! ---
# 1) Crea un tensor 0D con valore 99 e stampa shape/ndim
# 2) Crea un vettore 1D con 6 elementi e stampa shape
# 3) Crea una matrice 2x4 di zeri e stampa ndim
# 4) Scrivi nei commenti: quando passi da 2D a 3D?
tensor_0d = np.array(99)
print(f"\nTENSORE 0D => SCALARE\n")
print(f"Shape: {tensor_0d.shape}")
print(f"Ndim: {tensor_0d.ndim}")
print(f"\nTENSORE 1D => VETTORE\n")
vettore_1d = np.arange(1, 7)
print(f"Shape: {vettore_1d.shape}")
print(f"\nTENSORE 2D => MATRICE\n")
matrice = np.array([0, 0, 0, 0, 0, 0, 0, 0])
matrice_2d = matrice.reshape(2, 4)
print(f"Ndim: {matrice_2d.ndim}")
#passare a 3d significa dare un ulteriore dimensione a una matrice, quindi dividerla in più livelli, es.:
# matrice_3d = matrice_2d.reshape(2, 2, 2) => [[[0 0][0 0]][[0 0][0 0]]]




# ==========================================================================
# PARTE 2: Esempio Reale — Un'Immagine Come Tensor
# ==========================================================================

print("\n" + "=" * 60)
print("  UN'IMMAGINE È UN TENSOR!")
print("=" * 60)

# Un'immagine digitale è una griglia di pixel.
# Ogni pixel ha 3 valori: Rosso, Verde, Blu (RGB), ciascuno da 0 a 255.
#
# Un'immagine 4x4 pixel a colori è un tensor di shape (4, 4, 3):
#   4 = altezza (righe di pixel)
#   4 = larghezza (colonne di pixel)
#   3 = canali (R, G, B)

# Simuliamo una mini-immagine 4x4:
mini_immagine = np.zeros((4, 4, 3), dtype=np.uint8)  # uint8 = 0-255

# Coloriamo alcuni pixel:
mini_immagine[0, 0] = [255, 0, 0]     # Pixel in alto a sinistra: ROSSO
mini_immagine[0, 3] = [0, 0, 255]     # Pixel in alto a destra: BLU
mini_immagine[3, 0] = [0, 255, 0]     # Pixel in basso a sinistra: VERDE
mini_immagine[3, 3] = [255, 255, 0]   # Pixel in basso a destra: GIALLO
mini_immagine[1:3, 1:3] = [255, 255, 255]  # Centro: BIANCO

print(f"Shape dell'immagine: {mini_immagine.shape}")
print(f"  {mini_immagine.shape[0]} pixel di altezza")
print(f"  {mini_immagine.shape[1]} pixel di larghezza")
print(f"  {mini_immagine.shape[2]} canali colore (RGB)")
print(f"  Totale numeri: {mini_immagine.size}")

# Vediamo il canale ROSSO dell'immagine:
print(f"\nCanale Rosso:")
print(mini_immagine[:, :, 0])

# Un'immagine reale (es. foto del profilo 256x256) sarebbe:
foto_profilo = np.random.randint(0, 256, size=(256, 256, 3), dtype=np.uint8)
print(f"\nFoto profilo simulata:")
print(f"  Shape: {foto_profilo.shape}")
print(f"  Numeri totali: {foto_profilo.size:,}")  # 196,608 numeri!

# Una foto HD (1920x1080):
foto_hd_shape = (1080, 1920, 3)
totale_numeri = 1080 * 1920 * 3
print(f"\nFoto Full HD:")
print(f"  Shape: {foto_hd_shape}")
print(f"  Numeri totali: {totale_numeri:,}")  # 6,220,800 numeri!

# --- MINI-ESERCIZIO 2 — Prova subito! ---
# 1) Crea una "mini immagine" casuale di shape (5, 5, 3)
# 2) Stampa solo il canale verde (indice 1)
# 3) Stampa il pixel in posizione [2, 2]
# 4) Verifica quanti numeri totali contiene con .size
print(f"M\nini-esercizio 2\n")
test_image = np.random.randint(0, 256, size=(5, 5, 3), dtype=np.uint8)
test_image[0, 0] = [0, 255, 0]
print(f"Stampa solo il canale verde")
print(f"{test_image[:, :, 1]}\n")
print(f"Stampa solo il pixel in posizione [2, 2]:")
print(f"{test_image[2, 2]}\n")
print(f"Size dell'immagine:")
print(f"{test_image.size}\n")


# ==========================================================================
# PARTE 3: Shape — La "Carta d'Identità" del Tensor
# ==========================================================================

print("\n" + "=" * 60)
print("  SHAPE: LA CARTA D'IDENTITÀ DEL TENSOR")
print("=" * 60)

# Nella programmazione AI, la SHAPE è tutto. Se la shape non corrisponde,
# il codice crasha. È come passare un oggetto JSON con campi sbagliati
# a un endpoint API: otterrai un errore.

# Ecco le shape che incontrerai nel corso:

print("""
Shape comuni nell'AI:

(n,)            → Vettore: n numeri in fila
                  Es: (784,) = un'immagine 28x28 appiattita

(n, m)          → Matrice: n righe, m colonne
                  Es: (100, 3) = 100 campioni con 3 features (altezza, peso, età)

(n, h, w)       → Batch di immagini in bianco e nero
                  Es: (32, 28, 28) = 32 immagini, ciascuna 28x28 pixel

(n, h, w, c)    → Batch di immagini a colori
                  Es: (32, 224, 224, 3) = 32 immagini 224x224 RGB

(n, seq_len)    → Batch di testi (sequenze di numeri)
                  Es: (16, 512) = 16 frasi, ciascuna lunga 512 "token"
""")

# Esempio pratico: dataset di immagini per il training
batch_size = 32
altezza = 28
larghezza = 28
canali = 1  # Bianco e nero

batch_immagini = np.random.rand(batch_size, altezza, larghezza, canali)
print(f"Batch di immagini: shape = {batch_immagini.shape}")
print(f"  → {batch_size} immagini")
print(f"  → {altezza}x{larghezza} pixel ciascuna")
print(f"  → {canali} canale (bianco e nero)")
print(f"  → Totale numeri: {batch_immagini.ndim}")

# --- MINI-ESERCIZIO 3 — Prova subito! ---
# 1) Crea un batch RGB con shape (16, 64, 64, 3)
# 2) Stampa separatamente batch, altezza, larghezza, canali usando gli indici di shape
# 3) Calcola il totale numeri con una moltiplicazione manuale e confrontalo con .size
mio_batch = np.random.randint(0, 256, size=(16, 64, 64, 3))
print("\nMini-esercizio 3\n")
print(f"Batch => {mio_batch.shape}")
print(f"Altezza => {mio_batch.shape[1]}")
print(f"Larghezza => {mio_batch.shape[2]}")
print(f"Canali => {mio_batch.shape[3]}")
mia_size = mio_batch.shape[0]*mio_batch.shape[1]*mio_batch.shape[2]*mio_batch.shape[3]
print(f"Confronto sul totale numeri => {mia_size == mio_batch.size}")

# ==========================================================================
# PARTE 4: Operazioni sui Tensor — Broadcast
# ==========================================================================

print("\n" + "=" * 60)
print("  BROADCASTING: LA MAGIA DELLE OPERAZIONI")
print("=" * 60)

# Broadcasting è quando NumPy "espande" automaticamente un tensor
# più piccolo per adattarlo a uno più grande durante un'operazione.
#
# Analogia CSS: è come quando imposti font-size su un div padre
# e tutti i figli lo ereditano. Non devi impostarlo su ogni elemento.

# Esempio: normalizzare un'immagine (dividere tutti i pixel per 255)
immagine = np.random.randint(0, 256, size=(4, 4, 3))
print(f"Immagine (valori 0-255):\n{immagine[:2]}")  # Prime 2 righe

# Divido TUTTO per 255 (normalizzazione 0-1):
immagine_norm = immagine / 255.0
print(f"\nImmagine normalizzata (0-1):\n{np.round(immagine_norm[:2], 2)}")

# Broadcasting con un vettore:
# Sottraggo la media di ogni canale colore separatamente
medie_canali = immagine.mean(axis=(0, 1))  # Media per canale [media_R, media_G, media_B]
print(f"\nMedie per canale RGB: {np.round(medie_canali, 1)}")

# Shape: immagine (4, 4, 3) - medie_canali (3,)
# NumPy "espande" automaticamente (3,) a (4, 4, 3) per l'operazione
immagine_centrata = immagine - medie_canali
print(f"Immagine centrata (primi pixel): {np.round(immagine_centrata[0, 0], 1)}")

# --- MINI-ESERCIZIO 4 — Prova subito! ---
# 1) Crea un tensor "audio" shape (2, 5) con valori casuali
# 2) Crea un vettore offset di shape (5,)
# 3) Somma tensor + offset e verifica shape risultato
# 4) Spiega in una riga perché funziona (broadcasting)

# ==========================================================================
# PARTE 5: Perché i Tensor sono Diversi dalle Liste di Liste?
# ==========================================================================

print("\n" + "=" * 60)
print("  TENSOR vs LISTE: IL BENCHMARK")
print("=" * 60)

import time

dimensione = 1_000_000

# Lista Python:
lista = list(range(dimensione))
start = time.time()
lista_doppia = [x * 2 for x in lista]
tempo_lista = time.time() - start

# Array NumPy:
array = np.arange(dimensione)
start = time.time()
array_doppio = array * 2
tempo_numpy = time.time() - start

print(f"Raddoppiare {dimensione:,} numeri:")
print(f"  Lista Python: {tempo_lista:.4f} secondi")
print(f"  Array NumPy:  {tempo_numpy:.4f} secondi")
print(f"  NumPy è {tempo_lista/tempo_numpy:.0f}x più veloce!")

# ╔═════════════════════════════════════════════════════════════════════════╗
# ║  QUIZ DI VERIFICA — Prima degli esercizi                               ║
# ╚═════════════════════════════════════════════════════════════════════════╝
#
# DOMANDA 1 — Prevedi l'output:
#   x = np.zeros((3, 4, 2))
#   print(x.ndim, x.shape)
# La tua risposta:
#
# DOMANDA 2 — Vero o Falso?
# "Un'immagine RGB singola in NumPy ha tipicamente shape (H, W, 3)."
# La tua risposta (V/F):
#
# DOMANDA 3 — Trova l'errore:
#   batch = np.random.rand(32, 28, 28, 1)
#   print(batch.shape[4])
# Che errore produce e perché?
# La tua risposta:
#
# DOMANDA 4 — Definizione:
# Spiega in parole semplici cosa significa "shape".
# La tua risposta:
#
# DOMANDA 5 — Completa il codice:
#   img = np.random.randint(0, 256, (8, 8, 3))
#   gray = img.mean(axis=___)
#   flat = gray.reshape(___)
# Riempi i due spazi per ottenere shape (64,)
#
# DOMANDA 6 — Prevedi l'output:
#   a = np.array([[1, 2, 3], [4, 5, 6]])
#   b = np.array([10, 20, 30])
#   print(a + b)
# La tua risposta:
#
# DOMANDA 7 — 💬 Spiega con parole tue:
# Spiega a un collega web developer perché un dataset tabellare sta in 2D
# e quando invece serve un 3D o 4D.
# La tua risposta:
#

# ╔═════════════════════════════════════════════════════════════════════════╗
# ║  ESERCIZI — Ora Prova Tu!                                             ║
# ╚═════════════════════════════════════════════════════════════════════════╝

# ESERCIZIO 1 (Facile):
# Per ognuno di questi dati del mondo reale, indica la shape del tensor:
# a) La temperatura di oggi: 25°C                    → shape?
# b) Le temperature di una settimana: [20,22,25,...]  → shape?
# c) Le temperature di 4 settimane (4 righe x 7 col)  → shape?
# d) Un'immagine Instagram 1080x1080 a colori          → shape?
# e) 10 immagini Instagram                             → shape?
# Scrivi le risposte come commenti e verifica creando gli array con np.zeros()
#
# Scrivi il tuo codice qui sotto:
# ...


# ESERCIZIO 2 (Medio):
# Crea un "flag" (bandiera) italiana come tensor 3D.
# La bandiera è 6 righe x 9 colonne x 3 canali (RGB).
# - Le prime 3 colonne: Verde [0, 128, 0]
# - Le colonne centrali (3-5): Bianco [255, 255, 255]
# - Le ultime 3 colonne: Rosso [255, 0, 0]
# Stampa la shape e il primo pixel di ogni sezione per verificare.
#
# Scrivi il tuo codice qui sotto:
# ...


# ESERCIZIO 3 (Medio):
# Simula un mini-dataset per un modello AI.
# Crea un tensor di shape (50, 4) dove:
# - 50 = campioni (persone)
# - Colonna 0 = altezza (random 150-200)
# - Colonna 1 = peso (random 50-100)
# - Colonna 2 = età (random 18-65)
# - Colonna 3 = reddito annuo (random 15000-80000)
# Poi normalizza OGNI colonna (media 0, std 1).
# Stampa medie e std prima e dopo per verificare.
#
# Scrivi il tuo codice qui sotto:
# ...


# ESERCIZIO 4 (Sfida):
# Crea una funzione che simula come un'AI "vede" un'immagine:
# 1. Crea un'immagine casuale 8x8 RGB (come un emoji molto pixelato)
# 2. Convertila in bianco e nero (media dei 3 canali per ogni pixel)
# 3. "Appiattiscila" in un vettore 1D (come faresti per darla a una rete neurale)
# 4. Normalizza i valori tra 0 e 1 (dividi per 255)
# Stampa la shape ad ogni passaggio.
# Shape attese: (8,8,3) → (8,8) → (64,) → (64,)
#
# Scrivi il tuo codice qui sotto:
# ...


# ESERCIZIO 5 (Sfida — Benchmark):
# Scrivi un test di performance che confronta:
# a) Calcolare la somma di 10 milioni di numeri con una lista Python
# b) Calcolare la somma di 10 milioni di numeri con NumPy
# c) Calcolare il prodotto scalare (dot product) di due vettori di
#    1 milione di numeri (con lista vs NumPy)
#    Dot product con lista: sum(a[i]*b[i] for i in range(len(a)))
#    Dot product con NumPy: np.dot(a, b)
# Stampa i tempi e il rapporto di velocità.
#
# Scrivi il tuo codice qui sotto:
# ...


# ╔═════════════════════════════════════════════════════════════════════════╗
# ║  🏗️ PROGETTO INCREMENTALE — Catalogo E-commerce                        ║
# ╚═════════════════════════════════════════════════════════════════════════╝
#
# Nel capitolo 07 hai lavorato con una matrice 2D (campioni x feature).
# In questo capitolo fai il passo in più: rappresentare "mini immagini prodotto"
# come tensori, per preparare la strada al modulo di Computer Vision.
#
# Task (15-25 minuti):
# 1) Simula 12 "thumbnail prodotto" in scala ridotta con shape (12, 16, 16, 3)
#    usando valori casuali 0-255 (dtype=np.uint8).
# 2) Crea una versione normalizzata in [0, 1] dividendo per 255.0.
# 3) Crea una versione in bianco e nero (media sui canali RGB, axis=3),
#    mantenendo lo shape batch-first: (12, 16, 16).
# 4) Appiattisci ogni immagine in vettore 1D:
#    shape finale attesa (12, 256) usando reshape(batch_size, -1).
# 5) Stampa shape a ogni passaggio e verifica che il numero di campioni
#    resti 12 in tutte le trasformazioni.
#
# Obiettivo mentale:
# - 2D per dati tabellari (come nel 07)
# - 4D per batch immagini (n, h, w, c)
# - reshape/mean come ponte verso i modelli AI
#
# Scrivi il tuo codice qui sotto:
# ...
#

# ╔═════════════════════════════════════════════════════════════════════════╗
# ║  SOLUZIONI — Guardale Solo DOPO Aver Provato!                         ║
# ╚═════════════════════════════════════════════════════════════════════════╝

# --- RISPOSTE QUIZ D'INGRESSO ---
# 1) [25. 35. 45.] perché axis=0 calcola la media per colonna
# 2) Vero
# 3) randint(1, 20) include anche 20; per 1..19 usa randint(1, 19) oppure randrange(1, 20)
# 4) append aggiunge un solo elemento; extend aggiunge tutti gli elementi dell'iterabile
# 5) dtype=float (o int se i dati sono interi); rows[1:] serve a saltare l'header testuale
# 6) Vero (circa 0 e 1, salvo arrotondamenti)
#
# --- RISPOSTE QUIZ DI VERIFICA ---
# 1) 3 (3, 4, 2)
# 2) Vero
# 3) IndexError: tuple index out of range, perché shape ha indici 0..3
# 4) La shape è la "carta d'identità" del tensor: dice quante dimensioni ha e quanti elementi per ogni dimensione
# 5) axis=2 e reshape(-1)
# 6) [[11 22 33]
#     [14 25 36]]
# 7) 2D = righe/colonne (tabella); 3D/4D servono quando c'è una dimensione extra reale (canali colore, tempo, batch)

# --- SOLUZIONE ESERCIZIO 1 ---
# # a) Scalare → shape ()
# a = np.array(25)
# print(f"a) Temperatura: shape {a.shape}")
# # b) Vettore → shape (7,)
# b = np.zeros(7)
# print(f"b) Settimana: shape {b.shape}")
# # c) Matrice → shape (4, 7)
# c = np.zeros((4, 7))
# print(f"c) 4 settimane: shape {c.shape}")
# # d) Immagine → shape (1080, 1080, 3)
# d = np.zeros((1080, 1080, 3))
# print(f"d) Instagram: shape {d.shape}")
# # e) Batch → shape (10, 1080, 1080, 3)
# e = np.zeros((10, 1080, 1080, 3))
# print(f"e) 10 Instagram: shape {e.shape}")

# --- SOLUZIONE ESERCIZIO 2 ---
# bandiera = np.zeros((6, 9, 3), dtype=np.uint8)
# bandiera[:, :3] = [0, 128, 0]       # Verde
# bandiera[:, 3:6] = [255, 255, 255]  # Bianco
# bandiera[:, 6:] = [255, 0, 0]       # Rosso
# print(f"Bandiera shape: {bandiera.shape}")
# print(f"Pixel verde: {bandiera[0, 0]}")
# print(f"Pixel bianco: {bandiera[0, 4]}")
# print(f"Pixel rosso: {bandiera[0, 7]}")

# --- SOLUZIONE ESERCIZIO 3 ---
# np.random.seed(42)
# dataset = np.column_stack([
#     np.random.randint(150, 201, 50),  # altezza
#     np.random.randint(50, 101, 50),   # peso
#     np.random.randint(18, 66, 50),    # età
#     np.random.randint(15000, 80001, 50)  # reddito
# ]).astype(float)
# print(f"Shape: {dataset.shape}")
# print(f"Medie PRIMA: {dataset.mean(axis=0).round(1)}")
# print(f"Std PRIMA:   {dataset.std(axis=0).round(1)}")
# norm = (dataset - dataset.mean(axis=0)) / dataset.std(axis=0)
# print(f"Medie DOPO:  {norm.mean(axis=0).round(4)}")
# print(f"Std DOPO:    {norm.std(axis=0).round(4)}")

# --- SOLUZIONE ESERCIZIO 4 ---
# immagine_rgb = np.random.randint(0, 256, (8, 8, 3), dtype=np.uint8)
# print(f"1. RGB:     shape {immagine_rgb.shape}")
# grigio = immagine_rgb.mean(axis=2)
# print(f"2. B/N:     shape {grigio.shape}")
# vettore = grigio.flatten()
# print(f"3. Flatten: shape {vettore.shape}")
# normalizzato = vettore / 255.0
# print(f"4. Norm:    shape {normalizzato.shape}, min={normalizzato.min():.2f}, max={normalizzato.max():.2f}")

# --- SOLUZIONE ESERCIZIO 5 ---
# n = 10_000_000
# lista_a = list(range(n))
# array_a = np.arange(n)
#
# start = time.time()
# sum(lista_a)
# t_lista_sum = time.time() - start
#
# start = time.time()
# np.sum(array_a)
# t_numpy_sum = time.time() - start
#
# print(f"Somma 10M numeri: Lista={t_lista_sum:.3f}s, NumPy={t_numpy_sum:.4f}s, ratio={t_lista_sum/t_numpy_sum:.0f}x")
#
# n2 = 1_000_000
# la = list(range(n2))
# lb = list(range(n2))
# na = np.arange(n2)
# nb = np.arange(n2)
#
# start = time.time()
# sum(a*b for a,b in zip(la,lb))
# t_lista_dot = time.time() - start
#
# start = time.time()
# np.dot(na, nb)
# t_numpy_dot = time.time() - start
#
# print(f"Dot product 1M: Lista={t_lista_dot:.3f}s, NumPy={t_numpy_dot:.5f}s, ratio={t_lista_dot/t_numpy_dot:.0f}x")
