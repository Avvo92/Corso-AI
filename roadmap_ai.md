# Roadmap Completa — Corso AI per Web Developer

> **Obiettivo**: trasformare un Web Developer (HTML/CSS/JS/PHP/Laravel) in un **Full-Stack AI Engineer**
> capace di costruire, deployare e mantenere prodotti AI completi.
>
> **Profilo di arrivo**: professionista che sa collegare LLM, RAG e agenti a prodotti web reali —
> il profilo più ricercato nel mercato tech italiano ed europeo nel 2026.
>
> **Ultimo aggiornamento**: 22/02/2026 (integrazione obiettivo broker / MVP vendibile: § Modulo 10)

---

## Struttura del Corso — 10 Moduli + 3 Pilastri Trasversali

```
FONDAMENTA                    CORE AI                       PRODUZIONE
┌──────────────┐    ┌──────────────────────┐    ┌──────────────────────┐
│ M1: Python   │    │ M5: LLM & Prompt Eng │    │ M9: MLOps, Docker,   │
│    & Dati    │    │ M6: RAG Systems      │    │     Test & Deploy    │
│ M2: ML       │    │ M7: AI Agents        │    │ M10: Progetto Finale │
│ M3: DL & CV  │    │ M8: Fine-Tuning      │    │      Full-Stack AI   │
│ M4: NLP &    │    │                      │    │                      │
│   Embeddings │    │                      │    │                      │
└──────────────┘    └──────────────────────┘    └──────────────────────┘
        │                      │                          │
        └──────────────────────┼──────────────────────────┘
                               │
              ┌────────────────┼────────────────┐
              │     PILASTRI TRASVERSALI        │
              │                                 │
              │  🛠️  AI Tools Mastery            │
              │  🎯 Interview & System Design   │
              │  📦 Portfolio & Demo Strategy    │
              └─────────────────────────────────┘
```

---

## Timeline

| Mese | Moduli | Output concreto |
|------|--------|-----------------|
| **1** | M1 — Python & Dati | Base Python solida + Catalogo E-commerce v1 |
| **2** | M2 — ML + Ponte Matematico + M3 — DL & CV | 2 demo deployate (Streamlit + Gradio) + intuizioni matematiche |
| **3** | M4 — NLP + M5 — LLM & Prompt Eng. | 2 demo + competenze LLM operative |
| **4** | M6 — RAG + M7 — Agents | 2 demo + le 2 skill più richieste |
| **5** | M8 — Fine-Tuning + M9 — MLOps | Pipeline produzione completa |
| **6** | M10 — Progetto Finale | Prodotto full-stack deployato + portfolio completo |

**Totale**: ~6 mesi → profilo AI Engineer completo con 8 progetti deployati.

---

## Modulo 1 — Python & Dati

> **Stato**: in corso. Struttura già validata, 12 file.

**Obiettivo**: padroneggiare Python e la manipolazione dati — le fondamenta su cui si costruisce tutto.

| # | File | Concetto | Tempo stimato |
|---|------|----------|---------------|
| 01 | `01_benvenuto_python.py` | Variabili, tipi, print, f-string | 30-45 min |
| 02 | `02_condizioni_e_cicli.py` | if/else, for, while | 30-45 min |
| 03 | `03_funzioni.py` | Funzioni, parametri, return multipli | 45-60 min |
| 04 | `04_liste.py` | Liste, slicing, list comprehension | 45-60 min |
| 05 | `05_dizionari.py` | Dizionari, iterazione, nesting | 45-60 min |
| 06 | `06_file_csv.py` | Leggere file CSV "a mano" | 30-45 min |
| 07 | `07_numpy_intro.py` | Array NumPy — il mattone dell'AI | 60-90 min |
| 08 | `08_tensori_spiegati.py` | Cos'è un Tensor e perché ti serve | 60-90 min |
| 09 | `09_pandas_intro.py` | DataFrame — SQL in RAM | 60-90 min |
| 10 | `10_pandas_progetto.py` | Mini-progetto: analisi dati reale | 90-120 min |
| 11 | `11_matplotlib_grafici.py` | Grafici e visualizzazione dati | 45-60 min |
| 12 | `12_web_bridge.py` | FastAPI: il tuo primo endpoint AI | 60-90 min |

