# Mappatura dettagliata — Libri ↔ Moduli/Capitoli

> Usare questo file quando si prepara o revisiona un capitolo.
> I numeri di capitolo si riferiscono all’**edizione PDF in `books/`** (Géron ≈ 3ª ed.; verificare titolo sezione nel sommario).

---

## M3 — Deep Learning & Computer Vision

### `07_pytorch_intro.py` (chiuso anticipata 13/08/2026)

> PDF locale = **PYTORCH 1ª ed.** (Stevens et al. 2020). Schede: `schede/M03_C07_*`.

| Sezione corso | Concetto | [PYTORCH] 1ª ed. | [GERON] | Note mentor |
|---------------|----------|------------------|---------|-------------|
| Sez. 1 Tensori | ndarray vs Tensor, dtype, device | cap. 3–4 | cap. 12 intro | 📚 già dopo dizionario |
| Sez. 2 Autograd | `requires_grad`, `.backward()` | cap. 5 | — | 📚 + scheda puntatori |
| Sez. 3 `nn.Module` | Linear, forward | cap. 6 | cap. 10 | 📚 |
| Sez. 4 DataLoader | Dataset, batch, shuffle | cap. 1 overview, 7–8 | — | 📚 |
| Sez. 5 Training loop | zero_grad→step | cap. 5–6, §8.4 inizio | cap. 10–11 | 📚; `.item()` |
| Sez. 6 state_dict | save/load pesi | **§8.4.2–8.4.3**, §13.6.6 | cap. 10 save Keras | scheda piena + 📚 [LIBRO] |

**Esercizio 📚 [LIBRO] (Sez. 6):** checkpoint dict `{model_state, nota, d, h}` ispirato a §13.6.6 — senza `optimizer_state`.

---

### `08_cnn_computer_vision.py` (scritto 13/08/2026)

> Scheda: `schede/M03_C08_cnn.md`. **1ª ed. PYTORCH** = cap. **7–8** (non 10–11 della 2ª ed.).

| Concetto | [PYTORCH] 1ª ed. | [GERON] |
|----------|------------------|---------|
| Dataset CV, tensore C×H×W, limite FC | Cap. 7 *birds/airplanes* | Cap. 14 intro |
| Conv2d, pooling, feature maps | Cap. 8 §8.1–8.2 | Cap. 14 Convolutional Layers |
| Primo training (Fashion-MNIST) | Cap. 8 adattato (noi: Fashion vs CIFAR) | Cap. 14 es. |

---

### `09_transfer_learning.py`

| Concetto | [PYTORCH] | [GERON] |
|----------|-----------|---------|
| ResNet, freeze layers | cap. 12–13 | cap. 14 |
| Fine-tuning head | cap. 13 | cap. 14 |

**Prodotto:** script anonimizzazione — non coperto dai libri; resta task corso.

---

### `10_progetto_gradio.py`

| Concetto | [PYTORCH] | [GERON] |
|----------|-----------|---------|
| Inferenza, deploy demo | cap. 14+ | cap. 19 |
| Gradio | — | confronto Streamlit cap. M2 |

---

## M4 — NLP & Embeddings

| Capitolo corso (previsto) | [ALAMMAR] | [NLP-TRANS] |
|---------------------------|-----------|-------------|
| Token, embedding | cap. 2 | cap. 1–2 |
| Transformer (intuizione) | cap. 1 + blog Illustrated | cap. 3–4 |
| sentence-transformers | cap. 2–3 | cap. 5+ |
| Estrazione campi OCR | cap. 4 (applicazioni) | cap. 8+ |

---

## M5 — LLM & Prompt Engineering

| Tema | [HUYEN-AIE] | [ALAMMAR] |
|------|-------------|-----------|
| Stack LLM, API | Part I | Part 1 |
| Prompt engineering | cap. prompt | Part 2 |
| Structured output | evaluation / parsing | — |
| Function calling | tool use | — |
| Costi / Ollama vs API | deployment, cost | — |

---

## M6 — RAG

| Tema | [HUYEN-AIE] | [ALAMMAR] |
|------|-------------|-----------|
| Chunking, retrieval | RAG chapters | Part 2 RAG |
| Vector DB | embedding pipeline | semantic search |
| Evaluation (RAGAS) | eval frameworks | — |
| **Prodotto Validator** normativo | citazioni obbligatorie | grounding |

---

## M7 — AI Agents

| Tema | [HUYEN-AIE] |
|------|-------------|
| Agenti, tool use | agent / orchestration sections |
| Agentic RAG | RAG + agenti |

---

## Ripasso trasversale (on demand)

| Lacuna / bisogno | Libro | Capitoli indicativi |
|------------------|-------|---------------------|
| Pipeline sklearn, CV, leakage | GERON | 1–9 |
| Metriche, statistiche | STATS | 1–5 |
| Shape, matmul | LINALG / MML | Ponte già fatto; consulto |
| Colloquio DL teoria | GERON 10–11 | + PYTORCH 5–6 |

---

## Retrofit capitoli già chiusi

| Capitolo | Azione |
|----------|--------|
| M3 cap.01–06 | **Non modificare** (protocollo H). Citazioni libro solo **in chat** su richiesta. |
| M2 | Citazioni GERON in chat; opzionale mini-pacchetto 📚 in archivio M2 (non prioritario). |
| M3 cap.07+ | Inserire blocchi 📚 in revisione o alla prossima passata sezione per sezione. |
