# Modulo 3 — Deep Learning & Computer Vision

> **Stato**: ⬜ DA CREARE (pianificato).
> I file `.py` di questo modulo sono al momento **solo segnaposto con TODO MENTOR**: vanno completati uno alla volta, **alla chiusura del capitolo precedente**, come da protocollo del corso.
> Vedi `CONTESTO_CORSO.md` → sezione "Computer Vision nel Prodotto" per la decisione 30/04/2026 sul deliverable cap.07.

## Obiettivo del modulo

Capire come funzionano davvero le reti neurali (non più "Scikit-Learn nasconde tutto") e arrivare a un classificatore CNN deployato come **secondo URL portfolio** (Gradio + HuggingFace Spaces).

## Demo finale di portfolio

Classificatore visivo **busta paga vs non-busta paga** + demo Gradio deployata. Output integrabile come feature aggiuntiva nel modello supervisionato del Modulo 2.

## Indice capitoli

> **⚠️ Split del 27/05/2026**: il vecchio `03_backpropagation.py` (monolitico, 1700 righe, atteso 9/10) è stato spezzato in **4 sotto-capitoli** (03 loss → 04 derivate → 05 chain rule + GD → 06 backprop + training). I file successivi sono stati rinumerati di conseguenza (04→07, 05→08, 06→09, 07→10). Il modulo M3 è passato da 7 a **10 capitoli**.
>
> **Espansione del 27/05/2026 (post-split)**: su richiesta dello studente ("tanti esercizi, pipeline complete, richiami forti intra-M3 per padroneggiare la pipeline DL"), tutti i 4 sotto-capitoli sono ora **PIENI di esercizi e pipeline integrate** (~14-17 mini-esercizi inline + 16-19 TODO numerati per file). Ogni file ha 5-6 sezioni di teoria con mini-esercizio dopo ogni concetto, 1 pipeline integrata che lega col capitolo precedente, 6 esercizi tipologie (colloquio/refactor/debug/retrieval/interleaving/real-world), quiz d'ingresso + verifica, mini-progetto finale, checkpoint. Difficoltà attese ricalibrate (vedi tabella).

| # | File | Argomento | Difficoltà attesa | Piattaforma |
|---|------|-----------|-------------------|-------------|
| 01 | `01_neurone_artificiale.py` | Neurone come "if con pesi", attivazioni (sigmoid, ReLU), forward pass a mano in NumPy. **Recall cross-modulo** dal Ponte Matematico. | 6/10 | CPU locale |
| 02 | `02_reti_neurali.py` | Layer impilati = sequenza di `X @ W + b` (cap.02 Ponte) + attivazioni; rete full-NumPy che classifica le pratiche del CSV M2. | 7/10 | CPU locale |
| 03 | `03_loss.py` ✅ **completato** (01/06/2026, voto **8**/10) | LOSS (BCE), MSE, clip bilaterale, soglia 0.5. Pipeline `valuta_rete_random` + mini-progetto `valuta_modello_completo`. | 8/10 | CPU locale |
| 04 | `04_derivate_gradiente.py` ✅ **completato** (16/06/2026, voto **8**/10) | Derivata come pendenza, derivata sigmoid (max 0.25, vanishing teaser), derivata ReLU (step, dying ReLU), gradiente come vettore. Semplificazione miracolosa BCE+sigmoid → `dL/dz = p - y`. Pipeline `derivate_check_completo` + mini-progetto `analizza_funzione_attivazione`. 16 mini-inline + 16 TODO. | 6-7/10 | CPU locale |
| 05 | `05_chain_rule_gd.py` ✅ **completato** (27/07/2026, voto ⏳ da confermare) | Chain rule a 2/3/n livelli, chain rule QUALITATIVA su rete 2-layer (le 5 derivate per dL/dW1), gradient descent 1D e nD, effetto LR, piano dei pesi. Pipeline `addestramento_via_gradiente_numerico` (mini-neurone) + mini-progetto `confronto_lr_su_addestramento`. 17 mini-inline + 16 TODO. | 7-8/10 | CPU locale |
| 06 | `06_backprop_training.py` 🟢 **in corso** (aperto 27/07/2026, con 5 blocchi 🔁 di rinforzo dal cap.05) | Forward con cache, backward step-by-step (i 5 step), `sanity_check_grad` numerico vs analitico, training loop. Pipeline `train_rete_2_layer_completo` + **mini-progetto finale `train_rete_su_csv_m2`** (rete addestrata vs LogReg M2) + **CONFRONTO PRIMA/DOPO cap.01-06**. 14 mini-inline + 19 TODO. **Pezzo più importante del primo blocco**. | 8/10 ⚠️ | CPU locale |
| 07 | `07_pytorch_intro.py` *(segnaposto)* | Tensori PyTorch, `Dataset`/`DataLoader`, training loop "vero". Si passa a **Google Colab** (GPU gratuita). | 8/10 | Colab |
| 08 | `08_cnn_computer_vision.py` *(segnaposto)* | CNN: conv2D, pooling, feature maps. Primo training su dataset pubblico low-stakes (Fashion-MNIST/CIFAR). Niente buste paga ancora. | 8/10 | Colab |
| 09 | `09_transfer_learning.py` *(segnaposto)* | Transfer learning con ResNet pre-addestrata + script `anonimizza_buste.py` + setup dataset reale (200 buste paga anonimizzate + 200 "altro"). | 7/10 | Colab |
| 10 | `10_progetto_gradio.py` *(segnaposto)* | Fine-tuning ResNet su busta-paga-vs-altro + demo Gradio + deploy HuggingFace Spaces. **Portfolio piece #2**. | 7/10 | Colab + HF Spaces |

