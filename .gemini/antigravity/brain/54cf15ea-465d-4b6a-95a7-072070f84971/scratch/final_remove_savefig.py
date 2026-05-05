import nbformat as nbf
import os

notebook_path = r'c:\Users\Casa\Desktop\Mining_Premier_League\notebooks\Feature_extraction_EDA.ipynb'

with open(notebook_path, 'r', encoding='utf-8') as f:
    nb = nbf.read(f, as_version=4)

# Troviamo e aggiorniamo la cella di setup
for cell in nb.cells:
    if cell.cell_type == 'code' and 'def savefig' in cell.source:
        # Sostituiamo la logica di salvataggio
        lines = cell.source.split('\n')
        new_lines = []
        skip = False
        for line in lines:
            if 'OUT_DIR = Path(' in line or 'OUT_DIR.mkdir(' in line:
                continue  # Rimuove la creazione della cartella
            
            if 'def savefig(' in line:
                new_lines.append(line)
                new_lines.append("    plt.show()")
                new_lines.append("    plt.close()")
                skip = True
                continue
                
            if skip:
                if line.startswith('    ') or line.strip() == '':
                    continue # Salta il corpo originale della funzione
                else:
                    skip = False
            
            if not skip:
                new_lines.append(line)
                
        cell.source = '\n'.join(new_lines)
        break

with open(notebook_path, 'w', encoding='utf-8') as f:
    nbf.write(nb, f)

print("[OK] Notebook 2 pulito dal salvataggio immagini.")
