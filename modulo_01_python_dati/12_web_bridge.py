"""
============================================================================
 MODULO 1 — ESERCIZIO 12: Web Bridge — Il Tuo Primo Endpoint AI
 FastAPI: Da Python al Browser
============================================================================

 TEORIA: Collegare Python al Web — Il Ponte tra Due Mondi

 Finora hai lavorato con Python nel terminale. Ma tu sei un web developer:
 vuoi che i risultati arrivino al BROWSER, a una pagina React, a un'app.

 Come si fa? Con un'API! E in Python, la libreria più moderna e veloce
 per creare API è FastAPI.

 ANALOGIA CON LARAVEL (dettagliata):
 ┌────────────────────────────────────────────────────────────────┐
 │  Laravel                       →  FastAPI                     │
 │  ────────────────────────────────────────────────────────────│
 │  Route::get('/api/...', ...)   →  @app.get("/api/...")        │
 │  Route::post('/api/...', ...)  →  @app.post("/api/...")       │
 │  Controller                    →  Funzione con decoratore     │
 │  return response()->json(...)  →  return {"chiave": "valore"} │
 │  php artisan serve             →  uvicorn main:app --reload   │
 │  Porta 8000                    →  Porta 8000 (uguale!)        │
 │  Middleware                    →  Middleware / Depends         │
 │  Request $request              →  Parametri della funzione    │
 │  $request->query('citta')      →  Query(None, ...)            │
 │  $request->validate([...])     →  Validazione automatica!     │
 │  routes/api.php                →  Tutto nello stesso file     │
 │  .env                          →  .env (uguale!)              │
 └────────────────────────────────────────────────────────────────┘

 SPIEGAZIONE DEI CONCETTI LARAVEL (ripasso):
   Route::get('/api/...')    → Definisce una rotta GET nel file routes/api.php
   Controller                → Classe PHP che gestisce la logica di una rotta
   response()->json(...)     → Restituisce una risposta in formato JSON
   php artisan serve         → Avvia il server di sviluppo Laravel sulla porta 8000
   Middleware                → Codice che "filtra" le richieste prima del controller
   Request $request          → L'oggetto che contiene tutti i dati della richiesta
   $request->query('citta')  → Prende il parametro 'citta' dalla query string (?citta=Roma)
   $request->validate(...)   → Valida i dati in ingresso secondo regole specifiche

 In FastAPI tutto questo si fa con MENO codice:
   - Non serve creare file separati per rotte e controller
   - La validazione è automatica (se dici che un parametro è int, FastAPI
     controlla da solo e restituisce errore 422 se non lo è)
   - La documentazione è GENERATA AUTOMATICAMENTE

 FastAPI ha la DOCUMENTAZIONE AUTOMATICA delle API:
 dopo aver avviato il server, vai su http://localhost:8000/docs
 e trovi una pagina interattiva dove testare ogni endpoint
 (come Postman, ma integrato!). In Laravel dovresti installare
 un pacchetto come Swagger/L5-Swagger per ottenere la stessa cosa.

 COME AVVIARE IL SERVER:
 Nel terminale, dalla cartella del corso:
   cd modulo_01_python_dati
   uvicorn 12_web_bridge:app --reload

 Poi apri il browser su http://localhost:8000

============================================================================
"""

# ==========================================================================
# QUIZ D'INGRESSO (dal capitolo 11 — Matplotlib + report pre-plot)
# ==========================================================================
#
# 1) [Definizione] Differenza tra `size()`, `count()` e `nunique()` in Pandas?
#    Scrivi un esempio pratico su "ordini unici".
# in un dataframe, .size() conta le righe di uno specifico gruppo,  .count() conta tutte le righe che non hanno valore null
# e infine nunique conta gli elementi con valore unico
#
# 2) [Trova l'errore] In un esercizio hai scritto:
#    `quantita = vendite.groupby("prodotto")["quantita"].sum()`
#    ma la consegna chiedeva "quantità per categoria".
#    Qual è l'errore concettuale? avrei dovuto raggruppare per categoria e non per prodotto
#
# 3) [Vero/Falso] `sort_index()` ordina i valori della Series. 
# falso, ordine in base all'indice, e non per valore
#
# 4) [Prevedi output] Se `s = pd.Series([10, 20], index=["b", "a"])`,
#    cosa produce `s.sort_index()`?
# { a: 20, b: 10 }
#
# 5) [Completa codice] Completa:
#    `ordini_unici = vendite.groupby("citta")["id_ordine"].nunique()`
#
# 6) [Vero/Falso] Con `density=True` in `hist()`, l'asse Y rappresenta il conteggio righe. 
# falso, riporta il dato normalizzato per rappresentare il peso di un dato
#
# 7) [Spiega con parole tue - opzionale ingresso]
#    Perché "report corretto prima del grafico" evita errori anche nelle API?
# perchè fare un controllo sulla qualità, in generale evita che qualcosa posso bloccarsi

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import numpy as np
import os

# ==========================================================================
# SETUP: Creare l'App FastAPI
# ==========================================================================

# In Laravel crei un'app con:
#   laravel new progetto          → crea un'intera struttura di cartelle
#   // app/, routes/, config/, database/, resources/, public/...
#   // Decine di file generati automaticamente
#
# In FastAPI crei un'app con UNA riga — niente struttura, niente cartelle:

app = FastAPI(
    title="Modulo 1 — API Dati",
    description="Il tuo primo endpoint che collega Python al web!",
    version="1.0.0"
)

