# Roadmap Completa — Corso AI per Web Developer

> **Obiettivo**: trasformare un Web Developer (HTML/CSS/JS/PHP/Laravel) in un **Full-Stack AI Engineer**
> capace di costruire, deployare e mantenere prodotti AI completi.
>
> **Profilo di arrivo**: professionista che sa collegare LLM, RAG e agenti a prodotti web reali —
> il profilo più ricercato nel mercato tech italiano ed europeo nel 2026.
>
> **Ultimo aggiornamento**: 28/07/2026 — **revisione di allineamento al mercato**. Verificata contro le roadmap
> AI Engineer 2026 pubbliche, lo stato dei framework per agenti, il fine-tuning e i dati occupazionali.
> Modifiche principali: nuovo capitolo **Context Engineering** (M6-10), strato **multi-provider** e decisione
> **contesto lungo vs RAG** (M5), reranking e pgvector (M6), sicurezza MCP (M7), DPO/GRPO/RFT (M8),
> sezione mercato riscritta con dati 2026 e forbici salariali italiane.
> Revisione precedente: 22/02/2026 (integrazione obiettivo broker / MVP vendibile: § Modulo 10).

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

**Totale**: **6-9 mesi** → profilo AI Engineer completo con 8 progetti deployati.

> **Nota sulla timeline (rev. 28/07/2026)**: i 6 mesi restano il piano "a pieno ritmo". Le roadmap indipendenti
> 2026 indicano 6-12 mesi (8-12 per chi parte da zero; tu parti da sviluppatore web, quindi nella fascia bassa).
> Il ritmo reale dei primi 3 moduli suggerisce **8-9 mesi** come previsione onesta. Non è un problema:
> il vincolo vero è arrivare ai moduli M5-M7 (LLM, RAG, agenti) con basi solide, non arrivarci in fretta.

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

> **⚠️ Aggiornamento 27/05/2026**: il vecchio `03_backpropagation.py` (monolitico, atteso 9/10 di difficoltà, giudicato "troppo denso" dallo studente) è stato spezzato in **4 sotto-capitoli** (03 loss → 04 derivate → 05 chain rule + GD → 06 backprop + training). I successivi sono stati rinumerati (04→07, 05→08, 06→09, 07→10). Il modulo M3 passa da 7 a **10 capitoli**.

| # | File | Argomento | Perché serve |
|---|------|-----------|-------------|
| 01 | `01_neurone_artificiale.py` | Il neurone come un `if` con pesi che si regolano | Base concettuale |
| 02 | `02_reti_neurali.py` | Layer, attivazione, forward pass | Cosa succede "dentro" un modello |
| 03 | `03_loss.py` | LOSS (BCE, MSE) come misura continua e derivabile dell'errore | Senza questo non puoi minimizzare nulla |
| 04 | `04_derivate_gradiente.py` | Derivata = pendenza, gradiente = vettore di derivate parziali | Linguaggio della correzione (preparazione backprop) |
| 05 | `05_chain_rule_gd.py` | Chain rule + gradient descent + learning rate | Come si applica la correzione su funzioni composte |
| 06 | `06_backprop_training.py` | Backward 2-layer + training loop su CSV M2 | Backpropagation (GPS che ricalcola dopo svolta sbagliata) — colloquio classico |
| 07 | `07_pytorch_intro.py` | Tensori PyTorch, dataset, DataLoader, training loop | Framework standard dell'industria |
| 08 | `08_cnn_computer_vision.py` | CNN: filtri, pooling, feature maps — come un computer "vede" | Base per Computer Vision |
| 09 | `09_transfer_learning.py` | Modelli pre-addestrati (ResNet, YOLO), fine-tuning base | Nella pratica non si traina da zero quasi mai |
| 10 | `10_progetto_gradio.py` | Progetto: classificatore immagini + demo Gradio | Portfolio piece #2 |

**Librerie**: torch, torchvision, gradio

