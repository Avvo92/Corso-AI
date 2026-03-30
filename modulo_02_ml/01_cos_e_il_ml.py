"""
============================================================================
MODULO 2 — CAPITOLO 01: Cos'e il Machine Learning
Da "analisi dati" a "previsione automatica"
============================================================================

Analogia pratica:
- Modulo 1: hai imparato a leggere report e tabelle.
- Modulo 2: costruisci un "assistente" che impara dai casi passati
  e propone una previsione su un caso nuovo.

Confronto web:
- JavaScript/PHP: regole scritte a mano con if/else
- Machine Learning: regole apprese dai dati
"""

import pandas as pd
import numpy as np
import os

# ==========================================================================
# QUIZ D'INGRESSO — Ripasso da Pandas (cap.09-10)
# ==========================================================================
#
# DOMANDA 1 — Vero/Falso:
# "df['colonna'] restituisce un DataFrame." Falso, restituisce una Series
#
# DOMANDA 2 — Prevedi l'output:
#   print(df[["a", "b"]].shape)
# Se df ha 30 righe, cosa stampa? (30, 2)
#
# DOMANDA 3 — Trova l'errore:
#   top = df[df["prezzo"] = 100] l'operatore logico è sbagliato sintaticamente, sarebbe corretto "=="
#
# DOMANDA 4 — Definizione:
# Differenza tra `.loc` e `.iloc` in una frase.
# loc selezione per etichetta, iloc per indice
# DOMANDA 5 — Completa:
#   righe = df.shape[0]
#   colonne = df.shape[1]
#

# ==========================================================================
# PARTE 1: Cos'e il Machine Learning (ML)
# ==========================================================================
#
# Machine Learning = il computer impara pattern dai dati storici
# e li usa per fare previsioni su dati nuovi.
#
# Esempio e-commerce:
# input: metri quadri, citta, anno casa
# output: prezzo stimato
#
# Non scrivi a mano tutte le regole:
# il modello le apprende dai dati.
#
# Fermiamoci un momento sul senso profondo.
# Con la programmazione classica scrivi tu tutte le regole: "se succede A, fai B".
# Funziona bene quando il problema e piccolo e stabile.
# Con il Machine Learning ribalti il flusso: dai esempi al sistema e lasci che
# apprenda da solo una regola numerica che minimizza l'errore.
#
# In pratica il modello fa un ciclo: osserva dati (X), prova a prevedere y,
# misura quanto sbaglia, corregge i propri pesi e riprova. Questo processo
# ripetuto molte volte fa emergere pattern che con if/else diventerebbero
# troppo numerosi o fragili da mantenere.
#
# Non e una bacchetta magica: ML conviene quando il problema e predittivo,
# i dati sono decenti e vuoi generalizzare su casi nuovi.
# Se invece hai una regola semplice, deterministica e stabile, spesso la
# soluzione classica resta la scelta migliore.
#
# Tieni a mente tre anti-pattern molto comuni:
# 1) credere che il modello "indovini" anche con dati sporchi;
# 2) confondere correlazione e causalita;
# 3) valutare sul training e pensare che sia performance reale.
#
# Prima di andare avanti, checklist mentale rapida:
# input/target chiari, dati controllati, metrica adatta, test separato.

print("\nPARTE 1 — Cos'e il ML\n")
print("ML = apprendere pattern dai dati per fare previsioni.")

# --- MINI-ESERCIZIO 1 — Prova subito! ---
# 1) Scrivi un esempio reale (tuo dominio) di problema predittivo.
# Un problema predittivo nel mio dominio è, data una serie di documenti reddituali reali o alterati, capire se la pratica nuova che mi hanno portato è più probabilmente vera o falsa in qualcosa
# 2) Scrivi input (feature) e output (target).
# l'input deve essere un insieme di documenti reddituali che vanno analizzati in termini di coerenza tra loro, alterazioni grafiche, incongruenze numeriche e difformità nei metadati,
# e l'output deve essere un analisi che comprende, un semaforo che dia indicazione chiara della zona di genuinità in cui ci troviamo, uno scoring da 1 a 100 , e un riassunto sulle motivazione
# che hanno portato a quella valutazioni
# 3) Spiega in 1 riga perche conviene ML invece di if/else fissi.
# Perchè il campo delle possibilità è troppo vasto, e sarebbe impensabile senza l'aiuto dell'IA e del machine learnig avere un programma che gestisca tutte le casistiche.


