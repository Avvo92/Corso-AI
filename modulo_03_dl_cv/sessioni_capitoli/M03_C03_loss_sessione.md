# Diario sessione — Capitolo 03 — LOSS (BCE e MSE)

| Campo | Valore |
|-------|--------|
| **Modulo** | M03 — Deep Learning & Computer Vision |
| **File capitolo** | `03_loss.py` |
| **File diario** | `M03_C03_loss_sessione.md` |
| **Stato** | in corso |
| **Voto difficoltà** | — / X/10 (atteso 6-7/10, focalizzato sulla sola loss) |

---

## ⚠️ Nota sullo split del vecchio capitolo 03

In data 27/05/2026 il vecchio capitolo `03_backpropagation.py` (1700 righe, atteso 9/10 di difficolta') e' stato giudicato "troppo denso" dallo studente e spezzettato in **4 sotto-capitoli**:

- `03_loss.py` ← QUESTO (loss BCE, MSE)
- `04_derivate_gradiente.py` (derivata, gradiente, derivata sigmoid)
- `05_chain_rule_gd.py` (chain rule + gradient descent)
- `06_backprop_training.py` (backward 2-layer + training loop)

Il diario precedente `M03_C03_backpropagation_sessione.md` e' stato rinominato in questo file. Le valutazioni della parte LOSS (Q1-Q5, TODO 1.x, micro AUC) restano qui sotto. Le valutazioni della parte DERIVATA (TODO 2.1, 2.3) sono state migrate nel diario `M03_C04_derivate_gradiente_sessione.md`.

---

## Obiettivi del capitolo (per il mentor)

- Far capire **cos'e' una LOSS** (BCE vs MSE — perche' BCE per classificazione binaria) come **misura continua e derivabile**.
- Mostrare 3 pattern operativi che lo studente tende a sbagliare: segno meno BCE, clip BILATERALE, soglia 0.5.
- Inserire rinforzi cap.01-02 (sigmoid, forward 2-layer, vettorizzazione) per evitare che il cap.03 sembri "scollegato".
- NON introdurre derivate, gradienti, chain rule, training: spostati nei cap.04/05/06.

---

## Strategia didattica (regola 21 — obbligatoria qui)

- Sequenza per OGNI concetto: **analogia concreta -> codice Python -> grafico -> formula in parole**.
- **Niente LaTeX**, niente notazione compressa.
- Se a meta' capitolo lo studente e' bloccato -> **STOP**, mini-recap.
- Pretendere il segno meno corretto della BCE in 3+ esercizi prima di chiudere la lacuna.
- Pretendere il clip BILATERALE in 2+ esercizi prima di chiudere la lacuna.

---

## Promemoria specifici dal cap.02 M3 (mentor)

- **Bridge ripasso** `M03_R02_after_C02_before_C03_reti_to_loss.md` deve essere fatto **prima** di aprire la teoria del cap.03 (~10 min, 10 esercizi facili). Bridge gia' esistente, rinominato il 27/05/2026 da `..._reti_to_backprop.md`.
- **Lacuna #31 UAT** (🟡): inserito blocco `# 🔁 RINFORZO MIRATO` dopo i Quiz d'ingresso ("UAT: esistenza vs come la trovi"). Verificato 22/05/2026 con micro-esercizio post-blocco UAT (10/10) — segno positivo per chiusura definitiva (verificare ricomparsa in cap.04+).
- **Pattern ⚠️ "loss vs metrica"** (cap.02 mini-progetto, AUC su 0/1): inserito blocco `# 🔁 RINFORZO MIRATO` a fine Sez.1 ("LOSS per addestrare, METRICA per giudicare"). Verificato 25/05/2026 con micro-esercizio AUC ROC (7/10 - parziale, residuo "ranking" non spiegato).
- **Pattern #6 (consegne)** e **#21 (tuple/round)**: niente blocco dedicato. Richiamarli in correzione se ricompaiono.

---

## Domande durante lo studio

- _(da popolare durante il capitolo - capitolo focalizzato, prevedere poche domande)_

---

## Valutazioni esercizi / quiz / mini-esercizi

> **Regole di registrazione (promemoria mentor):**
> - Voto = "primo tentativo" (esame); le correzioni successive si annotano come "Fix applicato" con nuovo voto solo se l'utente lo richiede esplicitamente.
> - Riferimento puntuale al blocco/righe del file `03_loss.py`.
> - Collegare ogni lacuna emersa al suo ID in `CONTESTO_CORSO.md`.

### 2026-05-22 — Rinforzo UAT micro-esercizio (`03_loss.py` blocco "RINFORZO MIRATO UAT")

- **Esercizio / blocco:** Micro-esercizio post-blocco UAT — cosa cambia dopo training (architettura / pesi / input / sigmoid).
- **Valutazione (primo tentativo — "voto esame"):** **10/10**.
- **Punti di forza:** Risposta (b) corretta: training aggiorna i pesi; architettura, input e sigmoid restano gli stessi.
- **Errori / lacune:** —
- **Correzione / suggerimento:** Lacuna #31 UAT (esistenza vs training) — segno positivo; chiudere in contesto se ripetuto a fine cap.06 (training completo).
- **Pattern errore / ID contesto:** Lacuna #31 UAT 🟡 — progresso.

---

### 2026-05-22 — Quiz d'ingresso Q5 Feynman (`03_loss.py` ~Q5)

- **Esercizio / blocco:** Q5 — loop di training senza jargon (4 righe max).
- **Valutazione (primo tentativo — "voto esame"):** **8/10**.
- **Punti di forza:** Ciclo completo forward → confronto p vs y → errore → correzione «all'indietro» per parametro → ripeti; nessuna parola vietata; binario e probabilità chiari; tono da collega tecnico ma comprensibile.
- **Errori / lacune:** Non rispetta «4 righe» (testo lungo, ~6 frasi); «livelli di parametri» un po' ambiguo per web dev; manca analogia semplice (manopole / tentativi su dataset) come nella soluzione tipo.
- **Correzione / suggerimento:** Comprimere in 4 righe; es. «provi su N esempi → misuri errore → aggiusti le manopoline → ripeti finché sbagli meno».
- **Pattern errore / ID contesto:** Feynman — ok concettualmente; formato vincoli da stringere.

---

### 2026-05-22 — Quiz d'ingresso Q4 (`03_loss.py` ~Q4)

- **Esercizio / blocco:** Q4 — conteggio parametri W1 (4,8), W2 (8,1) + bias.
- **Valutazione (primo tentativo — "voto esame"):** **10/10**.
- **Punti di forza:** Scomposizione corretta (32+8+8+1); totale 49; include b1 e b2 nel conteggio.
- **Errori / lacune:** Label «49 pesi» — in rigore sono **49 parametri** (pesi + bias); calcolo già corretto.
- **Correzione / suggerimento:** Opzionale: «49 parametri (32+8+8+1)».
- **Pattern errore / ID contesto:** Lacuna shape W2 (h,1) — rinforzo positivo (da consolidare nel cap.06 con tabella shape).

---

### 2026-05-22 — Quiz d'ingresso Q3 (`03_loss.py` ~Q3)

- **Esercizio / blocco:** Q3 — p=0.05, y=1: errore intuitivo e direzione pesi.
- **Valutazione (primo tentativo — "voto esame"):** **8/10**.
- **Punti di forza:** Direzione giusta: p troppo bassa rispetto a y=1 → serve spingere verso probabilità più alte; collegamento z/logit più alto → sigmoid più vicina a 1; ragionamento su prodotto matriciale + sigmoid coerente col forward.
- **Errori / lacune:** Manca esplicitare l'errore intuitivo ("quasi sicuro NO/genuino quando era SÌ/alterato", loss BCE alta); formula generale "aumentare tutti i pesi" è semplificata — in realtà alcuni pesi salgono e altri scendono a seconda del segno delle feature (gradiente per peso).
- **Correzione / suggerimento:** Aggiungere 1 riga sull'errore umano; per i pesi: «far salire p» / «muovere i pesi lungo il gradiente (non tutti allo stesso modo)».
- **Pattern errore / ID contesto:** — (nessuno nuovo).

**Fix applicato (stessa sessione):** aggiunta riga errore intuitivo («quasi sicuramente genuina»). **Rivalutazione post-fix: 9/10** — resta solo la sfumatura «non tutti i pesi su insieme» (ok per quiz ingresso). Da chiudere quando arriverà la chain rule nel cap.05.

---

### 2026-05-22 — Quiz d'ingresso Q2 (`03_loss.py` ~Q2)

- **Esercizio / blocco:** Q2 — pendenza di f(x)=x² in x=3 e x=-3 (spiegazione geometrica).
- **Valutazione (primo tentativo — "voto esame"):** **9/10**.
- **Punti di forza:** Concetto corretto su entrambi i punti; usa passo verso destra con f(4) e f(-2); distingue salita vs discesa; risposta coerente col grafico `03_02_pendenza_parabola_q2.png`.
- **Errori / lacune:** Refuso "andamente" → andamento; opzionale citare x=0 (pendenza zero al fondo della U) per chiudere il quadro.
- **Correzione / suggerimento:** Formulazione modello: «x=3 pendenza + (salita verso destra); x=-3 pendenza − (discesa verso destra); in x=0 pendenza 0».
- **Pattern errore / ID contesto:** — (nessuno nuovo; intuizione "pendenza" da ribadire nel cap.04 derivate).

---

### 2026-05-22 — Quiz d'ingresso Q1 (`03_loss.py` ~Q1)

- **Esercizio / blocco:** Q1 — LOSS vs ACCURACY e differenza per backpropagation.
- **Valutazione (primo tentativo — "voto esame"):** **7/10**.
- **Punti di forza:** Intuizione corretta sulla loss come distanza previsione/verità; richiama probabilità (sigmoid) e idea di "gravità" dell'errore (sicurezza sbagliata); accuracy con formula TP/TN sensata.
- **Errori / lacune:** Risposta troppo lunga (chiedeva ~1 riga per LOSS e 1 per ACCURACY); manca il punto chiave per backprop — **loss continua e derivabile** vs **accuracy discreta (non derivabile)**; "informazioni qualitative" è vago rispetto a "gradiente sui pesi".
- **Correzione / suggerimento:** LOSS = errore continuo (es. BCE su p) che minimizzi in training. ACCURACY = % predizioni giuste (soglia 0,5). Backprop usa gradienti della **loss**, non dell'accuracy.
- **Pattern errore / ID contesto:** Pattern ⚠️ "loss vs metrica" (rinforzo Sez.1 cap.03) — da chiudere quando ripete il concetto **derivabile**.

---

### 2026-05-25 — TODO 1.1 BCE manuale (`03_loss.py` ~TODO 1.1)

- **Esercizio / blocco:** TODO 1.1 — calcolo BCE media + pratica peggiore (argmax loss singole).
- **Valutazione (primo tentativo — "voto esame"):** **6/10**.
- **Punti di forza:** Indice corretto (4); uso creativo di `np.abs()` per trovare il max; commento finale giusto ("si discosta di più").
- **Errori / lacune:** (1) **Segno meno mancante** nella formula → loss negativa, non ha senso fisico; (2) non stampa `bce_mean` (il task lo chiedeva); (3) niente `eps`/clip (minore, non esplode qui).
- **Correzione / suggerimento:** BCE = **-** y*log(p) - (1-y)*log(1-p). Il `-` iniziale rende tutto positivo. `abs()` maschera il bug — con la formula corretta non serve. Sempre stampare ciò che il task chiede.
- **Pattern errore / ID contesto:** Pattern nuovo 🔴 "segno BCE" — confusione segno negativo nella formula loss. Rinforzato in TODO 1.7 dedicato (4 formule candidate). Verificare chiusura.

---

### 2026-05-25 — TODO 1.2 BCE perfetta e clip (`03_loss.py` ~TODO 1.2)

- **Esercizio / blocco:** TODO 1.2 — verificare BCE=0 con p perfette + capire perché serve eps/clip.
- **Valutazione (primo tentativo — "voto esame"):** **6/10**.
- **Punti di forza:** Caso 1 eseguito correttamente (loss ≈ 0); commento corretto nel principio; ha usato clip spontaneamente.
- **Errori / lacune:** (1) **Caso 2 non fatto** (p=y senza/con clip); (2) clip solo lato basso `(eps, 1)` → manca `1-eps` sopra; (3) non menziona `nan` (il vero output di `0 * log(0)` in NumPy, non solo -inf).
- **Correzione / suggerimento:** Clip **bilaterale** `(eps, 1-eps)`. Con p=y senza clip: `0*(-inf) = nan` in NumPy, non 0 — nan contamina tutto. Fare sempre entrambi i test.
- **Pattern errore / ID contesto:** Pattern ⚠️ "clip bilaterale" — tende a proteggere solo un lato. Rinforzato in TODO 1.8 dedicato (3 versioni di clip). Verificare chiusura.

---

### 2026-05-25 — Micro-esercizio AUC ROC (rinforzo mirato, `03_loss.py` blocco "loss vs metrica")

- **Esercizio / blocco:** Micro-esercizio AUC — accuracy vs AUC su P=[0.10,0.45,0.55,0.95], y=[0,1,0,1].
- **Valutazione (primo tentativo — "voto esame"):** **7/10**.
- **Punti di forza:** Risultati numerici corretti (accuracy=0.5, AUC=0.75); intuizione "AUC più alto" corretta; capisce che AUC usa probabilità non soglia.
- **Errori / lacune:** (1) Soglia sbagliata: `P > 0` anziché `P >= 0.5` — risultato uguale per coincidenza; (2) spiegazione AUC generica — non menziona il meccanismo di ranking (coppie pos/neg ordinate).
- **Correzione / suggerimento:** AUC = "su tutte le coppie (un positivo, un negativo), in quante il positivo ha P più alta?" → 3/4 = 0.75. Soglia accuracy standard = 0.5.
- **Pattern errore / ID contesto:** Pattern ⚠️ "soglia 0.5 dimenticata" — confonde `> 0` con `>= 0.5`. Rinforzato in TODO 1.9 dedicato. Verificare chiusura.

---

### 2026-05-27 — TODO 4.2 Forward 2-layer (recall cap.02, `03_loss.py` ~TODO 4.2)

- **Esercizio / blocco:** TODO 4.2 — ricostruire forward 2-layer e stampare shape (Z1, H, Z2, P).
- **Valutazione (primo tentativo — "voto esame"):** **8.5/10**.
- **Punti di forza:** Forward corretto (Z1 = X@W1+b1, H=ReLU, Z2=H@W2+b2, P=sigmoid(Z2).ravel()); buona scelta di riscrivere “a mano” per ripasso; uso consapevole di `clip` nella sigmoid (stabilità numerica); assert su shape coerente.
- **Errori / lacune:** (1) Scostamento dalla consegna: inizializzazione pesi con He init invece di `* 0.1` (non è sbagliato, ma non stai replicando lo stesso setup richiesto); (2) stampa shape solo di Z1 e Z2: mancavano anche H e P (la consegna chiedeva “stampa le shape” per ogni step); (3) assert verifica solo shape, non verifica che P sia davvero in (0, 1).
- **Correzione / suggerimento:** Mantieni il ripasso a mano ma rispetta il setup richiesto quando l’obiettivo è seguire una consegna “identica”; aggiungi `print(H.shape)`, `print(P.shape)` e un check tipo `assert np.all((P > 0) & (P < 1))` (o almeno min/max).
- **Pattern errore / ID contesto:** Nessun pattern nuovo. Buon rinforzo intra-M3 (forward cap.02 → loss cap.03).

---

### 2026-05-27 — TODO 4.3 Forward + BCE + accuracy (interleaving cap.02+03, `03_loss.py` ~TODO 4.3)

- **Esercizio / blocco:** TODO 4.3 — riprendere P dal forward (TODO 4.2), calcolare BCE media con `bce_loss(P, y)` e accuracy con `accuracy_score(P, y)` (soglia 0.5).
- **Valutazione (primo tentativo — "voto esame"):** **5.5/10**.
- **Punti di forza:** Formula BCE scritta correttamente (segno ok); uso della soglia 0.5 coerente; interleaving corretto (forward → loss → metrica).
- **Errori / lacune:** (1) BCE calcolata “a mano” senza clip bilaterale → rischio `log(0)`/NaN se P contiene 0 o 1; (2) chiamata a `accuracy_score` con argomenti invertiti e input già binario: `accuracy_score(y, (P>=0.5).astype(int))` invece di `accuracy_score(P, y)`; così la funzione applica una soglia su `y` (0/1) e confronta col vettore predetto, ma non è l’uso corretto richiesto dall’esercizio; (3) mancata aderenza alla consegna: l’obiettivo era usare le funzioni `bce_loss` e `accuracy_score` già definite (per solidità e consistenza col resto del capitolo).
- **Correzione / suggerimento:** Usa direttamente `bce_loss(P, y)` e `accuracy_score(P, y)`; se vuoi anche il “ripasso a mano”, fai entrambe e assert che coincidano (dopo aver fatto `p_safe = np.clip(P, eps, 1-eps)` nella versione manuale). Nota: `accuracy_score` prende probabilità P e label y, NON le predizioni binarie già thresholdate.
- **Pattern errore / ID contesto:** Ricompare ⚠️ “clip bilaterale” (manca nella BCE manuale) e ⚠️ “uso metriche vs probabilità” (confusione input di `accuracy_score`).

**Fix applicato (post-feedback, 2026-05-27):** aggiunti `BCE_tool = bce_loss(P, y)` + clip bilaterale (`P_safe = np.clip(...)`) + `BCE_manual` + assert di coerenza. **Post-fix: 8.5/10** (restano solo finezze: usare `accuracy_score(P, y)` invece di passare già binari; allineare `eps` con quello del tool o usare `np.isclose(..., atol=...)`; stampare anche l’accuracy).

## Lacune e dubbi ancora aperti (a inizio cap.03 LOSS dopo split)

- 🔴 **Segno BCE:** corretto dopo feedback in TODO 1.1; rinforzo programmato in TODO 1.7. Chiudere a fine cap.03.
- ⚠️ **Clip bilaterale:** tende a proteggere solo il lato basso; rinforzo programmato in TODO 1.8. Chiudere a fine cap.03.
- ⚠️ **Soglia 0.5:** confonde `P > 0` con `P >= 0.5` nel calcolo accuracy; rinforzo programmato in TODO 1.9. Chiudere a fine cap.03.
- ⚠️ **Pattern "exists check"**: dimenticato in TODO 2.3 del vecchio file (vedi diario M03_C04_derivate_gradiente_sessione.md). Inserire 1 micro-promemoria in correzione TODO 1.3.

---

## Note per il capitolo successivo (mentor)

- I 3 pattern (segno BCE, clip bilaterale, soglia 0.5) devono essere chiusi PRIMA di passare al cap.04. Se a fine cap.03 sono ancora ⚠️, ripeterli nel bridge `M03_R03_after_C03_before_C04_loss_to_derivate.md` come mini-esercizi obbligatori.
- Il cap.03 LOSS dovrebbe risultare "facile" rispetto al vecchio cap.03 monolitico (atteso 6-7/10). Se voto > 7, segnale che la difficolta' del cap.04 puo' essere mantenuta come pianificato. Se voto < 5, segnale che lo split e' stato troppo conservativo e si puo' accelerare nel cap.04.
- Il bridge `M03_R02_after_C02_before_C03_reti_to_loss.md` resta valido (gia' fatto da Gianluca? verificare in chat).
- Dopo la chiusura del cap.03 LOSS, popolare il bridge `M03_R03_after_C03_before_C04_loss_to_derivate.md` (attualmente placeholder).
