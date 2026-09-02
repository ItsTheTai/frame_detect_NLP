import csv
import openpyxl

# 1. Pfade definieren
csv_file = 'Y_test_additional_dataset/datasets/raw-data/chinese_news_framing_dataset.csv'
gt_template_file = '/Users/Familie/Documents/Uni_Regensburg/A_Digital_Humanities/2SE_SS26/Natural_Language_Engineering/projekt/frame_detect_NLP/4_fine_tune_und_verbesserung/ground_truth_full.xlsx'
output_file = '/Users/Familie/Documents/Uni_Regensburg/A_Digital_Humanities/2SE_SS26/Natural_Language_Engineering/projekt/frame_detect_NLP/Y_test_additional_dataset/datasets/raw-data/ground_truth_chinese_extension_semeval.xlsx'

# 2. Excel-Header via openpyxl auslesen (ohne Pandas/NumPy C-Engine)
gt_wb = openpyxl.load_workbook(gt_template_file, read_only=True)
gt_sheet = gt_wb.active
target_columns = [cell.value for cell in next(gt_sheet.iter_rows(max_row=1))]
gt_wb.close()

# 3. Framing-Mapping definieren
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

# 4. CSV verarbeiten
records = []
with open(csv_file, mode='r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        # Standardmäßig alle Felder mit 0 initialisieren
        entry = {col: 0 for col in target_columns}
        entry['Filename'] = str(row['web_link'])
        entry['Language'] = 'chinese'
        
        frames_val = row.get('frames', '')
        if frames_val:
            active_tags = [tag.strip() for tag in str(frames_val).split(',')]
            for tag in active_tags:
                if tag in tag_mapping:
                    entry[tag_mapping[tag]] = 1
                    
        records.append(entry)

# 5. Neue Excel-Datei direkt mit openpyxl schreiben
wb_out = openpyxl.Workbook()
ws_out = wb_out.active
ws_out.title = "Sheet1"

# Kopfzeile schreiben
ws_out.append(target_columns)

# Datenzeilen schreiben
for rec in records:
    row_values = [rec[col] for col in target_columns]
    ws_out.append(row_values)

wb_out.save(output_file)

print(f"Erfolgreich konvertiert! {len(records)} Zeilen wurden in '{output_file}' gespeichert.")