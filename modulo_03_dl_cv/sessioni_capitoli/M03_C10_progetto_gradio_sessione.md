# Diario sessione — Capitolo 10 — Gradio + deploy HF Spaces

| Campo | Valore |
|-------|--------|
| **Modulo** | M03 — Deep Learning & Computer Vision |
| **File capitolo** | `10_progetto_gradio.py` |
| **File diario** | `M03_C10_progetto_gradio_sessione.md` |
| **Stato** | ✅ **Chiuso con residuo** il 25/09/2026 (aperto 14/09/2026). Residui: G6–G8 deploy, TODO 7 system design, 🔄 CONFRONTO PRIMA/DOPO |
| **Voto difficoltà** | **8.5**/10 — *“difficoltà di tenere mentalmente uniti i pezzi di tutta la pipeline, dall'addestramento alla costruzione del modello fino all'app Gradio”* |

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

### 2026-09-22 — Mini 7.1 (`10_progetto_gradio.py`, 3 file minimi Space)
- **Voto (1° tentativo): 6.5/10**
- **OK:** README+YAML (sdk/app_file) e requirements pinnati — contenuto buono; formato 3 bullet.
- **Manca:** il terzo file indispensabile è **`app.py`** (codice + oggetto `demo`), non il `.pt`. I pesi sono necessari alla *questa* demo ma non sono il file minimo dello Space Gradio (possono stare su Hub/LFS).
- **Soft:** typo READEME / requirments; note LFS/`hf_hub_download` utili ma fuori consegna.
- **Lacune:** none grave; ripasso “cos’è uno Space” = README + requirements + app.py.

### 2026-09-22 — Mini 7.1 fix applicato (`app.py` come 3°)
- **Fix applicato:** terzo bullet → `app.py` (logica / espone demo). Triade corretta.
- **Soft residuo:** typo READEME→README, requirments→requirements; “istuzioni”; B3 poteva citare oggetto `demo`.
- **Voto 1° resta 6.5/10**; fix ok → concetto chiuso.

### 2026-09-22 — Mini 7.2 (`10_progetto_gradio.py`, front-matter YAML)
- **Voto (1° tentativo): 9.5/10**
- **OK:** `---` delimiters; `sdk: gradio`; `app_file: app.py`; `title`; `sdk_version` pinnata; struttura come Sez. 7.2.
- **Soft:** due emoji ok; allineare `sdk_version` a quella reale in `requirements` / venv al deploy (ora in locale hai Gradio 6.x — per Spaces meglio pin coerente).
- **Lacune:** nessuna.