**Tempo stimato**: 3-4 settimane (dopo lo split: andare graduali sui 4 mini-capitoli matematici 03-06).

## Quiz ripasso fondamentali tra capitoli (Regola 40)

**Obbligatorio dal Modulo 3**: dopo ogni capitolo e prima del successivo, completare il file bridge corrispondente nella cartella:

`modulo_03_dl_cv/quiz_ripasso_tra_capitoli/`

(~10 mini-esercizi facili ciascuno — Python, NumPy, Pandas, recall ML; soluzioni in coda ai file). Indice e naming in `quiz_ripasso_tra_capitoli/README.md`.

## Vincoli operativi (BLOCCANTI)

### Hardware
- AMD Vega 10 → **niente CUDA in locale**.
- Cap.01–06: tutto in NumPy + Matplotlib su CPU (nessun cambio di setup).
- **Da cap.07 in poi**: training su Google Colab. Workflow: codice in Cursor → notebook Colab per il training → modelli/risultati salvati in locale.
- **Da preparare prima del cap.07**: notebook Colab template con `torch` + `torchvision` + verifica GPU (`torch.cuda.is_available()`).

### Privacy / GDPR (deliverable cap.10)
1. Le buste paga reali NON si caricano mai su Colab/cloud nello stato originale.
2. Pipeline di **anonimizzazione PRIMA del training**: script locale `anonimizza_buste.py` che applica maschere nere o blur su nome, codice fiscale, IBAN, indirizzi (`cv2.rectangle`). Per il classificatore "busta paga vs altro" interessa il **layout grafico**, non il testo.
3. **`.gitignore`**: aggiungere `data/buste_*/` PRIMA di iniziare il cap.08 M3 (era cap.05 prima dello split). Mai committare buste paga (anche anonimizzate) nel repo.
4. Su Colab si caricano SOLO le immagini anonimizzate.

## Filo del progetto incrementale (M3)

Il modulo costruisce il **ramo visivo** del prodotto "Controllo Documentale AI":
- l'output del classificatore CNN (M3) → diventa una feature aggiuntiva (`prob_busta_paga_visivo`) nel classificatore supervisionato M2
- la pipeline cresce: M2 (regole + tabulare) + M3 (visivo) → M4 (estrazione testo) → M6 (RAG normativo)

## Cosa si "ricicla" da moduli precedenti

- **Ponte cap.01 (norma, coseno, dot product)** → cap.01 M3 (recall cross-modulo: il neurone è un dot product + bias + attivazione).
- **Ponte cap.02 (matrici, layer Dense)** → cap.02 M3 (literalmente: ogni layer è `X @ W + b`).
- **M2 cap.06–07 (Streamlit + deploy)** → cap.10 M3 stesso pattern, libreria diversa (Gradio invece di Streamlit, HuggingFace Spaces invece di Streamlit Cloud).

## Da NON dimenticare quando si crea ogni capitolo

Ogni capitolo M3 DEVE includere (regole del corso):
- Quiz d'ingresso + Quiz di verifica (1 domanda Feynman per quiz)
- **Quiz ripasso fondamentali tra capitoli** (`quiz_ripasso_tra_capitoli/…`) — da fare dopo la chiusura del capitolo precedente (**Regola 40**, `CONTESTO_CORSO.md`)
- 1 esercizio `🎯 [COLLOQUIO]`
- 1 `🔧 [REFACTORING]` + 1 `🔍 [DEBUG]`
- 1 `🧠 [RETRIEVAL]` + 1 `🔀 [INTERLEAVING]`
- 1 `🌊 [REAL-WORLD]` (regola dal M5 in poi — opzionale qui ma utile)
- Cap.01 M3: 1 `# 🔄 [RECALL CROSS-MODULO]` (regola 26 — obbligatorio dal M3 in poi)
- Sezione `🏗️ PROGETTO INCREMENTALE` (regola 12)
- Cap.10 M3: sezione `🔄 CONFRONTO PRIMA/DOPO` (ultimo capitolo del modulo). Sezione anticipata anche nel cap.06 (chiusura "primo blocco" full-NumPy cap.01-06 dopo lo split).
- Diario sessione `M03_C0X_*_sessione.md` aggiornato in append-only

## Note per il primo capitolo (cap.01 M3)

Quando arriverà il momento di creare il cap.01 M3, partire da:
1. Lettura `CONTESTO_CORSO.md` (gate iniziale).
2. Lettura del **diario di chiusura cap.02 Ponte** per capire le lacune ancora aperte.
3. Posizionare il primo `# 🔄 [RECALL CROSS-MODULO]` sul ponte cap.02 → cap.01 M3 (forward pass = `X @ W + b` con W matrice di pesi).
4. Mantenere il setup leggero (CPU + NumPy + Matplotlib): Colab si introduce solo dal cap.04.
