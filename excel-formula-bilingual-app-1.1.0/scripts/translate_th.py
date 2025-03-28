
import sqlite3
import openai
import time
import os

openai.api_key = os.getenv("OPENAI_API_KEY")
conn = sqlite3.connect("excel_functions_template.db")
cursor = conn.cursor()

rows = cursor.execute("SELECT id, description_en FROM functions WHERE description_th IS NULL OR description_th = ''").fetchall()

for row in rows:
    id_, desc_en = row
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "คุณคือนักแปลเทคนิคจากอังกฤษเป็นไทย"},
                {"role": "user", "content": f"แปลคำอธิบายสูตร Excel นี้เป็นไทย:\n\n{desc_en}"}
            ]
        )
        desc_th = response["choices"][0]["message"]["content"].strip()
        cursor.execute("UPDATE functions SET description_th = ? WHERE id = ?", (desc_th, id_))
        conn.commit()
        print(f"✅ translated id {id_}")
        time.sleep(1.5)
    except Exception as e:
        print(f"❌ error at id {id_}: {e}")

conn.close()
