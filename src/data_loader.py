import os
import pandas as pd


def get_project_root():
    """
    Restituisce il percorso assoluto della cartella radice del progetto,
    indipendentemente da dove viene lanciato lo script.
    Funziona sia in locale che su Colab (dopo che la cella di setup
    ha eseguito os.chdir(REPO_NAME) portandoci nella root corretta).
    """
    # __file__ è src/data_loader.py → saliamo di un livello per arrivare alla root
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
    Nessun membro del team dovrà mai cambiare i path a mano.

    Su Colab: la cella di setup (Colab_setup.ipynb) scarica già i file
    in data/ prima che questo venga chiamato. os.chdir(REPO_NAME) garantisce
    che get_project_root() punti alla posizione corretta.

    In locale: legge da data/ relativa alla root del progetto.
    Se il parquet non esiste, lo genera automaticamente dal CSV originale.
    """
    project_root = get_project_root()
    data_dir = os.path.join(project_root, 'data')
    os.makedirs(data_dir, exist_ok=True)

    path = os.path.join(data_dir, file_name)
    csv_path = os.path.join(data_dir, '20-21_plEventsData.csv')

    # Se il parquet non esiste ancora, proviamo a crearlo dal CSV
    if not os.path.exists(path):
        if os.path.exists(csv_path):
            convert_csv_to_parquet(csv_path, path)
        else:
            raise FileNotFoundError(
                f"Errore: né '{file_name}' né il CSV originale trovati in {data_dir}.\n"
                f"Su Colab: assicurati di aver eseguito Colab_setup.ipynb.\n"
                f"In locale: metti il CSV in {data_dir}."
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
# HELPER INTERNI — gestione percorsi data/processed/
# ==============================================================================

def _get_processed_dir():
    """
    Restituisce il percorso alla cartella data/processed/.
    Funziona sia in locale che su Colab grazie a get_project_root().
    """
    project_root = get_project_root()
    return os.path.join(project_root, 'data', 'processed')


def _load_processed(file_name):
    """Carica un file Parquet dalla cartella data/processed/."""
    processed_dir = _get_processed_dir()
    path = os.path.join(processed_dir, file_name)
    if not os.path.exists(path):
        raise FileNotFoundError(
            f"File non trovato: {path}\n"
            f"Assicurati di aver eseguito il notebook precedente per generare '{file_name}'.\n"
            f"Su Colab: la cella di setup scarica questi file automaticamente da Drive."
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