**Piattaforma**: **Google Colab** (GPU gratuita) — la GPU locale (AMD Vega 10) non supporta CUDA. Workflow: sviluppo codice in Cursor → training su Colab → risultati in locale.

**Demo di modulo**: classificatore immagini su Gradio/HuggingFace Spaces.

**Analogie ponte**: CNN filtri → CSS selettori (cercano pattern). Transfer learning → pacchetto npm pre-fatto.

**Tempo**: 3-4 settimane (post split: il blocco matematico 03-06 va piu' graduale, ma ogni sotto-capitolo e' piu' "digeribile").

> **Nota di calibrazione (28/07/2026)**: nessun colloquio chiedera' mai di scrivere la backpropagation a mano.
> Le roadmap 2026 collocano la matematica alla voce "minimo indispensabile": algebra lineare per gli embedding,
> probabilita' per temperature e sampling, gradienti per l'**intuizione** sulla backprop. Il blocco 03-06 e'
> dentro questo perimetro — serve a rendere comprensibili M4 (attention) e M8 (LoRA) — ma e' il tratto del corso
> con il ritorno diretto sul mercato piu' basso. Regola operativa: **capire, non padroneggiare**. Se un
> sotto-capitolo costa piu' di ~1 settimana, chiudere con quello che si e' capito e proseguire: i concetti
> tornano in forma applicata nel M7 (PyTorch) dove autograd calcola i gradienti al posto tuo.

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
| 01 | `01_api_llm.py` | Setup, autenticazione, chat completions, modelli | La base di tutto |
| 02 | `02_prompt_engineering.py` | Zero-shot, few-shot, chain-of-thought, delimitatori | Skill #2 globale |
| 03 | `03_structured_output_pydantic.py` | Structured Outputs + Pydantic: risposte JSON con schema validato | Elimina il 90% dei bug in produzione |
| 04 | `04_function_calling.py` | L'LLM "chiama" le tue funzioni Python | Ponte tra linguaggio naturale e codice |
| 05 | `05_streaming_errori.py` | Streaming risposte + gestione errori + rate limiting | UX reattiva + robustezza |
| 06 | `06_multi_provider_litellm.py` | **NUOVO** — OpenAI vs Anthropic vs Gemini: differenze reali (streaming, rate limit, contesto, multimodale) + **LiteLLM** come strato unificato + fallback tra provider | Le roadmap 2026 danno per scontato il multi-provider. Scrivere codice legato a un solo fornitore e' debito tecnico |
| 07 | `07_ollama_modelli_locali.py` | Ollama + modelli open-source: deployment locale, API vs locale | Strategia costi + privacy |
| 08 | `08_multimodale_vision.py` | Inviare immagini all'LLM (vision) | Trend in crescita — testo + visione |
| 09 | `09_contesto_lungo_vs_rag.py` | **NUOVO** — finestre da 1-2M token: quando il contesto lungo basta e RAG e' overhead. **Prompt caching** lato provider (fino a ~90% di risparmio sulle parti fisse del prompt). Framework di decisione con calcolo costi | E' la prima decisione architetturale del 2026, e va presa **prima** di costruire un RAG. Prerequisito consapevole del M6 |
| 10 | `10_costi_caching.py` | Scelta modello, batching, semantic caching (concetto), tracciamento costi | Costi esplodono senza ottimizzazione |
| 11 | `11_sicurezza_ai.py` | Prompt injection, input sanitization, guardrails, content filtering | Non negoziabile in produzione |
| 12 | `12_progetto_assistente.py` | Progetto: assistente e-commerce con function calling + Streamlit | Portfolio piece #4 |

**Librerie**: openai, anthropic, google-genai, litellm, pydantic-ai, ollama

> **Perche' 12 capitoli invece di 10 (rev. 28/07/2026)**: i capitoli 06 e 09 sono aggiunte della revisione di
> allineamento. Il vecchio `01_api_openai.py` diventa `01_api_llm.py` perche' il corso non deve legarsi a un
> singolo fornitore: le roadmap 2026 elencano tutte OpenAI + Anthropic + Gemini + un layer unificato.

**Piattaforma**: CPU locale. Ollama con modelli fino a 3B parametri (Phi-3 Mini, Qwen2) per esercizi gratuiti + API OpenAI per esercizi che richiedono qualita superiore.

**Demo di modulo**: assistente AI e-commerce con function calling per cercare prodotti, controllare stock, calcolare preventivi — risposte in streaming.

**Analogie ponte**: Function calling → API REST endpoint (l'LLM fa la richiesta). Structured output → validazione form. Prompt → query SQL (istruisci il "database" a restituire ciò che vuoi). LiteLLM → un ORM (Eloquent) che parla con MySQL o PostgreSQL senza cambiare il tuo codice. Prompt caching → cache HTTP: la parte che non cambia non la ripaghi.

**Tempo**: 3 settimane (era 2-3, +2 capitoli)

---

## Modulo 6 — RAG Systems

**Obiettivo**: costruire un RAG completo da zero. **Skill #1 più richiesta** — 74.5% delle job posting AI.

| # | File | Argomento | Perché serve |
|---|------|-----------|-------------|
| 01 | `01_perche_rag.py` | Limiti degli LLM: conoscenza ferma, allucinazioni, niente dati privati | Il "problema" che RAG risolve |
| 02 | `02_document_loading.py` | Caricare PDF, CSV, Markdown, pagine web | L'input del sistema |
| 03 | `03_chunking_strategies.py` | Dimensione fissa, ricorsivo, semantico | La qualità del RAG dipende all'80% dal chunking |
| 04 | `04_vector_store.py` | ChromaDB: collection, inserimento, query, metadata filtering. **+ pgvector**: la stessa cosa dentro PostgreSQL, con nota su quando si sceglie l'uno o l'altro | Lo storage degli embedding |
| 05 | `05_pipeline_completo.py` | Query → embedding → retrieval → prompt augmentation → LLM → risposta | Architettura end-to-end |
| 06 | `06_langchain_basics.py` | LangChain: chain, retriever, prompt template, output parser | Il framework standard per RAG |
| 07 | `07_hybrid_search_reranking.py` | Ricerca semantica + keyword (BM25) + **reranking** (un secondo modello riordina i candidati per pertinenza) | La formula 2026 e' "vettoriale + BM25 + riordino": fermarsi ai primi due lascia qualita' sul tavolo |
| 08 | `08_ragas_evaluation.py` | RAGAS: faithfulness, answer relevancy, context precision. **+ DeepEval**: le stesse metriche dentro pytest come test bloccanti in CI | 65% delle app LLM falliscono senza valutazione |
| 09 | `09_observability.py` | Tracing e debugging della pipeline: **LangSmith** (nativo LangChain) e **Langfuse** (open source, self-hosted) | Sapere PERCHÉ il RAG ha risposto male |
| 10 | `10_context_engineering.py` | **NUOVO** — budget della finestra di contesto; **compaction/compressione** della cronologia; **memoria persistente vs retrieval** (non sono la stessa cosa); progressive disclosure degli strumenti; routing verso la fonte giusta | Disciplina emersa nel 2025-26 e oggi considerata **il** mestiere dell'AI Engineer. Riduzioni di token del 60-80% documentate. Gartner: "foundational" entro 18 mesi |
| 11 | `11_progetto_rag.py` | Progetto: assistente documentale RAG + Streamlit | Portfolio piece #5 |

**Librerie**: langchain, langchain-community, chromadb, pgvector, ragas, deepeval, langsmith, langfuse

> **Il capitolo 10 e' l'aggiunta piu' importante di questa revisione (28/07/2026).** Il corso aveva prompt
> engineering (M5-02) e RAG (M6-01/09), ma non lo strato intermedio: **cosa entra nella finestra di contesto,
> cosa viene compresso e cosa viene buttato**. Due errori che le fonti 2026 segnalano come i piu' frequenti e
> che il capitolo deve chiudere esplicitamente:
> 1. **Usare RAG come memoria.** RAG e' recupero *senza stato* da un corpus; la memoria e' persistenza *con
>    stato* tra sessioni. I sistemi in produzione usano entrambe, alimentate da fonti diverse.
> 2. **Compattare il contesto riscrivendolo con l'LLM.** La versione ingenua della compressione introduce
>    allucinazioni: si riassume cio' che il modello ha gia' frainteso.

**Demo di modulo**: assistente documentale che risponde a domande su una knowledge base con metriche di qualità visibili.

**Principio "concetti prima, framework dopo"**: il file 05 (pipeline completo) costruisce un RAG da zero con puro Python + ChromaDB — senza LangChain. Solo dal file 06 si introduce LangChain come astrazione. Così se LangChain cambia API (è già successo 3 volte in 2 anni), i concetti restano.

**Analogie ponte**: Vector DB → database SQL, ma cerca per significato. Chunking → paginazione API. RAG pipeline → middleware Laravel (intercetta, arricchisce, passa al controller). Reranking → ordinamento dei risultati di ricerca per rilevanza dopo la query. Context engineering → decidere cosa mettere nel bagaglio a mano quando il peso è limitato: RAG ti dice cosa esiste, il context engineering decide cosa parte.

**Tempo**: 3 settimane (era 2-3, +1 capitolo)

**Nota pgvector (rev. 28/07/2026)**: Chroma resta la scelta didattica giusta — si installa con un `pip install`, gira dentro il processo, e sotto i 5 milioni di vettori è produzione-ready. Ma quando hai già PostgreSQL in stack (ed è il caso del prodotto M10), **pgvector** è il default di produzione 2026: vettori e dati relazionali nella stessa tabella, stessa transazione, filtri in SQL, nessun servizio in più da monitorare. Il capitolo 04 mostra entrambi e la regola di scelta.

---

## Modulo 7 — AI Agents & Automation

**Obiettivo**: costruire agenti che ragionano, usano strumenti, e completano task multi-step. Il 67% delle grandi aziende usa agenti AI in produzione.

| # | File | Argomento | Perché serve |
|---|------|-----------|-------------|
| 01 | `01_agenti_vs_workflow.py` | Cos'è un agente vs un workflow (collega autonomo vs checklist) | Framework mentale |
| 02 | `02_langgraph_intro.py` | LangGraph: grafi, nodi, edge, stato, conditional routing | Framework standard per agenti |
| 03 | `03_tool_use.py` | Dare all'agente strumenti (API, database, file, web search) | L'agente diventa utile quando agisce nel mondo reale |
| 04 | `04_memoria_stato.py` | Agente con memoria: stato persistente, contesto tra interazioni. **Distinzione esplicita memoria vs RAG** (ripresa da M6-10): recupero senza stato ≠ persistenza tra sessioni | Conversazioni che "ricordano" — e l'errore architetturale piu' comune del 2026 |
| 05 | `05_agentic_rag.py` | RAG dove l'agente decide QUANDO, DOVE e QUANTE VOLTE cercare: ciclo di recupero invece di pipeline fissa, riformulazione della query, iterazione fino a sufficienza | **Spostato dal 08 al 05 (rev. 28/07/2026)**: nel 2026 non e' piu' l'evoluzione avanzata, e' il pattern predefinito. Va visto prima dei pattern generali, non dopo |
| 06 | `06_pattern_avanzati.py` | ReAct, Plan-and-Execute, Reflection | I pattern usati in produzione |
| 07 | `07_multi_agent.py` | Agenti che collaborano (intro a CrewAI) | Sistemi complessi con agenti specializzati |
| 08 | `08_mcp_server.py` | MCP: come funziona + costruire un MCP server custom + **sicurezza MCP** (tool poisoning, prompt injection via descrizione degli strumenti, OAuth 2.1, governo del registry) | Capisci Cursor + sai estenderlo. La parte sicurezza e' il rischio piu' segnalato e meno mitigato del 2026 |
| 09 | `09_progetto_agente.py` | Progetto: agente di ricerca e analisi + Streamlit | Portfolio piece #6 |

**Librerie**: langgraph, langchain, crewai

**Demo di modulo**: agente che cerca informazioni, le analizza, e produce un report strutturato con fonti.

**Principio "concetti prima, framework dopo"**: il file 01-03 costruiscono un agente con puro Python (loop, tool use manuale, stato). Solo dal file 04 si introduce LangGraph come framework. CrewAI (file 07) è introduttivo — il focus è sui concetti di multi-agent, non sul framework specifico.

**Verifica framework (rev. 28/07/2026)**: LangGraph è confermato come lo standard 2026 per agenti con stato, cicli e human-in-the-loop, ed è la scelta della stessa squadra che ha fatto LangChain. Le critiche ricorrenti a LangChain — documentazione frammentata tra v0 e v1, stack di chiamate profondi, difficoltà di debug — sono precisamente il motivo per cui il principio "concetti prima, framework dopo" resta la difesa giusta. Alternative da conoscere di nome per i colloqui, senza studiarle: **Pydantic AI** (agenti con tipi verificati), **OpenAI Agents SDK** e **Claude Agent SDK** (nativi di un singolo fornitore), **LlamaIndex Workflows** (quando il retrieval domina), **smolagents** (agenti che scrivono ed eseguono Python).

**Nota MCP (rev. 28/07/2026)**: la scommessa sul capitolo MCP ha pagato. Da dicembre 2025 il protocollo è governato dalla **Agentic AI Foundation** della Linux Foundation (co-fondatori Anthropic, Block, OpenAI; membri platinum AWS, Google, Microsoft, Cloudflare, Bloomberg), conta oltre 10.000 server pubblici e ~97 milioni di download mensili degli SDK, ed è supportato nativamente da ChatGPT, Claude, Gemini, Microsoft Copilot, VS Code e Cursor. Non è più una curiosità: è la via di integrazione attesa.

**Analogie ponte**: Agente → collega junior che segue istruzioni ma decide come. LangGraph → state machine. MCP → API REST che Cursor usa per parlare con i tuoi strumenti.

**Tempo**: 2-3 settimane

---

## Modulo 8 — Fine-Tuning & Personalizzazione Modelli

**Obiettivo**: adattare un modello ai tuoi dati specifici. Skill specializzata a più alto salario ($250K-$350K+).

| # | File | Argomento | Perché serve |
|---|------|-----------|-------------|
| 01 | `01_quando_fare_cosa.py` | Fine-tuning vs RAG vs prompt engineering — decision framework. **+ secondo livello di decisione**: SFT vs DPO vs GRPO/RFT, scelto in base ai dati che hai (output etichettati → SFT; coppie di preferenze → DPO; solo pollice su/giù → KTO; ricompensa verificabile come matematica/codice/formato → GRPO o RFT) | La domanda da colloquio #1 — e nel 2026 la risposta ha due livelli, non uno |
| 02 | `02_preparazione_dataset.py` | Formato, pulizia, bilanciamento, qualità dati | "Garbage in, garbage out" |
| 03 | `03_lora_spiegato.py` | LoRA: cos'è e perché funziona (aggiungere una stanza, non ristrutturare) | 99% riduzione parametri |
| 04 | `04_qlora_pratico.py` | QLoRA: fine-tuning su hardware consumer (6-10GB VRAM) | Democratizza il fine-tuning |
| 05 | `05_training_peft.py` | Training con PEFT + TRL + bitsandbytes + **Unsloth** (rende il training fattibile su GPU piccole: memoria ridotta e training piu' veloce a parita' di hardware) | Hands-on completo — e Unsloth e' cio' che rende il capitolo eseguibile sulla GPU gratuita di Colab |
| 06 | `06_valutazione_merge.py` | Valutazione modello fine-tunato + merge adapter | Verificare che il fine-tuning funziona |
| 07 | `07_progetto_finetuning.py` | Progetto: modello per descrizioni e-commerce + demo comparativa | Portfolio piece #7 |

**Librerie**: peft, bitsandbytes, trl, unsloth, transformers, datasets

> **Verifica 2026 (28/07/2026)**: LoRA/QLoRA restano dominanti — circa il **62%** dei progetti di fine-tuning usa
> metodi ad adattatori, e il full fine-tuning e' ormai riservato ai laboratori con cluster. Il modulo e' centrato.
> Sigle da conoscere almeno di nome, perche' compaiono nei colloqui: **DPO** (~38% dei progetti, allineamento da
> coppie di preferenze senza reward model), **GRPO** (~22% e in crescita rapida, e' la tecnica dietro DeepSeek R1,
> richiede una ricompensa verificabile), **DoRA** (variante di LoRA con qualita' leggermente superiore a costo
> simile), **RFT** (reinforcement fine-tuning gestito, sui modelli di ragionamento OpenAI). PPO e RLHF classico
> sono in calo: DPO e GRPO danno il 90% del beneficio al 10% del costo di ingegneria.

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
| 04 | `04_testing_ai.py` | Unit test, integration test, semantic evaluation, LLM-as-judge. **Architettura a due strati**: valutazione offline che blocca il deploy in CI (DeepEval/RAGAS) + osservabilita' in produzione che traccia il traffico vero (Langfuse/LangSmith) e rimanda i fallimenti reali nel dataset offline | 65% delle app LLM falliscono senza testing. Nel 2026 lo standard non e' "quale strumento" ma "i due strati" |
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
| M5 | "Progetta un chatbot customer service", "Cos'è il function calling?", "Cos'è il prompt injection?", "Con una finestra da 1M token, ti serve ancora RAG?" |
| M6 | "Progetta un RAG per 10M documenti", "Come valuteresti la qualità del retrieval?", "Qual è la differenza tra memoria e retrieval?", "Come riduci i token senza perdere qualità?" |
| M7 | "Progetta un agente che gestisce ordini", "Quando workflow vs agente?", "Cos'è MCP e che problema risolve?", "Quali rischi di sicurezza introduce un server MCP?" |
| M8 | "Quando fine-tuning vs RAG vs prompt engineering?", "Cos'è LoRA?", "SFT, DPO o GRPO: come scegli?" |
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

> **Revisione 28/07/2026**: la versione precedente di questa sezione citava percentuali di provenienza 2024-2025
> ("RAG 74.5% delle job posting", "prompt engineering +135.8%") e forbici salariali **statunitensi**
> ("$250K-$350K+" per il fine-tuning), fuorvianti per il mercato in cui Gianluca cerchera' lavoro.
> Sostituite con dati 2026 verificabili e con la fotografia italiana.

### Copertura per skill

| Skill | Stato 2026 | Modulo |
|-------|-----------|--------|
| Python (async, type hints, Pydantic) | Non negoziabile in tutte le roadmap | M1 + tutto |
| API / FastAPI / JSON schema | Non negoziabile | M1 + M9 |
| Prompt engineering | Base, non piu' differenziante da solo | M5 |
| **Context engineering** | **La disciplina emergente** — Gartner: "foundational" entro 18 mesi | **M6-10** (nuovo) |
| RAG | Ancora core, ma nella forma **agentic**, non pipeline fissa | M6 + M7 |
| Contesto lungo vs RAG + prompt caching | Prima decisione architetturale 2026 | M5-09 (nuovo) |
| AI Agents / tool use / orchestrazione | Requisito core, non piu' "nice to have" | M7 |
| MCP | Standard di fatto, governato da Linux Foundation | M7-08 |
| Evaluation (offline, in CI) | Critica — RAGAS, DeepEval | M6-08 + M9-04 |
| Observability (produzione) | Critica — LangSmith, Langfuse | M6-09 + M9 |
| Multi-provider / LiteLLM | Atteso: nessun lock-in su un fornitore | M5-06 (nuovo) |
| Vector DB / Embeddings | Prerequisito RAG — Chroma per prototipo, **pgvector** in produzione | M4 + M6 |
| Function calling / Structured output | Standard | M5 |
| Fine-tuning (LoRA/QLoRA) | ~62% dei progetti; sapere **quando NON farlo** vale piu' del farlo | M8 |
| Allineamento (DPO / GRPO / RFT) | Da conoscere a livello di decisione | M8-01 |
| MLOps / Docker / CI-CD / Deploy | Prerequisito professionale | M9 |
| AI Security (incl. sicurezza MCP) | In crescita, poco presidiata | M5-11 + M7-08 |
| NLP / Transformer / embeddings | Fondamenta per tutto il resto | M4 |
| Deep Learning / PyTorch | Utile come intuizione, non come mestiere | M3 |
| System design AI | Colloqui mid/senior | Trasversale (M5+) |
| Full-stack integration | Raro e ricercatissimo | M10 |
| Portfolio / Demo deployate | Requisito pratico | Trasversale |

**Copertura: 22 skill su 22 dopo questa revisione.** Prima della revisione mancavano **context engineering**,
**multi-provider** e la decisione **contesto lungo vs RAG**: la vecchia dicitura "zero lacune" non era piu' vera.

### Fotografia del mercato (dati 2026)

**Globale** — *PwC AI Jobs Barometer 2026*, oltre 1 miliardo di annunci analizzati in 27 paesi:
- **+69%** di offerte che richiedono competenze AI rispetto all'anno precedente
- **+42%** di premio salariale medio rispetto a profili equivalenti senza competenze AI
- Oltre 400 skill AI distinte mappate: non basta "saper usare un chatbot", serve integrare l'AI nei processi
  con risultati misurabili

**Italia** — *LinkedIn, gennaio 2026*:
- **24ª su 27** paesi UE per concentrazione di ingegneri AI: **0,43%** degli iscritti contro una media
  europea dello **0,90%** (davanti solo a Romania e Croazia)
- Saldo migratorio **negativo**: -0,21 ingegneri AI ogni 10.000 iscritti. L'Italia perde piu' talenti di
  quanti ne attragga
- Tasso di assunzioni complessivo **-30%** rispetto a gennaio 2019 (peggio della media UE, -26%)
- Gli annunci che richiedono competenze AI sono circa **1,7%** del totale pubblicato

**Come leggere questi due dati insieme**: domanda in crescita rapida su una base ancora piccola, e concorrenza
interna scarsa. Per chi entra adesso e' piu' opportunita' che ostacolo — ma conviene guardare anche a posizioni
**remote per aziende estere**, dove finiscono le retribuzioni migliori.

### Forbici salariali italiane (RAL lorda annua, 2026)

| Livello | Esperienza | Range realistico |
|---------|-----------|------------------|
| Junior | 0-2 anni | 22.000 - 32.000 € |
| Mid-level | 3-5 anni | 45.000 - 65.000 € |
| Senior (specializzato LLM / GenAI) | 6+ anni | 70.000 - 100.000 €+ |

Milano paga il 10-15% sopra la media nazionale. Torino e Bologna sono competitive sull'AI industriale con
costo della vita migliore.

### Norma UNI 11621-8:2026 — i nomi ufficiali dei ruoli

A inizio 2026 è stata pubblicata la **UNI 11621-8:2026**, primo standard nazionale in Europa che definisce
**12 profili professionali AI** con competenze e indicatori associati, allineato all'AI Act europeo
(Regolamento UE 2024/1689). Interessa direttamente la fase CV/colloqui: dà i nomi che le aziende italiane e
la Pubblica Amministrazione inizieranno a usare negli annunci. Da consultare al M10, quando si costruisce il
posizionamento professionale.

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