# CORS: permette al frontend React di chiamare questa API.
# Cos'è CORS? Quando il tuo frontend React (es. localhost:3000) chiama
# un'API su un dominio diverso (es. localhost:8000), il browser BLOCCA
# la richiesta per sicurezza. CORS dice al browser: "va bene, lascia passare".
#
# In Laravel useresti il pacchetto fruitcake/laravel-cors, oppure da Laravel 7+
# il file config/cors.php è già incluso.
# In FastAPI aggiungi un middleware:
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In produzione metti il dominio del frontend
    allow_methods=["*"],
    allow_headers=["*"],
)

# Carichiamo i dataset all'avvio (come un "singleton" in Laravel)
percorso_dati = os.path.join(os.path.dirname(__file__), "dati")
case = pd.read_csv(os.path.join(percorso_dati, "case.csv"))
vendite = pd.read_csv(os.path.join(percorso_dati, "vendite_ecommerce.csv"))

# Prepariamo i dati
vendite["prezzo"] = vendite["prezzo"].astype(float)
vendite["quantita"] = vendite["quantita"].astype(int)
vendite["fatturato"] = vendite["prezzo"] * vendite["quantita"]

case['prezzo_euro'] = case['prezzo_euro'].astype(float)

# --- MINI-ESERCIZIO 1 — Prova subito! ---
# 1) Stampa `vendite.shape` e `case.shape`
# 2) Stampa quante città uniche ci sono in `vendite`
# 3) Verifica il tipo di `vendite["fatturato"]`
# Scrivi qui sotto:
print(f"{vendite.shape}")
print(f"{case.shape}")
print(f"{vendite['citta'].nunique()}")
print(f"{type(vendite['fatturato'])}")

# ==========================================================================
# 🔁 RINFORZO MIRATO — Dal grafico all'API: stessa logica, stessi errori
# ==========================================================================
#
# Nel capitolo 11 sono emerse 3 fragilita importanti:
# 1) metrica giusta ma asse/label sbagliati
# 2) groupby sulla dimensione sbagliata (es. prodotto vs categoria)
# 3) consegna letta parzialmente (manca un requisito)
#
# In API succede UGUALE:
# - endpoint = "grafico senza grafico"
# - se l'aggregazione e sbagliata, restituisci JSON "formalmente valido" ma concettualmente errato
#
# Mini-regola pratica prima di ogni endpoint:
# - COSA devi contare?
#   * ordini unici -> nunique("id_ordine")
#   * righe/documenti -> size() o count()
#   * quantita venduta -> sum("quantita")
# - SU QUALE dimensione?
#   * per citta / per categoria / per prodotto (non confonderle)
# - NOME CHIAVI JSON coerente con la metrica (es. "ordini_unici", non solo "ordini")
#
# Mini-check di consegna (obbligatorio):
# [ ] ho tutti i campi richiesti in output
# [ ] ho i tipi giusti (int/float/string)
# [ ] il nome campo descrive davvero il valore
# [ ] il sorting richiesto e applicato

# ==========================================================================
# ENDPOINT 1: Home — Benvenuto
# ==========================================================================

# In Laravel (file routes/api.php):
#   Route::get('/', function () {
#       return response()->json([
#           'messaggio' => 'Benvenuto nella tua prima API!',
#       ]);
#   });
#   // Route::get() definisce una rotta GET
#   // La closure (function() {...}) è il "controller inline"
#   // response()->json() converte l'array PHP in JSON
#
# In FastAPI (tutto nello stesso file):

@app.get("/")
def home():
    """Homepage dell'API — restituisce info generali."""
    return {
        "messaggio": "Benvenuto nella tua prima API Python!",
        "endpoints": [
            {"path": "/vendite/overview", "descrizione": "Overview vendite"},
            {"path": "/vendite/per-citta", "descrizione": "Vendite raggruppate per città"},
            {"path": "/vendite/cerca", "descrizione": "Cerca ordini con filtri"},
            {"path": "/case/overview", "descrizione": "Overview immobiliare"},
            {"path": "/case/stima-prezzo", "descrizione": "Stima il prezzo di una casa"},
            {"path": "/docs", "descrizione": "Documentazione interattiva"},
        ]
    }

# ==========================================================================
# ENDPOINT 2: Overview Vendite
# ==========================================================================

@app.get("/vendite/overview")
def vendite_overview():
    """
    Restituisce un'overview del dataset vendite.
    Come: SELECT COUNT(*), SUM(fatturato), AVG(fatturato) FROM vendite
    """
    return {
        "totale_ordini": int(len(vendite)),
        "fatturato_totale": round(float(vendite["fatturato"].sum()), 2),
        "ordine_medio": round(float(vendite["fatturato"].mean()), 2),
        "prodotti_unici": int(vendite["prodotto"].nunique()),
        "citta_servite": int(vendite["citta"].nunique()),
        "categorie": list(vendite["categoria"].unique()),
    }

# ==========================================================================
# ENDPOINT 3: Vendite per Città
# ==========================================================================

