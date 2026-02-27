"""
============================================================================
 MODULO 1 — ESERCIZIO 07: Introduzione a NumPy
 Il Mattone Fondamentale dell'Intelligenza Artificiale
============================================================================

 TEORIA: Cos'è NumPy e Perché è il "jQuery dell'AI"?

 NumPy (Numerical Python) è LA libreria per fare calcoli matematici veloci
 in Python. Se JavaScript ha jQuery per semplificare il DOM, Python ha
 NumPy per semplificare i calcoli con numeri.

 PERCHÉ SERVE PER L'AI?
 Tutta l'Intelligenza Artificiale si basa su operazioni matematiche
 su grandi quantità di numeri. Un'immagine è una griglia di numeri.
 Un testo è una sequenza di numeri. Un modello AI è un insieme di numeri
 (chiamati "pesi") che vengono moltiplicati e sommati continuamente.

 La lista Python normale è troppo LENTA per questo:
   - Una lista Python di 1 milione di numeri: operazioni in ~0.5 secondi
   - Un array NumPy di 1 milione di numeri: operazioni in ~0.005 secondi
   → NumPy è circa 100 volte più veloce!

 Perché? Perché NumPy è scritto in C/C++ sotto il cofano. Tu scrivi
 Python (comodo), ma i calcoli vengono fatti in C (veloce).
 È come usare Eloquent (comodo) mentre sotto il cofano gira SQL ottimizzato.

 NIENTE DI SIMILE ESISTE IN PHP O JAVASCRIPT:
 PHP e JavaScript non hanno un equivalente di NumPy. In PHP faresti:
   $numeri = [1, 2, 3, 4, 5];
   $doppi = array_map(fn($n) => $n * 2, $numeri);  // serve array_map + funzione
   // array_map() applica la funzione a ogni elemento e crea un nuovo array.

 In JavaScript:
   const numeri = [1, 2, 3, 4, 5];
   const doppi = numeri.map(n => n * 2);  // serve .map() + funzione
   // .map() crea un nuovo array applicando la funzione ad ogni elemento.

 In NumPy, lo fai DIRETTAMENTE sull'array, SENZA funzioni wrapper:
   numeri = np.array([1, 2, 3, 4, 5])
   doppi = numeri * 2    # Basta moltiplicare! Niente map, niente loop.

 Questo si chiama "operazione vettorizzata" ed è il segreto della velocità.
 Immagina di avere 1 milione di numeri: in PHP/JS faresti 1 milione di
 giri di loop. NumPy li processa tutti in un colpo solo, in C.

============================================================================
"""

import numpy as np  # 'np' è la convenzione universale, come '$' per jQuery

# ╔═════════════════════════════════════════════════════════════════════════╗
# ║  QUIZ D'INGRESSO — Rispondi PRIMA di leggere la teoria NumPy          ║
# ╚═════════════════════════════════════════════════════════════════════════╝
#
# Obiettivo: verificare i prerequisiti dal capitolo 06 prima del passaggio
# a NumPy (soprattutto parsing operativo e output concreto).
#
# DOMANDA 1 — Output concreto:
# Cosa stampa: print("ciao mondo".split(" "))
# La tua risposta: ["ciao", "mondo"]
#
# DOMANDA 2 — Vero o Falso?
# "csv.DictReader restituisce numeri già convertiti in int/float"
# La tua risposta (V/F): F
#
# DOMANDA 3 — Pipeline operativa (lacuna #11):
# Descrivi IN ORDINE i passi del parsing manuale CSV, da file testo a
# lista di dizionari. Niente teoria astratta: solo passaggi operativi.
# La tua risposta:
import os
print(f"\nQuiz - 1\n")
percorso_file = os.path.join(os.path.join(os.path.dirname(__file__), "dati"), "catalogo.csv")
with open(percorso_file, "r", encoding="utf-8") as file:
  lettore = file.readlines()
  header = lettore[0].strip().split(',')
  dictionary_list = []
  for row in lettore[1:]:
    if row.strip():
      values = row.strip().split(",")
      dictionary = {}
      for i, v in enumerate(values, 0):
        dictionary[header[i]] = v
      dictionary_list.append(dictionary)
  print(f"{dictionary_list}")
        
        
