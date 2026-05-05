import nbformat as nbf

notebook_path = r'c:\Users\Casa\Desktop\Mining_Premier_League\notebooks\Data_Cleaning_and_Understanding.ipynb'

with open(notebook_path, 'r', encoding='utf-8') as f:
    nb = nbf.read(f, as_version=4)

# Verifica che la cella 11 sia quella giusta
cell = nb.cells[11]
assert cell.cell_type == 'code', f"Cella 11 non è una cella di codice! È: {cell.cell_type}"
assert 'Rimozione colonne opache' in cell.source, f"Cella 11 non contiene il testo atteso! Preview: {cell.source[:120]!r}"

print(f"[OK] Trovata cella di cleaning all'indice 11.")
print(f"     Preview attuale: {cell.source[:80]!r}")

# Nuova sorgente con l'estrazione dei qualifiers
new_source = """\
import ast

print(f"Dimensioni prima del cleaning: {df.shape[0]:,} righe × {df.shape[1]} colonne")

# 1. Duplicati su id — rilevazione e mantenimento consapevole
n_duplicati = df['id'].duplicated().sum()
print(f"\\nRighe con 'id' duplicato: {n_duplicati} → MANTENUTE (OffsideGiven speculari, comportamento atteso Opta)")

# --- ESTRAZIONE FEATURE DAI QUALIFIERS (Prima del drop) ---
# Nota metodologica: estraiamo solo attributi tattici ad alta frequenza e significato chiaro.
# La colonna 'qualifiers' viene rimossa subito dopo per evitare bias interpretativi.
print("\\nEstrazione attributi tattici dai qualifiers...")

def parse_qualifiers(q_str):
    try:
        return {d['type']['displayName']: d.get('value', True) for d in ast.literal_eval(q_str)}
    except:
        return {}

# Creiamo dizionario temporaneo (solo dove qualifiers non è nullo)
df['q_dict'] = df['qualifiers'].apply(parse_qualifiers)

# Feature booleane tattiche
df['is_longball']        = df['q_dict'].apply(lambda x: 'Longball' in x)
df['is_cross']           = df['q_dict'].apply(lambda x: 'Cross' in x)
df['is_throughball']     = df['q_dict'].apply(lambda x: 'Throughball' in x)
df['is_keypass']         = df['q_dict'].apply(lambda x: 'KeyPass' in x)
df['is_fastbreak']       = df['q_dict'].apply(lambda x: 'FastBreak' in x)
df['is_bigchance']       = df['q_dict'].apply(lambda x: 'BigChance' in x)
df['is_bigchancecreated']= df['q_dict'].apply(lambda x: 'BigChanceCreated' in x)
df['is_blocked']         = df['q_dict'].apply(lambda x: 'Blocked' in x)
df['is_outfielderblock'] = df['q_dict'].apply(lambda x: 'OutfielderBlock' in x)
df['is_sixyardblock']    = df['q_dict'].apply(lambda x: 'SixYardBlock' in x)
df['is_fromcorner']      = df['q_dict'].apply(lambda x: 'FromCorner' in x)
df['is_setpiece']        = df['q_dict'].apply(lambda x: 'SetPiece' in x)

# Lunghezza del passaggio (distanza euclidea sul campo 0-100)
df['pass_length'] = ((df['endX'] - df['x'])**2 + (df['endY'] - df['y'])**2)**0.5

# Rimuoviamo il dizionario temporaneo
df = df.drop(columns=['q_dict'])

n_qualifier_cols = 13  # 12 bool + pass_length
print(f"Colonne tattiche create dai qualifiers: {n_qualifier_cols}")

# 2. Rimozione colonne opache (qualifiers e satisfiedEventsTypes)
colonne_da_scartare = ['qualifiers', 'satisfiedEventsTypes']
df_clean = df.drop(columns=[c for c in colonne_da_scartare if c in df.columns])
print(f"Colonne rimosse: {colonne_da_scartare}")

# 3. Filtro fasi di gioco (esclude PreMatch=16 e PostGame=14)
n_before = len(df_clean)
df_clean = df_clean[df_clean['period_value'].isin([1, 2, 3, 4, 5])]
print(f"\\nEventi pre/post-match rimossi: {n_before - len(df_clean):,}")

# 4. Rimozione sentinella minute == 32767
n_before = len(df_clean)
df_clean = df_clean[df_clean['minute'] != 32767]
print(f"Righe con minute=32767 rimosse: {n_before - len(df_clean):,}")

# 5. Casting booleani
# NOTA: isShot/isGoal/isOwnGoal contengono solo NaN o la stringa 'True' (mai 'False').
bool_cols_native = ['isShot', 'isGoal', 'isOwnGoal']
bool_cols_qualifier = [
    'is_longball', 'is_cross', 'is_throughball', 'is_keypass', 'is_fastbreak',
    'is_bigchance', 'is_bigchancecreated', 'is_blocked', 'is_outfielderblock',
    'is_sixyardblock', 'is_fromcorner', 'is_setpiece'
]
for col in bool_cols_native:
    if col in df_clean.columns:
        df_clean[col] = df_clean[col].fillna(False).astype(bool)
for col in bool_cols_qualifier:
    if col in df_clean.columns:
        df_clean[col] = df_clean[col].astype(bool)
print(f"\\nCasting booleani applicato.")

# 6. shirtNo da float a int
if 'shirtNo' in df_clean.columns:
    df_clean['shirtNo'] = df_clean['shirtNo'].fillna(-1).astype(int)
    print("shirtNo convertito da float a int (NaN → -1)")

print(f"\\nDimensioni dopo il cleaning: {df_clean.shape[0]:,} righe × {df_clean.shape[1]} colonne")
print(f"Righe totali rimosse: {len(df) - len(df_clean):,}")
"""

nb.cells[11].source = new_source

with open(notebook_path, 'w', encoding='utf-8') as f:
    nbf.write(nb, f)

print("[OK] Notebook 1 aggiornato correttamente con le nuove colonne qualifiers.")