@app.get("/vendite/per-citta")
def vendite_per_citta():
    """
    Fatturato e ordini raggruppati per città.
    Come: SELECT citta, COUNT(*), SUM(fatturato) GROUP BY citta
    """
    report = vendite.groupby("citta").agg(
        ordini_unici=("id_ordine", "nunique"),
        fatturato=("fatturato", "sum"),
        ordine_medio=("fatturato", "mean")
    ).round(2)

    risultato = []
    for citta, dati in report.iterrows():
        risultato.append({
            "citta": citta,
            "ordini_unici": int(dati["ordini_unici"]),
            "fatturato": float(dati["fatturato"]),
            "ordine_medio": float(dati["ordine_medio"])
        })

    return {"data": sorted(risultato, key=lambda x: x["fatturato"], reverse=True)}

    
# ==========================================================================
# ENDPOINT 4: Cerca Ordini (con Query Parameters)
# ==========================================================================

@app.get("/vendite/cerca")
def cerca_ordini(
    citta: str = Query(None, description="Filtra per città"),
    categoria: str = Query(None, description="Filtra per categoria"),
    prezzo_min: float = Query(None, description="Prezzo minimo"),
    prezzo_max: float = Query(None, description="Prezzo massimo"),
    limit: int = Query(10, description="Numero massimo di risultati", le=100),
    quantita_min: int = Query(None, description="quantità minima")
):
    """
    Cerca ordini con filtri opzionali.
    Come: SELECT * FROM vendite WHERE ... LIMIT n

    Esempi:
    - /vendite/cerca?citta=Milano
    - /vendite/cerca?categoria=Elettronica&prezzo_min=50
    - /vendite/cerca?prezzo_max=30&limit=5
    """
    risultato = vendite.copy()

    if citta:
        risultato = risultato[risultato["citta"] == citta]
    if categoria:
        risultato = risultato[risultato["categoria"] == categoria]
    if prezzo_min is not None:
        risultato = risultato[risultato["prezzo"] >= prezzo_min]
    if prezzo_max is not None:
        risultato = risultato[risultato["prezzo"] <= prezzo_max]
    if quantita_min:
        risultato = risultato[risultato['quantita'] >= quantita_min]

    risultato = risultato.head(limit)

    return {
        "filtri_applicati": {
            "citta": citta,
            "categoria": categoria,
            "prezzo_min": prezzo_min,
            "prezzo_max": prezzo_max,
        },
        "risultati": int(len(risultato)),
        "data": risultato.to_dict(orient="records")
    }

# --- MINI-ESERCIZIO 2 — Prova subito! ---
# 1) Aggiungi un filtro opzionale `quantita_min` all'endpoint cerca_ordini
# 2) Se presente, tieni solo righe con `quantita >= quantita_min`
# 3) Testa da browser: /vendite/cerca?quantita_min=2
# Scrivi qui sotto:
@app.get("/vendite/cerca")
def cerca_ordini(
    citta: str = Query(None, description="Filtra per città"),
    categoria: str = Query(None, description="Filtra per categoria"),
    prezzo_min: float = Query(None, description="Prezzo minimo"),
    prezzo_max: float = Query(None, description="Prezzo massimo"),
    limit: int = Query(10, description="Numero massimo di risultati", le=100),
    quantita_min: int = Query(None, description="quantità minima")
):
    """
    Cerca ordini con filtri opzionali.
    Come: SELECT * FROM vendite WHERE ... LIMIT n

    Esempi:
    - /vendite/cerca?citta=Milano
    - /vendite/cerca?categoria=Elettronica&prezzo_min=50
    - /vendite/cerca?prezzo_max=30&limit=5
    """
    risultato = vendite.copy()

    if citta:
        risultato = risultato[risultato["citta"] == citta]
    if categoria:
        risultato = risultato[risultato["categoria"] == categoria]
    if prezzo_min is not None:
        risultato = risultato[risultato["prezzo"] >= prezzo_min]
    if prezzo_max is not None:
        risultato = risultato[risultato["prezzo"] <= prezzo_max]
    if quantita_min is not None:
        risultato = risultato[risultato['quantita'] >= quantita_min]

    risultato = risultato.head(limit)

    return {
        "filtri_applicati": {
            "citta": citta,
            "categoria": categoria,
            "prezzo_min": prezzo_min,
            "prezzo_max": prezzo_max,
            "quantita_min": quantita_min
        },
        "risultati": int(len(risultato)),
        "data": risultato.to_dict(orient="records")
    }

# ==========================================================================
# ENDPOINT 5: Overview Case
# ==========================================================================

@app.get("/case/overview")
def case_overview():
    """Overview del dataset immobiliare."""
    case_per_citta = case.groupby('citta')
    per_citta = {}

    return {
        "totale_case": int(len(case)),
        "prezzo_medio": round(float(case["prezzo_euro"].mean()), 0),
        "prezzo_min": int(case["prezzo_euro"].min()),
        "prezzo_max": int(case["prezzo_euro"].max()),
        "mq_medi": round(float(case["metri_quadri"].mean()), 0),
        "citta": list(case["citta"].unique()),
        "per_citta":
        {
            c: {
            "case": int(len(d)),
            "prezzo_medio": float(round(d['prezzo_euro'].mean(), 2))
            }
            for c, d in case_per_citta
        }
    }
# ==========================================================================
# ENDPOINT 6: Stima Prezzo Casa (Preview di Machine Learning!)
# ==========================================================================