# ==========================================================================
# PARTE 2: Tipi principali di Machine Learning
# ==========================================================================
#
# 1) Supervisionato:
#    hai input + target noto (es. prezzo casa)
#
# 2) Non supervisionato:
#    non hai target, cerchi gruppi/pattern (es. segmenti clienti)
#
# 3) Reinforcement Learning:
#    agente che impara da ricompense/penalita.
#
# Qui facciamo una distinzione che in pratica vale oro.
# Nel supervisionato hai una risposta storica affidabile: sai gia "come e andata"
# e alleni il modello a riprodurre quella logica su nuovi casi.
# Nel non supervisionato la risposta non c'e: il lavoro e scoprire struttura,
# gruppi nascosti, segmenti o anomalie.
# Nel reinforcement learning, infine, il sistema non studia un dataset statico:
# prende decisioni in sequenza e impara da premi/penalita.
#
# Tradotto sul tuo prodotto:
# supervisionato = predire score/esito da pratiche storiche;
# non supervisionato = trovare cluster di pratiche simili;
# reinforcement = agente che ottimizza il prossimo passo operativo.
#
# La regola da professionista e semplice: non scegliere l'approccio "di moda".
# Parti sempre dalla domanda: "ho un target affidabile oppure devo prima scoprire pattern?"

print("\nPARTE 2 — Tipi di ML\n")
print("Supervisionato, non supervisionato, reinforcement.")

# --- MINI-ESERCIZIO 2 — Prova subito! ---
# Classifica questi casi:
# a) Predire abbandono cliente (si/no) supervisionato
# b) Raggruppare utenti per comportamento acquisto non supervisionato
# c) Agente che impara a giocare reinforcement learning


# ==========================================================================
# PARTE 3: Dataset, Feature, Target (ponte con Pandas)
# ==========================================================================
#
# Adesso mettiamo ordine nei tre oggetti fondamentali:
# dataset, feature, target.
# Il dataset e il contenitore completo dei casi storici.
# Le feature sono i segnali che usi per spiegare il fenomeno.
# Il target e cio che vuoi prevedere.
#
# Nel progetto documentale, ad esempio, puoi usare come feature la confidence OCR,
# il numero di incoerenze e alcuni indicatori economici; il target puo essere
# lo score di genuinita o la classe semaforo.
#
# Attenzione a un errore classico ma devastante: il leakage.
# Se metti (direttamente o indirettamente) il target dentro le feature,
# il modello sembra eccellente ma e un falso positivo metodologico.
#
# Ripasso tecnico importante: X di solito e un DataFrame (2D), y una Series (1D).
# Questa distinzione non e solo teoria: evita bug quando passeremo a train/test e metriche.

percorso_case = os.path.join(os.path.dirname(__file__), "..", "modulo_01_python_dati", "dati", "case.csv")
case = pd.read_csv(percorso_case)

# Rinforzo mirato: Series vs DataFrame
print("\nRINFORZO — Series vs DataFrame")
print(type(case["prezzo_euro"]))             # Series
print(type(case[["prezzo_euro"]]))           # DataFrame

# Rinforzo mirato: shape su selezione colonne
print("\nRINFORZO — Shape selezione colonne")
print(case[["metri_quadri", "prezzo_euro"]].shape)

# Creiamo feature/target (concetto base ML)
X = case[["metri_quadri", "anno_costruzione", "distanza_centro_km"]]
y = case["prezzo_euro"]

