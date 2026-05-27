# Diario sessione — Capitolo 06 — Backpropagation + Training

| Campo | Valore |
|-------|--------|
| **Modulo** | M03 — Deep Learning & Computer Vision |
| **File capitolo** | `06_backprop_training.py` (segnaposto al 27/05/2026) |
| **File diario** | `M03_C06_backprop_training_sessione.md` |
| **Stato** | da aprire dopo chiusura cap.05 |
| **Voto difficoltà** | — / X/10 (atteso 8/10 dopo split, era 9/10 nel vecchio monolitico) |

---

## Obiettivi del capitolo (per il mentor — da affinare a chiusura cap.05)

- Mettere insieme tutto: forward (con cache) + loss (cap.03) + chain rule (cap.05) + gradient descent (cap.05) APPLICATI alla rete 2-layer del cap.02.
- Sanity check OBBLIGATORIO: gradiente analitico VS gradiente numerico (per dW1[0, 0]) — se differiscono > 1e-4 c'e' un bug.
- Far girare il **mini-progetto**: rete 2-layer addestrata sul CSV M2 che pareggia/batte LogisticRegression M2 cap.04.
- Inserire `🔄 CONFRONTO PRIMA/DOPO` (chiusura "primo blocco" full-NumPy cap.01-06, ANTICIPATO rispetto al fine modulo - cap.10).

---

## Strategia didattica (da affinare)

- Sequenza per OGNI concetto: **analogia concreta -> codice -> grafico -> formula in parole**.
- Le SHAPE di `dW1, db1, dW2, db2, dZ1, dZ2` devono essere VISIBILI in ogni passaggio (meta' dei bug di backprop sono shape mismatch).
- Se a meta' capitolo lo studente e' bloccato -> STOP, mini-recap dedicato.
- ⚠️ Capitolo difficile - andare lenti.

---

## Domande durante lo studio

- _(da popolare)_

---

## Valutazioni esercizi / quiz / mini-esercizi

> Voto = "primo tentativo".

_(Nessuna valutazione ancora — capitolo da aprire.)_

---

## Lacune e dubbi ancora aperti

- _(da popolare)_

---

## Note per il capitolo successivo (cap.07 PyTorch)

- Verificare che il sanity check numerico delle derivate (TODO 6.1 vecchio) sia stato fatto e funzioni. E' il check piu' importante prima di passare a PyTorch.
- Verificare che il mini-progetto su CSV M2 abbia raggiunto i target (loss < 0.3, accuracy paragonabile a LogReg).
- Preparare un notebook Colab con setup `torch + torchvision`, `device = "cuda" if available else "cpu"`, e mostrare che il training loop "vero" (PyTorch) e' lo STESSO concettuale di questo capitolo (forward -> loss -> backward -> update), solo che il backward lo fa autograd automaticamente.
- Mostrare anche il **confronto tempi**: training loop manuale (NumPy) vs `torch.optim.SGD` -> 10-50x piu' veloce in PyTorch su GPU, "ma con piu' magia nascosta".
