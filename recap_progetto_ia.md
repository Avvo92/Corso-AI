# 📋 RECAP PROGETTO: SISTEMA DI COORDINAMENTO AGENTICO MULTIMODALE

## 1. Visione del Prodotto (L'Obiettivo)
Creare un'applicazione software centrale (Dashboard) per l'automazione, il project management e il coordinamento dei flussi di lavoro in uno studio di consulenza complesso. Il sistema deve azzerare il disordine generato da clienti, tecnici e colleghi, permettendo all'utente di **interrogare l'assistente a voce o via testo** per avere aggiornamenti precisi, puntuali e contestuali sullo stato delle pratiche e sulle scadenze.

### Flussi di Input e Funzionalità Core:
*   **Apertura Pratica:** Avviene tramite input multimodale: conversazione iniziale con il cliente (audio), appunti scritti al PC o foto di appunti presi a mano a penna.
*   **Cacciatore di Documenti:** L'utente o il cliente caricano file (PDF/Immagini). L'IA legge il documento, ne verifica la correttezza, estrae i dati per i contratti, lo rinomina e lo sposta nella cartella corretta della pratica.
*   **Brainstorming Vocale Multi-Pratica:** Un microfono registra le riunioni d'ufficio in cui si salta in modo caotico tra oltre 10 pratiche diverse. L'IA separa le voci, isola i discorsi di ciascun cliente e ricompone il filo logico.
*   **Estrazione Scadenze Relative:** L'IA intercetta espressioni temporali complesse o contraddittorie (es. *"consegna venerdì, anzi no, facciamo il lunedì successivo"*) e le converte in date e ore assolute nel calendario.
*   **Notifiche Contestuali Inteligenti:** Il sistema invia notifiche che non dicono solo "cosa" fare, ma ricordano il **Quando**, il **Come** e il **Perché** logico (pescato dalla memoria storica delle riunioni).
*   **Gestione Chiamate e Privacy:** Intercettazione delle telefonate di lavoro (tramite sistemi VoIP o registratori hardware) con filtri automatici (White List di numeri o classificazione NLP del testo) per **cancellare istantaneamente le chiamate private** e proteggere la privacy.

---

## 2. Stack Tecnologico Open-Source Selezionato (Hardware: Nvidia RTX 3060)
Per garantire autonomia totale, costo zero di computazione e privacy assoluta dei dati dei clienti, il software girerà **al 100% in locale** sfruttando l'infrastruttura open-source e la VRAM della scheda video:

*   **Interfaccia e Backend Gestionale:** **Laravel 11 + Bootstrap + JavaScript**. Gestisce la struttura rigida, le schede clienti, il database relazionale (MySQL/PostgreSQL) e lo scheduler delle notifiche (Cron Jobs).
*   **Motore Inferenziale Locale:** **Ollama** per far girare modelli linguistici ottimizzati per il coding e la logica (es. **Qwen 2.5/3.5 Coder** o la serie **Llama**) in modalità quantizzata (4-bit).
*   **Trascrizione Audio:** **Faster-Whisper** (modelli ottimizzati come *Distil-Whisper* o *Whisper Turbo* per non saturare la VRAM durante lo streaming).
*   **Riconoscimento Vocale:** **PyAnnote.audio** per la *Speaker Diarization* (separare le voci nel brainstorming) e algoritmi come **ECAPA-TDNN** per la *Speaker Identification* (capire chi parla).
*   **Memoria Semantica (RAG):** **ChromaDB** come database vettoriale locale per archiviare gli embeddings delle trascrizioni e degli appunti, arricchiti con metadati strutturati.
*   **Orchestruzione Agentica e Loop di Controllo:** **LangGraph** (o *CrewAI*) per gestire i cicli di auto-correzione, la verifica delle allucinazioni (Hallucination Grader) e i nodi decisionali dei compiti.
*   **NLP e Logica Temporale:** Tecniche di **Chain-of-Thought** nel prompt unite a librerie di normalizzazione (es. *Duckling* o *SUTime*) per il calcolo delle date.
*   **Computer Vision:** Modelli di OCR (es. *EasyOCR*) o modelli *Vision-LLM* locali per la lettura degli appunti a mano e dei documenti scansionati.

---

## 3. Checklist per il Confronto con i 10 Moduli del Corso

Per verificare se il tuo corso copre tutto il necessario per costruire questa app, l'agente IA dovrà controllare la presenza dei seguenti macro-argomenti:

*   [ ] **Computer Vision & Deep Learning:** OCR (Optical Character Recognition), Object Detection (es. YOLO per i sensori di sedia/webcam), e architetture di Vision-LLM per la lettura dei documenti dei clienti.
*   [ ] **Fondamenta NLP (Natural Language Processing):** Tokenizzazione, Embeddings statici e dinamici, meccanismo di *Self-Attention* e architettura *Transformer*.
*   [ ] **Information Extraction (Estrazione Entità):** Named Entity Recognition (NER) e linking per estrarre nomi di clienti, scadenze e compiti da testi disordinati.
*   [ ] **Speech-to-Text & Audio Intelligence:** Modelli di trascrizione (Whisper) e techniques di gestione audio (*Voice Activity Detection*, *Speaker Diarization*, *Speaker Identification*).
*   [ ] **Sistemi RAG (Retrieval-Augmented Generation):** Architettura di Vector Database (ChromaDB), tecniche di *Chunking* (semantico e strutturato), calcolo degli embeddings e recupero ibrido delle informazioni.
*   [ ] **Advanced RAG:** Tecniche di *Reranking* (Cross-Encoders) e fusione dei risultati tra database relazionali e database vettoriali.
*   [ ] **Ingegneria del Prompt Avanzata:** Tecniche di *Chain-of-Thought* (CoT) per il ragionamento logico/temporale e strutture di *Structured Output* (forzare l'IA a rispondere in JSON puliti).
*   [ ] **Sistemi Agentici (Agentic AI):** Function Calling (capacità dell'LLM di attivare script Python esterni), pattern *ReAct* (Reasoning and Acting).
*   [ ] **Loop di Controllo e Grafi:** Architetture a states per implementare cicli di revisione del codice, auto-correzione degli errori di sintassi e validazione delle risposte contro le allucinazioni (es. tramite LangGraph).
*   [ ] **Deployment & Integrazione API:** Come far comunicare script di intelligenza artificiale in Python con backend tradizionali (Laravel) tramite endpoint API sicuri.