print(f"\nFeature X shape: {X.shape}")
print(f"Target y shape: {y.shape}")

# --- MINI-ESERCIZIO 3 — Prova subito! ---
# 1) Aggiungi `ha_garage` alle feature X.
# 2) Stampa shape nuova di X.
# 3) Scrivi in una riga: perche y e Series e non DataFrame?
X['ha_garage'] = case['ha_garage']
print(f"\nFeature X shape: {X.shape}")
# y prendi in considerazione solo la colonna prezzo euro contenuta in case, mentre x , prendendo in considerazione più colonne, costituisce un dataframe


# ==========================================================================
# PARTE 4: Rinforzo report con .agg (ponte M1 -> M2)
# ==========================================================================
#
# Nel lavoro reale di Machine Learning non fai solo modello:
# prima devi capire i dati con report sintetici.
# Il metodo .agg ti permette di costruire report leggibili e veloci.
#
# Questa parte e meno "glamour", ma in azienda fa la differenza tra modello solido
# e progetto fragile. Prima di allenare devi capire il territorio: distribuzioni,
# estremi, sbilanciamenti e differenze tra gruppi.
#
# `.agg` e il tuo ponte naturale da SQL a ML: con poche righe ottieni una vista
# ad alta densita informativa. In altre parole, stai trasformando "dati grezzi"
# in insight operativi che guidano feature engineering e scelte modellistiche.
#
# Qui nascono anche molti errori silenziosi: metrica sbagliata (size/count/nunique),
# proporzioni non rese leggibili, ordinamenti incoerenti con la domanda business.
# Per questo la regola e: prima allinei la domanda, poi costruisci l'aggregazione.

print("\nPARTE 4 — Report con .agg\n")

case["is_centro"] = case["distanza_centro_km"] < 3
report_base = (
    case.groupby("citta", as_index=False).agg(
        pratiche_totali=("id", "count"),
        prezzo_medio=("prezzo_euro", "mean"),
        metri_quadri_medi=("metri_quadri", "mean"),
        quota_centro=("is_centro", "mean"),
    )
)
report_base["quota_centro"] = (report_base["quota_centro"] * 100).round(2)
print(report_base.sort_values("prezzo_medio", ascending=False).round(2))

# --- MINI-ESERCIZIO 4 — Rinforzo .agg ---
# 1) Aggiungi una colonna prezzo_al_mq = prezzo_euro / metri_quadri
# 2) Crea report per citta con .agg:
#    - pratiche_totali
#    - prezzo_massimo
#    - prezzo_minimo
#    - prezzo_medio_al_mq
# 3) Ordina per prezzo_massimo desc e stampa top 3
print("\nMini-esercizio 4\n")
case['prezzo_al_mq'] = case['prezzo_euro'] / case['metri_quadri']
report = case.groupby('citta').agg(
    pratiche_totali = ('id', "count"),
    prezzo_massimo = ('prezzo_euro', 'max'),
    prezzo_minimo = ('prezzo_euro', 'min'),
    prezzo_medio_al_mq = ('prezzo_al_mq', lambda x: x.mean().round(2))    
    ).sort_values(by='prezzo_massimo', ascending=False)

print(report.head(3))


