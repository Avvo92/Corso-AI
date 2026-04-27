# Diario sessione — Capitolo 07 — Deploy Streamlit Cloud (primo URL portfolio)

| Campo | Valore |
|-------|--------|
| **Modulo** | M02 — Machine Learning Fundamentals |
| **File capitolo** | `07_deploy_streamlit_cloud.py` |
| **File diario** | `M02_C07_deploy_streamlit_cloud_sessione.md` |
| **Stato** | completato (27/04/2026) |
| **Voto difficoltà** | 6/10 |
| **Deploy live** | https://appappdazeropy-g5tde3wvxdewl5arzmeq2j.streamlit.app/ |

---

## Domande durante lo studio

- **Q:** Cosa serve davvero per portare la demo online su Streamlit Cloud?
  **Nota / risposta sintetica:** repo GitHub accessibile, `requirements.txt` allineato (solo dipendenze realmente usate), path deploy-safe (`__file__` + `os.path.join`), main file path corretto (`modulo_02_ml/app_streamlit_da_zero.py`).

- **Q:** Perché un import inutile è un problema in cloud?
  **Nota / risposta sintetica:** se finisce in `requirements.txt` allunga il build, può creare conflitti di versione, e se quella libreria manca o cambia API → app down. Inoltre confonde chi legge il codice (es. `from scipy.integrate._ivp.radau import C` non c'entra nulla con `LogisticRegression(C=...)`).

---

## Valutazioni esercizi / quiz / mini-esercizi

### 2026-04-27 — Quiz d'ingresso Q1 (V/F: locale = cloud?)

- **Blocco:** `07_deploy_streamlit_cloud.py` — Quiz d'ingresso Q1.
- **Valutazione (primo tentativo — "voto esame"):** **9/10**.
- **Punti chiave corretti:** "Falso" + 3 motivi reali: path deploy-safe (no assoluti), requirements allineati, evitare dipendenze inutili.
- **Micro-miglioria:** aggiungere "differenze di ambiente" (versioni Python, working directory, file presenti in cloud vs in locale).
- **Pattern errore / ID contesto:** rinforzo Lacuna #16 (scala UI) collaterale; consolidamento Regola 38 (primo deploy anticipato al M2).

### 2026-04-27 — Quiz d'ingresso Q2 (path assoluto in `read_csv`)

- **Blocco:** `07_deploy_streamlit_cloud.py` — Quiz d'ingresso Q2.
- **Valutazione (primo tentativo — "voto esame"):** **9.5/10**.
- **Punti chiave corretti:** path assoluti dipendono dal filesystem locale → in cloud non esistono → `FileNotFoundError`. Soluzione `os` + `__file__` + `os.path.join` per path cross-OS.
- **Micro-miglioria:** menziona anche `os.path.dirname(os.path.abspath(__file__))` per rendere l'absolute esplicito (edge case Windows con CWD diverso).

### 2026-04-27 — Quiz d'ingresso Q3 (file minimi per Streamlit Cloud) — primo tentativo

- **Blocco:** `07_deploy_streamlit_cloud.py` — Quiz d'ingresso Q3.
- **Valutazione (primo tentativo — "voto esame"):** **6/10**.
- **Punti ok:** corretto `requirements.txt` e il file mock CSV.
- **Errore principale:** dichiari "readme esplicativo" come file *obbligatorio* — il README è raccomandato (portfolio) ma non bloccante per il deploy. Manca invece il file **app principale** (`app_streamlit_da_zero.py`), che è il vero obbligatorio per il "Main file path" su Streamlit Cloud.

### 2026-04-27 — Quiz d'ingresso Q3 (file minimi) — fix con app principale

- **Blocco:** `07_deploy_streamlit_cloud.py` — Quiz d'ingresso Q3 (revisione).
- **Valutazione:** **9.5/10**.
- **Punti chiave corretti:** ora hai i 3 obbligatori giusti: (1) `requirements.txt`, (2) `app_streamlit_da_zero.py` (main file path), (3) i file dati che l'app legge a runtime (CSV mock).
- **Micro-miglioria (opzionale):** README + `.gitignore` puliti aiutano nel portfolio ma non sono richiesti dal cloud.

### 2026-04-27 — Quiz d'ingresso Q4 (Feynman: cos'è `requirements.txt`)

- **Blocco:** `07_deploy_streamlit_cloud.py` — Quiz d'ingresso Q4.
- **Valutazione (primo tentativo — "voto esame"):** **9/10**.
- **Punti chiave corretti:** definizione corretta (lista delle librerie usate dall'app); chi clona/deploya installa tutte le dipendenze e l'app funziona uguale ovunque.
- **Micro-miglioria:** aggiungi che è meglio **fissare le versioni** (`pandas==2.2.3`) per riproducibilità — senza pin, un upgrade silenzioso può rompere l'app in cloud.

### 2026-04-27 — Quiz d'ingresso Q5 (rischio: import inutili / dipendenze extra) — primo tentativo

- **Blocco:** `07_deploy_streamlit_cloud.py` — Quiz d'ingresso Q5.
- **Valutazione (primo tentativo — "voto esame"):** **8/10**.
- **Punti ok:** confusione, errori di dipendenza dichiarata mancante.
- **Cosa manca per il "10":** menziona anche (1) tempo di build più lungo in cloud, (2) superficie di attacco/maintenance maggiore, (3) potenziali conflitti tra versioni.

### 2026-04-27 — Quiz d'ingresso Q5 (rischio import) — fix completo

- **Blocco:** `07_deploy_streamlit_cloud.py` — Quiz d'ingresso Q5 (revisione).
- **Valutazione:** **9.5/10**.
- **Punti chiave corretti:** ora la risposta copre tutti i rischi rilevanti: confusione, errori di dipendenza, build più lento, superficie di attacco, conflitti di versione.

### 2026-04-27 — Rinforzo Lacuna #16 (scala prob 0–1 vs score 0–100)

- **Blocco:** `07_deploy_streamlit_cloud.py` — Micro-check Lacuna #16.
- **Valutazione (primo tentativo — "voto esame"):** **10/10**.
- **Punti chiave corretti:** in 1 riga hai chiarito le scale: `prob_alterato` 0–1 e `score_genuinita` 0–100. Coerente con le label in UI.
- **Stato lacuna:** 🟢 Superato (rinforzata in app live + label UI esplicite).

### 2026-04-27 — Rinforzo Lacuna #17 (drop colonne reali)

- **Blocco:** `07_deploy_streamlit_cloud.py` — Micro-check Lacuna #17.
- **Valutazione (primo tentativo — "voto esame"):** **9.5/10**.
- **Punti chiave corretti:** `drop(columns=["pratica_id","y_alterato"])` è centralizzato in `split_X_y` e replicato in `X_una_pratica_da_id` per coerenza; cambiando dataset/target tocchi un solo punto centrale.
- **Micro-miglioria:** in app c'è un secondo `drop` in `X_una_pratica_da_id`: è ridondante ma sicuro. In una refactor "DRY" potresti far passare `X` (già pulito) come argomento.
- **Stato lacuna:** 🟢 Superato (applicato in app + verificato live).

### 2026-04-27 — Rinforzo Lacuna #18 (FN nel dominio)

- **Blocco:** `07_deploy_streamlit_cloud.py` — Micro-check Lacuna #18.
- **Valutazione (primo tentativo — "voto esame"):** **10/10**.
- **Punti chiave corretti:** definizione perfetta del FN: "pratica alterata (classe 1) che il modello fa passare per genuina (classe 0)" → il rischio più grave nel controllo documentale, motiva l'uso di **recall** sul classe alterata come metrica primaria.
- **Stato lacuna:** 🟢 Superato (mostrato in UI con `recall_test` + nota didattica).

### 2026-04-27 — STEP 7.1–7.5 (pulizia + requirements + push + deploy + smoke test)

- **Blocco:** `07_deploy_streamlit_cloud.py` — STEP 7.1, 7.2, 7.3, 7.4, 7.5.
- **Valutazione complessiva:** **10/10** (deploy live funzionante).
- **Punti chiave corretti:**
  - 7.1 pulizia: rimosso import inutile (`scipy.integrate._ivp.radau.C`); app gira pulita in locale.
  - 7.2 `requirements.txt`: solo dipendenze reali (streamlit, pandas, numpy, scikit-learn).
  - 7.3 push GitHub: codice + dati + `requirements.txt` pubblicati nel repo.
  - 7.4 main file path: `modulo_02_ml/app_streamlit_da_zero.py` impostato correttamente.
  - 7.5 smoke test post-deploy: cambio `pratica_id` → output cambia; motivi_top3 con segno; CV media±std visibile; recall test visibile; nessun errore log.
- **Risultato:** primo URL portfolio live.

---

## Lacune e dubbi ancora aperti

- Nessuna lacuna critica residua per il M2.
- Lacune #16/#17/#18 → 🟢 Superate (rinforzate, applicate in codice, verificate in app live).
- Da monitorare in M3+: gestione delle dipendenze (pin versioni, conflitti) quando entreranno torch/transformers.

---

## Note per il capitolo successivo (mentor)

- Aggiornare la tabella **Portfolio — Demo deployate per modulo** in `CONTESTO_CORSO.md` con l'URL live del progetto M2.
- Avviare il **Ponte Matematico (M2→M3)**: vettori, dot product, coseno, gradiente, discesa — sequenza analogia → codice → grafico → formula (Regola 21). NumPy + Matplotlib only.
- Mantenere coerenza col dominio "controllo documentale": appena introdotti vettori, mostrare come una **pratica = vettore di feature** (ponte mentale già usato, ora reso esplicito con la matematica sottostante).
- Cambio di passo previsto: il Ponte è leggero in carico cognitivo per uno con basi web (vettori = array di numeri), ma alto in densità concettuale (introduce gli oggetti che reggeranno tutto da M3 in poi).
