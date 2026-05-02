import json
from pathlib import Path

file_path = r"c:\Users\Casa\Desktop\Mining_Premier_League\notebooks\feature_extraction_EDA (1).ipynb"

with open(file_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

for cell in nb['cells']:
    # 1. Update FILE_PATH
    if cell['cell_type'] == 'code':
        source = cell['source']
        for i, line in enumerate(source):
            if 'FILE_PATH =' in line and 'dataset.parquet' in line:
                source[i] = 'FILE_PATH = Path("../data/processed/dataset_clean.parquet")\n'

    # 2. Update Markdown Cell
    if cell['cell_type'] == 'markdown':
        source = cell['source']
        if len(source) > 0 and 'Costruzione del `match_id`' in source[0]:
            cell['source'] = [
                "## 1. Derivazione del Target (Win, Draw, Loss)\n",
                "\n",
                "Avendo già a disposizione il `match_id` e un dataset pulito (dal Notebook 1), procediamo al calcolo dei gol segnati e subiti da ciascuna squadra.\n",
                "\n",
                "Utilizziamo `transform('sum')` — operazione vettorializzata che evita `apply` lenti — per conteggiare i gol totali della partita, e deriviamo per differenza i gol subiti e il target testuale **Win / Draw / Loss** per ogni squadra."
            ]

    # 3. Update Code Cell for Match ID
    if cell['cell_type'] == 'code':
        source = cell['source']
        if len(source) > 0 and 'df = df.sort_index()' in source[0]:
            new_source = [
                "# Il dataset è già pulito e contiene solo eventi di gioco e il match_id.\\n\n",
                "df_game = df.copy()\n",
                "n_matches = df_game[\"match_id\"].nunique()\n",
                "print(f\"Partite identificate: {n_matches}  (attese: 380 per PL 2020-21)\\n\")\n",
                "\n"
            ]
            start_idx = 0
            for i, line in enumerate(source):
                if '# Gol per squadra per match' in line:
                    start_idx = i
                    break
            cell['source'] = new_source + source[start_idx:]

with open(file_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print("Notebook 2 aggiornato con successo.")
