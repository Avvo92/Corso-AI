# Libri di riferimento — Integrazione organica nel corso

> **Attivo dal 05/08/2026.** Gianluca ha acquistato i libri in `books/`.
> **Sync multi-PC (05/08/2026):** la cartella `books/` è **tracciata in Git** (repo del corso) così puoi clonare/pullare sul secondo PC.
> **Vincolo:** il repo GitHub deve restare **privato** — sono PDF protetti da copyright (uso personale / backup tra i tuoi dispositivi). Non rendere il repo pubblico.
> Indice e protocollo: questo file · mappa: [`MAPPATURA_LIBRI_MODULI.md`](MAPPATURA_LIBRI_MODULI.md) · schede: [`schede/`](schede/).

---

## Inventario locale (`books/`)

| Codice | File | Autore | Repo ufficiale (notebook gratis) |
|--------|------|--------|----------------------------------|
| **PYTORCH** | `Deep-Learning-with-PyTorch.pdf` | Stevens, Antiga, Viehmann (**1ª ed. 2020** nel PDF locale) | [pytorch.org/tutorials](https://pytorch.org/tutorials/) |
| **GERON** | `Hands-On Machine Learning Aurélien Géron.pdf` | Géron | [github.com/ageron/handson-ml3](https://github.com/ageron/handson-ml3) |
| **ALAMMAR** | `Hands-On_Large_Language_Models_-_Jay_Alammar.pdf` | Alammar, Grootendorst | [github.com/HandsOnLLM/Hands-On-Large-Language-Models](https://github.com/HandsOnLLM/Hands-On-Large-Language-Models) |
| **HUYEN-AIE** | `AI Engineering by Chip Huyen.pdf` | Chip Huyen | [github.com/chiphuyen/aie-book](https://github.com/chiphuyen/aie-book) |
| **NLP-TRANS** | `NLP with Transformers … Wolf.pdf` | Tunstall, von Werra, Wolf | [huggingface.co/learn/nlp-course](https://huggingface.co/learn/nlp-course) |
| **STATS** | `Practical Statistics for Data Scientists …` | Bruce | — |
| **MML** | `Mathematics for Machine Learning.pdf` | Deisenroth et al. | — |
| **LINALG** | `Linear Algebra for Everyone.pdf` | Strang | — |

Libri extra (non nel syllabus): `Jeff Hawkins - On Intelligence.pdf` — solo curiosità, ignorare per il corso.

---

## Principio: corso prima, libro dopo

1. **Il file capitolo `.py` resta la spina dorsale** — obiettivi, quiz, esercizi, prodotto.
2. **Il libro è seconda voce** — stesso concetto, angolo diverso, spesso con figura o esempio diverso.
3. **In chat** il mentor può citare il libro quando aiuta (lacuna, domanda, ripasso).
4. **Nei capitoli** compaiono blocchi `# 📚 LETTURA PARALLELA` (vedi sotto).
5. **Non si copiano pagine intere** — si cita capitolo/sezione, si parafrasa, si adattano esercizi.

---

## Protocollo schede (costruzione capitoli — attivo 05/08/2026)

Quando il mentor **crea o arricchisce** un pezzo di capitolo M3+:

1. Consulta `MAPPATURA_LIBRI_MODULI.md`.
2. Estrae testo mirato dal PDF (`pdftotext` / lettura sezioni).
3. Scrive o aggiorna una **scheda** in `docs/libri_corso/schede/` (template: `_TEMPLATE_scheda_libro.md`).
4. Inietta nel `.py`: teoria arricchita + `# 📚 LETTURA PARALLELA` + eventuale `# 📚 [LIBRO]`.
5. In chat: elenca cosa ha preso dal libro e cosa ha scartato.

| Scheda esistente | Capitolo |
|------------------|----------|
| `M03_C07_sez6_state_dict.md` | Sez. 6 `state_dict` |
| `M03_C07_sez2_5_puntatori.md` | Sez. 2–5 puntatori 📚 |

---

## Protocollo mentor (obbligatorio da M3 cap.07 in poi)

### Quando preparare o revisionare un capitolo

1. Leggere `docs/libri_corso/MAPPATURA_LIBRI_MODULI.md` per il capitolo target.
2. Inserire **1–3 blocchi** `# 📚 LETTURA PARALLELA` nelle sezioni teoria (dopo mini-esercizio o prima del quiz).
3. Opzionale: **1 esercizio** `# 📚 [LIBRO]` per modulo (ispirato al libro, **riformulato**, dominio corso/prodotto).
4. In **Self-check** (CONTESTO): citare codici libro usati nel capitolo.

### Formato blocco nei file `.py`

```python
# 📚 LETTURA PARALLELA — [PYTORCH] cap. 3, §3.2 "Tensors"
# Nel libro: stessa idea del dizionario NumPy→torch sopra, con enfasi su device e dtype.
# Dopo il mini-esercizio: apri il PDF e confronta la tabella del libro con la nostra.
# Domanda guida: cosa aggiunge il libro che qui non abbiamo scritto?
# TUA RISPOSTA (opzionale, 1-3 righe):
#
```

### Formato esercizio adattato

```python
# 📚 [LIBRO] — Ispirato a [GERON] cap. 10, es. 10.1 (adattato al CSV M2)
# Obiettivo: ... (stesso skill del libro, dati/contesto del corso)
```

### In chat (spiegazioni)

- Citare: `[PYTORCH cap. 5]` o `Géron, cap. 10 — training loop Keras vs il nostro in PyTorch`.
- Se il libro usa TensorFlow/Keras e il corso PyTorch: **sempre** tradurre (come già fatto NumPy→torch).
- Suggerire lettura **dopo** aver tentato mini-esercizio del capitolo, non prima.

---

## Protocollo studente (Gianluca)

| Momento | Cosa fare |
|---------|-----------|
| Durante il capitolo | Segui il `.py`; ignora il PDF salvo blocchi 📚 |
| Dopo ogni sezione con 📚 | 10–15 min: leggi la sezione indicata, rispondi alla "domanda guida" |
| Fine modulo | Ripasso verticale: 1 capitolo libro per intero (mappa sotto) |
| Lacuna persistente | Apri il libro alla sezione mappata + chiedi al mentor |

---

## Mappa sintetica (dettaglio in MAPPATURA_LIBRI_MODULI.md)

| Modulo / capitolo corso | Libro primario | Libro secondario |
|-------------------------|----------------|------------------|
| M3 cap.07 PyTorch intro | **PYTORCH** | GERON cap. 10–12 (DL, tradurre TF→torch) |
| M3 cap.08 CNN | **PYTORCH** + GERON cap. 14 | — |
| M3 cap.09 Transfer learning | **PYTORCH** + GERON cap. 14 | — |
| M3 cap.10 Gradio / deploy | GERON cap. 19 (deploy) | PYTORCH cap. deploy |
| M4 NLP / embedding | **ALAMMAR** Part 1–2 | NLP-TRANS |
| M5 LLM / prompt | **HUYEN-AIE** + **ALAMMAR** Part 2–3 | — |
| M6 RAG | **HUYEN-AIE** + **ALAMMAR** (RAG) | — |
| M7 Agents | **HUYEN-AIE** (agenti) | — |
| M2 ripasso (on demand) | **GERON** cap. 1–9 | STATS |
| Ponte / math (on demand) | LINALG, MML | — |

---

## Gate agenti

Per task didattici su capitoli M3+:

1. `CONTESTO_CORSO.md` (sezione **Libri di riferimento**)
2. Questo file + `MAPPATURA_LIBRI_MODULI.md`
3. Capitolo `.py` in lavorazione

---

## Changelog

| Data | Decisione |
|------|-----------|
| 05/08/2026 | Integrazione libri acquistati; cartella `books/` esclusa da Git; protocollo 📚 attivo da cap.07 M3. |