@app.get("/case/stima-prezzo")
def stima_prezzo(
    # Query(...) definisce un parametro letto dalla query string della URL.
    # Esempio: /case/stima-prezzo?metri_quadri=80&num_stanze=3
    #
    # Parametri di Query usati qui:
    # - primo argomento:
    #   ...   -> parametro obbligatorio (se manca, FastAPI risponde con errore 422)
    #   False -> parametro opzionale con default False
    #   5.0   -> parametro opzionale con default 5.0
    # - description="...":
    #   testo mostrato in /docs (Swagger), utile per documentare l'API.
    # - ge=...:
    #   "greater or equal" -> valore minimo accettato (>=).
    # - le=...:
    #   "less or equal" -> valore massimo accettato (<=).
    #
    # Nota sui type hint:
    # int/float/bool prima di "=" servono a FastAPI per fare parsing + validazione.
    # Se arriva un tipo non coerente, l'API restituisce 422 con dettaglio errore.
    metri_quadri: int = Query(..., description="Superficie in mq", ge=20, le=300),
    num_stanze: int = Query(..., description="Numero di stanze", ge=1, le=10),
    ha_garage: bool = Query(False, description="Ha il garage?"),
    distanza_centro_km: float = Query(5.0, description="Distanza dal centro in km", ge=0),
):
    """
    Stima il prezzo di una casa con una regola euristica semplice.

    Cosa significa "euristica"?
    - E una formula manuale costruita da noi, non un modello addestrato.
    - Serve come ponte didattico tra "analisi dati" e "predizione".
    - E utile per capire la pipeline end-to-end API -> input -> calcolo -> output JSON.

    Flusso logico dell'endpoint:
    1) Legge i parametri dalla query string validandoli (tipi + vincoli ge/le).
    2) Calcola un prezzo base usando il prezzo medio al metro quadro del dataset.
    3) Applica correttivi moltiplicativi (garage, distanza dal centro, stanze).
    4) Restituisce la stima con il dettaglio dei parametri usati.

    Perche usare moltiplicatori (1.15, 1.20, ecc.)?
    - Sono una forma semplice per "pesare" fattori che aumentano/diminuiscono il prezzo.
    - E simile a dire: "parti dal valore medio, poi applica bonus/malus percentuali".

    Limiti dichiarati (importante per trasparenza tecnica):
    - Non impara dai dati in modo statistico come farebbe il Machine Learning.
    - Le percentuali sono regole manuali, quindi non ottimizzate automaticamente.
    - Non considera tutte le feature possibili (zona, anno, stato immobile, ecc.).

    Esempio:
    /case/stima-prezzo?metri_quadri=80&num_stanze=3&ha_garage=true&distanza_centro_km=2.5
    """
    # Passo 1: baseline dal dataset storico.
    # prezzo_al_mq = totale prezzi / totale mq
    # Questo evita il bias che avresti facendo una semplice media di (prezzo/mq) riga per riga.
    prezzo_al_mq = case["prezzo_euro"].sum() / case["metri_quadri"].sum()

    # Passo 2: stima base della casa target.
    # E il prezzo "neutro" prima dei correttivi.
    stima_base = metri_quadri * prezzo_al_mq

    # Passo 3: correttivi euristici.
    # Garage -> bonus fisso percentuale.
    if ha_garage:
        stima_base *= 1.15
        

    # Distanza centro -> fascia di impatto.
    # Nota: if/elif/else assicura che applichiamo UNA sola fascia.
    if distanza_centro_km < 2:
        stima_base *= 1.20
    elif distanza_centro_km < 5:
        stima_base *= 1.05
    else:
        stima_base *= 0.90

    # Numero stanze -> incremento progressivo.
    # Esempio: 3 stanze => (1 + 3*0.03) = 1.09 => +9%
    stima_base *= (1 + num_stanze * 0.03)

    # Passo 4: response JSON "frontend-ready", con numeri puliti.
    # round(..., 0) produce il prezzo finale arrotondato all'euro.
    return {
        "stima_prezzo": round(float(stima_base), 0),
        "parametri": {
            "metri_quadri": metri_quadri,
            "num_stanze": num_stanze,
            "ha_garage": ha_garage,
            "distanza_centro_km": distanza_centro_km,
        },
        "nota": "Stima basata su medie semplici. Nel Modulo 2 costruiremo un modello ML molto piu accurato!",
        "prezzo_al_mq_medio_dataset": round(float(prezzo_al_mq), 2)
    }

# --- MINI-ESERCIZIO 3 — Prova subito! ---
# Obiettivo: consolidare Query params + validazione + logica euristica.
#
# 1) Aggiungi un nuovo parametro opzionale:
#    piano_alto: bool = Query(False, description="Immobile a piano alto?")
#
# 2) Se piano_alto e True, applica un bonus del +4% alla stima:
#    stima_base *= 1.04
#
# 3) Aggiungi il parametro "piano_alto" nel blocco "parametri" del JSON di risposta.
#
# 4) Testa questi due URL e confronta "stima_prezzo":
#    - /case/stima-prezzo?metri_quadri=90&num_stanze=3&ha_garage=true&distanza_centro_km=3
#    - /case/stima-prezzo?metri_quadri=90&num_stanze=3&ha_garage=true&distanza_centro_km=3&piano_alto=true
#
# 5) (Extra) Prova a inviare metri_quadri=10 e osserva l'errore 422:
#    spiega con parole tue quale regola di validazione lo blocca.
#
# Scrivi qui sotto:
@app.get("/case/stima-prezzo")
def stima_prezzo(    
    metri_quadri: int = Query(..., description="Superficie in mq", ge=20, le=300),
    num_stanze: int = Query(..., description="Numero di stanze", ge=1, le=10),
    ha_garage: bool = Query(False, description="Ha il garage?"),
    distanza_centro_km: float = Query(5.0, description="Distanza dal centro in km", ge=0),
    piano_alto: bool = Query(False, description="E' un piano alto?")
):    
    prezzo_al_mq = case["prezzo_euro"].sum() / case["metri_quadri"].sum()

    stima_base = metri_quadri * prezzo_al_mq
    
    if ha_garage:
        stima_base *= 1.15
        
    if piano_alto:
        stima_base *= 1.04

    if distanza_centro_km < 2:
        stima_base *= 1.20
    elif distanza_centro_km < 5:
        stima_base *= 1.05
    else:
        stima_base *= 0.90

    stima_base *= (1 + num_stanze * 0.03)
    return {
        "stima_prezzo": round(float(stima_base), 0),
        "parametri": {
            "metri_quadri": metri_quadri,
            "num_stanze": num_stanze,
            "ha_garage": ha_garage,
            "distanza_centro_km": distanza_centro_km,
            "piano_alto": piano_alto,
        },
        "nota": "Stima basata su medie semplici. Nel Modulo 2 costruiremo un modello ML molto piu accurato!",
        "prezzo_al_mq_medio_dataset": round(float(prezzo_al_mq), 2)
    }