# ==========================================================================
# PARTE 5: Workflow professionale minimo (dal dato alla previsione)
# ==========================================================================
#
# Ti lascio una sequenza che voglio diventi il tuo "pilota automatico" professionale.
# Parti sempre da una frase business chiara, definisci target e metrica, fai EDA minima,
# costruisci X/y senza leakage, separi train/test, alleni una baseline, interpreti errori
# e solo dopo iteri. Questo ordine riduce tantissimo il rischio di autoinganno.
#
# In questo capitolo fissiamo i mattoni. Nei prossimi entreremo con metodo in training,
# validazione e metrica, ma con una base concettuale gia stabile.
#
# --- MINI-ESERCIZIO 6 — Workflow in 8 righe ---
# Scrivi 8 righe (una per step) su come applicheresti il workflow sopra
# al progetto "Controllo Documentale AI" (usa parole semplici, niente teoria astratta).
#Frase di Business: "il mio applicativo deve fornire un supporto di facile interpretazione e chiaro nelle spiegazioni che fornisce, per aiutare nella valutazione di genuinità dei documenti forniti dai clienti che richiedono finanziamenti o mutui"
#Target: un semaforo verde giallo o rosso, uno scoring da 1 a 100 per grafica, coerenza anagrafica, coerenza numerica, coerenza fiscale e metedati e per ogni aspetto analizzato una sintessi chiara e puntuale sulle eventuali anomalie riscontrate, e in che modo e quanto pesantemente hanno contribuito alla valutazione finale.
#EDA: analisi dei documenti forniti, per capire le metriche principali che possono essere fornite dai dati
#X/y e train/test: costruisco un dataframe di feature che riassumano gli aspetti sopracitati, quindi coerenza anagrafica, numerica, fiscale, grafica e metadati,e divido la parte che utilizzerò in fase di test da quella che usero per il training ( 30%, 70%).


# ==========================================================================
# 🔁 RINFORZO MIRATO — Dal Web Bridge al ML (API, filtri, payload)
# ==========================================================================
#
# Nel capitolo 12 sono emersi 4 punti chiave da consolidare subito:
# 1) Query params URL: "?" una sola volta, poi "&"
# 2) Parametri opzionali numerici/bool:
#    - numerici: usare `is not None`
#    - bool opzionali: usare `is not None` (False e un valore valido)
# 3) Conteggi/percentuali per categoria:
#    - non usare `.sum()` per contare righe filtrate
#    - usare `len(masked_df)` o `value_counts(normalize=True)`
# 4) Naming JSON coerente:
#    - evitare chiavi diverse tra endpoint (es. score_genuinita sempre uguale)
#
# Micro-esempio operativo (stesso pattern del progetto semaforo):
demo = pd.DataFrame(
    {
        "id_pratica": ["P1", "P2", "P3", "P4", "P5"],
        "score_genuinita": [91, 76, 54, 43, 84],
    }
)

def mappa_semaforo(score: int) -> str:
    if score >= 80:
        return "verde"
    if score >= 50:
        return "giallo"
    return "rosso"

demo["semaforo"] = demo["score_genuinita"].apply(lambda x: mappa_semaforo(int(x)))
dist = (demo["semaforo"].value_counts(normalize=True) * 100).round(2)
print("\nRINFORZO — Distribuzione semaforo (%)")
print(dist)

