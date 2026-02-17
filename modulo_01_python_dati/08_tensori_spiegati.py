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
print(f"  → Totale numeri: {batch_immagini.size:,}")

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
# ║  SOLUZIONI — Guardale Solo DOPO Aver Provato!                         ║
# ╚═════════════════════════════════════════════════════════════════════════╝

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
