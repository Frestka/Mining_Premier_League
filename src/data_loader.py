import os
import pandas as pd


def get_project_root():
    """
    Restituisce il percorso assoluto della cartella radice del progetto,
    indipendentemente da dove viene lanciato lo script.
    (es: calcola dinamicamente 'c:\\Users\\Nome\\...\\Mining_Premier_League')
    """
    # __file__ è src/data_loader.py, quindi saliamo di un livello (..) per arrivare alla root
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))


def convert_csv_to_parquet(csv_path, parquet_path):
    """
    Converte il CSV originale in Parquet per ottimizzare spazio e velocità.
    """
    print(f"Conversione in corso: {csv_path} --> {parquet_path}")
    df = pd.read_csv(csv_path)
    df.to_parquet(parquet_path, engine='pyarrow', compression='snappy')
    print("Conversione completata!")


# ==============================================================================
# LIVELLO BRONZE — dataset.parquet (dato grezzo originale)
# ==============================================================================

def load_data(file_name="dataset.parquet"):
    """
    Carica i dati Bronze (grezzi) in modo dinamico tra Locale e Colab.
    Nessun membro del team dovra mai cambiare i path a mano.
    """
    # 1. Controllo se siamo su Colab (l'ambiente Cloud)
    if 'google.colab' in str(get_ipython.__class__) if 'get_ipython' in globals() else os.path.exists('/content'):
        try:
            from google.colab import drive
            if not os.path.exists('/content/drive'):
                drive.mount('/content/drive')
        except ImportError:
            pass

        # PERCORSO DRIVE CONDIVISO:
        # Trovate un accordo su come chiamare la cartella condivisa su Drive
        # e assicuratevi di aver creato il collegamento in "Il mio Drive".
        path = f'/content/drive/MyDrive/Mining_Premier_League/data/{file_name}'

    # 2. Se siamo in locale (sui vostri PC, da VS Code)
    else:
        project_root = get_project_root()
        local_data_dir = os.path.join(project_root, 'data')

        # Creo la cartella data se per sbaglio non esiste
        os.makedirs(local_data_dir, exist_ok=True)

        path = os.path.join(local_data_dir, file_name)
        csv_path = os.path.join(local_data_dir, '20-21_plEventsData.csv')

        # Se il parquet non esiste ancora in locale, lo creo dal CSV in automatico
        if not os.path.exists(path):
            if os.path.exists(csv_path):
                convert_csv_to_parquet(csv_path, path)
            else:
                raise FileNotFoundError(
                    f"Errore: Ne il file {file_name} ne il CSV di partenza sono stati trovati in {local_data_dir}.\n"
                    f"Assicurati di aver scaricato il CSV da Drive e averlo messo in quella cartella!"
                )

    print(f"Caricamento dati da: {path}")
    return pd.read_parquet(path)


# ==============================================================================
# LIVELLO SILVER — dataset_clean.parquet (prodotto dal Notebook 1)
# ==============================================================================

def load_clean_data():
    """
    Carica il dataset Silver (pulito) prodotto dal Notebook 1.
    Funziona sia in locale che su Colab senza modifiche.
    """
    return _load_processed('dataset_clean.parquet')


def save_clean_data(df):
    """
    Salva il DataFrame come Silver Layer (dataset_clean.parquet).
    Crea la cartella data/processed/ se non esiste.
    """
    _save_processed(df, 'dataset_clean.parquet')


# ==============================================================================
# LIVELLO GOLD — features.parquet (prodotto dal Notebook 2)
# ==============================================================================

def load_features():
    """
    Carica il dataset Gold (feature aggregate per partita) prodotto dal Notebook 2.
    Funziona sia in locale che su Colab senza modifiche.
    """
    return _load_processed('features.parquet')


def save_features(df):
    """
    Salva il DataFrame come Gold Layer (features.parquet).
    Crea la cartella data/processed/ se non esiste.
    """
    _save_processed(df, 'features.parquet')


# ==============================================================================
# HELPER INTERNI — gestione percorsi processed/
# ==============================================================================

def _get_processed_dir():
    """
    Restituisce il percorso alla cartella data/processed/
    corretta per l'ambiente (locale o Colab).
    """
    is_colab = (
        ('google.colab' in str(get_ipython.__class__) if 'get_ipython' in globals() else False)
        or os.path.exists('/content')
    )
    if is_colab:
        return '/content/drive/MyDrive/Mining_Premier_League/data/processed'
    else:
        project_root = get_project_root()
        return os.path.join(project_root, 'data', 'processed')


def _load_processed(file_name):
    """Carica un file Parquet dalla cartella data/processed/."""
    processed_dir = _get_processed_dir()
    path = os.path.join(processed_dir, file_name)
    if not os.path.exists(path):
        raise FileNotFoundError(
            f"File non trovato: {path}\n"
            f"Assicurati di aver eseguito il notebook precedente per generare '{file_name}'."
        )
    print(f"Caricamento dati da: {path}")
    return pd.read_parquet(path)


def _save_processed(df, file_name):
    """Salva un DataFrame come Parquet nella cartella data/processed/."""
    processed_dir = _get_processed_dir()
    os.makedirs(processed_dir, exist_ok=True)
    path = os.path.join(processed_dir, file_name)
    df.to_parquet(path, engine='pyarrow', compression='snappy')
    print(f"Salvato: {path}")
    print(f"  {df.shape[0]:,} righe x {df.shape[1]} colonne")


# ==============================================================================
# ENTRY POINT — test rapido da riga di comando
# ==============================================================================

if __name__ == "__main__":
    print("Avvio data_loader.py in modalita standalone...")
    df = load_data()
    print(f"[Bronze] Dataset caricato con successo! Dimensioni: {df.shape}")