#
# DOMANDA 4 — Differenza pratica:
# In 1 riga: quando preferisci csv.DictReader rispetto al parsing manuale?
# La tua risposta: quando non mi occorre particolare controllo sul parsing
#
# DOMANDA 5 — Tipi:
# Se record["prezzo"] vale "49.99", quale conversione usi per fare calcoli?
# La tua risposta: float(record["prezzo"])
#
# Checklist:
# [x] Ho risposto con output concreti dove richiesto.
# [x] Ho descritto la pipeline con passi ordinati.
# [x] Ho distinto chiaramente manuale vs DictReader.
#

# 🔁 RINFORZO MIRATO — Dal CSV a NumPy: stessa logica, struttura diversa
# Nel capitolo 06 hai consolidato il flusso "testo -> struttura dati".
# Qui la logica è analoga:
#   CSV (stringhe) -> lista/dizionari (struttura) -> array NumPy (calcolo veloce)
#
# Ponte mentale operativo:
# 1) Prima estrai dati puliti (e converti i tipi)
# 2) Poi li trasformi in array NumPy
# 3) Infine applichi operazioni vettorizzate/statistiche
#
# Errore da evitare:
# - saltare il controllo tipi e aspettarsi che tutto sia già numerico.
#   Anche in NumPy, se parti da stringhe sporche, i calcoli non sono affidabili.

# ==========================================================================
# PARTE 1: Creare Array NumPy
# ==========================================================================

# Un array NumPy è come una lista Python, ma ottimizzata per i numeri.

# Da una lista Python:
lista_python = [1, 2, 3, 4, 5]
array_numpy = np.array([1, 2, 3, 4, 5])

print("=== Creare Array ===")
print(f"Lista Python:  {lista_python}  (tipo: {type(lista_python).__name__})")
print(f"Array NumPy:   {array_numpy}  (tipo: {type(array_numpy).__name__})")

# DIFFERENZA VISIVA: nota le virgole!
# Lista Python:  [1, 2, 3, 4, 5]   ← CON virgole
# Array NumPy:   [1 2 3 4 5]        ← SENZA virgole

# Creare array con funzioni speciali:
zeri = np.zeros(5)               # [0. 0. 0. 0. 0.] — array di zeri
uni = np.ones(5)                 # [1. 1. 1. 1. 1.] — array di uni
sequenza = np.arange(0, 10, 2)  # [0 2 4 6 8] — come range() ma per array
lineare = np.linspace(0, 1, 5)  # [0. 0.25 0.5 0.75 1.] — 5 punti da 0 a 1
casuali = np.random.rand(5)     # 5 numeri casuali tra 0 e 1

print(f"\nZeri:     {zeri}")
print(f"Uni:      {uni}")
print(f"Sequenza: {sequenza}")
print(f"Lineare:  {lineare}")
print(f"Casuali:  {casuali}")

# Proprietà di un array:
print(f"\n=== Proprietà ===")
print(f"Forma (shape): {array_numpy.shape}")      # (5,) — 5 elementi, 1 dimensione
print(f"Tipo dati (dtype): {array_numpy.dtype}")   # int64 — numeri interi a 64 bit
print(f"Num. dimensioni: {array_numpy.ndim}")      # 1 — monodimensionale
print(f"Num. elementi: {array_numpy.size}")        # 5

# ==========================================================================
# PARTE 2: Operazioni Vettorizzate — Il Superpotere
# ==========================================================================

# Ecco la magia: operazioni su TUTTO l'array senza loop.

a = np.array([10, 20, 30, 40, 50])

print(f"\n=== Operazioni Vettorizzate ===")
print(f"Array:        {a}")
print(f"a + 5:        {a + 5}")          # Somma 5 a ogni elemento
print(f"a * 2:        {a * 2}")          # Moltiplica ogni elemento per 2
print(f"a / 10:       {a / 10}")         # Divide ogni elemento per 10
print(f"a ** 2:       {a ** 2}")         # Eleva al quadrato ogni elemento

