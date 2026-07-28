# Mentor Engine — idea post-corso (NON canonica, NON M10)

> **Stato:** parcheggiata. Da riprendere **dopo** il completamento del M10.
> **Non compete con Validator/Replicator**, che restano il prodotto del corso.
> Origine: conversazione del 28/07/2026 — canonizzare in applicativo il sistema di
> apprendimento usato in questo repo, per renderlo esportabile ed eventualmente vendibile.

---

## 1. Cos'è

Trasformare in applicazione vera il sistema didattico che ha retto questo corso: non un chatbot
che risponde, ma un **motore con modello dello studente persistente**.

Il nucleo differenziante è il **ciclo di gestione dell'errore**, non la conversazione:

```
risposta sbagliata
   -> lacuna registrata con ID e stato (rosso)
   -> stato consultato quando si prepara il capitolo successivo
   -> blocco di rinforzo mirato inserito dove il concetto debole
      si aggancia all'argomento nuovo
   -> verifica pratica
   -> stato aggiornato (rosso -> giallo -> verde)
```

Più: quiz ponte tra capitoli, ripetizione dilazionata con contatori sul glossario, diari di
sessione, protocolli bloccanti di apertura e chiusura capitolo, archiviazione dei moduli
completati per tenere snello il contesto attivo.

Nome tecnico della disciplina (utile per raccontarlo): **context engineering** — memoria
persistente distinta dal retrieval, caricamento progressivo, compressione dello storico.

## 2. Perché costa poco costruirlo dopo il M10

Ogni componente è già materia di studio del corso. Non è un prodotto nuovo, è un
riassemblaggio dello stesso stack su un dominio diverso.

| Componente del tutor | Dove lo impari |
|---|---|
| Memoria dello studente (stato persistente) | M7-04 |
| Recupero del materiale giusto | M6 (RAG) |
| Quale rinforzo iniettare e quando | M6-10 (context engineering, routing) |
| Correzione strutturata (voto, lacune, stato) | M5-03 (structured output + Pydantic) |
| Valutazione automatica delle risposte | M9-04 (LLM-as-judge) |
| Controllo costi (modello economico vs frontiera) | M5-09, M5-10 |
| Servizio, container, deploy | M9 |
| Interfaccia e streaming | M5-05 + M10 |

Stima a spanne: **1-2 settimane** riusando lo scheletro del M10, contro le 3-4 del M10 stesso.

## 3. Le tre domande che decidono se è remunerativo

### 3.1 Unit economics dei token

È il punto che uccide la maggior parte dei tutor AI. Questo corso consuma molti token di un
modello di frontiera: ogni valutazione rilegge file di contesto grandi. Se un abbonato paga
30 €/mese e ne brucia 20 di inferenza, non è un'azienda.

Da progettare **dall'inizio**, non da rattoppare:
- modello economico per le interazioni di routine (domande, chiarimenti)
- modello di frontiera solo per correzioni e chiusure di capitolo
- prompt caching aggressivo sulla parte fissa del contesto
- compressione/archiviazione dello storico (già fatta a mano qui con `archivi/`)

**Metrica da definire prima di scrivere codice:** costo medio di inferenza per studente attivo
al mese.

#### 3.1.1 Modelli gratuiti / open source — cosa regge e cosa no

Tre distinzioni da tenere ferme (discussione 28/07/2026):

1. **"Open source" ≠ "gratis".** I pesi aperti spostano il costo dall'API al server: paghi la
   GPU a ore. Sotto un certo numero di utenti attivi, la GPU affittata costa **più** delle
   chiamate API. L'unica versione davvero gratuita per il venditore è farlo girare **sulla
   macchina dello studente** (Ollama): modello di business legittimo, ma restringe il mercato.
2. **I prezzi crollano, la frontiera no.** Il costo per unità di capacità scende in fretta, ma
   quello che diventa economico è *la frontiera di ieri*. La scommessa giusta non è "aspetto
   che diventi gratis", è **rendere economico il cambio di modello**: codice provider-agnostico
   (LiteLLM, M5-06) → quando il prezzo cala si cambia una riga di configurazione.
3. **Il lavoro del mentore non è un compito solo.** Spacchettandolo:

