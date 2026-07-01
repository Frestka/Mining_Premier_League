# Progetto Data Mining - Premier League
VS Code ↔ GitHub ↔ Google Colab

## Setup Iniziale (Da fare SOLO la prima volta)

Se è la prima volta che scarichi questo progetto sul tuo PC, segui questi step:

1. Crea una catella locale chiamata "Mining_Premier_League"

2. **Clona il repository:**
   `https://github.com/Frestka/Mining_Premier_League.git`
3. **Apri la cartella su VS Code.**
4. **Crea l'ambiente virtuale (la "bolla"):**
   `python -m venv .venv`
5. **Attiva la bolla (l'ambiente virtuale):**
   - **Su Mac / Linux:** `source .venv/bin/activate`
   - **Su Windows:** `.\.venv\Scripts\activate`
   
   *(Attenzione all'errore tipico di Windows: se ricevi un testo rosso pieno di errori che dice "L'esecuzione di script è disabilitata...", apri PowerShell come Amministratore e lancia `Set-ExecutionPolicy RemoteSigned -Scope CurrentUser`, premi Invio, scrivi S e riprova).*
6. **Installa e attiva le librerie:**
   `pip install -r requirements.txt`
   `nbstripout --install`  (Questo comando serve a pulire i grafici pesanti dai notebook prima di salvarli su GitHub, evitando conflitti di codice).
7. **Scarica il dataset:**
   * Crea una cartella chiamata `data` nella root del progetto (se non c'è già).
   * Scarica il file CSV originale da Drive e mettilo dentro `data/`.
   * **Fatto!** Quando eseguirai il *Notebook 1*, se il file `.parquet` non esiste, il notebook lo convertirà automaticamente per te in locale.

---

## Routine Quotidiana (Da fare OGNI GIORNO)

Segui rigorosamente questo ordine per non creare conflitti con il codice degli altri:

### 1. Attiva la bolla
Appena apri VS Code, controlla che nel terminale ci sia la scritta verde
 `(.venv)`. Se non c'è, attivala:
`.\.venv\Scripts\activate`
Assicurati che in basso a destra nella finestra di VS Code (o premendo Ctrl + Shift + P e cercando "Python: Select Interpreter") sia selezionato l'interprete con scritto ('.venv': venv)

### 2. Salva e Condividi (Commit & Push)
Quando hai finito, manda tutto su GitHub:
`git add .`
`git commit -m "Descrizione di quello che hai fatto"`
`git push origin nome-tua-feature`


## Come lavorare su Google Colab

Per l'esecuzione dei calcoli pesanti o per mostrare i risultati, usiamo Google Colab. Segui questi step:

### 1. Preparazione Drive (Solo una volta)
Prima di iniziare, devi "agganciare" la cartella del progetto al tuo Drive:
* Vai su Google Drive e trova la cartella condivisa **Mining_Premier_League**.
* Clicca con il tasto destro sulla cartella e scegli **"Aggiungi scorciatoia a Drive"** (Add shortcut to Drive).
* Senza questo passaggio, Colab non riuscirà a trovare i dati!

### 2. Il Ciclo di Sviluppo Ibrido
1. **Scrivi il codice** (le funzioni `.py`) su **VS Code** nel tuo PC.
2. **Fai il Push** su GitHub (vedi sezione Routine Quotidiana).
3. **Apri Colab** e apri il file `notebooks/ambiente_setup.ipynb`.
4. **Esegui la cella di Setup**: Questo monterà il Drive, clonerà il codice aggiornato da GitHub e installerà le librerie.
5. **Lavora**: Ora puoi importare le tue funzioni con `from src.data_loader import load_data` e usarle!

### 3. Sincronizzazione in tempo reale
In cima a ogni notebook su Colab, aggiungiamo sempre:
```python
%load_ext autoreload
%autoreload 2
```
Così, se modifichi un file `.py` su VS Code e fai push, ti basterà fare un `git pull` su Colab e le funzioni si aggiorneranno da sole senza dover riavviare tutto!

---

## Le 3 Regole d'Oro del Team

1. **I DATI NON VANNO SU GITHUB:** Non fare MAI commit di file `.csv` o `.parquet`. I dati stanno solo su Google Drive e in locale nella cartella `data/` (che è protetta dal `.gitignore`).
2. **I NOTEBOOK STANNO SU COLAB:** I file `.ipynb` servono solo per l'esecuzione finale. Aprite Colab, clonate il repo, caricate i dati da Drive e importate le funzioni da `src/`.
3. **PULL PRIMA DI INIZIARE:** Fai sempre `git pull` prima di iniziare a lavorare per evitare conflitti.