"""
update_notebooks.py
Aggiorna le celle di setup di tutti i notebook Colab in modo idempotente.

Logica per notebook:
  - Data_Cleaning       → scarica solo Bronze  (genera Silver)
  - Feature_extraction  → scarica solo Silver come fallback  (genera Gold)
  - Machine_Learning    → scarica solo Gold come fallback
  - Full_Pipeline       → scarica solo Bronze  (genera tutto in sequenza)
  - Colab_setup         → scarica tutti i file (notebook panoramico)
"""

import json
from pathlib import Path

NOTEBOOKS_DIR = Path(__file__).parent / "notebooks"

# ---------------------------------------------------------------------------
# Blocco locale (identico per tutti)
# ---------------------------------------------------------------------------
LOCAL_BLOCK = """\
else:
    # In locale: risale le cartelle fino a trovare la root (quella con src/)
    import os, sys
    from pathlib import Path
    root = Path.cwd()
    while not (root / "src").exists() and root.parent != root:
        root = root.parent
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))
    os.chdir(root)
    print(f"Ambiente locale. Root progetto: {root}")\
"""

# ---------------------------------------------------------------------------
# Header Colab comune (clone + install)
# ---------------------------------------------------------------------------
COLAB_HEADER = """\
try:
    import google.colab
    IN_COLAB = True
except ImportError:
    IN_COLAB = False

if IN_COLAB:
    import os, sys
    from pathlib import Path

    REPO_NAME = "Mining_Premier_League"
    REPO_URL  = "https://github.com/Frestka/Mining_Premier_League.git"

    # Torna sempre a /content — evita la matrioska se la cella viene rieseguita
    os.chdir("/content")

    # Clona solo se non esiste già
    if not os.path.exists(REPO_NAME):
        !git clone -q {REPO_URL}
        print("Repository clonato.")

    # Entra nella cartella del progetto
    os.chdir(REPO_NAME)
    sys.path.insert(0, os.path.abspath("."))

    # Aggiorna solo src/ — niente conflitti sui notebook
    !git fetch -q origin
    !git checkout -q origin/main -- src/

    # Installa dipendenze
    !pip install -q -r requirements.txt

    # Crea cartelle dati
    Path("data/processed").mkdir(parents=True, exist_ok=True)

    import gdown
"""

# ---------------------------------------------------------------------------
# Blocchi di download specifici per notebook
# ---------------------------------------------------------------------------
DOWNLOAD_ONLY_BRONZE = """\
    # Questo notebook usa solo il Bronze come input e genera il Silver.
    FILES = {
        "data/dataset.parquet": "ID_DRIVE_BRONZE",   # ~37 MB
    }
    for path, file_id in FILES.items():
        if not os.path.exists(path):
            print(f"Download {path}...")
            gdown.download(id=file_id, output=path, quiet=False, fuzzy=True)
        else:
            print(f"Già presente, skip → {path}")

    print(f"\\n✅ Setup completato. Cartella: {os.getcwd()}")\
"""

DOWNLOAD_SILVER_FALLBACK = """\
    # Questo notebook legge il Silver (generato dal NB1) e produce il Gold.
    # Se il Silver non esiste (NB1 non eseguito), lo scarica da Drive come fallback.
    FILES = {
        "data/processed/dataset_clean.parquet": "ID_DRIVE_SILVER",  # ~16 MB
    }
    for path, file_id in FILES.items():
        if not os.path.exists(path):
            print(f"Download fallback {path}...")
            gdown.download(id=file_id, output=path, quiet=False, fuzzy=True)
        else:
            print(f"Già presente, skip → {path}")

    print(f"\\n✅ Setup completato. Cartella: {os.getcwd()}")\
"""

DOWNLOAD_GOLD_FALLBACK = """\
    # Questo notebook legge il Gold (generato dal NB2) e addestra i modelli.
    # Se il Gold non esiste (NB2 non eseguito), lo scarica da Drive come fallback.
    FILES = {
        "data/processed/features.parquet": "ID_DRIVE_GOLD",  # ~117 KB
    }
    for path, file_id in FILES.items():
        if not os.path.exists(path):
            print(f"Download fallback {path}...")
            gdown.download(id=file_id, output=path, quiet=False, fuzzy=True)
        else:
            print(f"Già presente, skip → {path}")

    print(f"\\n✅ Setup completato. Cartella: {os.getcwd()}")\
"""

