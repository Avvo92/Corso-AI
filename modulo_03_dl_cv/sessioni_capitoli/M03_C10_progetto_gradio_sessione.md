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

### 2026-09-16 — Quiz ingresso Q8 Feynman (`10_progetto_gradio.py`, transfer learning)
- **Voto (1° tentativo): 8/10**
- **OK:** analogia segretario vs bambino chiara; transfer = riuso backbone + nuova head; fase 1 head, fase 2 layer4 con prudenza; aggancio dominio documenti.
- **Manca:** *perché* due fasi esplicito (fase 1: pochi parametri, non rovinare pesi ImageNet; fase 2: LR basso, adattare feature più specifiche). Layer generici (bordi/texture) non citati. Vincolo “ogni termine spiegato in mezza riga” solo parziale (`backbone`, `rete` soft).
- **Next:** aggiungere 1 riga su freeze/LR basso; citare ImageNet o “milioni di foto” come pretraining.
- **Lacune:** residuo C09 TODO 8 (depth-1 vs depth-2 a voce) — migliorato ma non chiuso al 9+.

### 2026-09-16 — Mini 48.A (`10_progetto_gradio.py`, tre leve V/F)
- **Voto (1° tentativo): 8.5/10**
- **OK:** 1–2–3 tutti **Falso**; (1) eval → Dropout/BN non `requires_grad`; (2) `no_grad` → grafo, non BN; (3) freeze ≠ saltare il forward (parla di gradienti/backprop).
- **Soft:** (1) “Blocca il Dropout” impreciso — in `eval()` Dropout **non spegne** nessuno (passa tutto), non lo “blocca”. (3) meglio: forward **passa** dai layer; `requires_grad=False` evita l’**aggiornamento** dei pesi (non confondere con `no_grad`).
- **Lacune:** #48 → 🟡 quasi 🟢 (Q1 7/10 + Mini 48.A 8.5). Chiudere con Mini 48.B (una riga `with torch.no_grad()`).

### 2026-09-16 — Mini 48.B (`10_progetto_gradio.py`, contesto no_grad)
- **Voto (1° tentativo): 10/10**
- **OK:** `with torch.no_grad():` — riga esatta; formato corretto; non confuso con `eval()` già chiamato.
- **Lacune:** #48 → 🟢 chiusa (Q1 + 48.A + 48.B).

### 2026-09-16 — Mini 52.A (`10_progetto_gradio.py`, decomposizione matmul)
- **Voto (1° tentativo): 9.5/10**
- **OK:** 32=batch; 512=feature dal backbone; 256=`in_features` del Linear (il mismatch); fix portabile `modello.fc.in_features` + `nn.Linear(..., 2)`.
- **Soft:** bullet 3 un po’ prolisso; non serve nominare D=2 (non chiesto). Concetto #52 coperto a freddo sul 32.
- **Lacune:** #52 → 🟢 chiusa.

### 2026-09-16 — Mini 53.A (`10_progetto_gradio.py`, obiezione ancorata)
- **Voto (1° tentativo): 8/10**
- **OK:** acc 89% + recall 83% (calcolo 25/30 ok); non generica; domanda sul costo di perdere il 17% delle api (dominio).
- **Manca (schema 4 pezzi):** conteggio assoluto **5/30** mancate; **leva** (soglia ↓) e **prezzo** (precision). “Accuracy buona” soft vs citare il 89% del PM e smontarlo.
- **Lacune:** #53 resta 🟡 (quasi 🟢); consolidare Mini 8.2 / model card.

### 2026-09-16 — Mini AVG (`10_progetto_gradio.py`, AdaptiveAvgPool)
- **Voto (1° tentativo): 10/10**
- **OK:** `(4,2048,12,12)` → `(4,2048,1,1)` → flatten `(4,2048)`; `in_features=2048` = ResNet50 (vs 512 ResNet18).
- **Lacune:** avgpool→vettore fisso consolidato (già 🟢 su Q2).

### 2026-09-16 — Mini 1.1 (`10_progetto_gradio.py`, 6 voci contratto)
- **Voto (1° tentativo): 8/10**
- **OK:** le 6 voci ci sono (arch, classi+ordine, size, norm, soglia, versione); fonti classi/soglia nella direzione giusta.
- **Soft:** (1)(3) meglio “scelta training / checkpoint”, non “dal codice del modello”; (4) mean/std ImageNet (o dal checkpoint), non “tipo di modello”; (6) VERSIONE_CONTRATTO / scheda modello, non solo “versione del modello”.
- **Next:** Sez. 2 — le voci vivono *dentro* il `.pt`.