**Librerie**: numpy, pandas, matplotlib, fastapi, uvicorn

**Demo di modulo**: dashboard Matplotlib + endpoint FastAPI del catalogo.

**Tempo totale**: 3-4 settimane

---

## Modulo 2 — Machine Learning Fundamentals

**Obiettivo**: capire come un computer "impara" dai dati. Base concettuale per tutti i moduli successivi.

| # | File | Argomento | Perché serve |
|---|------|-----------|-------------|
| 01 | `01_cos_e_il_ml.py` | ML supervisionato, non supervisionato, reinforcement | Framework mentale per tutto il corso |
| 02 | `02_ciclo_ml.py` | Dati → preprocessing → split → train → evaluate | Processo usato anche con LLM |
| 03 | `03_regressione.py` | Regressione lineare + decision tree con Scikit-Learn | Cosa fa un modello "sotto il cofano" |
| 04 | `04_classificazione_metriche.py` | Random Forest, accuracy, precision, recall, F1 | Domande da colloquio garantite |
| 05 | `05_overfitting_validazione.py` | Overfitting, cross-validation, feature engineering | Concetti che tornano nel fine-tuning LLM |
| 06 | `06_progetto_streamlit.py` | Progetto: predittore prezzo case + prima demo Streamlit | Portfolio piece #1 |

**Librerie**: scikit-learn, streamlit

**Demo di modulo**: app Streamlit che prevede il prezzo di una casa. Deployata su Streamlit Cloud.

**Analogie ponte**: Scikit-Learn pipeline → middleware Laravel. Train/test split → staging/production.

**Tempo**: 2 settimane

---

## Ponte Matematico — 2 capitoli bridge tra M2 e M3

> **Stato**: da creare (si affronta dopo il completamento del M2)
>
> Questi 2 capitoli NON sono un modulo separato — sono un **ponte** tra il mondo ML
> (dove la matematica è nascosta dentro Scikit-Learn) e il mondo Deep Learning / NLP
> (dove servono intuizioni su vettori, gradienti e spazi). L'approccio resta invariato:
> codice Python prima, formula solo come "etichetta" di ciò che il codice fa.

| # | File | Argomento | Perché serve |
|---|------|-----------|-------------|
| 01 | `01_matematica_per_ai.py` | Vettori come liste, moltiplicazione matrice come loop annidato, dot product, similarità coseno — tutto in codice | Prerequisito per embeddings (M4), attention (M4), LoRA (M8) |
| 02 | `02_gradiente_discesa.py` | Derivata come "pendenza della collina", gradiente come "direzione di discesa", learning rate come "dimensione del passo" — visualizzato con Matplotlib | Prerequisito per backpropagation (M3), training loop (M3), loss function (M3) |

**Librerie**: numpy, matplotlib (già installate dal M1)

**Piattaforma**: CPU locale (nessuna GPU necessaria)

**Approccio didattico**:
- Ogni concetto matematico segue la sequenza: **analogia concreta → codice Python → grafico Matplotlib → formula** (la formula arriva ULTIMA, solo come etichetta)
- Esempio: "il dot product è come calcolare quanto due frecce puntano nella stessa direzione" → codice con `sum(a*b for a,b in zip(v1,v2))` → grafico con le frecce → formula `a · b = Σ aᵢbᵢ` (solo come etichetta)
- I 5-6 concetti coperti: vettore, matrice, moltiplicazione matriciale, dot product, similarità coseno, gradiente/derivata, discesa del gradiente

**Analogie ponte**: Vettore → array JS. Matrice → array di array. Dot product → il "punteggio di compatibilità" tra due prodotti. Gradiente → GPS che ricalcola la strada.

**Tempo**: 3-4 giorni

---

## Modulo 3 — Deep Learning & Computer Vision

**Obiettivo**: capire come funzionano le reti neurali. Prerequisito per capire Transformer e LLM.

