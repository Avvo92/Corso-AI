# Corso AI — Manuale di Navigazione

> Da Web Developer a Full-Stack AI Engineer in ~6 mesi.
> Questo file e' la tua bussola. Torna qui ogni volta che non sai cosa fare.

---

## Come Funziona il Corso — In 30 Secondi

```
TU (Web Dev)                                         TU (AI Engineer)
    |                                                      |
    |   10 moduli + 1 ponte matematico                     |
    |   ~12 capitoli per modulo                            |
    |   1 progetto che cresce per tutto il corso           |
    |   8 demo deployate nel portfolio                     |
    |   7 mock interview superati                          |
    |                                                      |
    v                                                      v
  Mese 1          Mese 2-3         Mese 4-5          Mese 6
  Python &        ML + DL +        LLM + RAG +       Progetto
  Dati            NLP              Agents             Finale
```

---

## Passo 1 — Setup Iniziale (fallo una volta sola)

```bash
# 1. Apri il terminale in Cursor (Ctrl+Shift+ò)

# 2. Vai nella cartella del corso
cd "C:\Users\gianl\Desktop\Corso-AI"

# 3. Crea l'ambiente virtuale (come node_modules per Python)
python -m venv venv

# 4. Attivalo
venv\Scripts\activate

# 5. Installa le dipendenze del Modulo 1
pip install -r requirements.txt
```

**Ogni volta che apri un nuovo terminale**, attiva il venv:
```bash
venv\Scripts\activate
```
Se vedi `(venv)` all'inizio della riga, sei dentro.

---

## Passo 2 — Come Studiare un Capitolo

Ogni capitolo segue la stessa struttura. Ecco cosa fare, nell'ordine:

### A. Quiz d'Ingresso (5 min)
- Apri il file `.py` del capitolo
- Rispondi alle domande del **quiz d'ingresso** (in cima, dopo il docstring)
- Sono domande sul capitolo PRECEDENTE — servono a verificare cosa ricordi
- Scrivi le risposte sotto ogni domanda, poi confrontale con le soluzioni in fondo

### B. Teoria + Mini-Esercizi (20-40 min)
- Leggi ogni sezione di teoria, nell'ordine
- Dopo ogni sezione c'e' un **mini-esercizio** — fallo SUBITO, prima di proseguire
- Se trovi un blocco `RINFORZO MIRATO`, fermati e fallo: e' un esercizio su un tuo errore passato

### C. Quiz di Verifica (5 min)
- Dopo tutta la teoria, rispondi al **quiz di verifica**
- Include una domanda "Spiega con parole tue" — rispondi come se lo stessi spiegando a un collega

### D. Esercizi (30-60 min)
- Parti dagli esercizi Livello 1 e sali
- Presta attenzione ai tag:
  - `[COLLOQUIO]` — questo te lo chiedono ai colloqui, ripassalo
  - `[REFACTORING]` — codice brutto da migliorare
  - `[INTERLEAVING]` — mescola concetti di capitoli diversi
  - `[RETRIEVAL]` — riscrivi da zero dalla memoria
  - `[DEBUG]` — trova il bug da solo (dal M2 in poi)
  - `[REAL-WORLD]` — consegna vaga, dati sporchi (dal M5 in poi)
  - `[RECALL CROSS-MODULO]` — riprendi skill di moduli precedenti (dal M3 in poi)
  - `[SYSTEM DESIGN]` — progetta un'architettura (dal M5 in poi)

### E. Progetto Incrementale (15-25 min)
- Alla fine degli esercizi c'e' la sezione `PROGETTO INCREMENTALE`
- Ogni capitolo aggiunge un pezzo al "Catalogo E-commerce" — il tuo progetto che attraversa tutto il corso

### F. Soluzioni
- In fondo al file trovi tutte le soluzioni (quiz + esercizi)
- **NON guardarle prima di aver provato**

### G. Correzione con il Mentor
- Quando hai finito, chiedi al Mentor AI (in chat) di correggere
- Il Mentor ti da' un feedback e aggiorna il tuo progresso
- Alla fine, **dai un voto di difficolta da 1 a 10** — se dimentichi, il Mentor te lo chiede

---

## Passo 3 — La Mappa dei Moduli

Segui questo ordine. Non saltare moduli.

```
FONDAMENTA (Mese 1-2)
━━━━━━━━━━━━━━━━━━━━━
 M1  Python & Dati .................. 12 capitoli  | CPU locale
 M2  Machine Learning ............... 6 capitoli  | CPU locale
 PM  Ponte Matematico ............... 2 capitoli  | CPU locale
 M3  Deep Learning & Computer Vision  7 capitoli  | Google Colab (GPU)
 M4  NLP, Embeddings & Transformers   7 capitoli  | CPU locale

CORE AI (Mese 3-4)
━━━━━━━━━━━━━━━━━━
 M5  LLM & Prompt Engineering ...... 10 capitoli  | CPU + API/Ollama
 M6  RAG Systems ................... 10 capitoli  | CPU + API/Ollama
 M7  AI Agents & Automation ........  9 capitoli  | CPU + API/Ollama
 M8  Fine-Tuning & Personalizzazione  7 capitoli  | Google Colab (GPU)

PRODUZIONE (Mese 5-6)
━━━━━━━━━━━━━━━━━━━━━
 M9  MLOps, Docker, Test & Deploy ..  9 capitoli  | CPU locale
 M10 Progetto Finale Full-Stack ....  8 fasi      | CPU + Colab + Cloud
```