### 2026-09-16 — Mini 1.1 (post-feedback)
- **Voto: 9.5/10**
- **OK:** (1) stringa scelta da te; (2) ImageFolder; (3) training / 224 ImageNet; (4) mean/std ImageNet; (6) versione + data + metriche.
- **Soft residuo:** (5) “la decido io” → più preciso: **sul validation** (cap.09). In deploy tutte e 6 si **leggono dal checkpoint**.

### 2026-09-16 — Mini 1.2 (`10_progetto_gradio.py`, bug senza crash)
- **Voto (1° tentativo): 9.5/10**
- **OK:** due voci senza eccezione: **ordine classi** (etichette invertite in demo) + **mean/std** (sicuro sempre sulla stessa classe). Concetto Sez. 1.2/1.3 centrato.
- **Soft:** prima riga un filo “perché” (manca contratto) vs solo sintomo UI; ok comunque. Altre valide: dimensione, soglia, versione.

### 2026-09-16 — Mini 1.3 (`10_progetto_gradio.py`, email collega + .pt)
- **Voto (1° tentativo): 7.5/10**
- **OK:** le 6 voci del contratto ci sono tutte (arch≈tipo, classi+ordine, size, norm, soglia, versione/metriche). Concetto “.pt non basta” ok.
- **Manca (formato):** consegna = **2 righe** stile email; hai fatto elenco. Pattern **#6**. Soft lessico: “tipo del modello” → **architettura**; “soglia ottimale” → soglia scelta sul validation.
- **Target:** “Ti mando il .pt ma ti serve il contratto: arch, classi ordinate, 224, mean/std, soglia, versione. Meglio: un checkpoint ricco che li include.”