# ==========================================================================
# ENDPOINT 7: Statistiche per la Data Visualization (per React)
# ==========================================================================

@app.get("/vendite/stats-per-grafici")
def stats_per_grafici():
    """
    Restituisce payload gia pronto per grafici frontend.

    Obiettivo pratico:
    - Evitare logica di aggregazione nel browser.
    - Tenere la "single source of truth" nel backend.
    - Consegnare al frontend una struttura standard labels/values.

    Struttura pensata per librerie tipiche (Chart.js / Recharts):
    {
      "grafico_x": {
        "labels": [...],
        "values": [...]
      }
    }

    Perche e utile in un'app reale?
    - Il team frontend consuma JSON coerente senza conoscere Pandas.
    - Se cambia la logica business (es. metrica), la aggiorni una sola volta qui.
    - Riduci bug di allineamento tra report backend e dashboard UI.
    """
    # 1) Bar chart: fatturato per categoria.
    # GROUP BY categoria + SUM fatturato
    fatt_cat = vendite.groupby("categoria")["fatturato"].sum().round(2)

    # 2) Pie chart: numero ordini per citta.
    # value_counts conta le occorrenze per valore.
    ordini_citta = vendite["citta"].value_counts()

    # 3) Line chart: serie temporale fatturato giornaliero.
    fatt_giorno = vendite.groupby("data")["fatturato"].sum().round(2)

    # Conversione in liste JSON-serializzabili.
    # Nota: in alcuni casi conviene cast esplicito int/float per evitare tipi NumPy.
    return {
        "grafico_barre_categorie": {
            "labels": list(fatt_cat.index),
            "values": list(fatt_cat.values)
        },
        "grafico_torta_citta": {
            "labels": list(ordini_citta.index),
            "values": [int(v) for v in ordini_citta.values]
        },
        "grafico_linea_tempo": {
            "labels": list(fatt_giorno.index),
            "values": list(fatt_giorno.values)
        }
    }


# ==========================================================================
# 🔁 RINFORZO MIRATO — Coerenza requisito -> output API
# ==========================================================================
#
# Regola d'oro:
# requisito business -> chiave groupby -> output API.
#
# Se la richiesta e "quantita vendute PER CATEGORIA", il groupby DEVE essere
# sulla colonna "categoria". Se fai groupby("prodotto"), hai cambiato domanda.
#
# Mappa mentale veloce:
# - "per categoria" -> groupby("categoria")
# - "per citta"     -> groupby("citta")
# - "per giorno"    -> groupby("data")
#
# Esempio corretto:
# quantita_categoria = (
#     vendite.groupby("categoria")["quantita"]
#     .sum()
#     .sort_values(ascending=False)
# )
#
# Output API frontend-ready:
# {
#   "labels": [...categorie...],
#   "values": [...quantita...]
# }
#
# Perche questo rinforzo e importante:
# un grafico bello ma con aggregazione sbagliata racconta una bugia.
# Nel prodotto reale questo porta decisioni operative sbagliate.


# ╔═════════════════════════════════════════════════════════════════════════╗
# ║  COME TESTARE                                                         ║
# ╚═════════════════════════════════════════════════════════════════════════╝
#
# Procedura completa (Windows + Git Bash):
#
# 1) Apri terminale nella root del progetto.
# 2) Attiva virtual environment (se presente):
#    venv\Scripts\activate
# 3) Vai nella cartella del capitolo:
#    cd modulo_01_python_dati
# 4) Avvia il server in hot-reload:
#    uvicorn 12_web_bridge:app --reload
#
# 5) Test rapido "is alive":
#    http://localhost:8000
#    Se risponde, il server e su.
#
# 6) Test docs auto-generate (Swagger UI):
#    http://localhost:8000/docs
#    Qui puoi chiamare endpoint senza Postman.
#
# 7) Test endpoint principali:
#    http://localhost:8000/vendite/overview
#    http://localhost:8000/vendite/cerca?citta=Milano
#    http://localhost:8000/vendite/cerca?prezzo_min=50&prezzo_max=200&limit=5
#    http://localhost:8000/case/stima-prezzo?metri_quadri=80&num_stanze=3&ha_garage=true
#
# 8) Test edge case utili:
#    - limit oltre soglia (deve bloccare per `le=100`)
#    - prezzo_min=0 (deve essere accettato)
#    - distanza_centro_km negativa (deve dare errore validazione)
#
# 9) Per fermare il server:
#    Ctrl+C nel terminale.


