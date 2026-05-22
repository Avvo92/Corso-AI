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

### [YYYY-MM-DD] — Riferimento (placeholder)

- **Esercizio / blocco:** …
- **Valutazione (primo tentativo — "voto esame"):** **X/10**.
- **Punti di forza:** …
- **Errori / lacune:** …
- **Correzione / suggerimento:** …
- **Pattern errore / ID contesto** (se applicabile): …

---

## Lacune e dubbi ancora aperti

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
