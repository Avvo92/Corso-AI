"""
============================================================================
MODULO 4 — CAPITOLO 02a (parte concettuale)
Embeddings: le coordinate del significato — l'idea
============================================================================

⚠️ PLACEHOLDER — capitolo NON ancora scritto.
   Questo file esiste per fissare struttura, prerequisiti e vincoli.

----------------------------------------------------------------------------
PERCHÉ IL CAPITOLO 02 È SPEZZATO IN DUE (decisione 29/09/2026)
----------------------------------------------------------------------------
Il cap.02 originale mescolava due lavori diversi:
  (a) capire COSA sia un embedding — astrazione pura
  (b) far funzionare `sentence-transformers` — installazioni, download da
      centinaia di MB, cache, modelli multilingua

Tenerli insieme è rischioso: se l'installazione fa storie, la frustrazione
si attacca al concetto. È esattamente quello che è successo nel M3 cap.10,
dove un blocco di piattaforma (paywall Hugging Face) ha contaminato un
capitolo tecnicamente riuscito.

Quindi: **02a = l'idea, zero installazioni. 02b = la pratica.**
Sono due parti dello STESSO capitolo, non due capitoli separati: il bridge
Regola 40 resta uno solo, dopo 02b e prima del cap.03.

----------------------------------------------------------------------------
PERCHÉ ESISTE QUESTO CAPITOLO
----------------------------------------------------------------------------
È IL concetto più importante del modulo, e forse della seconda metà del
corso. Senza embeddings non esistono ricerca semantica, RAG (M6), memoria
degli agenti (M7). Se un capitolo del M4 va studiato due volte, è questo.

Si apre come RISPOSTA ai tre limiti chiusi nel cap.01:
  - sinonimi ("cedolino" ≠ "busta paga" per TF-IDF)
  - ordine perso ("il netto supera il lordo" = "il lordo supera il netto")
  - fuori vocabolario (parola mai vista → ignorata in silenzio)

Non presentarli come tecnologia a sé: presentarli come la cosa che ripara
quei tre buchi.

----------------------------------------------------------------------------
CONTENUTO PREVISTO
----------------------------------------------------------------------------
  Sez. 1  Da "una casella per parola" a "un punto nello spazio":
          perché poche centinaia di dimensioni invece di migliaia di caselle.
          Sparsità vs densità, ripresa diretta dalla Sez. 2.3 del cap.01
  Sez. 2  L'idea distribuzionale: una parola è definita dalla compagnia che
          frequenta. Il famoso re - uomo + donna ≈ regina, con onestà su
          quanto funziona davvero e quanto è aneddoto da slide
  Sez. 3  Da parola a FRASE: perché fare la media degli embedding di parola
          è una baseline debole, e cosa fa invece un sentence-transformer
  Sez. 4  Cosa gli embedding NON catturano: negazione, numeri, entità
          specifiche. Serve per non promettere magia al cap.03
  Sez. 5  Statico vs contestuale: anticipazione onesta del cap.04
          ("banca" del fiume vs "banca" del conto)

----------------------------------------------------------------------------
COME RENDERLO CONCRETO SENZA LIBRERIE (vincolo di questo file)
----------------------------------------------------------------------------
Il capitolo deve girare con numpy/pandas/matplotlib, **niente installazioni**.
Strategia: embedding GIOCATTOLO costruiti a mano in 2 dimensioni, dove lo
studente assegna le coordinate e poi le disegna. Serve a vedere con gli
occhi che "vicino = simile" prima di fidarsi di un modello vero.

Motivo didattico: il profilo dello studente è forte su ciò che è
verificabile a schermo, debole sull'astrazione dichiarativa. Un grafico con
i punti vale più di tre paragrafi.

----------------------------------------------------------------------------
DEFINITION OF DONE (provvisoria)
----------------------------------------------------------------------------
  1) Spiegare cos'è un embedding senza usare la parola "vettore"
  2) Dire perché uno spazio denso di 384 dimensioni batte 20.000 caselle
  3) Disegnare 6-8 parole del dominio documentale in 2D e commentare i gruppi
  4) Elencare 2 cose che gli embedding NON catturano, con esempio proprio
  5) Distinguere embedding statico e contestuale in una frase

----------------------------------------------------------------------------
PREREQUISITI E VINCOLI
----------------------------------------------------------------------------
  Prima di aprirlo: cap.01 chiuso. **Nessuna installazione.**
  Hardware: CPU, matplotlib.

  🔁 Ripassi Regola 43 obbligatori: i tre limiti della Sez. 5 del cap.01,
     sparsità della matrice BoW, similarità coseno (attenzione: lacuna
     **#59**, 1 = stessa direzione, 0 = indipendenti).

  📚 Libri: [ALAMMAR] cap. 2 — è il capitolo dove le figure rendono di più.

  🏗️ Progetto: niente codice di prodotto qui, è la parte concettuale.
     Il deliverable arriva in 02b.

  Esercizi: quiz d'ingresso sul cap.01, mini-esercizi inline,
  1 💬 Feynman ("spiega un embedding a un collega web").
  Gli esercizi 🎯 COLLOQUIO / 🔧 REFACTORING / 🔍 DEBUG / 🧠 RETRIEVAL /
  🔀 INTERLEAVING stanno in **02b**, dove c'è codice vero su cui esercitarli.

============================================================================
"""

if __name__ == "__main__":
    print("Capitolo 02a non ancora scritto: completa prima il cap.01.")
