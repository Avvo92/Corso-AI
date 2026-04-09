# MODULO 1 — Python & Dati: Il "Mindset" dei Dati

## Benvenuto!

Questo è il modulo più importante di tutto il corso. Non perché sia il più "spettacolare"
(quello arriva col Deep Learning), ma perché **tutto quello che farai dopo dipende da quanto
bene capisci questi concetti**.

Pensa a questo modulo come alle fondamenta di una casa: nessuno le vede, ma se le fai male
crolla tutto.

---

## Cosa Imparerai

| # | File | Concetto | Tempo stimato |
|---|------|----------|---------------|
| 01 | `01_benvenuto_python.py` | Variabili, tipi, print, f-string | 30-45 min |
| 02 | `02_condizioni_e_cicli.py` | if/else, for, while | 30-45 min |
| 03 | `03_funzioni.py` | Funzioni, parametri, return multipli | 45-60 min |
| 04 | `04_liste.py` | Liste, slicing, list comprehension | 45-60 min |
| 05 | `05_dizionari.py` | Dizionari, iterazione, nesting | 45-60 min |
| 06 | `06_file_csv.py` | Leggere file CSV "a mano" | 30-45 min |
| 07 | `07_numpy_intro.py` | Array NumPy — il mattone dell'AI | 60-90 min |
| 08 | `08_tensori_spiegati.py` | Cos'è un Tensor e perché ti serve | 60-90 min |
| 09 | `09_pandas_intro.py` | DataFrame — SQL in RAM | 60-90 min |
| 10 | `10_pandas_progetto.py` | Mini-progetto: analisi dati reale | 90-120 min |
| 11 | `11_matplotlib_grafici.py` | Grafici e visualizzazione dati | 45-60 min |
| 12 | `12_web_bridge.py` | FastAPI: il tuo primo endpoint AI | 60-90 min |

**Tempo totale stimato: 2-3 settimane (a 1-2 ore al giorno)**

---

## Diario sessione per capitolo

Per ogni capitolo puoi tenere un file Markdown in `sessioni_capitoli/` (naming e istruzioni in `sessioni_capitoli/README.md`). Il mentor vi annota domande e valutazioni mentre studi; il file viene letto in **chiusura capitolo** per personalizzare il passo successivo. Vedi **Regola 39** e sezione **J** in `CONTESTO_CORSO.md`.

---

## Come Usare Ogni File

Ogni file `.py` è strutturato così:

```
╔═══════════════════════════════════════╗
║  1. TEORIA (commenti in cima)         ║  ← Leggi prima questo
║     Analogia + spiegazione            ║
╠═══════════════════════════════════════╣
║  2. ESEMPIO COMMENTATO                ║  ← Leggi il codice, eseguilo
║     Codice funzionante con commenti   ║
╠═══════════════════════════════════════╣
║  3. ESERCIZI                          ║  ← Ora prova tu!
║     Istruzioni chiare su cosa fare    ║
╠═══════════════════════════════════════╣
║  4. SOLUZIONI                         ║  ← Guardale SOLO dopo aver provato
║     Commentate in fondo al file       ║
╚═══════════════════════════════════════╝
```

### Regole d'Oro:

1. **Esegui SEMPRE il codice**, non limitarti a leggerlo
2. **Modifica gli esempi** — cambia un numero, aggiungi una riga, rompi il codice e vedi che errore dà
3. **Prova gli esercizi PRIMA di guardare le soluzioni**
4. **Scrivi i tuoi commenti** — se capisci qualcosa, scrivilo con parole tue sopra il codice

---

## Setup Iniziale

> Per il setup completo e la navigazione dell'intero corso, leggi il **[README principale](../README.md)** nella root.

```bash
# 1. Entra nella cartella del corso
cd "C:\Users\gianl\Desktop\Corso-AI"

# 2. Crea un ambiente virtuale (è come un node_modules per Python)
python -m venv venv

# 3. Attiva l'ambiente virtuale
venv\Scripts\activate

# 4. Installa le librerie
pip install -r requirements.txt
```

Se vedi `(venv)` all'inizio della riga del terminale, sei dentro l'ambiente virtuale.
Ogni volta che apri un nuovo terminale, ricordati di attivarlo con `venv\Scripts\activate`.

---

## Come Eseguire gli Esercizi

```bash
# Assicurati di essere nella cartella del corso con venv attivo
cd "C:\Users\gianl\Desktop\Corso-AI"
venv\Scripts\activate

# Esegui un file
python modulo_01_python_dati/01_benvenuto_python.py
```

Oppure, direttamente da Cursor: apri il file e premi `Ctrl+Shift+ò` per aprire il
terminale integrato, poi esegui `python nome_file.py`.

---

## Prossimo Modulo

Quando avrai completato tutti i 12 esercizi e ti sentirai a tuo agio con Python, Pandas
e NumPy, sarà il momento del **Modulo 2: Machine Learning con Scikit-Learn** — dove
darai la tua prima "intelligenza" ai dati.