# ╔═════════════════════════════════════════════════════════════════════════╗
# ║  ESERCIZI — Ora Prova Tu!                                             ║
# ╚═════════════════════════════════════════════════════════════════════════╝

# ==========================================================================
# QUIZ DI VERIFICA (capitolo 12 — FastAPI Web Bridge)
# ==========================================================================
#
# 1) [Definizione]
# Cosa fa `@app.get("/path")` in FastAPI?
# Spiega:
# - come collega URL -> funzione Python
# - quando quella funzione viene eseguita
# - che tipo di risposta produce di default
#in pratica esegue una chiamata di tipo get, la quale innesca la funzione collegata e restituisce una risposta di 
# tipo json
#
# 2) [Vero/Falso + perche]
# FastAPI genera automaticamente docs interattive su `/docs`.
# Rispondi V/F e aggiungi una riga di spiegazione tecnica.
#Vero, /docs è l'url a cui trovare la ui di Swagger che permette di visualizzare tutte le api e 
#testarne il corretto funzionamento
#
# 3) [Trova l'errore]
# In un endpoint di filtro usi:
# `if prezzo_max:` invece di `if prezzo_max is not None:`
# Perche puo essere un bug quando il client invia `prezzo_max=0`?
# Perchè 0 è un valore falsy, quindi la richiesta qualora coincidesse con 0 non eseguirebbe il blocco if

# 4) [Prevedi output]
# Se chiami `/vendite/cerca?limit=2`, quel parametro limita:
# A) numero massimo righe restituite
# B) numero colonne
# C) valore massimo del prezzo
# Scegli e spiega in una frase.
#restituisce le prime 2 righe, ossia limita la mia ricerca ai primi 2 risultati

# 5) [Completa codice]
# Completa:
# `@app.get("/ping")`
# `def ping():`
# `    return {"status": "____"}`
# Poi aggiungi una seconda chiave utile per debugging (es. versione API).
#
# 6) [Spiega con parole tue - Feynman]
# Spiega a un collega Laravel la differenza tra:
# - endpoint "controller-like" (Route + Controller separati)
# - funzione FastAPI decorata
# Includi almeno 1 pro e 1 contro di ciascun approccio.
#In laravel, le rotte sono gestire dal file web.php, nel quale è contenuta la logica che collega un url e un chiamata
#di tipo GET o POST, e un file chiamato controller, che gestisce l'esecuzione di una specifica funzione. E' un metodo
#molto schematico che spacchetta i passaggi, ma in appliccativi grandi diventa difficile gestire i flussi.
#Fastapi consente di risparmiare codice, e fare tutto in un un unico file, rendendo tutto molto più compatto, ma potenzialmente
#apre a confuzione nel momento in cui nello stesso file cominciamo a gestire tante rotte diverse.
#
# Scrivi le risposte qui sotto (nei commenti) prima degli esercizi.

# 🎯 [COLLOQUIO] ESERCIZIO 1 (Facile):
# Aggiungi un endpoint GET /vendite/top-prodotti che restituisca
# i top 5 prodotti per fatturato.
# Deve restituire: [{"prodotto": "...", "fatturato": 123.45, "quantita": 10}, ...]
#
# Obiettivo colloquio:
# - verificare se sai tradurre una richiesta business in query Pandas
# - verificare se sai pulire i tipi in output JSON (int/float/string)
#
# Checklist prima di consegnare:
# - groupby corretto su "prodotto"
# - fatturato somma, quantita somma
# - ordinamento decrescente su fatturato
# - limit applicato (default 5)
# - niente tipi NumPy "grezzi" nel JSON finale
#
# Scrivi il tuo codice qui sotto (aggiungi una nuova funzione con @app.get):
path_file = os.path.join(os.path.dirname(__file__),"dati", "vendite_ecommerce.csv")
vendite = pd.read_csv(path_file)
vendite['fatturato'] = vendite['prezzo'] * vendite['quantita']
@app.get("/vendite/top-prodotti")
def top_prodotti(
    limit: int = Query(5, description="Numero massimo di risultati", le=10)
):
    """
    In questo endpoint vengono trovati i 5 prodotti migliori rispetto al
    fatturato generato raccolto all'interno del dataset preso in considerazione
    """
    top_prodotti = vendite.groupby('prodotto').agg(
        fatturato_totale = ("fatturato", lambda x: x.sum().round(2) ),
        totale_ordini = ("quantita", "sum")
    )
    sorted_top = top_prodotti.sort_values(by="fatturato_totale", ascending=False).head(limit)
    risultato = []
    for prodotto, dati in sorted_top.iterrows():
        risultato.append({
            "prodotto": prodotto,
            "fatturato_totale": float(dati['fatturato_totale']),
            "quantita": int(dati['totale_ordini'])
        })
    return risultato   


# 🔀 [INTERLEAVING] ESERCIZIO 2 (Medio):
# Aggiungi un endpoint GET /case/cerca che accetti parametri:
# - citta (opzionale)
# - mq_min e mq_max (opzionali)
# - prezzo_max (opzionale)
# - ha_garage (opzionale, booleano)
# Restituisci le case che corrispondono ai filtri.
#
# Perche e interleaving:
# - mescola FastAPI (query params) + Pandas (maschere) + logica booleana.
# - non stai ripetendo un pattern uguale al precedente: devi scegliere lo strumento giusto.
#
# Attenzione ai bug tipici:
# - per parametri numerici opzionali usa `is not None`
# - per bool opzionale valuta bene `None` vs `False`
# - applica i filtri in modo cumulativo, non alternativo
#
# Scrivi il tuo codice qui sotto:

