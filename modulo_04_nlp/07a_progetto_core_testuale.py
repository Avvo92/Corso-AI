"""
============================================================================
MODULO 4 — CAPITOLO 07a (ULTIMO DEL MODULO, parte 1)
Progetto: il core testuale e il suo contratto — senza interfaccia
============================================================================

⚠️ PLACEHOLDER — capitolo NON ancora scritto.

----------------------------------------------------------------------------
PERCHÉ IL CAPITOLO 07 È SPEZZATO IN DUE (decisione 29/09/2026)
----------------------------------------------------------------------------
Il capitolo di assemblaggio è il punto in cui, nel M3, il carico è salito:
cap.10 chiuso con voto difficoltà **8.5**, motivazione testuale dello
studente — *"difficoltà di tenere mentalmente uniti i pezzi di tutta la
pipeline, dall'addestramento alla costruzione del modello fino ad arrivare
all'app"*.

Nel M3 la cosa che ha funzionato è stata la tappa G2: **verificare il core
senza interfaccia**, prima di toccare la UI. Qui quella tappa diventa un
capitolo a sé.

  07a → il componente testuale funziona da riga di comando. Fine.
  07b → sopra ci si mette l'interfaccia, il deploy e il confronto finale.

Due sessioni con una consegna verificabile in mezzo, invece di un unico
blocco da tenere tutto in testa.

----------------------------------------------------------------------------
CONTENUTO PREVISTO
----------------------------------------------------------------------------
  Sez. 1  **Mappa della pipeline, all'INIZIO del capitolo** (non alla fine):
          cosa entra e cosa esce da ogni pezzo, dal testo grezzo alla
          risposta. Un disegno, una riga per stadio
  Sez. 2  Il contratto di inferenza in versione testuale: le stesse 6 voci
          del M3 cap.10 tradotte al testo — modello, classi ordinate,
          tokenizer/pipeline di normalizzazione, vocabolario e IDF,
          soglia, versione
  Sez. 3  Salvare modello e vettorizzatore INSIEME (o l'intera Pipeline).
          È il fix del bug visto al TODO 4 del cap.01
  Sez. 4  La funzione unica di ingresso: `analizza_testo(testo) -> dict`
          con categoria, punteggio, parole decisive
  Sez. 5  Verifica del core **senza UI**: script da riga di comando su 5
          testi, output stampato, tempi misurati
  Sez. 6  Struttura del pacchetto: cartella dedicata, `requirements.txt`
          pinnato, dati di esempio sintetici, niente pesi enormi in git

----------------------------------------------------------------------------
DEFINITION OF DONE (provvisoria)
----------------------------------------------------------------------------
  1) `analizza_testo()` funziona da riga di comando su 5 testi di esempio
  2) Modello e vettorizzatore caricati da file salvato, non ricostruiti
  3) Contratto salvato accanto al modello, con tutte le voci compilate
  4) Tempo di prima chiamata e chiamate successive misurati e annotati
  5) Nessun file pesante entrato in git (controllare `.gitignore`)

  ⚠️ Il capitolo NON si chiude finché la DoD 1-5 non è verde. Solo dopo
     si apre 07b. È il punto di controllo che nel M3 è mancato.

----------------------------------------------------------------------------
PREREQUISITI E VINCOLI
----------------------------------------------------------------------------
  Prima di aprirlo: cap.06 chiuso, bridge R06 completato.
  Hardware: CPU.

  ⚠️ Privacy: solo esempi sintetici — quello che esce da qui finirà in una
     demo pubblica in 07b.

  🔁 Ripassi Regola 43 obbligatori: contratto di inferenza (M3 cap.10),
     il bug del vettorizzatore rifatto in produzione (cap.01 TODO 4),
     tutta la pipeline testuale dei capitoli 01-06.

  🏗️ Progetto (ramo testuale): è il capitolo in cui il ramo testuale
     diventa un componente con interfaccia stabile, chiamabile dal M5
     (LLM) e dal M7 (orchestratore).

============================================================================
"""

if __name__ == "__main__":
    print("Capitolo 07a non ancora scritto: completa prima il cap.06.")