| # | File | Argomento | Perché serve |
|---|------|-----------|-------------|
| 01 | `01_neurone_artificiale.py` | Il neurone come un `if` con pesi che si regolano | Base concettuale |
| 02 | `02_reti_neurali.py` | Layer, attivazione, forward pass | Cosa succede "dentro" un modello |
| 03 | `03_backpropagation.py` | Backpropagation (GPS che ricalcola dopo svolta sbagliata) | Colloquio: "spiega la backpropagation" |
| 04 | `04_pytorch_intro.py` | Tensori PyTorch, dataset, DataLoader, training loop | Framework standard dell'industria |
| 05 | `05_cnn_computer_vision.py` | CNN: filtri, pooling, feature maps — come un computer "vede" | Base per Computer Vision |
| 06 | `06_transfer_learning.py` | Modelli pre-addestrati (ResNet, YOLO), fine-tuning base | Nella pratica non si traina da zero quasi mai |
| 07 | `07_progetto_gradio.py` | Progetto: classificatore immagini + demo Gradio | Portfolio piece #2 |

**Librerie**: torch, torchvision, gradio

**Piattaforma**: **Google Colab** (GPU gratuita) — la GPU locale (AMD Vega 10) non supporta CUDA. Workflow: sviluppo codice in Cursor → training su Colab → risultati in locale.

**Demo di modulo**: classificatore immagini su Gradio/HuggingFace Spaces.

**Analogie ponte**: CNN filtri → CSS selettori (cercano pattern). Transfer learning → pacchetto npm pre-fatto.

**Tempo**: 2-3 settimane

---

## Modulo 4 — NLP, Embeddings & Transformers

**Obiettivo**: capire come il testo diventa numeri e come funzionano i modelli di linguaggio. Gli **embeddings** sono il concetto più importante dal M4 in poi.

| # | File | Argomento | Perché serve |
|---|------|-----------|-------------|
| 01 | `01_testo_come_numeri.py` | Tokenizzazione, bag of words, TF-IDF | Come il testo diventa numeri |
| 02 | `02_embeddings.py` | Word2Vec, sentence-transformers — "coordinate GPS del significato" | IL concetto chiave — prerequisito per RAG, vector DB, tutto |
| 03 | `03_similarita_coseno.py` | Misurare la "distanza" tra significati | Prerequisito per RAG e vector DB |
| 04 | `04_transformer_spiegato.py` | L'architettura Transformer ad alto livello (senza formule) | "Perché GPT funziona?" — domanda da colloquio |
| 05 | `05_huggingface_pipeline.py` | HuggingFace: pipeline, modelli pre-addestrati, tokenizer | L'ecosistema standard open-source |
| 06 | `06_sentiment_classificazione.py` | Sentiment analysis + classificazione testo | Applicazione pratica immediata |
| 07 | `07_progetto_recensioni.py` | Progetto: analizzatore recensioni e-commerce + Streamlit | Portfolio piece #3 |

**Librerie**: transformers, sentence-transformers, tokenizers

**Demo di modulo**: app Streamlit che analizza recensioni prodotti (sentiment, categorie, keyword).

**Analogie ponte**: Embedding → coordinate GPS. Tokenizer → `split()` intelligente. HuggingFace → npm dell'AI.

**Tempo**: 2 settimane

---

## Modulo 5 — LLM Integration & Prompt Engineering

**Obiettivo**: passare da "uso ChatGPT" a "costruisco prodotti con le API LLM". Skill #2 più richiesta al mondo (+135.8% crescita).

