# Scheda mentor — M4 cap.03 `03_similarita_coseno.py`

> Fonte: **[ALAMMAR]** Hands-On Large Language Models (Alammar & Grootendorst) — parti su
> *embeddings*, *semantic search* e *retrieval*. Uso: riformulare nel capitolo (Regola 44d).
> **Mai** copiare testo dal PDF. Il capitolo deve stare in piedi senza aprire il libro.

## Idee da riformulare nel capitolo (con esercizi sopra)

1. **Semantic search = due fasi: retrieve, poi (eventualmente) re-rank.**
   Prima un set di candidati veloce (top-k sui vettori), poi — se serve — un modello più
   costoso che riordina. Nel corso: la fase 1 è `E @ q` + `top_k`; la fase 2 è rimandata
   (RAG, M6). Esercizio E9: ordinare le fasi e dire chi può essere pre-calcolato.

2. **Bi-encoder vs cross-encoder.**
   - *Bi-encoder* (MiniLM): due "torri" uguali — ogni testo diventa un punto **da solo**.
     I punti dei documenti si possono calcolare **una volta** e salvare (`note_minilm.pkl`):
     a query-time resta solo un vettore da codificare + una matmul. Veloce, scala.
   - *Cross-encoder*: legge la **coppia** (query, documento) insieme e dà un punteggio.
     Più accurato, ma non puoi pre-calcolare nulla: N coppie = N forward. Si usa nel
     re-ranking dei primi 20-50 candidati, non su tutto il corpus.
   Ponte per Gianluca: bi-encoder = indice SQL preparato prima; cross-encoder = JOIN
   costosa fatta solo sulle poche righe già filtrate.

3. **Vettori normalizzati → dot product = coseno.**
   I modelli di sentence-transformers si usano con `normalize_embeddings=True` proprio
   per questo: la similarità diventa una matmul sola. Nel capitolo: Sez. 1, verificato
   sui dati reali (norme di `note_minilm.pkl` tutte 1.0).

4. **La valutazione di una ricerca NON è l'accuracy.**
   I "veri negativi" nel retrieval sono milioni e nessuno li conta: si usano
   precision@k / recall@k (e MRR, qui solo nominato a parole). Nel capitolo: Sez. 4,
   con i numeri veri del corpus (precision@1 = 24/30 = 0.80).

5. **Il punteggio di similarità non è una probabilità.**
   0.80 non vuol dire "80% di fiducia": è una posizione relativa. Conta la **classifica**
   e la **soglia scelta sui dati**, non il numero assoluto (lezione già avviata nel 02b
   con la pagella; qui diventa la Sez. 3).

6. **Limiti noti del retrieval denso**: testi cortissimi (poco contesto), negazioni,
   dati fuori dominio, codici/identificativi (lì serve match esatto o ricerca ibrida).
   Nel capitolo: Sez. 5 "falsi amici" con numeri misurati (negazione 0.942, CF 0.992).

7. **A scala serve un indice**: oltre qualche centinaio di migliaia di vettori si passa
   a indici ANN (approximate nearest neighbor) / vector DB. Citato a parole nella Sez. 6,
   ponte a M6 (ChromaDB, pgvector). Niente implementazione qui.

## Cosa si SCARTA (per ora)

- MRR/NDCG come formule: restano parole; le metriche del corso sono precision@k/recall@k.
- Training del bi-encoder (già intuito in E9 del 02b col contrastivo: basta così).
- Reranker veri (modelli cross-encoder da scaricare): raccontati, non eseguiti.
- Hybrid search (BM25 + denso): solo la regola pratica "cifre → match esatto" (#69);
  il resto è M6.

## Verifica numerica del capitolo (eseguita dal mentor il 19/10/2026)

Numeri calcolati su `dati/mappe/note_minilm.pkl` (30×384, norme 1.0) e sul modello in cache:
- vicino più simile dello stesso tipo: **24/30** → precision@1 = 0.80; errori: indici 2, 13, 17, 18, 20, 26
- precision@3 media = **0.667**
- punteggi vicino1 sbagliati: 0.74, **0.807** (nota 13, estratto→busta), 0.75, 0.475, 0.627, 0.723
- vicino1 giusti: min 0.404 (nota 28), mediana 0.799
- query "prospetto paga di aprile": top3 = nota 1 (busta, 0.612), nota 24 (altro, 0.582), nota 5 (busta, 0.570)
- negazione "il netto supera il lordo" vs invertita: **0.942**
- "netto 1850" vs "netto 1851": 0.935 · CF con 2 caratteri diversi: **0.992**
- "cedolino" vs "busta paga" (testi corti): 0.428

## Verifica numerica — revisione 19/10/2026 (2ª, fix qualità C1–C7)

- **E2 (errore trovato in revisione)**: il codice buggato con `[:3]` NON esplode: stampa 3 note fuori tema (indici peggiori `[16, 7, 19]` → testi di id 16/7/19: estratto conto 0.826, CU 0.907, visura 0.916) e `punteggi.max() = 2.457 > 1`. Crash reale solo su classifica completa: `IndexError: single positional indexer is out-of-bounds` a i=0 (16ª iterazione su 30). E2 riscritto con questi output veri.
- **Soglia**: a 0.70 → errori bloccati 2/6, giusti persi **7/24**; a 0.85 → errori bloccati 6/6, giusti persi **20/24** (per Mini 3.2/3.5).
- **Euclidea = coseno su norme 1**: `dist² = 2 − 2·cos` verificato su E[3] vs E[7] → 1.604118 da entrambe le parti; `argsort(-cos)` ≡ `argsort(dist)`.
- **E6 benchmark nuovo** (le 4 query vecchie davano precision media 0.0): "busta paga con totale competenze e trattenute del mese" → 3 busta_paga (0.708/0.608/0.572), sopra soglia 1; "redditi da lavoro dipendente e ritenute nella certificazione unica" → 3 cu (0.873/0.868/0.657), sopra soglia 2; "estratto conto con elenco movimenti bonifici e saldo progressivo" → 3 estratto_conto (0.479/0.426/0.321), sopra soglia 0 (ranking perfetto, motore muto); "atto notarile" → busta 0.298/altro 0.294/altro 0.286, "non lo so" corretto. precision@3 media sul ranking = **0.917**.
- Query guida Sez. 2.1 ("stipendio e trattenute del mese"): 0.701 busta_paga · 0.677 cu · 0.644 cu.
- Encoding console Windows (cp1252): nei `print` niente U+2212/≈/→ (errore reale trovato in riesecuzione, corretto in ASCII).

