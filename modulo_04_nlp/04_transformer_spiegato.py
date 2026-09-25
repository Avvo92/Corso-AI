"""
============================================================================
MODULO 4 — CAPITOLO 04
Il Transformer spiegato: perché GPT funziona
============================================================================

⚠️ PLACEHOLDER — capitolo NON ancora scritto.

----------------------------------------------------------------------------
PERCHÉ ESISTE QUESTO CAPITOLO
----------------------------------------------------------------------------
"Come funziona un Transformer?" è una delle domande da colloquio più
probabili per un ruolo AI Engineer. Non la chiedono per sentirsi recitare
le formule: la chiedono per capire se sai di cosa parli quando usi un LLM.

Capitolo di COMPRENSIONE, non di implementazione. Vale la nota di
calibrazione della roadmap: **capire, non padroneggiare**. Nessuno ti
chiederà di scrivere l'attention a mano, e non la scriveremo.

----------------------------------------------------------------------------
CONTENUTO PREVISTO
----------------------------------------------------------------------------
  Sez. 1  Il problema che il Transformer risolve: gli embedding del cap.02
          danno alla parola "banca" sempre lo stesso vettore, che parli di
          soldi o di un fiume. Serve il CONTESTO
  Sez. 2  Attention come "a cosa guardo mentre leggo questa parola".
          Analogia: rileggere un contratto e, alla parola "il medesimo",
          tornare indietro a cercare a cosa si riferisce
  Sez. 3  Self-attention in una frase italiana ambigua, seguita passo passo
          senza formule. Visualizzazione dei pesi di attenzione
  Sez. 4  Perché "multi-head": più letture in parallelo della stessa frase
  Sez. 5  Posizione: se l'attention guarda tutto insieme, chi si ricorda
          l'ordine delle parole? (il limite 2 del cap.01 torna qui)
  Sez. 6  Encoder, decoder, encoder-decoder: a cosa servono le tre famiglie
          (BERT vs GPT vs T5), spiegate per COSA CI FAI
  Sez. 7  Cosa significa "pre-addestrato" e perché nessuno allena da zero

----------------------------------------------------------------------------
DEFINITION OF DONE (provvisoria)
----------------------------------------------------------------------------
  1) Spiegare l'attention in 60 secondi, a voce, senza formule
  2) Dire perché gli embedding contestuali battono quelli statici del cap.02
  3) Distinguere BERT-like e GPT-like in base al compito
  4) Rispondere a "perché i Transformer hanno soppiantato le RNN" con UN
     argomento solido (parallelizzazione + dipendenze a lunga distanza)
  5) Riconoscere cosa NON si è capito e dirlo, invece di recitare

----------------------------------------------------------------------------
PREREQUISITI E VINCOLI
----------------------------------------------------------------------------
  Prima di aprirlo: cap.03 chiuso, bridge R03 completato.
  Hardware: CPU. Capitolo quasi tutto concettuale + qualche
  visualizzazione dei pesi di attention su frasi corte.

  ⚠️ Regola 42 (vincolante): è il capitolo più discorsivo del modulo.
     Ogni domanda "spiega perché" deve avere, PRIMA, la teoria nello
     stesso file: analogia + meccanismo + esempio guidato. Vietato dare
     per scontato.

  ⚠️ Regola 30 (teoria potenziata): qui serve tutta —
     analogia → meccanismo → esempio guidato → anti-pattern →
     quando sì/no → checklist.

  🔁 Ripassi Regola 43 obbligatori: embedding statici (cap.02), perdita
     dell'ordine in BoW (cap.01), e — se si accenna al training — il
     ripasso onesto di cosa fa la backpropagation (M3 cap.06), senza
     riaprirla.

  📚 Libri: [ALAMMAR] cap. 1 + The Illustrated Transformer (le figure sono
     il motivo per cui questo libro esiste). [NLP-TRANS] cap. 3.

  🎯 MOCK INTERVIEW (Regola 27): questo è il punto naturale del modulo per
     il primo mock del M4 — siamo a metà. Tono freddo, 3 domande, voto
     secco, feedback solo alla fine.

  🏗️ Progetto: capitolo senza deliverable di codice. Se serve una sezione
     prodotto, farla in forma di decisione documentata: quale famiglia di
     modello useremo per il ramo testuale e perché.

============================================================================
"""

if __name__ == "__main__":
    print("Capitolo 04 non ancora scritto: completa prima il cap.03.")