# In JavaScript questo richiederebbe:
#   a.map(x => x + 5)
#   a.map(x => x * 2)
# In NumPy è diretto, senza .map(), e 100x più veloce.

# Operazioni tra due array (elemento per elemento):
b = np.array([1, 2, 3, 4, 5])
print(f"\na: {a}")
print(f"b: {b}")
print(f"a + b: {a + b}")       # [11 22 33 44 55]
print(f"a * b: {a * b}")       # [10 40 90 160 250]
print(f"a / b: {a / b}")       # [10. 10. 10. 10. 10.]

# Confronti (restituiscono array di True/False):
print(f"\na > 25: {a > 25}")   # [False False  True  True  True]

# ==========================================================================
# PARTE 3: Funzioni Statistiche
# ==========================================================================

voti = np.array([75, 92, 88, 65, 95, 70, 85, 60, 98, 72])

print(f"\n=== Funzioni Statistiche ===")
print(f"Voti: {voti}")
print(f"Media:     {np.mean(voti):.1f}")      # oppure voti.mean()
print(f"Mediana:   {np.median(voti):.1f}")
print(f"Dev. Std:  {np.std(voti):.1f}")        # Quanto i voti "si spargono"
print(f"Minimo:    {np.min(voti)}")
print(f"Massimo:   {np.max(voti)}")
print(f"Somma:     {np.sum(voti)}")

# DEVIAZIONE STANDARD — Spiegata semplice:
# È una misura di quanto i valori sono "sparpagliati" rispetto alla media.
# - Dev. Std. bassa = i voti sono tutti vicini alla media (classe omogenea)
# - Dev. Std. alta = i voti sono molto diversi tra loro (classe eterogenea)
# Esempio:
# Classe A: [70, 72, 68, 71, 69] → media 70, std ≈ 1.4 (tutti simili)
# Classe B: [50, 90, 60, 95, 55] → media 70, std ≈ 18.7 (molto diversi)

classe_a = np.array([70, 72, 68, 71, 69])
classe_b = np.array([50, 90, 60, 95, 55])
print(f"\nClasse A: media={classe_a.mean():.0f}, std={classe_a.std():.1f} (omogenea)")
print(f"Classe B: media={classe_b.mean():.0f}, std={classe_b.std():.1f} (eterogenea)")

# ==========================================================================
# PARTE 4: Indicizzazione e Slicing (come le liste, ma più potente)
# ==========================================================================

arr = np.array([10, 20, 30, 40, 50, 60, 70, 80, 90, 100])

print(f"\n=== Indicizzazione ===")
print(f"Array:     {arr}")
print(f"arr[0]:    {arr[0]}")          # 10
print(f"arr[-1]:   {arr[-1]}")         # 100
print(f"arr[2:5]:  {arr[2:5]}")        # [30 40 50]
print(f"arr[::2]:  {arr[::2]}")        # [10 30 50 70 90]

# NOVITÀ RISPETTO ALLE LISTE: Indicizzazione con array booleano!
# Puoi usare una condizione per selezionare elementi.
# È come un WHERE in SQL.

print(f"\n=== Filtro con condizione (come SQL WHERE) ===")
print(f"arr > 50:          {arr > 50}")             # [False...True True True...]
print(f"arr[arr > 50]:     {arr[arr > 50]}")         # [60 70 80 90 100]
print(f"arr[arr % 30 == 0]: {arr[arr % 30 == 0]}")   # [30 60 90]

# Esempio pratico: filtrare voti
print(f"\nVoti: {voti}")
promossi = voti[voti >= 70]
bocciati = voti[voti < 70]
print(f"Promossi (>=70): {promossi}")
print(f"Bocciati (<70):  {bocciati}")

# ==========================================================================
# PARTE 5: Array 2D — Le Matrici
# ==========================================================================

# Un array 2D è come una tabella (righe e colonne).
# Pensa a un foglio Excel o a una tabella HTML.

# Creare un array 2D:
matrice = np.array([
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
])

