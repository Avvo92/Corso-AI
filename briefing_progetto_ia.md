# Prompt di Contesto per Agente IA - Progetto "Ecosistema Agentico di Project Management"

## Obiettivo dell'Utente
L'utente è un programmatore (con competenze in HTML, CSS, JS, Bootstrap e Laravel) che sta seguendo un percorso di formazione in 10 moduli per diventare **AI Engineer**. L'obiettivo è sviluppare in totale autonomia un'applicazione web gestionale avanzata, agentica e multimodale, da far girare interamente **in locale su hardware dedicato (GPU Nvidia RTX 3060 con 12GB/16GB VRAM, 32GB RAM)**, azzerando la dipendenza da API commerciali (OpenAI, Anthropic) per motivi di privacy, costi e sovranità tecnologica.

---

## 1. Visione Dettagliata dell'Applicazione
L'applicazione agirà come una "Torre di Controllo" intelligente per un consulente che gestisce contemporaneamente decine di clienti, pratiche e un team di lavoro composto da tecnici e colleghi (spesso disordinati). Il flusso operativo si articola in 5 fasi logiche:

1. **Ingestione Multimodale (La cattura del caos):**
   * Input da foto/appunti cartacei tramite OCR o modelli Vision locali.
   * Input da conversazioni fisiche o chiamate telefoniche (catturate tramite centralino VoIP, integrazioni app o registratori come Plaud/Omi Pendant e gestite tramite tasti rapidi *Push-to-Talk* globale o *Buffer Circolare* in RAM per evitare *Data Swamp* e violazioni GDPR).
   * Separazione delle voci dei parlanti e identificazione degli attori (tecnici, clienti stranieri con difetti di pronuncia).
2. **Archiviazione Ibrida e RAG (La Memoria):**
   * Elaborazione del testo grezzo, taglio semantico dei blocchi senza spezzare il codice o le scadenze.
   * Indicizzazione vettoriale di manuali, contratti e storici delle riunioni.
   * Salvataggio dei dati strutturati (anagrafiche, scadenze assolute) su database relazionale classico.
3. **Agentic Loop & Controllo (Il Cervello):**
   * Estrazione di entità linguistiche complesse e scadenze relative ("entro mercoledì alle 12").
   * Risoluzione delle incongruenze o dei ripensamenti temporali all'interno dei dialoghi disordinati.
   * Loop di validazione rigorosi per azzerare le allucinazioni prima dell'azione.
4. **Scrittura nel Backend:**
   * Invio dei dati validati tramite JSON puliti al backend gestionale che aggiorna le schede e i diagrammi di Gantt.
   * Automazione della ridenominazione dei file e smistamento nelle cartelle corrette.
5. **Notifiche Contestuali (Il Quando, il Come e il Perché):**
   * Invio di promemoria intelligenti estratti dalla memoria storica (RAG) che spiegano i motivi profondi di una determinata scadenza.

---

## 2. Lo Stack Tecnologico Aperto (Tutto Locale su RTX 3060)
* **Interfaccia e Struttura:** Laravel 11 + Bootstrap + JavaScript (Gestione dei dati rigidi, tabelle relazionali, UI).
* **Motore Logico/LLM:** Ollama (Modelli attivi: `qwen2.5-coder:7b`/`14b` per programmazione, `deepseek-r1:8b` per ragionamento e logica, modelli della famiglia `Llama 3.2`).
* **Trascrizione e Audio:** `faster-whisper` (Speech-to-Text ottimizzato con suggerimento iniziale dei nomi dei clienti stranieri per prevenire errori di trascrizione fonetica).
* **Identificazione Vocale:** `pyannnote.audio` (Speaker Diarization e tracciamento delle impronte digitali vocali).
* **Algoritmi NLP Storici:** `Double Metaphone` o `Soundex` per la correzione fonetica di nomi storpiati.
* **Memoria Vettoriale (RAG):** ChromaDB (Database vettoriale locale e leggero integrato con modelli di embedding come `nomic-embed-text` o `bge-m3`).
* **Orchestratori Agentici:** LangGraph (Gestione dei grafi a stati per i loop di controllo ciclici) o CrewAI.

---

## 3. Checklist di Verifica per il Corso dell'Utente (10 Moduli)
L'agente IA deve analizzare la struttura del corso dell'utente per assicurarsi che copra le seguenti competenze obbligatorie per la realizzazione del progetto:

### Moduli 1 & 2: Deep Learning & Computer Vision (Già Completati)
* [ ] **Competenza richiesta:** Estrazione di testi da immagini di appunti scritti a mano (OCR evoluto).
* [ ] **Competenza richiesta:** Analisi di documenti tramite modelli Vision per identificare tipi di file (Fattura, Contratto, Visura).

### Modulo 3: NLP - Natural Language Processing (In Corso)
* [ ] **Competenza richiesta:** Tokenizzazione e manipolazione delle stringhe di testo.
* [ ] **Competenza richiesta:** **NER (Named Entity Recognition)** per estrarre nomi di clienti, pratiche e scadenze da trascrizioni disordinate.
* [ ] **Competenza richiesta:** Algoritmi fonetici di base per la gestione delle stringhe simili nel suono.
* [ ] **Competenza richiesta:** Concetti teorici sulle finestre di contesto (*Context Window*) e meccanismi di *Self-Attention* nei Transformer.

### Moduli Successivi (RAG, Agenti, Messa in Produzione)
* [ ] **Competenza richiesta: Ingegneria dei Dati per RAG:** Tecniche di split del testo (*Semantic Chunking*, *Parent-Child Chunking*).
* [ ] **Competenza richiesta: Database Vettoriali:** Configurazione locale di database come ChromaDB, Qdrant o Milvus.
* [ ] **Competenza richiesta: Retrieval Avanzato:** Sistemi di *Hybrid Search* (semantica + parole chiave) e implementazione di modelli di *Reranking* (Cross-Encoders).
* [ ] **Competenza richiesta: Prompt Engineering Avanzato:** Tecniche di *Chain-of-Thought* (Catena di pensiero) applicate al calcolo del tempo relativo e all'ancoraggio temporale (*Time Anchor*).
* [ ] **Competenza richiesta: Architetture Agentiche:** Sviluppo di grafi ciclici con **LangGraph** o framework equivalenti per la gestione dello stato dell'agente.
* [ ] **Competenza richiesta: Loop di Validazione:** Programmazione di cicli di auto-correzione del codice (*Self-Correction*) e controllori contro le allucinazioni (*Hallucination Grader*).
* [ ] **Competenza richiesta: Integrazione Hardware e Dispositivi:** Gestione delle chiamate a modelli locali (Ollama API), ottimizzazione della VRAM e integrazione di librerie audio come Whisper e PyAnnote.