# Diario sessione — Capitolo 03 — Backpropagation e training

| Campo | Valore |
|-------|--------|
| **Modulo** | M03 — Deep Learning & Computer Vision |
| **File capitolo** | `03_backpropagation.py` |
| **File diario** | `M03_C03_backpropagation_sessione.md` |
| **Stato** | in corso |
| **Voto difficoltà** | — / X/10 (atteso **9/10** — capitolo PIU' TOSTO del modulo) |

---

## Obiettivi del capitolo (per il mentor)

- Far capire **cos'e' una LOSS** (BCE vs MSE — perche' BCE per classificazione binaria) come **misura continua e derivabile**.
- Tradurre **derivata = pendenza** e **gradiente = vettore di pendenze** in codice + grafico PRIMA della formula.
- Introdurre la **chain rule** con un esempio numerico, poi mostrarla **applicata a una rete 2-layer**.
- Implementare **gradient descent generico** (su paraboloide) e farne vedere l'effetto del **learning rate** (3 lr a confronto, grafico).
- Implementare **backward 2-layer** in NumPy puro (chain rule + derivate di ReLU e sigmoid) + training loop completo (forward -> loss -> backward -> update).
- Sanity check OBBLIGATORIO: gradiente analitico VS gradiente numerico (per dW1[0, 0]) — se differiscono > 1e-4 c'e' un bug.
- Far girare il **mini-progetto**: rete 2-layer addestrata sul CSV M2 che pareggia/batte LogisticRegression M2 cap.04.

---

## Strategia didattica (regola 21 — obbligatoria qui)

- Sequenza per OGNI concetto matematico: **analogia concreta -> codice Python -> grafico -> formula in parole**.
- **Niente LaTeX**, niente notazione compressa.
- Se a meta' capitolo lo studente e' bloccato -> **STOP**, mini-recap in una sessione dedicata, non proseguire alla cieca.
- Le SHAPE di `dW1, db1, dW2, db2, dZ1, dZ2` devono essere visibili in ogni passaggio (meta' dei bug di backprop sono shape mismatch).

---

## Promemoria specifici dal cap.02 M3 (mentor)

- **Bridge ripasso** `M03_R02_after_C02_before_C03_reti_to_backprop.md` deve essere fatto **prima** di aprire la teoria del cap.03 (~10 min, 10 esercizi facili).
- **Lacuna #31 UAT** (🟡): inserito blocco `# 🔁 RINFORZO MIRATO` dopo i Quiz d'ingresso ("UAT: esistenza vs come la trovi"). Verificare in correzione se il concetto e' chiuso (→ 🟢).
- **Pattern ⚠️ "loss vs metrica"** (cap.02 mini-progetto, AUC su 0/1): inserito blocco `# 🔁 RINFORZO MIRATO` a fine Sez.1 ("LOSS per addestrare, METRICA per giudicare"). Da richiamare anche in correzione mini-progetto.
- **Shape `W2 (h, 1)`** (E1 cap.02): inserito blocco `# 🔁 RINFORZO MIRATO` a inizio Sez.6, prima di `forward_2layer`. Da pretendere precisa nelle prossime risposte (Q4 d'ingresso, V7 di verifica, C4 finale).
- **AUC su probabilita'** (cap.02 mini-progetto): aggiunto rinforzo nel blocco "MINI-PROGETTO" prima del "TUO CODICE QUI" con esempio sklearn `predict_proba`.
- **Pattern #6 (consegne)** e **#21 (tuple/round)**: niente blocco dedicato. Richiamarli in correzione se ricompaiono (specialmente nel mini-progetto e in E1).
- **E6 cap.02 (REAL-WORLD)** rinviato dallo studente: programmarlo come **mock system design** a meta'/fine M3 (idealmente fra cap.06 transfer learning e cap.07 Gradio), NON in coda al cap.03.

---

## Domande durante lo studio

- _(da popolare durante il capitolo)_

---

## Valutazioni esercizi / quiz / mini-esercizi

> **Regole di registrazione (promemoria mentor):**
> - Voto = "primo tentativo" (esame); le correzioni successive si annotano come "Fix applicato" con nuovo voto solo se l'utente lo richiede esplicitamente.
> - Riferimento puntuale al blocco/righe del file `03_backpropagation.py`.
> - Collegare ogni lacuna emersa al suo ID in `CONTESTO_CORSO.md`.

### 2026-05-22 — Rinforzo UAT micro-esercizio (`03_backpropagation.py` ~236-241)

- **Esercizio / blocco:** Micro-esercizio post-blocco UAT — cosa cambia dopo training (architettura / pesi / input / sigmoid).
- **Valutazione (primo tentativo — "voto esame"):** **10/10**.
- **Punti di forza:** Risposta (b) corretta: training aggiorna i pesi; architettura, input e sigmoid restano gli stessi.
- **Errori / lacune:** —
- **Correzione / suggerimento:** Lacuna #31 UAT (esistenza vs training) — segno positivo; chiudere in contesto se ripetuto a fine Sez.6.
- **Pattern errore / ID contesto:** Lacuna #31 UAT 🟡 — progresso.

---

### 2026-05-22 — Quiz d'ingresso Q5 Feynman (`03_backpropagation.py` ~205-209)

- **Esercizio / blocco:** Q5 — loop di training senza jargon (4 righe max).
- **Valutazione (primo tentativo — "voto esame"):** **8/10**.
- **Punti di forza:** Ciclo completo forward → confronto p vs y → errore → correzione «all'indietro» per parametro → ripeti; nessuna parola vietata; binario e probabilità chiari; tono da collega tecnico ma comprensibile.
- **Errori / lacune:** Non rispetta «4 righe» (testo lungo, ~6 frasi); «livelli di parametri» un po' ambiguo per web dev; manca analogia semplice (manopole / tentativi su dataset) come nella soluzione tipo.
- **Correzione / suggerimento:** Comprimere in 4 righe; es. «provi su N esempi → misuri errore → aggiusti le manopoline → ripeti finché sbagli meno».
- **Pattern errore / ID contesto:** Feynman — ok concettualmente; formato vincoli da stringere.

---

### 2026-05-22 — Quiz d'ingresso Q4 (`03_backpropagation.py` ~200-203)

- **Esercizio / blocco:** Q4 — conteggio parametri W1 (4,8), W2 (8,1) + bias.
- **Valutazione (primo tentativo — "voto esame"):** **10/10**.
- **Punti di forza:** Scomposizione corretta (32+8+8+1); totale 49; include b1 e b2 nel conteggio.
- **Errori / lacune:** Label «49 pesi» — in rigore sono **49 parametri** (pesi + bias); calcolo già corretto.
- **Correzione / suggerimento:** Opzionale: «49 parametri (32+8+8+1)».
- **Pattern errore / ID contesto:** Lacuna shape W2 (h,1) — rinforzo positivo.

---

### 2026-05-22 — Quiz d'ingresso Q3 (`03_backpropagation.py` ~194-198)

- **Esercizio / blocco:** Q3 — p=0.05, y=1: errore intuitivo e direzione pesi.
- **Valutazione (primo tentativo — "voto esame"):** **8/10**.
- **Punti di forza:** Direzione giusta: p troppo bassa rispetto a y=1 → serve spingere verso probabilità più alte; collegamento z/logit più alto → sigmoid più vicina a 1; ragionamento su prodotto matriciale + sigmoid coerente col forward.
- **Errori / lacune:** Manca esplicitare l'errore intuitivo ("quasi sicuro NO/genuino quando era SÌ/alterato", loss BCE alta); formula generale "aumentare tutti i pesi" è semplificata — in realtà alcuni pesi salgono e altri scendono a seconda del segno delle feature (gradiente per peso).
- **Correzione / suggerimento:** Aggiungere 1 riga sull'errore umano; per i pesi: «far salire p» / «muovere i pesi lungo il gradiente (non tutti allo stesso modo)».
- **Pattern errore / ID contesto:** — (nessuno nuovo).

**Fix applicato (stessa sessione):** aggiunta riga errore intuitivo («quasi sicuramente genuina»). **Rivalutazione post-fix: 9/10** — resta solo la sfumatura «non tutti i pesi su insieme» (ok per quiz ingresso).

---

### 2026-05-22 — Quiz d'ingresso Q2 (`03_backpropagation.py` ~187-192)

- **Esercizio / blocco:** Q2 — pendenza di f(x)=x² in x=3 e x=-3 (spiegazione geometrica).
- **Valutazione (primo tentativo — "voto esame"):** **9/10**.
- **Punti di forza:** Concetto corretto su entrambi i punti; usa passo verso destra con f(4) e f(-2); distingue salita vs discesa; risposta coerente col grafico `03_02_pendenza_parabola_q2.png`.
- **Errori / lacune:** Refuso "andamente" → andamento; opzionale citare x=0 (pendenza zero al fondo della U) per chiudere il quadro.
- **Correzione / suggerimento:** Formulazione modello: «x=3 pendenza + (salita verso destra); x=-3 pendenza − (discesa verso destra); in x=0 pendenza 0».
- **Pattern errore / ID contesto:** — (nessuno nuovo).

---

### 2026-05-22 — Quiz d'ingresso Q1 (`03_backpropagation.py` ~179-185)

- **Esercizio / blocco:** Q1 — LOSS vs ACCURACY e differenza per backpropagation.
- **Valutazione (primo tentativo — "voto esame"):** **7/10**.
- **Punti di forza:** Intuizione corretta sulla loss come distanza previsione/verità; richiama probabilità (sigmoid) e idea di "gravità" dell'errore (sicurezza sbagliata); accuracy con formula TP/TN sensata.
- **Errori / lacune:** Risposta troppo lunga (chiedeva ~1 riga per LOSS e 1 per ACCURACY); manca il punto chiave per backprop — **loss continua e derivabile** vs **accuracy discreta (non derivabile)**; "informazioni qualitative" è vago rispetto a "gradiente sui pesi".
- **Correzione / suggerimento:** LOSS = errore continuo (es. BCE su p) che minimizzi in training. ACCURACY = % predizioni giuste (soglia 0,5). Backprop usa gradienti della **loss**, non dell'accuracy.
- **Pattern errore / ID contesto:** Pattern ⚠️ "loss vs metrica" (rinforzo Sez.1 cap.03) — da chiudere quando ripete il concetto **derivabile**.

---

### 2026-05-25 — TODO 1.1 BCE manuale (`03_backpropagation.py` ~372-390)

- **Esercizio / blocco:** TODO 1.1 — calcolo BCE media + pratica peggiore (argmax loss singole).
- **Valutazione (primo tentativo — "voto esame"):** **6/10**.
- **Punti di forza:** Indice corretto (4); uso creativo di `np.abs()` per trovare il max; commento finale giusto ("si discosta di più").
- **Errori / lacune:** (1) **Segno meno mancante** nella formula → loss negativa, non ha senso fisico; (2) non stampa `bce_mean` (il task lo chiedeva); (3) niente `eps`/clip (minore, non esplode qui).
- **Correzione / suggerimento:** BCE = **-** y*log(p) - (1-y)*log(1-p). Il `-` iniziale rende tutto positivo. `abs()` maschera il bug — con la formula corretta non serve. Sempre stampare ciò che il task chiede.
- **Pattern errore / ID contesto:** Pattern nuovo 🔴 "segno BCE" — confusione segno negativo nella formula loss. Da verificare in TODO successivi e nel backward.

---

### 2026-05-25 — TODO 1.2 BCE perfetta e clip (`03_backpropagation.py` ~392-409)

- **Esercizio / blocco:** TODO 1.2 — verificare BCE=0 con p perfette + capire perché serve eps/clip.
- **Valutazione (primo tentativo — "voto esame"):** **6/10**.
- **Punti di forza:** Caso 1 eseguito correttamente (loss ≈ 0); commento corretto nel principio; ha usato clip spontaneamente.
- **Errori / lacune:** (1) **Caso 2 non fatto** (p=y senza/con clip); (2) clip solo lato basso `(eps, 1)` → manca `1-eps` sopra; (3) non menziona `nan` (il vero output di `0 * log(0)` in NumPy, non solo -inf).
- **Correzione / suggerimento:** Clip **bilaterale** `(eps, 1-eps)`. Con p=y senza clip: `0*(-inf) = nan` in NumPy, non 0 — nan contamina tutto. Fare sempre entrambi i test.
- **Pattern errore / ID contesto:** Pattern ⚠️ "clip bilaterale" — tende a proteggere solo un lato.

---

### 2026-05-25 — Micro-esercizio AUC ROC (rinforzo mirato, `03_backpropagation.py` ~470-483)

- **Esercizio / blocco:** Micro-esercizio AUC — accuracy vs AUC su P=[0.10,0.45,0.55,0.95], y=[0,1,0,1].
- **Valutazione (primo tentativo — "voto esame"):** **7/10**.
- **Punti di forza:** Risultati numerici corretti (accuracy=0.5, AUC=0.75); intuizione "AUC più alto" corretta; capisce che AUC usa probabilità non soglia.
- **Errori / lacune:** (1) Soglia sbagliata: `P > 0` anziché `P >= 0.5` — risultato uguale per coincidenza; (2) spiegazione AUC generica — non menziona il meccanismo di ranking (coppie pos/neg ordinate).
- **Correzione / suggerimento:** AUC = "su tutte le coppie (un positivo, un negativo), in quante il positivo ha P più alta?" → 3/4 = 0.75. Soglia accuracy standard = 0.5.
- **Pattern errore / ID contesto:** Pattern ⚠️ "soglia 0.5 dimenticata" — confonde `> 0` con `>= 0.5`.

---

## Lacune e dubbi ancora aperti

- 🔴 **Segno BCE:** (dal TODO 1.1) manca il `-` davanti → corretto dopo feedback.
- ⚠️ **Clip bilaterale:** tende a proteggere solo il lato basso, dimenticando `1 - eps` sopra.
- ⚠️ **Soglia 0.5:** confonde `P > 0` con `P >= 0.5` nel calcolo accuracy.
- _(da popolare durante il capitolo — capitolo difficile, prevedere molte iterazioni)_

---

## Note per il capitolo successivo (mentor)

- Se il TODO 6.1 (sanity check numerico delle derivate) **NON funziona al primo tentativo**, fermarsi e rifare con lo studente. E' il check piu' importante del capitolo.
- Se la rete non scende sotto loss 0.3 sul CSV M2: probabili cause da investigare in ordine — (1) `lr` sbagliato, (2) bug nel backward (shape!), (3) iter troppe poche, (4) X non scalato.
- Verificare che il mini-progetto sia **deployabile come notebook Colab** (regola hardware M3): la GPU non serve qui, ma la struttura va testata in Colab prima del cap.04 M3 dove PyTorch arriva davvero.
- Per il cap.04 M3 (PyTorch): preparare un notebook con setup `torch + torchvision`, `device = "cuda" if available else "cpu"`, e mostrare che il training loop "vero" (PyTorch) e' lo STESSO concettuale di questo capitolo (forward -> loss -> backward -> update), solo che il backward lo fa autograd automaticamente.
- Mostrare anche il **confronto tempi**: training loop manuale vs `torch.optim.SGD` -> 10-50x piu' veloce in PyTorch su GPU, "ma con piu' magia nascosta".

---

## Note tecniche di stesura (mentor)

- _(da popolare quando il capitolo verra' aperto e lavorato)_
