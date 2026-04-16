# Diario sessione — Capitolo 05 — Overfitting e validazione

| Campo | Valore |
|-------|--------|
| **Modulo** | M02 — Machine Learning Fundamentals |
| **File capitolo** | `05_overfitting_validazione.py` |
| **File diario** | `M02_C05_overfitting_validazione_sessione.md` |
| **Stato** | in corso |

---

## Domande durante lo studio

- **Q:** Perché `score_genuinita` è in percentuale (0–100) e `prob_alterato` in 0–1?  
  **Nota / risposta sintetica:** È la stessa informazione su due scale: `prob_alterato` è la probabilità nativa di `predict_proba` (0–1). `score_genuinita` è una scelta di prodotto/UX per essere leggibile (0–100) e utile per soglie semaforo.

- **Q:** “Demo” = codice scritto dal mentor?  
  **Nota / risposta sintetica:** Sì: demo = blocchi eseguibili già presenti nel capitolo per illustrare (Parti 1–5). Studente completa quiz/esercizi e il progetto in `modello_base.py`.

---

## Valutazioni esercizi / quiz / mini-esercizi

### 2026-04-14 — Rinforzo mirato (zona indecisa) + leakage micro-check

- **Esercizio / blocco:** `05_overfitting_validazione.py` — rinforzo “zona indecisa” (prob vs score) + micro-check leakage (drop colonne).
- **Punti di forza:** Ha capito la trasformazione concettuale `score_genuinita = 1 - prob_alterato` e il pattern “droppare ID + target da X”.
- **Errori / lacune:** 1) Confusione di scala: ha scritto `0.55` invece di `55` (0–100). 2) Uso di nomi astratti `id/target` invece dei nomi reali del mock (`pratica_id`, `y_alterato`) — dovuto anche a consegna poco specifica.
- **Correzione / suggerimento:** Fissare la conversione: `score_genuinita = (1 - prob_alterato) * 100` e `prob_alterato = 1 - score/100`. Sul mock: `X = pratiche.drop(columns=['pratica_id','y_alterato'])`, `y = pratiche['y_alterato']`.
- **Pattern errore / ID contesto:** Lacuna #16 (scala 0–1 vs 0–100), Lacuna #17 (nomi colonne reali); monitor #6 (chiarezza consegne / aderenza ai requisiti).

### 2026-04-14 — Quiz d’ingresso cap.05 — DOMANDA 1 (recall train ≠ produzione)

- **Esercizio / blocco:** `05_overfitting_validazione.py` — Quiz d’ingresso, Domanda 1.
- **Punti di forza:** Risposta **Falso** corretta; buon ragionamento: il train non misura la generalizzazione; hai collegato la “forbice” train vs test al rischio **overfitting**.
- **Errori / lacune:** Piccola precisione: dire “per avere un giudizio affidabile dobbiamo confrontarlo col recall del test” è vero **come fotografia finale**, ma in generale la scelta/ottimizzazione va fatta su **validation o CV sul train** e il test va usato una volta (o raramente) per evitare tuning sul test.
- **Correzione / suggerimento:** Formula mentale: **train = imparare**, **validation/CV (solo train) = scegliere**, **test = stimare**. Se scrivi una riga in più, cita esplicitamente che il test non va “guardato” ripetutamente.
- **Pattern errore / ID contesto:** Nessun pattern nuovo. Richiamo concettuale: evitare “tuning sul test” (già tema del cap.05).

### 2026-04-14 — Quiz d’ingresso cap.05 — DOMANDA 2 (recall alterati e priorità dominio)

- **Esercizio / blocco:** `05_overfitting_validazione.py` — Quiz d’ingresso, Domanda 2.
- **Punti di forza:** Hai centrato il cuore: sul dominio frodi/documenti, il recall sugli alterati ti dice quanto spesso **non ti scappano** casi alterati (riduci i **falsi negativi**). Ottima analogia “antifurto” e motivazione di business.
- **Errori / lacune:** Una precisione: il recall non “è il numero di falsi negativi”, ma la frazione \(TP/(TP+FN)\). Quindi è meglio dirlo come: “tra tutti gli alterati reali, quanti ne intercetto”.
- **Correzione / suggerimento:** Definizione pulita: **recall classe 1 = alterati trovati / alterati totali**. Poi aggiungi: “alto recall = pochi falsi negativi”.
- **Pattern errore / ID contesto:** Nessun pattern nuovo.

