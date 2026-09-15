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

### 2026-09-15 — Domanda: non ricordo i 4 passi preprocess ResNet (Q5)
- Ricostruita la pipeline: Resize → CenterCrop → ToTensor → Normalize(ImageNet).
- Nota: `convert("RGB")` sta *prima* (gestione canali), non è uno dei 4 del tensore “ImageNet-ready”.

### 2026-09-15 — Quiz ingresso Q5 (`10_progetto_gradio.py`, preprocess) — **post-feedback**
- **Voto contenuto: 10/10** — ordine corretto: `Resize(256)` → `CenterCrop(224)` → `ToTensor()` → `Normalize(mean, std)`.
- **Nota esame:** non è retrieval a freddo (aveva chiesto ripasso subito prima). Per il diario: assimilazione dopo spiegazione OK; verifica a freddo possibile su Mini 5.x / Sez. 5.
- **Bonus non richiesto:** poteva citare mean/std ImageNet; non necessario per la consegna.
- **Lacune:** nessuna nuova; Q5 chiusa sul merito assistito.

### 2026-09-15 — Quiz ingresso Q6 (`10_progetto_gradio.py`, map_location)
- **Voto (1° tentativo): 8.5/10**
- **OK:** `map_location=device` con `cuda if available else cpu`; pattern portabile corretto per il caso “Colab GPU → PC senza CUDA” (su PC diventa `"cpu"`).
- **Soft:** il *perché* preciso (i tensori portano etichetta `cuda:0` e senza remap torch tenta di riallocarli su GPU assente) è solo accennato (“posto giusto”). Nella Q secca bastava anche `map_location="cpu"`.
- **Nota cap.10:** se il file è un checkpoint ricco, `torch.load` torna un dict → poi `load_state_dict(pacchetto["model_state"])`; la Q6 testa solo `map_location`.
- **Lacune:** nessuna; #46 confermata operativa.

### 2026-09-15 — Quiz ingresso Q7 (`10_progetto_gradio.py`, soglia → recall/precision)
- **Voto (1° tentativo): 5/10**
- **OK:** abbassare soglia → più spesso classe positiva (“busta”); ↑ FP → ↓ precision. Idea del trade-off c’è.
- **ERRORE:** meno FN ⇒ la **recall SALE** (TP/(TP+FN)), non scende. Ha invertito il verso della recall.
- **Lessico:** “più severo” è al contrario — soglia più bassa = più **permissivo** sulla positiva; “severo” = soglia alta.
- **Lacune:** soglia/recall da rinforzare (ripasso formula recall); non è #53 ma concetto affine a Mini soglie C09.
- **Next:** riscrivere Q7 in 2 righe: ↓ soglia → ↑ recall, ↓ precision + perché (più TP pescati, più FP in mezzo).

### 2026-09-15 — Quiz ingresso Q7 — **post-feedback**
- **Voto post-fix: 9/10** (1° resta **5**/10 come voto esame)
- **OK:** ora FN ↓ → **recall ↑**; FP ↑ → precision ↓; più spesso “busta”. Trade-off corretto.
- **Soft residuo:** resta “più severo” — andrebbe “più permissivo / sensibile” sulla positiva.
- **Fix applicato:** verso della recall corretto.
- **Lacune:** soglia/recall → 🟡 soft lessico; concetto numerico OK.

---

## Valutazioni esercizi / quiz / mini-esercizi

### 2026-09-14 — Quiz ingresso Q1 (`10_progetto_gradio.py`, lacuna #48)
- **Voto (1° tentativo): 7/10**
- **OK:** formato 2 bullet rispettato; `eval()` → modalità valutazione + BatchNorm con buffer; `no_grad()` → niente grafo / risparmio memoria.
- **Manca:** per ciascuna leva il pezzo **NON FA** (consegna esplicita). Su `eval()`: non congela i pesi, non spegne autograd; su `no_grad()`: non cambia Dropout/BatchNorm. Soft: “scalare i dati” impreciso; manca Dropout accanto a BN.
- **Next:** rileggere 🔁 #48 (analogia tre leve) e rifare Mini 48.A (V/F) — lì il NON FA è obbligatorio.
- **Lacune:** #48 resta 🟡 (FA ok, NON FA soft — stesso pattern C09 Mini 5.3).

### 2026-09-15 — Quiz ingresso Q2 (`10_progetto_gradio.py`, AdaptiveAvgPool / residuo C09)
- **Voto (1° tentativo): 9.5/10**
- **OK:** 512 come dimensione del vettore; meccanismo avgpool H×W→1×1; esempi (8,512,10,10) e (8,512,7,7) → flatten (8,512); spiega perché 320×320 non rompe `Linear(512,2)`.
- **Soft:** poteva aprire con “512 numeri” secco; typo “se se”. Il pezzo “in_features = canali, non risoluzione” c’è in sostanza.
- **Lacune:** residuo avgpool→512 da C09 **chiuso sul merito**; #52 (decomposizione matmul con batch esplicito) resta da verificare su Mini 52.A.

### 2026-09-15 — Quiz ingresso Q3 (`10_progetto_gradio.py`, ImageFolder / ordine classi)
- **Voto (1° tentativo): 9.5/10**
- **OK:** `ants→0`, `bees→1`; motivo = ordine **alfabetico** delle cartelle (ImageFolder). Concetto critico per Sez. 1.3 (bug etichette invertite) già a posto.
- **Soft:** forma dizionario esplicita `{"ants": 0, "bees": 1}` sarebbe più “colloquio-ready”; contenuto equivalente.
- **Lacune:** nessuna nuova.

### 2026-09-15 — Quiz ingresso Q4 (`10_progetto_gradio.py`, lacuna #53 obiezione numerica)
- **Voto (1° tentativo): 8.5/10**
- **OK:** numeri veri (45; scenario 40/45 → ~90% se predici sempre la maggioranza); collega accuracy alta + recall bassa a sbilanciamento; non resta sulla frase generica “accuracy non basta”.
- **Soft:** 40/45 = 88.9% (ha detto ~90%, ok); poteva aggiungere volatilità 1/45≈2.2 punti oppure un conteggio FN esplicito; costo di dominio (busta persa) opzionale ma da colloquio.
- **Lacune:** #53 → 🟡→ quasi 🟢 (forte miglioramento vs Mini 6.2 C09 5/10). Consolidare su Mini 8.2 model card.

---

## Lacune e dubbi ancora aperti

Ereditate da C09 da verificare qui:

- 🟡 **#48** — `eval` / `no_grad` / freeze (tre leve) → 🔁 + Q1 + Sez. 3.4 + V6
- 🟡 **#52** — decomposizione matmul + `in_features` → 🔁 + Mini 52.A + TODO 4 (Q2 ha chiuso la parte avgpool→512)
- 🟢 **avgpool → vettore 512** — Q2 9.5/10 (15/09): meccanismo + esempi shape OK
- 🟡 **Soglia/recall** — Q7 **5**/10: ↓ soglia ⇒ meno FN ma ha detto ↓ recall (verso invertito). Precision OK.
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