### Legenda piattaforme

| Piattaforma | Quando | Perche' |
|-------------|--------|---------|
| **CPU locale** | M1, M2, PM, M4, M5-M7, M9 | Tutto gira sul tuo PC |
| **Google Colab** | M3, M8 | La tua GPU (AMD Vega 10) non supporta CUDA. Colab ti da' una GPU NVIDIA gratis |
| **API OpenAI** | M5, M6, M7 | Per le chiamate LLM. Budget: 30-50 EUR totali |
| **Ollama (CPU)** | M5, M6, M7 | Modelli AI gratuiti che girano in locale (fino a ~3B parametri) |
| **Cloud** | M9, M10 | Per il deploy delle demo (Streamlit Cloud, HuggingFace Spaces, Railway) |

---

## Documentazione prodotto (Validator + Replicator)

Specifiche e architettura delle due app del portfolio (fine corso M10):

- Indice: [`docs/prodotto/README.md`](docs/prodotto/README.md) (stub rapido: [`APPUNTI_APPLICATIVO.md`](APPUNTI_APPLICATIVO.md))
- Codice scaffold: [`aplicativo/`](aplicativo/README.md)

---

## Passo 4 — Cosa Fare a Inizio Modulo

Quando inizi un nuovo modulo:

1. **Apri il README.md** dentro la cartella del modulo (es. `modulo_02_ml/README.md`)
2. **Scommmenta le dipendenze** nel file `requirements.txt` della root e reinstalla:
   ```bash
   pip install -r requirements.txt
   ```
3. Se il modulo richiede **Google Colab** (M3, M8):
   - Il Mentor ti preparera' un notebook Colab con tutto preinstallato
   - Workflow: scrivi codice in Cursor → copia nel notebook → training su Colab → risultati in locale
4. Se il modulo usa **API a pagamento** (M5-M7):
   - Prova PRIMA con Ollama (gratis)
   - Passa alle API solo quando serve qualita' superiore
   - Il Mentor tiene traccia dei costi — chiedigli "quanto ho speso fin qui?"

---

## Passo 5 — Cosa Fare a Fine Modulo

1. Completa la sezione `CONFRONTO PRIMA/DOPO` nell'ultimo capitolo
2. Verifica che la **demo del modulo** sia deployata e funzionante
3. Il Mentor crea un file archivio (`ARCHIVIO_MODULO_XX.md`) per liberare spazio nel contesto

---

## Passo 6 — Mock Interview (dal M4 in poi)

Una volta al mese, il Mentor simula un colloquio tecnico reale:
- 3 domande, 15 minuti ciascuna
- **Cronometrati** — non sforare
- Il Mentor diventa freddo e professionale (niente hint, niente incoraggiamenti)
- Alla fine ricevi un voto: "Passeresti / Borderline / Non passeresti"
- I risultati sono tracciati in `CONTESTO_CORSO.md`

Puoi chiedere un mock interview in qualsiasi momento scrivendo: **"facciamo un mock interview"**

---

## Il Tuo Portfolio — 8 Demo Deployate

Man mano che avanzi, costruirai 8 progetti deployati:

| # | Progetto | Modulo | Dove lo trovi |
|---|----------|--------|---------------|
| 1 | Predittore prezzo case | M2 | Streamlit Cloud |
| 2 | Classificatore immagini | M3 | HuggingFace Spaces |
| 3 | Analizzatore recensioni | M4 | Streamlit Cloud |
| 4 | Assistente e-commerce AI | M5 | Streamlit Cloud |
| 5 | RAG documentale | M6 | Streamlit Cloud |
| 6 | Agente di ricerca | M7 | Streamlit Cloud |
| 7 | Demo fine-tuning | M8 | HuggingFace Spaces |
| 8 | Prodotto full-stack AI | M10 | Cloud (Railway/Render) |

**3-5 demo deployate battono qualsiasi certificazione.**

---

## Struttura delle Cartelle