### 2026-09-22 — Mini 7.3 (`10_progetto_gradio.py`, pin versioni)
- **Voto (1° tentativo): 8.5/10**
- **OK:** caso concreto = breaking change su nuova release → app che ieri andava oggi no; pin = install riproducibile.
- **Soft:** non è “a ogni launch”: tipicamente a **build/reinstall** dopo push; formato chiedeva 1 riga (paragrafo lungo — #6 soft). Esempio ancora più concreto: `allow_flagging` rimosso in Gradio 6.
- **Lacune:** nessuna.

### 2026-09-22 — Mini 7.3 post-feedback
- **Fix applicato:** “build” al posto di launch + esempio reale `allow_flagging` / Gradio 6.
- **Soft residuo:** ancora più di 1 riga (#6 soft).
- **Voto 1° resta 8.5/10**; concetto chiuso bene.

### 2026-09-22 — Mini 7.4 (`10_progetto_gradio.py`, build vs runtime)
- **Voto (1° tentativo): 7.5/10**
- **OK:** 1 runtime, 2 runtime, 4 build.
- **Errore:** 3 `ModuleNotFoundError: torchvision` → **RUNTIME** (pip del build finisce; fallisce l’`import` all’avvio dell’app). Build fallirebbe solo se `pip install` stesso esplode.
- **Lacune:** soft — distinguere “manca dal requirements” (sintomo a runtime) vs “install che fallisce” (build).

### 2026-09-23 — Mini 8.1 (`10_progetto_gradio.py`, smoke test 3 controlli)
- **Voto (1° tentativo): 9/10**
- **OK:** 3 punti numerati; (1) ape palese → ordine classi; (2) somma≈1 → softmax/`dim`; (3) A poi B → cache o input ignorato. Allineati alla checklist Sez. 8.1.
- **Soft:** “unico modo” per le classi invertite è un po’ forte (anche foto formica + confronto); typo “un ape”.
- **Lacune:** nessuna.

### 2026-09-24 — Mini 8.2 (`10_progetto_gradio.py`, model card “quanto va” / #53)
- **Voto (1° tentativo): 9/10**
- **OK:** 2 frasi in voce 4 con `bees`, `45`, `~0.889` + recall/precision (schema #53 ancorato); riuso `ClassificatoreVisivo`/`valuta`/`tabella_soglie`; pipeline `grayscale_doc`, `num_workers=0`, dl test `[2]`; soglia come `[contratto['soglia']]`.
- **Soft:** consegna chiedeva solo 2 frasi — hai fatto model card intera (plus, ok); codice top-level nel capitolo (side effect all’import); `DIM_IMMAGINE` inutilizzata.
- **Lacune:** #53 su model card → rinforzata (quasi 🟢 se i numeri recall/prec sono quelli misurati a soglia 0.5).

### 2026-09-24 — Mini 8.3 (`10_progetto_gradio.py`, p50/p95 vs media)
- **Voto (1° tentativo): 6/10**
- **OK:** idea giusta (mediana non sporcata dagli estremi); 1 riga.
- **Manca:** esempio numerico obbligatorio di 8.3.b (19×30 ms + 1×2000 ms → media ~128 ms, che non è né tipica né peggiore). Senza numeri non chiudi #53-style / consegna.
- **Lacune:** soft Pattern #6 (formato ok, contenuto incompleto rispetto a “esempio numerico”).

### 2026-09-24 — Mini 8.4 (`10_progetto_gradio.py`, gatto / fuori dominio)
- **Voto (1° tentativo): 7/10**
- **OK:** capisce che ha solo 2 classi e deve comunque rispondere → sceglie ants/bees.
- **Manca:** (1) meccanismo softmax (probabilità solo sulle classi note, anche alta confidenza); (2) seconda parte consegna — **come lo dichiari nella model card** (limiti / fuori dominio). Formato 2 righe non rispettato (un blocco solo).
- **Lacune:** soft — chiudere il pezzo “dichiarazione onesta in model card”.

### 2026-09-24 — Mini 9.1 (`10_progetto_gradio.py`, Gradio → FastAPI)
- **Voto (1° tentativo): 8/10**
- **OK:** 2 bullet; immagine = PIL vs bytes→PIL; errori = UI vs `HTTPException`.
- **Soft:** B1 dice “analizza” (in API è `predict_etichetta`); B2 “risposta https” → meglio **status code HTTP** (es. 400) + detail per il client software.
- **Lacune:** nessuna grave.

### 2026-09-24 — Mini 9.2 (`10_progetto_gradio.py`, endpoint `/info`)
- **Voto (1° tentativo): 7.5/10**
- **OK:** perché = client API conosce caratteristiche senza leggere docs; arch + classi + soglia.
- **Manca / fuori luogo:** per riuso inferenza servono anche **dimensione_input, mean/std, pipeline_eval, versione_contratto**. LR / “transfer+finetune” / nome `fc` sono più model card che contratto di predizione (ok in `note`/`metriche`, non essenziali in `/info`).
- **Lacune:** soft — `/info` ≈ `scheda()` (contratto senza pesi).

### 2026-09-24 — Mini 9.3 (`10_progetto_gradio.py`, leakage prob_busta_paga_visivo)
- **Voto (1° tentativo): 8.5/10**
- **OK:** regola anti-leakage = CNN non allenata sulle stesse righe del train tabellare; in produzione i documenti sono nuovi → niente leakage da costruzione dataset.
- **Soft:** “non è necessario specificarla” → meglio: il problema **non esiste** in prod (casi fuori dal training), non che “non va dichiarata”. Opzionale: citare out-of-fold / CNN fit solo su train → predici su val/test.
- **Lacune:** nessuna.

### 2026-09-24 — Quiz verifica V1 (`10_progetto_gradio.py`, shape tensore)
- **Voto (1° tentativo): 9.5/10**
- **OK:** `(1, 3, 224, 224)`; 3 = RGB dopo `convert`; 224 dal contratto; 1 = batch.
- **Soft:** poteva dire esplicitamente che 500×400 sparisce nel resize/crop della pipeline.
- **Lacune:** nessuna.

### 2026-09-24 — Quiz verifica V2 (`10_progetto_gradio.py`, map_location CUDA→CPU)
- **Voto (1° tentativo): 9.5/10**
- **OK:** manca `map_location="cpu"` su **`torch.load`** (prima riga); Colab salva tensori etichettati cuda; in locale senza GPU serve rimappare. Lacuna #46 ok.
- **Soft:** typo minori; `load_state_dict` è la seconda riga e va bene dopo il load corretto.
- **Lacune:** nessuna.

### 2026-09-24 — Quiz verifica V3 (`10_progetto_gradio.py`, quantizzazione Spaces)
- **Voto (1° tentativo): 7/10**
- **OK:** **Falso** — ResNet18 in inferenza sta su Spaces CPU gratuito senza quantizzare.
- **Motivazione debole:** lazy load / non caricare i pesi al build è un tema di **cold start**, non risponde a “devo quantizzare?”. Motivo giusto: modello già abbastanza leggero; ms per immagine su CPU, non serve alleggerirlo per far partire la demo.
- **Lacune:** soft — non confondere quantizzazione con lazy loading.

### 2026-09-24 — Quiz verifica V4 (`10_progetto_gradio.py`, completa softmax)
- **Voto (1° tentativo): 5.5/10** ~~(errata: non avevo visto il codice compilato sotto)~~
- **Rivalutazione corretta sotto.**

### 2026-09-24 — Quiz verifica V4 rivalutato (`10_progetto_gradio.py`)
- **Voto (1° tentativo, corretto): 9/10**
- **OK:** `softmax`, `dim=1`, `zip(self.classi, …)`; `[0]` già in traccia; spiegazione dim = softmax sulle classi (colonne) per riga batch.
- **Soft:** formulazione “confrontare” un po’ informale (è normalizzare/sommare a 1 sull’asse classi).
- **Lacune:** nessuna. Mentor: scusa confusione sulla lettura della risposta.

### 2026-09-24 — Quiz verifica V5 (`10_progetto_gradio.py`, bug silenzioso ants)
- **Voto (1° tentativo): 6/10**
- **OK:** causa più probabile = **inversione ordine classi** (Sez. 1.3 / nomi a mano vs checkpoint).
- **Manca:** il 2° bullet ripete il *sintomo* della consegna (ape → ants ~0.99), non un *controllo* che conferma la causa. Controllo giusto: stampare `classificatore.classi` / confronto con `class_to_idx` del training (o mean/std vs contratto).
- **Lacune:** soft Pattern #6 + diagnostica (controllo ≠ riprodurre il bug).

### 2026-09-24 — Quiz verifica V5 post-feedback (`10_progetto_gradio.py`)
- **Voto (post-feedback, non esame): 9.5/10**
- **OK:** inversione classi; controllo `classificatore.classi` / `class_to_idx` vs ordine dict; ipotesi B mean/std ≠ training.
- **Soft:** consegna chiedeva 2 bullet → 3 (contenuto ok, formato Pattern #6 soft).
- **Lacune:** #54 → 🟡 (corretto dopo hint; da verificare a freddo).

### 2026-09-24 — Quiz verifica V6 (`10_progetto_gradio.py`, tre leve)
- **Voto (1° tentativo): 5.5/10**
- **OK:** `no_grad` = wrap sul forward / niente grafo / meno memoria.
- **Manca / errore:** (1) `requires_grad=False` in un *servizio di inferenza* **non serve** (era freeze in training) — ha risposto solo “dove freezo i layer”; (2) `eval()`: BN in eval **usa** `running_mean`/`running_var` (non le “spegne”); Dropout sì off. Dove: **subito dopo load pesi** (stato del modello), non “dopo no_grad”.
- **Lacune:** #48 riaperta 🟡 (BN + dove va freeze vs inferenza).

### 2026-09-24 — Quiz verifica V6 post-feedback (`10_progetto_gradio.py`)
- **Voto (post-feedback, non esame): 8/10**
- **OK:** `no_grad` wrap ogni predizione; `requires_grad=False` = freeze training, **in inferenza non serve**.
- **Soft:** `eval` — running_* ok, ma ancora “smette di usare BatchNorm” (BN resta attiva, cambia solo *quali* stats); manca “subito dopo load”. Typo `modell`.
- **Lacune:** #48 resta 🟡 (phrasing BN da chiudere a freddo).

### 2026-09-24 — Quiz verifica V7 (`10_progetto_gradio.py`, Feynman cold start Space)
- **Voto (1° tentativo): 6/10**
- **OK:** lazy load pesi alla 1ª predizione; dalla 2ª i pesi restano in RAM → solo forward. Niente “si scalda”.
- **Manca (rubrica ≥3 di 4):** risveglio container sleep; avvio processo + import `torch`; prima forward con allocazione buffer. Risposta corta vs 4–6 righe.
- **Lacune:** soft cold start Spaces (solo pezzo lazy load).

### 2026-09-24 — Quiz verifica V7 post-feedback (`10_progetto_gradio.py`)
- **Voto (post-feedback, non esame): 9.5/10**
- **OK:** sleep container; import torch; lazy load pesi; buffer 1ª forward; dalla 2ª solo calcoli. Niente “si scalda”.
- **Soft:** un blocco unico (poteva essere 4–6 righe più spezzate); “avvio processo” implicito nell’import.
- **Lacune:** #55 → 🟡 (completo dopo hint; da verificare a freddo).

### 2026-09-24 — Quiz verifica V8 (`10_progetto_gradio.py`, Feynman contratto)
- **Voto (1° tentativo): 7/10**
- **OK:** idea “.pt ≠ tutto”; guasto silenzioso mean/std ≠ training (accettabile, Sez. 1.2); nessun errore di runtime.
- **Manca:** (a) cos’è il contratto in concreto (arch, **classi ordinate**, size, mean/std, soglia, versione) — “tutte le info” è vago; (b) rubrica preferisce anche **classi invertite**; (c) conclusione: contratto **nel** checkpoint, nomi letti da lì non a mano in demo.
- **Lacune:** soft — elenco voci contratto + caso classi.

### 2026-09-24 — TODO 1 (`10_progetto_gradio.py`, colloquio produzione 5 bullet)
- **Voto (1° tentativo): 6.5/10**
- **OK:** (1) contratto a 6 voci; (2) Gradio vs API criterio umani/software; (5) pezzi di smoke utili (A≠B, somma 1, bees, RGB, guardia).
- **Manca:** (1) esplicita “pesi **+** contratto”; (3) **numero** (decine di ms ResNet18 CPU) — ha solo regola qualitativa; (4) **come esporre** versione (`/info` o campo in risposta); (5) post-deploy continuo: latenza, distribuzione predizioni, errori nei log (oltre checklist UI).
- **Lacune:** soft Pattern #6 su “con un numero” + esposizione versione.

### 2026-09-25 — TODO 2 annotazioni a lato (`10_progetto_gradio.py`, pre-parte a)
- **Voto (check diagnostico, non ancora parte a formale): 7.5/10**
- **OK:** reload/`if is None`; `DEFAULT` inutile; path assoluto; `map_location`; `512`→`in_features`; RGB; Normalize; `no_grad`.
- **Errore:** `train()` — BN confusa: in train usa stats del **batch**; `running_*` sono quelle accumulate e le usa **`eval()`**.
- **Manca come 6° problema distinto:** `return argmax` + `print` (indice grezzo, niente nomi/proba, mescola logica/UI). Soft: `Resize((224,224))` deforma vs Resize+CenterCrop.
- **Lacune:** #48 BN phrasing ancora aperta.

### 2026-09-25 — TODO 2 annotazioni rivalutate (`10_progetto_gradio.py`)
- **Voto (check diagnostico): 9.5/10**
- **OK:** tutti e 6 i filoni rubrica — reload; path; DEFAULT+`map_location`; `train`→batch stats vs `running_*` + `no_grad`; `512`/Resize+crop/RGB/Normalize; return/`print` senza proba utili.
- **Soft:** su `return argmax().item()` hai scritto “nome classe” — è un **indice intero** (0/1), peggio del solo nome. Parte (a) formale ancora da scrivere in **esattamente 6 bullet**.
- **Lacune:** #48 → 🟡 quasi chiusa su BN (spiegazione train corretta nelle annotazioni).

### 2026-09-25 — TODO 3 (`10_progetto_gradio.py`, DEBUG git-lfs 133 byte)
- **Voto (1° tentativo scritto): 9/10**
- **OK:** (a) 133 B = puntatore ≠ ~40 MB pesi; LFS assente/non usato al commit. (b) `lfs track` + add `.gitattributes` + `.pt` + commit/push.
- **Soft:** manca `git lfs install`; se il file era già in history come non-LFS a volte serve `git rm --cached` + ri-add; alternativa valida `hf_hub_download`. Nota: concetto rinforzato in chat prima della risposta scritta.
- **Lacune:** nessuna grave su LFS.

### 2026-09-25 — TODO 4 (`10_progetto_gradio.py`, retrieval costruisci_modello)
- **Voto (1° tentativo dopo iterazioni in chat): 8.5/10**
- **OK:** getattr + check None; `modello = costruttore(weights=pesi)`; testa via `in_features`; `hasattr` su modello per `fc`/`classifier`; else chiaro.
- **Soft:** `AttributeError` → meglio `ValueError` + messaggio con esempi; su EfficientNet `classifier` è spesso `Sequential` → serve `[-1].in_features` / sostituire solo l’ultimo (estensione non ancora robusta al 100%).
- **Lacune:** soft — Sequential vs Linear sulla testa `classifier`.

### 2026-09-25 — TODO 4 rivalutato (`10_progetto_gradio.py`)
- **Voto (post-iterazioni): 9.5/10**
- **OK:** getattr/`is None`/`ValueError`; build una volta; `hasattr` su modello; `fc` + `classifier[-1].in_features` con replace dell’ultimo Linear (tiene Dropout).
- **Soft:** messaggio errore arch potrebbe citare esempi (`resnet18`, …); edge case se `classifier` fosse Linear puro (senza `[-1]`) — raro sulle reti tipiche del TODO.
- **Lacune:** nessuna grave.

### 2026-09-25 — TODO 5 (`10_progetto_gradio.py`, interleaving Streamlit/Gradio)
- **Voto (1° tentativo): 6/10**
- **OK:** (1) semaforo riusabile; (2) `motivi_top3` no su immagine (feature senza nome umano).
- **Manca / errore:** (1) meglio anche **disclaimer** + logica soglia→decisione→azione; recall in UI è soft. (3) non diventa “prob. genuinità” — diventa **feature map / Grad-CAM** (“dove ha guardato”, cap.08). (4) affiancare score tabellare + visivo e semaforo sulla **combinazione** con pesi dichiarati, non solo una sezione extra.
- **Lacune:** soft — explainability visiva ≠ probabilità.

---

## Lacune e dubbi ancora aperti

Ereditate da C09 da verificare qui:

- 🟡 **#48** — BN chiarita in TODO 2 annotazioni (train=batch, eval=running_*); da fissare a freddo
- 🟢 **#52** — Mini 52.A **9.5**/10
- 🟢 **avgpool → vettore 512** — Q2 9.5/10
- 🟡 **Soglia/recall** — Q7 **5**/10
- 🔴 **Pattern #6** — formato consegne (TODO 1.3: manca il numero)
- 🟡 **#53** — Mini 53.A **8**/10
- 🟡 **#54** — diagnostica V5 (post-fix ok)
- 🟡 **#55** — cold start Space (V7 post-fix 9.5; da verificare a freddo)
- 🟡 **Contratto di inferenza (V8)** — idea ok, elenco voci + conclusione checkpoint soft
- 🟡 **TODO 1 colloquio** — versione esposta + latenza numerica
- 🟡 **TODO 2** — annotazioni 9.5; manca ancora parte (a) 6 bullet + codice (b)
- 🟢 **TODO 3 LFS** — 9/10
- 🟢 **TODO 4** — 9.5/10 (post-iterazioni; `classifier[-1]`)
- 🟡 **TODO 5** — Grad-CAM/feature map vs proba; combo semaforo

---

### 2026-09-25 — Decisione corso: Grad-CAM ripianificato (saturazione)
- **Prima ipotesi:** coda M3 subito dopo C10.
- **Decisione studente:** troppo saturo → Grad-CAM in **ripresa M3/prodotto** (buste / Validator / ripasso), non post-Spaces.
- **Fine modulo formale:** chiusura C10. Seed `grad_cam_pipeline.py` resta. Evitare `11_*` (c’è già `11_colab_track_...`).

### 2026-09-25 — Decisione corso: M3-11 Grad-CAM (superata, vedi sopra)
- Ipotesi iniziale post-C10: archiviata lo stesso giorno.

---

### 2026-09-25 — Canonizzata Regola 43 (ripasso propositivo)
- Obbligo: prima di citare il passato in esercizi/teoria/chat → `# 🔁 RIPASSO PROPOSITIVO`.
- File aggiornati: CONTESTO, mentor-ai-corso, AGENTS, .cursorrules, `.cursor/rules/43-ripasso-propositivo.mdc`.

---

### 2026-09-25 — TODO 6 (`10_progetto_gradio.py`, real-world buste nella demo)
- **Nota esame:** la versione nel file è stata scritta **dopo** aver visto la traccia del mentor (era partito con 1 solo punto: “non accetto senza anonimizzazione”). Non è un primo tentativo a freddo → **non si registra voto**.
- **1° tentativo autonomo (parziale):** solo punto 1, e troppo debole (“ok se anonimizzate”): in una demo/repo i documenti dei clienti non entrano comunque.
- **Copertura finale (5/5):** no documenti reali; storia Git non si cancella; decisione non individuale (titolare/privacy); alternativa praticabile (Space privato / sintetici / locale); prematuro anche tecnicamente (modello su proxy ants-bees).
- **Lacuna:** nessuna nuova sul merito privacy; conferma Pattern #6 (partire dal formato richiesto: 5 punti numerati).

### 2026-09-25 — 🏗️ PROGETTO INCREMENTALE G1–G5 (pacchetto Space `modulo_03_dl_cv/app/`)
- **Valutazione: 8.5/10** sul lavoro di packaging.
- **OK:** cartella dedicata con `app.py` + `modello.py`; `dati/pesi/ants_vs_bees.pt`; 4 immagini di esempio; `requirements.txt` **solo demo** e pinnato (`torch==2.14.0`, `torchvision==0.29.0`, `gradio==6.27.0`, `pillow==12.1.1`) con extra-index **CPU**; `README.md` con front-matter (`sdk`, `sdk_version` allineata, `app_file`) + model card nelle 6 voci; demo verificata in locale su `127.0.0.1:7860`.
- **Errori intercettati prima del deploy:** (1) primo `requirements` era quello del corso (`>=`, sklearn/streamlit/fastapi); (2) dataset `proxy_ants_bees` (~47 MB) e secondo `.pt` dentro il pacchetto; (3) **path esempi**: `app.py` leggeva `QUI/"esempi"` mentre le foto erano in `dati/esempi/` → `examples=None`; (4) `"""` residuo in fondo al README.
- **Lettura positiva:** tutti e 4 trovati **prima** di pubblicare — è esattamente il comportamento chiesto dallo smoke test (lacuna #54 usata sul campo).

### 2026-09-25 — G6–G8 NON eseguiti: blocco di piattaforma (non didattico)
- **Fatto:** aperta la creazione dello Space su Hugging Face.
- **Blocco:** policy HF 2026 — **Gradio/Docker Spaces girano su compute e richiedono un piano a pagamento** (PRO per account personali). Restano free: Static HTML e **Gradio Lite** (browser, niente PyTorch/`.pt` → incompatibili con questa demo) oppure fino a **2 Space ZeroGPU** per account personale in regola (email verificata, account >30 giorni), che però richiederebbero `@spaces.GPU` nel codice.
- **Decisione studente:** non pagare, non forzare → **chiudere il capitolo** con il residuo dichiarato.
- **Conseguenze:** Portfolio #2 resta senza URL; **niente archivio M3** né scommento dipendenze M4 finché il deliverable non è sciolto.
- **Opzioni aperte (prossima sessione):** ZeroGPU + `@spaces.GPU` · HF PRO · altro host (Render/Railway) · community grant · demo locale documentata con screenshot/GIF nel portfolio.

---

## Esito finale del capitolo (25/09/2026)

| Blocco | Esito |
|--------|-------|
| Quiz d'ingresso Q1–Q8 | ✅ svolti (medi 1° tentativo ~7.5) |
| Quiz verifica V1–V8 | ✅ svolti (deboli V6 5.5, V7 6, V8 7 → lacune #55/#56/#57) |
| Mini-esercizi | ✅ svolti |
| TODO 1–6 | ✅ svolti (TODO 6 con traccia vista) |
| TODO 7 📐 system design | ❌ **non svolto** |
| 🏗️ G1–G5 | ✅ |
| 🏗️ G6–G8 (deploy/smoke/latenza) | ❌ bloccati (policy HF) |
| 🏗️ P1–P5 track buste | ❌ debito noto (serve C1–C8) |
| 🔄 CONFRONTO PRIMA/DOPO | ❌ **non svolto** (Regola 16: da fare prima dell'archivio M3) |

**Voto difficoltà: 8.5/10** — il più alto del modulo dopo il 9 del cap.05. Motivazione dello studente: il carico non viene dai concetti singoli ma dal **tenere insieme la catena** addestramento → checkpoint/contratto → costruzione modello → app.

---

## Note per fine modulo (mentor)

- ⚠️ **Archivio M3 NON eseguito il 25/09/2026**: il protocollo FINE MODULO (archivio + scommento M4 in `requirements.txt` + URL portfolio) resta **sospeso** finché non si scioglie il blocco deploy e non si completa il 🔄 CONFRONTO PRIMA/DOPO.
- Passo 13 solo a chiusura di **questo** capitolo, non di C09.
- Nota tecnica emersa scrivendo il capitolo: da PyTorch 2.6 `torch.load` usa
  `weights_only=True` per default, quindi nel checkpoint ricco vanno **solo**
  tipi base (`str(torch.__version__)`, non l'oggetto `TorchVersion`).
  Il caso è documentato in Sez. 2.6 con l'errore reale.
