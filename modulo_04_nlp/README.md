# Modulo 4 — NLP, Embeddings & Transformers

> **Stato**: 🟡 **In corso — 0/7 capitoli** (modulo aperto il 25/09/2026). Capitolo attivo: `01_testo_come_numeri.py`.
> Vedi `CONTESTO_CORSO.md` → Stato Attuale / Ramo testuale nel Prodotto.

> ⚠️ **Debito M3 aperto**: il Modulo 3 è chiuso sui contenuti (10/10 capitoli) ma **non archiviato** — manca l'URL pubblico della demo (portfolio #2, bloccato dalla policy Hugging Face) e restano `12_grad_cam_interpretabilita.py` da svolgere, il TODO 7 e il 🔄 CONFRONTO PRIMA/DOPO del cap.10. Il M4 parte comunque: sono debiti di deploy/coda, non prerequisiti.

## Obiettivo del modulo

Capire **come il testo diventa numeri** e come si misura il *significato*. È il modulo più importante per tutto ciò che viene dopo: senza embeddings non esistono RAG (M6), ricerca semantica, né la maggior parte delle domande da colloquio su GenAI.

Filo narrativo del modulo:

```
testo grezzo → conteggi (cap.01) → coordinate del significato (cap.02-03)
             → come fa un Transformer a leggerlo (cap.04)
             → ecosistema HuggingFace (cap.05) → classificare davvero (cap.06)
             → demo di portfolio (cap.07)
```

## Demo finale di portfolio

Analizzatore di testi (recensioni / note documentali) con Streamlit — **portfolio #3**.
Nota: il portfolio #2 (M3, Gradio) è ancora senza URL; se nel frattempo si sblocca l'hosting, si recupera lì.

## Indice capitoli