DOWNLOAD_ALL = """\
    # Scarica tutti i livelli dati (Bronze, Silver, Gold).
    FILES = {
        "data/dataset.parquet":                 "ID_DRIVE_BRONZE",  # ~37 MB
        "data/processed/dataset_clean.parquet": "ID_DRIVE_SILVER",  # ~16 MB
        "data/processed/features.parquet":      "ID_DRIVE_GOLD",    # ~117 KB
    }
    for path, file_id in FILES.items():
        if not os.path.exists(path):
            print(f"Download {path}...")
            gdown.download(id=file_id, output=path, quiet=False, fuzzy=True)
        else:
            print(f"Già presente, skip → {path}")

    print(f"\\n✅ Setup completato. Cartella: {os.getcwd()}")\
"""

# ---------------------------------------------------------------------------
# Mappa notebook → blocco di download
# ---------------------------------------------------------------------------
NOTEBOOK_CONFIG = {
    "Data_Cleaning_and_Understanding.ipynb": DOWNLOAD_ONLY_BRONZE,
    "Feature_extraction_EDA.ipynb":          DOWNLOAD_SILVER_FALLBACK,
    "Machine_Learning_Modeling.ipynb":        DOWNLOAD_GOLD_FALLBACK,
    "Full_Pipeline_Trigger.ipynb":            DOWNLOAD_ONLY_BRONZE,
    "Colab_setup.ipynb":                      DOWNLOAD_ALL,
}

# ---------------------------------------------------------------------------
# Funzione che costruisce il codice della cella di setup
# ---------------------------------------------------------------------------
def build_setup_source(download_block: str) -> str:
    return COLAB_HEADER + "\n" + download_block + "\n\n" + LOCAL_BLOCK


def source_to_lines(source: str) -> list:
    """Converte stringa sorgente in lista di righe con \\n (formato Jupyter)."""
    lines = source.split("\n")
    return [line + "\n" for line in lines[:-1]] + ([lines[-1]] if lines[-1] else [])


def is_setup_cell(cell: dict) -> bool:
    """Riconosce la cella di setup cercando il pattern distintivo."""
    src = "".join(cell.get("source", []))
    return (
        "import google.colab" in src
        and "IN_COLAB" in src
        and cell.get("cell_type") == "code"
    )


def update_notebook(nb_path: Path, download_block: str) -> bool:
    with open(nb_path, "r", encoding="utf-8") as f:
        nb = json.load(f)

    new_source = build_setup_source(download_block)
    new_lines  = source_to_lines(new_source)

    updated = False
    for cell in nb["cells"]:
        if is_setup_cell(cell):
            if cell["source"] != new_lines:
                cell["source"] = new_lines
                updated = True
            break
    else:
        # Cella non trovata → inserisci come seconda cella (dopo il badge Colab)
        new_cell = {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": new_lines,
        }
        nb["cells"].insert(1, new_cell)
        updated = True

    if updated:
        with open(nb_path, "w", encoding="utf-8") as f:
            json.dump(nb, f, ensure_ascii=False, indent=1)
        print(f"  ✅ Aggiornato: {nb_path.name}")
    else:
        print(f"  ⏭  Già aggiornato: {nb_path.name}")

    return updated


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("=== Aggiornamento celle di setup nei notebook ===\n")
    any_updated = False
    for nb_name, dl_block in NOTEBOOK_CONFIG.items():
        nb_path = NOTEBOOKS_DIR / nb_name
        if not nb_path.exists():
            print(f"  ⚠️  Non trovato: {nb_name}")
            continue
        changed = update_notebook(nb_path, dl_block)
        any_updated = any_updated or changed

    print("\n" + ("✅ Tutti i notebook aggiornati." if any_updated else "⏭  Nessuna modifica necessaria."))
