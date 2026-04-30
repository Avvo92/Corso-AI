# Modulo 3 — Deep Learning & Computer Vision

> **Stato**: ⬜ DA CREARE (pianificato).
> I file `.py` di questo modulo sono al momento **solo segnaposto con TODO MENTOR**: vanno completati uno alla volta, **alla chiusura del capitolo precedente**, come da protocollo del corso.
> Vedi `CONTESTO_CORSO.md` → sezione "Computer Vision nel Prodotto" per la decisione 30/04/2026 sul deliverable cap.07.

## Obiettivo del modulo

Capire come funzionano davvero le reti neurali (non più "Scikit-Learn nasconde tutto") e arrivare a un classificatore CNN deployato come **secondo URL portfolio** (Gradio + HuggingFace Spaces).

## Demo finale di portfolio

Classificatore visivo **busta paga vs non-busta paga** + demo Gradio deployata. Output integrabile come feature aggiuntiva nel modello supervisionato del Modulo 2.

## Indice capitoli

| # | File | Argomento | Difficoltà attesa | Piattaforma |
|---|------|-----------|-------------------|-------------|
| 01 | `01_neurone_artificiale.py` | Neurone come "if con pesi", attivazioni (sigmoid, ReLU), forward pass a mano in NumPy. **Recall cross-modulo** dal Ponte Matematico. | 6/10 | CPU locale |
| 02 | `02_reti_neurali.py` | Layer impilati = sequenza di `X @ W + b` (cap.02 Ponte) + attivazioni; rete full-NumPy che classifica le pratiche del CSV M2. | 7/10 | CPU locale |
| 03 | `03_backpropagation.py` | Gradiente, chain rule, discesa del gradiente. **Capitolo più tosto del modulo** (probabile 9/10). Tutto in NumPy + plot loss. | 9/10 ⚠️ | CPU locale |
| 04 | `04_pytorch_intro.py` | Tensori PyTorch, `Dataset`/`DataLoader`, training loop "vero". Si passa a **Google Colab** (GPU gratuita). | 8/10 | Colab |
| 05 | `05_cnn_computer_vision.py` | CNN: conv2D, pooling, feature maps. Primo training su dataset pubblico low-stakes (Fashion-MNIST/CIFAR). Niente buste paga ancora. | 8/10 | Colab |
| 06 | `06_transfer_learning.py` | Transfer learning con ResNet pre-addestrata + script `anonimizza_buste.py` + setup dataset reale (200 buste paga anonimizzate + 200 "altro"). | 7/10 | Colab |
| 07 | `07_progetto_gradio.py` | Fine-tuning ResNet su busta-paga-vs-altro + demo Gradio + deploy HuggingFace Spaces. **Portfolio piece #2**. | 7/10 | Colab + HF Spaces |

**Tempo stimato**: 2-3 settimane.

## Vincoli operativi (BLOCCANTI)

### Hardware
- AMD Vega 10 → **niente CUDA in locale**.
- Cap.01–03: tutto in NumPy + Matplotlib su CPU (nessun cambio di setup).
- **Da cap.04 in poi**: training su Google Colab. Workflow: codice in Cursor → notebook Colab per il training → modelli/risultati salvati in locale.
- **Da preparare prima del cap.04**: notebook Colab template con `torch` + `torchvision` + verifica GPU (`torch.cuda.is_available()`).

### Privacy / GDPR (deliverable cap.07)
1. Le buste paga reali NON si caricano mai su Colab/cloud nello stato originale.
2. Pipeline di **anonimizzazione PRIMA del training**: script locale `anonimizza_buste.py` che applica maschere nere o blur su nome, codice fiscale, IBAN, indirizzi (`cv2.rectangle`). Per il classificatore "busta paga vs altro" interessa il **layout grafico**, non il testo.
3. **`.gitignore`**: aggiungere `data/buste_*/` PRIMA di iniziare il cap.05 M3. Mai committare buste paga (anche anonimizzate) nel repo.
4. Su Colab si caricano SOLO le immagini anonimizzate.

## Filo del progetto incrementale (M3)

Il modulo costruisce il **ramo visivo** del prodotto "Controllo Documentale AI":
- l'output del classificatore CNN (M3) → diventa una feature aggiuntiva (`prob_busta_paga_visivo`) nel classificatore supervisionato M2
- la pipeline cresce: M2 (regole + tabulare) + M3 (visivo) → M4 (estrazione testo) → M6 (RAG normativo)

## Cosa si "ricicla" da moduli precedenti

- **Ponte cap.01 (norma, coseno, dot product)** → cap.01 M3 (recall cross-modulo: il neurone è un dot product + bias + attivazione).
- **Ponte cap.02 (matrici, layer Dense)** → cap.02 M3 (literalmente: ogni layer è `X @ W + b`).
- **M2 cap.06–07 (Streamlit + deploy)** → cap.07 M3 stesso pattern, libreria diversa (Gradio invece di Streamlit, HuggingFace Spaces invece di Streamlit Cloud).

## Da NON dimenticare quando si crea ogni capitolo

Ogni capitolo M3 DEVE includere (regole del corso):
- Quiz d'ingresso + Quiz di verifica (1 domanda Feynman per quiz)
- 1 esercizio `🎯 [COLLOQUIO]`
- 1 `🔧 [REFACTORING]` + 1 `🔍 [DEBUG]`
- 1 `🧠 [RETRIEVAL]` + 1 `🔀 [INTERLEAVING]`
- 1 `🌊 [REAL-WORLD]` (regola dal M5 in poi — opzionale qui ma utile)
- Cap.01 M3: 1 `# 🔄 [RECALL CROSS-MODULO]` (regola 26 — obbligatorio dal M3 in poi)
- Sezione `🏗️ PROGETTO INCREMENTALE` (regola 12)
- Cap.07 M3: sezione `🔄 CONFRONTO PRIMA/DOPO` (ultimo capitolo del modulo)
- Diario sessione `M03_C0X_*_sessione.md` aggiornato in append-only

## Note per il primo capitolo (cap.01 M3)

Quando arriverà il momento di creare il cap.01 M3, partire da:
1. Lettura `CONTESTO_CORSO.md` (gate iniziale).
2. Lettura del **diario di chiusura cap.02 Ponte** per capire le lacune ancora aperte.
3. Posizionare il primo `# 🔄 [RECALL CROSS-MODULO]` sul ponte cap.02 → cap.01 M3 (forward pass = `X @ W + b` con W matrice di pesi).
4. Mantenere il setup leggero (CPU + NumPy + Matplotlib): Colab si introduce solo dal cap.04.