print(f"\n=== Array 2D (Matrice) ===")
print(f"Matrice:\n{matrice}")
print(f"Forma: {matrice.shape}")       # (3, 3) — 3 righe, 3 colonne
print(f"Dimensioni: {matrice.ndim}")   # 2

# Accedere agli elementi:
print(f"\nElemento [0,0]: {matrice[0, 0]}")   # 1 (prima riga, prima colonna)
print(f"Elemento [1,2]: {matrice[1, 2]}")     # 6 (seconda riga, terza colonna)
print(f"Riga 0: {matrice[0]}")                # [1 2 3]
print(f"Colonna 1: {matrice[:, 1]}")          # [2 5 8] — tutte le righe, colonna 1

# Operazioni su assi:
# axis=0 → opera sulle COLONNE (dall'alto in basso)
# axis=1 → opera sulle RIGHE (da sinistra a destra)

tabella_voti = np.array([
    [85, 90, 78],   # Marco: Matematica, Italiano, Inglese
    [92, 88, 95],   # Laura
    [70, 75, 80],   # Giulia
])
nomi = ["Marco", "Laura", "Giulia"]
materie = ["Mat", "Ita", "Ing"]

print(f"\n=== Operazioni sugli assi ===")
print(f"Voti:\n{tabella_voti}")
print(f"Media per studente (axis=1): {tabella_voti.mean(axis=1)}")   # Media di ogni riga
print(f"Media per materia (axis=0):  {tabella_voti.mean(axis=0)}")   # Media di ogni colonna

for i, nome in enumerate(nomi):
    print(f"  {nome}: media {tabella_voti[i].mean():.1f}")

# ==========================================================================
# PARTE 6: Reshape — Cambiare la Forma dell'Array
# ==========================================================================

# Reshape è FONDAMENTALE in AI. Spesso devi "rimodellare" i dati
# per darli a un modello. È come fare un CSS display:grid e cambiare
# il layout degli elementi senza cambiare il contenuto.

arr_1d = np.arange(12)  # [0 1 2 3 4 5 6 7 8 9 10 11]
print(f"\n=== Reshape ===")
print(f"1D: {arr_1d}  (shape: {arr_1d.shape})")

# Trasformo in matrice 3x4:
arr_3x4 = arr_1d.reshape(3, 4)
print(f"3x4:\n{arr_3x4}  (shape: {arr_3x4.shape})")

# Trasformo in matrice 4x3:
arr_4x3 = arr_1d.reshape(4, 3)
print(f"4x3:\n{arr_4x3}  (shape: {arr_4x3.shape})")

# Trasformo in 3D (2 "strati" di 2x3):
arr_3d = arr_1d.reshape(2, 2, 3)
print(f"2x2x3:\n{arr_3d}  (shape: {arr_3d.shape})")

# Il -1 significa "calcola tu questa dimensione":
arr_auto = arr_1d.reshape(3, -1)  # Python calcola: 12/3 = 4 colonne
print(f"reshape(3, -1):\n{arr_auto}  (shape: {arr_auto.shape})")

# PREVIEW AI: Un'immagine 28x28 pixel in scala di grigio ha shape (28, 28).
# Per darla a una rete neurale, spesso devi fare reshape in (784,) — un vettore.
# 28 * 28 = 784. Questo "appiattimento" si chiama "flatten".
immagine_simulata = np.random.randint(0, 256, size=(28, 28))
vettore = immagine_simulata.reshape(-1)  # Equivalente di .flatten()
print(f"\nImmagine 28x28 → vettore: {immagine_simulata.shape} → {vettore.shape}")


# ╔═════════════════════════════════════════════════════════════════════════╗
# ║  ESERCIZI — Ora Prova Tu!                                             ║
# ╚═════════════════════════════════════════════════════════════════════════╝