@app.get("/case/cerca")
def cerca_case(
    citta: str = Query(None, description="Città"),
    mq_min: int = Query(None, description="Metri quadri minimi", ge=0, le=200),
    mq_max: int = Query(None, description="Metri quadri massimi", ge=0, le=200),
    ha_garage: bool = Query(None, description="Ha il garage?")
):
    risultato = case
    if citta:
        risultato = risultato[risultato["citta"] == citta]
    if mq_min is not None:
        risultato = risultato[risultato['metri_quadri'] >= mq_min]
    if mq_max is not None:
            risultato = risultato[risultato['metri_quadri'] <= mq_max]
    if ha_garage is not None:
        risultato = risultato[risultato['ha_garage'] == ha_garage]
    return risultato.to_dict(orient="records")


# 🧠 [RETRIEVAL] ESERCIZIO 4 (Memoria attiva):
# Senza guardare gli endpoint sopra, riscrivi da zero un endpoint GET
# `/vendite/per-categoria` che restituisca:
# - categoria
# - ordini_unici (nunique su id_ordine)
# - fatturato_totale
# ordinato per fatturato_totale decrescente.
#
# Vincolo: usa naming coerente e tipi JSON puliti (int/float/string).
#
# Obiettivo retrieval:
# - richiamare da memoria schema endpoint + pipeline groupby/agg/sort
# - verificare che il pattern sia davvero interiorizzato senza copia/incolla

@app.get("/vendite/per-categoria")
def per_categoria():
    vendite['fatturato'] = vendite['quantita'] * vendite['prezzo']
    vendite_per_categoria = vendite.groupby('categoria').agg(
        ordini_unici = ("id_ordine", "nunique"),
        fatturato_totale = ("fatturato", "sum")        
    )
    sorted_vendite = vendite_per_categoria.sort_values(by="fatturato_totale", ascending=False).round(2)
    risultati = []
    for categoria, dati in sorted_vendite.iterrows():
        risultati.append({
            "categoria": str(categoria),
            "ordini_unici": int(dati['ordini_unici']),
            "fatturato_totale": float(dati['fatturato_totale'])
        })
    return {"data": risultati}


# 🏗️ PRODOTTO REALE (micro-task capitolo 12) — Bridge verso app documentale
# Obiettivo: aggiungi un endpoint preview "semaforo operativo" riusando i dati disponibili.
#
# Task:
# 1) Crea GET /pratiche/semaforo-preview
# 2) Restituisci una lista di record con:
#    - id_pratica (puo essere id_ordine nel mock)
#    - score_genuinita (mock semplice 0-100)
#    - semaforo (verde/giallo/rosso in base a soglie)
#    - motivo_top1
#
# Deliverable atteso:
# - endpoint funzionante e visibile in /docs
# - JSON coerente con naming prodotto (score/semaforo/motivo)
#
# Definition of Done minima:
# - almeno 5 record in output
# - semaforo coerente con score
# - naming chiavi allineato a APPUNTI_APPLICATIVO.md
#
# Suggerimento architetturale:
# - tieni una piccola funzione helper per mappare score -> semaforo
# - in questo modo quando cambiano le soglie modifichi un solo punto
path_mock = os.path.join(os.path.dirname(__file__),"dati", "pratiche_semaforo_mock.csv")
pratiche = pd.read_csv(path_mock)

def scoring_semaforo(scoring: int):
    if scoring >= 80:
        return "verde"
    if scoring >= 50:
        return "giallo"
    else:
        return "rosso"
    
@app.get("/pratiche/semaforo-preview")
def scoring_pratiche():
    """
    Questo endpoint restituisce una valutazione, espressa tramite semaforo "verde, giallo o rosso", 
    delle pratiche presenti all'interno di una dataset di prova, a partire da uno scoring da 1 a 100
    sulla genuinità, accompagnata da una breve descrizione sul motivo dello scoring
    """
    pratiche_ordinate = pratiche.sort_values(by="score_genuinita", ascending=False)
    pratiche_ordinate['semaforo'] = pratiche_ordinate['score_genuinita'].apply(lambda x : scoring_semaforo(int(x)))
    result = []
    for _, riga in pratiche_ordinate.iterrows():
        result.append({
            "id_pratica": riga['id_pratica'],
            "score_genuinita": int(riga['score_genuinita']),
            "semaforo": riga['semaforo'],
            "motivo_top1": riga['motivo_top1']
        })
    return {"dati": result}
    

