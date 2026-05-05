import nbformat as nbf
import os

notebook_path = r'c:\Users\Casa\Desktop\Mining_Premier_League\notebooks\Feature_extraction_EDA.ipynb'

# Load the notebook
with open(notebook_path, 'r', encoding='utf-8') as f:
    nb = nbf.read(f, as_version=4)

# Update Cell 2 (index 2)
new_source = """import sys, os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
from pathlib import Path

warnings.filterwarnings('ignore')

# Caricamento tramite data_loader (environment-agnostic: funziona su VS Code e Colab)
sys.path.append(os.path.abspath('..'))
from src.data_loader import load_clean_data, save_features

sns.set_theme(style='whitegrid', palette='tab10')

def savefig(name):
    plt.show()
    plt.close()

# Carica il Silver Layer prodotto dal Notebook 1
df = load_clean_data()
print(f'Dataset caricato: {df.shape[0]:,} righe x {df.shape[1]} colonne')
print(f'Memoria: {df.memory_usage(deep=True).sum() / 1e6:.1f} MB')

# Verifica che il match_id sia gia presente (prodotto dal Notebook 1)
assert 'match_id' in df.columns, 'ERRORE: match_id non trovato! Riesegui il Notebook 1.'

# Gli id duplicati sono eventi OffsideGiven registrati specularmente -- comportamento atteso Opta.
duplicati_id = df['id'].duplicated().sum()
print(f'Righe con id duplicato: {duplicati_id} (OffsideGiven speculari, mantenuti)')"""

nb.cells[2].source = new_source

# Save back
with open(notebook_path, 'w', encoding='utf-8') as f:
    nbf.write(nb, f)

print("Notebook 2 setup cell updated successfully to not save plots.")