### 2026-04-14 — Quiz d’ingresso cap.05 — DOMANDA 3 (predict_proba e conversione score)

- **Esercizio / blocco:** `05_overfitting_validazione.py` — Quiz d’ingresso, Domanda 3.
- **Punti di forza:** Hai azzeccato entrambi i pezzi: colonna 1 = probabilità della classe positiva (`y_alterato`) e lo score usa moltiplicatore `100`.
- **Errori / lacune:** Nessuno.
- **Correzione / suggerimento:** Solo una micro-precisione di notazione: nello script il valore da inserire è `1` (cioè P(y=1)), non il nome della colonna. Ma il significato che hai scritto è corretto.
- **Pattern errore / ID contesto:** Nessun pattern nuovo.

### 2026-04-14 — Quiz d’ingresso cap.05 — DOMANDA 4 (scaler fit prima dello split = leakage)

- **Esercizio / blocco:** `05_overfitting_validazione.py` — Quiz d’ingresso, Domanda 4.
- **Punti di forza:** Corretto: se fai `scaler.fit(X)` prima dello split, fai entrare nel preprocessing informazioni del futuro test (media/deviazione standard calcolate anche sul test). Hai spiegato bene anche il “perché” operativo.
- **Errori / lacune:** Terminologia: si usa più spesso dire **data leakage** o **preprocessing leakage** (non “processing leakage”), ma il concetto è quello.
- **Correzione / suggerimento:** Regola da ricordare: `fit` (scaler, encoder, imputazione) **solo su X_train**, poi `transform` su train e test. Se vuoi essere ancora più “da lavoro”, collega alla `Pipeline` (così il fit avviene correttamente dentro ogni fold di CV).
- **Pattern errore / ID contesto:** Nessun pattern nuovo.

### 2026-04-14 — Quiz d’ingresso cap.05 — DOMANDA 5 (tuning su test = scorretto)

- **Esercizio / blocco:** `05_overfitting_validazione.py` — Quiz d’ingresso, Domanda 5.
- **Punti di forza:** Risposta **Falso** corretta. Ottima motivazione: il test deve restare “arbitro imparziale” e non deve influenzare la scelta di `max_depth`.
- **Errori / lacune:** Nessuno. (Se vuoi essere super-preciso: oltre al validation hold-out va benissimo anche CV sul solo train.)
- **Correzione / suggerimento:** Frase “da colloquio”: *tuning su validation/CV; test usato una volta per stima finale di generalizzazione*.
- **Pattern errore / ID contesto:** Nessun pattern nuovo.

### 2026-04-14 — Quiz d’ingresso cap.05 — DOMANDA 6 (albero profondo su dati piccoli)

- **Esercizio / blocco:** `05_overfitting_validazione.py` — Quiz d’ingresso, Domanda 6.
- **Punti di forza:** Risposta corretta e centrata: con `max_depth=None` su dati piccoli l’albero tende a “memorizzare” → accuracy sul train spesso ~100% e sul test spesso più bassa (segnale di overfitting).
- **Errori / lacune:** Solo forma: nella consegna c’era “più ___ (più bassa / più alta / uguale)”: tu hai scritto “bassa”. Inteso correttamente come “più bassa”.
- **Correzione / suggerimento:** Versione super-chiara: “train ≈ 100%, test **più bassa**”.
- **Pattern errore / ID contesto:** Nessun pattern nuovo.

### 2026-04-14 — Quiz d’ingresso cap.05 — DOMANDA 7 (accuracy ingannevole su classi sbilanciate)