```
Corso-AI/
├── README.md                    ← SEI QUI — il manuale che stai leggendo
├── CONTESTO_CORSO.md            ← La "memoria" del Mentor AI (non toccare)
├── roadmap_ai.md                ← La struttura dettagliata di ogni modulo
├── requirements.txt             ← Le dipendenze Python
├── .cursor/rules/               ← Le regole per il Mentor AI (non toccare)
│
├── modulo_01_python_dati/       ← MODULO 1 (in corso)
│   ├── README.md                ← Guida specifica del modulo
│   ├── 01_benvenuto_python.py   ← Capitolo 1
│   ├── 02_condizioni_e_cicli.py
│   ├── ...
│   ├── 12_web_bridge.py         ← Ultimo capitolo del modulo
│   └── dati/                    ← File CSV e dati di supporto
│
├── modulo_02_ml/                ← MODULO 2 (da creare)
├── ponte_matematico/            ← PONTE MATEMATICO (da creare)
├── modulo_03_dl_cv/             ← MODULO 3 (da creare)
├── ...
└── modulo_10_progetto_finale/   ← MODULO 10 (da creare)
```

### File che NON devi modificare manualmente

| File | Perche' |
|------|---------|
| `CONTESTO_CORSO.md` | Lo aggiorna il Mentor AI automaticamente. Contiene il tuo progresso, errori, glossario |
| `.cursor/rules/mentor-ai-corso.mdc` | Le istruzioni per il Mentor. Modificarle cambierebbe il comportamento dell'AI |
| `roadmap_ai.md` | La struttura dei moduli. Consultalo per sapere cosa ti aspetta |

### File che PUOI e DEVI modificare

| File | Come |
|------|------|
| I file `.py` dei capitoli | Scrivi il tuo codice sotto ogni esercizio |
| `requirements.txt` | Scommenta le dipendenze quando inizi un nuovo modulo |

---

## Ripassare — Come Non Dimenticare

Il corso ha un sistema di ripasso integrato:

1. **Quiz d'ingresso**: ogni capitolo inizia con domande sul capitolo precedente
2. **Rinforzo mirato**: se sbagli un quiz, il concetto viene rispiegato nel capitolo successivo
3. **Glossario con contatore**: il Mentor traccia quante volte usi correttamente ogni termine
4. **Esercizi RETRIEVAL**: riscrivi funzioni precedenti dalla memoria
5. **Esercizi RECALL CROSS-MODULO**: usa competenze di moduli precedenti in contesti nuovi
6. **Ripasso programmato**: il Mentor inserisce ripassi a 3, 7 e 14 giorni

**Consiglio extra**: una volta a settimana, scegli 2-3 esercizi `[COLLOQUIO]` gia' fatti e riscrivili da zero su un file vuoto, cronometrandoti (15-20 min per esercizio).

---

## Domande Frequenti

### "Devo seguire i capitoli in ordine?"
**Si'.** Ogni capitolo costruisce sul precedente. Saltare e' come saltare un gradino rotto sulle scale.

### "Posso usare l'autocompletamento?"
**No, durante lo studio.** L'autocompletamento ti impedisce di memorizzare. Riattivalo quando lavori su progetti reali.

### "Quanto tempo ci vuole al giorno?"
**1-2 ore** e' il ritmo ideale. Con meno di 1 ora perdi il filo, con piu' di 3 ti esaurisci.

### "Se sono bloccato su un esercizio?"
Chiedi al Mentor in chat. Lui ti guida senza darti la soluzione — ti dice dove guardare, poi perche', poi un esempio simile. La soluzione completa arriva solo dopo 2+ tentativi.

### "Non ho capito un concetto, posso andare avanti?"
**No.** Dillo al Mentor: "non ho capito X". Lui te lo rispiega con un'analogia diversa. Non andare avanti con dubbi — si accumulano.

### "Cosa faccio se il Mentor non ha contesto?"
All'inizio di ogni nuova chat, il Mentor legge automaticamente il tuo progresso da `CONTESTO_CORSO.md`. Se qualcosa non torna, digli "sono al file X del modulo Y" e lui si riallinea.

### "Posso studiare su un altro PC?"
Si'. Clona la repo da GitHub e ricrea il venv:
```bash
git clone <url-della-tua-repo>
cd Corso-AI
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### "Google Colab e' gratis?"
Si'. Il piano gratuito include una GPU (T4 o simile) con limite di tempo (~12 ore/sessione). Piu' che sufficiente per il corso.

### "Quanto spendero' in API?"
Budget stimato: **30-50 EUR totali** per tutto il corso. La maggior parte degli esercizi funziona con Ollama (gratis). Le API servono solo per demo finali e funzionalita' avanzate (vision, function calling).

---

## Checklist Rapida — Inizio Sessione di Studio

- [ ] Terminale aperto con `(venv)` attivo
- [ ] Capitolo corrente aperto in Cursor
- [ ] Chat col Mentor aperta (lui ti dice dove sei)
- [ ] Autocompletamento disattivato
- [ ] 1-2 ore di tempo senza distrazioni
- [ ] Quiz d'ingresso fatto PRIMA di leggere la teoria

---

## La Tua Posizione Attuale

> Questa sezione la aggiorna il Mentor. Guardala per sapere dove sei.

**Modulo**: 1 — Python & Dati
**Capitolo in corso**: 05_dizionari.py
**Prossimo**: completare gli esercizi finali del cap. 05, poi quiz di verifica
**Demo completate**: 0/8
**Mock interview superati**: 0/7
