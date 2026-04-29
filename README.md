# ⚽ Progetto Data Mining - Premier League
VS Code ↔ GitHub ↔ Google Colab

## 🛠️ Setup Iniziale (Da fare SOLO la prima volta)

Se è la prima volta che scarichi questo progetto sul tuo PC, segui questi step:

1. Crea una catella locale chiamata "Mining_Premier_League"

2. **Clona il repository:**
   `https://github.com/Frestka/Mining_Premier_League.git`
3. **Apri la cartella su VS Code.**
4. **Crea l'ambiente virtuale (la "bolla"):**
   `python -m venv .venv`
5. **Attiva la bolla:**
   `.\.venv\Scripts\activate`
   *⚠️ Attenzione all'errore tipico di Windows: > Se ricevi un testo rosso pieno di errori che dice qualcosa come "L'esecuzione di script è disabilitata in questo sistema", è colpa della sicurezza di Windows PowerShell.
   La soluzione: Apri PowerShell su Windows come Amministratore (fuori da VS Code), digita Set-ExecutionPolicy RemoteSigned, premi Invio, scrivi S (Sì) e riprova.(Se ti dà errore di permessi su Windows, apri PowerShell come amministratore e lancia `Set-ExecutionPolicy RemoteSigned -Scope CurrentUser`, poi riprova).*
6. **Installa le librerie fisse:**
   `pip install -r requirements.txt`
7. **Scarica il dataset:**:
   * Crea una cartella chiamata data nella root del progetto.
   * Scarica il file CSV da Drive e mettilo dentro data/.
   * Lancia il comando: python src/data_loader.py per generare il file .parquet

---

## ☀️ Routine Quotidiana (Da fare OGNI GIORNO)

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


---

lavoro su colab:
Apri Google Colab.
crea i notebbok su vs cose e Li salvi con git commit come tutti gli altri file.
Carica il tuo notebook Jupyter (es. analisi.ipynb).


Quando sei su Colab Per portarci dentro il tuo lavoro, segui questi 3 step in una cella di codice in alto al notebook
Nelle prime celle, importi le funzioni da src/ (che di solito sono già sincronizzate su Drive o le hai salvate lì).

Esegui le analisi usando i dati che hai caricato su Drive.  





## ⚠️ Le 3 Regole d'Oro del Team

1. **I DATI NON VANNO SU GITHUB:** Non fare MAI commit di file `.csv` o `.parquet`. I dati stanno solo su Google Drive e in locale nella cartella `data/` (che è protetta dal `.gitignore`).
2. **I NOTEBOOK STANNO SU COLAB:** I file `.ipynb` servono solo per l'esecuzione finale. Aprite Colab, clonate il repo, caricate i dati da Drive e importate le funzioni da `src/`.
3. **PULL PRIMA DI INIZIARE:** Fai sempre `git pull` prima di iniziare a lavorare per evitare conflitti.