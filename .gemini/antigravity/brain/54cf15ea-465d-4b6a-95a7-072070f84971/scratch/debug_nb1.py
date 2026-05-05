import nbformat as nbf

notebook_path = r'c:\Users\Casa\Desktop\Mining_Premier_League\notebooks\Data_Cleaning_and_Understanding.ipynb'

with open(notebook_path, 'r', encoding='utf-8') as f:
    nb = nbf.read(f, as_version=4)

# DEBUG: mostriamo indici e testi delle celle codice
for i, cell in enumerate(nb.cells):
    if cell.cell_type == 'code':
        preview = cell.source[:80].replace('\n', ' ')
        print(f"  [cell #{i}] source preview: {preview!r}")