| Compito | Difficoltà | Modello adeguato |
|---|---|---|
| Rispondere a domande di sintassi / definizioni | Bassa | Piccolo, anche locale |
| Generare quiz da un capitolo esistente | Bassa | Piccolo |
| Tenere glossario, contatori, stato di avanzamento | Nulla (è codice) | Nessun LLM |
| **Valutare una risposta libera con giudizio sfumato** | **Alta** | **Frontiera** |
| **Scrivere il rinforzo mirato** (agganciare una lacuna vecchia all'argomento nuovo, con analogia nuova) | **Alta** | **Frontiera** |

**Architettura conseguente — instradamento (routing):** modello economico/locale per ~80%
delle interazioni, frontiera solo per correzioni e chiusure di capitolo. Il costo per studente
scende di quasi un ordine di grandezza senza perdere il pezzo differenziante.

#### 3.1.2 Golden set già disponibile (asset raro)

La scelta del modello **non si decide a opinioni, si misura**. Il materiale esiste già: i
`sessioni_capitoli/*.md` e le tabelle di `CONTESTO_CORSO.md` contengono ~6 mesi di
**valutazioni con voto e motivazione** (risposta grezza → giudizio → errore preciso
individuato). È un *golden set* pronto, e produrre i giudizi di riferimento è normalmente la
parte costosa di un banco di prova.

Procedura: si dà la stessa risposta grezza al modello candidato, si confronta il suo giudizio
con quello registrato, si misura la concordanza. Mezz'ora di lavoro, nessuna congettura.

**Vincolo operativo:** non buttare i diari di sessione durante l'archiviazione dei moduli.

#### 3.1.3 Licenze

Se si vende, verificare la licenza dei pesi. Apache 2.0 è pulita per uso commerciale; alcune
licenze "community" pongono condizioni. Da controllare **prima** di costruirci sopra.

### 3.2 Chi scrive i contenuti (vero collo di bottiglia)

L'applicazione senza curriculum è un guscio. Tre strade:

| Strada | Pro | Contro |
|---|---|---|
| A. Porti solo questo corso | Dimostrabile, qualità nota | Mercato stretto |
| B. Motore che genera il curriculum dall'obiettivo | Scalabile | Qualità incerta, molto più ambizioso |
| C. Strumento per chi insegna (portano loro i contenuti) | Clienti che pagano, meno supporto | Meno romantico |

Ipotesi corrente: **C**, con **A** come prova di funzionamento.

### 3.3 Prova che funziona (oggi n=1)

Prima di chiedere soldi servono 5-10 studenti beta reali, con dati misurati: tasso di
completamento, lacune chiuse, tempo per modulo, voti di difficoltà. Senza, l'affermazione
"sostituisce un workshop da decine di migliaia di euro" non è difendibile.

## 4. Modello di vendita — ipotesi da verificare

- **B2C in abbonamento**: strada più dura. Il supporto erode i margini e l'abbandono
  nell'autoapprendimento è altissimo.
- **B2B a chi fa formazione** (scuole, aziende che riqualificano, bootcamp che vogliono
  ridurre il costo dei tutor umani): meno affascinante, clienti ricorrenti, meno supporto
  individuale. **Ipotesi preferita.**
- **Open source + tier a pagamento**: il template è gratis, si paga l'hosting e la gestione.
  Ottimo per visibilità e portfolio, monetizzazione lenta.

## 5. Da non dimenticare

- **GDPR** (Regolamento europeo sui dati personali): il profilo di uno studente — errori,
  lacune, voti — è dato personale. Serve base giuridica, informativa, cancellazione.
- **Anonimizzazione**: il `CONTESTO_CORSO.md` di questo repo contiene il profilo dettagliato
  degli errori di Gianluca. Qualunque versione pubblica o commerciale parte da un template
  ripulito, non da questo file.
- **I diari di sessione sono un asset, non scarti** (vedi §3.1.2): sono il golden set per
  scegliere il modello. Conservarli anche dopo l'archiviazione dei moduli.
- **Doppio uso portfolio**: una volta costruito è anche un progetto da mostrare, a costo
  quasi zero perché il contenuto esiste già.

## 6. Prossima azione

**Nessuna, fino al completamento del M10.** Alla chiusura del M10, rileggere questo documento
e decidere se aprire una scheda prodotto vera in `docs/prodotto/`.
