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

def load_data(file_name="dataset.parquet"):
    """
    Carica i dati in modo dinamico tra Locale e Colab.
    Nessun membro del team dovrà mai cambiare i path a mano.
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
    
    # 2. Se siamo in locale (Sui vostri 3 PC, da VS Code)
    else:
        # Calcolo il percorso della cartella data/ dinamicamente dalla radice
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
                raise FileNotFoundError(f"Errore: Né il file {file_name} né il CSV di partenza sono stati trovati in {local_data_dir}.\nAssicurati di aver scaricato il CSV da Drive e averlo messo in quella cartella!")

    print(f"Caricamento dati da: {path}")
    return pd.read_parquet(path)

# Se eseguiamo direttamente questo script (es. premendo Play in VS Code), 
# parte in automatico il caricamento/conversione!
if __name__ == "__main__":
    print("Avvio data_loader.py in modalità standalone...")
    df = load_data()
    print(f"Dataset caricato con successo! Dimensioni: {df.shape}")
    print(df.head())