| # | File | Argomento | Difficoltà attesa | Piattaforma |
|---|------|-----------|-------------------|-------------|
| 01 | `01_testo_come_numeri.py` 🟡 **scritto** (25/09/2026), da svolgere | Normalizzazione e tokenizzazione del testo italiano (apostrofi, accenti, importi, date), vocabolario, **Bag of Words** a mano e con `CountVectorizer`, **TF-IDF** (intuizione → codice → formula), similarità coseno fra documenti, limiti del conteggio. Recall M2: `fit` solo sul train = niente leakage. | 6/10 | CPU locale |
| 02 | `02_embeddings.py` ⚪ placeholder | Da conteggi a **coordinate del significato**: word embeddings, `sentence-transformers`, modelli multilingua, cosa cattura e cosa no | 7/10 | CPU locale (modelli piccoli) |
| 03 | `03_similarita_coseno.py` ⚪ placeholder | Misurare distanza fra significati, soglie, top-k, valutazione di una ricerca semantica | 6/10 | CPU locale |
| 04 | `04_transformer_spiegato.py` ⚪ placeholder | Architettura Transformer ad alto livello: attention come "a cosa guardo mentre leggo". Domanda da colloquio. **Mock interview** del modulo (Regola 27) | 7/10 | CPU locale |
| 05 | `05_huggingface_pipeline.py` ⚪ placeholder | `transformers`: pipeline, tokenizer, modelli pre-addestrati, model card. L'"npm dell'AI" | 6/10 | CPU locale + Colab se serve |
| 06 | `06_sentiment_classificazione.py` ⚪ placeholder | Classificazione di testo e sentiment: baseline TF-IDF vs modello pre-addestrato, metriche, analisi errori | 7/10 | CPU locale |
| 07 | `07_progetto_recensioni.py` ⚪ placeholder | Progetto: analizzatore testi + Streamlit (portfolio #3) + 🔄 CONFRONTO PRIMA/DOPO | 7/10 | CPU + Streamlit Cloud |

**Tempo stimato**: 2-3 settimane.

> ⚪ **placeholder** = il file esiste e contiene già obiettivo, contenuto previsto, DoD provvisoria, prerequisiti, ripassi Regola 43 da inserire, libri di riferimento e task del progetto incrementale. **Non è il capitolo**: va sostituito dal mentor con il contenuto completo quando il capitolo precedente è chiuso. Eseguirlo stampa solo un promemoria.

## Librerie

Già disponibili nel `venv`: `numpy`, `pandas`, `scikit-learn`, `matplotlib`, `streamlit`.

Da installare **prima del cap.02** (scommentate in `requirements.txt`):

```
transformers>=4.46
sentence-transformers>=3.3
tokenizers>=0.20
```

Il **cap.01 non richiede installazioni**: gira con quello che hai già.

## Vincoli operativi

### Hardware
- AMD Vega 10 → niente CUDA in locale, ma qui serve poco: gli embedding di frasi con modelli piccoli (`all-MiniLM`, `paraphrase-multilingual-MiniLM`) girano su CPU.
- Colab solo se un capitolo richiede un modello grande o un fine-tuning (non previsto prima del M8).

### Privacy / GDPR
1. Nel M3 il rischio era l'**immagine** del documento. Qui è il **testo**, che è peggio: un OCR contiene nome, codice fiscale, IBAN, importi — tutti dati personali in chiaro.
2. Regola: nel corso si lavora **solo** su testi sintetici (`dati/note_documenti.csv`) o su testo reale **già anonimizzato in locale**.
3. Mai incollare testo di documenti reali in servizi esterni (API, demo pubbliche, notebook condivisi).
4. Il `.gitignore` esistente copre `dati/buste_*/` e i corpus dell'applicativo: non aggirarlo.

## Quiz ripasso fondamentali tra capitoli (Regola 40)

**Obbligatorio dal Modulo 3**: dopo ogni capitolo e prima del successivo, completare il bridge corrispondente in:

`modulo_04_nlp/quiz_ripasso_tra_capitoli/`

(~10 mini-esercizi facili — Python, Pandas, NumPy, recall M2/M3). Indice e naming nel README di quella cartella.

## Filo del progetto incrementale (M4)

Il modulo costruisce il **ramo testuale** del prodotto "Controllo Documentale AI":

- M2 → cuore predittivo tabellare · M3 → ramo visivo (`prob_busta_paga_visivo`)
- **M4 → ramo testuale**: normalizzazione del testo OCR, classificazione del **tipo documento** dal testo, estrazione campi e **matching semantico** fra documenti della stessa pratica (il codice fiscale sulla busta paga corrisponde a quello sulla CU?)
- M5 → estrazione strutturata con LLM · M6 → RAG normativo

Deliverable che nasce qui: `testo_utils.py` (normalizzazione + tokenizzazione robusta per OCR italiano) e la feature `prob_tipo_doc_testuale`.

## Cosa si "ricicla" da moduli precedenti

- **Ponte cap.01 (norma, dot product, similarità coseno)** → cap.01 M4: la stessa formula, applicata a vettori di parole invece che a vettori di pratiche.
- **M2 cap.05 (leakage, `fit` solo sul train)** → cap.01 M4: il vocabolario del vettorizzatore si impara **solo** sul train, altrimenti è leakage silenzioso.
- **M2 cap.04 (metriche, soglie)** → cap.06 M4 sulla classificazione di testo.
- **M3 cap.10 (contratto di inferenza, demo)** → cap.07 M4: stessa disciplina, testo invece di immagini.

## Da NON dimenticare quando si crea ogni capitolo

- Quiz d'ingresso + quiz di verifica (almeno 1 Feynman nel quiz di verifica)
- Bridge Regola 40 fra un capitolo e il successivo
- Blocchi `# 🔁 RIPASSO PROPOSITIVO` (**Regola 43**) prima di ogni richiamo al passato
- 1 `🎯 [COLLOQUIO]` · 1 `🔧 [REFACTORING]` · 1 `🔍 [DEBUG]` · 1 `🧠 [RETRIEVAL]` · 1 `🔀 [INTERLEAVING]`
- Cap.01: 1 `🔄 [RECALL CROSS-MODULO]` (Regola 26)
- Sezione `🏗️ PROGETTO INCREMENTALE`
- Cap.07 (ultimo del modulo): sezione `🔄 CONFRONTO PRIMA/DOPO`
- Blocchi 📚 dai libri: **[NLP-TRANS]** (Tunstall/von Werra/Wolf) e **[ALAMMAR]** — vedi `docs/libri_corso/MAPPATURA_LIBRI_MODULI.md`
- Diario `sessioni_capitoli/M04_C0X_*_sessione.md` aggiornato in append-only
- Dal M4: **mock interview** mensile (Regola 27)