# ESERCIZIO 1 (Facile) — Fondamentali array 1D
# Obiettivo: verificare creazione array, statistiche base e filtro booleano.
# Input: nessuno (crei tu l'array con np.arange).
# Output atteso:
# a) array 1..20
# b) media, mediana, deviazione standard
# c) solo numeri divisibili per 3
# d) array moltiplicato per 10
# Vincoli: usa NumPy puro (no loop per c e d).
# Checklist:
# [ ] Ho usato array NumPy e non lista Python.
# [ ] Ho usato filtro booleano per i divisibili.
# [ ] Ho stampato i 4 output richiesti.
#
# Scrivi il tuo codice qui sotto:
# ...


# ESERCIZIO 2 (Medio) — Matrici e assi
# Obiettivo: padroneggiare axis=0/1 e metriche su array 2D.
# Input:
# - array 2D 5x4 con numeri casuali tra 50 e 100:
# Simula i voti di 5 studenti in 4 materie (crea un array 2D 5x4
# con numeri casuali tra 50 e 100):
#   voti = np.random.randint(50, 101, size=(5, 4))
# Output atteso:
# a) Calcola la media di ogni studente (axis=1)
# b) Calcola la media di ogni materia (axis=0)
# c) Trova lo studente con la media più alta (suggerimento: .argmax())
# d) Conta quanti voti sono insufficienti (<60) in totale
# Vincoli: niente loop per media/count insufficienze.
# Checklist:
# [ ] Ho usato axis correttamente.
# [ ] Ho usato argmax per il migliore.
# [ ] Ho contato insufficienze con condizione vettorizzata.
#
# Scrivi il tuo codice qui sotto:
# ...


# ESERCIZIO 3 (Medio — Operazioni Vettorizzate):
# Obiettivo: usare algebra vettoriale senza loop.
# Hai i prezzi di 8 prodotti in euro:
#   prezzi_eur = np.array([10.00, 25.50, 99.99, 149.00, 5.99, 45.00, 200.00, 35.50])
# Output atteso:
# a) Converti in dollari (tasso 1.08) SENZA usare un loop
# b) Applica uno sconto del 15% a tutti i prezzi SENZA loop
# c) Trova tutti i prodotti che costano tra 20€ e 100€ (usa & per "and")
# d) Calcola il ricavo totale se vendi 1 di ogni prodotto, con IVA 22%
# Checklist:
# [ ] Nessun for/while usato.
# [ ] Ho usato operatori vettorizzati.
# [ ] Ho usato maschera booleana con &.
#
# Scrivi il tuo codice qui sotto:
# ...


# ESERCIZIO 4 (Sfida — Reshape):
# Obiettivo: capire le trasformazioni di shape senza perdere dati.
# a) Crea un array 1D con 24 numeri (da 1 a 24)
# b) Fai reshape in una matrice 4x6
# c) Fai reshape in un array 3D di forma (2, 3, 4) — pensa a 2 "pagine"
#    di 3 righe e 4 colonne ciascuna
# d) Da (2,3,4) torna a 1D con .flatten()
# e) Stampa la shape ad ogni passaggio
# Vincoli: nessun dato deve andare perso; controlla sempre .shape.
# Checklist:
# [ ] Shape stampata a ogni step.
# [ ] Stesso numero totale elementi in ogni forma.
# [ ] Flatten finale corretto.
#
# Scrivi il tuo codice qui sotto:
# ...


# ESERCIZIO 5 (Sfida — Preview AI):
# Obiettivo: simulare una pipeline minima di preprocessing per ML.
# Simula un mini-dataset di un modello AI.
# Crea una matrice di 100 "campioni" con 3 "features" ciascuno:
#   - Feature 1: altezza (casuale tra 150 e 200)
#   - Feature 2: peso (casuale tra 50 e 100)
#   - Feature 3: età (casuale tra 18 e 65)
#
# Poi "normalizza" ogni feature: trasformala in modo che abbia
# media 0 e deviazione standard 1. La formula è:
#   feature_normalizzata = (feature - media) / deviazione_standard
#
# Questo si chiama "standardizzazione" ed è un passo FONDAMENTALE
# prima di dare i dati a un modello AI. Fallo SENZA loop!
# Output atteso:
# - shape dataset
# - medie/std prima della normalizzazione
# - medie/std dopo la normalizzazione (circa 0 e 1)
# Checklist:
# [ ] Dataset creato con shape (100, 3).
# [ ] Normalizzazione fatta senza loop.
# [ ] Medie ~0 e std ~1 dopo il transform.
#
# Scrivi il tuo codice qui sotto:
# ...


