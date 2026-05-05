import nbformat as nbf
import os

notebook_path = r'c:\Users\Casa\Desktop\Mining_Premier_League\notebooks\Feature_extraction_EDA.ipynb'

# Load the notebook
with open(notebook_path, 'r', encoding='utf-8') as f:
    nb = nbf.read(f, as_version=4)

# New source for Cell 6
cell_6_source = """# Creiamo il flag di successo prima del groupby per efficienza
if "outcomeType_displayName" in df_game.columns:
    df_game["is_successful"] = df_game["outcomeType_displayName"] == "Successful"

def extract_features(grp):
    \"\"\"
    Estrae le feature tattiche e spaziali per squadra-partita.
    Previene il Data Leakage ignorando i gol.
    \"\"\"
    total_events = len(grp)
    minutes_played = grp["minute"].clip(upper=120).max() - grp["minute"].clip(upper=120).min()
    minutes_played = max(minutes_played, 1)

    # Sub-dataframe
    passes = grp[grp["type_displayName"] == "Pass"]
    # FIX LEAKAGE: Un tiro è valido se isShot è True MA isGoal è False
    shots = grp[(grp.get("isShot", False) == True) & (grp.get("isGoal", False) == False)]
    goals = grp[grp["type_displayName"] == "Goal"]
    tackles = grp[grp["type_displayName"] == "Tackle"]
    fouls = grp[grp["type_displayName"] == "Foul"]
    corners = grp[grp["type_displayName"] == "CornerAwarded"]
    aerials = grp[grp["type_displayName"] == "Aerial"]
    clearances = grp[grp["type_displayName"] == "Clearance"]
    intercepts = grp[grp["type_displayName"] == "Interception"]
    takeons = grp[grp["type_displayName"] == "TakeOn"]
    recoveries = grp[grp["type_displayName"] == "BallRecovery"]
    
    ft = grp[grp["period_displayName"] == "FirstHalf"]

    def safe_rate(num, den):
        return num / den if den > 0 else 0.0

    # Coordinate Spaziali Sicure
    avg_x = grp["x"].mean()
    avg_y = grp["y"].mean()
    avg_pass_end_x = passes["endX"].mean() if "endX" in passes.columns else np.nan

    # Field Tilt
    offensive_third = grp[grp['x'] > 66.6]
    field_tilt = len(offensive_third) / total_events if total_events > 0 else 0.0

    # Gestione Cartellini
    n_yellow = grp[grp['cardType_displayName'] == 'Yellow'].shape[0]
    red_events = grp[grp['cardType_displayName'].isin(['Red', 'SecondYellow'])]
    n_red = red_events['playerId'].nunique() if 'playerId' in red_events.columns else red_events.shape[0]

    # --- FUNZIONI HELPER PER ESTRAZIONI SICURE ---
    def safe_sum(col_name):
        return grp[col_name].sum() if col_name in grp.columns else 0
        
    def safe_mean(col_name):
        return grp[col_name].mean() if col_name in grp.columns else np.nan
    # ---------------------------------------------

    return pd.Series({
        # 1. Metriche Volume Base
        "n_passes": len(passes),
        "n_shots_no_goal": len(shots),
        "n_tackles": len(tackles),
        "n_fouls": len(fouls),
        "n_corners": len(corners),
        "n_aerials": len(aerials),
        "n_clearances": len(clearances),
        "n_interceptions": len(intercepts),
        "n_takeons": len(takeons),
        "n_ball_recoveries": len(recoveries),
        "events_per_minute": total_events / minutes_played,
        "first_half_ratio":  safe_rate(len(ft), total_events),
        
        # 2. Metriche Tattiche Avanzate (dai Qualifiers)
        "n_longballs": safe_sum('is_longball'),
        "n_crosses": safe_sum('is_cross'),
        "n_throughballs": safe_sum('is_throughball'),
        "n_keypasses": safe_sum('is_keypass'),
        "n_fastbreaks": safe_sum('is_fastbreak'),
        
        # Somme sicure aggregate
        "n_big_chances": safe_sum('is_bigchance') + safe_sum('is_bigchancecreated'),
        "n_blocks": safe_sum('is_blocked') + safe_sum('is_outfielderblock') + safe_sum('is_sixyardblock'),
        
        # 3. Metriche Spaziali e Dominio Territoriale
        "avg_x": avg_x,
        "avg_y": avg_y,
        "avg_pass_end_x": avg_pass_end_x,
        "field_tilt": field_tilt,
        "n_passes_offensive_third": len(offensive_third[offensive_third['type_displayName'] == 'Pass']),
        "avg_pass_length": safe_mean('pass_length'),
        "avg_goal_mouth_z": safe_mean('goal_mouth_z'),
        "set_piece_ratio": safe_rate((safe_sum('is_fromcorner') + safe_sum('is_setpiece')), len(shots)),
        
        # 4. Disciplina
        "n_yellow_cards": n_yellow,
        "n_red_cards": n_red,
        
        # 5. Ratei di Efficienza
        "pass_success_rate": safe_rate(passes["is_successful"].sum(), len(passes)) if "is_successful" in passes.columns else np.nan,
        "tackle_success_rate": safe_rate(tackles["is_successful"].sum(), len(tackles)) if "is_successful" in tackles.columns else np.nan,
        "aerial_success_rate": safe_rate(aerials["is_successful"].sum(), len(aerials)) if "is_successful" in aerials.columns else np.nan,
        "takeon_success_rate": safe_rate(takeons["is_successful"].sum(), len(takeons)) if "is_successful" in takeons.columns else np.nan,
    })

print("Funzione 'extract_features' definita con successo. Pronta per il groupby!")"""

