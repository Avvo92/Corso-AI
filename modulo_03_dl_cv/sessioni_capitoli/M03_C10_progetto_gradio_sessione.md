# Diario sessione — Capitolo 10 — Gradio + deploy HF Spaces

| Campo | Valore |
|-------|--------|
| **Modulo** | M03 — Deep Learning & Computer Vision |
| **File capitolo** | `10_progetto_gradio.py` |
| **File diario** | `M03_C10_progetto_gradio_sessione.md` |
| **Stato** | in corso (aperto 14/09/2026 alla chiusura C09; capitolo esteso il 14/09/2026) |
| **Voto difficoltà** | — |

---

## Obiettivi del capitolo (per il mentor)

Il capitolo è stato **riscritto ed esteso** il 14/09/2026 su richiesta dello
studente ("troppo snello, importante per creare reti di facile riutilizzo").
Il filo conduttore è: *un file `.pt` non è un modello, è un sacco di numeri;
diventa un modello quando lo accompagna il contratto che dice come si usa.*

**Asse 1 — riuso del modello** (Sez. 1-2)
- Contratto di inferenza in 6 voci (architettura, classi ordinate, dimensione
  input, mean/std, soglia, versione) e il danno che fa ognuna se manca.
- Punto chiave didattico: 5 voci su 6, se sbagliate, **non** danno eccezione.
  Il caso principe è l'ordine delle classi invertito (Sez. 1.3).
- Checkpoint ricco: `salva_checkpoint` / `carica_checkpoint`, le tre strade di
  salvataggio, `strict` e le chiavi Missing/Unexpected, `weights_only`.

**Asse 2 — riuso del codice** (Sez. 3, 9)
- `costruisci_modello` (chiude il residuo TODO 2 di C09: `getattr` + pesi
  `"DEFAULT"` come stringa + `fc.in_features` letto dal modello).
- `transform_eval` con i parametri **derivati dal contratto**, non hardcoded.
- Classe `ClassificatoreVisivo` con caricamento pigro e una sola istanza;
  nessun `print`, nessuna dipendenza da Gradio → riusabile da FastAPI (Sez. 9).

**Gradio e deploy** (Sez. 4-8)
- Anatomia `Interface`/`Blocks`, componenti tipizzati (`type="pil"` e perché),
  `gr.Label` con dizionario, `Examples` e privacy, parametri di `launch()`.
- `predict` end-to-end: `convert("RGB")`, `Normalize`, `unsqueeze(0)`,
  softmax vs argmax, applicazione della soglia scelta in C09.
- `app.py` in 4 blocchi (config / modello / core / interfaccia) con il test
  "se togli Gradio, quante righe riscrivi?".
- Spaces: front-matter YAML, requirements pinnati, torch CPU, git-lfs vs
  `hf_hub_download`, cold start, i 4 errori tipici build/runtime.
- Smoke test in 8 punti, model card come contratto in forma umana, p50/p95.

**Residui C09 chiusi con blocchi 🔁**: #48 (tre leve), #52 (decomposizione
matmul), #53 (obiezione ancorata), Pattern #6 (formato consegne), avgpool
come imbuto a vettore fisso.

Restano fermi: 🔄 CONFRONTO PRIMA/DOPO (fine modulo), URL Portfolio #2,
debito C1-C8 buste → `busta_vs_altro.pt`.

---

## Prerequisiti

- [ ] Bridge `M03_R09_after_C09_before_C10_transfer_to_gradio.md` (+ micro 09.A–E)
- [ ] `.pt` track prova disponibile (locale o da scaricare da Colab)
- [ ] Account HuggingFace per Spaces
- [ ] ⚠️ `torchvision` **non** è installato nell'ambiente locale (`venv`):
      serve per eseguire `costruisci_modello` / `transform_eval` in Sez. 3.
      Da installare prima di iniziare, oppure lavorare sulla parte teorica.

---

## Domande durante lo studio

### 2026-09-14 — Cos’è Dropout?
- Chiaro dopo spiegazione: spegnimento casuale neuroni in **training** (anti-overfitting); in **`eval()`** non spegne nessuno.
- Collegato a #48: `eval()` tocca Dropout **e** BatchNorm; distinto da freeze e da `no_grad()`.

---

## Valutazioni esercizi / quiz / mini-esercizi

### 2026-09-14 — Quiz ingresso Q1 (`10_progetto_gradio.py`, lacuna #48)
- **Voto (1° tentativo): 7/10**
- **OK:** formato 2 bullet rispettato; `eval()` → modalità valutazione + BatchNorm con buffer; `no_grad()` → niente grafo / risparmio memoria.
- **Manca:** per ciascuna leva il pezzo **NON FA** (consegna esplicita). Su `eval()`: non congela i pesi, non spegne autograd; su `no_grad()`: non cambia Dropout/BatchNorm. Soft: “scalare i dati” impreciso; manca Dropout accanto a BN.
- **Next:** rileggere 🔁 #48 (analogia tre leve) e rifare Mini 48.A (V/F) — lì il NON FA è obbligatorio.
- **Lacune:** #48 resta 🟡 (FA ok, NON FA soft — stesso pattern C09 Mini 5.3).

---

## Lacune e dubbi ancora aperti

Ereditate da C09 da verificare qui:

- 🟡 **#48** — `eval` / `no_grad` / freeze (tre leve) → 🔁 + Q1 + Sez. 3.4 + V6
- 🟡 **#52** — decomposizione matmul + `in_features` → 🔁 + Q2 + Sez. 3.1 + TODO 4
- 🟡 **#53** — obiezione numerica (Mini 6.2 style) → 🔁 + Q4 + Mini 8.2
- 🔴 **Pattern #6** — formato consegne (quasi ogni consegna del cap.10 dichiara
  il formato atteso: numero di bullet/righe. Serve a misurare il pattern)
- 📌 Debito prodotto C1–C8 buste

---

## Note per fine modulo (mentor)

- Aggiornare Portfolio URL #2; protocollo FINE MODULO (archivio M3, scommentare M4 in requirements).
- Passo 13 solo a chiusura di **questo** capitolo, non di C09.
- Nota tecnica emersa scrivendo il capitolo: da PyTorch 2.6 `torch.load` usa
  `weights_only=True` per default, quindi nel checkpoint ricco vanno **solo**
  tipi base (`str(torch.__version__)`, non l'oggetto `TorchVersion`).
  Il caso è documentato in Sez. 2.6 con l'errore reale.
