
import pandas as pd
import json

df = pd.read_csv("Excel_Template_for_Editing.csv")
data = df.to_dict(orient="records")

with open("functions_en_th_completed.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("✅ JSON updated successfully.")