# ╔═════════════════════════════════════════════════════════════════════════╗
# ║  SOLUZIONI — Guardale Solo DOPO Aver Provato!                         ║
# ╚═════════════════════════════════════════════════════════════════════════╝

# --- SOLUZIONE ESERCIZIO 1 ---
# a = np.arange(1, 21)
# print(f"Array: {a}")
# print(f"Media: {a.mean():.1f}")
# print(f"Mediana: {np.median(a):.1f}")
# print(f"Std: {a.std():.1f}")
# print(f"Divisibili per 3: {a[a % 3 == 0]}")
# print(f"Moltiplicati per 10: {a * 10}")

# --- SOLUZIONE ESERCIZIO 2 ---
# voti = np.random.randint(50, 101, size=(5, 4))
# nomi = ["Studente 1", "Studente 2", "Studente 3", "Studente 4", "Studente 5"]
# materie = ["Mat", "Ita", "Ing", "Sci"]
# print(f"Voti:\n{voti}")
# medie_studenti = voti.mean(axis=1)
# medie_materie = voti.mean(axis=0)
# print(f"\nMedia studenti: {medie_studenti}")
# print(f"Media materie: {medie_materie}")
# migliore = medie_studenti.argmax()
# print(f"Studente migliore: {nomi[migliore]} (media: {medie_studenti[migliore]:.1f})")
# insufficienti = (voti < 60).sum()
# print(f"Voti insufficienti totali: {insufficienti}")

# --- SOLUZIONE ESERCIZIO 3 ---
# prezzi_eur = np.array([10.00, 25.50, 99.99, 149.00, 5.99, 45.00, 200.00, 35.50])
# prezzi_usd = prezzi_eur * 1.08
# print(f"USD: {np.round(prezzi_usd, 2)}")
# prezzi_scontati = prezzi_eur * 0.85
# print(f"Scontati 15%: {np.round(prezzi_scontati, 2)}")
# fascia_media = prezzi_eur[(prezzi_eur >= 20) & (prezzi_eur <= 100)]
# print(f"Tra 20€ e 100€: {fascia_media}")
# ricavo_con_iva = np.sum(prezzi_eur) * 1.22
# print(f"Ricavo totale con IVA: {ricavo_con_iva:.2f}€")

# --- SOLUZIONE ESERCIZIO 4 ---
# arr = np.arange(1, 25)
# print(f"1D: shape {arr.shape}")
# m4x6 = arr.reshape(4, 6)
# print(f"4x6: shape {m4x6.shape}\n{m4x6}")
# m3d = arr.reshape(2, 3, 4)
# print(f"2x3x4: shape {m3d.shape}\n{m3d}")
# flat = m3d.flatten()
# print(f"Flatten: shape {flat.shape}\n{flat}")

# --- SOLUZIONE ESERCIZIO 5 ---
# np.random.seed(42)
# altezza = np.random.randint(150, 201, size=100).astype(float)
# peso = np.random.randint(50, 101, size=100).astype(float)
# eta = np.random.randint(18, 66, size=100).astype(float)
# dataset = np.column_stack([altezza, peso, eta])
# print(f"Dataset shape: {dataset.shape}")
# print(f"Prime 3 righe:\n{dataset[:3]}")
# print(f"\nPrima della normalizzazione:")
# print(f"  Medie: {dataset.mean(axis=0)}")
# print(f"  Std:   {dataset.std(axis=0)}")
# dataset_norm = (dataset - dataset.mean(axis=0)) / dataset.std(axis=0)
# print(f"\nDopo la normalizzazione:")
# print(f"  Medie: {np.round(dataset_norm.mean(axis=0), 2)}")
# print(f"  Std:   {np.round(dataset_norm.std(axis=0), 2)}")
# print(f"  Prime 3 righe:\n{np.round(dataset_norm[:3], 2)}")
