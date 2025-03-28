
import streamlit as st
import json
from fuzzywuzzy import fuzz

# ===== Load Language =====
def load_lang(lang_code):
    with open(f"lang/lang_{lang_code}.json", "r", encoding="utf-8") as f:
        return json.load(f)

# ===== Load Data =====
with open("functions_en_th_completed.json", "r", encoding="utf-8") as f:
    functions = json.load(f)

if "lang" not in st.session_state:
    st.session_state.lang = "en"

lang_choice = st.selectbox("🌐 Language / ภาษา", ["English", "ไทย"])
st.session_state.lang = "en" if lang_choice == "English" else "th"
lang_code = st.session_state.lang
lang = load_lang(lang_code)

st.title("🔍 Excel Formula Helper (JSON Version)")
query = st.text_input(lang["search_placeholder"])

def search_formula(query, lang="en"):
    name_col = "name_en" if lang == "en" else "name_th"
    return [f for f in functions if fuzz.partial_ratio(query.lower(), f[name_col].lower()) > 70]

if query:
    results = search_formula(query, lang_code)
    if results:
        for r in results:
            name = r["name_en"] if lang_code == "en" else r["name_th"]
            desc = r["description_en"] if lang_code == "en" else r["description_th"]
            syntax = r["syntax_en"]
            example = r["example_en"]
            with st.expander(f"📌 {name}"):
                st.markdown(f"**📝 {lang['description']}**\n{desc}")
                st.code(syntax, language="excel")
                st.markdown(f"**💡 {lang['example']}**\n{example}")
                st.markdown(f"**📘 {lang['tutorial']}**")
                for i in range(1, 5):
                    tutorial = r.get(f"Tutorial_{i}", "")
                    if tutorial:
                        st.markdown(f"- {tutorial}")
    else:
        st.warning(lang["not_found"])