# --- MINI-ESERCIZIO 5 — Rinforzo cap.12 -> cap.01 M2 ---
# Dati: `dati/pratiche_semaforo.csv` (cwd = cartella `modulo_02_ml`)
# 1) Calcola il numero pratiche verdi senza usare `.sum()` sul DataFrame intero.
# 2) Calcola percentuale verdi/gialli/rossi con `value_counts(normalize=True)`.
# 3) Scrivi una riga: perche `if ha_garage:` e pericoloso se il parametro e bool opzionale?
# 4) Scrivi URL corretta (con query params) per:
#    endpoint `/progetto/pratiche`, filtro `semaforo=giallo` e `limit=5`
#    (nota: "?" una volta, poi "&").
path_file = os.path.join(os.path.dirname(__file__), "dati", "pratiche_semaforo.csv")
pratiche = pd.read_csv(path_file)
conta_per_semaforo = pratiche['semaforo'].value_counts()
perc_semafori = (pratiche['semaforo'].value_counts(normalize=True) * 100).round(2)
# perchè False e null, essendo entrambi valori "falsy", qualora di dovesse fare un contenggio, il risultato dei risultati
#che effettivamente non hanno un garage sarebbe falsato. Qui, nel momento in cui si procede con il calcolo, si potrebbe ad
# esempio usare una mask del tipo "filtro_null = pratiche['ha_garage'] != null"

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI(
    title="Modulo 2 — ML",
    version="1.0.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In produzione metti il dominio del frontend
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/progetto/pratiche")
def filtro(
    semaforo: str | None = Query(None, description="Indicare il semaforo scelto"),
    limit: int = Query(5, description="Quanti risultati vuoi visualizzare", ge=1, le=5)
):
    if semaforo:
        return pratiche.loc[pratiche['semaforo'] == semaforo].head(limit).to_dict(orient="records")
    return pratiche.head(2).to_dict(orient="records")




# ==========================================================================
# QUIZ DI VERIFICA — Prima degli esercizi
# ==========================================================================
#
# DOMANDA 1 — Vero/Falso:
# "Nel supervisionato il target e noto nel training." Vero
#
# DOMANDA 2 — Completa:
# `X` contiene il DataFrame con le feature ; `y` contiene il target
#
# DOMANDA 3 — Trova l'errore:
#   X = case["metri_quadri", "prezzo_euro"] => X = case[["metri_quadri", "prezzo_euro"]]
#
# DOMANDA 4 — Prevedi:
# Se X ha shape (30, 4), quante feature per campione ha? 4
#
# DOMANDA 5 — 💬 Spiega con parole tue:
# differenza pratica tra scrivere regole a mano e farle apprendere al modello.
# la differenza è che scrivendo le regole a mano non si riescono a gestire in maniera efficiente un gran numero di variabili, in quanto ogni condizione deve essere specificata. Facendole apprendere al modello, sarà lui a trovare tramite prove mirata ad allinearsi al target a trovare la strada giusta per trovare, in base alla richiesta il risultato previsto nel target
# DOMANDA 6 — Errori tipici:
# Cita 2 anti-pattern reali:
# - uno legato alla preparazione dei dati => Inserire, anche in maniera indiretta, il target nelle feature (leakage)
# - uno legato alla valutazione del modello => usare delle feature che non rappresentano in modo coerente i dati utili a raggiungere il nostro target (data misinterpretation)


# ==========================================================================
# ESERCIZI — Ora prova tu
# ==========================================================================
#
# ESERCIZIO 1 (Facile):
# Carica `case.csv` e identifica chiaramente:
# - feature candidate
# - target candidate
# Stampa shape e tipi (`type`) di entrambe.
print("\nEsercizio 1\n")
path_file = os.path.join(os.path.dirname(__file__), "dati", "case.csv")
houses = pd.read_csv(path_file)
feature_candidates = houses[['metri_quadri', 'num_stanze', 'piano', 'ha_balcone', 'ha_garage','distanza_centro_km', 'citta', 'anno_costruzione']]
target_candidate = houses['prezzo_euro']
print(feature_candidates.columns.to_list())
print(target_candidate.name)

# ESERCIZIO 2 (Medio):
# Crea 2 versioni di X:
# a) X_base con 3 feature
# b) X_plus con 5 feature
#scrivi quale versione useresti e perche.
X_base = houses[['metri_quadri', 'num_stanze', 'ha_garage']]
X_plus = houses[['metri_quadri', 'num_stanze', 'ha_garage', 'ha_balcone', 'distanza_centro_km']]
print(X_base.shape)
print(X_plus.shape)
# userei X_plus perchè avere il 66 % in più di variabili, da sicuramente un visione più chiara e accurata sulla realtà della composizione del prezzo delle case, e dunque crea dei modelli più affidabili per arrivare a una previsione il più possibile vicina alla realtà

# ESERCIZIO 3 (🎯 [COLLOQUIO]):
# Spiega in 8-10 righe:
# - differenza regressione vs classificazione
# - un esempio reale per ciascuna
# - quale metrica useresti per valutarle
# la regressione si una per i valori numerici, ossia partendo dalle feature la macchina produce in output un valore numerico
# la classificazione invece in sostanza, sempre partendo da delle feature, da un etichetta all'oggetto che si sta analizzando

# ESERCIZIO 4 (🔧 [REFACTORING]):
# Riscrivi questo codice "brutto" in modo pulito:
# dati = pd.read_csv(...)
# a = dati[['metri_quadri','anno_costruzione','distanza_centro_km']]
# b = dati['prezzo_euro']
# print(a.shape); print(b.shape)
# (usa nomi espliciti + output leggibili)
#
case = pd.read_csv(path_file)
variabili_case = case[['metri_quadri','anno_costruzione','distanza_centro_km']]
obiettivo_case = case['prezzo_euro']
print(f"Shape delle variabili:\n{variabili_case.shape}")
print(f"Shape dell'obiettivo:\n{obiettivo_case.shape}")


# ESERCIZIO 5 (🔍 [DEBUG]):
# Correggi questo blocco e spiega l'errore:
# X = case["metri_quadri", "anno_costruzione"] => X = case[["metri_quadri", "anno_costruzione"]]
# y = case[["prezzo_euro"]] => y = case["prezzo_euro"]
# print(X.shape[1], y.shape)
# Nella versione sbagliata, per la X si sarebbe prodotto un key error, mentre la y cosi scritta avrebbe prodotto un dataframe 
# con una sola colonna, e non una series

# ESERCIZIO 6 (🔀 [INTERLEAVING] — Pandas + ML):
# Partendo da `case.csv`:
# 1) Crea `fascia_prezzo` con 3 classi: basso, medio, alto
# 2) Costruisci un report con `.agg` per `citta` e `fascia_prezzo`:
#    - pratiche_totali
#    - prezzo_medio
#    - metri_quadri_medi
# 3) Spiega in 3 righe come useresti questo report per scegliere feature utili.
# userei questo report per capire il potenziale per citta rispetto case di fascie di prezzo differenti, potendo vedere
# più chiaramente il numero per città, metri quadri medi e media dei prezzi
case["fascia_prezzo"] = pd.cut(
    case["prezzo_euro"],
    bins=[0, 150_000, 300_000, 1_000_000_000],
    labels=["basso", "medio", "alto"],
    include_lowest=True,
    right=False,  # opzionale: come trattare i bordi
)

case_citta_fascia = case.groupby(['citta', 'fascia_prezzo']).agg(
    pratiche_totali = ('id', 'count'),
    prezzo_medio = ('prezzo_euro', 'mean'),
    metri_quadri_medi = ('metri_quadri', 'mean')
).round({'prezzo_medio': 2, 'metri_quadri_medi': 2}).reset_index()

print(case_citta_fascia)
#
# ESERCIZIO 7 (🧠 [RETRIEVAL] — riscrittura da memoria):
# Senza guardare il capitolo 09, riscrivi da zero (solo dalla memoria + questo testo):
#
# 1) Mask booleana (specifica):
#    Crea una variabile `mask` che sia True per le righe in cui `anno_costruzione >= 2000`
#    (case “recenti”). Opzionale: verifica con `mask.sum()` quante righe sono True.

mask = case['anno_costruzione'] >= 2_000
print(case['id'].loc[mask].count())
# 2) Assegnazione condizionale con `.loc`:
#    Aggiungi una colonna `eta_casa` (stringa) al DataFrame `case`:
#    - dove `mask` è True  -> `eta_casa = "recente"`
#    - dove `mask` è False -> `eta_casa = "non_recente"`
#    Usa `.loc[mask, ...]` e `.loc[~mask, ...]` (o un unico `.loc` con due passaggi).
case.loc[mask, 'eta_casa'] = 'recente'
case.loc[~mask, 'eta_casa'] = 'non_recente'
# 3) Report con `.groupby(...).agg(...)`:
#    Raggruppa per `citta` e `eta_casa` e calcola almeno:
#    - `pratiche_totali` (conteggio righe)
#    - `prezzo_medio` (media di `prezzo_euro`)
#    - `metri_quadri_medi` (media di `metri_quadri`)
#    Arrotonda se serve, usa `reset_index()` per una tabella piatta.
report = case.groupby(['citta', 'eta_casa']).agg(
    pratiche_totali = ("id", "count"),
    prezzo_medio = ('prezzo_euro', 'mean'),
    metri_quadri_medi = ('metri_quadri', 'mean')
).round({'prezzo_medio': 2, 'metri_quadri_medi': 2}).reset_index()
# Carica sempre `dati/case.csv`, poi salva il report finale in `dati/report_retrieval_agg.csv`
# (es. `report.to_csv(..., index=False)`).
report.to_csv(os.path.join(os.path.dirname(__file__), "dati", "report_retrieval_agg.csv"), index=False)
#

# ESERCIZIO 8 (Rinforzo focus `.agg`):
# Crea un report "pronto recruiter" con colonne:
# - citta
# - pratiche_totali
# - prezzo_medio
# - metri_quadri_medi
# - quota_case_recenti (anno_costruzione >= 2000, in %)
# - varianza_prezzo
# Vincoli:
# - usare `.agg` in modo esplicito
# - ordinare per `quota_case_recenti` decrescente
# - stampare top 5 e salvare CSV in `dati/report_rinforzo_agg.csv`

case['eta_casa'] = (case['anno_costruzione'] >= 2_000).astype(int)

report = case.groupby('citta').agg(
    pratiche_totali = ('id', 'count'),
    prezzo_medio = ('prezzo_euro', 'mean'),
    metri_quadri_medi = ('metri_quadri', 'mean'),
    quota_case_recenti = ('eta_casa', lambda x: x.mean()*100),
    varianza_prezzo = ('prezzo_euro', 'var')
).round({'prezzo_medio': 2, 'metri_quadri_medi': 2, 'quota_case_recenti': 2, 'varianza_prezzo': 2}).reset_index().sort_values(by='quota_case_recenti', ascending=False)

print(report.head(5))
report.head(5).to_csv(os.path.join(os.path.dirname(__file__), "dati", "report_rinforzo_agg.csv"), index=False)


# ESERCIZIO 9 (Teoria applicata, no codice lungo):
# In massimo 12 righe:
# - descrivi un caso in cui useresti regole manuali e NON ML
# - descrivi un caso in cui useresti ML e NON sole regole
# - spiega per ciascuno: rischio principale + mitigazione

# CASO 1 — Regole manuali, NON ML:
# Validazione codice fiscale: la struttura è fissa (16 caratteri, pattern noto),
# basta un controllo deterministico con regex + checksum.
# Rischio: se il formato cambia (es. nuovo standard), le regole vanno aggiornate a mano.
# Mitigazione: versionare le regole con validità temporale e test automatici.
#
# CASO 2 — ML, NON sole regole:
# Riconoscere se una busta paga è stata alterata graficamente:
# i pattern di manipolazione sono troppi e troppo sottili per scrivere if/else esaustivi.
# Un modello addestrato su esempi storici (genuini vs alterati) generalizza meglio.
# Rischio: il modello può non riconoscere un tipo di alterazione mai visto (falso negativo).
# Mitigazione: monitorare il recall in produzione e aggiungere nuovi casi al training
# quando emergono pattern non coperti (feedback loop con il revisore).


# ==========================================================================
# SOLUZIONI — Solo dopo aver provato
# ==========================================================================
#
# --- RISPOSTE QUIZ D'INGRESSO ---
# 1) Falso (Series)
# 2) (30, 2)
# 3) Usa "=" invece di "=="
# 4) .loc = label, .iloc = posizione numerica
# 5) 0 e 1
#
# --- RISPOSTE QUIZ DI VERIFICA ---
# 1) Vero
# 2) feature, target
# 3) Serve doppia parentesi quadra: case[["metri_quadri", "prezzo_euro"]]
# 4) 4
# 5) Regole a mano = statiche; ML = pattern appresi e adattabili ai dati

