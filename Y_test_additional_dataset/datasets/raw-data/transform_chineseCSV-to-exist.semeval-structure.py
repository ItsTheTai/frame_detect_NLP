import pandas as pd

# 1. Dateien einlesen
csv_file = 'chinese_news_framing_dataset Kopie.csv'
gt_template_file = 'ground_truth_full.xlsx'

df_csv = pd.read_csv(csv_file)
df_gt_template = pd.read_excel(gt_template_file)

# Exakte Spaltenreihenfolge aus der Ground-Truth-Vorlage übernehmen
target_columns = df_gt_template.columns.tolist()

# 2. Mapping von den CSV-Frame-Bezeichnungen auf die Excel-Spaltennamen
tag_mapping = {
    'Economic': 'Economic',
    'Capacity_and_resources': 'Capacity and resources',
    'Morality': 'Morality',
    'Fairness_and_equality': 'Fairness and equality',
    'Legality_Constitutionality_and_jurisprudence': 'Legality, constitutionality and jurisprudence',
    'Policy_prescription_and_evaluation': 'Policy prescription and evaluation',
    'Crime_and_punishment': 'Crime and punishment',
    'Security_and_defense': 'Security and defense',
    'Health_and_safety': 'Health and safety',
    'Quality_of_life': 'Quality of life',
    'Cultural_identity': 'Cultural identity',
    'Public_opinion': 'Public opinion',
    'Political': 'Political',
    'External_regulation_and_reputation': 'External regulation and reputation'
}

# 3. Ziel-DataFrame aufbauen
df_out = pd.DataFrame()
df_out['Filename'] = df_csv['web_link']
df_out['Language'] = 'chinese'

# Frame-Spalten mit 0 initialisieren
frame_columns = [col for col in target_columns if col not in ['Filename', 'Language']]
for col in frame_columns:
    df_out[col] = 0

# 4. Binäre Flags (0 / 1) basierend auf der Spalte 'frames' setzen
for idx, row in df_csv.iterrows():
    if pd.notna(row['frames']):
        # Kommasortierte Strings aufspalten
        active_tags = [tag.strip() for tag in str(row['frames']).split(',')]
        for tag in active_tags:
            if tag in tag_mapping:
                col_name = tag_mapping[tag]
                df_out.loc[idx, col_name] = 1

# 5. Spaltenreihenfolge an Ground Truth angleichen und als Excel speichern
df_out = df_out[target_columns]
output_file = 'ground_truth_chinese_extension_semeval.xlsx'
df_out.to_excel(output_file, index=False)

print(f"Datei erfolgreich unter '{output_file}' gespeichert. Datensätze: {len(df_out)}")