# New source for Cell 7
cell_7_source = """import time

print("Avvio aggregazione feature tattiche. Attendere...")
start_time = time.time()

# Esecuzione dell'aggregazione (con i FIX per Pandas)
features_raw = (
    df_game.groupby(["match_id", "teamId"], group_keys=False)
    .apply(extract_features, include_groups=False)
    .reset_index()
)

# Uniamo il dataset con il target (esito e gol)
features = features_raw.merge(
    opp[["match_id", "teamId", "goals_scored", "goals_conceded", "outcome"]],
    on=["match_id", "teamId"],
    how="inner"
)

# Sicurezza finale per il ML: sostituiamo eventuali NaN con 0
features = features.fillna(0)

end_time = time.time()
print(f"Aggregazione completata in {end_time - start_time:.2f} secondi.")
print(f"Dimensioni dataset Gold: {features.shape[0]} righe × {features.shape[1]} colonne (Attesi: 760 righe)")

# Definiamo rigorosamente le feature 
FEATURE_COLS = [c for c in features.columns 
                if c not in ["match_id", "teamId", "goals_scored", 
                             "goals_conceded", "outcome"]]

print(f"\\nColonne feature pronte per l'EDA e il ML: {len(FEATURE_COLS)}")
print(\"\\nAnteprima delle nuove metriche estratte:\")
print(features[['teamId', 'n_passes', 'n_longballs', 'n_big_chances', 'n_fastbreaks', 'pass_success_rate', 'outcome']].head())"""

# New source for Cell 9
cell_9_source = """OUTCOME_ORDER = ["Win", "Draw", "Loss"]
PALETTE = {"Win": "#10B981", "Draw": "#F59E0B", "Loss": "#EF4444"}

# ESCLUSIONE DATA LEAKAGE: Rimuoviamo n_goals e conversion rate prima del test
eda_cols = [c for c in FEATURE_COLS if c not in ['n_goals', 'shot_conversion_rate']]

class_means = features.groupby("outcome")[eda_cols].mean()
global_std  = features[eda_cols].std()

print("--- Media per classe (Win / Draw / Loss) ---")
# Stampiamo solo alcune colonne per brevità
print(class_means[['n_passes', 'n_big_chances', 'n_keypasses', 'avg_x']].round(2).T.to_string())

diff_win_loss = (class_means.loc["Win"] - class_means.loc["Loss"]).abs()
significant   = diff_win_loss[diff_win_loss > global_std]

print("\\n--- Analisi significatività (> 1sigma) TATTICA ---")
for feat in diff_win_loss.sort_values(ascending=False).index:
    w  = class_means.loc["Win",  feat]
    d  = class_means.loc["Draw", feat]
    l  = class_means.loc["Loss", feat]
    sd = global_std[feat]
    marker = "[SÌ]" if feat in significant.index else "[NO]"
    
    # Stampiamo le prime 15 per evitare log infiniti
    if diff_win_loss.sort_values(ascending=False).index.get_loc(feat) < 15:
        print(f"{marker} {feat:<26} Win={w:.2f}  Draw={d:.2f}  Loss={l:.2f}  "
              f"|diff|={diff_win_loss[feat]:.2f}  sigma={sd:.2f}  -> {diff_win_loss[feat]/sd:.1f}sigma")"""

# Update cells
nb.cells[6].source = cell_6_source
nb.cells[7].source = cell_7_source
nb.cells[9].source = cell_9_source

# Save back
with open(notebook_path, 'w', encoding='utf-8') as f:
    nbf.write(nb, f)

print("Notebook updated successfully.")