| # | File | Argomento | Perché serve |
|---|------|-----------|-------------|
| 01 | `01_api_openai.py` | Setup, autenticazione, chat completions, modelli | La base di tutto |
| 02 | `02_prompt_engineering.py` | Zero-shot, few-shot, chain-of-thought, delimitatori | Skill #2 globale |
| 03 | `03_structured_output_pydantic.py` | Structured Outputs + Pydantic: risposte JSON con schema validato | Elimina il 90% dei bug in produzione |
| 04 | `04_function_calling.py` | L'LLM "chiama" le tue funzioni Python | Ponte tra linguaggio naturale e codice |
| 05 | `05_streaming_errori.py` | Streaming risposte + gestione errori + rate limiting | UX reattiva + robustezza |
| 06 | `06_ollama_modelli_locali.py` | Ollama + modelli open-source: deployment locale, API vs locale | Strategia costi + privacy |
| 07 | `07_multimodale_vision.py` | Inviare immagini all'LLM (GPT-4o Vision) | Trend in crescita — testo + visione |
| 08 | `08_costi_caching.py` | Scelta modello, caching, batching, semantic caching (concetto) | Costi esplodono senza ottimizzazione |
| 09 | `09_sicurezza_ai.py` | Prompt injection, input sanitization, guardrails, content filtering | Non negoziabile in produzione |
| 10 | `10_progetto_assistente.py` | Progetto: assistente e-commerce con function calling + Streamlit | Portfolio piece #4 |

**Librerie**: openai, pydantic-ai, ollama

**Piattaforma**: CPU locale. Ollama con modelli fino a 3B parametri (Phi-3 Mini, Qwen2) per esercizi gratuiti + API OpenAI per esercizi che richiedono qualita superiore.

**Demo di modulo**: assistente AI e-commerce con function calling per cercare prodotti, controllare stock, calcolare preventivi — risposte in streaming.