### 2026-09-16 — Mini 1.3 (post-feedback)
- **Voto: 8.5/10**
- **OK:** tono email; **architettura**; soglia **su validation**; 6 voci complete.
- **Soft residuo:** ancora elenco multi-riga, non **2 righe** compressi (Pattern #6). Concetto chiuso; formato ancora soft.

### 2026-09-16 — Mini 2.1 (`10_progetto_gradio.py`, dentro/fuori checkpoint)
- **Voto (1° tentativo): 10/10**
- **OK:** DENTRO = classi, soglia, mean/std, nome_arch; FUORI = optimizer, percorsi training, immagini val, LR. Criterio “serve a predire vs serve a riprendere training” applicato.
- **Soft:** “classe” → **classi** (plurale / ordine).

### 2026-09-16 — Mini 2.2 (`10_progetto_gradio.py`, chiamata salva_checkpoint)
- **Voto (1° tentativo): 5.5/10**
- **OK:** nome_arch resnet18; mean/std ImageNet; note proxy; idea keyword args.
- **Errori:** (1) `*,` in chiamata — SyntaxError, `*` solo in def; (2) `classi` deve essere **lista** `["ants","bees"]` non dict; (3) soglia consegna **0.45** non 0.5; (4) accuracy **0.889**; (5) `):` di troppo.
- **Next:** riscrivere la chiamata senza `*` e con lista classi.

### 2026-09-16 — Mini 2.2 (post-feedback)
- **Voto: 10/10**
- **OK:** niente `*` in call; `classi=["ants","bees"]`; soglia 0.45; accuracy 0.889; mean/std; note proxy. Sintassi valida.

### 2026-09-16 — Mini 2.3 (`10_progetto_gradio.py`, Missing/Unexpected + strict)
- **Voto (1° tentativo): 7.5/10**
- **OK:** (a) idea rinomina testa; (b) `strict=False` → testa non caricata → predizioni a caso. Punto produzione centrato.
- **Soft/errore:** direzione Missing/Unexpected invertita a parole: **Missing** = il *modello* ha `fc`, il *file* no; **Unexpected** = il *file* ha `head`, il *modello* no. Nell’errore il nome è **`head`**, non “classificatore”.
- **Target (a):** stesso scheletro, testa salvata come `head` e codice attuale aspetta `fc`.

### 2026-09-16 — Mini 2.3 (post-feedback)
- **Voto: 10/10**
- **OK:** (a) modello `.fc` vs file `.head` = rinomina testa; (b) `strict=False` → `fc` random, demo silenziosamente sbagliata. Direzione Missing/Unexpected corretta.

### 2026-09-16 — Mini 2.4 (`10_progetto_gradio.py`, weights_only + data)
- **Voto (1° tentativo): 8.5/10**
- **OK:** `"data": str(datetime.now())`; idea tipi base / niente oggetti ricchi.
- **Soft:** il blocco è al **load** (`weights_only=True`), non alla serializzazione in sé; `datetime.now()` spesso si salva, ma non si ricarica in modo sicuro. Typo “possimo”.

### 2026-09-16 — Mini 3.1 (`10_progetto_gradio.py`, pesi_pretrained=None)
- **Voto (1° tentativo): 9/10**
- **OK:** spreco perché subito dopo `load_state_dict` del checkpoint; ImageNet scaricato sarebbe inutilizzato/sovrascritto (anche backbone).
- **Soft:** poteva citare ~45 MB / tempo boot Spaces; “pesi aggiornati” → più preciso **sovrascritti** dal `.pt`.

### 2026-09-16 — Mini 3.2 (`10_progetto_gradio.py`, caricamento pigro)
- **Voto (1° tentativo): 3.5/10**
- **Errore:** confonde lazy con “ricarica a ogni predict”. In `ClassificatoreVisivo` il load è `if self._modello is None` → **una volta**, poi cache.
- **Manca:** `__init__` eager = boot lento, 1ª+succ. veloci; lazy = boot veloce, **1ª** predict lenta, **succ.** veloci come eager.
- **Next:** rileggere Sez. 3.3 punti 1–2 (lazy + una volta sola).

### 2026-09-16 — Mini 3.2 (post-feedback)
- **Voto: 8/10**
- **OK:** health check Spaces + lazy; guardia `_modello is None` (non ricarica ogni volta). Concetto corretto dopo chiarimento.
- **Soft (consegna):** manca esplicito **1ª vs successive** sui tempi: eager → 1ª già veloce; lazy → **solo la 1ª** lenta, poi come eager. Un po’ lungo vs 2 righe.

### 2026-09-16 — Mini 3.3 (`10_progetto_gradio.py`, difetti di riuso)
- **Voto (1° tentativo): 6/10**
- **OK:** vedi hardcode (arch, 512, path assoluto) → sintomo 1 “devi editare il codice”. Fix `getattr` / `in_features` / path parametro nella direzione giusta.
- **Manca (sintomi 2 e 3 di Sez. 3.0):** (2) a **ogni** chiamata ricostruisce, `weights="DEFAULT"` (scarica ImageNet) + load da disco — side effect / non riuso pulito; (3) **`print`** intrecciato, ritorna indice non probabilità. Extra validi: no `eval`/`no_grad`, no Normalize, `Resize((224,224))` deforma, no `map_location`.
- **Next:** mappare 1→hardcode, 2→ricarica/side effect, 3→print/UI.

### 2026-09-16 — Mini 3.3 (alternativa: riscrittura `crea_predittore`)
- **Voto: 9.5/10**
- **OK:** factory+closure chiude i 3 sintomi in pratica: (1) path/device/contratto non hardcode; (2) load una volta in `crea_predittore`, non a ogni predict; (3) return dict probabilità, no print. Pipeline: RGB, transform da contratto, unsqueeze, no_grad, softmax. Riga `predici = crea_...` commentata → no side effect all’import.
- **Soft:** a voce saper ancora *nominare* i 3 sintomi 3.0 (consegna originale era elenco); codice dimostra padronanza operativa.

### 2026-09-16 — Mini 3.4 (`10_progetto_gradio.py`, eval stato vs no_grad contesto)
- **Voto (1° tentativo): 8/10**
- **OK:** eval → Dropout off + BN running stats; no_grad → niente grafo / risparmio; no_grad a ogni forward di predizione.
- **Soft:** manca la parola-chiave **stato vs contesto** (perché uno basta una volta: resta sull’oggetto; l’altro vale solo dentro `with`). “Smette BatchNorm” impreciso (BN gira ancora, ma con running). Consegna 1 riga → 2. Typo: autograd, “in tutto”.

### 2026-09-16 — Mini 3.4 (post-feedback)
- **Voto: 8.5/10**
- **OK:** BN corretta (running_mean/var, normalizza ancora); no_grad/autograd/VRAM ok.
- **Soft residuo:** ancora non esplicita **stato persistente vs contesto `with`** (il “perché” della consegna). Ancora 2 righe vs 1.

### 2026-09-17 — Mini 4.1 (`10_progetto_gradio.py`, Interface minima)
- **Voto (1° tentativo / fix immediato): 9.5/10**
- **OK:** `gr.Interface` + `lambda x: x**2` + `gr.Number()` in/out + `.launch()`. Parentisi componenti ok; riga commentata → no side effect all’import.
- **Soft:** opzionale `if __name__ == "__main__":` intorno al launch.

### 2026-09-17 — Mini 4.1 (post-feedback)
- **Voto: 9/10**
- **OK:** Interface + Number() + launch sotto guardia `__main__`.
- **Soft sintassi:** manca `:` dopo `if __name__ == "__main__"` e indentazione di `launch()` (in codice vero sarebbe SyntaxError). Come bozza commentata concetto ok.

### 2026-09-17 — Mini 4.2 (`10_progetto_gradio.py`, gr.Label V/F)
- **Voto (1° tentativo): 9.5/10**
- **OK:** **Falso**; `gr.Label` accetta dict `{classe: probabilità}` e disegna le barre — non serve un altro componente solo per le probabilità.
- **Soft:** “in ordine” non è il punto centrale; il punto è dict → barre / stringa → etichetta secca.

### 2026-09-17 — Mini 4.3 (`10_progetto_gradio.py`, Image type pil vs numpy)
- **Voto (1° tentativo): 9/10**
- **OK:** (1) transforms torchvision lavorano bene su PIL (+ `convert("RGB")`); (2) numpy è (H,W,C), PyTorch vuole (C,H,W) — con PIL+`ToTensor` la permutazione è inclusa.
- **Soft:** “tensore numpy” → array NumPy; typo “immagile”.

### 2026-09-17 — Mini 4.4 (`10_progetto_gradio.py`, TypeError Interface arity)
- **Voto (1° tentativo): 9.5/10**
- **OK:** mismatch n°/ordine `inputs` di `Interface` vs parametri di `predici` (qui 2 componenti → 1 arg). Errore tipico Sez. 4.2.
- **Soft:** si può citare anche `outputs` vs valori di `return` (stessa regola); qui il messaggio punta agli **inputs**.

### 2026-09-17 — Mini 5.1 (`10_progetto_gradio.py`, shape pipeline)
- **Voto (1° tentativo): 6/10**
- **OK:** numeri Resize ~341 e 256; CenterCrop 224; finali `(3,224,224)` e `(1,3,224,224)`.
- **Errori:** (1) dopo `convert`/`Resize`/`Crop` è ancora **PIL**, non `(C,H,W)` — i canali arrivano con **ToTensor**; (2) PIL 400×300 = W×H → lato corto è **300**; dopo Resize(256): **341×256** (W×H) = in CHW sarebbe `(3,256,341)`, non `(3,341,256)`.
- **Target:** RGB 400×300 → Resize 341×256 → Crop 224×224 → ToTensor `(3,224,224)` → unsqueeze `(1,3,224,224)`.

### 2026-09-17 — Mini 5.2 (`10_progetto_gradio.py`, softmax dim)
- **Voto (1° tentativo): 9.5/10**
- **OK:** `(4,2)` = 4 esempi × 2 classi; `dim=1` somma 1 sulle classi per riga (giusto); `dim=0` somma sulle immagini per classe (senza senso).
- **Soft:** consegna 1 riga → 3 (Pattern #6); contenuto pieno.

### 2026-09-17 — Mini 5.3 (`10_progetto_gradio.py`, Normalize assente)
- **Voto (1° tentativo): 9.5/10**
- **OK:** (1) no crash: shape/range ancora validi per Conv2d (0–1); (2) probabilità plausibili ma sbagliate, tipico “sempre sicuro sulla stessa classe”. Allineato Sez. 1.2 / 5.2.
- **Soft:** “inevitabilmente” un filo forte (è il caso *tipico*); il perché profondo = input fuori scala ImageNet `(x-mean)/std`.

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

### 2026-09-17 — Assemblaggio `modello.py` (core riusabile per `app.py`)
- **Voto (1° tentativo): 9/10**
- **OK:** import protetti; costanti; `transform_eval` + `costruisci_modello` + `carica_checkpoint` + `ClassificatoreVisivo`; ordine dipendenze corretto (`costruisci` prima di `carica`); import del modulo OK.
- **Soft:** `ROOT` e `PIL`/`VERSIONE_CONTRATTO` inutilizzati (ok se tieni `salva_checkpoint` dopo); manca `salva_checkpoint` (non serve alla sola demo Gradio).
- **Next:** `pip install torchvision` nel venv (oggi manca → predizione fallirebbe); poi smoke con `.pt` + Gradio.
- **Lacune:** nessuna nuova sul riuso codice.

### 2026-09-21 — Mini 6.1 (`10_progetto_gradio.py`, 4 blocchi app.py)
- **Voto (1° tentativo): 8.5/10**
- **OK:** 4 bullet come da formato (#6 ok); B1 config senza logica; B3 core testabile senza Gradio; B4 solo UI. Criterio separazione logica/presentazione compreso.
- **Soft:** B2 — manca “caricamento pigro / una sola istanza a livello modulo”; typo minori.
- **Lacune:** nessuna nuova.

### 2026-09-21 — Mini 6.2 (`10_progetto_gradio.py`, test togli Gradio)
- **Voto (1° tentativo): 8/10**
- **OK:** riscrivi solo blocco 4 (UI); idea separazione corretta; 1 riga come da formato.
- **Soft:** non dice esplicitamente che B1–B3 restano; typo “blocca”.
- **Lacune:** nessuna nuova.

### 2026-09-21 — Mini 6.3 (`10_progetto_gradio.py`, test core senza Gradio)
- **Voto (1° tentativo): 9/10**
- **OK:** `Image.open` → `analizza` → assert somma ≈ 1 (`isclose`/`atol=1e-5`); path corretto sotto `dati/`; nessun `demo.launch`.
- **Soft:** `esito['ants']+esito['bees']` ok sul proxy; più generico `sum(esito.values())`. Codice a livello modulo nel capitolo (side effect all'import) — accettabile per il mini.
- **Lacune:** nessuna nuova.

### 2026-09-21 — Mini 6.3 post-feedback (sum generico)
- **Voto (post-feedback): 7.5/10** — idea giusta, bug: `sum(esito.values)` senza `()` → non itera le probabilità (TypeError o assert senza senso). Serve `sum(esito.values())`.
- **Fix atteso:** `assert np.isclose(sum(esito.values()), 1.0, atol=1e-5), ...`
- **Lacune:** attenzione metodi dict da chiamare (`.values()` / `.keys()` / `.items()`).

### 2026-09-21 — Mini 6.3 fix applicato (`.values()`)
- **Fix applicato:** `sum(esito.values())` corretto; assert + PIL + path ok.
- **Voto 1° tentativo resta 9/10**; post-bug risolto → esercizio chiuso sul merito.

---

## Lacune e dubbi ancora aperti

Ereditate da C09 da verificare qui:

- 🟢 **#48** — `eval` / `no_grad` / freeze → chiusa (Mini 48.B **10**/10)
- 🟢 **#52** — decomposizione matmul + `in_features` → Mini 52.A **9.5**/10
- 🟢 **avgpool → vettore 512** — Q2 9.5/10 (15/09): meccanismo + esempi shape OK
- 🟡 **Soglia/recall** — Q7 **5**/10: ↓ soglia ⇒ meno FN ma ha detto ↓ recall (verso invertito). Precision OK.
- 🔴 **Pattern #6** — formato consegne (quasi ogni consegna del cap.10 dichiara
  il formato atteso: numero di bullet/righe. Serve a misurare il pattern)
- 🟡 **#53** — obiezione sui numeri → Mini 53.A **8**/10 (manca 5/30 + leva soglia); consolidare Mini 8.2

---

## Note per fine modulo (mentor)

- Aggiornare Portfolio URL #2; protocollo FINE MODULO (archivio M3, scommentare M4 in requirements).
- Passo 13 solo a chiusura di **questo** capitolo, non di C09.
- Nota tecnica emersa scrivendo il capitolo: da PyTorch 2.6 `torch.load` usa
  `weights_only=True` per default, quindi nel checkpoint ricco vanno **solo**
  tipi base (`str(torch.__version__)`, non l'oggetto `TorchVersion`).
  Il caso è documentato in Sez. 2.6 con l'errore reale.
