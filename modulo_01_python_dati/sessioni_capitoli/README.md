# Sessioni capitolo — diario persistente

Questa cartella contiene **un file Markdown per capitolo** in cui il mentor annota, durante lo studio:

- domande che fai mentre lavori sul file `.py` del capitolo;
- valutazioni e correzioni quando chiedi feedback su esercizi, quiz o mini-esercizi;
- pattern ricorrenti e note per il **rinforzo** nel capitolo successivo.

## Convenzione di naming

Per il capitolo il cui file è ad esempio `12_web_bridge.py`:

- nome file: **`M01_C12_web_bridge_sessione.md`**
  - `M01` = Modulo 1 (due cifre)
  - `C12` = prefisso numerico del file capitolo (`12_`)
  - `web_bridge` = parte del nome file dopo il numero (slug breve)

Se il file è `04_classificazione_metriche.py` (altro modulo):

- esempio: **`M02_C04_classificazione_metriche_sessione.md`**

Regola pratica: **`M{modulo}_C{NN}_{resto_nome_senza_estensione}_sessione.md`**

## Come si usa

1. **All’inizio** di un nuovo capitolo: copia `_TEMPLATE_sessione_capitolo.md` nel nome corretto (o chiedi al mentor in Agent mode di crearlo).
2. **Durante** il capitolo: a ogni richiesta di valutazione/correzione, il mentor **appende** una voce (non cancellare il resto).
3. **In chiusura capitolo** (`jarvis chiusura/correzione capitolo N`): il mentor legge questo file **insieme** a `CONTESTO_CORSO.md` e `APPUNTI_APPLICATIVO.md` per aggiornare il contesto e preparare rinforzi nel file del capitolo successivo.

## Nota privacy

Contenuto solo in locale sul tuo PC; evita dati sensibili o PII nei snippet se incolli estratti da documenti reali.
