import os
import json
import pandas as pd

# Aktuellen Ordner als Input- und Output-Ordner verwenden
folder = os.path.dirname(os.path.abspath(__file__))

for filename in os.listdir(folder):
    if filename.endswith('.json'):
        json_path = os.path.join(folder, filename)
        csv_path = os.path.join(folder, f"{os.path.splitext(filename)[0]}.csv")

        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            df = pd.DataFrame(data) if isinstance(data, list) else pd.DataFrame([data])
            df.to_csv(csv_path, index=False, encoding='utf-8')
            print(f"✅ {filename} → {os.path.basename(csv_path)}")

        except Exception as e:
            print(f"❌ Fehler bei {filename}: {e}")