- **Esercizio / blocco:** `05_overfitting_validazione.py` — Quiz d’ingresso, Domanda 7.
- **Punti di forza:** Esempio centrato: se il 90% è genuino e predici sempre 0, puoi avere accuracy ~90% ma un modello inutile per intercettare alterati. Buona analogia “allarme rotto”.
- **Errori / lacune:** Hai confuso la formula del recall: hai scritto `TP/(TP+FP)` (quella è la **precision**) e hai derivato un caso `0/0`. In realtà recall (classe 1) = `TP/(TP+FN)`; nel caso “predico tutti genuini”: TP=0 e FN=numero alterati ⇒ recall=0.
- **Correzione / suggerimento:** Frase pulita: “accuracy alta può essere uno specchietto per le allodole su classi sbilanciate; guardo anche recall sugli alterati perché mi dice quanti casi 1 mi scappano (FN).”
- **Pattern errore / ID contesto:** Lacuna (quiz): recall vs precision (denominatore TP+FN vs TP+FP).

---

## Lacune e dubbi ancora aperti

- Scala `prob_alterato` vs `score_genuinita` da ri-verificare al prossimo quiz.
- Aderenze ai nomi reali delle colonne (evitare `id/target` generici nei capitoli con dataset esplicito).

---

## Note per il capitolo successivo (mentor)

- Inserire `# 🔁 RINFORZO MIRATO` su: (a) scale 0–1 vs 0–100; (b) “drop colonne reali” con micro-esempio coerente con `pratiche_genuinita_mock.csv`.

---

### 2026-04-15 — Correzioni live + avanzamento cap.05 (mini-esercizi, quiz verifica, es.1-2)

- **Mini-esercizio 1 (gap train-test + “generalizzare”)**: risposta corretta. Hai notato un gap ~7% e definito generalizzazione come “andare bene su dati mai visti”.
- **Mini-esercizio 2 (ordine tuning vs test + soglie semaforo)**: corretto dopo revisione. Punto chiave scritto bene: **non si ottimizzano soglie/iperparametri sul test** (test = arbitro finale).
- **Mini-esercizio 3 (perché CV solo su train + std alta)**: corretto. Std alta = metrica instabile tra split (spesso per dataset piccolo/rumoroso).
- **Mini-esercizio 4 (iperparametri vs policy + parola mentor + bias-varianza)**:
  - Sequenza corretta: prima stabilizzi modello (CV/validation), poi calibri soglie policy, test solo alla fine.
  - “Recall alto train e basso test” → overfitting (varianza alta). Da ripulire solo la terminologia “flex-varianza” → **bias-varianza**.
  - Trade-off visibile come picco su valid/test e poi calo mentre train resta alto.

- **Quiz di verifica (Domande 1–7)**:
  - D1 (CV non sostituisce test): corretta e ben motivata.
  - D2 (definizione overfitting): corretta; nota utile: train alto vs test/val più basso.
  - D3 (trova l’errore): corretto dopo aggiornamento — errore = **tuning sul test**; `random_state` è extra di riproducibilità.
  - D4 (StratifiedKFold): concetto corretto (“proporzione delle classi”).
  - D5 (andamento accuracy train/test vs max_depth): corretto (train sale; test sale poi può scendere).
  - D6 (test visto più volte = “barare”): corretto, con motivazione centrata (ottimismo/stima non onesta).
  - D7 (dataset piccolo e singolo split): corretto (CV stabilizza: media + variabilità).

- **Esercizio 1 (albero max_depth=2 vs None, accuracy train/test)**: esecuzione corretta (split con stratify e `random_state=42`, stampa 4 numeri). Commento sul gap centrato: albero profondo tende a overfittare; modello semplice può generalizzare meglio.
- **Esercizio 2 (CV recall per max_depth in [2,4,6,None])**: implementazione corretta (loop + `cross_val_score` su `X_train,y_train`, tabella con media e std). Nota: coerenza su percentuali/std; `random_state=42` nel classifier consigliato per replicabilità (poi aggiunto).

- **Domande concettuali chiarite in chat (da tenere come ponte mentale)**:
  - Differenza tra validation set e cross-validation; cosa vuol dire “ruotare” i fold.
  - `cross_val_score` vs `validation_curve`: il primo dà score su fold di validazione; la seconda esplora valori iperparametro e restituisce matrici train/valid per fold.
  - `np.argmax`: restituisce l’indice del massimo (usato per scegliere il `max_depth` migliore in griglia).

- **Pattern/lacune emerse**:
  - Attenzione a terminologia e concetti: bias-varianza; tuning sul test; distinzione recall vs precision (già emersa il 2026-04-14 nella D7 del quiz d’ingresso).

