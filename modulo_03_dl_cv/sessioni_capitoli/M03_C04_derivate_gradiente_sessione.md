# Diario sessione — Capitolo 04 — Derivate e Gradiente

| Campo | Valore |
|-------|--------|
| **Modulo** | M03 — Deep Learning & Computer Vision |
| **File capitolo** | `04_derivate_gradiente.py` (segnaposto al 27/05/2026) |
| **File diario** | `M03_C04_derivate_gradiente_sessione.md` |
| **Stato** | da aprire dopo chiusura cap.03 LOSS |
| **Voto difficoltà** | — / X/10 (atteso 6-7/10 dopo split) |

---

## ⚠️ Note sullo split (27/05/2026)

Le valutazioni di alcuni esercizi qui sotto sono state migrate dal vecchio diario `M03_C03_backpropagation_sessione.md` (capitolo monolitico, poi splittato in 4). Sono i TODO che riguardavano la sezione DERIVATA del vecchio file (Sez.2 originale).

---

## Obiettivi del capitolo (per il mentor — da affinare a chiusura cap.03)

- Far interiorizzare **derivata = pendenza** in codice, grafico, parole (NIENTE limiti formali).
- Introdurre il **gradiente come "lista di derivate parziali"** (= vettore).
- Mostrare la **derivata della sigmoid** `s(z) * (1 - s(z))` e farne capire il massimo (0.25) come anticipazione del vanishing gradient.
- Inserire rinforzi cap.01-02 (vettori come liste di coordinate, ReLU come step function).

---

## Strategia didattica (da affinare)

- Sequenza per OGNI concetto matematico: **analogia concreta -> codice Python -> grafico -> formula in parole**.
- Niente LaTeX.
- Se il cap.03 LOSS ha lasciato lacune aperte (segno BCE, clip, soglia), inserire blocchi `🔁 RINFORZO MIRATO` qui.

---

## Domande durante lo studio

- _(da popolare quando il capitolo verra' aperto)_

---

## Valutazioni esercizi / quiz / mini-esercizi

> Voto = "primo tentativo".

### 2026-05-25 — TODO 2.1 derivata sigmoid numerica vs analitica (`04_derivate_gradiente.py` ~TODO sigmoid)

> ⚠️ MIGRATA dal vecchio `03_backpropagation.py` (Sez.2 monolitico).

- **Esercizio / blocco:** TODO 2.1 — confronto derivata sigmoid (funzioni proprie). Riferimento storico: vecchio `03_backpropagation.py` righe ~608-639.
- **Valutazione (primo tentativo post-fix — "voto esame"):** **9/10**.
- **Punti di forza:** Formula numerica corretta (`/ 2h`); analitica `s*(1-s)` corretta; tutti i 5 punti z coincidono (es. z=0 → 0.25); `assert np.isclose` ottimo; `h=1e-6` passato esplicitamente.
- **Errori / lacune:** (1) type hint `Callable[[float, float]]` → dovrebbe essere `Callable[[float], float]`; (2) default `h=1e-12` in firma ma usa 1e-6 in chiamata — allineare; (3) `sigmoid` chiamata 2 volte nell'analitica (minore).
- **Correzione / suggerimento:** `s = sigmoid(z_safe); return s * (1 - s)` — una sola chiamata.
- **Pattern errore / ID contesto:** — (primo TODO derivate OK dopo fix divisione/precedenza).

---

### 2026-05-27 — TODO 2.3 grafico funzione+derivata (`04_derivate_gradiente.py` ~TODO grafico)

> ⚠️ MIGRATA dal vecchio `03_backpropagation.py` (Sez.2 monolitico).

- **Esercizio / blocco:** Generare PNG `figures/03_02_derivata.png` e (richiesto) verificare esistenza file. Riferimento storico: vecchio `03_backpropagation.py` righe ~651-672.
- **Valutazione (primo tentativo — "voto esame"):** **8/10**.
- **Punti di forza:** `os.makedirs(...)` presente; plot creato con `fig, ax`; `plt.savefig(out_path, ...)` salva correttamente (file effettivamente presente).
- **Errori / lacune:** non implementa la parte richiesta di "verifica esistenza file" (`os.path.exists` + print/flag); inoltre salva con `plt.savefig` invece di `fig.savefig` (minore, ma più pulito).
- **Correzione / suggerimento:** dopo `savefig`, fai `exists = os.path.exists(out_path)` e stampa/`assert exists`.
- **Pattern errore / ID contesto:** ⚠️ "consegna salva ma manca exists check". Rinforzato in TODO 1.3 del nuovo `03_loss.py` (ora corretto con `assert file_created`).

---

## Lacune e dubbi ancora aperti

- _(da popolare quando il capitolo verra' aperto)_

---

## Note per il capitolo successivo (cap.05 chain rule + gd)

- _(da popolare a chiusura del cap.04)_
