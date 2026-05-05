import nbformat as nbf

notebook_path = r'c:\Users\Casa\Desktop\Mining_Premier_League\notebooks\Feature_extraction_EDA.ipynb'

with open(notebook_path, 'r', encoding='utf-8') as f:
    nb = nbf.read(f, as_version=4)

for cell in nb.cells:
    if cell.cell_type == 'code':
        # 1. Rimuovi def savefig(...) dalla cella 2
        if 'def savefig' in cell.source:
            lines = cell.source.split('\n')
            new_lines = []
            skip = False
            for line in lines:
                if 'def savefig' in line:
                    skip = True
                    continue
                if skip:
                    if line.startswith('    ') or line.strip() == '':
                        continue
                    else:
                        skip = False
                
                if not skip:
                    new_lines.append(line)
            cell.source = '\n'.join(new_lines)
            
        # 2. Sostituisci tutte le chiamate savefig(...) con plt.show()
        if 'savefig(' in cell.source:
            lines = cell.source.split('\n')
            new_lines = []
            for line in lines:
                if line.strip().startswith('savefig('):
                    # Mantieni l'indentazione originale, se c'è
                    indent = line[:len(line) - len(line.lstrip())]
                    new_lines.append(f"{indent}plt.show()")
                else:
                    new_lines.append(line)
            cell.source = '\n'.join(new_lines)

with open(notebook_path, 'w', encoding='utf-8') as f:
    nbf.write(nb, f)

print("[OK] Tutte le chiamate 'savefig' sono state rimosse e sostituite con plt.show().")
