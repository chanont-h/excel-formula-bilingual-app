
import streamlit as st
import sqlite3
from fuzzywuzzy import fuzz
import json

# โหลดภาษา
def load_lang(lang_code):
    with open(f"lang/lang_{lang_code}.json", "r", encoding="utf-8") as f:
        return json.load(f)

if "lang" not in st.session_state:
    st.session_state.lang = "en"

lang_choice = st.selectbox("🌐 Language / ภาษา", ["English", "ไทย"])
st.session_state.lang = "en" if lang_choice == "English" else "th"
lang_code = st.session_state.lang
lang = load_lang(lang_code)

st.title("🔍 Excel Formula Helper")
query = st.text_input(lang["search_placeholder"])

# DB
conn = sqlite3.connect("excel_functions_template.db")
cursor = conn.cursor()

def search_formula(query, lang="en"):
    col_name = "name_en" if lang == "en" else "name_th"
    sql = f"SELECT * FROM functions WHERE {col_name} LIKE ?"
    rows = cursor.execute(sql, (f"%{query}%",)).fetchall()
    col_idx = 1 if lang == "en" else 2
    return [row for row in rows if fuzz.partial_ratio(query.lower(), row[col_idx].lower()) > 70]

if query:
    results = search_formula(query, lang_code)
    if results:
        for r in results:
            name = r[1] if lang_code == "en" else r[2]
            desc = r[3] if lang_code == "en" else r[4]
            syntax = r[5] if lang_code == "en" else r[6]
            example = r[7] if lang_code == "en" else r[8]
            with st.expander(f"📌 {name}"):
                st.markdown(f"**📝 {lang['description']}**\n{desc}")
                st.code(syntax, language="excel")
                st.markdown(f"**💡 {lang['example']}**\n{example}")
    else:
        st.warning(lang["not_found"])