**Analogie ponte**: Function calling → API REST endpoint (l'LLM fa la richiesta). Structured output → validazione form. Prompt → query SQL (istruisci il "database" a restituire ciò che vuoi).

**Tempo**: 2-3 settimane

---

## Modulo 6 — RAG Systems

**Obiettivo**: costruire un RAG completo da zero. **Skill #1 più richiesta** — 74.5% delle job posting AI.

| # | File | Argomento | Perché serve |
|---|------|-----------|-------------|
| 01 | `01_perche_rag.py` | Limiti degli LLM: conoscenza ferma, allucinazioni, niente dati privati | Il "problema" che RAG risolve |
| 02 | `02_document_loading.py` | Caricare PDF, CSV, Markdown, pagine web | L'input del sistema |
| 03 | `03_chunking_strategies.py` | Dimensione fissa, ricorsivo, semantico | La qualità del RAG dipende all'80% dal chunking |
| 04 | `04_chromadb_vector_store.py` | ChromaDB: collection, inserimento, query, metadata filtering | Lo storage degli embedding |
| 05 | `05_pipeline_completo.py` | Query → embedding → retrieval → prompt augmentation → LLM → risposta | Architettura end-to-end |
| 06 | `06_langchain_basics.py` | LangChain: chain, retriever, prompt template, output parser | Il framework standard per RAG |
| 07 | `07_hybrid_search.py` | Ricerca semantica + keyword (BM25) combinati | Migliora la qualità del retrieval |
| 08 | `08_ragas_evaluation.py` | RAGAS: faithfulness, answer relevancy, context precision | 65% delle app LLM falliscono senza valutazione |
| 09 | `09_langsmith_observability.py` | LangSmith: tracing, debugging, monitoraggio pipeline | Sapere PERCHÉ il RAG ha risposto male |
| 10 | `10_progetto_rag.py` | Progetto: assistente documentale RAG + Streamlit | Portfolio piece #5 |

**Librerie**: langchain, langchain-community, chromadb, ragas, langsmith

**Demo di modulo**: assistente documentale che risponde a domande su una knowledge base con metriche di qualità visibili.

**Principio "concetti prima, framework dopo"**: il file 05 (pipeline completo) costruisce un RAG da zero con puro Python + ChromaDB — senza LangChain. Solo dal file 06 si introduce LangChain come astrazione. Così se LangChain cambia API (è già successo 3 volte in 2 anni), i concetti restano.

**Analogie ponte**: Vector DB → database SQL, ma cerca per significato. Chunking → paginazione API. RAG pipeline → middleware Laravel (intercetta, arricchisce, passa al controller).

**Tempo**: 2-3 settimane

---

## Modulo 7 — AI Agents & Automation

**Obiettivo**: costruire agenti che ragionano, usano strumenti, e completano task multi-step. Il 67% delle grandi aziende usa agenti AI in produzione.

| # | File | Argomento | Perché serve |
|---|------|-----------|-------------|
| 01 | `01_agenti_vs_workflow.py` | Cos'è un agente vs un workflow (collega autonomo vs checklist) | Framework mentale |
| 02 | `02_langgraph_intro.py` | LangGraph: grafi, nodi, edge, stato, conditional routing | Framework standard per agenti |
| 03 | `03_tool_use.py` | Dare all'agente strumenti (API, database, file, web search) | L'agente diventa utile quando agisce nel mondo reale |
| 04 | `04_memoria_stato.py` | Agente con memoria: stato persistente, contesto tra interazioni | Conversazioni che "ricordano" |
| 05 | `05_pattern_avanzati.py` | ReAct, Plan-and-Execute, Reflection | I pattern usati in produzione |
| 06 | `06_multi_agent.py` | Agenti che collaborano (intro a CrewAI) | Sistemi complessi con agenti specializzati |
| 07 | `07_mcp_server.py` | MCP: come funziona + costruire un MCP server custom | Capisci Cursor + sai estenderlo |
| 08 | `08_agentic_rag.py` | RAG dove l'agente decide QUANDO e COME cercare | Evoluzione del RAG classico |
| 09 | `09_progetto_agente.py` | Progetto: agente di ricerca e analisi + Streamlit | Portfolio piece #6 |

**Librerie**: langgraph, langchain, crewai

**Demo di modulo**: agente che cerca informazioni, le analizza, e produce un report strutturato con fonti.

**Principio "concetti prima, framework dopo"**: il file 01-03 costruiscono un agente con puro Python (loop, tool use manuale, stato). Solo dal file 04 si introduce LangGraph come framework. CrewAI (file 06) è introduttivo — il focus è sui concetti di multi-agent, non sul framework specifico.

**Analogie ponte**: Agente → collega junior che segue istruzioni ma decide come. LangGraph → state machine. MCP → API REST che Cursor usa per parlare con i tuoi strumenti.

**Tempo**: 2-3 settimane

---

## Modulo 8 — Fine-Tuning & Personalizzazione Modelli

**Obiettivo**: adattare un modello ai tuoi dati specifici. Skill specializzata a più alto salario ($250K-$350K+).

| # | File | Argomento | Perché serve |
|---|------|-----------|-------------|
| 01 | `01_quando_fare_cosa.py` | Fine-tuning vs RAG vs prompt engineering — decision framework | La domanda da colloquio #1 |
| 02 | `02_preparazione_dataset.py` | Formato, pulizia, bilanciamento, qualità dati | "Garbage in, garbage out" |
| 03 | `03_lora_spiegato.py` | LoRA: cos'è e perché funziona (aggiungere una stanza, non ristrutturare) | 99% riduzione parametri |
| 04 | `04_qlora_pratico.py` | QLoRA: fine-tuning su hardware consumer (6-10GB VRAM) | Democratizza il fine-tuning |
| 05 | `05_training_peft.py` | Training con PEFT + Transformers + bitsandbytes | Hands-on completo |
| 06 | `06_valutazione_merge.py` | Valutazione modello fine-tunato + merge adapter | Verificare che il fine-tuning funziona |
| 07 | `07_progetto_finetuning.py` | Progetto: modello per descrizioni e-commerce + demo comparativa | Portfolio piece #7 |

**Librerie**: peft, bitsandbytes, trl, transformers, datasets

**Piattaforma**: **Google Colab** (GPU gratuita) — QLoRA richiede GPU NVIDIA. Workflow: preparazione dataset in locale → training su Colab → valutazione e demo in locale/HuggingFace Spaces.

**Demo di modulo**: confronto interattivo tra modello base e modello fine-tunato sullo stesso task.

**Analogie ponte**: LoRA → aggiungere una stanza alla casa senza ristrutturare. Dataset → dati di training come training set di un nuovo assunto. Adapter → plugin WordPress (componente aggiuntivo, non modifica il core).

**Tempo**: 1-2 settimane

---

## Modulo 9 — MLOps, Testing, Docker & Deploy

**Obiettivo**: portare un progetto AI dalla tua macchina al mondo reale. L'87% dei modelli ML non arriva mai in produzione. Tu sarai nel 13%.

| # | File | Argomento | Perché serve |
|---|------|-----------|-------------|
| 01 | `01_async_python.py` | asyncio, async/await in FastAPI, event loop | Prerequisito per servizi AI performanti |
| 02 | `02_docker_fondamentali.py` | Container, Dockerfile, docker-compose, multi-stage build | Il tuo codice gira ovunque, identico |
| 03 | `03_containerizzare_ai.py` | FastAPI + modello AI + ChromaDB in container | Stack completo in container |
| 04 | `04_testing_ai.py` | Unit test, integration test, semantic evaluation, LLM-as-judge | 65% delle app LLM falliscono senza testing |
| 05 | `05_github_actions_cicd.py` | Build automatica, test, deploy su push | Workflow professionale |
| 06 | `06_deploy_cloud.py` | Railway/Render/Fly.io (tier gratuiti) | Link live nel CV = 10x un repo statico |
| 07 | `07_monitoring_logging.py` | Health checks, logging strutturato, alerting | Sapere quando qualcosa si rompe |
| 08 | `08_semantic_caching.py` | Redis + caching semantico: ridurre costi LLM del 70-80% | Ottimizzazione costi in produzione |
| 09 | `09_progetto_deploy.py` | Progetto: dockerizzare e deployare il RAG del M6 come servizio live | Portfolio piece #8 |

**Librerie**: docker, redis, pytest, httpx, github actions (yaml)

**Demo di modulo**: il RAG del Modulo 6, containerizzato, deployato su cloud, con CI/CD, monitoring, e caching.

**Analogie ponte**: Docker → `node_modules` per l'intero OS. CI/CD → deployment pipeline Laravel Forge/Envoyer. Health check → ping monitoring. Redis cache → cache Laravel.

**Tempo**: 2 settimane

---

## Modulo 10 — Progetto Finale: Full-Stack AI Product

**Obiettivo**: costruire IL prodotto del portfolio — il diamante. Un prodotto AI completo, deployato, con demo live, documentazione professionale, e video demo.

**Dominio applicativo** (allineato a Gianluca): **due applicativi** sullo stesso spettro documentale — **Validator** (controllo fascicolo) e **Replicator** (generazione PDF **vettoriale** fedele **a schermo**, transfer X→Y, imputazione, **QA dual-channel vettoriale+raster** — `docs/prodotto/APPUNTI_APPLICATIVO_REPLICATOR.md` §4.3). Indice: `docs/prodotto/README.md` (stub root: `APPUNTI_APPLICATIVO.md`); piano e spettro in `docs/prodotto/`. Contesto **broker/intermediazione mutui**. M10: deploy di entrambe le app; Replicator P0 = `busta_paga` + `transfer_xy` (hold-out QA V+R). Monetizzazione verso terzi fuori syllabus; codice modulare e configurabile.

### Architettura

```
┌─────────────────────────────────┐
│         Frontend React          │
│    (Vercel AI SDK / Next.js)    │
│  Streaming • Chat UI • Auth    │
└──────────────┬──────────────────┘
               │ API calls
┌──────────────▼──────────────────┐
│        Backend (FastAPI)        │
│  Auth • Business Logic • DB    │
└──────────────┬──────────────────┘
               │ Internal API
┌──────────────▼──────────────────┐
│      AI Microservice (FastAPI)  │
│  ┌─────────┐  ┌──────────────┐ │
│  │   RAG   │  │  AI Agent    │ │
│  │ChromaDB │  │  LangGraph   │ │
│  └─────────┘  └──────────────┘ │
│  ┌─────────────────────────────┐│
│  │ LLM (OpenAI / Ollama)      ││
│  │ Structured Output (Pydantic)││
│  │ Function Calling            ││
│  │ Semantic Cache (Redis)      ││
│  └─────────────────────────────┘│
└──────────────┬──────────────────┘
               │
┌──────────────▼──────────────────┐
│     Docker Compose → Cloud     │
│  CI/CD • Monitoring • Logs     │
└─────────────────────────────────┘
```

### Fasi del progetto

| Fase | Settimana | Cosa fai |
|------|-----------|----------|
| 0. Setup Git workflow | 0 | Feature branches, conventional commits, template PR — simulazione lavoro in team |
| 1. Progettazione | 1 | Architettura, schema DB, user stories, API design |
| 2. AI Service | 1-2 | RAG pipeline + Agent system + LLM integration |
| 3. Backend | 2 | FastAPI endpoints, autenticazione, business logic |
| 4. Frontend | 2-3 | React UI con streaming, chat, dashboard |
| 5. Integrazione | 3 | Frontend ↔ Backend ↔ AI service end-to-end |
| 6. Docker + Deploy | 3-4 | Containerizzazione, CI/CD, deploy live |
| 7. Polish | 4 | Error handling, loading states, edge cases, testing |
| 8. Portfolio | 4 | README, architettura diagram, video demo, profilo GitHub |

**Simulazione team workflow**: il progetto M10 usa feature branches, PR con descrizione strutturata, code review dall'AI mentor, e conventional commits. Ogni fase (AI service, backend, frontend, deploy) ha il suo branch e la sua PR — come in un team reale.

**Output finale**: link live + repo GitHub + README professionale + video demo 2 minuti + storico PR con code review.

**Tempo**: 3-4 settimane

---

## Pilastri Trasversali

### 🛠️ AI Tools Mastery (integrato in ogni modulo)

| Modulo | Skill AI Tools |
|--------|---------------|
| M1-M4 | Cursor: rules, agent mode, context management |
| M5 | Prompt engineering per il TUO workflow (non solo per i prodotti) |
| M6 | Cursor come strumento di debug per pipeline RAG |
| M7 | Costruire un MCP server custom — capisci come funziona Cursor e sai estenderlo |
| M8 | Usare AI per generare e validare dataset di training |
| M9 | GitHub Actions + workflow automatizzati |
| M10 | Flusso completo: Cursor → GitHub → CI/CD → deploy automatico |

### 🎯 Interview & System Design Readiness (dal M2 in poi)

Esercizi allineati alle domande reali dei colloqui AI Engineer 2026 (60%+ GenAI-focused):

| Modulo | Domande da colloquio coperte |
|--------|------------------------------|
| M2 | "Spiega bias-variance tradeoff", "Cos'è overfitting?", "Che metrica per classificatore sbilanciato?" |
| M3 | "Spiega backpropagation con parole tue", "Cos'è il transfer learning e quando lo usi?" |
| M4 | "Cos'è un embedding?", "Come funziona un Transformer ad alto livello?" |
| M5 | "Progetta un chatbot customer service", "Cos'è il function calling?", "Cos'è il prompt injection?" |
| M6 | "Progetta un RAG per 10M documenti", "Come valuteresti la qualità del retrieval?" |
| M7 | "Progetta un agente che gestisce ordini", "Quando workflow vs agente?" |
| M8 | "Quando fine-tuning vs RAG vs prompt engineering?", "Cos'è LoRA?" |
| M9 | "Come deployeresti un servizio LLM?", "Come gestisci i costi in produzione?" |

Ogni modulo ha: almeno 2 esercizi `🎯 [COLLOQUIO]` + dal M5 in poi almeno 1 esercizio `📐 [SYSTEM DESIGN]`.

### 📦 Portfolio & Demo Strategy (dal M2 in poi)

| # | Progetto | Modulo | Deploy | Cosa dimostra |
|---|----------|--------|--------|---------------|
| 1 | Predittore prezzo case | M2 | Streamlit Cloud | ML classico, Streamlit |
| 2 | Classificatore immagini | M3 | HuggingFace Spaces | Deep Learning, Gradio |
| 3 | Analizzatore recensioni | M4 | Streamlit Cloud | NLP, embeddings |
| 4 | Assistente e-commerce AI | M5 | Streamlit Cloud | LLM API, function calling |
| 5 | RAG documentale | M6 | Streamlit Cloud | RAG, vector DB, evaluation |
| 6 | Agente di ricerca | M7 | Streamlit Cloud | AI agents, LangGraph |
| 7 | Demo fine-tuning | M8 | HuggingFace Spaces | LoRA, comparison |
| 8 | Prodotto full-stack AI | M10 | Cloud (Railway/Render) | TUTTO — il diamante |

**3-5 progetti deployati battono qualsiasi certificazione.** I recruiter passano 10 secondi sul CV ma si fermano 80% di più su GitHub con codice eseguibile.

---

## Copertura Skill Mercato 2026

| Skill | % job posting | Modulo |
|-------|--------------|--------|
| RAG | 74.5% | M6 + M7 |
| Python | 65.1% | M1 + tutto |
| Prompt Engineering | #2 globale (+135.8%) | M5 |
| NLP | +155% | M4 |
| AI Agents | 31.6%, $10.86B | M7 |
| LLM Fine-Tuning | $250K-$350K+ | M8 |
| MLOps / Deploy | 87% modelli falliscono | M9 |
| Docker | Prerequisito | M9 |
| AI Security | Crescente | M5 + M9 |
| Evaluation / Observability | Critica | M6 + M9 |
| Function calling / Structured output | Standard | M5 |
| Vector DB / Embeddings | Prerequisito RAG | M4 + M6 |
| System design AI | Colloqui senior | Trasversale (M5+) |
| Streaming / Async | Produzione | M5 + M9 |
| CI/CD | Professionale | M9 |
| Open-source / Ollama | Strategia costi | M5 |
| Multimodale | Trend crescita | M5 |
| Semantic caching | Ottimizzazione | M9 |
| Full-stack integration | Raro e ricercatissimo | M10 |
| Portfolio / Demo | Requisito pratico | Trasversale |

**Copertura: 20/20 skill. Zero lacune.**

---

## Nota Strutturale — File Lunghi e Jupyter

I moduli avanzati (dal M2 in poi) possono avere capitoli complessi che superano le 400 righe.
In questi casi:
- **Split in due file**: `XXa_teoria.py` (spiegazione + mini-esercizi) e `XXb_pratica.py` (esercizi + progetto + soluzioni)
- **Jupyter Notebook**: per i moduli dove la visualizzazione inline migliora l'apprendimento (M3: curve di loss, M4: embedding visualizzati, Ponte Matematico: grafici Matplotlib), usare `.ipynb` al posto di `.py`
- La scelta va fatta capitolo per capitolo in base al contenuto

---

## Approccio Didattico (invariato per tutti i moduli)

Ogni capitolo di ogni modulo segue le stesse regole validate nel Modulo 1:

1. **Lingua**: italiano, tono da collega senior, dare del "tu"
2. **Sequenza**: analogia concreta → codice JS/PHP (o analogia web) → codice Python → esercizio
3. **Struttura file**: docstring → quiz ingresso → sezioni teoria con mini-esercizi → quiz verifica → esercizi → progetto incrementale → soluzioni
4. **Quiz**: 2 per capitolo (ingresso + verifica), 6 formati (output, V/F, errore, definizione, completa codice, Feynman)
5. **Esercizi speciali**: `[COLLOQUIO]`, `[REFACTORING]`, `[INTERLEAVING]`, `[RETRIEVAL]`, `[SYSTEM DESIGN]` (dal M5), `[DEBUG]` (dal M2), `[REAL-WORLD]` (dal M5), `[RECALL CROSS-MODULO]` (dal M3)
6. **Spaced repetition**: glossario con contatore, ripasso programmato, rinforzo mirato dalle lacune quiz
7. **Scala di aiuto**: indica zona → spiega perché → esempio analogo → soluzione
8. **Voto difficoltà** obbligatorio dopo ogni capitolo
9. **Progetto incrementale** a fine capitolo

Per i concetti AI senza equivalente JS/PHP (embedding, backpropagation, RAG, ecc.), i confronti a tre lingue sono sostituiti da **analogie dal mondo web/e-commerce** che Gianluca conosce.