# 🏗️ PROGETTO INCREMENTALE — Modulo 1 / Capitolo 12
# Obiettivo capitolo: esporre via API il primo "ponte web" del progetto documentale.
#
# Task:
# - crea endpoint `/progetto/overview` che ritorni:
#   - totale_pratiche_mock
#   - score_medio_mock
#   - distribuzione_semaforo_mock
# - crea endpoint `/progetto/pratiche` con filtro opzionale `semaforo`
# - usa naming allineato al prodotto (`id_pratica`, `score_genuinita`, `semaforo`, `motivo_top1`)
#
# Deliverable:
# - endpoint testabili da `/docs`
# - JSON coerente con schema deciso negli appunti
#
# Definition of Done:
# - almeno 1 endpoint overview + 1 endpoint lista filtrabile
# - filtro `semaforo` funzionante
# - output pronto per consumo frontend (React)
#
# Focus didattico:
# con questo task chiudi il "ponte web" del Modulo 1:
# dai dati locali (Pandas) a una API che un frontend puo consumare.
# Questo e il primo mattoncino concreto del prodotto finale portfolio-ready.
@app.get("/progetto/overview")
def analisi_mock():
    totale_pratiche = pratiche['id_pratica'].nunique()
    scoring_medio = pratiche['score_genuinita'].mean().round(2)
    copia_pratiche = pratiche.copy()
    copia_pratiche['semaforo'] = copia_pratiche['score_genuinita'].apply(lambda x:scoring_semaforo(int(x)))
    tot = copia_pratiche['id_pratica'].nunique()
    perc_verdi = (len(copia_pratiche.loc[copia_pratiche['semaforo'] == "verde"]) / tot) * 100
    perc_gialli = (len(copia_pratiche.loc[copia_pratiche['semaforo'] == "giallo"]) / tot) * 100
    perc_rossi = (len(copia_pratiche.loc[copia_pratiche['semaforo'] == "rosso"]) / tot) * 100
    
    return {"dati": {
        "totale_pratiche_mock": totale_pratiche,
        "score_medio_mock": scoring_medio,
        "distribuzione_semaforo_mock_percentuali": {
            "verdi": round(float(perc_verdi), 2),
            "gialli": round(float(perc_gialli), 2),
            "rossi": round(float(perc_rossi), 2)
            }
        }
    }


@app.get("/progetto/pratiche")
def progetto_pratiche(semaforo: str = Query(None, description="Filtro opzionale: verde/giallo/rosso")):
    """
    Restituisce la lista pratiche mock in formato frontend-ready.
    Se `semaforo` e valorizzato, applica il filtro per stato.
    """
    copia_pratiche = pratiche.copy()
    copia_pratiche["semaforo"] = copia_pratiche["score_genuinita"].apply(lambda x: scoring_semaforo(int(x)))

    if semaforo:
        valore = semaforo.strip().lower()
        if valore in {"verde", "giallo", "rosso"}:
            copia_pratiche = copia_pratiche[copia_pratiche["semaforo"] == valore]

    data = []
    for _, riga in copia_pratiche.iterrows():
        data.append({
            "id_pratica": riga["id_pratica"],
            "score_genuinita": int(riga["score_genuinita"]),
            "semaforo": riga["semaforo"],
            "motivo_top1": riga["motivo_top1"],
        })

    return {"risultati": int(len(data)), "data": data}
# ╔═════════════════════════════════════════════════════════════════════════╗
# ║  SOLUZIONI                                                             ║
# ╚═════════════════════════════════════════════════════════════════════════╝

# --- SOLUZIONI QUIZ D'INGRESSO (sintesi) ---
# 1) size=righe del gruppo, count=non-null della colonna, nunique=valori distinti
# 2) Errore dimensione: richiesta per categoria, implementato per prodotto
# 3) Falso (sort_index ordina indice)
# 4) indice ordinato: a->20, b->10
# 5) nunique
# 6) Falso (density=True -> densita/probabilita, non conteggio puro)
# 7) Perche l'API espone la stessa aggregazione usata nel report/grafico

# --- SOLUZIONI QUIZ DI VERIFICA (sintesi) ---
# 1) Collega una route GET a una funzione Python
# 2) Vero
# 3) Perde il caso prezzo_max=0, serve controllo esplicito su None
# 4) Limita il numero massimo di record restituiti
# 5) {"status": "ok"}
# 6) In FastAPI la funzione decorata e insieme route+handler con validazione automatica

# --- SOLUZIONE ESERCIZIO 1 ---
# @app.get("/vendite/top-prodotti")
# def top_prodotti(limit: int = Query(5, description="Numero di prodotti")):
#     top = vendite.groupby("prodotto").agg(
#         fatturato=("fatturato", "sum"),
#         quantita=("quantita", "sum")
#     ).sort_values("fatturato", ascending=False).head(limit)
#     risultato = []
#     for prodotto, dati in top.iterrows():
#         risultato.append({
#             "prodotto": prodotto,
#             "fatturato": round(float(dati["fatturato"]), 2),
#             "quantita": int(dati["quantita"])
#         })
#     return {"data": risultato}

# --- SOLUZIONE ESERCIZIO 2 ---
# @app.get("/case/cerca")
# def cerca_case(
#     citta: str = Query(None),
#     mq_min: int = Query(None),
#     mq_max: int = Query(None),
#     prezzo_max: float = Query(None),
#     ha_garage: bool = Query(None)
# ):
#     risultato = case.copy()
#     if citta:
#         risultato = risultato[risultato["citta"] == citta]
#     if mq_min:
#         risultato = risultato[risultato["metri_quadri"] >= mq_min]
#     if mq_max:
#         risultato = risultato[risultato["metri_quadri"] <= mq_max]
#     if prezzo_max:
#         risultato = risultato[risultato["prezzo_euro"] <= prezzo_max]
#     if ha_garage is not None:
#         risultato = risultato[risultato["ha_garage"] == int(ha_garage)]
#     return {"risultati": len(risultato), "data": risultato.to_dict(orient="records")}
